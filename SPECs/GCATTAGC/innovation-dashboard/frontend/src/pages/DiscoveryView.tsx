import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { supabase } from '../lib/supabase';
import { Layout } from '../components/Layout';
import { generateDiscoverySynthesis, type SynthesisResult } from '../services/geminiService';

interface DiscoveryData {
  userResearch: {
    interviews: Array<{
      id: string;
      participantName: string;
      date: string;
      notes: string;
      keyQuotes: string[];
    }>;
    surveys: Array<{
      id: string;
      title: string;
      responses: string;
      insights: string;
    }>;
    demographics: string;
  };
  observations: {
    fieldNotes: Array<{
      id: string;
      date: string;
      context: string;
      observation: string;
    }>;
    contextualFindings: string;
  };
  insights: {
    patterns: string[];
    themes: string[];
    opportunities: string[];
    challenges: string[];
  };
  synthesis?: {
    aiGenerated: string;
    userRefined: string;
    timestamp: string;
  };
}

const defaultDiscoveryData: DiscoveryData = {
  userResearch: {
    interviews: [],
    surveys: [],
    demographics: '',
  },
  observations: {
    fieldNotes: [],
    contextualFindings: '',
  },
  insights: {
    patterns: [],
    themes: [],
    opportunities: [],
    challenges: [],
  },
};

