import React, { useState, useEffect, useRef } from 'react';
import {
  Play,
  Terminal,
  Activity,
  CheckCircle2,
  LayoutDashboard,
  Zap,
  Shield,
  Search,
  Cpu,
  FileText,
  UserCheck
} from 'lucide-react';
import { motion } from 'framer-motion';
import ReactMarkdown from 'react-markdown';

interface LogEntry {
  time: string;
  msg: string;
  isError?: boolean;
}

interface NodeState {
  id: string;
  label: string;
  icon: React.ReactNode;
  description: string;
  status: 'idle' | 'active' | 'completed';
}

const INITIAL_NODES: NodeState[] = [
  { id: 'lead_planner', label: 'Lead Orchestrator', icon: <Cpu size={20} />, description: 'Planning testing mission...', status: 'idle' },
  { id: 'unit_static_node', label: 'Unit/Static Analysis', icon: <Search size={20} />, description: 'Analyzing code quality...', status: 'idle' },
  { id: 'functional_node', label: 'Functional Expert', icon: <Zap size={20} />, description: 'Verifying core features...', status: 'idle' },
  { id: 'e2e_node', label: 'E2E Specialist', icon: <LayoutDashboard size={20} />, description: 'Testing user journeys...', status: 'idle' },
  { id: 'security_node', label: 'Security Specialist', icon: <Shield size={20} />, description: 'Scanning for vulnerabilities...', status: 'idle' },
  { id: 'performance_node', label: 'Performance Expert', icon: <Activity size={20} />, description: 'Running load tests...', status: 'idle' },
  { id: 'reviewer', label: 'Quality Reviewer', icon: <UserCheck size={20} />, description: 'Consolidating findings...', status: 'idle' },
  { id: 'finalizer', label: 'Report Finalizer', icon: <FileText size={20} />, description: 'Generating final report...', status: 'idle' },
];

