import { useEffect, useMemo, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Layout } from '../components/Layout';
import { supabase, type StageData } from '../lib/supabase';
import { generateWithGemini } from '../lib/gemini';

type StageName = 'discovery' | 'define' | 'ideate' | 'prototype' | 'test';

interface StageSnapshot {
  name: StageName;
  title: string;
  hasData: boolean;
  summary: string;
}

export function SummaryView() {
  const { projectId } = useParams<{ projectId: string }>();
  const [stageRows, setStageRows] = useState<Record<StageName, StageData | null>>({
    discovery: null,
    define: null,
    ideate: null,
    prototype: null,
    test: null,
  });
  const [loading, setLoading] = useState<boolean>(true);
  const [synthesis, setSynthesis] = useState<string>('');
  const [generating, setGenerating] = useState<boolean>(false);

  useEffect(() => {
    const loadAllStages = async () => {
      if (!projectId) return;
      setLoading(true);
      const { data, error } = await supabase
        .from('stage_data')
        .select('*')
        .eq('project_id', projectId);

      if (error) {
        console.error('Error loading stage data:', error);
        setLoading(false);
        return;
      }

      const next: Record<StageName, StageData | null> = {
        discovery: null,
        define: null,
        ideate: null,
        prototype: null,
        test: null,
      };
      (data || []).forEach((row: any) => {
        if (['discovery', 'define', 'ideate', 'prototype', 'test'].includes(row.stage_name)) {
          next[row.stage_name as StageName] = row as StageData;
        }
      });
      setStageRows(next);
      setLoading(false);
    };

    loadAllStages();
  }, [projectId]);

  const stageOrder: Array<{ key: StageName; title: string; color: string }> = useMemo(
    () => [
      { key: 'discovery', title: 'Discovery', color: 'blue' },
      { key: 'define', title: 'Define', color: 'purple' },
      { key: 'ideate', title: 'Ideate', color: 'green' },
      { key: 'prototype', title: 'Prototype', color: 'orange' },
      { key: 'test', title: 'Test', color: 'red' },
    ],
    []
  );

  const snapshots: StageSnapshot[] = useMemo(() => {
    return stageOrder.map((s) => {
      const row = stageRows[s.key];
      const dataJson = (row?.data_json as Record<string, any>) || {};
      const raw = dataJson.content || dataJson.summary || JSON.stringify(dataJson).slice(0, 500);
      const hasData = !!row && Object.keys(dataJson || {}).length > 0;
      const summary = typeof raw === 'string' ? raw : JSON.stringify(raw);
      return { name: s.key, title: s.title, hasData, summary };
    });
  }, [stageRows, stageOrder]);

  const buildCrossStagePrompt = (): string => {
    const lines: string[] = [];
    lines.push('You are an innovation consultant. Create a cross-stage project synthesis.');
    lines.push('Stages available: Discovery, Define, Ideate, Prototype, Test.');
    lines.push('For each stage, you may receive partial or empty data.');
    lines.push('Output sections:');
    lines.push('1) Executive Summary (6-8 sentences)');
    lines.push('2) Problem Definition (from Discovery/Define)');
    lines.push('3) Top Ideas (from Ideate)');
    lines.push('4) Prototype Plan (from Prototype)');
    lines.push('5) Test Highlights (from Test)');
    lines.push('6) Top 5 Risks and Mitigations');
    lines.push('7) Next 5 Actions');
    lines.push('\nProject data:');
    snapshots.forEach((snap) => {
      lines.push(`\n### ${snap.title}`);
      if (snap.hasData) {
        lines.push(snap.summary.substring(0, 2000));
      } else {
        lines.push('[No data yet]');
      }
    });
    return lines.join('\n');
  };

  const handleGenerateSynthesis = async () => {
    setGenerating(true);
    const prompt = buildCrossStagePrompt();
    const response = await generateWithGemini({ prompt, temperature: 0.7, maxTokens: 2048 });
    if (response.success) {
      setSynthesis(response.text);
    } else {
      alert(response.error || 'Failed to generate synthesis.');
    }
    setGenerating(false);
  };

  const buildMarkdownReport = (): string => {
    const date = new Date().toISOString().split('T')[0];
    const parts: string[] = [];
    parts.push(`# Project Summary Report`);
    parts.push('');
    parts.push(`Generated: ${date}`);
    parts.push('');
    parts.push('## Stage Overviews');
    snapshots.forEach((snap) => {
      parts.push(`### ${snap.title}`);
      parts.push(snap.hasData ? snap.summary : '_No data yet_');
      parts.push('');
    });
    parts.push('---');
    parts.push('');
    parts.push('## Cross-Stage AI Synthesis');
    parts.push(synthesis ? synthesis : '_No synthesis generated yet_');
    return parts.join('\n');
  };

  const handleDownloadMarkdown = () => {
    const md = buildMarkdownReport();
    const blob = new Blob([md], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `project-summary-${new Date().toISOString().split('T')[0]}.md`;
    a.click();
  };

  const handlePrintPdf = () => {
    window.print();
  };

  const handleShare = async () => {
    const shareText = 'Innovation Project Summary (Design Thinking: Discovery→Define→Ideate→Prototype→Test)';
    const url = window.location.href;
    // Prefer Web Share API where available
    if ((navigator as any).share) {
      try {
        await (navigator as any).share({ title: 'Project Summary', text: shareText, url });
        return;
      } catch (e) {
        // fall back below
      }
    }
    try {
      await navigator.clipboard.writeText(url);
      alert('Link copied to clipboard.');
    } catch {
      // Fallback to mailto
      window.location.href = `mailto:?subject=Project Summary&body=${encodeURIComponent(shareText + '\n' + url)}`;
    }
  };

  if (loading) {
    return (
      <Layout>
        <div className="min-h-[40vh] flex items-center justify-center text-gray-600">Loading summary…</div>
      </Layout>
    );
  }

  const totalWithData = snapshots.filter((s) => s.hasData).length;

  return (
    <Layout>
      <div className="max-w-5xl mx-auto">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Project Summary</h1>
          <p className="text-gray-600">Overview across stages with optional AI synthesis and export.</p>
        </div>

        {/* Actions */}
        <div className="flex flex-wrap gap-3 mb-6">
          <button
            onClick={handleGenerateSynthesis}
            disabled={generating}
            className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
          >
            {generating ? 'Generating…' : 'Generate Cross-Stage Synthesis'}
          </button>
          <button
            onClick={handleDownloadMarkdown}
            className="px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-300"
          >
            Download Markdown
          </button>
          <button
            onClick={handlePrintPdf}
            className="px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-300"
          >
            Print / Save PDF
          </button>
          <button
            onClick={handleShare}
            className="px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-300"
          >
            Share
          </button>
          <div className="ml-auto text-sm text-gray-600 self-center">
            Stage data present: {totalWithData}/5
          </div>
        </div>

        {/* Stage snapshots */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {snapshots.map((snap) => (
            <div key={snap.name} className="bg-white rounded-lg shadow p-5 border border-gray-200">
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-lg font-semibold text-gray-900">{snap.title}</h3>
                <span
                  className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${
                    snap.hasData ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-600'
                  }`}
                >
                  {snap.hasData ? 'Has Data' : 'No Data'}
                </span>
              </div>
              <div className="text-sm text-gray-700 whitespace-pre-wrap">
                {snap.hasData ? snap.summary : 'Add content in this stage to populate the summary.'}
              </div>
            </div>
          ))}
        </div>

        {/* AI Synthesis */}
        <div className="mt-8">
          <h2 className="text-xl font-bold text-gray-900 mb-3">Cross-Stage AI Synthesis</h2>
          {synthesis ? (
            <div className="p-6 bg-white border-2 border-primary-100 rounded-lg">
              <pre className="whitespace-pre-wrap font-sans text-sm text-gray-800">{synthesis}</pre>
            </div>
          ) : (
            <div className="p-4 bg-blue-50 border border-blue-200 rounded-md text-sm text-blue-800">
              Generate a synthesis to create an executive summary and recommended next actions across stages.
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}

export default SummaryView;


