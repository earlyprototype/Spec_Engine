import { useState } from 'react';
import type { TestSession, UserFeedback, MetricData } from '../../types/test';

interface TestData {
  sessions: TestSession[];
  feedback: UserFeedback[];
  metrics: MetricData[];
  synthesisResult?: string;
  lastModified?: string;
}

interface TestAISynthesisProps {
  projectId: string;
  data: TestData;
  onSynthesisComplete: (synthesis: string) => void;
}

export function TestAISynthesis({ projectId, data, onSynthesisComplete }: TestAISynthesisProps) {
  const [synthesizing, setSynthesizing] = useState(false);
  const [synthesisType, setSynthesisType] = useState<'overview' | 'insights' | 'recommendations'>(
    'overview'
  );

  const generateSynthesis = async () => {
    if (data.feedback.length === 0) {
      alert('Please collect some user feedback before generating synthesis');
      return;
    }

    setSynthesizing(true);

    // Calculate statistics for synthesis input
    const avgSatisfaction =
      data.feedback.reduce((sum, f) => sum + f.satisfactionScore, 0) / data.feedback.length;
    const avgUsability =
      data.feedback.reduce((sum, f) => sum + f.usabilityScore, 0) / data.feedback.length;

    // Aggregate pain points
    const allPainPoints = data.feedback.flatMap((f) => f.painPoints);
    const painPointCounts: Record<string, number> = {};
    allPainPoints.forEach((point) => {
      painPointCounts[point] = (painPointCounts[point] || 0) + 1;
    });
    const topPainPoints = Object.entries(painPointCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5);

    // Aggregate positive aspects
    const allPositives = data.feedback.flatMap((f) => f.positiveAspects);
    const positiveCounts: Record<string, number> = {};
    allPositives.forEach((aspect) => {
      positiveCounts[aspect] = (positiveCounts[aspect] || 0) + 1;
    });
    const topPositives = Object.entries(positiveCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5);

    // Aggregate suggestions
    const allSuggestions = data.feedback.flatMap((f) => f.suggestions);
    const suggestionCounts: Record<string, number> = {};
    allSuggestions.forEach((suggestion) => {
      suggestionCounts[suggestion] = (suggestionCounts[suggestion] || 0) + 1;
    });
    const topSuggestions = Object.entries(suggestionCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5);

    // Simulate AI synthesis (placeholder - will be replaced with actual LLM API call)
    setTimeout(() => {
      let synthesisText = '';

      if (synthesisType === 'overview') {
        synthesisText = `# Testing Overview Synthesis

## Executive Summary
Based on ${data.sessions.length} test sessions with ${data.feedback.length} participant responses:

**Overall Performance:**
- Average Satisfaction: ${avgSatisfaction.toFixed(1)}/10 (${
          avgSatisfaction >= 8 ? 'Excellent' : avgSatisfaction >= 6 ? 'Good' : 'Needs Improvement'
        })
- Average Usability: ${avgUsability.toFixed(1)}/10 (${
          avgUsability >= 8 ? 'Excellent' : avgUsability >= 6 ? 'Good' : 'Needs Improvement'
        })

## Key Findings

### Critical Issues (${topPainPoints.length} identified)
${topPainPoints
  .map(
    ([point, count]) =>
      `- **${point}** (mentioned by ${count} participant${count > 1 ? 's' : ''})`
  )
  .join('\n')}

### Strengths (${topPositives.length} identified)
${topPositives
  .map(
    ([aspect, count]) =>
      `- **${aspect}** (mentioned by ${count} participant${count > 1 ? 's' : ''})`
  )
  .join('\n')}

### User Suggestions (${topSuggestions.length} collected)
${topSuggestions
  .map(
    ([suggestion, count]) =>
      `- **${suggestion}** (mentioned by ${count} participant${count > 1 ? 's' : ''})`
  )
  .join('\n')}

${
  data.metrics.length > 0
    ? `\n## Quantitative Metrics
${data.metrics
  .map(
    (m) =>
      `- **${m.metricName}**: ${m.value}${m.unit}${
        m.target ? ` (Target: ${m.target}${m.unit})` : ''
      }`
  )
  .join('\n')}`
    : ''
}

---
*This is a placeholder synthesis. Real AI synthesis will integrate with an LLM API.*`;
      } else if (synthesisType === 'insights') {
        synthesisText = `# AI-Generated Insights

## Pattern Analysis

### Usability Patterns
Based on the feedback data, several patterns emerge:

1. **${avgUsability >= 7 ? 'Strong Positive Reception' : 'Usability Concerns Identified'}**
   - Users ${
     avgUsability >= 7
       ? 'find the interface intuitive and easy to navigate'
       : 'encountered difficulties with navigation and task completion'
   }
   - Average usability score: ${avgUsability.toFixed(1)}/10

2. **User Satisfaction Trends**
   - Overall satisfaction: ${avgSatisfaction.toFixed(1)}/10
   - ${
     avgSatisfaction >= avgUsability
       ? 'Satisfaction exceeds usability, suggesting emotional appeal compensates for functional issues'
       : 'Usability exceeds satisfaction, suggesting functional design is present but lacking appeal'
   }

### Critical Pain Point Analysis
${
  topPainPoints.length > 0
    ? `The most frequently mentioned issue is "${topPainPoints[0][0]}" (${
        topPainPoints[0][1]
      } mentions). This suggests:
- This is a systemic issue affecting multiple users
- Priority should be given to addressing this concern
- ${
        topPainPoints[0][1] > data.feedback.length * 0.5
          ? 'Over half of testers encountered this problem - CRITICAL PRIORITY'
          : 'A significant portion of users experienced this issue'
      }`
    : 'No consistent pain points identified across testers.'
}

### Positive Reinforcement
${
  topPositives.length > 0
    ? `Users particularly appreciated "${topPositives[0][0]}" (${topPositives[0][1]} mentions). Consider:
- Highlighting this feature in marketing and onboarding
- Using this as a design pattern for other features
- Building on this success for future iterations`
    : 'No consistent positive feedback patterns identified.'
}

### Cross-Session Comparison
${
  data.sessions.length > 1
    ? 'Multiple test sessions suggest iterative testing approach. Monitor trends across sessions to track improvements.'
    : 'Single test session completed. Consider additional testing rounds to validate findings.'
}

---
*This is a placeholder synthesis. Real AI will provide deeper pattern analysis and predictive insights.*`;
      } else {
        // recommendations
        synthesisText = `# Actionable Recommendations

## Priority 1: Critical Issues (Immediate Action Required)
${
  topPainPoints.length > 0
    ? topPainPoints
        .slice(0, 3)
        .map(
          ([point, count], index) => `
${index + 1}. **Address: ${point}**
   - Urgency: ${
     count > data.feedback.length * 0.5
       ? 'CRITICAL (affects majority of users)'
       : 'HIGH (frequently reported)'
   }
   - Recommendation: Investigate root cause and implement fix
   - Validation: Re-test with same user group to confirm resolution
`
        )
        .join('\n')
    : '✓ No critical issues identified. Focus on enhancements.'
}

## Priority 2: Enhancements (Improve User Experience)
${
  topSuggestions.length > 0
    ? topSuggestions
        .slice(0, 3)
        .map(
          ([suggestion, count], index) => `
${index + 1}. **Implement: ${suggestion}**
   - User demand: ${count} participant${count > 1 ? 's' : ''} requested this
   - Impact: Moderate to High (user-requested feature)
   - Effort: Requires assessment
`
        )
        .join('\n')
    : 'No specific enhancement suggestions provided by users.'
}

## Priority 3: Leverage Strengths
${
  topPositives.length > 0
    ? topPositives
        .slice(0, 2)
        .map(
          ([aspect, count], index) => `
${index + 1}. **Amplify: ${aspect}**
   - Validation: ${count} participant${count > 1 ? 's' : ''} appreciated this
   - Action: Feature this prominently in marketing and onboarding
   - Expansion: Consider applying this successful pattern to other areas
`
        )
        .join('\n')
    : 'Continue testing to identify strengths.'
}

## Next Steps

### Immediate (This Week)
- [ ] ${
          topPainPoints.length > 0
            ? `Fix "${topPainPoints[0][0]}" (highest priority pain point)`
            : 'Plan next testing round'
        }
- [ ] ${
          avgSatisfaction < 7
            ? 'Conduct stakeholder review of low satisfaction scores'
            : 'Document success patterns for replication'
        }
- [ ] ${
          data.metrics.length > 0
            ? 'Review quantitative metrics against targets'
            : 'Define quantitative success metrics'
        }

### Short-term (Next 2 Weeks)
- [ ] Implement top user suggestions if feasible
- [ ] Conduct follow-up testing round to validate changes
- [ ] Update documentation based on user feedback

### Medium-term (Next Month)
- [ ] ${
          avgUsability < avgSatisfaction
            ? 'Improve functional usability to match emotional appeal'
            : 'Maintain current design excellence while adding new features'
        }
- [ ] Expand testing to broader user demographics
- [ ] Establish ongoing feedback collection mechanism

## Decision Points

**Should we proceed to deployment?**
${
  avgSatisfaction >= 7 && avgUsability >= 7 && topPainPoints.length < 3
    ? '✓ YES - Metrics indicate readiness for deployment with minor iteration'
    : avgSatisfaction >= 6 && avgUsability >= 6
    ? '⚠ CONDITIONAL - Address critical pain points before full launch, consider soft launch'
    : '✗ NOT YET - Significant improvements needed before deployment'
}

**Risk Assessment:**
- User Satisfaction: ${avgSatisfaction >= 7 ? 'LOW RISK' : avgSatisfaction >= 5 ? 'MODERATE RISK' : 'HIGH RISK'}
- Usability: ${avgUsability >= 7 ? 'LOW RISK' : avgUsability >= 5 ? 'MODERATE RISK' : 'HIGH RISK'}
- Critical Issues: ${topPainPoints.length === 0 ? 'NONE' : topPainPoints.length < 3 ? 'MANAGEABLE' : 'SIGNIFICANT'}

---
*This is a placeholder synthesis. Real AI will provide contextual, project-specific recommendations.*`;
      }

      onSynthesisComplete(synthesisText);
      setSynthesizing(false);
    }, 2500);
  };

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-2">AI-Powered Test Insights</h3>
        <p className="text-sm text-gray-600 mb-4">
          Generate AI-driven insights, identify patterns, and get actionable recommendations based on
          your test results
        </p>
      </div>

      {/* Synthesis Type Selection */}
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Select Synthesis Type
        </label>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <button
            onClick={() => setSynthesisType('overview')}
            className={`p-4 text-left rounded-lg border-2 transition-colors ${
              synthesisType === 'overview'
                ? 'border-purple-500 bg-purple-50'
                : 'border-gray-200 hover:border-purple-300'
            }`}
          >
            <div className="font-medium text-gray-900 mb-1">Testing Overview</div>
            <div className="text-xs text-gray-600">
              Comprehensive summary of test results, key findings, and metrics
            </div>
          </button>
          <button
            onClick={() => setSynthesisType('insights')}
            className={`p-4 text-left rounded-lg border-2 transition-colors ${
              synthesisType === 'insights'
                ? 'border-purple-500 bg-purple-50'
                : 'border-gray-200 hover:border-purple-300'
            }`}
          >
            <div className="font-medium text-gray-900 mb-1">Pattern Analysis</div>
            <div className="text-xs text-gray-600">
              Deep insights into user behaviour patterns and emerging trends
            </div>
          </button>
          <button
            onClick={() => setSynthesisType('recommendations')}
            className={`p-4 text-left rounded-lg border-2 transition-colors ${
              synthesisType === 'recommendations'
                ? 'border-purple-500 bg-purple-50'
                : 'border-gray-200 hover:border-purple-300'
            }`}
          >
            <div className="font-medium text-gray-900 mb-1">Recommendations</div>
            <div className="text-xs text-gray-600">
              Prioritised action items and next steps based on test results
            </div>
          </button>
        </div>
      </div>

      {/* Generate Button */}
      <div>
        <button
          onClick={generateSynthesis}
          disabled={synthesizing || data.feedback.length === 0}
          className="w-full px-6 py-3 bg-purple-600 text-white rounded-md hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {synthesizing
            ? 'Generating Synthesis...'
            : `Generate ${
                synthesisType === 'overview'
                  ? 'Overview'
                  : synthesisType === 'insights'
                  ? 'Insights'
                  : 'Recommendations'
              }`}
        </button>

        {data.feedback.length === 0 && (
          <div className="mt-4 p-4 bg-yellow-50 border border-yellow-200 rounded-md">
            <p className="text-sm text-yellow-800">
              Collect user feedback in the "Feedback Collection" tab before generating AI synthesis.
            </p>
          </div>
        )}

        {data.feedback.length > 0 && data.feedback.length < 3 && (
          <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-md">
            <p className="text-sm text-blue-800">
              Note: More feedback responses will improve synthesis quality. Consider collecting at
              least 5-10 responses for robust insights.
            </p>
          </div>
        )}
      </div>

      {/* Synthesis Results */}
      {data.synthesisResult && (
        <div className="mt-6">
          <div className="flex justify-between items-center mb-3">
            <h4 className="text-sm font-medium text-gray-900">Synthesis Results</h4>
            <button
              onClick={() => {
                navigator.clipboard.writeText(data.synthesisResult || '');
                alert('Synthesis copied to clipboard!');
              }}
              className="text-sm text-purple-600 hover:text-purple-800"
            >
              Copy to Clipboard
            </button>
          </div>
          <div className="p-6 bg-white border-2 border-purple-200 rounded-lg">
            <div className="prose prose-sm max-w-none">
              <pre className="whitespace-pre-wrap font-sans text-sm text-gray-800">
                {data.synthesisResult}
              </pre>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="mt-4 flex gap-3">
            <button
              onClick={() => {
                const blob = new Blob([data.synthesisResult || ''], {
                  type: 'text/markdown',
                });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `test-synthesis-${new Date().toISOString().split('T')[0]}.md`;
                a.click();
              }}
              className="px-4 py-2 bg-white border border-purple-300 text-purple-700 rounded-md hover:bg-purple-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
            >
              Download as Markdown
            </button>
            <button
              onClick={generateSynthesis}
              className="px-4 py-2 bg-white border border-purple-300 text-purple-700 rounded-md hover:bg-purple-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500"
            >
              Regenerate
            </button>
          </div>
        </div>
      )}

      {/* Info Panel */}
      <div className="bg-purple-50 rounded-lg p-4 border border-purple-200">
        <h4 className="text-sm font-medium text-purple-900 mb-2">About AI Synthesis</h4>
        <ul className="text-sm text-purple-700 space-y-1">
          <li>
            <strong>Overview:</strong> Get a comprehensive summary of all test sessions, metrics,
            and key findings
          </li>
          <li>
            <strong>Insights:</strong> Discover hidden patterns, correlations, and trends in user
            behaviour
          </li>
          <li>
            <strong>Recommendations:</strong> Receive prioritised action items and strategic next
            steps
          </li>
          <li className="mt-2 text-xs">
            Note: Current implementation uses placeholder synthesis. Production version will integrate
            with LLM APIs (OpenAI, Anthropic, or local models) for advanced analysis.
          </li>
        </ul>
      </div>
    </div>
  );
}


