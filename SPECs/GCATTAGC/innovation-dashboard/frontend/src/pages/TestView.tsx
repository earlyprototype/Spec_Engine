import { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { supabase } from '../lib/supabase';
import { Layout } from '../components/Layout';
import { FeedbackCollectionForm } from '../components/test/FeedbackCollectionForm';
import { ResultsAnalysisDashboard } from '../components/test/ResultsAnalysisDashboard';
import { TestAISynthesis } from '../components/test/TestAISynthesis';
import type { TestSession, UserFeedback, MetricData } from '../types/test';

interface TestData {
  sessions: TestSession[];
  feedback: UserFeedback[];
  metrics: MetricData[];
  synthesisResult?: string;
  lastModified?: string;
}

export function TestView() {
  const { projectId } = useParams<{ projectId: string }>();
  const [data, setData] = useState<TestData>({
    sessions: [],
    feedback: [],
    metrics: [],
  });
  const [activeTab, setActiveTab] = useState<'feedback' | 'analysis' | 'synthesis'>('feedback');
  const [saving, setSaving] = useState(false);
  const [lastSaved, setLastSaved] = useState<Date | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTestData();
  }, [projectId]);

  // Auto-save with 2-second debouncing (matches Discovery, Define, and Ideate pattern)
  useEffect(() => {
    const timer = setTimeout(() => {
      if (projectId && (data.sessions.length > 0 || data.feedback.length > 0)) {
        saveTestData(true);
      }
    }, 2000);

    return () => clearTimeout(timer);
  }, [data, projectId]);

  const loadTestData = async () => {
    if (!projectId) return;

    setLoading(true);
    const { data: stageData, error } = await supabase
      .from('stage_data')
      .select('*')
      .eq('project_id', projectId)
      .eq('stage_name', 'test')
      .single();

    if (error && error.code !== 'PGRST116') {
      console.error('Error loading test data:', error);
    } else if (stageData?.data_json) {
      setData(stageData.data_json as TestData);
    }
    setLoading(false);
  };

  const saveTestData = async (isAutoSave = false) => {
    if (!projectId) return;

    if (!isAutoSave) setSaving(true);

    const dataToSave = {
      ...data,
      lastModified: new Date().toISOString(),
    };

    const { error } = await supabase.from('stage_data').upsert(
      {
        project_id: projectId,
        stage_name: 'test',
        data_json: dataToSave,
      },
      { onConflict: 'project_id,stage_name' }
    );

    if (error) {
      console.error('Error saving test data:', error);
      if (!isAutoSave) alert('Error saving data: ' + error.message);
    } else {
      setLastSaved(new Date());
      setData(dataToSave);
    }

    if (!isAutoSave) setSaving(false);
  };

  const calculateCompletionScore = () => {
    let score = 0;
    if (data.sessions.length > 0) score += 30;
    if (data.feedback.length > 0) score += 30;
    if (data.metrics.length > 0) score += 20;
    if (data.synthesisResult) score += 20;
    return Math.min(score, 100);
  };

  const completionScore = calculateCompletionScore();

  if (loading) {
    return (
      <Layout>
        <div className="flex items-center justify-center h-64">
          <div className="text-gray-500">Loading test stage...</div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Test Stage</h1>
          <p className="text-gray-600">
            Collect user feedback, analyse test results, and generate insights to validate your prototypes
          </p>
        </div>

        {/* Progress Bar */}
        <div className="mb-6 bg-white rounded-lg shadow p-4">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700">Testing Progress</span>
            <span className="text-sm font-semibold text-purple-600">{completionScore}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-purple-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${completionScore}%` }}
            />
          </div>
          <div className="mt-2 text-xs text-gray-500">
            {completionScore < 100 && (
              <span>
                Add test sessions, collect feedback, and run analysis to complete your testing phase
              </span>
            )}
            {completionScore === 100 && (
              <span>Excellent! Your testing phase is comprehensive and well-documented.</span>
            )}
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="mb-6 bg-white rounded-lg shadow">
          <div className="border-b border-gray-200">
            <nav className="flex -mb-px">
              <button
                onClick={() => setActiveTab('feedback')}
                className={`py-4 px-6 text-sm font-medium border-b-2 transition-colors ${
                  activeTab === 'feedback'
                    ? 'border-purple-500 text-purple-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Feedback Collection
              </button>
              <button
                onClick={() => setActiveTab('analysis')}
                className={`py-4 px-6 text-sm font-medium border-b-2 transition-colors ${
                  activeTab === 'analysis'
                    ? 'border-purple-500 text-purple-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                Results Analysis
              </button>
              <button
                onClick={() => setActiveTab('synthesis')}
                className={`py-4 px-6 text-sm font-medium border-b-2 transition-colors ${
                  activeTab === 'synthesis'
                    ? 'border-purple-500 text-purple-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                AI Synthesis
              </button>
            </nav>
          </div>

          {/* Tab Content */}
          <div className="p-6">
            {activeTab === 'feedback' && (
              <FeedbackCollectionForm
                data={data}
                onDataChange={setData}
                onSave={() => saveTestData()}
              />
            )}
            {activeTab === 'analysis' && (
              <ResultsAnalysisDashboard
                data={data}
                onDataChange={setData}
                onSave={() => saveTestData()}
              />
            )}
            {activeTab === 'synthesis' && (
              <TestAISynthesis
                projectId={projectId || ''}
                data={data}
                onSynthesisComplete={(synthesis) => {
                  setData({ ...data, synthesisResult: synthesis });
                  saveTestData();
                }}
              />
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
            onClick={() => saveTestData()}
            disabled={saving}
            className="px-6 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50"
          >
            {saving ? 'Saving...' : 'Save Progress'}
          </button>
        </div>

        {/* Next Steps Suggestion */}
        <div className="mt-6 bg-purple-50 rounded-lg p-4">
          <h3 className="text-sm font-medium text-purple-900 mb-2">Next Steps</h3>
          <ul className="text-sm text-purple-700 space-y-1">
            {completionScore < 30 && (
              <>
                <li>Create test sessions and plan your user testing methodology</li>
                <li>Define metrics to track during testing</li>
              </>
            )}
            {completionScore >= 30 && completionScore < 60 && (
              <>
                <li>Collect feedback from test participants</li>
                <li>Document observations and pain points</li>
              </>
            )}
            {completionScore >= 60 && completionScore < 100 && (
              <>
                <li>Analyse results to identify patterns and trends</li>
                <li>Use AI synthesis to generate actionable insights</li>
              </>
            )}
            {completionScore === 100 && (
              <>
                <li>Your Test stage is complete!</li>
                <li>Review insights and prepare for iteration or deployment</li>
              </>
            )}
          </ul>
        </div>
      </div>
    </Layout>
  );
}