function App() {
  const [missionInput, setMissionInput] = useState('');
  const [isRunning, setIsRunning] = useState(false);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [nodes, setNodes] = useState<NodeState[]>(INITIAL_NODES);
  const [finalReport, setFinalReport] = useState<string | null>(null);
  const logRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (logRef.current) {
      logRef.current.scrollTop = logRef.current.scrollHeight;
    }
  }, [logs]);

  const addLog = (msg: string, isError = false) => {
    const time = new Date().toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' });
    setLogs(prev => [...prev, { time, msg, isError }]);
  };

  const startMission = async () => {
    if (!missionInput) return;

    setIsRunning(true);
    setFinalReport(null);
    setLogs([]);
    setNodes(INITIAL_NODES);
    addLog(`Initiating mission: ${missionInput}`);

    try {
      const response = await fetch('http://localhost:8000/mission/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: missionInput }),
      });

      const reader = response.body?.getReader();
      const decoder = new TextDecoder();

      if (!reader) throw new Error("Stream not available");

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const payload = JSON.parse(line.substring(6));
            handleServerEvent(payload);
          }
        }
      }
    } catch (err: any) {
      addLog(`Error: ${err.message}`, true);
      setIsRunning(false);
    }
  };

  const handleServerEvent = (payload: any) => {
    switch (payload.event) {
      case 'start':
        addLog(payload.message);
        break;
      case 'node_update':
        const nodeName = payload.node;
        addLog(`Processing at node: ${nodeName}`);
        setNodes(prev => prev.map(n => {
          if (n.id === nodeName) return { ...n, status: 'active' };
          if (n.status === 'active') return { ...n, status: 'completed' };
          return n;
        }));

        if (nodeName === 'finalizer' && payload.data?.final_report) {
          setFinalReport(payload.data.final_report);
        }
        break;
      case 'complete':
        addLog(payload.message);
        setIsRunning(false);
        setNodes(prev => prev.map(n => n.status === 'active' ? { ...n, status: 'completed' } : n));
        break;
      case 'error':
        addLog(payload.message, true);
        setIsRunning(false);
        break;
    }
  };

  return (
    <div className="app-container">
      <header>
        <div>
          <h1>AGENTIC QA ORGANIZATION</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>Autonomous Testing & Quality Orchestration</p>
        </div>
        <div className="glass-card" style={{ padding: '0.5rem 1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <div style={{ width: 8, height: 8, borderRadius: '50%', background: isRunning ? 'var(--accent-secondary)' : '#444' }} />
          <span style={{ fontSize: '0.8rem', fontWeight: 600 }}>{isRunning ? 'MISSION ACTIVE' : 'READY'}</span>
        </div>
      </header>

      <div className="dashboard-grid">
        <main className="graph-container">
          <section className="glass-card mission-input-section">
            <h2 style={{ fontSize: '1rem', marginBottom: '0.5rem' }}>MISSION CONTROL</h2>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <input
                type="text"
                placeholder="Ex: Test the performance of the login page..."
                value={missionInput}
                onChange={(e) => setMissionInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && startMission()}
                disabled={isRunning}
              />
              <button onClick={startMission} disabled={isRunning || !missionInput}>
                {isRunning ? <Activity className="animate-spin" size={20} /> : <Play size={20} />}
              </button>
            </div>
          </section>

          <section className="nodes-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '1rem' }}>
            {nodes.map((node) => (
              <motion.div
                key={node.id}
                className={`node ${node.status}`}
                layout
                initial={false}
              >
                <div className="node-icon" style={{
                  background: node.status === 'active' ? 'var(--accent-primary)' :
                    node.status === 'completed' ? 'var(--accent-secondary)' : 'rgba(255,255,255,0.05)'
                }}>
                  {node.icon}
                </div>
                <div className="node-content">
                  <h3>{node.label}</h3>
                  <p>{node.status === 'active' ? node.description : node.status === 'completed' ? 'Tasks completed.' : 'Waiting...'}</p>
                </div>
                {node.status === 'completed' && <CheckCircle2 size={16} color="var(--accent-secondary)" style={{ marginLeft: 'auto' }} />}
              </motion.div>
            ))}
          </section>

          {finalReport && (
            <motion.section
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="glass-card"
              style={{ marginTop: '1rem' }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1rem', borderBottom: '1px solid var(--border-glass)', paddingBottom: '0.75rem' }}>
                <FileText size={20} color="var(--accent-primary)" />
                <h2 style={{ fontSize: '1.1rem' }}>EXECUTIVE SUMMARY</h2>
              </div>
              <div className="markdown-content" style={{ fontSize: '0.95rem', lineHeight: '1.6', color: '#cbd5e1' }}>
                <ReactMarkdown>{finalReport}</ReactMarkdown>
              </div>
            </motion.section>
          )}
        </main>

        <aside className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '1rem', height: 'fit-content' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Terminal size={18} color="var(--accent-primary)" />
            <h2 style={{ fontSize: '0.9rem', fontWeight: 700 }}>LIVE ACTIVITY STREAM</h2>
          </div>
          <div className="log-container" ref={logRef}>
            {logs.length === 0 && <p style={{ color: '#444' }}>No active logs...</p>}
            {logs.map((log, i) => (
              <div key={i} className="log-entry">
                <span className="log-time">{log.time}</span>
                <span className={`log-msg ${log.isError ? 'error' : ''}`}>{log.msg}</span>
              </div>
            ))}
          </div>
        </aside>
      </div>

      <style>{`
        .animate-spin {
          animation: spin 1s linear infinite;
        }
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        .markdown-content h1, .markdown-content h2, .markdown-content h3 {
          margin-top: 1.5rem;
          margin-bottom: 0.75rem;
          color: white;
        }
        .markdown-content ul, .markdown-content ol {
          margin-left: 1.5rem;
          margin-bottom: 1rem;
        }
        .markdown-content li {
          margin-bottom: 0.5rem;
        }
        .markdown-content blockquote {
          border-left: 4px solid var(--accent-primary);
          padding-left: 1rem;
          margin: 1rem 0;
          color: var(--text-muted);
        }
      `}</style>
    </div>
  );
}

export default App;
