import React, { useEffect, useState, useRef } from "react";
import { useParams, Link, useNavigate } from "react-router-dom";
import Editor from "@monaco-editor/react";
import { useAuth, API_BASE_URL } from "../context/AuthContext";
import { VisualizationEngine } from "../components/VisualizationEngine";
import { AITutorPanel } from "../components/AITutorPanel";
import { 
  Play, 
  Send, 
  BookOpen, 
  Sliders, 
  Code, 
  Info,
  CheckCircle,
  AlertTriangle,
  RotateCcw,
  Loader2,
  ChevronLeft,
  ChevronRight,
  Star,
  Maximize2,
  Minimize2,
  ChevronDown,
  HelpCircle,
  Flame,
  Terminal,
  Cpu,
  GraduationCap,
  History
} from "lucide-react";

interface ChallengeTest {
  id: string;
  input_data: string;
  expected_output: string;
  is_public: boolean;
}

interface ChallengeHint {
  id: string;
  hint_text: string;
  order_index: number;
}

interface ChallengeDetail {
  id: string;
  title: string;
  slug: string;
  description: string;
  concept?: string;
  difficulty: string;
  category: string;
  starter_code: string;
  constraints?: string;
  visualization_type?: string;
  visualization_config?: string;
  tests: ChallengeTest[];
  hints: ChallengeHint[];
  prerequisites?: string;
}

