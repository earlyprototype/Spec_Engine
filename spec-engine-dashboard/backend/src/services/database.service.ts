import { PrismaClient } from '@prisma/client';

// Create Prisma client instance
const prisma = new PrismaClient({
  log: process.env.NODE_ENV === 'development' ? ['query', 'error', 'warn'] : ['error'],
});

// Handle disconnection on app termination
process.on('beforeExit', async () => {
  await prisma.$disconnect();
});

// Database service with helper methods
export class DatabaseService {
  private static instance: DatabaseService;
  private client: PrismaClient;

  private constructor() {
    this.client = prisma;
  }

  public static getInstance(): DatabaseService {
    if (!DatabaseService.instance) {
      DatabaseService.instance = new DatabaseService();
    }
    return DatabaseService.instance;
  }

  public getClient(): PrismaClient {
    return this.client;
  }

  // Health check
  public async healthCheck(): Promise<boolean> {
    try {
      await this.client.$queryRaw`SELECT 1`;
      return true;
    } catch (error) {
      console.error('Database health check failed:', error);
      return false;
    }
  }

  // DNA Profile operations
  public async createDnaProfile(data: {
    dnaCode: string;
    projectName: string;
    testing: string;
    risk: string;
    autonomy: string;
    customTools?: string;
    constraints?: string;
  }) {
    return this.client.dnaProfile.create({ data });
  }

  public async getDnaProfile(dnaCode: string) {
    return this.client.dnaProfile.findUnique({
      where: { dnaCode },
      include: { specs: true }
    });
  }

  public async listDnaProfiles() {
    return this.client.dnaProfile.findMany({
      include: { _count: { select: { specs: true } } },
      orderBy: { createdAt: 'desc' }
    });
  }

  public async updateDnaProfile(dnaCode: string, data: Partial<{
    projectName: string;
    testing: string;
    risk: string;
    autonomy: string;
    customTools: string;
    constraints: string;
  }>) {
    return this.client.dnaProfile.update({
      where: { dnaCode },
      data
    });
  }

  public async deleteDnaProfile(dnaCode: string) {
    return this.client.dnaProfile.delete({
      where: { dnaCode }
    });
  }

  // SPEC operations
  public async createSpec(data: {
    descriptor: string;
    dnaCode: string;
    goal?: string;
    filePath: string;
  }) {
    return this.client.spec.create({ data });
  }

  public async getSpec(id: string) {
    return this.client.spec.findUnique({
      where: { id },
      include: {
        dnaProfile: true,
        executions: {
          orderBy: { startedAt: 'desc' },
          take: 10
        }
      }
    });
  }

  public async listSpecs(filters?: {
    dnaCode?: string;
    status?: string;
  }) {
    return this.client.spec.findMany({
      where: filters,
      include: {
        dnaProfile: { select: { projectName: true } },
        _count: { select: { executions: true } }
      },
      orderBy: { updatedAt: 'desc' }
    });
  }

  public async updateSpec(id: string, data: Partial<{
    goal: string;
    status: string;
  }>) {
    return this.client.spec.update({
      where: { id },
      data
    });
  }

  public async deleteSpec(id: string) {
    return this.client.spec.delete({
      where: { id }
    });
  }

  // Execution operations
  public async createExecution(data: {
    specId: string;
    mode: string;
  }) {
    return this.client.execution.create({ data });
  }

  public async getExecution(id: string) {
    return this.client.execution.findUnique({
      where: { id },
      include: {
        spec: { include: { dnaProfile: true } },
        progressLogs: {
          orderBy: { timestamp: 'asc' }
        }
      }
    });
  }

  public async listExecutions(filters?: {
    specId?: string;
    status?: string;
  }) {
    return this.client.execution.findMany({
      where: filters,
      include: {
        spec: { select: { descriptor: true, dnaCode: true } }
      },
      orderBy: { startedAt: 'desc' }
    });
  }

  public async updateExecution(id: string, data: Partial<{
    status: string;
    goalStatus: string;
    completedAt: Date;
    duration: number;
    errorMessage: string;
  }>) {
    return this.client.execution.update({
      where: { id },
      data
    });
  }

  // Progress log operations
  public async createProgressLog(data: {
    executionId: string;
    taskId?: string;
    stepId?: string;
    status: string;
    method?: string;
    details?: string;
  }) {
    return this.client.progressLog.create({ data });
  }

  public async getProgressLogs(executionId: string) {
    return this.client.progressLog.findMany({
      where: { executionId },
      orderBy: { timestamp: 'asc' }
    });
  }
}

// Export singleton instance
export const dbService = DatabaseService.getInstance();
export default prisma;
