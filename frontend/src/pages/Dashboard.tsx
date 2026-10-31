import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth, API_BASE_URL } from "../context/AuthContext";
import { 
  Trophy, 
  Flame, 
  CheckCircle, 
  Map, 
  ArrowRight,
  Code,
  BookOpen,
  Plus
} from "lucide-react";

interface LearningPath {
  id: string;
  title: string;
  slug: string;
  description: string;
  category: string;
  items: any[];
}

export const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [learningPaths, setLearningPaths] = useState<LearningPath[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPaths = async () => {
      try {
        const res = await fetch(`${API_BASE_URL}/learning-paths`);
        if (res.ok) {
          const data = await res.json();
          setLearningPaths(data);
        }
      } catch (err) {
        console.error("Error fetching learning paths", err);
      } finally {
        setLoading(false);
      }
    };
    fetchPaths();
  }, []);

  return (
    <div className="space-y-6 max-w-6xl mx-auto select-none">
      {/* Welcome Banner */}
      <div className="p-6 md:p-8 bg-dark-card border border-dark-border rounded shadow-xl relative overflow-hidden">
        <div className="relative z-10">
          <span className="text-[9px] font-mono text-brand uppercase tracking-widest block mb-2">Workspace Overview</span>
          <h1 className="text-2xl font-bold text-white tracking-tight">
            Welcome, researcher <span className="text-brand font-mono">@{user?.profile?.display_name || user?.email.split("@")[0] || "operator"}</span>
          </h1>
          <p className="text-[#8B958E] mt-2 max-w-2xl text-xs leading-relaxed font-sans">
            AI/ML Coding Environment initialized. Select an active learning path to implement numerical functions, execute sandboxed tests, and plot results.
          </p>
        </div>
      </div>

      {/* Grid Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left 2 Columns: Learning Tracks & Recent */}
        <div className="lg:col-span-2 space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <Map className="w-5 h-5 text-brand" />
              Active Learning Paths
            </h2>
            <Link to="/learn" className="text-xs text-brand hover:underline font-semibold flex items-center gap-1">
              Browse All <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {[1, 2].map((i) => (
                <div key={i} className="h-40 bg-dark-card border border-dark-border rounded-lg animate-pulse" />
              ))}
            </div>
          ) : learningPaths.length === 0 ? (
            <div className="p-8 text-center bg-dark-card border border-dark-border rounded-lg">
              <p className="text-slate-400 text-sm">No learning paths found.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {learningPaths.map((path) => (
                <div key={path.id} className="p-4 bg-dark-card border border-dark-border hover:border-brand/40 transition-all rounded flex flex-col justify-between group">
                  <div>
                    <span className="text-[9px] text-brand-cyan bg-dark-panel border border-brand-cyan/20 px-2 py-0.5 rounded font-mono uppercase tracking-wider font-semibold">
                      {path.category}
                    </span>
                    <h3 className="text-sm font-bold text-white mt-2.5 group-hover:text-brand font-mono transition-colors">
                      {path.title}
                    </h3>
                    <p className="text-xs text-[#8B958E] mt-1.5 line-clamp-2">
                      {path.description}
                    </p>
                  </div>
                  <div className="mt-4 pt-3 border-t border-dark-border/40 flex items-center justify-between text-[11px]">
                    <span className="text-[#59635D] font-mono">
                      {path.items?.length || 0} kernels
                    </span>
                    <Link 
                      to={`/problems`} 
                      className="font-bold text-brand flex items-center gap-1 hover:underline font-mono"
                    >
                      Start Path <ArrowRight className="w-3.5 h-3.5" />
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Recent Challenges Section */}
          <div className="space-y-3">
            <h2 className="text-sm font-bold text-white flex items-center gap-2 font-mono uppercase tracking-wider">
              <Code className="w-4 h-4 text-accent-blue" />
              Recent Challenge Attempts
            </h2>
            <div className="p-8 text-center bg-dark-card border border-dark-border rounded">
              <p className="text-[#8B958E] text-xs font-mono">No active challenge logs recorded.</p>
              <Link 
                to="/problems" 
                className="mt-4 inline-flex items-center gap-1.5 bg-dark-panel hover:bg-brand border border-dark-border hover:border-brand text-[#C8D0CA] hover:text-dark-deep font-bold px-3 py-1.5 rounded text-xs transition-all font-mono"
              >
                Go to Problems
              </Link>
            </div>
          </div>
        </div>

        {/* Right 1 Column: Stats Overview */}
        <div className="space-y-4">
          <span className="text-[10px] font-mono text-brand uppercase tracking-widest block">Metrics & Progress</span>
          
          <div className="grid grid-cols-1 gap-3">
            {/* XP Card */}
            <div className="p-4 bg-dark-card border border-dark-border rounded flex items-center justify-between">
              <div>
                <p className="text-[9px] text-[#8B958E] font-mono uppercase tracking-wider">Experience Points</p>
                <p className="text-lg font-bold text-white mt-1 font-mono">{user?.profile?.xp ?? 0} <span className="text-brand text-xs">XP</span></p>
              </div>
              <div className="w-8 h-8 rounded bg-brand/5 border border-brand/20 flex items-center justify-center text-brand">
                <Trophy className="w-4 h-4" />
              </div>
            </div>

            {/* Streak Card */}
            <div className="p-4 bg-dark-card border border-dark-border rounded flex items-center justify-between">
              <div>
                <p className="text-[9px] text-[#8B958E] font-mono uppercase tracking-wider">Current Streak</p>
                <p className="text-lg font-bold text-white mt-1 font-mono">{user?.streak?.current_streak ?? 0} <span className="text-brand-yellow text-xs">DAYS</span></p>
              </div>
              <div className="w-8 h-8 rounded bg-brand-yellow/5 border border-brand-yellow/20 flex items-center justify-center text-brand-yellow">
                <Flame className="w-4 h-4 fill-brand-yellow/10" />
              </div>
            </div>

            {/* Solved Card */}
            <div className="p-4 bg-dark-card border border-dark-border rounded flex items-center justify-between">
              <div>
                <p className="text-[9px] text-[#8B958E] font-mono uppercase tracking-wider">Challenges Solved</p>
                <p className="text-lg font-bold text-white mt-1 font-mono">
                  {user?.progress?.filter((p: any) => p.completed).length ?? 0} <span className="text-brand-green text-xs">SOLVED</span>
                </p>
              </div>
              <div className="w-8 h-8 rounded bg-brand-green/5 border border-brand-green/20 flex items-center justify-center text-brand-green">
                <CheckCircle className="w-4 h-4" />
              </div>
            </div>

            {/* Badges / Achievements Summary */}
            <div className="p-4 bg-dark-card border border-dark-border rounded space-y-2">
              <p className="text-[9px] text-[#8B958E] font-mono uppercase tracking-wider">Achievements</p>
              <div className="text-[10px] text-[#59635D] font-mono leading-normal">
                Unlock badges and operational medals by completing learning path nodes.
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};
