import { useState } from 'react';
import type { Idea, Cluster } from '../../types/ideate';

interface IdeaCanvasProps {
  ideas: Idea[];
  clusters: Cluster[];
  onIdeasChange: (ideas: Idea[]) => void;
  onClustersChange: (clusters: Cluster[]) => void;
  onSave: () => void;
}

const COLORS = [
  { name: 'Yellow', value: '#FEF3C7', border: '#FCD34D' },
  { name: 'Pink', value: '#FCE7F3', border: '#F9A8D4' },
  { name: 'Blue', value: '#DBEAFE', border: '#93C5FD' },
  { name: 'Green', value: '#D1FAE5', border: '#6EE7B7' },
  { name: 'Purple', value: '#E9D5FF', border: '#C084FC' },
  { name: 'Orange', value: '#FED7AA', border: '#FDBA74' },
];

export function IdeaCanvas({ ideas, clusters, onIdeasChange, onClustersChange, onSave }: IdeaCanvasProps) {
  const [newIdeaText, setNewIdeaText] = useState('');
  const [selectedColor, setSelectedColor] = useState(COLORS[0]);
  const [draggedIdea, setDraggedIdea] = useState<string | null>(null);
  const [editingIdea, setEditingIdea] = useState<string | null>(null);
  const [editText, setEditText] = useState('');

  const addIdea = () => {
    if (!newIdeaText.trim()) return;

    const newIdea: Idea = {
      id: `idea-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      content: newIdeaText,
      color: selectedColor.value,
      position: {
        x: Math.random() * 400,
        y: Math.random() * 300,
      },
      createdAt: new Date().toISOString(),
    };

    onIdeasChange([...ideas, newIdea]);
    setNewIdeaText('');
  };

  const deleteIdea = (ideaId: string) => {
    onIdeasChange(ideas.filter((idea) => idea.id !== ideaId));
  };

  const startEditing = (idea: Idea) => {
    setEditingIdea(idea.id);
    setEditText(idea.content);
  };

  const saveEdit = () => {
    if (editingIdea && editText.trim()) {
      onIdeasChange(
        ideas.map((idea) =>
          idea.id === editingIdea ? { ...idea, content: editText } : idea
        )
      );
    }
    setEditingIdea(null);
    setEditText('');
  };

  const cancelEdit = () => {
    setEditingIdea(null);
    setEditText('');
  };

  const handleDragStart = (ideaId: string) => {
    setDraggedIdea(ideaId);
  };

  const handleDragEnd = () => {
    setDraggedIdea(null);
  };

  const handleDrop = (e: React.DragEvent, targetIdeaId?: string) => {
    e.preventDefault();
    if (!draggedIdea) return;

    if (targetIdeaId && targetIdeaId !== draggedIdea) {
      // Cluster ideas together
      createCluster([draggedIdea, targetIdeaId]);
    }
  };

  const createCluster = (ideaIds: string[]) => {
    const newCluster: Cluster = {
      id: `cluster-${Date.now()}`,
      name: 'New Cluster',
      color: COLORS[Math.floor(Math.random() * COLORS.length)].border,
      ideaIds,
    };

    // Update ideas to include cluster ID
    const updatedIdeas = ideas.map((idea) =>
      ideaIds.includes(idea.id) ? { ...idea, clusterId: newCluster.id } : idea
    );

    onIdeasChange(updatedIdeas);
    onClustersChange([...clusters, newCluster]);
  };

  const updateClusterName = (clusterId: string, name: string) => {
    onClustersChange(
      clusters.map((cluster) =>
        cluster.id === clusterId ? { ...cluster, name } : cluster
      )
    );
  };

  const removeFromCluster = (ideaId: string) => {
    const idea = ideas.find((i) => i.id === ideaId);
    if (!idea?.clusterId) return;

    const updatedIdeas = ideas.map((i) =>
      i.id === ideaId ? { ...i, clusterId: undefined } : i
    );

    // Remove cluster if empty
    const clusteredIdeas = updatedIdeas.filter((i) => i.clusterId === idea.clusterId);
    if (clusteredIdeas.length === 0) {
      onClustersChange(clusters.filter((c) => c.id !== idea.clusterId));
    } else {
      onClustersChange(
        clusters.map((c) =>
          c.id === idea.clusterId
            ? { ...c, ideaIds: c.ideaIds.filter((id) => id !== ideaId) }
            : c
        )
      );
    }

    onIdeasChange(updatedIdeas);
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      {/* Add Idea Form */}
      <div className="mb-6 pb-6 border-b border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Add New Idea</h3>
        <div className="flex gap-4">
          <input
            type="text"
            value={newIdeaText}
            onChange={(e) => setNewIdeaText(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && addIdea()}
            placeholder="Type your idea here..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500"
          />
          <div className="flex gap-2">
            {COLORS.map((color) => (
              <button
                key={color.value}
                onClick={() => setSelectedColor(color)}
                className={`w-8 h-8 rounded border-2 ${
                  selectedColor.value === color.value ? 'ring-2 ring-green-500' : ''
                }`}
                style={{ backgroundColor: color.value, borderColor: color.border }}
                title={color.name}
              />
            ))}
          </div>
          <button
            onClick={addIdea}
            className="px-6 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500"
          >
            Add Idea
          </button>
        </div>
      </div>

      {/* Canvas Area */}
      <div className="mb-4">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">
            Brainstorming Canvas ({ideas.length} ideas)
          </h3>
          <div className="text-sm text-gray-500">
            Drag ideas onto each other to create clusters
          </div>
        </div>

        {ideas.length === 0 ? (
          <div className="text-center py-16 text-gray-500">
            <p className="text-lg mb-2">No ideas yet</p>
            <p className="text-sm">Start adding ideas above to begin brainstorming</p>
          </div>
        ) : (
          <div>
            {/* Unclustered Ideas */}
            <div className="mb-8">
              <h4 className="text-sm font-medium text-gray-700 mb-3">Individual Ideas</h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                {ideas
                  .filter((idea) => !idea.clusterId)
                  .map((idea) => (
                    <div
                      key={idea.id}
                      draggable
                      onDragStart={() => handleDragStart(idea.id)}
                      onDragEnd={handleDragEnd}
                      onDrop={(e) => handleDrop(e, idea.id)}
                      onDragOver={(e) => e.preventDefault()}
                      className={`p-4 rounded-lg border-2 cursor-move shadow-sm hover:shadow-md transition-shadow ${
                        draggedIdea === idea.id ? 'opacity-50' : ''
                      }`}
                      style={{
                        backgroundColor: idea.color,
                        borderColor: COLORS.find((c) => c.value === idea.color)?.border || '#ccc',
                      }}
                    >
                      {editingIdea === idea.id ? (
                        <div>
                          <textarea
                            value={editText}
                            onChange={(e) => setEditText(e.target.value)}
                            className="w-full px-2 py-1 text-sm border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-green-500"
                            rows={3}
                            autoFocus
                          />
                          <div className="flex gap-2 mt-2">
                            <button
                              onClick={saveEdit}
                              className="text-xs px-2 py-1 bg-green-600 text-white rounded hover:bg-green-700"
                            >
                              Save
                            </button>
                            <button
                              onClick={cancelEdit}
                              className="text-xs px-2 py-1 bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
                            >
                              Cancel
                            </button>
                          </div>
                        </div>
                      ) : (
                        <div>
                          <p className="text-sm text-gray-800 mb-3">{idea.content}</p>
                          <div className="flex gap-2">
                            <button
                              onClick={() => startEditing(idea)}
                              className="text-xs text-blue-600 hover:text-blue-800"
                            >
                              Edit
                            </button>
                            <button
                              onClick={() => deleteIdea(idea.id)}
                              className="text-xs text-red-600 hover:text-red-800"
                            >
                              Delete
                            </button>
                          </div>
                        </div>
                      )}
                    </div>
                  ))}
              </div>
            </div>

            {/* Clustered Ideas */}
            {clusters.length > 0 && (
              <div>
                <h4 className="text-sm font-medium text-gray-700 mb-3">Idea Clusters</h4>
                <div className="space-y-6">
                  {clusters.map((cluster) => (
                    <div
                      key={cluster.id}
                      className="p-4 rounded-lg border-2"
                      style={{ borderColor: cluster.color }}
                    >
                      <input
                        type="text"
                        value={cluster.name}
                        onChange={(e) => updateClusterName(cluster.id, e.target.value)}
                        className="text-lg font-semibold mb-3 bg-transparent border-b border-gray-300 focus:outline-none focus:border-gray-500"
                      />
                      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
                        {ideas
                          .filter((idea) => idea.clusterId === cluster.id)
                          .map((idea) => (
                            <div
                              key={idea.id}
                              className="p-3 rounded-lg border-2"
                              style={{
                                backgroundColor: idea.color,
                                borderColor:
                                  COLORS.find((c) => c.value === idea.color)?.border || '#ccc',
                              }}
                            >
                              <p className="text-sm text-gray-800 mb-2">{idea.content}</p>
                              <button
                                onClick={() => removeFromCluster(idea.id)}
                                className="text-xs text-red-600 hover:text-red-800"
                              >
                                Remove from cluster
                              </button>
                            </div>
                          ))}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}


