import { spawn, ChildProcess } from 'child_process';
import { pathConfig } from '../config/paths';
import { dbService } from './database.service';
import { progressMonitorService } from './progress-monitor.service';
import { io } from '../server';

interface ExecutionProcess {
  executionId: string;
  specId: string;
  process: ChildProcess;
  startedAt: Date;
}

/**
 * Service for managing SPEC executions
 * Spawns child processes for exe_*.md files and monitors progress
 */
export class ExecutionService {
  private activeExecutions: Map<string, ExecutionProcess> = new Map();

  /**
   * Start a new SPEC execution
   */
  public async startExecution(
    dnaCode: string,
    descriptor: string,
    mode: string
  ): Promise<{ executionId: string; error?: string }> {
    try {
      const specId = `${dnaCode}/${descriptor}`;
      
      // Check if already running
      if (this.activeExecutions.has(specId)) {
        return {
          executionId: '',
          error: 'SPEC is already executing'
        };
      }

      // Get SPEC metadata from database
      const specs = await dbService.listSpecs({ dnaCode });
      const spec = specs.find(s => s.descriptor === descriptor);
      
      if (!spec) {
        return {
          executionId: '',
          error: 'SPEC not found in database'
        };
      }

      // Create execution record
      const execution = await dbService.createExecution({
        specId: spec.id,
        mode: mode,
      });

      const executionId = execution.id;

      // Start progress monitoring
      await progressMonitorService.startMonitoring(dnaCode, descriptor);

      // Set up progress update listener
      const progressHandler = (update: any) => {
        if (update.dnaCode === dnaCode && update.descriptor === descriptor) {
          // Broadcast to WebSocket clients
          io.to(`progress-${specId}`).emit('progress-update', update.progress);
          
          // Update database
          this.updateExecutionProgress(executionId, update.progress);
        }
      };

      progressMonitorService.on('progress-update', progressHandler);

      // Note: In a real implementation, we would spawn a child process here
      // that runs the exe_*.md file with the LLM. For now, we simulate execution.
      // The actual spawning depends on how the LLM executor is invoked in your setup.
      
      // Example (commented - needs actual LLM invocation method):
      /*
      const exePath = pathConfig.getExecutorFilePath(dnaCode, descriptor);
      const childProcess = spawn('node', [exePath], {
        cwd: pathConfig.getSpecPath(dnaCode, descriptor),
        env: { ...process.env, EXECUTION_MODE: mode }
      });
      
      childProcess.stdout?.on('data', (data) => {
        console.log(`Execution ${executionId}: ${data}`);
      });
      
      childProcess.on('exit', async (code) => {
        await this.handleExecutionComplete(executionId, code === 0 ? 'completed' : 'failed');
      });
      */

      // Store execution process info
      this.activeExecutions.set(specId, {
        executionId,
        specId,
        process: null as any, // Would store actual ChildProcess
        startedAt: new Date(),
      });

      // Update execution status
      await dbService.updateExecution(executionId, {
        status: 'running',
      });

      console.log(`Started execution ${executionId} for ${specId} in ${mode} mode`);

      return { executionId };
    } catch (error: any) {
      console.error('Error starting execution:', error);
      return {
        executionId: '',
        error: error.message
      };
    }
  }

  /**
   * Stop a running execution
   */
  public async stopExecution(executionId: string): Promise<{ success: boolean; error?: string }> {
    try {
      // Find the execution
      let specId: string | null = null;
      for (const [sid, proc] of this.activeExecutions) {
        if (proc.executionId === executionId) {
          specId = sid;
          break;
        }
      }

      if (!specId) {
        return { success: false, error: 'Execution not found or already stopped' };
      }

      const proc = this.activeExecutions.get(specId);
      if (proc?.process) {
        proc.process.kill('SIGTERM');
      }

      this.activeExecutions.delete(specId);

      // Stop progress monitoring
      const [dnaCode, descriptor] = specId.split('/');
      await progressMonitorService.stopMonitoring(dnaCode, descriptor);

      // Update database
      await dbService.updateExecution(executionId, {
        status: 'failed',
        completedAt: new Date(),
        errorMessage: 'Stopped by user',
      });

      return { success: true };
    } catch (error: any) {
      console.error('Error stopping execution:', error);
      return { success: false, error: error.message };
    }
  }

  /**
   * Get execution status
   */
  public async getExecutionStatus(executionId: string): Promise<any> {
    try {
      const execution = await dbService.getExecution(executionId);
      return execution;
    } catch (error: any) {
      console.error('Error getting execution status:', error);
      return null;
    }
  }

  /**
   * Update execution progress in database
   */
  private async updateExecutionProgress(executionId: string, progress: any): Promise<void> {
    try {
      // Extract status from progress
      const status = progress.status || 'running';
      const goalStatus = progress.goal_achievement_status;
      
      const updates: any = { status };
      
      if (goalStatus) {
        updates.goalStatus = goalStatus;
      }
      
      if (status === 'completed' || status === 'failed') {
        updates.completedAt = new Date();
        const execution = await dbService.getExecution(executionId);
        if (execution) {
          const duration = new Date().getTime() - new Date(execution.startedAt).getTime();
          updates.duration = duration;
        }
      }

      await dbService.updateExecution(executionId, updates);

      // Log progress if task/step info available
      if (progress.current_task || progress.current_step) {
        await dbService.createProgressLog({
          executionId,
          taskId: progress.current_task?.toString(),
          stepId: progress.current_step?.toString(),
          status: progress.step_status || 'unknown',
          method: progress.method_used || 'primary',
        });
      }
    } catch (error) {
      console.error('Error updating execution progress:', error);
    }
  }

  /**
   * Handle execution completion
   */
  private async handleExecutionComplete(executionId: string, status: string): Promise<void> {
    try {
      await dbService.updateExecution(executionId, {
        status,
        completedAt: new Date(),
      });

      // Remove from active executions
      for (const [specId, proc] of this.activeExecutions) {
        if (proc.executionId === executionId) {
          this.activeExecutions.delete(specId);
          const [dnaCode, descriptor] = specId.split('/');
          await progressMonitorService.stopMonitoring(dnaCode, descriptor);
          break;
        }
      }
    } catch (error) {
      console.error('Error handling execution completion:', error);
    }
  }

  /**
   * Get all active executions
   */
  public getActiveExecutions(): string[] {
    return Array.from(this.activeExecutions.keys());
  }

  /**
   * Check if a SPEC is currently executing
   */
  public isExecuting(specId: string): boolean {
    return this.activeExecutions.has(specId);
  }
}

export const executionService = new ExecutionService();
