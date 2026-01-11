import { Router, Request, Response } from 'express';
import { specFilesService } from '../services/spec-files.service';
import { dbService } from '../services/database.service';

const router = Router();

// GET /api/specs - List all SPECs
router.get('/', async (req: Request, res: Response) => {
  try {
    const { dnaCode, status, search } = req.query;
    
    const filters: any = {};
    if (dnaCode) filters.dnaCode = dnaCode as string;
    if (status) filters.status = status as string;
    if (search) filters.search = search as string;
    
    const specs = await specFilesService.listSpecs(filters);
    
    console.log(`[SPECS] Found ${specs.length} SPECs:`, specs);
    res.json({ specs });
  } catch (error: any) {
    console.error('Error listing SPECs:', error);
    res.status(500).json({ error: 'Failed to fetch SPECs', message: error.message });
  }
});

// GET /api/specs/:dnaCode/:descriptor - Get specific SPEC details
router.get('/:dnaCode/:descriptor', async (req: Request, res: Response) => {
  try {
    const { dnaCode, descriptor } = req.params;
    
    const metadata = await specFilesService.getSpecMetadata(dnaCode, descriptor);
    if (!metadata) {
      return res.status(404).json({ error: 'SPEC not found' });
    }
    
    const content = await specFilesService.readSpec(dnaCode, descriptor);
    const structure = await specFilesService.parseSpecStructure(dnaCode, descriptor);
    
    console.log(`[SPECS] Returning SPEC ${dnaCode}/${descriptor}:`, metadata);
    res.json({ ...metadata, content, structure });
  } catch (error: any) {
    console.error('Error fetching SPEC:', error);
    res.status(500).json({ error: 'Failed to fetch SPEC', message: error.message });
  }
});

// POST /api/specs - Create new SPEC
router.post('/', async (req: Request, res: Response) => {
  try {
    const { dnaCode, descriptor, goal, tasks } = req.body;
    
    if (!dnaCode || !descriptor || !goal) {
      return res.status(400).json({ error: 'Missing required fields: dnaCode, descriptor, goal' });
    }
    
    const result = await specFilesService.createSpec({ dnaCode, descriptor, goal, tasks });
    
    if (!result.success) {
      return res.status(400).json({ error: result.error });
    }
    
    const dbSpec = await dbService.createSpec({
      descriptor,
      dnaCode,
      goal,
      filePath: `SPECs/${dnaCode}/spec_${descriptor}/`,
    });
    
    res.status(201).json({ message: 'SPEC created successfully', spec: dbSpec });
  } catch (error: any) {
    console.error('Error creating SPEC:', error);
    res.status(500).json({ error: 'Failed to create SPEC', message: error.message });
  }
});

// GET /api/specs/:dnaCode/:descriptor/parameters - Get SPEC parameters file
router.get('/:dnaCode/:descriptor/parameters', async (req: Request, res: Response) => {
  try {
    const { dnaCode, descriptor } = req.params;
    
    const content = await specFilesService.readParameters(dnaCode, descriptor);
    
    if (!content) {
      return res.status(404).json({ error: 'Parameters file not found' });
    }
    
    console.log(`[SPECS] Returning parameters for ${dnaCode}/${descriptor}`);
    res.json({ content });
  } catch (error: any) {
    console.error('Error fetching parameters:', error);
    res.status(500).json({ error: 'Failed to fetch parameters', message: error.message });
  }
});

// PUT /api/specs/:dnaCode/:descriptor/parameters - Update SPEC parameters file
router.put('/:dnaCode/:descriptor/parameters', async (req: Request, res: Response) => {
  try {
    const { dnaCode, descriptor } = req.params;
    const { content } = req.body;
    
    const result = await specFilesService.writeParameters(dnaCode, descriptor, content);
    
    if (!result.success) {
      return res.status(400).json({ error: result.error });
    }
    
    console.log(`[SPECS] Updated parameters for ${dnaCode}/${descriptor}`);
    res.json({ 
      message: 'Parameters updated successfully', 
      backupPath: result.backupPath 
    });
  } catch (error: any) {
    console.error('Error updating parameters:', error);
    res.status(500).json({ error: 'Failed to update parameters', message: error.message });
  }
});

export default router;
