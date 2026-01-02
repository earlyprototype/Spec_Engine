import { useState } from 'react';
import type { TestSession, UserFeedback, MetricData } from '../../types/test';

interface TestData {
  sessions: TestSession[];
  feedback: UserFeedback[];
  metrics: MetricData[];
  synthesisResult?: string;
  lastModified?: string;
}

interface FeedbackCollectionFormProps {
  data: TestData;
  onDataChange: (data: TestData) => void;
  onSave: () => void;
}

export function FeedbackCollectionForm({ data, onDataChange, onSave }: FeedbackCollectionFormProps) {
  const [showSessionForm, setShowSessionForm] = useState(false);
  const [showFeedbackForm, setShowFeedbackForm] = useState(false);
  const [selectedSession, setSelectedSession] = useState<string>('');
  
  // New session form state
  const [newSession, setNewSession] = useState<Partial<TestSession>>({
    sessionName: '',
    date: new Date().toISOString().split('T')[0],
    participants: 0,
    duration: 60,
    methodology: '',
    status: 'planned',
  });

  // New feedback form state
  const [newFeedback, setNewFeedback] = useState<Partial<UserFeedback>>({
    sessionId: '',
    participantName: '',
    satisfactionScore: 5,
    usabilityScore: 5,
    comments: '',
    painPoints: [],
    positiveAspects: [],
    suggestions: [],
  });

  const [currentPainPoint, setCurrentPainPoint] = useState('');
  const [currentPositive, setCurrentPositive] = useState('');
  const [currentSuggestion, setCurrentSuggestion] = useState('');

  const createTestSession = () => {
    if (!newSession.sessionName || !newSession.methodology) {
      alert('Please fill in session name and methodology');
      return;
    }

    const session: TestSession = {
      id: Date.now().toString(),
      sessionName: newSession.sessionName || '',
      date: newSession.date || new Date().toISOString().split('T')[0],
      participants: newSession.participants || 0,
      duration: newSession.duration || 60,
      methodology: newSession.methodology || '',
      status: newSession.status || 'planned',
    };

    onDataChange({
      ...data,
      sessions: [...data.sessions, session],
    });

    // Reset form
    setNewSession({
      sessionName: '',
      date: new Date().toISOString().split('T')[0],
      participants: 0,
      duration: 60,
      methodology: '',
      status: 'planned',
    });
    setShowSessionForm(false);
  };

  const addFeedback = () => {
    if (!newFeedback.sessionId || !newFeedback.participantName) {
      alert('Please select a session and enter participant name');
      return;
    }

    const feedback: UserFeedback = {
      id: Date.now().toString(),
      sessionId: newFeedback.sessionId || '',
      participantId: Date.now().toString(),
      participantName: newFeedback.participantName || '',
      timestamp: new Date().toISOString(),
      satisfactionScore: newFeedback.satisfactionScore || 5,
      usabilityScore: newFeedback.usabilityScore || 5,
      comments: newFeedback.comments || '',
      painPoints: newFeedback.painPoints || [],
      positiveAspects: newFeedback.positiveAspects || [],
      suggestions: newFeedback.suggestions || [],
    };

    onDataChange({
      ...data,
      feedback: [...data.feedback, feedback],
    });

    // Reset form
    setNewFeedback({
      sessionId: '',
      participantName: '',
      satisfactionScore: 5,
      usabilityScore: 5,
      comments: '',
      painPoints: [],
      positiveAspects: [],
      suggestions: [],
    });
    setShowFeedbackForm(false);
  };

  const addPainPoint = () => {
    if (!currentPainPoint.trim()) return;
    setNewFeedback({
      ...newFeedback,
      painPoints: [...(newFeedback.painPoints || []), currentPainPoint.trim()],
    });
    setCurrentPainPoint('');
  };

  const removePainPoint = (index: number) => {
    setNewFeedback({
      ...newFeedback,
      painPoints: (newFeedback.painPoints || []).filter((_, i) => i !== index),
    });
  };

  const addPositive = () => {
    if (!currentPositive.trim()) return;
    setNewFeedback({
      ...newFeedback,
      positiveAspects: [...(newFeedback.positiveAspects || []), currentPositive.trim()],
    });
    setCurrentPositive('');
  };

  const removePositive = (index: number) => {
    setNewFeedback({
      ...newFeedback,
      positiveAspects: (newFeedback.positiveAspects || []).filter((_, i) => i !== index),
    });
  };

  const addSuggestion = () => {
    if (!currentSuggestion.trim()) return;
    setNewFeedback({
      ...newFeedback,
      suggestions: [...(newFeedback.suggestions || []), currentSuggestion.trim()],
    });
    setCurrentSuggestion('');
  };

  const removeSuggestion = (index: number) => {
    setNewFeedback({
      ...newFeedback,
      suggestions: (newFeedback.suggestions || []).filter((_, i) => i !== index),
    });
  };

  const updateSessionStatus = (sessionId: string, status: TestSession['status']) => {
    onDataChange({
      ...data,
      sessions: data.sessions.map((s) => (s.id === sessionId ? { ...s, status } : s)),
    });
  };

  const deleteSession = (sessionId: string) => {
    if (!confirm('Delete this session and all its feedback?')) return;
    onDataChange({
      ...data,
      sessions: data.sessions.filter((s) => s.id !== sessionId),
      feedback: data.feedback.filter((f) => f.sessionId !== sessionId),
    });
  };

  const deleteFeedback = (feedbackId: string) => {
    if (!confirm('Delete this feedback entry?')) return;
    onDataChange({
      ...data,
      feedback: data.feedback.filter((f) => f.id !== feedbackId),
    });
  };

  const getStatusColor = (status: TestSession['status']) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'in_progress':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'planned':
        return 'bg-gray-100 text-gray-800 border-gray-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  return (
    <div className="space-y-6">
      {/* Test Sessions Section */}
      <div>
        <div className="flex justify-between items-center mb-4">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Test Sessions</h3>
            <p className="text-sm text-gray-500 mt-1">
              Plan and track your user testing sessions
            </p>
          </div>
          <button
            onClick={() => setShowSessionForm(!showSessionForm)}
            className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
          >
            {showSessionForm ? 'Cancel' : 'New Session'}
          </button>
        </div>

        {/* New Session Form */}
        {showSessionForm && (
          <div className="mb-4 p-4 bg-purple-50 rounded-md border border-purple-200">
            <h4 className="text-sm font-medium text-gray-900 mb-3">Create Test Session</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">
                  Session Name *
                </label>
                <input
                  type="text"
                  value={newSession.sessionName}
                  onChange={(e) => setNewSession({ ...newSession, sessionName: e.target.value })}
                  placeholder="e.g., Usability Test Round 1"
                  className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">Date</label>
                <input
                  type="date"
                  value={newSession.date}
                  onChange={(e) => setNewSession({ ...newSession, date: e.target.value })}
                  className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">
                  Participants
                </label>
                <input
                  type="number"
                  value={newSession.participants}
                  onChange={(e) =>
                    setNewSession({ ...newSession, participants: parseInt(e.target.value) || 0 })
                  }
                  min="0"
                  className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">
                  Duration (minutes)
                </label>
                <input
                  type="number"
                  value={newSession.duration}
                  onChange={(e) =>
                    setNewSession({ ...newSession, duration: parseInt(e.target.value) || 0 })
                  }
                  min="0"
                  className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
              <div className="md:col-span-2">
                <label className="block text-xs font-medium text-gray-700 mb-1">
                  Testing Methodology *
                </label>
                <textarea
                  value={newSession.methodology}
                  onChange={(e) => setNewSession({ ...newSession, methodology: e.target.value })}
                  placeholder="Describe your testing approach (e.g., moderated usability test, A/B testing, think-aloud protocol)"
                  rows={3}
                  className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">Status</label>
                <select
                  value={newSession.status}
                  onChange={(e) =>
                    setNewSession({
                      ...newSession,
                      status: e.target.value as TestSession['status'],
                    })
                  }
                  className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                >
                  <option value="planned">Planned</option>
                  <option value="in_progress">In Progress</option>
                  <option value="completed">Completed</option>
                </select>
              </div>
            </div>
            <div className="mt-3 flex justify-end">
              <button
                onClick={createTestSession}
                className="px-4 py-2 bg-purple-600 text-white text-sm rounded-md hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
              >
                Create Session
              </button>
            </div>
          </div>
        )}

        {/* Sessions List */}
        <div className="space-y-3">
          {data.sessions.map((session) => {
            const feedbackCount = data.feedback.filter((f) => f.sessionId === session.id).length;
            return (
              <div
                key={session.id}
                className="p-4 bg-white rounded-md border border-gray-200 hover:border-purple-300 transition-colors"
              >
                <div className="flex justify-between items-start mb-2">
                  <div className="flex-1">
                    <h4 className="font-medium text-gray-900">{session.sessionName}</h4>
                    <p className="text-sm text-gray-600 mt-1">{session.methodology}</p>
                  </div>
                  <span
                    className={`px-2 py-1 text-xs rounded border ${getStatusColor(
                      session.status
                    )}`}
                  >
                    {session.status.replace('_', ' ')}
                  </span>
                </div>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs text-gray-600 mb-3">
                  <div>Date: {session.date}</div>
                  <div>Participants: {session.participants}</div>
                  <div>Duration: {session.duration}min</div>
                  <div>Feedback: {feedbackCount}</div>
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => {
                      setSelectedSession(session.id);
                      setNewFeedback({ ...newFeedback, sessionId: session.id });
                      setShowFeedbackForm(true);
                    }}
                    className="text-sm text-purple-600 hover:text-purple-800"
                  >
                    Add Feedback
                  </button>
                  <select
                    value={session.status}
                    onChange={(e) =>
                      updateSessionStatus(session.id, e.target.value as TestSession['status'])
                    }
                    className="text-xs px-2 py-1 border border-gray-300 rounded"
                  >
                    <option value="planned">Planned</option>
                    <option value="in_progress">In Progress</option>
                    <option value="completed">Completed</option>
                  </select>
                  <button
                    onClick={() => deleteSession(session.id)}
                    className="text-sm text-red-600 hover:text-red-800"
                  >
                    Delete
                  </button>
                </div>
              </div>
            );
          })}
          {data.sessions.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              <p>No test sessions yet.</p>
              <p className="text-sm mt-1">Click "New Session" to create your first test session.</p>
            </div>
          )}
        </div>
      </div>

      {/* User Feedback Section */}
      <div>
        <div className="flex justify-between items-center mb-4">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">User Feedback</h3>
            <p className="text-sm text-gray-500 mt-1">
              Collect and document feedback from test participants
            </p>
          </div>
          <button
            onClick={() => {
              if (data.sessions.length === 0) {
                alert('Please create a test session first');
                return;
              }
              setShowFeedbackForm(!showFeedbackForm);
            }}
            className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
          >
            {showFeedbackForm ? 'Cancel' : 'Add Feedback'}
          </button>
        </div>

        {/* New Feedback Form */}
        {showFeedbackForm && (
          <div className="mb-4 p-4 bg-purple-50 rounded-md border border-purple-200">
            <h4 className="text-sm font-medium text-gray-900 mb-3">Add User Feedback</h4>
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-medium text-gray-700 mb-1">
                    Test Session *
                  </label>
                  <select
                    value={newFeedback.sessionId}
                    onChange={(e) =>
                      setNewFeedback({ ...newFeedback, sessionId: e.target.value })
                    }
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                  >
                    <option value="">Select session...</option>
                    {data.sessions.map((session) => (
                      <option key={session.id} value={session.id}>
                        {session.sessionName}
                      </option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-700 mb-1">
                    Participant Name *
                  </label>
                  <input
                    type="text"
                    value={newFeedback.participantName}
                    onChange={(e) =>
                      setNewFeedback({ ...newFeedback, participantName: e.target.value })
                    }
                    placeholder="e.g., Participant A, John Doe"
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-700 mb-1">
                    Satisfaction Score (1-10)
                  </label>
                  <input
                    type="range"
                    min="1"
                    max="10"
                    value={newFeedback.satisfactionScore}
                    onChange={(e) =>
                      setNewFeedback({
                        ...newFeedback,
                        satisfactionScore: parseInt(e.target.value),
                      })
                    }
                    className="w-full"
                  />
                  <div className="text-center text-sm font-medium text-purple-600">
                    {newFeedback.satisfactionScore}
                  </div>
                </div>
                <div>
                  <label className="block text-xs font-medium text-gray-700 mb-1">
                    Usability Score (1-10)
                  </label>
                  <input
                    type="range"
                    min="1"
                    max="10"
                    value={newFeedback.usabilityScore}
                    onChange={(e) =>
                      setNewFeedback({
                        ...newFeedback,
                        usabilityScore: parseInt(e.target.value),
                      })
                    }
                    className="w-full"
                  />
                  <div className="text-center text-sm font-medium text-purple-600">
                    {newFeedback.usabilityScore}
                  </div>
                </div>
              </div>

              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">Comments</label>
                <textarea
                  value={newFeedback.comments}
                  onChange={(e) => setNewFeedback({ ...newFeedback, comments: e.target.value })}
                  placeholder="Overall feedback and observations..."
                  rows={3}
                  className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>

              {/* Pain Points */}
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">Pain Points</label>
                <div className="flex gap-2 mb-2">
                  <input
                    type="text"
                    value={currentPainPoint}
                    onChange={(e) => setCurrentPainPoint(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && addPainPoint()}
                    placeholder="Add a pain point..."
                    className="flex-1 px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                  />
                  <button
                    onClick={addPainPoint}
                    className="px-3 py-2 bg-red-600 text-white text-sm rounded-md hover:bg-red-700"
                  >
                    Add
                  </button>
                </div>
                <div className="flex flex-wrap gap-2">
                  {newFeedback.painPoints?.map((point, index) => (
                    <span
                      key={index}
                      className="inline-flex items-center gap-1 px-2 py-1 bg-red-100 text-red-800 text-xs rounded"
                    >
                      {point}
                      <button
                        onClick={() => removePainPoint(index)}
                        className="text-red-600 hover:text-red-800"
                      >
                        ×
                      </button>
                    </span>
                  ))}
                </div>
              </div>

              {/* Positive Aspects */}
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">
                  Positive Aspects
                </label>
                <div className="flex gap-2 mb-2">
                  <input
                    type="text"
                    value={currentPositive}
                    onChange={(e) => setCurrentPositive(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && addPositive()}
                    placeholder="Add a positive aspect..."
                    className="flex-1 px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                  />
                  <button
                    onClick={addPositive}
                    className="px-3 py-2 bg-green-600 text-white text-sm rounded-md hover:bg-green-700"
                  >
                    Add
                  </button>
                </div>
                <div className="flex flex-wrap gap-2">
                  {newFeedback.positiveAspects?.map((aspect, index) => (
                    <span
                      key={index}
                      className="inline-flex items-center gap-1 px-2 py-1 bg-green-100 text-green-800 text-xs rounded"
                    >
                      {aspect}
                      <button
                        onClick={() => removePositive(index)}
                        className="text-green-600 hover:text-green-800"
                      >
                        ×
                      </button>
                    </span>
                  ))}
                </div>
              </div>

              {/* Suggestions */}
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">
                  Improvement Suggestions
                </label>
                <div className="flex gap-2 mb-2">
                  <input
                    type="text"
                    value={currentSuggestion}
                    onChange={(e) => setCurrentSuggestion(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && addSuggestion()}
                    placeholder="Add a suggestion..."
                    className="flex-1 px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                  />
                  <button
                    onClick={addSuggestion}
                    className="px-3 py-2 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700"
                  >
                    Add
                  </button>
                </div>
                <div className="flex flex-wrap gap-2">
                  {newFeedback.suggestions?.map((suggestion, index) => (
                    <span
                      key={index}
                      className="inline-flex items-center gap-1 px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded"
                    >
                      {suggestion}
                      <button
                        onClick={() => removeSuggestion(index)}
                        className="text-blue-600 hover:text-blue-800"
                      >
                        ×
                      </button>
                    </span>
                  ))}
                </div>
              </div>
            </div>
            <div className="mt-4 flex justify-end">
              <button
                onClick={addFeedback}
                className="px-4 py-2 bg-purple-600 text-white text-sm rounded-md hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
              >
                Submit Feedback
              </button>
            </div>
          </div>
        )}

        {/* Feedback List */}
        <div className="space-y-3">
          {data.feedback.map((feedback) => {
            const session = data.sessions.find((s) => s.id === feedback.sessionId);
            return (
              <div
                key={feedback.id}
                className="p-4 bg-white rounded-md border border-gray-200 hover:border-purple-300 transition-colors"
              >
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <h4 className="font-medium text-gray-900">{feedback.participantName}</h4>
                    <p className="text-xs text-gray-500">
                      {session?.sessionName} • {new Date(feedback.timestamp).toLocaleString()}
                    </p>
                  </div>
                  <button
                    onClick={() => deleteFeedback(feedback.id)}
                    className="text-sm text-red-600 hover:text-red-800"
                  >
                    Delete
                  </button>
                </div>
                <div className="grid grid-cols-2 gap-2 mb-3">
                  <div className="text-sm">
                    <span className="text-gray-600">Satisfaction:</span>
                    <span className="ml-2 font-medium text-purple-600">
                      {feedback.satisfactionScore}/10
                    </span>
                  </div>
                  <div className="text-sm">
                    <span className="text-gray-600">Usability:</span>
                    <span className="ml-2 font-medium text-purple-600">
                      {feedback.usabilityScore}/10
                    </span>
                  </div>
                </div>
                {feedback.comments && (
                  <p className="text-sm text-gray-700 mb-2">{feedback.comments}</p>
                )}
                <div className="space-y-2">
                  {feedback.painPoints.length > 0 && (
                    <div>
                      <span className="text-xs font-medium text-red-700">Pain Points:</span>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {feedback.painPoints.map((point, index) => (
                          <span
                            key={index}
                            className="text-xs px-2 py-0.5 bg-red-100 text-red-800 rounded"
                          >
                            {point}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                  {feedback.positiveAspects.length > 0 && (
                    <div>
                      <span className="text-xs font-medium text-green-700">Positive:</span>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {feedback.positiveAspects.map((aspect, index) => (
                          <span
                            key={index}
                            className="text-xs px-2 py-0.5 bg-green-100 text-green-800 rounded"
                          >
                            {aspect}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                  {feedback.suggestions.length > 0 && (
                    <div>
                      <span className="text-xs font-medium text-blue-700">Suggestions:</span>
                      <div className="flex flex-wrap gap-1 mt-1">
                        {feedback.suggestions.map((suggestion, index) => (
                          <span
                            key={index}
                            className="text-xs px-2 py-0.5 bg-blue-100 text-blue-800 rounded"
                          >
                            {suggestion}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </div>
            );
          })}
          {data.feedback.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              <p>No feedback collected yet.</p>
              <p className="text-sm mt-1">Click "Add Feedback" to document participant feedback.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}


