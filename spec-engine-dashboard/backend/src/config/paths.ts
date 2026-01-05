import path from 'path';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

/**
 * Path configuration for SPEC Engine integration
 * Reads paths from environment variables or uses defaults
 */
export class PathConfig {
  private static instance: PathConfig;
  
  public readonly specEnginePath: string;
  public readonly specsPath: string;
  public readonly constitutionPath: string;
  public readonly templatesPath: string;
  public readonly dnaPath: string;

  private constructor() {
    // SPEC Engine root path
    this.specEnginePath = process.env.SPEC_ENGINE_PATH || 
      path.join(process.cwd(), '../../__SPEC_Engine');
    
    // SPECs root path
    this.specsPath = process.env.SPECS_PATH || 
      path.join(process.cwd(), '../../SPECs');
    
    // Derived paths
    this.constitutionPath = path.join(this.specEnginePath, '_Constitution');
    this.templatesPath = path.join(this.specEnginePath, '_templates');
    this.dnaPath = path.join(this.specEnginePath, '_DNA');
  }

  public static getInstance(): PathConfig {
    if (!PathConfig.instance) {
      PathConfig.instance = new PathConfig();
    }
    return PathConfig.instance;
  }

  /**
   * Get path to DNA profile directory
   */
  public getDnaProfilePath(dnaCode: string): string {
    return path.join(this.specsPath, dnaCode);
  }

  /**
   * Get path to DNA profile constitution file
   */
  public getDnaConstitutionPath(dnaCode: string): string {
    return path.join(this.getDnaProfilePath(dnaCode), 'project_constitution.toml');
  }

  /**
   * Get path to SPEC directory
   */
  public getSpecPath(dnaCode: string, descriptor: string): string {
    return path.join(this.specsPath, dnaCode, `spec_${descriptor}`);
  }

  /**
   * Get path to spec markdown file
   */
  public getSpecFilePath(dnaCode: string, descriptor: string): string {
    return path.join(this.getSpecPath(dnaCode, descriptor), `spec_${descriptor}.md`);
  }

  /**
   * Get path to parameters TOML file
   */
  public getParametersFilePath(dnaCode: string, descriptor: string): string {
    return path.join(this.getSpecPath(dnaCode, descriptor), `parameters_${descriptor}.toml`);
  }

  /**
   * Get path to executor markdown file
   */
  public getExecutorFilePath(dnaCode: string, descriptor: string): string {
    return path.join(this.getSpecPath(dnaCode, descriptor), `exe_${descriptor}.md`);
  }

  /**
   * Get path to progress JSON file
   */
  public getProgressFilePath(dnaCode: string, descriptor: string): string {
    return path.join(this.getSpecPath(dnaCode, descriptor), `progress_${descriptor}.json`);
  }

  /**
   * Get backup directory for parameter files
   */
  public getBackupPath(dnaCode: string, descriptor: string): string {
    return path.join(this.getSpecPath(dnaCode, descriptor), '.backups');
  }

  /**
   * Validate that paths exist and are accessible
   */
  public validatePaths(): { valid: boolean; errors: string[] } {
    const errors: string[] = [];
    const fs = require('fs');

    if (!fs.existsSync(this.specEnginePath)) {
      errors.push(`SPEC Engine path not found: ${this.specEnginePath}`);
    }

    if (!fs.existsSync(this.specsPath)) {
      errors.push(`SPECs path not found: ${this.specsPath}`);
    }

    return {
      valid: errors.length === 0,
      errors
    };
  }

  /**
   * Get all paths for logging/debugging
   */
  public getAllPaths() {
    return {
      specEnginePath: this.specEnginePath,
      specsPath: this.specsPath,
      constitutionPath: this.constitutionPath,
      templatesPath: this.templatesPath,
      dnaPath: this.dnaPath
    };
  }
}

// Export singleton instance
export const pathConfig = PathConfig.getInstance();
