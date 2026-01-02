import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { supabase } from '../lib/supabase';
import { Layout } from '../components/Layout';

interface Prototype {
  id: string;
  name: string;
  type: 'paper_sketch' | 'digital_mockup' | 'physical_model' | 'interactive_prototype' | 'other';
  description: string;
  imageUrl?: string;
  createdAt: string;
}

interface ValidationPlan {
  testScenarios: Array<{
    id: string;
    scenario: string;
    testers: string;
  }>;
  successMetrics: Array<{
    id: string;
    metric: string;
  }>;
  assumptions: Array<{
    id: string;
    assumption: string;
  }>;
}

interface PrototypeData {
  prototypes: Prototype[];
  validationPlan: ValidationPlan;
  aiSynthesis?: {
    strategy: string;
    generatedAt: string;
  };
}

const initialData: PrototypeData = {
  prototypes: [],
  validationPlan: {
    testScenarios: [],
    successMetrics: [],
    assumptions: [],
  },
};

export function PrototypeView() {
  const { projectId } = useParams<{ projectId: string }>();
  const [data, setData] = useState<PrototypeData>(initialData);
  const [saving, setSaving] = useState(false);
  const [lastSaved, setLastSaved] = useState<Date | null>(null);
  const [loading, setLoading] = useState(true);
  const [generatingAI, setGeneratingAI] = useState(false);
  const [aiError, setAiError] = useState<string | null>(null);

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
      .eq('stage_name', 'prototype')
      .single();

    if (error && error.code !== 'PGRST116') {
      console.error('Error loading prototype data:', error);
    } else if (stageData && stageData.data_json) {
      setData(stageData.data_json as PrototypeData);
    }
    setLoading(false);
  };

  const saveStageData = async () => {
    if (!projectId) return;

    setSaving(true);
    const { error } = await supabase.from('stage_data').upsert(
      {
        project_id: projectId,
        stage_name: 'prototype',
        data_json: data,
      },
      { onConflict: 'project_id,stage_name' }
    );

    if (error) {
      console.error('Error saving prototype data:', error);
      alert('Error saving data: ' + error.message);
    } else {
      setLastSaved(new Date());
    }
    setSaving(false);
  };

  // Prototype management functions
  const addPrototype = () => {
    const newPrototype: Prototype = {
      id: `prototype-${Date.now()}`,
      name: '',
      type: 'paper_sketch',
      description: '',
      createdAt: new Date().toISOString(),
    };
    setData({ ...data, prototypes: [...data.prototypes, newPrototype] });
  };

  const removePrototype = (index: number) => {
    const newPrototypes = data.prototypes.filter((_, i) => i !== index);
    setData({ ...data, prototypes: newPrototypes });
  };

  const updatePrototype = (index: number, field: keyof Prototype, value: string) => {
    const newPrototypes = [...data.prototypes];
    newPrototypes[index] = { ...newPrototypes[index], [field]: value };
    setData({ ...data, prototypes: newPrototypes });
  };

  // Validation planning functions
  const addValidationItem = (type: keyof ValidationPlan) => {
    const newItem = {
      id: `${type}-${Date.now()}`,
      ...(type === 'testScenarios' ? { scenario: '', testers: '' } : {}),
      ...(type === 'successMetrics' ? { metric: '' } : {}),
      ...(type === 'assumptions' ? { assumption: '' } : {}),
    };
    
    setData({
      ...data,
      validationPlan: {
        ...data.validationPlan,
        [type]: [...data.validationPlan[type], newItem],
      },
    });
  };

  const removeValidationItem = (type: keyof ValidationPlan, index: number) => {
    const newItems = data.validationPlan[type].filter((_, i) => i !== index);
    setData({
      ...data,
      validationPlan: {
        ...data.validationPlan,
        [type]: newItems,
      },
    });
  };

  const updateValidationItem = (
    type: keyof ValidationPlan,
    index: number,
    field: string,
    value: string
  ) => {
    const newItems = [...data.validationPlan[type]];
    newItems[index] = { ...newItems[index], [field]: value };
    setData({
      ...data,
      validationPlan: {
        ...data.validationPlan,
        [type]: newItems,
      },
    });
  };

  // AI Synthesis functions
  const generateAISynthesis = async () => {
    if (!projectId) return;
    
    setGeneratingAI(true);
    setAiError(null);

    try {
      // Fetch context from previous stages
      const { data: stageDataList, error: fetchError } = await supabase
        .from('stage_data')
        .select('*')
        .eq('project_id', projectId)
        .in('stage_name', ['discovery', 'define', 'ideate']);

      if (fetchError) {
        throw new Error('Failed to fetch stage data for context');
      }

      // Build context from previous stages
      const context = stageDataList?.reduce((acc, stage) => {
        acc[stage.stage_name] = stage.data_json;
        return acc;
      }, {} as Record<string, any>) || {};

      // Call Gemini API
      const apiKey = import.meta.env.VITE_GEMINI_API_KEY;
      
      if (!apiKey) {
        throw new Error('Gemini API key not configured. Please add VITE_GEMINI_API_KEY to your .env file.');
      }

      const prompt = `You are an innovation consultant helping a team develop a prototype strategy.

Context from previous stages:
- Discovery insights: ${JSON.stringify(context.discovery || 'No discovery data yet', null, 2)}
- Define phase: ${JSON.stringify(context.define || 'No define data yet', null, 2)}
- Ideate phase: ${JSON.stringify(context.ideate || 'No ideate data yet', null, 2)}

Current prototype plan:
- Prototypes: ${JSON.stringify(data.prototypes, null, 2)}
- Validation plan: ${JSON.stringify(data.validationPlan, null, 2)}

Please provide a comprehensive prototype strategy that includes:
1. Recommended prototype types and fidelity levels
2. Specific validation approach based on the assumptions
3. Risk areas to watch out for
4. Timeline recommendations
5. Resource requirements
6. Success indicators

Format your response as clear, actionable recommendations that a consultant can use to guide their client.`;

      const response = await fetch(
        `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key=${apiKey}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            contents: [{
              parts: [{
                text: prompt
              }]
            }]
          })
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error?.message || 'Failed to generate AI synthesis');
      }

      const result = await response.json();
      const generatedText = result.candidates?.[0]?.content?.parts?.[0]?.text || 'No response generated';

      setData({
        ...data,
        aiSynthesis: {
          strategy: generatedText,
          generatedAt: new Date().toISOString(),
        },
      });
    } catch (error) {
      console.error('Error generating AI synthesis:', error);
      setAiError(error instanceof Error ? error.message : 'Failed to generate AI synthesis');
    } finally {
      setGeneratingAI(false);
    }
  };

  const clearAISynthesis = () => {
    setData({
      ...data,
      aiSynthesis: undefined,
    });
  };

  const updateAISynthesis = (newText: string) => {
    if (data.aiSynthesis) {
      setData({
        ...data,
        aiSynthesis: {
          ...data.aiSynthesis,
          strategy: newText,
        },
      });
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="max-w-6xl mx-auto">
          <div className="flex items-center justify-center min-h-[400px]">
            <div className="text-gray-500">Loading prototype data...</div>
          </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Prototype Stage</h1>
          <p className="text-gray-600">
            Build quick prototypes to test your ideas and validate assumptions with real users.
          </p>
        </div>

        {/* Save Button and Status - Fixed at top */}
        <div className="mb-6 flex items-center justify-between bg-white rounded-lg shadow p-4 sticky top-0 z-10">
          <div className="text-sm text-gray-500">
            {lastSaved && `Last saved: ${lastSaved.toLocaleTimeString()}`}
            {!lastSaved && 'Not saved yet'}
          </div>
          <button
            onClick={saveStageData}
            disabled={saving}
            className="px-6 py-2 bg-orange-600 text-white rounded-md hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500 disabled:opacity-50 transition-colors"
          >
            {saving ? 'Saving...' : 'Save Progress'}
          </button>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Left Column: Prototype Documentation */}
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold text-gray-900">
                  Prototype Documentation
                </h2>
                <button
                  onClick={addPrototype}
                  className="px-4 py-2 bg-orange-600 text-white text-sm rounded-md hover:bg-orange-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-orange-500"
                >
                  + Add Prototype
                </button>
              </div>
              <p className="text-sm text-gray-600 mb-4">
                Document your prototypes to track iterations and communicate ideas with your team.
              </p>
              
              {/* Prototype List */}
              {data.prototypes.length === 0 ? (
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center text-gray-500">
                  <p className="mb-2">No prototypes yet</p>
                  <p className="text-sm">Click "Add Prototype" to get started</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {data.prototypes.map((prototype, index) => (
                    <div key={prototype.id} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex-1">
                          <input
                            type="text"
                            value={prototype.name}
                            onChange={(e) => updatePrototype(index, 'name', e.target.value)}
                            placeholder="Prototype name"
                            className="text-lg font-medium text-gray-900 w-full border-0 border-b border-transparent hover:border-gray-300 focus:border-orange-500 focus:outline-none focus:ring-0 px-0"
                          />
                        </div>
                        <button
                          onClick={() => removePrototype(index)}
                          className="ml-2 text-red-600 hover:text-red-800 text-sm"
                        >
                          Remove
                        </button>
                      </div>

                      {/* Prototype Type Selector */}
                      <div className="mb-3">
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Prototype Type
                        </label>
                        <select
                          value={prototype.type}
                          onChange={(e) => updatePrototype(index, 'type', e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                        >
                          <option value="paper_sketch">Paper Sketch</option>
                          <option value="digital_mockup">Digital Mockup</option>
                          <option value="physical_model">Physical Model</option>
                          <option value="interactive_prototype">Interactive Prototype</option>
                          <option value="other">Other</option>
                        </select>
                      </div>

                      {/* Description */}
                      <div className="mb-3">
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Description
                        </label>
                        <textarea
                          value={prototype.description}
                          onChange={(e) => updatePrototype(index, 'description', e.target.value)}
                          placeholder="Describe this prototype, what it tests, and key features..."
                          rows={3}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                        />
                      </div>

                      {/* Image Upload Placeholder */}
                      <div className="mb-2">
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Image/Sketch
                        </label>
                        {prototype.imageUrl ? (
                          <div className="relative">
                            <img
                              src={prototype.imageUrl}
                              alt={prototype.name}
                              className="w-full h-48 object-cover rounded-md"
                            />
                            <button
                              onClick={() => updatePrototype(index, 'imageUrl', '')}
                              className="absolute top-2 right-2 px-2 py-1 bg-red-600 text-white text-xs rounded hover:bg-red-700"
                            >
                              Remove Image
                            </button>
                          </div>
                        ) : (
                          <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
                            <p className="text-sm text-gray-500 mb-2">Image upload coming soon</p>
                            <p className="text-xs text-gray-400">For now, add image URLs:</p>
                            <input
                              type="text"
                              value={prototype.imageUrl || ''}
                              onChange={(e) => updatePrototype(index, 'imageUrl', e.target.value)}
                              placeholder="https://example.com/image.jpg"
                              className="mt-2 w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                            />
                          </div>
                        )}
                      </div>

                      {/* Timestamp */}
                      <div className="text-xs text-gray-400 mt-2">
                        Created: {new Date(prototype.createdAt).toLocaleDateString()}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Right Column: Validation Planning */}
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">
                Validation Planning
              </h2>
              <p className="text-sm text-gray-600 mb-4">
                Plan how you'll test your prototypes and what success looks like.
              </p>
              
              {/* Test Scenarios */}
              <div className="mb-6">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-sm font-semibold text-gray-800">Test Scenarios</h3>
                  <button
                    onClick={() => addValidationItem('testScenarios')}
                    className="text-sm text-orange-600 hover:text-orange-800"
                  >
                    + Add
                  </button>
                </div>
                <p className="text-xs text-gray-500 mb-3">
                  Who will test and what specific scenarios will you test?
                </p>
                {data.validationPlan.testScenarios.length === 0 ? (
                  <div className="border border-gray-200 rounded p-3 text-sm text-gray-400 text-center">
                    No test scenarios yet
                  </div>
                ) : (
                  <div className="space-y-2">
                    {data.validationPlan.testScenarios.map((item, index) => (
                      <div key={item.id} className="flex gap-2">
                        <div className="flex-1 space-y-2">
                          <input
                            type="text"
                            value={item.testers}
                            onChange={(e) => updateValidationItem('testScenarios', index, 'testers', e.target.value)}
                            placeholder="Who will test? (e.g., 5 target users)"
                            className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                          />
                          <input
                            type="text"
                            value={item.scenario}
                            onChange={(e) => updateValidationItem('testScenarios', index, 'scenario', e.target.value)}
                            placeholder="What scenario? (e.g., Complete checkout flow)"
                            className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                          />
                        </div>
                        <button
                          onClick={() => removeValidationItem('testScenarios', index)}
                          className="text-red-600 hover:text-red-800 text-xs px-2"
                        >
                          ×
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Success Metrics */}
              <div className="mb-6">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-sm font-semibold text-gray-800">Success Metrics</h3>
                  <button
                    onClick={() => addValidationItem('successMetrics')}
                    className="text-sm text-orange-600 hover:text-orange-800"
                  >
                    + Add
                  </button>
                </div>
                <p className="text-xs text-gray-500 mb-3">
                  How will you measure if the prototype is successful?
                </p>
                {data.validationPlan.successMetrics.length === 0 ? (
                  <div className="border border-gray-200 rounded p-3 text-sm text-gray-400 text-center">
                    No success metrics yet
                  </div>
                ) : (
                  <div className="space-y-2">
                    {data.validationPlan.successMetrics.map((item, index) => (
                      <div key={item.id} className="flex gap-2">
                        <input
                          type="text"
                          value={item.metric}
                          onChange={(e) => updateValidationItem('successMetrics', index, 'metric', e.target.value)}
                          placeholder="e.g., 80% of users complete task without help"
                          className="flex-1 px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                        />
                        <button
                          onClick={() => removeValidationItem('successMetrics', index)}
                          className="text-red-600 hover:text-red-800 text-xs px-2"
                        >
                          ×
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Assumptions to Validate */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <h3 className="text-sm font-semibold text-gray-800">Assumptions to Validate</h3>
                  <button
                    onClick={() => addValidationItem('assumptions')}
                    className="text-sm text-orange-600 hover:text-orange-800"
                  >
                    + Add
                  </button>
                </div>
                <p className="text-xs text-gray-500 mb-3">
                  What key assumptions are you testing with this prototype?
                </p>
                {data.validationPlan.assumptions.length === 0 ? (
                  <div className="border border-gray-200 rounded p-3 text-sm text-gray-400 text-center">
                    No assumptions yet
                  </div>
                ) : (
                  <div className="space-y-2">
                    {data.validationPlan.assumptions.map((item, index) => (
                      <div key={item.id} className="flex gap-2">
                        <input
                          type="text"
                          value={item.assumption}
                          onChange={(e) => updateValidationItem('assumptions', index, 'assumption', e.target.value)}
                          placeholder="e.g., Users understand the navigation without instructions"
                          className="flex-1 px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500"
                        />
                        <button
                          onClick={() => removeValidationItem('assumptions', index)}
                          className="text-red-600 hover:text-red-800 text-xs px-2"
                        >
                          ×
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* AI Synthesis Section - Full Width */}
        <div className="mt-6 bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-xl font-semibold text-gray-900">
                AI Prototype Strategy
              </h2>
              <p className="text-sm text-gray-600 mt-1">
                Get AI-powered recommendations based on your Discovery, Define, and Ideate insights.
              </p>
            </div>
            <button
              onClick={generateAISynthesis}
              disabled={generatingAI}
              className="px-6 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50 flex items-center gap-2"
            >
              {generatingAI ? (
                <>
                  <span className="animate-spin">⚙</span>
                  Generating...
                </>
              ) : (
                <>Generate Strategy</>
              )}
            </button>
          </div>

          {aiError && (
            <div className="mb-4 bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-sm text-red-800">{aiError}</p>
            </div>
          )}

          {data.aiSynthesis ? (
            <div>
              <div className="bg-purple-50 border border-purple-200 rounded-lg p-4 mb-3">
                <div className="flex items-center justify-between mb-2">
                  <div className="text-xs text-purple-600 font-medium">
                    Generated by Gemini 2.5 Pro • {new Date(data.aiSynthesis.generatedAt).toLocaleString()}
                  </div>
                  <button
                    onClick={clearAISynthesis}
                    className="text-xs text-purple-600 hover:text-purple-800"
                  >
                    Clear
                  </button>
                </div>
              </div>
              <textarea
                value={data.aiSynthesis.strategy}
                onChange={(e) => updateAISynthesis(e.target.value)}
                rows={12}
                className="w-full px-4 py-3 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-purple-500 font-mono text-sm"
                placeholder="AI-generated strategy will appear here..."
              />
              <p className="text-xs text-gray-500 mt-2">
                You can edit the AI-generated strategy above. Click "Save Progress" to persist your changes.
              </p>
            </div>
          ) : (
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center text-gray-500">
              <p className="mb-2">No AI strategy generated yet</p>
              <p className="text-sm">
                Click "Generate Strategy" to get AI-powered recommendations for your prototype approach
              </p>
            </div>
          )}
        </div>

        {/* Info Box */}
        <div className="mt-6 bg-orange-50 rounded-lg p-4 border border-orange-200">
          <h3 className="text-sm font-medium text-orange-900 mb-2">Prototyping Tips</h3>
          <ul className="text-sm text-orange-800 space-y-1 list-disc list-inside">
            <li>Start with low-fidelity prototypes (paper sketches, wireframes)</li>
            <li>Focus on testing specific assumptions, not building perfect products</li>
            <li>Plan your validation before building the prototype</li>
            <li>Document learnings from each iteration</li>
          </ul>
        </div>
      </div>
    </Layout>
  );
}

