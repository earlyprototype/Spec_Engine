import chokidar, { FSWatcher } from 'chokidar';
import fs from 'fs-extra';
import path from 'path';
import { pathConfig } from '../config/paths';
import { EventEmitter } from 'events';

export interface ProgressUpdate {
  specId: string;
  dnaCode: string;
  descriptor: string;
  progress: any;
  timestamp: Date;
}

/**
 * Service for monitoring progress file changes
 * Uses chokidar to watch progress_*.json files and emit updates
 */
export class ProgressMonitorService extends EventEmitter {
  private watchers: Map<string, FSWatcher> = new Map();
  private watching: Set<string> = new Set();

  constructor() {
    super();
  }

  /**
   * Start monitoring a specific SPEC's progress file
   */
  public async startMonitoring(dnaCode: string, descriptor: string): Promise<void> {
    const watchKey = `${dnaCode}/${descriptor}`;
    
    if (this.watching.has(watchKey)) {
      console.log(`Already monitoring ${watchKey}`);
      return;
    }

    const progressPath = pathConfig.getProgressFilePath(dnaCode, descriptor);
    const progressDir = path.dirname(progressPath);

    try {
      // Ensure directory exists
      await fs.ensureDir(progressDir);

      // Create watcher for the specific progress file
      const watcher = chokidar.watch(progressPath, {
        persistent: true,
        ignoreInitial: false,
        awaitWriteFinish: {
          stabilityThreshold: 500,
          pollInterval: 100
        }
      });

      watcher
        .on('add', (filePath) => {
          console.log(`Progress file created: ${filePath}`);
          this.handleProgressChange(dnaCode, descriptor, filePath);
        })
        .on('change', (filePath) => {
          console.log(`Progress file changed: ${filePath}`);
          this.handleProgressChange(dnaCode, descriptor, filePath);
        })
        .on('error', (error) => {
          console.error(`Watcher error for ${watchKey}:`, error);
          this.emit('error', { dnaCode, descriptor, error });
        });

      this.watchers.set(watchKey, watcher);
      this.watching.add(watchKey);

      console.log(`Started monitoring progress for ${watchKey}`);
    } catch (error) {
      console.error(`Failed to start monitoring ${watchKey}:`, error);
      throw error;
    }
  }

  /**
   * Stop monitoring a specific SPEC's progress file
   */
  public async stopMonitoring(dnaCode: string, descriptor: string): Promise<void> {
    const watchKey = `${dnaCode}/${descriptor}`;
    
    const watcher = this.watchers.get(watchKey);
    if (watcher) {
      await watcher.close();
      this.watchers.delete(watchKey);
      this.watching.delete(watchKey);
      console.log(`Stopped monitoring progress for ${watchKey}`);
    }
  }

  /**
   * Stop all monitoring
   */
  public async stopAll(): Promise<void> {
    console.log(`Stopping all progress monitors (${this.watchers.size} active)`);
    
    for (const [key, watcher] of this.watchers) {
      await watcher.close();
    }
    
    this.watchers.clear();
    this.watching.clear();
  }

  /**
   * Handle progress file changes
   */
  private async handleProgressChange(
    dnaCode: string,
    descriptor: string,
    filePath: string
  ): Promise<void> {
    try {
      // Read and parse progress file
      const content = await fs.readFile(filePath, 'utf-8');
      const progress = JSON.parse(content);

      // Create update event
      const update: ProgressUpdate = {
        specId: `${dnaCode}/${descriptor}`,
        dnaCode,
        descriptor,
        progress,
        timestamp: new Date()
      };

      // Emit update event
      this.emit('progress-update', update);
    } catch (error) {
      console.error(`Error reading progress file ${filePath}:`, error);
      // Don't throw - file might be mid-write
    }
  }

  /**
   * Get current monitoring status
   */
  public getStatus(): { watching: string[]; count: number } {
    return {
      watching: Array.from(this.watching),
      count: this.watching.size
    };
  }

  /**
   * Check if monitoring a specific SPEC
   */
  public isMonitoring(dnaCode: string, descriptor: string): boolean {
    return this.watching.has(`${dnaCode}/${descriptor}`);
  }

  /**
   * Read current progress without setting up monitoring
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
      console.error(`Error reading progress for ${dnaCode}/${descriptor}:`, error);
      return null;
    }
  }
}

// Export singleton instance
export const progressMonitorService = new ProgressMonitorService();

// Cleanup on process exit
process.on('SIGINT', async () => {
  console.log('Shutting down progress monitors...');
  await progressMonitorService.stopAll();
  process.exit(0);
});

process.on('SIGTERM', async () => {
  console.log('Shutting down progress monitors...');
  await progressMonitorService.stopAll();
  process.exit(0);
});
