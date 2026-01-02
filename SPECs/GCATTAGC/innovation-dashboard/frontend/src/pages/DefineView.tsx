import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { supabase } from '../lib/supabase';
import { Layout } from '../components/Layout';
import { generateDefineSynthesis, type DefineSynthesisResult } from '../services/defineGeminiService';

interface HMWStatement {
  id: string;
  statement: string;
  priority: 'high' | 'medium' | 'low';
}

interface Stakeholder {
  id: string;
  name: string;
  role: string;
  influence: 'high' | 'medium' | 'low';
  interest: 'high' | 'medium' | 'low';
  needs: string;
}

interface DefineData {
  hmwStatements: HMWStatement[];
  stakeholders: Stakeholder[];
  constraints: string;
  opportunities: string;
  problemContext: string;
  synthesisResult?: DefineSynthesisResult;
  lastModified?: string;
}

export function DefineView() {
  const { projectId } = useParams<{ projectId: string }>();
  const [data, setData] = useState<DefineData>({
    hmwStatements: [],
    stakeholders: [],
    constraints: '',
    opportunities: '',
    problemContext: '',
  });
  const [saving, setSaving] = useState(false);
  const [lastSaved, setLastSaved] = useState<Date | null>(null);
  const [activeTab, setActiveTab] = useState<'problem' | 'stakeholders' | 'synthesis'>('problem');
  const [newHMW, setNewHMW] = useState('');
  const [synthesizing, setSynthesizing] = useState(false);

  useEffect(() => {
    loadDefineData();
  }, [projectId]);

  // Auto-save with 2-second debouncing (matches Discovery pattern)
  useEffect(() => {
    const timer = setTimeout(() => {
      if (projectId && (data.hmwStatements.length > 0 || data.problemContext)) {
        saveDefineData(true);
      }
    }, 2000);

    return () => clearTimeout(timer);
  }, [data, projectId]);

  const loadDefineData = async () => {
    if (!projectId) return;

    const { data: stageData, error } = await supabase
      .from('stage_data')
      .select('*')
      .eq('project_id', projectId)
      .eq('stage_name', 'define')
      .single();

    if (error && error.code !== 'PGRST116') {
      console.error('Error loading define data:', error);
    } else if (stageData?.data_json) {
      setData(stageData.data_json as DefineData);
    }
  };

  const saveDefineData = async (isAutoSave = false) => {
    if (!projectId) return;

    if (!isAutoSave) setSaving(true);

    const dataToSave = {
      ...data,
      lastModified: new Date().toISOString(),
    };

    const { error } = await supabase.from('stage_data').upsert(
      {
        project_id: projectId,
        stage_name: 'define',
        data_json: dataToSave,
      },
      { onConflict: 'project_id,stage_name' }
    );

    if (error) {
      console.error('Error saving define data:', error);
      if (!isAutoSave) alert('Error saving data: ' + error.message);
    } else {
      setLastSaved(new Date());
      setData(dataToSave);
    }

    if (!isAutoSave) setSaving(false);
  };

  const addHMWStatement = () => {
    if (!newHMW.trim()) return;

    const hmwStatement: HMWStatement = {
      id: Date.now().toString(),
      statement: newHMW.trim(),
      priority: 'medium',
    };

    setData({
      ...data,
      hmwStatements: [...data.hmwStatements, hmwStatement],
    });
    setNewHMW('');
  };

  const removeHMWStatement = (id: string) => {
    setData({
      ...data,
      hmwStatements: data.hmwStatements.filter((hmw) => hmw.id !== id),
    });
  };

  const updateHMWPriority = (id: string, priority: 'high' | 'medium' | 'low') => {
    setData({
      ...data,
      hmwStatements: data.hmwStatements.map((hmw) =>
        hmw.id === id ? { ...hmw, priority } : hmw
      ),
    });
  };

  const addStakeholder = () => {
    const newStakeholder: Stakeholder = {
      id: Date.now().toString(),
      name: 'New Stakeholder',
      role: '',
      influence: 'medium',
      interest: 'medium',
      needs: '',
    };

    setData({
      ...data,
      stakeholders: [...data.stakeholders, newStakeholder],
    });
  };

  const updateStakeholder = (id: string, updates: Partial<Stakeholder>) => {
    setData({
      ...data,
      stakeholders: data.stakeholders.map((stakeholder) =>
        stakeholder.id === id ? { ...stakeholder, ...updates } : stakeholder
      ),
    });
  };

  const removeStakeholder = (id: string) => {
    setData({
      ...data,
      stakeholders: data.stakeholders.filter((s) => s.id !== id),
    });
  };

  const triggerAISynthesis = async () => {
    setSynthesizing(true);
    
    try {
      const synthesisResult = await generateDefineSynthesis({
        hmwStatements: data.hmwStatements,
        stakeholders: data.stakeholders,
        constraints: data.constraints,
        opportunities: data.opportunities,
        problemContext: data.problemContext,
      });
      
      setData({
        ...data,
        synthesisResult,
      });
      setActiveTab('synthesis');
    } catch (error) {
      console.error('Error generating synthesis:', error);
      alert(error instanceof Error ? error.message : 'Failed to generate synthesis. Please try again.');
    } finally {
      setSynthesizing(false);
    }
  };

  const calculateCompletionScore = () => {
    let score = 0;
    if (data.problemContext.length > 50) score += 20;
    if (data.hmwStatements.length > 0) score += 30;
    if (data.stakeholders.length > 0) score += 20;
    if (data.constraints.length > 20) score += 15;
    if (data.opportunities.length > 20) score += 15;
    return Math.min(score, 100);
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-800 border-red-200';
      case 'medium':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'low':
        return 'bg-green-100 text-green-800 border-green-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const completionScore = calculateCompletionScore();

  return (
    <Layout>
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Define Stage</h1>
          <p className="text-gray-600">Frame the problem clearly based on discovery insights</p>
        </div>

        {/* Progress Bar */}
        <div className="mb-6 bg-white rounded-lg shadow p-4">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700">Problem Definition Progress</span>
            <span className="text-sm font-semibold text-primary-600">{completionScore}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-primary-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${completionScore}%` }}
            />
          </div>
          <div className="mt-2 text-xs text-gray-500">
            {completionScore < 100 && (
              <span>
                Keep adding context, HMW statements, and stakeholder information to improve clarity
              </span>
            )}
            {completionScore === 100 && (
              <span>Excellent! Your problem definition is well-structured.</span>
            )}
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="mb-6 bg-white rounded-lg shadow">
          <div className="border-b border-gray-200">
            <nav className="flex -mb-px">
              <button
                onClick={() => setActiveTab('problem')}
                className={`py-4 px-6 text-sm font-medium border-b-2 transition-colors ${
                  activeTab === 'problem'
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Problem Framing
              </button>
              <button
                onClick={() => setActiveTab('stakeholders')}
                className={`py-4 px-6 text-sm font-medium border-b-2 transition-colors ${
                  activeTab === 'stakeholders'
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Stakeholders
              </button>
              <button
                onClick={() => setActiveTab('synthesis')}
                className={`py-4 px-6 text-sm font-medium border-b-2 transition-colors ${
                  activeTab === 'synthesis'
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                AI Synthesis
              </button>
            </nav>
          </div>

          {/* Tab Content */}
          <div className="p-6">
            {/* Problem Framing Tab */}
            {activeTab === 'problem' && (
              <div className="space-y-6">
                {/* Problem Context */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Problem Context
                  </label>
                  <textarea
                    value={data.problemContext}
                    onChange={(e) => setData({ ...data, problemContext: e.target.value })}
                    rows={4}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    placeholder="Describe the problem context and background from your discovery phase..."
                  />
                </div>

                {/* How Might We Statements */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    How Might We... (HMW) Statements
                  </label>
                  <p className="text-sm text-gray-500 mb-3">
                    Create problem-framing questions that open up possibilities for solutions
                  </p>

                  <div className="flex gap-2 mb-4">
                    <input
                      type="text"
                      value={newHMW}
                      onChange={(e) => setNewHMW(e.target.value)}
                      onKeyPress={(e) => e.key === 'Enter' && addHMWStatement()}
                      placeholder="How might we..."
                      className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    />
                    <button
                      onClick={addHMWStatement}
                      className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                    >
                      Add
                    </button>
                  </div>

                  <div className="space-y-2">
                    {data.hmwStatements.map((hmw) => (
                      <div
                        key={hmw.id}
                        className="flex items-center gap-3 p-3 bg-gray-50 rounded-md border border-gray-200"
                      >
                        <span className="flex-1 text-gray-900">{hmw.statement}</span>
                        <select
                          value={hmw.priority}
                          onChange={(e) =>
                            updateHMWPriority(
                              hmw.id,
                              e.target.value as 'high' | 'medium' | 'low'
                            )
                          }
                          className={`px-2 py-1 text-xs rounded border ${getPriorityColor(
                            hmw.priority
                          )}`}
                        >
                          <option value="high">High</option>
                          <option value="medium">Medium</option>
                          <option value="low">Low</option>
                        </select>
                        <button
                          onClick={() => removeHMWStatement(hmw.id)}
                          className="text-red-600 hover:text-red-800 text-sm"
                        >
                          Remove
                        </button>
                      </div>
                    ))}
                    {data.hmwStatements.length === 0 && (
                      <p className="text-sm text-gray-500 italic">
                        No HMW statements yet. Add your first one above.
                      </p>
                    )}
                  </div>
                </div>

                {/* Constraints */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Constraints & Limitations
                  </label>
                  <textarea
                    value={data.constraints}
                    onChange={(e) => setData({ ...data, constraints: e.target.value })}
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    placeholder="What constraints or limitations must be considered? (budget, time, technical, regulatory, etc.)"
                  />
                </div>

                {/* Opportunities */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Opportunities & Assets
                  </label>
                  <textarea
                    value={data.opportunities}
                    onChange={(e) => setData({ ...data, opportunities: e.target.value })}
                    rows={3}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                    placeholder="What opportunities or assets can be leveraged? (existing resources, partnerships, technologies, etc.)"
                  />
                </div>
              </div>
            )}

            {/* Stakeholders Tab */}
            {activeTab === 'stakeholders' && (
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <div>
                    <h3 className="text-lg font-medium text-gray-900">Stakeholder Mapping</h3>
                    <p className="text-sm text-gray-500 mt-1">
                      Identify key stakeholders, their influence, interest, and needs
                    </p>
                  </div>
                  <button
                    onClick={addStakeholder}
                    className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                  >
                    Add Stakeholder
                  </button>
                </div>

                <div className="space-y-4">
                  {data.stakeholders.map((stakeholder) => (
                    <div
                      key={stakeholder.id}
                      className="p-4 bg-gray-50 rounded-md border border-gray-200"
                    >
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                          <label className="block text-xs font-medium text-gray-700 mb-1">
                            Name
                          </label>
                          <input
                            type="text"
                            value={stakeholder.name}
                            onChange={(e) =>
                              updateStakeholder(stakeholder.id, { name: e.target.value })
                            }
                            className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                          />
                        </div>
                        <div>
                          <label className="block text-xs font-medium text-gray-700 mb-1">
                            Role
                          </label>
                          <input
                            type="text"
                            value={stakeholder.role}
                            onChange={(e) =>
                              updateStakeholder(stakeholder.id, { role: e.target.value })
                            }
                            className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                          />
                        </div>
                        <div>
                          <label className="block text-xs font-medium text-gray-700 mb-1">
                            Influence
                          </label>
                          <select
                            value={stakeholder.influence}
                            onChange={(e) =>
                              updateStakeholder(stakeholder.id, {
                                influence: e.target.value as 'high' | 'medium' | 'low',
                              })
                            }
                            className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                          >
                            <option value="high">High</option>
                            <option value="medium">Medium</option>
                            <option value="low">Low</option>
                          </select>
                        </div>
                        <div>
                          <label className="block text-xs font-medium text-gray-700 mb-1">
                            Interest
                          </label>
                          <select
                            value={stakeholder.interest}
                            onChange={(e) =>
                              updateStakeholder(stakeholder.id, {
                                interest: e.target.value as 'high' | 'medium' | 'low',
                              })
                            }
                            className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                          >
                            <option value="high">High</option>
                            <option value="medium">Medium</option>
                            <option value="low">Low</option>
                          </select>
                        </div>
                        <div className="md:col-span-2">
                          <label className="block text-xs font-medium text-gray-700 mb-1">
                            Key Needs & Concerns
                          </label>
                          <textarea
                            value={stakeholder.needs}
                            onChange={(e) =>
                              updateStakeholder(stakeholder.id, { needs: e.target.value })
                            }
                            rows={2}
                            className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                            placeholder="What are their key needs, concerns, or motivations?"
                          />
                        </div>
                      </div>
                      <div className="mt-3 flex justify-end">
                        <button
                          onClick={() => removeStakeholder(stakeholder.id)}
                          className="text-sm text-red-600 hover:text-red-800"
                        >
                          Remove Stakeholder
                        </button>
                      </div>
                    </div>
                  ))}
                  {data.stakeholders.length === 0 && (
                    <div className="text-center py-8 text-gray-500">
                      <p>No stakeholders added yet.</p>
                      <p className="text-sm mt-1">Click "Add Stakeholder" to get started.</p>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* AI Synthesis Tab */}
            {activeTab === 'synthesis' && (
              <div className="space-y-4">
                <div>
                  <h3 className="text-lg font-medium text-gray-900 mb-2">
                    AI-Powered Problem Synthesis
                  </h3>
                  <p className="text-sm text-gray-500 mb-4">
                    Use AI to synthesise your problem framing, refine HMW statements, and identify
                    patterns across stakeholders
                  </p>
                </div>

                <button
                  onClick={triggerAISynthesis}
                  disabled={synthesizing || data.hmwStatements.length === 0}
                  className="px-6 py-3 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {synthesizing ? 'Synthesising...' : 'Generate AI Synthesis'}
                </button>

                {data.hmwStatements.length === 0 && (
                  <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-md">
                    <p className="text-sm text-yellow-800">
                      Add at least one HMW statement in the Problem Framing tab to enable AI
                      synthesis.
                    </p>
                  </div>
                )}

                {data.synthesisResult && (
                  <div className="mt-6 space-y-6">
                    <h4 className="text-lg font-semibold text-gray-900">AI Synthesis Results</h4>
                    
                    {/* Refined Problem Statement */}
                    <div className="p-4 bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg">
                      <h5 className="text-sm font-semibold text-blue-900 mb-2">
                        Refined Problem Statement
                      </h5>
                      <p className="text-sm text-gray-800 leading-relaxed">
                        {data.synthesisResult.refinedProblemStatement}
                      </p>
                    </div>

                    {/* Alternative Framings */}
                    {data.synthesisResult.alternativeFramings.length > 0 && (
                      <div className="p-4 bg-purple-50 border border-purple-200 rounded-lg">
                        <h5 className="text-sm font-semibold text-purple-900 mb-2">
                          Alternative Problem Framings
                        </h5>
                        <ul className="space-y-2">
                          {data.synthesisResult.alternativeFramings.map((framing, idx) => (
                            <li key={idx} className="text-sm text-gray-800 flex">
                              <span className="mr-2 text-purple-600 font-semibold">{idx + 1}.</span>
                              <span className="flex-1">{framing}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Prioritized HMWs */}
                    {data.synthesisResult.prioritizedHMWs.length > 0 && (
                      <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                        <h5 className="text-sm font-semibold text-green-900 mb-2">
                          Prioritised HMW Statements
                        </h5>
                        <ul className="space-y-2">
                          {data.synthesisResult.prioritizedHMWs.map((hmw, idx) => (
                            <li key={idx} className="text-sm text-gray-800 flex">
                              <span className="mr-2 text-green-600 font-semibold">{idx + 1}.</span>
                              <span className="flex-1">{hmw}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Two Column Layout for Insights and Constraints/Opportunities */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      {/* Stakeholder Insights */}
                      {data.synthesisResult.stakeholderInsights.length > 0 && (
                        <div className="p-4 bg-orange-50 border border-orange-200 rounded-lg">
                          <h5 className="text-sm font-semibold text-orange-900 mb-2">
                            Stakeholder Insights
                          </h5>
                          <ul className="space-y-2">
                            {data.synthesisResult.stakeholderInsights.map((insight, idx) => (
                              <li key={idx} className="text-sm text-gray-800 flex">
                                <span className="mr-2 text-orange-600">•</span>
                                <span className="flex-1">{insight}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {/* Key Constraints */}
                      {data.synthesisResult.keyConstraints.length > 0 && (
                        <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                          <h5 className="text-sm font-semibold text-red-900 mb-2">
                            Key Constraints
                          </h5>
                          <ul className="space-y-2">
                            {data.synthesisResult.keyConstraints.map((constraint, idx) => (
                              <li key={idx} className="text-sm text-gray-800 flex">
                                <span className="mr-2 text-red-600">•</span>
                                <span className="flex-1">{constraint}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {/* Key Opportunities */}
                      {data.synthesisResult.opportunities.length > 0 && (
                        <div className="p-4 bg-teal-50 border border-teal-200 rounded-lg">
                          <h5 className="text-sm font-semibold text-teal-900 mb-2">
                            Key Opportunities
                          </h5>
                          <ul className="space-y-2">
                            {data.synthesisResult.opportunities.map((opportunity, idx) => (
                              <li key={idx} className="text-sm text-gray-800 flex">
                                <span className="mr-2 text-teal-600">•</span>
                                <span className="flex-1">{opportunity}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>

                    {/* Recommendations */}
                    {data.synthesisResult.recommendations.length > 0 && (
                      <div className="p-4 bg-indigo-50 border border-indigo-200 rounded-lg">
                        <h5 className="text-sm font-semibold text-indigo-900 mb-2">
                          Recommendations for Ideation Stage
                        </h5>
                        <ul className="space-y-2">
                          {data.synthesisResult.recommendations.map((rec, idx) => (
                            <li key={idx} className="text-sm text-gray-800 flex">
                              <span className="mr-2 text-indigo-600 font-semibold">→</span>
                              <span className="flex-1">{rec}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Save Button */}
        <div className="flex items-center justify-between bg-white rounded-lg shadow p-4">
          <div className="text-sm text-gray-500">
            {lastSaved && `Last saved: ${lastSaved.toLocaleTimeString()}`}
            {!lastSaved && 'Not saved yet'}
          </div>
          <button
            onClick={() => saveDefineData()}
            disabled={saving}
            className="px-6 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
          >
            {saving ? 'Saving...' : 'Save Progress'}
          </button>
        </div>

        {/* Next Steps Suggestion */}
        <div className="mt-6 bg-blue-50 rounded-lg p-4">
          <h3 className="text-sm font-medium text-blue-900 mb-2">Next Steps</h3>
          <ul className="text-sm text-blue-700 space-y-1">
            {completionScore < 50 && (
              <li>Continue building out your problem framing and stakeholder analysis</li>
            )}
            {completionScore >= 50 && completionScore < 100 && (
              <>
                <li>Use AI synthesis to refine your problem statements</li>
                <li>Review and prioritise your HMW statements</li>
              </>
            )}
            {completionScore === 100 && (
              <>
                <li>Your Define stage is complete!</li>
                <li>Move to the Ideate stage to generate solution ideas</li>
              </>
            )}
          </ul>
        </div>
      </div>
    </Layout>
  );
}