export const Workspace: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const { user, token, refreshUser } = useAuth();
  const navigate = useNavigate();
  
  // Data States
  const [challenge, setChallenge] = useState<ChallengeDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [challengesList, setChallengesList] = useState<{ id: string; slug: string; title: string; prerequisites?: string }[]>([]);
  
  // Code and settings states
  const [code, setCode] = useState("");
  const [fontSize, setFontSize] = useState(14);
  const [showMinimap, setShowMinimap] = useState(false);
  const [draftSavedMessage, setDraftSavedMessage] = useState<string | null>(null);

  // Split panel drag resize states
  const containerRef = useRef<HTMLDivElement>(null);
  const [leftWidth, setLeftWidth] = useState(45); // Split percentage
  const [isResizing, setIsResizing] = useState(false);

  // Tabs selections
  const [leftTab, setLeftTab] = useState<"description" | "concept" | "hints" | "submissions">("description");
  const [rightTab, setRightTab] = useState<"tests" | "output" | "visualization" | "tutor">("tests");
  const [activeTestCaseIndex, setActiveTestCaseIndex] = useState(0);

  // Progressive Hint Reveal states
  const [revealedHints, setRevealedHints] = useState<Record<string, boolean>>({});
  const [showFullSolution, setShowFullSolution] = useState(false);
  const [solutionCode, setSolutionCode] = useState<string | null>(null);
  const [fetchingSolution, setFetchingSolution] = useState(false);
  const [visualizationData, setVisualizationData] = useState<any>(null);

  // Bookmarking states
  const [isBookmarked, setIsBookmarked] = useState(false);
  const [bookmarking, setBookmarking] = useState(false);

  // Run / Submit Simulation state
  const [running, setRunning] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [submissionsHistory, setSubmissionsHistory] = useState<any[]>([]);
  const [actionResponse, setActionResponse] = useState<{
    type: "success" | "info" | "error";
    message: string;
    details?: string;
  } | null>(null);

  // Load challenge detail
  const fetchChallenge = async () => {
    setLoading(true);
    setError(null);
    setActionResponse(null);
    setRevealedHints({});
    setShowFullSolution(false);
    setSolutionCode(null);
    setVisualizationData(null);
    
    try {
      const res = await fetch(`${API_BASE_URL}/challenges/${slug}`);
      if (!res.ok) {
        throw new Error("Failed to load challenge details.");
      }
      const data = await res.json();
      setChallenge(data);

      // Load draft from localStorage if it exists, otherwise default starter_code
      const savedDraft = localStorage.getItem(`neuracode_draft_${data.slug}`);
      if (savedDraft) {
        setCode(savedDraft);
      } else {
        setCode(data.starter_code);
      }

      // Check if bookmarked
      if (token) {
        const bookmarksRes = await fetch(`${API_BASE_URL}/bookmarks`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        if (bookmarksRes.ok) {
          const bookmarks = await bookmarksRes.json();
          setIsBookmarked(bookmarks.includes(data.slug));
        }
      }
    } catch (err: any) {
      setError(err.message || "Unable to fetch challenge details.");
    } finally {
      setLoading(false);
    }
  };

  // Fetch full list of challenges to support Prev/Next navigation
  const fetchChallengesList = async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/challenges`);
      if (res.ok) {
        const data = await res.json();
        setChallengesList(data.map((c: any) => ({
          id: c.id,
          slug: c.slug,
          title: c.title,
          prerequisites: c.prerequisites
        })));
      }
    } catch (err) {
      console.error("Failed to fetch challenges list:", err);
    }
  };

  const fetchSubmissionHistory = async () => {
    if (!token || !challenge) return;
    try {
      const res = await fetch(`${API_BASE_URL}/submissions?challenge_slug=${challenge.slug}`, {
        headers: {
          Authorization: `Bearer ${token}`
        }
      });
      if (res.ok) {
        const data = await res.json();
        setSubmissionsHistory(data);
      }
    } catch (err) {
      console.error("Failed to fetch submission history:", err);
    }
  };

  useEffect(() => {
    fetchChallenge();
  }, [slug]);

  useEffect(() => {
    if (challenge) {
      fetchSubmissionHistory();
    }
  }, [challenge, token]);

  useEffect(() => {
    fetchChallengesList();
  }, []);

  // Draggable panels event handling
  const handleMouseDown = (e: React.MouseEvent) => {
    e.preventDefault();
    setIsResizing(true);
  };

  useEffect(() => {
    if (!isResizing) return;

    const handleMouseMove = (e: MouseEvent) => {
      if (containerRef.current) {
        const containerRect = containerRef.current.getBoundingClientRect();
        const newLeftWidth = ((e.clientX - containerRect.left) / containerRect.width) * 100;
        if (newLeftWidth > 20 && newLeftWidth < 80) {
          setLeftWidth(newLeftWidth);
        }
      }
    };

    const handleMouseUp = () => {
      setIsResizing(false);
    };

    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseup", handleMouseUp);

    return () => {
      window.removeEventListener("mousemove", handleMouseMove);
      window.removeEventListener("mouseup", handleMouseUp);
    };
  }, [isResizing]);

  // Code editor draft handling
  const handleEditorChange = (value: string | undefined) => {
    const val = value || "";
    setCode(val);
    if (challenge) {
      localStorage.setItem(`neuracode_draft_${challenge.slug}`, val);
    }
  };

  const handleEditorBeforeMount = (monaco: any) => {
    monaco.editor.defineTheme("neuracode-dark", {
      base: "vs-dark",
      inherit: true,
      rules: [
        { token: "", foreground: "DCE5DF", background: "111315" },
        { token: "comment", foreground: "66756D", fontStyle: "italic" },
        { token: "keyword", foreground: "FF5DAA" },
        { token: "functions", foreground: "19DFFF" },
        { token: "number", foreground: "FFD84D" },
        { token: "string", foreground: "82E7B0" },
        { token: "type", foreground: "42B8FF" },
        { token: "variable", foreground: "DCE5DF" },
        { token: "operator", foreground: "DCE5DF" }
      ],
      colors: {
        "editor.background": "#111315",
        "editor.foreground": "#DCE5DF",
        "editor.selectionBackground": "#183337",
        "editor.lineHighlightBackground": "#151C19",
        "editorCursor.foreground": "#19DFFF",
        "editorLineNumber.foreground": "#52615A",
        "editorLineNumber.activeForeground": "#19DFFF"
      }
    });
  };

  const handleEditorMount = (editor: any, monaco: any) => {
    monaco.editor.defineTheme("neuracode-dark", {
      base: "vs-dark",
      inherit: true,
      rules: [
        { token: "", foreground: "DCE5DF", background: "111315" },
        { token: "comment", foreground: "66756D", fontStyle: "italic" },
        { token: "keyword", foreground: "FF5DAA" },
        { token: "functions", foreground: "19DFFF" },
        { token: "number", foreground: "FFD84D" },
        { token: "string", foreground: "82E7B0" },
        { token: "type", foreground: "42B8FF" },
        { token: "variable", foreground: "DCE5DF" },
        { token: "operator", foreground: "DCE5DF" }
      ],
      colors: {
        "editor.background": "#111315",
        "editor.foreground": "#DCE5DF",
        "editor.selectionBackground": "#183337",
        "editor.lineHighlightBackground": "#151C19",
        "editorCursor.foreground": "#19DFFF",
        "editorLineNumber.foreground": "#52615A",
        "editorLineNumber.activeForeground": "#19DFFF"
      }
    });
    monaco.editor.setTheme("neuracode-dark");
  };

  const handleSaveDraftManual = () => {
    if (challenge) {
      localStorage.setItem(`neuracode_draft_${challenge.slug}`, code);
      setDraftSavedMessage("Draft saved successfully to localStorage.");
      setTimeout(() => setDraftSavedMessage(null), 3000);
    }
  };

  const handleResetCode = () => {
    if (challenge) {
      if (window.confirm("Are you sure you want to reset your code to the starter template? This will discard your current draft.")) {
        setCode(challenge.starter_code);
        localStorage.removeItem(`neuracode_draft_${challenge.slug}`);
      }
    }
  };

  // Bookmark toggling
  const handleToggleBookmark = async () => {
    if (!token || !challenge) return;
    setBookmarking(true);
    try {
      const res = await fetch(`${API_BASE_URL}/challenges/${challenge.slug}/bookmark`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setIsBookmarked(data.bookmarked);
      }
    } catch (e) {
      console.error("Failed to toggle bookmark", e);
    } finally {
      setBookmarking(false);
    }
  };

  // Run / Submit Simulated Operations (No arbitrary eval, correctly mocked)
  const handleRun = async () => {
    if (!token || !challenge) return;
    setRunning(true);
    setActionResponse(null);
    setRightTab("output");
    try {
      const res = await fetch(`${API_BASE_URL}/executions`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          challenge_slug: challenge.slug,
          code: code,
          language: "python"
        })
      });

      if (res.status === 429) {
        setActionResponse({
          type: "error",
          message: "Too Many Requests",
          details: "Too many executions. Please wait before running another job."
        });
        return;
      }
      
      if (!res.ok) {
        const errData = await res.json();
        setActionResponse({
          type: "error",
          message: "Execution Error",
          details: errData.detail || "Failed to execute your code inside the secure container."
        });
        return;
      }

      const data = await res.json();
      if (data.visualization) {
        setVisualizationData(data.visualization);
      }
      
      if (data.status === "COMPLETED" || data.status === "FAILED" || data.status === "TIMEOUT") {
        if (data.status === "COMPLETED") {
          const allPassed = data.tests.length > 0 && data.tests.every((t: any) => t.status === "passed");
          let detailStr = "";
          
          data.tests.forEach((t: any, idx: number) => {
            detailStr += `Test Case ${idx + 1}\n`;
            detailStr += `────────────────────\n`;
            detailStr += `Expected:\n${t.expected}\n\n`;
            detailStr += `Received:\n${t.actual !== null ? t.actual : "None"}\n\n`;
            if (t.error) {
              detailStr += `Error Traceback:\n${t.error}\n\n`;
            }
            detailStr += `Status:\n${t.status.toUpperCase()}\n\n`;
          });
          
          detailStr += `Runtime:\n${data.runtime_ms} ms\n`;
          if (data.stdout) {
            detailStr += `\nStdout:\n${data.stdout}\n`;
          }
          if (data.stderr) {
            detailStr += `\nStderr:\n${data.stderr}\n`;
          }
          
          setActionResponse({
            type: allPassed ? "success" : "error",
            message: allPassed ? "✓ Execution completed" : "✗ Execution failed",
            details: detailStr
          });
        } else if (data.status === "TIMEOUT") {
          setActionResponse({
            type: "error",
            message: "⏱ Execution timed out",
            details: `Your program exceeded the maximum execution time of 5 seconds.`
          });
        } else {
          // FAILED status
          let detailStr = "";
          if (data.error_type) {
            detailStr += `Type:\n${data.error_type}\n\n`;
          }
          if (data.stderr) {
            detailStr += `Traceback:\n${data.stderr}\n\n`;
          }
          if (data.stdout) {
            detailStr += `Stdout:\n${data.stdout}\n\n`;
          }
          detailStr += `Runtime:\n${data.runtime_ms} ms\n`;
          
          setActionResponse({
            type: "error",
            message: "✗ Execution failed",
            details: detailStr
          });
        }
      } else {
        setActionResponse({
          type: "info",
          message: `Execution state: ${data.status}`,
          details: data.stderr || "Workspace sandboxing completed."
        });
      }
      
    } catch (err) {
      setActionResponse({
        type: "error",
        message: "Failed to establish execution sandbox handshake.",
        details: err instanceof Error ? err.message : String(err)
      });
    } finally {
      setRunning(false);
    }
  };

  const handleRunExperiment = async (customInputs: any) => {
    if (!token || !challenge) return;
    setRunning(true);
    setRightTab("visualization");
    try {
      const res = await fetch(`${API_BASE_URL}/executions`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({
          challenge_slug: challenge.slug,
          code: code,
          language: "python",
          custom_inputs: customInputs
        })
      });

      if (!res.ok) {
        return;
      }

      const data = await res.json();
      if (data.visualization) {
        setVisualizationData(data.visualization);
      }
    } catch (err) {
      console.error("Experiment run failed", err);
    } finally {
      setRunning(false);
    }
  };

  const handleSubmit = async () => {
    if (!token || !challenge) return;
    setSubmitting(true);
    setActionResponse(null);
    setRightTab("output");
    try {
      const res = await fetch(`${API_BASE_URL}/submissions?challenge_slug=${challenge.slug}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`
        },
        body: JSON.stringify({ code, language: "python" })
      });

      if (res.status === 429) {
        setActionResponse({
          type: "error",
          message: "Too Many Requests",
          details: "Too many concurrent runs. Please wait before submitting another job."
        });
        return;
      }

      if (!res.ok) {
        const errData = await res.json();
        setActionResponse({
          type: "error",
          message: "Submission Error",
          details: errData.detail || "Failed to evaluate your submission."
        });
        return;
      }

      const data = await res.json();
      
      let detailStr = "";
      detailStr += `Status:\n${data.status.replace(/_/g, " ")}\n\n`;
      detailStr += `Tests Passed:\n${data.passed_tests} / ${data.total_tests}\n\n`;
      detailStr += `Score:\n${(data.score * 100).toFixed(0)}%\n\n`;
      detailStr += `Runtime:\n${data.runtime_ms} ms\n\n`;
      
      if (data.status === "ACCEPTED") {
        setActionResponse({
          type: "success",
          message: "ACCEPTED ✓",
          details: detailStr
        });
      } else {
        const failedTest = data.results.find((r: any) => r.status !== "passed");
        if (failedTest) {
          detailStr += `First Failed Test ID:\n${failedTest.test_id}\n\n`;
          if (failedTest.actual_output) {
            detailStr += `Received:\n${failedTest.actual_output}\n\n`;
          }
          if (failedTest.error_message) {
            detailStr += `Diagnostic Message:\n${failedTest.error_message}\n\n`;
          }
        }
        setActionResponse({
          type: "error",
          message: data.status.replace(/_/g, " "),
          details: detailStr
        });
      }
      
      // Update local submission list and user streak statistics
      fetchSubmissionHistory();
      refreshUser();
      
    } catch (err) {
      setActionResponse({
        type: "error",
        message: "Connection lost while evaluating submission.",
        details: err instanceof Error ? err.message : String(err)
      });
    } finally {
      setSubmitting(false);
    }
  };

  // Keyboard Shortcuts (Ctrl+Enter, Ctrl+Shift+Enter, Ctrl+S)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "s") {
        e.preventDefault();
        handleSaveDraftManual();
      }
      if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === "Enter") {
        e.preventDefault();
        handleSubmit();
      } else if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
        e.preventDefault();
        handleRun();
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [code, challenge]);

  // Fetch prev/next navigation slugs
  const getNavSlugs = () => {
    if (!challenge || challengesList.length === 0) return { prev: null, next: null };
    const slugs = challengesList.map(c => c.slug);
    const currentIndex = slugs.indexOf(challenge.slug);
    if (currentIndex === -1) return { prev: null, next: null };

    return {
      prev: currentIndex > 0 ? slugs[currentIndex - 1] : null,
      next: currentIndex < slugs.length - 1 ? slugs[currentIndex + 1] : null
    };
  };

  const navSlugs = getNavSlugs();

  // Find unmet prerequisites
  const getUnmetPrerequisites = () => {
    if (!challenge || !challenge.prerequisites) return [];
    const slugs = challenge.prerequisites.split(",").map((s: string) => s.trim()).filter(Boolean);
    return slugs
      .map((s: string) => challengesList.find(c => c.slug === s))
      .filter((c): c is { id: string; slug: string; title: string } => !!c)
      .filter((c: any) => !user?.progress?.some((p: any) => p.challenge_id === c.id && p.completed));
  };

  const unmetPrerequisites = getUnmetPrerequisites();
  const hasUnmetPrerequisites = unmetPrerequisites.length > 0;

  // Find next recommended challenge (next in the list)
  const getNextRecommendedChallenge = () => {
    if (!challenge || challengesList.length === 0) return null;
    const slugs = challengesList.map((c: any) => c.slug);
    const currentIndex = slugs.indexOf(challenge.slug);
    if (currentIndex === -1 || currentIndex >= challengesList.length - 1) return null;
    return challengesList[currentIndex + 1];
  };

  const nextChallengeDetail = getNextRecommendedChallenge();
  const isCompleted = (challenge && user?.progress?.some((p: any) => p.challenge_id === challenge.id && p.completed)) || false;

  const handleRevealSolution = async () => {
    if (showFullSolution) {
      setShowFullSolution(false);
      return;
    }
    if (solutionCode) {
      setShowFullSolution(true);
      return;
    }
    if (!token || !challenge) return;
    setFetchingSolution(true);
    try {
      const res = await fetch(`${API_BASE_URL}/challenges/${challenge.slug}/solution`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setSolutionCode(data.reference_solution);
        setShowFullSolution(true);
      }
    } catch (err) {
      console.error("Failed to fetch reference solution:", err);
    } finally {
      setFetchingSolution(false);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[70svh] bg-dark space-y-4">
        <Loader2 className="w-10 h-10 text-brand animate-spin" />
        <p className="text-slate-400 text-sm font-mono">Mounting AI/ML Workspace...</p>
      </div>
    );
  }

  if (error || !challenge) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[70svh] space-y-4 p-8 bg-dark-card border border-dark-border rounded-lg max-w-xl mx-auto text-center">
        <AlertTriangle className="w-12 h-12 text-red-400" />
        <h2 className="text-lg font-bold text-white font-mono">Challenge not loaded</h2>
        <p className="text-sm text-slate-400">{error || "Challenge Registry returned null."}</p>
        <Link to="/problems" className="bg-brand hover:bg-brand-dark text-dark-deep font-semibold px-4 py-2 rounded text-xs transition-all shadow">
          Return to Problems
        </Link>
      </div>
    );
  }

  const publicTests = challenge.tests ? challenge.tests.filter(t => t.is_public) : [];
  const currentTest = publicTests[activeTestCaseIndex];

  return (
    <div className="flex flex-col h-full overflow-hidden bg-[#050807]">
      
      {/* Workspace Sub Header */}
      <div className="flex flex-wrap items-center justify-between px-6 py-2.5 bg-dark border-b border-dark-border select-none shrink-0 gap-3">
        <div className="flex items-center gap-3">
          <Link to="/problems" className="text-xs text-[#8B958E] hover:text-white transition-colors flex items-center font-semibold">
            <ChevronLeft className="w-3.5 h-3.5 mr-1" /> Problems
          </Link>
          <div className="h-4 w-px bg-dark-border" />
          <h2 className="text-xs font-bold text-white font-mono">{challenge.title}</h2>
          <span className={`text-[9px] font-bold px-2 py-0.5 rounded border uppercase font-mono ${
            challenge.difficulty === "Easy"
              ? "bg-brand-green/10 text-brand-green border-brand-green/20"
              : challenge.difficulty === "Medium"
              ? "bg-brand-yellow/10 text-brand-yellow border-brand-yellow/20"
              : "bg-brand-pink/10 text-brand-pink border-brand-pink/20"
          }`}>
            {challenge.difficulty}
          </span>
          <span className="text-[10px] text-brand bg-brand/10 border border-brand/20 px-2 py-0.5 rounded font-mono font-medium">
            {challenge.category}
          </span>
        </div>

        {/* Workspace Operations Navigation & Controls */}
        <div className="flex items-center gap-2.5">
          {/* Bookmark Button */}
          <button
            onClick={handleToggleBookmark}
            disabled={!token || bookmarking}
            className={`flex items-center gap-1.5 text-xs bg-dark-panel border border-[#29312B] hover:border-brand px-2.5 py-1.5 rounded transition-colors ${
              isBookmarked ? "text-brand-yellow bg-brand-yellow/5 border-brand-yellow/30 font-semibold" : "text-[#AAB4AC] hover:text-white"
            }`}
          >
            <Star className={`w-3.5 h-3.5 ${isBookmarked ? "fill-brand-yellow" : ""}`} />
            {isBookmarked ? "Saved" : "Save"}
          </button>

          {/* Navigation Previous / Next */}
          <div className="flex items-center gap-1">
            <button
              onClick={() => navSlugs.prev && navigate(`/problems/${navSlugs.prev}`)}
              disabled={!navSlugs.prev}
              className="p-1.5 bg-[#111612] hover:bg-dark-hover disabled:opacity-30 border border-[#29312B] rounded text-[#AAB4AC] transition-colors"
              title="Previous challenge"
            >
              <ChevronLeft className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => navSlugs.next && navigate(`/problems/${navSlugs.next}`)}
              disabled={!navSlugs.next}
              className="p-1.5 bg-[#111612] hover:bg-dark-hover disabled:opacity-30 border border-[#29312B] rounded text-[#AAB4AC] transition-colors"
              title="Next challenge"
            >
              <ChevronRight className="w-3.5 h-3.5" />
            </button>
          </div>

          <div className="h-4 w-px bg-dark-border" />

          {/* Draft manual save */}
          <button
            onClick={handleSaveDraftManual}
            className="text-xs bg-dark-panel border border-[#29312B] hover:border-brand text-[#AAB4AC] active:text-brand px-3 py-1.5 rounded transition-all font-semibold relative"
          >
            Save Draft
            {draftSavedMessage && (
              <span className="absolute bottom-full mb-2 left-1/2 transform -translate-x-1/2 bg-brand text-dark-deep font-mono text-[9px] px-2 py-0.5 rounded shadow-lg z-50 whitespace-nowrap">
                {draftSavedMessage}
              </span>
            )}
          </button>

          <button
            onClick={handleResetCode}
            className="p-1.5 bg-dark-panel hover:bg-dark-hover border border-dark-border text-slate-400 hover:text-white rounded transition-colors"
            title="Reset code"
          >
            <RotateCcw className="w-3.5 h-3.5" />
          </button>

          <div className="h-4 w-px bg-dark-border" />

          {/* Run/Submit triggers */}
          <button
            onClick={handleRun}
            disabled={running || submitting || !token}
            className="flex items-center gap-1.5 bg-[#111612] border border-[#29312B] hover:border-brand text-[#AAB4AC] hover:text-[#12DFFF] px-3.5 py-1.5 rounded text-xs font-semibold disabled:opacity-40 transition-colors"
          >
            {running ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Play className="w-3.5 h-3.5 text-[#2FA8FF]" />}
            Run
          </button>

          <button
            onClick={handleSubmit}
            disabled={running || submitting || !token}
            className="flex items-center gap-1.5 bg-[#00E58A] hover:bg-[#00E58A]/90 text-[#050807] px-4 py-1.5 rounded text-xs font-bold disabled:opacity-40 transition-all font-mono"
          >
            {submitting ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Send className="w-3.5 h-3.5 text-[#050807]" />}
            Submit
          </button>
        </div>
      </div>

      {/* Draggable container */}
      <div 
        ref={containerRef}
        className="flex flex-1 flex-col lg:flex-row overflow-hidden relative select-text"
      >
        
        {/* Left Panel (Description, Concept, progressive Hints) */}
        <div 
          className="flex flex-col border-b lg:border-b-0 border-dark-border overflow-hidden bg-[#09100D] text-[#E8EEE9]"
          style={{ width: window.innerWidth > 1024 ? `${leftWidth}%` : "100%" }}
        >
          {/* Tabs */}
          <div className="flex border-b border-[#1C2922] bg-[#0B120F] text-[11px] font-mono shrink-0 select-none">
            <button
              onClick={() => setLeftTab("description")}
              className={`flex items-center gap-1.5 px-5 py-3 font-bold transition-all border-b-2 uppercase tracking-wider ${
                leftTab === "description" ? "border-brand text-brand bg-[#09100D]" : "border-transparent text-slate-400 hover:text-slate-200"
              }`}
            >
              <Info className="w-3.5 h-3.5 text-brand" /> Description
            </button>
            <button
              onClick={() => setLeftTab("concept")}
              className={`flex items-center gap-1.5 px-5 py-3 font-bold transition-all border-b-2 uppercase tracking-wider ${
                leftTab === "concept" ? "border-brand text-brand bg-[#09100D]" : "border-transparent text-slate-400 hover:text-slate-200"
              }`}
            >
              <BookOpen className="w-3.5 h-3.5 text-[#2FA8FF]" /> Concept
            </button>
            <button
              onClick={() => setLeftTab("hints")}
              className={`flex items-center gap-1.5 px-5 py-3 font-bold transition-all border-b-2 uppercase tracking-wider ${
                leftTab === "hints" ? "border-brand text-brand bg-[#09100D]" : "border-transparent text-slate-400 hover:text-slate-200"
              }`}
            >
              <HelpCircle className="w-3.5 h-3.5 text-[#FFD84D]" /> Hints
            </button>
            <button
              onClick={() => setLeftTab("submissions")}
              className={`flex items-center gap-1.5 px-5 py-3 font-bold transition-all border-b-2 uppercase tracking-wider ${
                leftTab === "submissions" ? "border-brand text-brand bg-[#09100D]" : "border-transparent text-slate-400 hover:text-slate-200"
              }`}
            >
              <History className="w-3.5 h-3.5 text-[#FF4FA3]" /> Submissions
            </button>
          </div>

          {/* Left panel contents */}
          <div className="flex-1 overflow-y-auto p-6 space-y-6 text-xs text-[#E8EEE9] leading-relaxed">
            
            {/* Prerequisite Warnings */}
            {hasUnmetPrerequisites && (
              <div className="p-3.5 bg-yellow-500/10 border border-yellow-500/20 text-yellow-400 text-xs rounded-md flex items-start gap-2.5 mb-2 shadow-lg">
                <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5" />
                <div>
                  <span className="font-bold font-mono">Prerequisites Required:</span>
                  <p className="mt-1 leading-relaxed">
                    We recommend completing these challenges first to build up your math kernels:{" "}
                    {unmetPrerequisites.map((p: any, idx: number) => (
                      <React.Fragment key={p.slug}>
                        {idx > 0 && ", "}
                        <Link to={`/problems/${p.slug}`} className="underline hover:text-yellow-300 font-semibold font-mono">
                          {p.title}
                        </Link>
                      </React.Fragment>
                    ))}
                  </p>
                </div>
              </div>
            )}

            {/* Description Tab */}
            {leftTab === "description" && (
              <div className="space-y-6">
                
                {/* Completed Recommendation Card */}
                {isCompleted && nextChallengeDetail && (
                  <div className="p-4 bg-brand/10 border border-brand/20 text-brand text-xs rounded flex items-center justify-between shadow-md">
                    <div className="flex items-center gap-2">
                      <CheckCircle className="w-4 h-4 text-brand shrink-0" />
                      <span>
                        Challenge Solved! Next recommended challenge:{" "}
                        <Link to={`/problems/${nextChallengeDetail.slug}`} className="font-bold underline hover:text-brand-light font-mono">
                          {nextChallengeDetail.title}
                        </Link>
                      </span>
                    </div>
                    <Link 
                      to={`/problems/${nextChallengeDetail.slug}`} 
                      className="flex items-center gap-1 text-[10px] bg-brand hover:bg-brand-dark text-dark-deep px-3 py-1 rounded font-bold uppercase transition-all font-mono"
                    >
                      Go <ChevronRight className="w-3.5 h-3.5" />
                    </Link>
                  </div>
                )}

                <div>
                  <h3 className="text-sm font-bold text-[#18D7FF] mb-2.5 font-mono uppercase tracking-wider">Problem Statement</h3>
                  <div className="whitespace-pre-wrap font-sans text-[#E8EEE9] leading-relaxed">{challenge.description}</div>
                </div>

                {/* Examples Section */}
                <div className="space-y-4">
                  <h4 className="text-[#18D7FF] font-bold text-xs uppercase tracking-wider font-mono">Examples</h4>
                  {publicTests.length > 0 ? (
                    publicTests.slice(0, 2).map((test, index) => (
                      <div key={test.id} className="p-3 bg-[#070B0A] border border-[#242B26] rounded space-y-1.5 font-mono text-xs text-[#D7DED9]">
                        <p className="text-[#9AA59D] font-bold uppercase text-[9px]">Example #{index + 1}</p>
                        <div>
                          <span className="text-[#8B958E] block text-[10px]">Input:</span>
                          <pre className="text-[#18D7FF] whitespace-pre-wrap font-bold bg-[#050706]/40 p-1.5 rounded">{test.input_data}</pre>
                        </div>
                        <div className="pt-1.5 border-t border-[#242B26]/60">
                          <span className="text-[#8B958E] block text-[10px]">Output:</span>
                          <pre className="text-[#12D99B] font-bold bg-[#050706]/40 p-1.5 rounded">{test.expected_output}</pre>
                        </div>
                      </div>
                    ))
                  ) : (
                    <p className="text-slate-500 italic text-xs">No examples provided.</p>
                  )}
                </div>

                {/* Constraints */}
                {challenge.constraints && (
                  <div>
                    <h4 className="text-[#18D7FF] font-bold text-xs uppercase tracking-wider mb-2 font-mono">Constraints</h4>
                    <pre className="p-3 bg-[#070B0A] border border-[#242B26] text-xs rounded text-[#9AA59D] font-mono whitespace-pre-wrap leading-normal">
                      {challenge.constraints}
                    </pre>
                  </div>
                )}
              </div>
            )}

            {/* Concept Tab */}
            {leftTab === "concept" && (
              <div className="space-y-4">
                <h3 className="text-base font-bold text-white">Mathematical Concept</h3>
                {challenge.concept ? (
                  <div className="p-4 bg-dark-deep border border-dark-border rounded-md whitespace-pre-wrap text-slate-300 font-mono text-xs leading-relaxed">
                    {challenge.concept}
                  </div>
                ) : (
                  <p className="text-slate-400 italic text-xs">Conceptual guidelines are preparing for this challenge.</p>
                )}
              </div>
            )}

            {/* Hints Tab (Progressive hint reveal) */}
            {leftTab === "hints" && (
              <div className="space-y-4">
                <h3 className="text-base font-bold text-white mb-2">Progressive Help</h3>
                <p className="text-xs text-dark-muted mb-4 leading-normal">
                  Reveal hints one by one to help you formulate the mathematical matrices.
                </p>

                <div className="space-y-3">
                  {challenge.hints && challenge.hints.length > 0 ? (
                    challenge.hints.map((hint, idx) => {
                      const isRevealed = revealedHints[hint.id];
                      return (
                        <div key={hint.id} className="p-3 bg-dark-card border border-dark-border rounded-lg space-y-2">
                          <div className="flex justify-between items-center select-none">
                            <span className="font-bold text-slate-300 text-xs font-mono">💡 Hint #{idx + 1}</span>
                            {!isRevealed && (
                              <button
                                onClick={() => setRevealedHints(prev => ({ ...prev, [hint.id]: true }))}
                                className="text-[10px] bg-brand/10 hover:bg-brand text-brand hover:text-dark-deep border border-brand/20 px-2 py-0.5 rounded transition-all font-semibold font-mono"
                              >
                                Reveal
                              </button>
                            )}
                          </div>
                          {isRevealed && (
                            <p className="text-xs text-slate-400 leading-relaxed font-mono bg-dark-deep/50 p-2.5 rounded border border-dark-border">
                              {hint.hint_text}
                            </p>
                          )}
                        </div>
                      );
                    })
                  ) : (
                    <p className="text-slate-500 italic text-xs">No hints available for this challenge.</p>
                  )}

                  {/* Reference Solution warning placeholder */}
                  <div className="pt-4 border-t border-dark-border space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-xs text-slate-400 font-bold font-mono">🔒 Reference Solution</span>
                      <button
                        onClick={handleRevealSolution}
                        disabled={fetchingSolution}
                        className="text-[10px] bg-accent-blue/10 hover:bg-accent-blue border border-accent-blue/20 hover:border-accent-blue text-accent-blue hover:text-white px-2.5 py-1 rounded transition-all font-semibold font-mono disabled:opacity-50"
                      >
                        {fetchingSolution ? (
                          <Loader2 className="w-3 h-3 animate-spin inline mr-1" />
                        ) : null}
                        {showFullSolution ? "Hide Solution" : "Reveal Solution"}
                      </button>
                    </div>

                    {showFullSolution && (
                      <div className="p-3 bg-accent-blue/5 border border-accent-blue/20 rounded-md">
                        <p className="text-[11px] text-accent-blue mb-2.5 font-bold">⚠️ Warning: Copying the solution reduces training retention!</p>
                        <pre className="p-3 bg-dark-deep border border-dark-border text-xs rounded font-mono text-slate-300 overflow-x-auto">
                          {solutionCode || "# Solution code is not loaded."}
                        </pre>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            )}

            {/* Submissions Tab (Submission History) */}
            {leftTab === "submissions" && (
              <div className="space-y-4">
                <h3 className="text-base font-bold text-white mb-2 font-mono">Submission History</h3>
                {submissionsHistory.length === 0 ? (
                  <p className="text-xs text-slate-500 italic">No submissions recorded for this challenge yet.</p>
                ) : (
                  <div className="space-y-3 max-h-[70vh] overflow-y-auto pr-1">
                    {submissionsHistory.map((sub: any) => {
                      const dateStr = new Date(sub.created_at).toLocaleString();
                      const statusColor = sub.status === "ACCEPTED" ? "text-green-400 font-semibold" : "text-red-400";
                      
                      return (
                        <div key={sub.id} className="p-4 bg-dark-deep border border-dark-border rounded-lg space-y-2 text-xs font-mono">
                          <div className="flex justify-between items-center select-none">
                            <span className={`font-bold ${statusColor} text-xs uppercase tracking-wider`}>
                              {sub.status.replace(/_/g, " ")} {sub.status === "ACCEPTED" ? "✓" : "✗"}
                            </span>
                            <span className="text-[10px] text-slate-500">{dateStr}</span>
                          </div>
                          
                          <div className="grid grid-cols-2 gap-2 text-[10px] text-slate-400 border-t border-b border-dark-border/40 py-2">
                            <div>Passed: <span className="text-slate-200">{sub.passed_tests} / {sub.total_tests}</span></div>
                            <div>Score: <span className="text-slate-200">{(sub.score * 100).toFixed(0)}%</span></div>
                            <div>Runtime: <span className="text-slate-200">{sub.runtime_ms} ms</span></div>
                            <div>Memory: <span className="text-slate-200">{(sub.memory_bytes / (1024 * 1024)).toFixed(1)} MB</span></div>
                          </div>
                          
                          <div className="space-y-1">
                            <span className="text-[9px] text-slate-500">Submitted Code:</span>
                            <pre className="bg-dark-card p-2 rounded text-[10px] text-slate-300 max-h-32 overflow-y-auto whitespace-pre-wrap font-mono border border-dark-border/20">
                              {sub.code}
                            </pre>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Draggable Divider (Hidden on mobile) */}
        <div 
          onMouseDown={handleMouseDown}
          className="hidden lg:flex w-[6px] hover:w-[8px] bg-dark-border hover:bg-brand/30 cursor-col-resize transition-all shrink-0 items-center justify-center relative z-20"
        >
          <div className="h-8 w-[2px] bg-slate-700" />
        </div>

        {/* Right Panel (Monaco Editor & Bottom Tab panels) */}
        <div 
          className="flex flex-col overflow-hidden bg-dark-deep"
          style={{ width: window.innerWidth > 1024 ? `${100 - leftWidth}%` : "100%" }}
        >
          
          {/* Monaco Editor Header / Controls */}
          <div className="flex items-center justify-between px-4 py-2 border-b border-dark-border bg-[#09100D] text-xs text-slate-400 select-none shrink-0 gap-3">
            <span className="font-mono text-slate-300 flex items-center gap-1.5">
              <Code className="w-3.5 h-3.5 text-brand" /> solution.py
            </span>
            
            {/* Editor Sizing and view parameters */}
            <div className="flex items-center gap-3">
              {/* Minimap toggle */}
              <button
                onClick={() => setShowMinimap(!showMinimap)}
                className={`text-[10px] px-2 py-0.5 border rounded transition-colors ${
                  showMinimap ? "text-brand bg-brand/5 border-brand/30" : "text-slate-500 border-dark-border hover:text-slate-400"
                }`}
              >
                Minimap
              </button>

              {/* Font Size controls */}
              <div className="flex items-center gap-1 bg-dark-deep border border-dark-border px-1.5 py-0.5 rounded font-mono text-[10px]">
                <button
                  onClick={() => setFontSize(prev => Math.max(11, prev - 1))}
                  className="hover:text-white px-1.5"
                  title="Decrease font size"
                >
                  A-
                </button>
                <span className="text-slate-500 border-x border-dark-border px-1.5">{fontSize}px</span>
                <button
                  onClick={() => setFontSize(prev => Math.min(20, prev + 1))}
                  className="hover:text-white px-1.5"
                  title="Increase font size"
                >
                  A+
                </button>
              </div>
            </div>
          </div>

          {/* Monaco Editor Wrapper */}
          <div className="flex-1 bg-dark-editor min-h-[200px]">
            <Editor
              height="100%"
              defaultLanguage="python"
              theme="neuracode-dark"
              beforeMount={handleEditorBeforeMount}
              onMount={handleEditorMount}
              value={code}
              onChange={handleEditorChange}
              options={{
                fontSize: fontSize,
                fontFamily: "JetBrains Mono, Fira Code, Courier New, monospace",
                minimap: { enabled: showMinimap },
                automaticLayout: true,
                padding: { top: 12, bottom: 12 },
                cursorBlinking: "smooth",
                renderLineHighlight: "all",
                folding: true,
                lineNumbers: "on",
                scrollbar: {
                  vertical: "visible",
                  horizontal: "visible"
                }
              }}
            />
          </div>

          {/* Bottom Console Tabs panel */}
          <div className="h-72 border-t border-dark-border bg-[#070C0A] flex flex-col overflow-hidden shrink-0">
            {/* Tabs */}
            <div className="flex border-b border-dark-border bg-dark-deep/40 text-[11px] font-mono shrink-0 select-none overflow-x-auto">
              <button
                onClick={() => setRightTab("tests")}
                className={`flex items-center gap-1.5 px-4 py-2.5 font-bold transition-all border-b-2 uppercase tracking-wider ${
                  rightTab === "tests" ? "border-brand text-brand bg-[#070C0A]" : "border-transparent text-slate-400 hover:text-slate-200"
                }`}
              >
                <Terminal className="w-3.5 h-3.5" /> Test Cases
              </button>
              <button
                onClick={() => setRightTab("output")}
                className={`flex items-center gap-1.5 px-4 py-2.5 font-bold transition-all border-b-2 uppercase tracking-wider ${
                  rightTab === "output" ? "border-brand text-brand bg-[#070C0A]" : "border-transparent text-slate-400 hover:text-slate-200"
                }`}
              >
                <Terminal className="w-3.5 h-3.5" /> Output
              </button>
              <button
                onClick={() => setRightTab("visualization")}
                className={`flex items-center gap-1.5 px-4 py-2.5 font-bold transition-all border-b-2 uppercase tracking-wider ${
                  rightTab === "visualization" ? "border-brand text-brand bg-[#070C0A]" : "border-transparent text-slate-400 hover:text-slate-200"
                }`}
              >
                <Sliders className="w-3.5 h-3.5" /> Visual Experiment
              </button>
              <button
                onClick={() => setRightTab("tutor")}
                className={`flex items-center gap-1.5 px-4 py-2.5 font-bold transition-all border-b-2 uppercase tracking-wider ${
                  rightTab === "tutor" ? "border-brand text-brand bg-[#070C0A]" : "border-transparent text-slate-400 hover:text-slate-200"
                }`}
              >
                <GraduationCap className="w-3.5 h-3.5" /> AI Tutor
              </button>
            </div>

            {/* Bottom tab content panels */}
            <div className="flex-1 overflow-y-auto p-4 bg-[#070C0A] font-mono text-xs text-[#E8EEE9]">
              
              {/* Test Cases Panel */}
              {rightTab === "tests" && (
                <div className="space-y-4">
                  {publicTests.length > 0 ? (
                    <div className="space-y-3">
                      {/* Test case index select */}
                      <div className="flex items-center gap-2 select-none overflow-x-auto pb-1">
                        {publicTests.map((test, index) => (
                          <button
                            key={test.id}
                            onClick={() => setActiveTestCaseIndex(index)}
                            className={`px-3 py-1.5 rounded font-mono text-[10px] font-bold border transition-colors ${
                              activeTestCaseIndex === index
                                ? "bg-[#12DFFF]/10 text-[#12DFFF] border-[#12DFFF]/30"
                                : "bg-dark-card border-dark-border text-slate-400 hover:text-slate-200"
                            }`}
                          >
                            Case {index + 1}
                          </button>
                        ))}
                      </div>

                      {/* Render active case details */}
                      {currentTest && (
                        <div className="p-3 bg-dark border border-dark-border rounded-md space-y-3">
                          <div>
                            <span className="text-slate-500 font-bold text-[9px] uppercase tracking-wider block mb-1">Input Data</span>
                            <code className="text-slate-200 bg-dark-deep px-2 py-1.5 rounded border border-dark-border block whitespace-pre-wrap overflow-x-auto text-[11px] leading-relaxed">
                              {currentTest.input_data}
                            </code>
                          </div>
                          <div className="pt-2 border-t border-dark-border/40">
                            <span className="text-slate-500 font-bold text-[9px] uppercase tracking-wider block mb-1">Expected Output</span>
                            <code className="text-brand bg-dark-deep px-2 py-1.5 rounded border border-dark-border block whitespace-pre-wrap text-[11px]">
                              {currentTest.expected_output}
                            </code>
                          </div>
                        </div>
                      )}
                    </div>
                  ) : (
                    <p className="text-slate-500 italic text-xs">No public test cases registered for this challenge.</p>
                  )}
                </div>
              )}

              {/* Output Panel */}
              {rightTab === "output" && (
                <div className="space-y-3">
                  {actionResponse ? (
                    <div className={`p-4 rounded border text-sm ${
                      actionResponse.type === "success"
                        ? "bg-green-500/10 border-green-500/20 text-green-400"
                        : actionResponse.type === "info"
                        ? "bg-blue-500/10 border-blue-500/20 text-blue-400"
                        : "bg-red-500/10 border-red-500/20 text-red-400"
                    }`}>
                      <h4 className="font-bold flex items-center gap-1.5 mb-2 font-mono">
                        {actionResponse.type === "success" && <CheckCircle className="w-4 h-4" />}
                        {actionResponse.type === "error" && <AlertTriangle className="w-4 h-4" />}
                        {actionResponse.message}
                      </h4>
                      {actionResponse.details && (
                        <pre className="whitespace-pre-wrap mt-2.5 p-3 bg-dark-deep/90 rounded border border-dark-border text-xs text-slate-300 font-mono leading-relaxed">
                          {actionResponse.details}
                        </pre>
                      )}
                      
                      {/* Contextual AI Tutor actions */}
                      {actionResponse.type === "error" && (
                        <div className="mt-3 pt-2 border-t border-red-500/20 flex items-center justify-between">
                          <span className="text-[11px] text-red-300/80 font-mono">Need guidance with this error?</span>
                          <button
                            onClick={() => setRightTab("tutor")}
                            className="flex items-center gap-1.5 text-xs font-mono font-bold bg-[#18D7FF]/10 hover:bg-[#18D7FF]/20 text-[#18D7FF] border border-[#18D7FF]/30 px-3 py-1.5 rounded transition-all shadow"
                          >
                            <GraduationCap className="w-3.5 h-3.5" />
                            Ask AI Tutor why this failed
                          </button>
                        </div>
                      )}
                    </div>
                  ) : (
                    <div className="flex flex-col items-center justify-center py-6 text-center text-slate-500">
                      <Terminal className="w-8 h-8 text-dark-muted mb-2 animate-pulse" />
                      <p className="text-xs">Run or Submit code to inspect validation diagnostics.</p>
                      <p className="text-[10px] text-dark-muted mt-1 leading-normal max-w-sm">
                        Sandbox docker workers will compile and output assertion reports in Phase 3.
                      </p>
                    </div>
                  )}
                </div>
              )}

              {/* Visualizations Hyperparameters Experiment tab */}
              {rightTab === "visualization" && challenge && (
                <VisualizationEngine
                  challenge={challenge}
                  visualizationData={visualizationData}
                  onRunExperiment={handleRunExperiment}
                  running={running}
                />
              )}

              {/* AI Tutor Panel */}
              {rightTab === "tutor" && challenge && (
                <AITutorPanel
                  challengeSlug={challenge.slug}
                  challengeTitle={challenge.title}
                  userCode={code}
                  lastError={actionResponse?.type === "error" ? actionResponse.details : null}
                  visualizationData={visualizationData}
                />
              )}

            </div>
          </div>

        </div>

      </div>
      {/* Bottom Status Bar */}
      <div className="h-[28px] border-t border-[#1C2922] bg-[#080D0B] flex items-center justify-between px-4 text-[10px] font-mono text-[#59635D] select-none shrink-0">
        <div className="flex items-center gap-4">
          <span className="flex items-center gap-1.5 text-[#8B958E]">
            <span className="w-1.5 h-1.5 rounded-full bg-[#00E58A]" /> Python 3.11
          </span>
          <span>Auto-run: OFF</span>
          <span>Tests: {publicTests.length}</span>
          <span>Time Limit: 5s</span>
          <span>Memory Limit: 256MB</span>
        </div>
        <div className="flex items-center gap-4">
          <span className="flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-[#00E58A]" /> All tests passed
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-[#FFD84D]" /> 1 test failed
          </span>
          <span className="flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 rounded-full bg-[#FF4F5E]" /> Runtime error
          </span>
        </div>
      </div>
    </div>
  );
};
