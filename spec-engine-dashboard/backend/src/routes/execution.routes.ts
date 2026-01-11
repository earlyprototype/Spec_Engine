import { Router, Request, Response } from 'express';
import { executionService } from '../services/execution.service';
import { dbService } from '../services/database.service';
import { specFilesService } from '../services/spec-files.service';

const router = Router();

// GET /api/executions - List all executions
router.get('/', async (req: Request, res: Response) => {
  try {
    const { specId, status } = req.query;
    
    const filters: any = {};
    if (specId) filters.specId = specId as string;
    if (status) filters.status = status as string;
    
    const executions = await dbService.listExecutions(filters);
    
    res.json({ executions });
  } catch (error: any) {
    console.error('Error listing executions:', error);
    res.status(500).json({ error: 'Failed to fetch executions', message: error.message });
  }
});

// GET /api/executions/:executionId - Get execution details
router.get('/:executionId', async (req: Request, res: Response) => {
  try {
    const { executionId } = req.params;
    
    const execution = await executionService.getExecutionStatus(executionId);
    
    if (!execution) {
      return res.status(404).json({ error: 'Execution not found' });
    }
    
    res.json({ execution });
  } catch (error: any) {
    console.error('Error fetching execution:', error);
    res.status(500).json({ error: 'Failed to fetch execution', message: error.message });
  }
});

// POST /api/executions - Start new execution
router.post('/', async (req: Request, res: Response) => {
  try {
    const { specId, mode } = req.body;
    
    if (!specId || !mode) {
      return res.status(400).json({ 
        error: 'Missing required fields: specId, mode' 
      });
    }
    
    const [dnaCode, descriptor] = specId.split('/');
    
    // Validate mode
    const validModes = ['silent', 'dynamic', 'collaborative'];
    if (!validModes.includes(mode)) {
      return res.status(400).json({ 
        error: `Invalid mode. Must be one of: ${validModes.join(', ')}` 
      });
    }
    
    // Start execution
    const result = await executionService.startExecution(dnaCode, descriptor, mode);
    
    if (result.error) {
      return res.status(400).json({ error: result.error });
    }
    
    res.status(201).json({ 
      message: 'Execution started',
      execution: {
        executionId: result.executionId,
        specId,
        mode
      }
    });
  } catch (error: any) {
    console.error('Error starting execution:', error);
    res.status(500).json({ error: 'Failed to start execution', message: error.message });
  }
});

// POST /api/executions/:executionId/stop - Stop execution
router.post('/:executionId/stop', async (req: Request, res: Response) => {
  try {
    const { executionId } = req.params;
    
    const result = await executionService.stopExecution(executionId);
    
    if (!result.success) {
      return res.status(400).json({ error: result.error });
    }
    
    res.json({ message: 'Execution stopped', executionId });
  } catch (error: any) {
    console.error('Error stopping execution:', error);
    res.status(500).json({ error: 'Failed to stop execution', message: error.message });
  }
});

// GET /api/executions/:executionId/results - Get execution results
router.get('/:executionId/results', async (req: Request, res: Response) => {
  try {
    const { executionId } = req.params;
    
    const execution = await dbService.getExecution(executionId);
    
    if (!execution || !execution.spec) {
      return res.status(404).json({ error: 'Execution or SPEC not found' });
    }
    
    // Read progress file for detailed results
    const progress = await specFilesService.readProgress(
      execution.spec.dnaCode, 
      execution.spec.descriptor
    );
    
    res.json({ 
      execution,
      progress,
      goalStatus: execution.goalStatus || progress?.goal_achievement_status,
      completionVerification: progress?.completion_verification,
      postExecutionAnalysis: progress?.post_execution_analysis,
    });
  } catch (error: any) {
    console.error('Error fetching results:', error);
    res.status(500).json({ error: 'Failed to fetch results', message: error.message });
  }
});

// GET /api/executions/:executionId/logs - Get execution logs
router.get('/:executionId/logs', async (req: Request, res: Response) => {
  try {
    const { executionId } = req.params;
    
    const logs = await dbService.getProgressLogs(executionId);
    
    res.json({ logs });
  } catch (error: any) {
    console.error('Error fetching logs:', error);
    res.status(500).json({ error: 'Failed to fetch logs', message: error.message });
  }
});

export default router;
