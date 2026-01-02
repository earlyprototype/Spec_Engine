import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { supabase } from '../lib/supabase';
import { Layout } from '../components/Layout';

const stageInfo = {
  discovery: {
    title: 'Discovery Stage',
    description: 'Understand the users, their needs, and the problem space.',
    color: 'blue',
  },
  define: {
    title: 'Define Stage',
    description: 'Frame the problem clearly based on discovery insights.',
    color: 'purple',
  },
  ideate: {
    title: 'Ideate Stage',
    description: 'Generate creative solutions and ideas.',
    color: 'green',
  },
  prototype: {
    title: 'Prototype Stage',
    description: 'Build quick prototypes to test ideas.',
    color: 'orange',
  },
  test: {
    title: 'Test Stage',
    description: 'Test prototypes with users and gather feedback.',
    color: 'red',
  },
};

type StageName = keyof typeof stageInfo;

export function StageView() {
  const { projectId, stage } = useParams<{ projectId: string; stage: StageName }>();
  const [content, setContent] = useState('');
  const [saving, setSaving] = useState(false);
  const [lastSaved, setLastSaved] = useState<Date | null>(null);

  const info = stage ? stageInfo[stage] : stageInfo.discovery;

  useEffect(() => {
    loadStageData();
  }, [projectId, stage]);

  const loadStageData = async () => {
    if (!projectId || !stage) return;

    const { data: stageData, error } = await supabase
      .from('stage_data')
      .select('*')
      .eq('project_id', projectId)
      .eq('stage_name', stage)
      .single();

    if (error && error.code !== 'PGRST116') {
      console.error('Error loading stage data:', error);
    } else if (stageData) {
      setContent(stageData.data_json.content || '');
    }
  };

  const saveStageData = async () => {
    if (!projectId || !stage) return;

    setSaving(true);
    const dataJson = { content, lastModified: new Date().toISOString() };

    const { error } = await supabase.from('stage_data').upsert(
      {
        project_id: projectId,
        stage_name: stage,
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

  return (
    <Layout>
      <div className="max-w-4xl mx-auto">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">{info.title}</h1>
          <p className="text-gray-600">{info.description}</p>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="mb-4">
            <label htmlFor="content" className="block text-sm font-medium text-gray-700 mb-2">
              Stage Notes
            </label>
            <textarea
              id="content"
              rows={15}
              value={content}
              onChange={(e) => setContent(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              placeholder={`Enter your ${stage} stage notes here...`}
            />
          </div>

          <div className="flex items-center justify-between">
            <div className="text-sm text-gray-500">
              {lastSaved && `Last saved: ${lastSaved.toLocaleTimeString()}`}
            </div>
            <button
              onClick={saveStageData}
              disabled={saving}
              className="px-6 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
            >
              {saving ? 'Saving...' : 'Save'}
            </button>
          </div>
        </div>

        <div className="mt-6 bg-blue-50 rounded-lg p-4">
          <h3 className="text-sm font-medium text-blue-900 mb-2">Coming Soon</h3>
          <p className="text-sm text-blue-700">
            AI-powered synthesis and facilitation tools will be added in future SPEClets.
          </p>
        </div>
      </div>
    </Layout>
  );
}