export function DiscoveryView() {
  const { projectId } = useParams<{ projectId: string }>();
  const [data, setData] = useState<DiscoveryData>(defaultDiscoveryData);
  const [saving, setSaving] = useState(false);
  const [lastSaved, setLastSaved] = useState<Date | null>(null);
  const [activeTab, setActiveTab] = useState<'research' | 'observations' | 'insights' | 'synthesis'>('research');
  const [synthesizing, setSynthesizing] = useState(false);

  // Load existing data
  useEffect(() => {
    loadDiscoveryData();
  }, [projectId]);

  const loadDiscoveryData = async () => {
    if (!projectId) return;

    const { data: stageData, error } = await supabase
      .from('stage_data')
      .select('*')
      .eq('project_id', projectId)
      .eq('stage_name', 'discovery')
      .single();

    if (error && error.code !== 'PGRST116') {
      console.error('Error loading discovery data:', error);
    } else if (stageData?.data_json) {
      setData({ ...defaultDiscoveryData, ...stageData.data_json });
    }
  };

  // Auto-save with debouncing
  useEffect(() => {
    const timer = setTimeout(() => {
      if (projectId) {
        saveDiscoveryData();
      }
    }, 2000);

    return () => clearTimeout(timer);
  }, [data, projectId]);

  const saveDiscoveryData = async () => {
    if (!projectId) return;

    setSaving(true);

    const { error } = await supabase.from('stage_data').upsert(
      {
        project_id: projectId,
        stage_name: 'discovery',
        data_json: data,
      },
      { onConflict: 'project_id,stage_name' }
    );

    if (error) {
      console.error('Error saving discovery data:', error);
    } else {
      setLastSaved(new Date());
    }
    setSaving(false);
  };

  // Add new interview
  const addInterview = () => {
    setData({
      ...data,
      userResearch: {
        ...data.userResearch,
        interviews: [
          ...data.userResearch.interviews,
          {
            id: Date.now().toString(),
            participantName: '',
            date: new Date().toISOString().split('T')[0],
            notes: '',
            keyQuotes: [],
          },
        ],
      },
    });
  };

  // Update interview
  const updateInterview = (id: string, field: string, value: any) => {
    setData({
      ...data,
      userResearch: {
        ...data.userResearch,
        interviews: data.userResearch.interviews.map((interview) =>
          interview.id === id ? { ...interview, [field]: value } : interview
        ),
      },
    });
  };

  // Delete interview
  const deleteInterview = (id: string) => {
    setData({
      ...data,
      userResearch: {
        ...data.userResearch,
        interviews: data.userResearch.interviews.filter((interview) => interview.id !== id),
      },
    });
  };

  // Add new survey
  const addSurvey = () => {
    setData({
      ...data,
      userResearch: {
        ...data.userResearch,
        surveys: [
          ...data.userResearch.surveys,
          {
            id: Date.now().toString(),
            title: '',
            responses: '',
            insights: '',
          },
        ],
      },
    });
  };

  // Update survey
  const updateSurvey = (id: string, field: string, value: string) => {
    setData({
      ...data,
      userResearch: {
        ...data.userResearch,
        surveys: data.userResearch.surveys.map((survey) =>
          survey.id === id ? { ...survey, [field]: value } : survey
        ),
      },
    });
  };

  // Delete survey
  const deleteSurvey = (id: string) => {
    setData({
      ...data,
      userResearch: {
        ...data.userResearch,
        surveys: data.userResearch.surveys.filter((survey) => survey.id !== id),
      },
    });
  };

  // Add field note
  const addFieldNote = () => {
    setData({
      ...data,
      observations: {
        ...data.observations,
        fieldNotes: [
          ...data.observations.fieldNotes,
          {
            id: Date.now().toString(),
            date: new Date().toISOString().split('T')[0],
            context: '',
            observation: '',
          },
        ],
      },
    });
  };

  // Update field note
  const updateFieldNote = (id: string, field: string, value: string) => {
    setData({
      ...data,
      observations: {
        ...data.observations,
        fieldNotes: data.observations.fieldNotes.map((note) =>
          note.id === id ? { ...note, [field]: value } : note
        ),
      },
    });
  };

  // Delete field note
  const deleteFieldNote = (id: string) => {
    setData({
      ...data,
      observations: {
        ...data.observations,
        fieldNotes: data.observations.fieldNotes.filter((note) => note.id !== id),
      },
    });
  };

  // Add insight item
  const addInsightItem = (category: keyof DiscoveryData['insights']) => {
    setData({
      ...data,
      insights: {
        ...data.insights,
        [category]: [...data.insights[category], ''],
      },
    });
  };

  // Update insight item
  const updateInsightItem = (category: keyof DiscoveryData['insights'], index: number, value: string) => {
    const updatedItems = [...data.insights[category]];
    updatedItems[index] = value;
    setData({
      ...data,
      insights: {
        ...data.insights,
        [category]: updatedItems,
      },
    });
  };

  // Delete insight item
  const deleteInsightItem = (category: keyof DiscoveryData['insights'], index: number) => {
    setData({
      ...data,
      insights: {
        ...data.insights,
        [category]: data.insights[category].filter((_, i) => i !== index),
      },
    });
  };

  // Calculate completeness
  const calculateCompleteness = (): number => {
    let total = 0;
    let completed = 0;

    // User Research (40%)
    total += 4;
    if (data.userResearch.interviews.length > 0) completed++;
    if (data.userResearch.surveys.length > 0) completed++;
    if (data.userResearch.demographics.trim().length > 0) completed++;
    if (data.userResearch.interviews.some(i => i.notes.trim().length > 50)) completed++;

    // Observations (30%)
    total += 3;
    if (data.observations.fieldNotes.length > 0) completed++;
    if (data.observations.contextualFindings.trim().length > 0) completed++;
    if (data.observations.fieldNotes.some(n => n.observation.trim().length > 50)) completed++;

    // Insights (30%)
    total += 3;
    if (data.insights.patterns.length > 0) completed++;
    if (data.insights.themes.length > 0) completed++;
    if (data.insights.opportunities.length > 0) completed++;

    return Math.round((completed / total) * 100);
  };

  // AI Synthesis with Gemini
  const triggerSynthesis = async () => {
    setSynthesizing(true);
    try {
      const result: SynthesisResult = await generateDiscoverySynthesis(data);
      
      // Format the synthesis result into readable text
      const synthesisText = `## Executive Summary

${result.summary}

## Key Insights

${result.keyInsights.map((insight, i) => `${i + 1}. ${insight}`).join('\n')}

## User Needs Identified

${result.userNeeds.map((need, i) => `${i + 1}. ${need}`).join('\n')}

## Recommendations for Define Stage

${result.recommendations.map((rec, i) => `${i + 1}. ${rec}`).join('\n')}

## Problem Areas to Explore

${result.problemAreas.map((problem, i) => `${i + 1}. ${problem}`).join('\n')}`;
      
      setData({
        ...data,
        synthesis: {
          aiGenerated: synthesisText,
          userRefined: data.synthesis?.userRefined || '',
          timestamp: new Date().toISOString(),
        },
      });
    } catch (error) {
      console.error('Error generating synthesis:', error);
      const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
      alert(`Error generating synthesis: ${errorMessage}\n\nPlease ensure your Gemini API key is configured in the .env file.`);
    } finally {
      setSynthesizing(false);
    }
  };

  const completeness = calculateCompleteness();

  return (
    <Layout>
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Discovery Stage</h1>
          <p className="text-gray-600">Understand the users, their needs, and the problem space.</p>
        </div>

        {/* Progress Bar */}
        <div className="mb-6 bg-white rounded-lg shadow p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="text-sm font-medium text-gray-700">Discovery Progress</span>
            <span className="text-sm font-semibold text-primary-600">{completeness}% Complete</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-primary-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${completeness}%` }}
            />
          </div>
          <div className="mt-2 text-xs text-gray-500 flex items-center justify-between">
            <span>{saving ? 'Saving...' : lastSaved ? `Saved ${lastSaved.toLocaleTimeString()}` : 'Not saved'}</span>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="mb-6 border-b border-gray-200">
          <nav className="flex space-x-8" aria-label="Discovery Tabs">
            {[
              { id: 'research', label: 'User Research' },
              { id: 'observations', label: 'Observations' },
              { id: 'insights', label: 'Insights' },
              { id: 'synthesis', label: 'AI Synthesis' },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`py-4 px-1 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-primary-500 text-primary-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        {/* Tab Content */}
        <div className="bg-white rounded-lg shadow p-6">
          {/* User Research Tab */}
          {activeTab === 'research' && (
            <div className="space-y-6">
              <div>
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-semibold text-gray-900">Interviews</h2>
                  <button
                    onClick={addInterview}
                    className="px-4 py-2 bg-primary-600 text-white text-sm rounded-md hover:bg-primary-700"
                  >
                    + Add Interview
                  </button>
                </div>
                {data.userResearch.interviews.length === 0 ? (
                  <p className="text-gray-500 text-sm italic">No interviews added yet. Click "Add Interview" to get started.</p>
                ) : (
                  <div className="space-y-4">
                    {data.userResearch.interviews.map((interview) => (
                      <div key={interview.id} className="border border-gray-200 rounded-lg p-4">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-3">
                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Participant Name</label>
                            <input
                              type="text"
                              value={interview.participantName}
                              onChange={(e) => updateInterview(interview.id, 'participantName', e.target.value)}
                              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                              placeholder="e.g., User A, Participant 1"
                            />
                          </div>
                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Date</label>
                            <input
                              type="date"
                              value={interview.date}
                              onChange={(e) => updateInterview(interview.id, 'date', e.target.value)}
                              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                            />
                          </div>
                        </div>
                        <div className="mb-3">
                          <label className="block text-sm font-medium text-gray-700 mb-1">Interview Notes</label>
                          <textarea
                            value={interview.notes}
                            onChange={(e) => updateInterview(interview.id, 'notes', e.target.value)}
                            rows={4}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                            placeholder="Record key insights, behaviours, pain points, goals..."
                          />
                        </div>
                        <button
                          onClick={() => deleteInterview(interview.id)}
                          className="text-sm text-red-600 hover:text-red-800"
                        >
                          Delete Interview
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div>
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-semibold text-gray-900">Surveys</h2>
                  <button
                    onClick={addSurvey}
                    className="px-4 py-2 bg-primary-600 text-white text-sm rounded-md hover:bg-primary-700"
                  >
                    + Add Survey
                  </button>
                </div>
                {data.userResearch.surveys.length === 0 ? (
                  <p className="text-gray-500 text-sm italic">No surveys added yet.</p>
                ) : (
                  <div className="space-y-4">
                    {data.userResearch.surveys.map((survey) => (
                      <div key={survey.id} className="border border-gray-200 rounded-lg p-4">
                        <div className="mb-3">
                          <label className="block text-sm font-medium text-gray-700 mb-1">Survey Title</label>
                          <input
                            type="text"
                            value={survey.title}
                            onChange={(e) => updateSurvey(survey.id, 'title', e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                            placeholder="e.g., User Satisfaction Survey"
                          />
                        </div>
                        <div className="mb-3">
                          <label className="block text-sm font-medium text-gray-700 mb-1">Response Summary</label>
                          <textarea
                            value={survey.responses}
                            onChange={(e) => updateSurvey(survey.id, 'responses', e.target.value)}
                            rows={3}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                            placeholder="Summarise key response data..."
                          />
                        </div>
                        <div className="mb-3">
                          <label className="block text-sm font-medium text-gray-700 mb-1">Key Insights</label>
                          <textarea
                            value={survey.insights}
                            onChange={(e) => updateSurvey(survey.id, 'insights', e.target.value)}
                            rows={2}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                            placeholder="What did you learn?"
                          />
                        </div>
                        <button
                          onClick={() => deleteSurvey(survey.id)}
                          className="text-sm text-red-600 hover:text-red-800"
                        >
                          Delete Survey
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div>
                <h2 className="text-xl font-semibold text-gray-900 mb-4">User Demographics</h2>
                <textarea
                  value={data.userResearch.demographics}
                  onChange={(e) => setData({ ...data, userResearch: { ...data.userResearch, demographics: e.target.value } })}
                  rows={4}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  placeholder="Describe your target users: age range, occupation, technical proficiency, goals, pain points..."
                />
              </div>
            </div>
          )}

          {/* Observations Tab */}
          {activeTab === 'observations' && (
            <div className="space-y-6">
              <div>
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-semibold text-gray-900">Field Notes</h2>
                  <button
                    onClick={addFieldNote}
                    className="px-4 py-2 bg-primary-600 text-white text-sm rounded-md hover:bg-primary-700"
                  >
                    + Add Field Note
                  </button>
                </div>
                {data.observations.fieldNotes.length === 0 ? (
                  <p className="text-gray-500 text-sm italic">No field notes added yet.</p>
                ) : (
                  <div className="space-y-4">
                    {data.observations.fieldNotes.map((note) => (
                      <div key={note.id} className="border border-gray-200 rounded-lg p-4">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-3">
                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Date</label>
                            <input
                              type="date"
                              value={note.date}
                              onChange={(e) => updateFieldNote(note.id, 'date', e.target.value)}
                              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                            />
                          </div>
                          <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Context/Location</label>
                            <input
                              type="text"
                              value={note.context}
                              onChange={(e) => updateFieldNote(note.id, 'context', e.target.value)}
                              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                              placeholder="e.g., Office, Home, Workshop"
                            />
                          </div>
                        </div>
                        <div className="mb-3">
                          <label className="block text-sm font-medium text-gray-700 mb-1">Observation</label>
                          <textarea
                            value={note.observation}
                            onChange={(e) => updateFieldNote(note.id, 'observation', e.target.value)}
                            rows={4}
                            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                            placeholder="What did you observe? Behaviours, environment, interactions..."
                          />
                        </div>
                        <button
                          onClick={() => deleteFieldNote(note.id)}
                          className="text-sm text-red-600 hover:text-red-800"
                        >
                          Delete Field Note
                        </button>
                      </div>
                    ))}
                  </div>
                )}
              </div>

              <div>
                <h2 className="text-xl font-semibold text-gray-900 mb-4">Contextual Findings</h2>
                <textarea
                  value={data.observations.contextualFindings}
                  onChange={(e) => setData({ ...data, observations: { ...data.observations, contextualFindings: e.target.value } })}
                  rows={6}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                  placeholder="Describe the broader context: environmental factors, social dynamics, workflow patterns, cultural considerations..."
                />
              </div>
            </div>
          )}

          {/* Insights Tab */}
          {activeTab === 'insights' && (
            <div className="space-y-6">
              {/* Patterns */}
              <div>
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-semibold text-gray-900">Patterns</h2>
                  <button
                    onClick={() => addInsightItem('patterns')}
                    className="px-4 py-2 bg-primary-600 text-white text-sm rounded-md hover:bg-primary-700"
                  >
                    + Add Pattern
                  </button>
                </div>
                <div className="space-y-2">
                  {data.insights.patterns.map((pattern, index) => (
                    <div key={index} className="flex items-center gap-2">
                      <input
                        type="text"
                        value={pattern}
                        onChange={(e) => updateInsightItem('patterns', index, e.target.value)}
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                        placeholder="Describe a recurring pattern you noticed..."
                      />
                      <button
                        onClick={() => deleteInsightItem('patterns', index)}
                        className="text-red-600 hover:text-red-800 px-2"
                      >
                        ✕
                      </button>
                    </div>
                  ))}
                  {data.insights.patterns.length === 0 && (
                    <p className="text-gray-500 text-sm italic">No patterns identified yet.</p>
                  )}
                </div>
              </div>

              {/* Themes */}
              <div>
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-semibold text-gray-900">Themes</h2>
                  <button
                    onClick={() => addInsightItem('themes')}
                    className="px-4 py-2 bg-primary-600 text-white text-sm rounded-md hover:bg-primary-700"
                  >
                    + Add Theme
                  </button>
                </div>
                <div className="space-y-2">
                  {data.insights.themes.map((theme, index) => (
                    <div key={index} className="flex items-center gap-2">
                      <input
                        type="text"
                        value={theme}
                        onChange={(e) => updateInsightItem('themes', index, e.target.value)}
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                        placeholder="Describe an overarching theme..."
                      />
                      <button
                        onClick={() => deleteInsightItem('themes', index)}
                        className="text-red-600 hover:text-red-800 px-2"
                      >
                        ✕
                      </button>
                    </div>
                  ))}
                  {data.insights.themes.length === 0 && (
                    <p className="text-gray-500 text-sm italic">No themes identified yet.</p>
                  )}
                </div>
              </div>

              {/* Opportunities */}
              <div>
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-semibold text-gray-900">Opportunities</h2>
                  <button
                    onClick={() => addInsightItem('opportunities')}
                    className="px-4 py-2 bg-primary-600 text-white text-sm rounded-md hover:bg-primary-700"
                  >
                    + Add Opportunity
                  </button>
                </div>
                <div className="space-y-2">
                  {data.insights.opportunities.map((opportunity, index) => (
                    <div key={index} className="flex items-center gap-2">
                      <input
                        type="text"
                        value={opportunity}
                        onChange={(e) => updateInsightItem('opportunities', index, e.target.value)}
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                        placeholder="Describe a potential opportunity..."
                      />
                      <button
                        onClick={() => deleteInsightItem('opportunities', index)}
                        className="text-red-600 hover:text-red-800 px-2"
                      >
                        ✕
                      </button>
                    </div>
                  ))}
                  {data.insights.opportunities.length === 0 && (
                    <p className="text-gray-500 text-sm italic">No opportunities identified yet.</p>
                  )}
                </div>
              </div>

              {/* Challenges */}
              <div>
                <div className="flex items-center justify-between mb-4">
                  <h2 className="text-xl font-semibold text-gray-900">Challenges</h2>
                  <button
                    onClick={() => addInsightItem('challenges')}
                    className="px-4 py-2 bg-primary-600 text-white text-sm rounded-md hover:bg-primary-700"
                  >
                    + Add Challenge
                  </button>
                </div>
                <div className="space-y-2">
                  {data.insights.challenges.map((challenge, index) => (
                    <div key={index} className="flex items-center gap-2">
                      <input
                        type="text"
                        value={challenge}
                        onChange={(e) => updateInsightItem('challenges', index, e.target.value)}
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                        placeholder="Describe a key challenge or pain point..."
                      />
                      <button
                        onClick={() => deleteInsightItem('challenges', index)}
                        className="text-red-600 hover:text-red-800 px-2"
                      >
                        ✕
                      </button>
                    </div>
                  ))}
                  {data.insights.challenges.length === 0 && (
                    <p className="text-gray-500 text-sm italic">No challenges identified yet.</p>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Synthesis Tab */}
          {activeTab === 'synthesis' && (
            <div className="space-y-6">
              <div>
                <h2 className="text-xl font-semibold text-gray-900 mb-4">AI-Powered Synthesis</h2>
                <p className="text-gray-600 mb-4">
                  Use AI to analyse all your discovery data and generate insights, patterns, and recommendations.
                </p>
                <button
                  onClick={triggerSynthesis}
                  disabled={synthesizing || completeness < 30}
                  className="px-6 py-3 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {synthesizing ? 'Generating Synthesis...' : 'Generate AI Synthesis'}
                </button>
                {completeness < 30 && (
                  <p className="mt-2 text-sm text-amber-600">
                    Complete at least 30% of discovery activities to enable AI synthesis.
                  </p>
                )}
              </div>

              {data.synthesis && (
                <div className="space-y-4">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">AI-Generated Insights</h3>
                    <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                      <p className="text-gray-800 whitespace-pre-wrap">{data.synthesis.aiGenerated}</p>
                      <p className="text-xs text-gray-500 mt-2">
                        Generated: {new Date(data.synthesis.timestamp).toLocaleString()}
                      </p>
                    </div>
                  </div>

                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-2">Your Refinements</h3>
                    <textarea
                      value={data.synthesis.userRefined}
                      onChange={(e) =>
                        setData({
                          ...data,
                          synthesis: data.synthesis ? { ...data.synthesis, userRefined: e.target.value } : undefined,
                        })
                      }
                      rows={6}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                      placeholder="Refine or add to the AI-generated insights based on your expertise..."
                    />
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Suggested Actions */}
        <div className="mt-6 bg-blue-50 rounded-lg p-4">
          <h3 className="text-sm font-medium text-blue-900 mb-2">Suggested Next Steps</h3>
          <ul className="text-sm text-blue-700 space-y-1">
            {completeness < 40 && <li>• Add at least one interview or survey to capture user insights</li>}
            {data.observations.fieldNotes.length === 0 && <li>• Record field observations from user environments</li>}
            {data.insights.patterns.length === 0 && <li>• Identify patterns emerging from your research</li>}
            {completeness >= 30 && !data.synthesis && <li>• Generate AI synthesis to analyse your findings</li>}
            {completeness >= 70 && <li>• Move to the Define stage to frame the problem</li>}
          </ul>
        </div>
      </div>
    </Layout>
  );
}

