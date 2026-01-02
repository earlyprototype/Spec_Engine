import { useState } from 'react';
import type { Idea } from '../../types/ideate';

interface IdeaEvaluationMatrixProps {
  ideas: Idea[];
  onIdeasChange: (ideas: Idea[]) => void;
  onSave: () => void;
}

export function IdeaEvaluationMatrix({ ideas, onIdeasChange, onSave }: IdeaEvaluationMatrixProps) {
  const [selectedIdea, setSelectedIdea] = useState<string | null>(null);

  const updateEvaluation = (ideaId: string, feasibility: number, impact: number) => {
    onIdeasChange(
      ideas.map((idea) =>
        idea.id === ideaId
          ? { ...idea, evaluation: { feasibility, impact } }
          : idea
      )
    );
  };

  const getQuadrant = (feasibility: number, impact: number) => {
    if (feasibility >= 5 && impact >= 5) return 'Quick Wins';
    if (feasibility < 5 && impact >= 5) return 'Major Projects';
    if (feasibility >= 5 && impact < 5) return 'Fill Ins';
    return 'Time Wasters';
  };

  const getQuadrantColor = (quadrant: string) => {
    switch (quadrant) {
      case 'Quick Wins':
        return 'bg-green-100 border-green-500';
      case 'Major Projects':
        return 'bg-yellow-100 border-yellow-500';
      case 'Fill Ins':
        return 'bg-blue-100 border-blue-500';
      default:
        return 'bg-red-100 border-red-500';
    }
  };

  const evaluatedIdeas = ideas.filter((idea) => idea.evaluation);
  const unevaluatedIdeas = ideas.filter((idea) => !idea.evaluation);

  return (
    <div className="space-y-6">
      {/* Evaluation Form */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Evaluate Ideas</h3>
        
        {unevaluatedIdeas.length === 0 && evaluatedIdeas.length > 0 ? (
          <div className="text-center py-4 text-green-600">
            All ideas have been evaluated!
          </div>
        ) : unevaluatedIdeas.length === 0 ? (
          <div className="text-center py-4 text-gray-500">
            No ideas to evaluate yet. Add ideas in the Brainstorming Canvas first.
          </div>
        ) : (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Select Idea to Evaluate
              </label>
              <select
                value={selectedIdea || ''}
                onChange={(e) => setSelectedIdea(e.target.value || null)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
              >
                <option value="">Choose an idea...</option>
                {unevaluatedIdeas.map((idea) => (
                  <option key={idea.id} value={idea.id}>
                    {idea.content.substring(0, 60)}{idea.content.length > 60 ? '...' : ''}
                  </option>
                ))}
              </select>
            </div>

            {selectedIdea && (
              <div className="space-y-4 p-4 bg-gray-50 rounded-lg">
                <div className="text-sm text-gray-700 mb-4">
                  <strong>Idea:</strong>{' '}
                  {unevaluatedIdeas.find((i) => i.id === selectedIdea)?.content}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Feasibility (1-10)
                    <span className="ml-2 text-xs text-gray-500">
                      How easy is this to implement?
                    </span>
                  </label>
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-gray-500">Hard</span>
                    <input
                      type="range"
                      min="1"
                      max="10"
                      defaultValue="5"
                      id={`feasibility-${selectedIdea}`}
                      className="flex-1"
                    />
                    <span className="text-xs text-gray-500">Easy</span>
                  </div>
                  <div className="text-center text-sm font-medium text-gray-700 mt-1">
                    {
                      (document.getElementById(`feasibility-${selectedIdea}`) as HTMLInputElement)
                        ?.value || '5'
                    }
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Impact (1-10)
                    <span className="ml-2 text-xs text-gray-500">
                      How much value will this create?
                    </span>
                  </label>
                  <div className="flex items-center gap-2">
                    <span className="text-xs text-gray-500">Low</span>
                    <input
                      type="range"
                      min="1"
                      max="10"
                      defaultValue="5"
                      id={`impact-${selectedIdea}`}
                      className="flex-1"
                    />
                    <span className="text-xs text-gray-500">High</span>
                  </div>
                  <div className="text-center text-sm font-medium text-gray-700 mt-1">
                    {
                      (document.getElementById(`impact-${selectedIdea}`) as HTMLInputElement)
                        ?.value || '5'
                    }
                  </div>
                </div>

                <button
                  onClick={() => {
                    const feasibility = parseInt(
                      (document.getElementById(`feasibility-${selectedIdea}`) as HTMLInputElement)
                        ?.value || '5'
                    );
                    const impact = parseInt(
                      (document.getElementById(`impact-${selectedIdea}`) as HTMLInputElement)
                        ?.value || '5'
                    );
                    updateEvaluation(selectedIdea, feasibility, impact);
                    setSelectedIdea(null);
                    onSave();
                  }}
                  className="w-full px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500"
                >
                  Save Evaluation
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Impact/Feasibility Matrix */}
      {evaluatedIdeas.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            Impact vs Feasibility Matrix
          </h3>
          
          {/* Matrix Grid */}
          <div className="grid grid-cols-2 gap-4 mb-6">
            {/* Quick Wins (High Impact, High Feasibility) */}
            <div className="p-4 border-2 border-green-500 bg-green-50 rounded-lg min-h-48">
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-semibold text-green-900">Quick Wins</h4>
                <span className="text-xs text-green-700">High Impact, Easy</span>
              </div>
              <div className="space-y-2">
                {evaluatedIdeas
                  .filter(
                    (idea) =>
                      idea.evaluation &&
                      idea.evaluation.feasibility >= 5 &&
                      idea.evaluation.impact >= 5
                  )
                  .map((idea) => (
                    <div
                      key={idea.id}
                      className="p-2 bg-white rounded border border-green-300 text-sm"
                    >
                      <p className="text-gray-800 mb-1">{idea.content}</p>
                      <div className="flex gap-3 text-xs text-gray-600">
                        <span>Feasibility: {idea.evaluation?.feasibility}</span>
                        <span>Impact: {idea.evaluation?.impact}</span>
                      </div>
                    </div>
                  ))}
              </div>
            </div>

            {/* Major Projects (High Impact, Low Feasibility) */}
            <div className="p-4 border-2 border-yellow-500 bg-yellow-50 rounded-lg min-h-48">
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-semibold text-yellow-900">Major Projects</h4>
                <span className="text-xs text-yellow-700">High Impact, Hard</span>
              </div>
              <div className="space-y-2">
                {evaluatedIdeas
                  .filter(
                    (idea) =>
                      idea.evaluation &&
                      idea.evaluation.feasibility < 5 &&
                      idea.evaluation.impact >= 5
                  )
                  .map((idea) => (
                    <div
                      key={idea.id}
                      className="p-2 bg-white rounded border border-yellow-300 text-sm"
                    >
                      <p className="text-gray-800 mb-1">{idea.content}</p>
                      <div className="flex gap-3 text-xs text-gray-600">
                        <span>Feasibility: {idea.evaluation?.feasibility}</span>
                        <span>Impact: {idea.evaluation?.impact}</span>
                      </div>
                    </div>
                  ))}
              </div>
            </div>

            {/* Fill Ins (Low Impact, High Feasibility) */}
            <div className="p-4 border-2 border-blue-500 bg-blue-50 rounded-lg min-h-48">
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-semibold text-blue-900">Fill Ins</h4>
                <span className="text-xs text-blue-700">Low Impact, Easy</span>
              </div>
              <div className="space-y-2">
                {evaluatedIdeas
                  .filter(
                    (idea) =>
                      idea.evaluation &&
                      idea.evaluation.feasibility >= 5 &&
                      idea.evaluation.impact < 5
                  )
                  .map((idea) => (
                    <div
                      key={idea.id}
                      className="p-2 bg-white rounded border border-blue-300 text-sm"
                    >
                      <p className="text-gray-800 mb-1">{idea.content}</p>
                      <div className="flex gap-3 text-xs text-gray-600">
                        <span>Feasibility: {idea.evaluation?.feasibility}</span>
                        <span>Impact: {idea.evaluation?.impact}</span>
                      </div>
                    </div>
                  ))}
              </div>
            </div>

            {/* Time Wasters (Low Impact, Low Feasibility) */}
            <div className="p-4 border-2 border-red-500 bg-red-50 rounded-lg min-h-48">
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-semibold text-red-900">Time Wasters</h4>
                <span className="text-xs text-red-700">Low Impact, Hard</span>
              </div>
              <div className="space-y-2">
                {evaluatedIdeas
                  .filter(
                    (idea) =>
                      idea.evaluation &&
                      idea.evaluation.feasibility < 5 &&
                      idea.evaluation.impact < 5
                  )
                  .map((idea) => (
                    <div
                      key={idea.id}
                      className="p-2 bg-white rounded border border-red-300 text-sm"
                    >
                      <p className="text-gray-800 mb-1">{idea.content}</p>
                      <div className="flex gap-3 text-xs text-gray-600">
                        <span>Feasibility: {idea.evaluation?.feasibility}</span>
                        <span>Impact: {idea.evaluation?.impact}</span>
                      </div>
                    </div>
                  ))}
              </div>
            </div>
          </div>

          {/* Summary */}
          <div className="bg-gray-50 rounded-lg p-4">
            <h4 className="font-semibold text-gray-900 mb-2">Recommendations</h4>
            <ul className="space-y-1 text-sm text-gray-700">
              <li>
                • <strong>Prioritise Quick Wins</strong> - High impact and easy to implement
              </li>
              <li>
                • <strong>Plan Major Projects</strong> - High impact but need resources
              </li>
              <li>
                • <strong>Consider Fill Ins</strong> - Low-hanging fruit when capacity allows
              </li>
              <li>
                • <strong>Avoid Time Wasters</strong> - Low return on investment
              </li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}


