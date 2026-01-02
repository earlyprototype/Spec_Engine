import type { ReactNode } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useEffect, useState } from 'react';
import { supabase, type StageData } from '../lib/supabase';

interface LayoutProps {
  children: ReactNode;
}

export function Layout({ children }: LayoutProps) {
  const { projectId } = useParams();
  const { user, signOut } = useAuth();
  const navigate = useNavigate();

  const handleSignOut = async () => {
    await signOut();
    navigate('/login');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <button
                onClick={() => navigate('/dashboard')}
                className="text-xl font-bold text-gray-900 hover:text-primary-600"
              >
                Innovation Dashboard
              </button>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">{user?.email}</span>
              <button
                onClick={handleSignOut}
                className="px-4 py-2 text-sm font-medium text-gray-700 hover:text-gray-900"
              >
                Sign Out
              </button>
            </div>
          </div>
        </div>
      </nav>

      {projectId && <StageNav projectId={projectId} />}

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">{children}</div>
      </main>
    </div>
  );
}

function StageNav({ projectId }: { projectId: string }) {
  const navigate = useNavigate();
  const stages = [
    { name: 'Summary', path: 'summary' },
    { name: 'Discovery', path: 'discovery' },
    { name: 'Define', path: 'define' },
    { name: 'Ideate', path: 'ideate' },
    { name: 'Prototype', path: 'prototype' },
    { name: 'Test', path: 'test' },
  ];

  const [hasDataByStage, setHasDataByStage] = useState<Record<string, boolean>>({});

  useEffect(() => {
    const loadPresence = async () => {
      const { data, error } = await supabase
        .from('stage_data')
        .select('stage_name, data_json')
        .eq('project_id', projectId);
      if (error) {
        console.error('Stage presence load error:', error);
        return;
      }
      const presence: Record<string, boolean> = {};
      (data as Pick<StageData, 'stage_name' | 'data_json'>[] | null)?.forEach((row) => {
        const has = row && row.data_json && Object.keys(row.data_json || {}).length > 0;
        presence[row.stage_name] = !!has;
      });
      setHasDataByStage(presence);
    };
    loadPresence();
  }, [projectId]);

  const currentPath = window.location.pathname;

  return (
    <div className="bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <nav className="flex space-x-8" aria-label="Stages">
          {stages.map((stage) => {
            const isActive = currentPath.includes(stage.path);
            return (
              <button
                key={stage.path}
                onClick={() => navigate(`/project/${projectId}/${stage.path}`)}
                className={`
                  py-4 px-1 border-b-2 font-medium text-sm
                  ${
                    isActive
                      ? 'border-primary-500 text-primary-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }
                `}
              >
                <span className="inline-flex items-center gap-1">
                  {stage.name}
                  {stage.path !== 'summary' && (
                    <span
                      className={`inline-block h-1.5 w-1.5 rounded-full ${
                        hasDataByStage[stage.path]
                          ? 'bg-green-500'
                          : 'bg-gray-300'
                      }`}
                      aria-hidden
                    />
                  )}
                </span>
              </button>
            );
          })}
        </nav>
      </div>
    </div>
  );
}

