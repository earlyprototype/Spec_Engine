import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

class ApiService {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
      withCredentials: true,
    });

    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        console.error('API Error:', error.response?.data || error.message);
        return Promise.reject(error);
      }
    );
  }

  // Health check
  async healthCheck() {
    return this.client.get('/health');
  }

  // DNA Profile endpoints
  async listDnaProfiles() {
    return this.client.get('/api/dna');
  }

  async getDnaProfile(dnaCode: string) {
    return this.client.get(`/api/dna/${dnaCode}`);
  }

  async createDnaProfile(data: any) {
    return this.client.post('/api/dna', data);
  }

  async updateDnaProfile(dnaCode: string, data: any) {
    return this.client.put(`/api/dna/${dnaCode}`, data);
  }

  async deleteDnaProfile(dnaCode: string) {
    return this.client.delete(`/api/dna/${dnaCode}`);
  }

  // SPEC endpoints
  async listSpecs(filters?: any) {
    return this.client.get('/api/specs', { params: filters });
  }

  async getSpec(specId: string) {
    return this.client.get(`/api/specs/${specId}`);
  }

  async createSpec(data: any) {
    return this.client.post('/api/specs', data);
  }

  async getParameters(specId: string) {
    return this.client.get(`/api/specs/${specId}/parameters`);
  }

  async updateParameters(specId: string, content: string) {
    return this.client.put(`/api/specs/${specId}/parameters`, { content });
  }

  // Execution endpoints
  async listExecutions(filters?: any) {
    return this.client.get('/api/executions', { params: filters });
  }

  async getExecution(executionId: string) {
    return this.client.get(`/api/executions/${executionId}`);
  }

  async startExecution(data: { specId: string; mode: string }) {
    return this.client.post('/api/executions', data);
  }

  async stopExecution(executionId: string) {
    return this.client.post(`/api/executions/${executionId}/stop`);
  }

  async getExecutionResults(executionId: string) {
    return this.client.get(`/api/executions/${executionId}/results`);
  }

  async getExecutionLogs(executionId: string) {
    return this.client.get(`/api/executions/${executionId}/logs`);
  }

  // File validation
  async validateToml(content: string) {
    return this.client.post('/api/files/validate/toml', { content });
  }

  async getProgress(specId: string) {
    return this.client.get(`/api/files/progress/${specId}`);
  }
}

export const apiService = new ApiService();
export default apiService;
