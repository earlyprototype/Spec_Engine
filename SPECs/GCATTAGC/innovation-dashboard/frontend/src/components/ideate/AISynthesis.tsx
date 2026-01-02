import { useState } from 'react';
import type { Idea } from '../../types/ideate';
import { generateIdeas, clusterIdeas, synthesizeIdeas } from '../../services/ideateGeminiService';

interface AISynthesisProps {
  projectId: string;
  ideas: Idea[];
  onIdeasGenerated: (ideas: Idea[]) => void;
}

const COLORS = [
  '#FEF3C7',
  '#FCE7F3',
  '#DBEAFE',
  '#D1FAE5',
  '#E9D5FF',
  '#FED7AA',
];

export function AISynthesis({ projectId, ideas, onIdeasGenerated }: AISynthesisProps) {
  const [context, setContext] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [generatedIdeas, setGeneratedIdeas] = useState<string[]>([]);
  const [synthesis, setSynthesis] = useState<string>('');
  const [clusteringSuggestion, setClusteringSuggestion] = useState<any>(null);
  const [activeAction, setActiveAction] = useState<string | null>(null);

  const handleGenerateIdeas = async () => {
    if (!context.trim() && ideas.length === 0) {
      setError('Please provide context or add some ideas first');
      return;
    }

    setLoading(true);
    setError(null);
    setActiveAction('generate');

    try {
      const existingIdeas = ideas.map((idea) => idea.content);
      const newIdeas = await generateIdeas(context, existingIdeas);
      setGeneratedIdeas(newIdeas);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate ideas');
    } finally {
      setLoading(false);
      setActiveAction(null);
    }
  };

  const handleAddGeneratedIdeas = () => {
    const newIdeas: Idea[] = generatedIdeas.map((content, index) => ({
      id: `ai-idea-${Date.now()}-${index}`,
      content,
      color: COLORS[index % COLORS.length],
      position: {
        x: Math.random() * 400,
        y: Math.random() * 300,
      },
      createdAt: new Date().toISOString(),
    }));

    onIdeasGenerated(newIdeas);
    setGeneratedIdeas([]);
  };

  const handleClusterSuggestions = async () => {
    if (ideas.length < 3) {
      setError('Need at least 3 ideas to suggest clusters');
      return;
    }

    setLoading(true);
    setError(null);
    setActiveAction('cluster');

    try {
      const ideaContents = ideas.map((idea) => idea.content);
      const clustering = await clusterIdeas(ideaContents);
      setClusteringSuggestion(clustering);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to cluster ideas');
    } finally {
      setLoading(false);
      setActiveAction(null);
    }
  };

  const handleSynthesize = async () => {
    if (ideas.length === 0) {
      setError('No ideas to synthesize');
      return;
    }

    setLoading(true);
    setError(null);
    setActiveAction('synthesize');

    try {
      const ideaContents = ideas.map((idea) => idea.content);
      const synthesisSummary = await synthesizeIdeas(ideaContents);
      setSynthesis(synthesisSummary);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to synthesize ideas');
    } finally {
      setLoading(false);
      setActiveAction(null);
    }
  };

  return (
    <div className="space-y-6">
      {/* Context Input */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          AI-Powered Ideation Assistant
        </h3>
        <p className="text-sm text-gray-600 mb-4">
          Powered by Gemini Pro 2.5 - Use AI to generate new ideas, suggest clusters, or synthesize
          your brainstorming session.
        </p>

        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Problem Context (Optional)
          </label>
          <textarea
            value={context}
            onChange={(e) => setContext(e.target.value)}
            placeholder="Describe the problem you're trying to solve, user needs, constraints, or goals..."
            rows={4}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
          />
          <p className="text-xs text-gray-500 mt-1">
            Providing context helps AI generate more relevant ideas
          </p>
        </div>

        {error && (
          <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-md text-sm text-red-700">
            {error}
          </div>
        )}

        {/* Action Buttons */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <button
            onClick={handleGenerateIdeas}
            disabled={loading}
            className="px-4 py-3 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading && activeAction === 'generate' ? (
              <span>Generating...</span>
            ) : (
              <>
                <span className="block font-semibold">Generate Ideas</span>
                <span className="text-xs opacity-90">AI creates 5 new ideas</span>
              </>
            )}
          </button>

          <button
            onClick={handleClusterSuggestions}
            disabled={loading || ideas.length < 3}
            className="px-4 py-3 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading && activeAction === 'cluster' ? (
              <span>Clustering...</span>
            ) : (
              <>
                <span className="block font-semibold">Suggest Clusters</span>
                <span className="text-xs opacity-90">Group similar ideas</span>
              </>
            )}
          </button>

          <button
            onClick={handleSynthesize}
            disabled={loading || ideas.length === 0}
            className="px-4 py-3 bg-purple-600 text-white rounded-md hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading && activeAction === 'synthesize' ? (
              <span>Synthesizing...</span>
            ) : (
              <>
                <span className="block font-semibold">Synthesize</span>
                <span className="text-xs opacity-90">AI summary of ideas</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Generated Ideas */}
      {generatedIdeas.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900">AI-Generated Ideas</h3>
            <button
              onClick={handleAddGeneratedIdeas}
              className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 text-sm"
            >
              Add All to Canvas
            </button>
          </div>
          <ul className="space-y-3">
            {generatedIdeas.map((idea, index) => (
              <li
                key={index}
                className="p-3 bg-green-50 border border-green-200 rounded-md text-gray-800"
              >
                {idea}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Clustering Suggestions */}
      {clusteringSuggestion && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            AI Clustering Suggestions
          </h3>
          <div className="space-y-4">
            {clusteringSuggestion.clusters?.map((cluster: any, index: number) => (
              <div key={index} className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <h4 className="font-semibold text-blue-900 mb-2">{cluster.name}</h4>
                <ul className="space-y-1">
                  {cluster.ideas?.map((idea: string, ideaIndex: number) => (
                    <li key={ideaIndex} className="text-sm text-gray-700 pl-4">
                      • {idea}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
          <p className="text-xs text-gray-500 mt-4">
            Use these suggestions to manually cluster ideas on the Brainstorming Canvas
          </p>
        </div>
      )}

      {/* Synthesis Summary */}
      {synthesis && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">AI Synthesis</h3>
          <div className="prose prose-sm max-w-none">
            <div className="p-4 bg-purple-50 border border-purple-200 rounded-lg text-gray-800 whitespace-pre-wrap">
              {synthesis}
            </div>
          </div>
          <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-md">
            <p className="text-sm text-yellow-800">
              <strong>Next Steps:</strong> Use this synthesis to refine your ideas and identify the
              most promising directions to prototype.
            </p>
          </div>
        </div>
      )}

      {/* Statistics */}
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Ideation Statistics</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <div className="text-3xl font-bold text-green-600">{ideas.length}</div>
            <div className="text-sm text-gray-600">Total Ideas</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-blue-600">
              {ideas.filter((i) => i.evaluation).length}
            </div>
            <div className="text-sm text-gray-600">Evaluated</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-purple-600">
              {ideas.filter((i) => i.clusterId).length}
            </div>
            <div className="text-sm text-gray-600">Clustered</div>
          </div>
          <div className="text-center">
            <div className="text-3xl font-bold text-orange-600">
              {ideas.filter((i) => i.id.startsWith('ai-idea')).length}
            </div>
            <div className="text-sm text-gray-600">AI-Generated</div>
          </div>
        </div>
      </div>
    </div>
  );
}

