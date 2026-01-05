import { io, Socket } from 'socket.io-client';

const WS_URL = import.meta.env.VITE_WS_URL || 'http://localhost:5000';

class SocketService {
  private socket: Socket | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;

  public connect(): void {
    if (this.socket?.connected) {
      console.log('Socket already connected');
      return;
    }

    this.socket = io(WS_URL, {
      transports: ['websocket', 'polling'],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionDelayMax: 5000,
      reconnectionAttempts: this.maxReconnectAttempts,
    });

    this.socket.on('connect', () => {
      console.log('WebSocket connected:', this.socket?.id);
      this.reconnectAttempts = 0;
    });

    this.socket.on('disconnect', (reason) => {
      console.log('WebSocket disconnected:', reason);
    });

    this.socket.on('connect_error', (error) => {
      console.error('WebSocket connection error:', error);
      this.reconnectAttempts++;
      
      if (this.reconnectAttempts >= this.maxReconnectAttempts) {
        console.error('Max reconnection attempts reached');
      }
    });
  }

  public disconnect(): void {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }

  public subscribeToProgress(specId: string, callback: (progress: any) => void): void {
    if (!this.socket) {
      console.error('Socket not connected');
      return;
    }

    // Subscribe to progress updates
    this.socket.emit('subscribe-progress', specId);
    
    // Listen for progress updates
    this.socket.on('progress-update', callback);
    
    console.log(`Subscribed to progress updates for ${specId}`);
  }

  public unsubscribeFromProgress(specId: string, callback?: (progress: any) => void): void {
    if (!this.socket) return;

    // Unsubscribe from progress updates
    this.socket.emit('unsubscribe-progress', specId);
    
    // Remove listener
    if (callback) {
      this.socket.off('progress-update', callback);
    }
    
    console.log(`Unsubscribed from progress updates for ${specId}`);
  }

  public isConnected(): boolean {
    return this.socket?.connected || false;
  }

  public getSocket(): Socket | null {
    return this.socket;
  }
}

export const socketService = new SocketService();
export default socketService;
