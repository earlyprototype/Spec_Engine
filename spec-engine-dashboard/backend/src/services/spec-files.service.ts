import fs from 'fs-extra';
import path from 'path';
import { pathConfig } from '../config/paths';
import TOML from '@iarna/toml';

export interface SpecMetadata {
  descriptor: string;
  dnaCode: string;
  goal: string;
  filePath: string;
  parametersPath: string;
  progressPath: string;
  exists: boolean;
}

/**
 * Service for SPEC file operations
 */
export class SpecFilesService {
  /**
   * List all SPECs across all DNA profiles
   */
  public async listSpecs(filters?: {
    dnaCode?: string;
    search?: string;
  }): Promise<SpecMetadata[]> {
    try {
      const specsPath = pathConfig.specsPath;
      
      if (!await fs.pathExists(specsPath)) {
        return [];
      }

      const specs: SpecMetadata[] = [];
      const entries = await fs.readdir(specsPath, { withFileTypes: true });

      for (const entry of entries) {
        if (entry.isDirectory() && this.isValidDnaCode(entry.name)) {
          // Skip if filtering by DNA code and doesn't match
          if (filters?.dnaCode && entry.name !== filters.dnaCode) {
            continue;
          }

          const dnaPath = path.join(specsPath, entry.name);
          const specDirs = await fs.readdir(dnaPath, { withFileTypes: true });

          for (const specDir of specDirs) {
            if (specDir.isDirectory() && specDir.name.startsWith('spec_')) {
              const descriptor = specDir.name.replace('spec_', '');
              const specMeta = await this.getSpecMetadata(entry.name, descriptor);
              
              if (specMeta) {
                // Apply search filter
                if (filters?.search) {
                  const searchLower = filters.search.toLowerCase();
                  if (
                    !descriptor.toLowerCase().includes(searchLower) &&
                    !specMeta.goal.toLowerCase().includes(searchLower)
                  ) {
                    continue;
                  }
                }
                
                specs.push(specMeta);
              }
            }
          }
        }
      }

      return specs;
    } catch (error) {
      console.error('Error listing SPECs:', error);
      throw new Error('Failed to list SPECs');
    }
  }

