import express, { Request, Response, NextFunction } from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import { Server } from 'socket.io';
import { createServer } from 'http';

// Load environment variables
dotenv.config();

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: {
    origin: process.env.FRONTEND_URL || 'http://localhost:3000',
    methods: ['GET', 'POST', 'PUT', 'DELETE'],
    credentials: true
  }
});

const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors({
  origin: process.env.FRONTEND_URL || 'http://localhost:3000',
  credentials: true
}));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Request logging middleware
app.use((req: Request, res: Response, next: NextFunction) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
  next();
});

// Health check endpoint
app.get('/health', (req: Request, res: Response) => {
  res.json({ 
    status: 'ok', 
    timestamp: new Date().toISOString(),
    service: 'spec-engine-dashboard-backend'
  });
});

// API routes (to be added)
app.get('/api', (req: Request, res: Response) => {
  res.json({ 
    message: 'SPEC Engine Dashboard API',
    version: '1.0.0',
    endpoints: {
      dna: '/api/dna',
      specs: '/api/specs',
      executions: '/api/executions',
      files: '/api/files'
    }
  });
});

// Import routes
import dnaRoutes from './routes/dna.routes';
import specsRoutes from './routes/specs.routes';
import executionRoutes from './routes/execution.routes';
import filesRoutes from './routes/files.routes';

// Mount routes
app.use('/api/dna', dnaRoutes);
app.use('/api/specs', specsRoutes);
app.use('/api/executions', executionRoutes);
app.use('/api/files', filesRoutes);

// WebSocket connection handling
io.on('connection', (socket) => {
  console.log('Client connected:', socket.id);
  
  socket.on('disconnect', () => {
    console.log('Client disconnected:', socket.id);
  });
  
  socket.on('subscribe-progress', (specId: string) => {
    socket.join(`progress-${specId}`);
    console.log(`Client ${socket.id} subscribed to progress updates for ${specId}`);
  });
  
  socket.on('unsubscribe-progress', (specId: string) => {
    socket.leave(`progress-${specId}`);
    console.log(`Client ${socket.id} unsubscribed from progress updates for ${specId}`);
  });
});

// Export io for use in other modules
export { io };

// Error handling middleware
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  console.error('Error:', err.message);
  console.error('Stack:', err.stack);
  res.status(500).json({ 
    error: 'Internal server error',
    message: process.env.NODE_ENV === 'development' ? err.message : 'Something went wrong'
  });
});

// 404 handler
app.use((req: Request, res: Response) => {
  res.status(404).json({ 
    error: 'Not found',
    path: req.path 
  });
});

// Start server
httpServer.listen(PORT, () => {
  console.log(`
╔═══════════════════════════════════════════════════════╗
║  SPEC Engine Dashboard Backend                        ║
║  Server running on port ${PORT}                          ║
║  Environment: ${process.env.NODE_ENV || 'development'}                        ║
║  Health: http://localhost:${PORT}/health                 ║
╚═══════════════════════════════════════════════════════╝
  `);
});

export default app;
