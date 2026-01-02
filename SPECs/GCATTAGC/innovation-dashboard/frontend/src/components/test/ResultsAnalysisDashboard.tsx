import { useState } from 'react';
import type { TestSession, UserFeedback, MetricData } from '../../types/test';

interface TestData {
  sessions: TestSession[];
  feedback: UserFeedback[];
  metrics: MetricData[];
  synthesisResult?: string;
  lastModified?: string;
}

interface ResultsAnalysisDashboardProps {
  data: TestData;
  onDataChange: (data: TestData) => void;
  onSave: () => void;
}

export function ResultsAnalysisDashboard({
  data,
  onDataChange,
  onSave,
}: ResultsAnalysisDashboardProps) {
  const [showMetricForm, setShowMetricForm] = useState(false);
  const [selectedSession, setSelectedSession] = useState<string>('all');
  const [newMetric, setNewMetric] = useState<Partial<MetricData>>({
    sessionId: '',
    metricName: '',
    value: 0,
    unit: '',
    target: undefined,
    category: 'usability',
  });

  const addMetric = () => {
    if (!newMetric.sessionId || !newMetric.metricName) {
      alert('Please select a session and enter a metric name');
      return;
    }

    const metric: MetricData = {
      id: Date.now().toString(),
      sessionId: newMetric.sessionId || '',
      metricName: newMetric.metricName || '',
      value: newMetric.value || 0,
      unit: newMetric.unit || '',
      target: newMetric.target,
      category: newMetric.category || 'other',
    };

    onDataChange({
      ...data,
      metrics: [...data.metrics, metric],
    });

    setNewMetric({
      sessionId: '',
      metricName: '',
      value: 0,
      unit: '',
      target: undefined,
      category: 'usability',
    });
    setShowMetricForm(false);
  };

  const deleteMetric = (metricId: string) => {
    if (!confirm('Delete this metric?')) return;
    onDataChange({
      ...data,
      metrics: data.metrics.filter((m) => m.id !== metricId),
    });
  };

  // Filter feedback by selected session
  const filteredFeedback =
    selectedSession === 'all'
      ? data.feedback
      : data.feedback.filter((f) => f.sessionId === selectedSession);

  const filteredMetrics =
    selectedSession === 'all'
      ? data.metrics
      : data.metrics.filter((m) => m.sessionId === selectedSession);

  // Calculate statistics
  const calculateStats = () => {
    if (filteredFeedback.length === 0) {
      return {
        avgSatisfaction: 0,
        avgUsability: 0,
        totalFeedback: 0,
        totalSessions: data.sessions.length,
        topPainPoints: [],
        topPositives: [],
        topSuggestions: [],
      };
    }

    const avgSatisfaction =
      filteredFeedback.reduce((sum, f) => sum + f.satisfactionScore, 0) / filteredFeedback.length;
    const avgUsability =
      filteredFeedback.reduce((sum, f) => sum + f.usabilityScore, 0) / filteredFeedback.length;

    // Count pain points
    const painPointCounts: Record<string, number> = {};
    filteredFeedback.forEach((f) => {
      f.painPoints.forEach((point) => {
        painPointCounts[point] = (painPointCounts[point] || 0) + 1;
      });
    });

    // Count positive aspects
    const positiveCounts: Record<string, number> = {};
    filteredFeedback.forEach((f) => {
      f.positiveAspects.forEach((aspect) => {
        positiveCounts[aspect] = (positiveCounts[aspect] || 0) + 1;
      });
    });

    // Count suggestions
    const suggestionCounts: Record<string, number> = {};
    filteredFeedback.forEach((f) => {
      f.suggestions.forEach((suggestion) => {
        suggestionCounts[suggestion] = (suggestionCounts[suggestion] || 0) + 1;
      });
    });

    const topPainPoints = Object.entries(painPointCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([point, count]) => ({ point, count }));

    const topPositives = Object.entries(positiveCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([aspect, count]) => ({ aspect, count }));

    const topSuggestions = Object.entries(suggestionCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([suggestion, count]) => ({ suggestion, count }));

    return {
      avgSatisfaction: Math.round(avgSatisfaction * 10) / 10,
      avgUsability: Math.round(avgUsability * 10) / 10,
      totalFeedback: filteredFeedback.length,
      totalSessions: data.sessions.length,
      topPainPoints,
      topPositives,
      topSuggestions,
    };
  };

  const stats = calculateStats();

  const getScoreColor = (score: number) => {
    if (score >= 8) return 'text-green-600';
    if (score >= 6) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBgColor = (score: number) => {
    if (score >= 8) return 'bg-green-100 border-green-500';
    if (score >= 6) return 'bg-yellow-100 border-yellow-500';
    return 'bg-red-100 border-red-500';
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'usability':
        return 'bg-blue-100 text-blue-800';
      case 'performance':
        return 'bg-purple-100 text-purple-800';
      case 'satisfaction':
        return 'bg-green-100 text-green-800';
      case 'completion':
        return 'bg-yellow-100 text-yellow-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getMetricStatus = (value: number, target?: number) => {
    if (!target) return 'neutral';
    const percentage = (value / target) * 100;
    if (percentage >= 100) return 'success';
    if (percentage >= 80) return 'warning';
    return 'danger';
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'success':
        return 'text-green-600';
      case 'warning':
        return 'text-yellow-600';
      case 'danger':
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };

  return (
    <div className="space-y-6">
      {/* Session Filter */}
      <div className="flex items-center gap-4">
        <label className="text-sm font-medium text-gray-700">Filter by Session:</label>
        <select
          value={selectedSession}
          onChange={(e) => setSelectedSession(e.target.value)}
          className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
        >
          <option value="all">All Sessions</option>
          {data.sessions.map((session) => (
            <option key={session.id} value={session.id}>
              {session.sessionName}
            </option>
          ))}
        </select>
      </div>

      {/* Key Metrics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className={`p-4 rounded-lg border-2 ${getScoreBgColor(stats.avgSatisfaction)}`}>
          <div className="text-sm font-medium text-gray-700 mb-1">Avg Satisfaction</div>
          <div className={`text-3xl font-bold ${getScoreColor(stats.avgSatisfaction)}`}>
            {stats.avgSatisfaction}
            <span className="text-lg">/10</span>
          </div>
        </div>
        <div className={`p-4 rounded-lg border-2 ${getScoreBgColor(stats.avgUsability)}`}>
          <div className="text-sm font-medium text-gray-700 mb-1">Avg Usability</div>
          <div className={`text-3xl font-bold ${getScoreColor(stats.avgUsability)}`}>
            {stats.avgUsability}
            <span className="text-lg">/10</span>
          </div>
        </div>
        <div className="p-4 bg-white rounded-lg border-2 border-purple-200">
          <div className="text-sm font-medium text-gray-700 mb-1">Total Feedback</div>
          <div className="text-3xl font-bold text-purple-600">{stats.totalFeedback}</div>
        </div>
        <div className="p-4 bg-white rounded-lg border-2 border-purple-200">
          <div className="text-sm font-medium text-gray-700 mb-1">Test Sessions</div>
          <div className="text-3xl font-bold text-purple-600">{stats.totalSessions}</div>
        </div>
      </div>

      {/* Quantitative Metrics */}
      <div>
        <div className="flex justify-between items-center mb-4">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Quantitative Metrics</h3>
            <p className="text-sm text-gray-500 mt-1">
              Track specific performance and usability metrics
            </p>
          </div>
          <button
            onClick={() => {
              if (data.sessions.length === 0) {
                alert('Please create a test session first');
                return;
              }
              setShowMetricForm(!showMetricForm);
            }}
            className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
          >
            {showMetricForm ? 'Cancel' : 'Add Metric'}
          </button>
        </div>

        {/* Add Metric Form */}
        {showMetricForm && (
          <div className="mb-4 p-4 bg-purple-50 rounded-md border border-purple-200">
            <h4 className="text-sm font-medium text-gray-900 mb-3">Add Metric</h4>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">
                  Test Session *
                </label>
                <select
                  value={newMetric.sessionId}
                  onChange={(e) => setNewMetric({ ...newMetric, sessionId: e.target.value })}
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
                  Metric Name *
                </label>
                <input
                  type="text"
                  value={newMetric.metricName}
                  onChange={(e) => setNewMetric({ ...newMetric, metricName: e.target.value })}
                  placeholder="e.g., Task Completion Rate"
                  className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">Value *</label>
                <input
                  type="number"
                  value={newMetric.value}
                  onChange={(e) =>
                    setNewMetric({ ...newMetric, value: parseFloat(e.target.value) || 0 })
                  }
                  step="0.01"
                  className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">Unit</label>
                <input
                  type="text"
                  value={newMetric.unit}
                  onChange={(e) => setNewMetric({ ...newMetric, unit: e.target.value })}
                  placeholder="e.g., %, seconds, clicks"
                  className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">
                  Target (optional)
                </label>
                <input
                  type="number"
                  value={newMetric.target || ''}
                  onChange={(e) =>
                    setNewMetric({
                      ...newMetric,
                      target: e.target.value ? parseFloat(e.target.value) : undefined,
                    })
                  }
                  step="0.01"
                  placeholder="Target value"
                  className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1">Category</label>
                <select
                  value={newMetric.category}
                  onChange={(e) =>
                    setNewMetric({
                      ...newMetric,
                      category: e.target.value as MetricData['category'],
                    })
                  }
                  className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-purple-500"
                >
                  <option value="usability">Usability</option>
                  <option value="performance">Performance</option>
                  <option value="satisfaction">Satisfaction</option>
                  <option value="completion">Completion</option>
                  <option value="other">Other</option>
                </select>
              </div>
            </div>
            <div className="mt-3 flex justify-end">
              <button
                onClick={addMetric}
                className="px-4 py-2 bg-purple-600 text-white text-sm rounded-md hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
              >
                Add Metric
              </button>
            </div>
          </div>
        )}

        {/* Metrics List */}
        <div className="space-y-2">
          {filteredMetrics.map((metric) => {
            const session = data.sessions.find((s) => s.id === metric.sessionId);
            const status = getMetricStatus(metric.value, metric.target);
            return (
              <div
                key={metric.id}
                className="p-3 bg-white rounded-md border border-gray-200 hover:border-purple-300 transition-colors"
              >
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-1">
                      <h4 className="font-medium text-gray-900">{metric.metricName}</h4>
                      <span className={`text-xs px-2 py-0.5 rounded ${getCategoryColor(metric.category)}`}>
                        {metric.category}
                      </span>
                    </div>
                    <p className="text-xs text-gray-500">{session?.sessionName}</p>
                    <div className="mt-2 flex items-baseline gap-2">
                      <span className={`text-2xl font-bold ${getStatusColor(status)}`}>
                        {metric.value}
                        {metric.unit && <span className="text-sm ml-1">{metric.unit}</span>}
                      </span>
                      {metric.target && (
                        <span className="text-sm text-gray-600">
                          / {metric.target} {metric.unit} target
                        </span>
                      )}
                    </div>
                    {metric.target && (
                      <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full ${
                            status === 'success'
                              ? 'bg-green-500'
                              : status === 'warning'
                              ? 'bg-yellow-500'
                              : 'bg-red-500'
                          }`}
                          style={{
                            width: `${Math.min((metric.value / metric.target) * 100, 100)}%`,
                          }}
                        />
                      </div>
                    )}
                  </div>
                  <button
                    onClick={() => deleteMetric(metric.id)}
                    className="text-sm text-red-600 hover:text-red-800"
                  >
                    Delete
                  </button>
                </div>
              </div>
            );
          })}
          {filteredMetrics.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              <p>No metrics tracked yet.</p>
              <p className="text-sm mt-1">Click "Add Metric" to track quantitative metrics.</p>
            </div>
          )}
        </div>
      </div>

      {/* Qualitative Analysis */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Top Pain Points */}
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-3">Top Pain Points</h3>
          {stats.topPainPoints.length > 0 ? (
            <div className="space-y-2">
              {stats.topPainPoints.map((item, index) => (
                <div
                  key={index}
                  className="p-3 bg-red-50 rounded-md border border-red-200"
                >
                  <div className="flex justify-between items-start mb-1">
                    <p className="text-sm text-gray-900 flex-1">{item.point}</p>
                    <span className="text-xs font-medium text-red-600 ml-2">
                      {item.count}x
                    </span>
                  </div>
                  <div className="w-full bg-red-200 rounded-full h-1.5">
                    <div
                      className="bg-red-500 h-1.5 rounded-full"
                      style={{
                        width: `${(item.count / stats.totalFeedback) * 100}%`,
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-gray-500 italic">No pain points documented yet.</p>
          )}
        </div>

        {/* Top Positive Aspects */}
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-3">Top Positives</h3>
          {stats.topPositives.length > 0 ? (
            <div className="space-y-2">
              {stats.topPositives.map((item, index) => (
                <div
                  key={index}
                  className="p-3 bg-green-50 rounded-md border border-green-200"
                >
                  <div className="flex justify-between items-start mb-1">
                    <p className="text-sm text-gray-900 flex-1">{item.aspect}</p>
                    <span className="text-xs font-medium text-green-600 ml-2">
                      {item.count}x
                    </span>
                  </div>
                  <div className="w-full bg-green-200 rounded-full h-1.5">
                    <div
                      className="bg-green-500 h-1.5 rounded-full"
                      style={{
                        width: `${(item.count / stats.totalFeedback) * 100}%`,
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-gray-500 italic">No positive aspects documented yet.</p>
          )}
        </div>

        {/* Top Suggestions */}
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-3">Top Suggestions</h3>
          {stats.topSuggestions.length > 0 ? (
            <div className="space-y-2">
              {stats.topSuggestions.map((item, index) => (
                <div
                  key={index}
                  className="p-3 bg-blue-50 rounded-md border border-blue-200"
                >
                  <div className="flex justify-between items-start mb-1">
                    <p className="text-sm text-gray-900 flex-1">{item.suggestion}</p>
                    <span className="text-xs font-medium text-blue-600 ml-2">
                      {item.count}x
                    </span>
                  </div>
                  <div className="w-full bg-blue-200 rounded-full h-1.5">
                    <div
                      className="bg-blue-500 h-1.5 rounded-full"
                      style={{
                        width: `${(item.count / stats.totalFeedback) * 100}%`,
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-gray-500 italic">No suggestions documented yet.</p>
          )}
        </div>
      </div>

      {/* Analysis Summary */}
      {stats.totalFeedback > 0 && (
        <div className="bg-purple-50 rounded-lg p-4 border border-purple-200">
          <h3 className="text-sm font-medium text-purple-900 mb-2">Quick Analysis</h3>
          <ul className="text-sm text-purple-700 space-y-1">
            <li>
              Collected {stats.totalFeedback} feedback responses across {stats.totalSessions}{' '}
              test sessions
            </li>
            <li>
              Average satisfaction score: {stats.avgSatisfaction}/10 (
              {stats.avgSatisfaction >= 8
                ? 'Excellent'
                : stats.avgSatisfaction >= 6
                ? 'Good'
                : 'Needs Improvement'}
              )
            </li>
            <li>
              Average usability score: {stats.avgUsability}/10 (
              {stats.avgUsability >= 8
                ? 'Excellent'
                : stats.avgUsability >= 6
                ? 'Good'
                : 'Needs Improvement'}
              )
            </li>
            {stats.topPainPoints.length > 0 && (
              <li>
                Most critical pain point: "{stats.topPainPoints[0].point}" (mentioned{' '}
                {stats.topPainPoints[0].count} times)
              </li>
            )}
            {stats.topPositives.length > 0 && (
              <li>
                Top positive aspect: "{stats.topPositives[0].aspect}" (mentioned{' '}
                {stats.topPositives[0].count} times)
              </li>
            )}
          </ul>
        </div>
      )}
    </div>
  );
}


