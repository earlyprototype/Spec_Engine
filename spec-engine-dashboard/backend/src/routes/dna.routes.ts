import { Router, Request, Response } from 'express';
import { dnaFilesService } from '../services/dna-files.service';
import { dbService } from '../services/database.service';

const router = Router();

// GET /api/dna - List all DNA profiles
router.get('/', async (req: Request, res: Response) => {
  try {
    // Get DNA profiles from file system
    const profiles = await dnaFilesService.listDnaProfiles();
    
    // Sync with database (get additional metadata like spec count)
    const enrichedProfiles = await Promise.all(
      profiles.map(async (profile) => {
        // Try to get from database for additional info
        let dbProfile = await dbService.getDnaProfile(profile.dnaCode);
        
        // If not in database, create it
        if (!dbProfile) {
          dbProfile = await dbService.createDnaProfile({
            dnaCode: profile.dnaCode,
            projectName: profile.projectName,
            testing: profile.testing,
            risk: profile.risk,
            autonomy: profile.autonomy,
            customTools: profile.customTools,
            constraints: profile.constraints,
          });
        }
        
        return {
          ...profile,
          id: dbProfile.id,
          createdAt: dbProfile.createdAt,
          updatedAt: dbProfile.updatedAt,
          specCount: dbProfile.specs?.length || 0,
        };
      })
    );
    
    console.log(`[DNA] Returning ${enrichedProfiles.length} profiles:`, enrichedProfiles);
    res.json({ profiles: enrichedProfiles });
  } catch (error: any) {
    console.error('Error listing DNA profiles:', error);
    res.status(500).json({ 
      error: 'Failed to fetch DNA profiles',
      message: error.message 
    });
  }
});

// GET /api/dna/:dnaCode - Get specific DNA profile
router.get('/:dnaCode', async (req: Request, res: Response) => {
  try {
    const { dnaCode } = req.params;
    
    // Get from file system
    const profile = await dnaFilesService.readDnaProfile(dnaCode);
    
    if (!profile) {
      return res.status(404).json({ 
        error: 'DNA profile not found',
        dnaCode 
      });
    }
    
    // Get database info
    const dbProfile = await dbService.getDnaProfile(dnaCode);
    
    const fullProfile = {
      ...profile,
      id: dbProfile?.id,
      specs: dbProfile?.specs || [],
      createdAt: dbProfile?.createdAt,
      updatedAt: dbProfile?.updatedAt,
    };
    
    console.log(`[DNA] Returning single profile:`, fullProfile);
    res.json({ profile: fullProfile }); // Wrap in profile object
  } catch (error: any) {
    console.error('Error fetching DNA profile:', error);
    res.status(500).json({ 
      error: 'Failed to fetch DNA profile',
      message: error.message 
    });
  }
});

// POST /api/dna - Create new DNA profile
router.post('/', async (req: Request, res: Response) => {
  try {
    const { projectName, testing, risk, autonomy, customTools, constraints } = req.body;
    
    // Validate required fields
    if (!projectName || !testing || !risk || !autonomy) {
      return res.status(400).json({ 
        error: 'Missing required fields',
        required: ['projectName', 'testing', 'risk', 'autonomy']
      });
    }
    
    // Generate unique DNA code
    const dnaCode = await dnaFilesService.generateUniqueDnaCode();
    
    // Create file system profile
    const filePath = await dnaFilesService.writeDnaProfile({
      dnaCode,
      projectName,
      testing,
      risk,
      autonomy,
      customTools,
      constraints,
    });
    
    // Create database record
    const dbProfile = await dbService.createDnaProfile({
      dnaCode,
      projectName,
      testing,
      risk,
      autonomy,
      customTools,
      constraints,
    });
    
    res.status(201).json({ 
      message: 'DNA profile created successfully',
      profile: {
        ...dbProfile,
        filePath,
      }
    });
  } catch (error: any) {
    console.error('Error creating DNA profile:', error);
    res.status(500).json({ 
      error: 'Failed to create DNA profile',
      message: error.message 
    });
  }
});

// PUT /api/dna/:dnaCode - Update DNA profile
router.put('/:dnaCode', async (req: Request, res: Response) => {
  try {
    const { dnaCode } = req.params;
    const { projectName, testing, risk, autonomy, customTools, constraints } = req.body;
    
    // Check if profile exists
    const existing = await dnaFilesService.readDnaProfile(dnaCode);
    if (!existing) {
      return res.status(404).json({ 
        error: 'DNA profile not found',
        dnaCode 
      });
    }
    
    // Update file system
    await dnaFilesService.updateDnaProfile(dnaCode, {
      projectName,
      testing,
      risk,
      autonomy,
      customTools,
      constraints,
    });
    
    // Update database
    const dbProfile = await dbService.updateDnaProfile(dnaCode, {
      projectName,
      testing,
      risk,
      autonomy,
      customTools,
      constraints,
    });
    
    console.log(`[DNA] Updated profile:`, dbProfile);
    res.json({ 
      message: 'DNA profile updated successfully',
      profile: dbProfile
    });
  } catch (error: any) {
    console.error('Error updating DNA profile:', error);
    res.status(500).json({ 
      error: 'Failed to update DNA profile',
      message: error.message 
    });
  }
});

// DELETE /api/dna/:dnaCode - Delete DNA profile
router.delete('/:dnaCode', async (req: Request, res: Response) => {
  try {
    const { dnaCode } = req.params;
    
    // Check if profile exists
    const existing = await dnaFilesService.readDnaProfile(dnaCode);
    if (!existing) {
      return res.status(404).json({ 
        error: 'DNA profile not found',
        dnaCode 
      });
    }
    
    // Delete from file system (moves to .trash)
    await dnaFilesService.deleteDnaProfile(dnaCode);
    
    // Delete from database (cascade deletes specs and executions)
    await dbService.deleteDnaProfile(dnaCode);
    
    res.json({ 
      message: 'DNA profile deleted successfully (moved to .trash)',
      dnaCode
    });
  } catch (error: any) {
    console.error('Error deleting DNA profile:', error);
    res.status(500).json({ 
      error: 'Failed to delete DNA profile',
      message: error.message 
    });
  }
});

export default router;