  /**
   * Get metadata for a specific SPEC
   */
  public async getSpecMetadata(dnaCode: string, descriptor: string): Promise<SpecMetadata | null> {
    try {
      const specDirPath = path.join(pathConfig.specsPath, dnaCode, `spec_${descriptor}`);
      
      // Check if SPEC directory exists
      if (!await fs.pathExists(specDirPath)) {
        return null;
      }
      
      const specFilePath = pathConfig.getSpecFilePath(dnaCode, descriptor);
      const parametersPath = pathConfig.getParametersFilePath(dnaCode, descriptor);
      const progressPath = pathConfig.getProgressFilePath(dnaCode, descriptor);
      
      const exists = await fs.pathExists(specFilePath);
      
      let goal = '';
      if (exists) {
        // Try to extract goal from spec file
        try {
          const content = await fs.readFile(specFilePath, 'utf-8');
          const goalMatch = content.match(/##\s+Goal\s*\n\s*(.+)/i);
          if (goalMatch) {
            goal = goalMatch[1].trim();
          }
        } catch (error) {
          console.error(`Error reading spec file ${specFilePath}:`, error);
        }
      } else {
        // If main spec file doesn't exist, try to get goal from README or other sources
        try {
          const readmePath = path.join(specDirPath, 'README.md');
          if (await fs.pathExists(readmePath)) {
            const content = await fs.readFile(readmePath, 'utf-8');
            const goalMatch = content.match(/##\s+(?:Project Overview|Goal)\s*\n\s*(?:This project creates |)?(.+)/i);
            if (goalMatch) {
              goal = goalMatch[1].trim().replace(/\*\*/g, '');
            }
          }
        } catch (error) {
          console.error(`Error reading README for ${dnaCode}/${descriptor}:`, error);
        }
      }

      console.log(`[SPEC] Found SPEC ${dnaCode}/${descriptor} - Goal: "${goal}"`);
      return {
        descriptor,
        dnaCode,
        goal: goal || `SPEC: ${descriptor}`,
        filePath: specFilePath,
        parametersPath,
        progressPath,
        exists
      };
    } catch (error) {
      console.error(`Error getting SPEC metadata for ${dnaCode}/${descriptor}:`, error);
      return null;
    }
  }

  /**
   * Read SPEC markdown file content
   */
  public async readSpec(dnaCode: string, descriptor: string): Promise<string | null> {
    try {
      const specFilePath = pathConfig.getSpecFilePath(dnaCode, descriptor);
      
      if (!await fs.pathExists(specFilePath)) {
        return null;
      }

      return await fs.readFile(specFilePath, 'utf-8');
    } catch (error) {
      console.error(`Error reading SPEC ${dnaCode}/${descriptor}:`, error);
      return null;
    }
  }

  /**
   * Read parameters TOML file content
   */
  public async readParameters(dnaCode: string, descriptor: string): Promise<string | null> {
    try {
      const parametersPath = pathConfig.getParametersFilePath(dnaCode, descriptor);
      
      if (!await fs.pathExists(parametersPath)) {
        return null;
      }

      return await fs.readFile(parametersPath, 'utf-8');
    } catch (error) {
      console.error(`Error reading parameters ${dnaCode}/${descriptor}:`, error);
      return null;
    }
  }

  /**
   * Write parameters TOML file with automatic backup
   */
  public async writeParameters(
    dnaCode: string,
    descriptor: string,
    content: string
  ): Promise<{ success: boolean; backupPath?: string; error?: string }> {
    try {
      const parametersPath = pathConfig.getParametersFilePath(dnaCode, descriptor);
      
      // Validate TOML syntax before writing
      try {
        TOML.parse(content);
      } catch (error: any) {
        return {
          success: false,
          error: `Invalid TOML syntax: ${error.message}`
        };
      }

      // Create backup if file exists
      let backupPath: string | undefined;
      if (await fs.pathExists(parametersPath)) {
        const backupDir = pathConfig.getBackupPath(dnaCode, descriptor);
        await fs.ensureDir(backupDir);
        
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        backupPath = path.join(backupDir, `parameters_${descriptor}_${timestamp}.toml`);
        
        await fs.copy(parametersPath, backupPath);
      }

      // Write new content
      await fs.writeFile(parametersPath, content, 'utf-8');

      return {
        success: true,
        backupPath
      };
    } catch (error: any) {
      console.error(`Error writing parameters ${dnaCode}/${descriptor}:`, error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Read progress JSON file
   */
  public async readProgress(dnaCode: string, descriptor: string): Promise<any | null> {
    try {
      const progressPath = pathConfig.getProgressFilePath(dnaCode, descriptor);
      
      if (!await fs.pathExists(progressPath)) {
        return null;
      }

      const content = await fs.readFile(progressPath, 'utf-8');
      return JSON.parse(content);
    } catch (error) {
      console.error(`Error reading progress ${dnaCode}/${descriptor}:`, error);
      return null;
    }
  }

  /**
   * Create a new SPEC from template (simplified)
   */
  public async createSpec(data: {
    dnaCode: string;
    descriptor: string;
    goal: string;
    tasks?: string[];
  }): Promise<{ success: boolean; error?: string }> {
    try {
      const { dnaCode, descriptor, goal, tasks = [] } = data;
      const specPath = pathConfig.getSpecPath(dnaCode, descriptor);
      
      // Check if SPEC already exists
      if (await fs.pathExists(specPath)) {
        return {
          success: false,
          error: 'SPEC already exists with this descriptor'
        };
      }

      // Create SPEC directory
      await fs.ensureDir(specPath);

      // Generate basic spec.md content
      const specContent = this.generateSpecMarkdown(descriptor, goal, tasks);
      await fs.writeFile(
        pathConfig.getSpecFilePath(dnaCode, descriptor),
        specContent,
        'utf-8'
      );

      // Generate basic parameters.toml content
      const paramsContent = this.generateParametersToml(descriptor, goal, tasks);
      await fs.writeFile(
        pathConfig.getParametersFilePath(dnaCode, descriptor),
        paramsContent,
        'utf-8'
      );

      return { success: true };
    } catch (error: any) {
      console.error('Error creating SPEC:', error);
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Generate basic spec markdown content
   */
  private generateSpecMarkdown(descriptor: string, goal: string, tasks: string[]): string {
    const lines = [
      `# ${descriptor.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}`,
      '',
      `**Version:** 1.0`,
      `**Created:** ${new Date().toISOString().split('T')[0]}`,
      `**Purpose:** ${goal}`,
      '',
      '---',
      '',
      '## Goal',
      '',
      goal,
      '',
      '---',
      '',
      '## Definition of Complete',
      '',
      '- [ ] Primary deliverable exists',
      '- [ ] Quality standards met',
      '- [ ] Verification method passed',
      '',
      '---',
      '',
      '## Tasks',
      ''
    ];

    tasks.forEach((task, index) => {
      lines.push(`### Task [${index + 1}]: ${task}`);
      lines.push('');
      lines.push('- **Step [1]:** TODO');
      lines.push('  - **Primary method:** TODO');
      lines.push('  - **Expected output:** TODO');
      lines.push('  - **Critical:** true');
      lines.push('');
    });

    return lines.join('\n');
  }

  /**
   * Generate basic parameters TOML content
   */
  private generateParametersToml(descriptor: string, goal: string, tasks: string[]): string {
    const lines = [
      `# ${descriptor} - Parameters`,
      `# Generated: ${new Date().toISOString()}`,
      '',
      '[metadata]',
      'spec_version = "1.0"',
      `created_date = "${new Date().toISOString().split('T')[0]}"`,
      `descriptor = "${descriptor}"`,
      '',
      '[goal]',
      `statement = "${goal}"`,
      'singular = true',
      '',
      '[definition_of_complete]',
      'primary_deliverable = "TODO"',
      'quality_standards = ["TODO"]',
      'verification_method = "TODO"',
      ''
    ];

    tasks.forEach((task, index) => {
      lines.push('[[tasks]]');
      lines.push(`id = ${index + 1}`);
      lines.push(`name = "${task}"`);
      lines.push('purpose = "TODO"');
      lines.push('');
    });

    return lines.join('\n');
  }

  /**
   * Validate DNA code format
   */
  private isValidDnaCode(code: string): boolean {
    return /^[ATGC]{8}$/.test(code);
  }

  /**
   * Parse SPEC structure from markdown
   */
  public async parseSpecStructure(dnaCode: string, descriptor: string): Promise<any> {
    try {
      const content = await this.readSpec(dnaCode, descriptor);
      if (!content) return null;

      // Extract tasks
      const tasks: any[] = [];
      const taskMatches = content.matchAll(/###\s+Task\s+\[(\d+)\]:\s+(.+)/g);
      
      for (const match of taskMatches) {
        const taskId = parseInt(match[1]);
        const taskName = match[2].trim();
        tasks.push({ id: taskId, name: taskName });
      }

      return { tasks };
    } catch (error) {
      console.error('Error parsing SPEC structure:', error);
      return null;
    }
  }
}

export const specFilesService = new SpecFilesService();
