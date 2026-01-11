import fs from 'fs-extra';
import path from 'path';
import { pathConfig } from '../config/paths';
import TOML from '@iarna/toml';

export interface DnaProfileData {
  dnaCode: string;
  projectName: string;
  testing: string;
  risk: string;
  autonomy: string;
  customTools?: string;
  constraints?: string;
  filePath: string;
}

/**
 * Service for DNA profile file operations
 */
export class DnaFilesService {
  /**
   * Generate random DNA code (8 characters: A, T, G, C)
   */
  public generateDnaCode(): string {
    const bases = ['A', 'T', 'G', 'C'];
    let code = '';
    for (let i = 0; i < 8; i++) {
      code += bases[Math.floor(Math.random() * bases.length)];
    }
    return code;
  }

  /**
   * List all DNA profiles by scanning SPECs directory
   */
  public async listDnaProfiles(): Promise<DnaProfileData[]> {
    try {
      const specsPath = pathConfig.specsPath;
      
      if (!await fs.pathExists(specsPath)) {
        await fs.ensureDir(specsPath);
        return [];
      }

      const entries = await fs.readdir(specsPath, { withFileTypes: true });
      const profiles: DnaProfileData[] = [];

      for (const entry of entries) {
        if (entry.isDirectory() && this.isValidDnaCode(entry.name)) {
          const profilePath = path.join(specsPath, entry.name);
          const constitutionPath = path.join(profilePath, 'project_constitution.toml');
          
          if (await fs.pathExists(constitutionPath)) {
            try {
              const profile = await this.readDnaProfile(entry.name);
              if (profile) {
                profiles.push(profile);
              }
            } catch (error) {
              console.error(`Error reading DNA profile ${entry.name}:`, error);
            }
          }
        }
      }

      return profiles;
    } catch (error) {
      console.error('Error listing DNA profiles:', error);
      throw new Error('Failed to list DNA profiles');
    }
  }

  /**
   * Read a specific DNA profile
   */
  public async readDnaProfile(dnaCode: string): Promise<DnaProfileData | null> {
    try {
      const constitutionPath = pathConfig.getDnaConstitutionPath(dnaCode);
      
      if (!await fs.pathExists(constitutionPath)) {
        return null;
      }

      const content = await fs.readFile(constitutionPath, 'utf-8');
      const parsed = TOML.parse(content) as any;

      return {
        dnaCode,
        projectName: parsed.project?.name || parsed.metadata?.project_name || 'Unnamed Project',
        testing: parsed.preferences?.testing || 'standard',
        risk: parsed.preferences?.risk_tolerance || 'medium',
        autonomy: parsed.preferences?.autonomy_level || 'high',
        customTools: parsed.preferences?.custom_tools || '',
        constraints: parsed.constraints?.description || '',
        filePath: constitutionPath
      };
    } catch (error) {
      console.error(`Error reading DNA profile ${dnaCode}:`, error);
      return null;
    }
  }

  /**
   * Create a new DNA profile
   */
  public async writeDnaProfile(data: Omit<DnaProfileData, 'filePath'>): Promise<string> {
    try {
      const { dnaCode, projectName, testing, risk, autonomy, customTools, constraints } = data;
      
      // Create DNA directory
      const profilePath = pathConfig.getDnaProfilePath(dnaCode);
      await fs.ensureDir(profilePath);

      // Create project_constitution.toml
      const tomlContent = this.generateConstitutionToml({
        projectName,
        testing,
        risk,
        autonomy,
        customTools,
        constraints
      });

      const constitutionPath = pathConfig.getDnaConstitutionPath(dnaCode);
      await fs.writeFile(constitutionPath, tomlContent, 'utf-8');

      return constitutionPath;
    } catch (error) {
      console.error('Error writing DNA profile:', error);
      throw new Error('Failed to create DNA profile');
    }
  }

  /**
   * Update an existing DNA profile
   */
  public async updateDnaProfile(
    dnaCode: string,
    data: Partial<Omit<DnaProfileData, 'dnaCode' | 'filePath'>>
  ): Promise<void> {
    try {
      const existing = await this.readDnaProfile(dnaCode);
      if (!existing) {
        throw new Error(`DNA profile ${dnaCode} not found`);
      }

      // Merge with existing data
      const updated = {
        dnaCode,
        projectName: data.projectName || existing.projectName,
        testing: data.testing || existing.testing,
        risk: data.risk || existing.risk,
        autonomy: data.autonomy || existing.autonomy,
        customTools: data.customTools ?? existing.customTools,
        constraints: data.constraints ?? existing.constraints
      };

      // Write updated constitution
      await this.writeDnaProfile(updated);
    } catch (error) {
      console.error('Error updating DNA profile:', error);
      throw new Error('Failed to update DNA profile');
    }
  }

  /**
   * Delete a DNA profile (with confirmation required)
   */
  public async deleteDnaProfile(dnaCode: string): Promise<void> {
    try {
      const profilePath = pathConfig.getDnaProfilePath(dnaCode);
      
      if (await fs.pathExists(profilePath)) {
        // Move to trash instead of permanent delete (safer)
        const trashPath = path.join(pathConfig.specsPath, '.trash', dnaCode);
        await fs.ensureDir(path.dirname(trashPath));
        await fs.move(profilePath, trashPath, { overwrite: true });
      }
    } catch (error) {
      console.error('Error deleting DNA profile:', error);
      throw new Error('Failed to delete DNA profile');
    }
  }

  /**
   * Generate TOML content for project constitution
   */
  private generateConstitutionToml(data: {
    projectName: string;
    testing: string;
    risk: string;
    autonomy: string;
    customTools?: string;
    constraints?: string;
  }): string {
    const lines = [
      '# Project Constitution',
      `# Generated: ${new Date().toISOString()}`,
      '',
      '[metadata]',
      'version = "1.0"',
      `created_date = "${new Date().toISOString().split('T')[0]}"`,
      '',
      '[project]',
      `name = "${data.projectName}"`,
      'type = "general"',
      '',
      '[preferences]',
      `testing = "${data.testing}"`,
      `risk_tolerance = "${data.risk}"`,
      `autonomy_level = "${data.autonomy}"`
    ];

    if (data.customTools) {
      lines.push(`custom_tools = "${data.customTools}"`);
    }

    if (data.constraints) {
      lines.push('');
      lines.push('[constraints]');
      lines.push(`description = "${data.constraints}"`);
    }

    return lines.join('\n') + '\n';
  }

  /**
   * Validate DNA code format (8 characters: A, T, G, C)
   */
  private isValidDnaCode(code: string): boolean {
    return /^[ATGC]{8}$/.test(code);
  }

  /**
   * Check if DNA code already exists
   */
  public async dnaCodeExists(dnaCode: string): Promise<boolean> {
    const profilePath = pathConfig.getDnaProfilePath(dnaCode);
    return fs.pathExists(profilePath);
  }

  /**
   * Generate unique DNA code (not already in use)
   */
  public async generateUniqueDnaCode(): Promise<string> {
    let code: string;
    let attempts = 0;
    const maxAttempts = 100;

    do {
      code = this.generateDnaCode();
      attempts++;
      
      if (attempts > maxAttempts) {
        throw new Error('Failed to generate unique DNA code after 100 attempts');
      }
    } while (await this.dnaCodeExists(code));

    return code;
  }
}

export const dnaFilesService = new DnaFilesService();
