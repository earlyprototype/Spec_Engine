import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { supabase } from '../lib/supabase';
import { Layout } from '../components/Layout';
import { IdeaCanvas } from '../components/ideate/IdeaCanvas';
import { IdeaEvaluationMatrix } from '../components/ideate/IdeaEvaluationMatrix';
import { AISynthesis } from '../components/ideate/AISynthesis';
import type { Idea, Cluster, IdeateData } from '../types/ideate';

export function IdeateView() {
  const { projectId } = useParams<{ projectId: string }>();
  const [ideas, setIdeas] = useState<Idea[]>([]);
  const [clusters, setClusters] = useState<Cluster[]>([]);
  const [activeTab, setActiveTab] = useState<'canvas' | 'evaluate' | 'ai'>('canvas');
  const [saving, setSaving] = useState(false);
  const [lastSaved, setLastSaved] = useState<Date | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStageData();
  }, [projectId]);

  const loadStageData = async () => {
    if (!projectId) return;

    setLoading(true);
    const { data: stageData, error } = await supabase
      .from('stage_data')
      .select('*')
      .eq('project_id', projectId)
      .eq('stage_name', 'ideate')
      .single();

    if (error && error.code !== 'PGRST116') {
      console.error('Error loading stage data:', error);
    } else if (stageData) {
      const data = stageData.data_json as IdeateData;
      setIdeas(data.ideas || []);
      setClusters(data.clusters || []);
    }
    setLoading(false);
  };

  const saveStageData = async () => {
    if (!projectId) return;

    setSaving(true);
    const dataJson: IdeateData = {
      ideas,
      clusters,
      lastModified: new Date().toISOString(),
    };

    const { error } = await supabase.from('stage_data').upsert(
      {
        project_id: projectId,
        stage_name: 'ideate',
        data_json: dataJson,
      },
      { onConflict: 'project_id,stage_name' }
    );

    if (error) {
      console.error('Error saving stage data:', error);
      alert('Error saving data: ' + error.message);
    } else {
      setLastSaved(new Date());
    }
    setSaving(false);
  };

  // Auto-save with 2-second debouncing (matches Discovery and Define pattern)
  useEffect(() => {
    const timer = setTimeout(() => {
      if (projectId && ideas.length > 0) {
        saveStageData();
      }
    }, 2000);

    return () => clearTimeout(timer);
  }, [ideas, clusters, projectId]);

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-64">
          <div className="text-gray-500">Loading ideate stage...</div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-7xl mx-auto">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Ideate Stage</h1>
          <p className="text-gray-600">
            Generate creative solutions and ideas. Use the canvas to brainstorm, cluster similar ideas, and evaluate their potential.
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="mb-6 border-b border-gray-200">
          <nav className="-mb-px flex space-x-8">
            <button
              onClick={() => setActiveTab('canvas')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'canvas'
                  ? 'border-green-500 text-green-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Brainstorming Canvas
            </button>
            <button
              onClick={() => setActiveTab('evaluate')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'evaluate'
                  ? 'border-green-500 text-green-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Evaluation Matrix
            </button>
            <button
              onClick={() => setActiveTab('ai')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'ai'
                  ? 'border-green-500 text-green-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              AI Synthesis
            </button>
          </nav>
        </div>

        {/* Tab Content */}
        <div className="mb-6">
          {activeTab === 'canvas' && (
            <IdeaCanvas
              ideas={ideas}
              clusters={clusters}
              onIdeasChange={setIdeas}
              onClustersChange={setClusters}
              onSave={saveStageData}
            />
          )}
          {activeTab === 'evaluate' && (
            <IdeaEvaluationMatrix
              ideas={ideas}
              onIdeasChange={setIdeas}
              onSave={saveStageData}
            />
          )}
          {activeTab === 'ai' && (
            <AISynthesis
              projectId={projectId || ''}
              ideas={ideas}
              onIdeasGenerated={(newIdeas) => {
                setIdeas([...ideas, ...newIdeas]);
                saveStageData();
              }}
            />
          )}
        </div>

        {/* Save Status */}
        <div className="flex items-center justify-between bg-white rounded-lg shadow p-4">
          <div className="text-sm text-gray-500">
            {lastSaved ? `Last saved: ${lastSaved.toLocaleTimeString()}` : 'Auto-save enabled'}
          </div>
          <button
            onClick={saveStageData}
            disabled={saving}
            className="px-6 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50"
          >
            {saving ? 'Saving...' : 'Save Now'}
          </button>
        </div>
      </div>
    </Layout>
  );
}

