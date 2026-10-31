import React, { useEffect, useState, useRef } from "react";
import { 
  Bot, 
  User, 
  Send, 
  Lightbulb, 
  BookOpen, 
  Code2, 
  AlertCircle, 
  BarChart2, 
  Trash2, 
  Loader2, 
  Sparkles,
  HelpCircle,
  CheckCircle2,
  AlertTriangle
} from "lucide-react";
import { useAuth, API_BASE_URL } from "../context/AuthContext";

interface Message {
  id?: string;
  role: "user" | "assistant";
  content: string;
  created_at?: string;
}

interface AITutorPanelProps {
  challengeSlug: string;
  challengeTitle?: string;
  userCode: string;
  lastError?: string | null;
  visualizationData?: any;
  onNavigateToTab?: (tab: string) => void;
}

export const AITutorPanel: React.FC<AITutorPanelProps> = ({
  challengeSlug,
  challengeTitle,
  userCode,
  lastError,
  visualizationData,
  onNavigateToTab,
}) => {
  const { token } = useAuth();
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [fetchingHistory, setFetchingHistory] = useState(true);
  const [errorBanner, setErrorBanner] = useState<string | null>(null);
  const [hintLevel, setHintLevel] = useState(1);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom of chat
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  // Load existing conversation on mount or challenge change
  useEffect(() => {
    let isMounted = true;
    const fetchHistory = async () => {
      if (!token || !challengeSlug) {
        setFetchingHistory(false);
        return;
      }
      setFetchingHistory(true);
      try {
        const res = await fetch(`${API_BASE_URL}/tutor/conversations/${challengeSlug}`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (res.ok && isMounted) {
          const data = await res.json();
          if (data.messages && Array.isArray(data.messages)) {
            setMessages(
              data.messages.map((m: any) => ({
                id: m.id,
                role: m.role === "tutor" ? "assistant" : m.role,
                content: m.content,
                created_at: m.created_at,
              }))
            );
          }
        }
      } catch (err) {
        console.error("Failed to load tutor history:", err);
      } finally {
        if (isMounted) setFetchingHistory(false);
      }
    };

    fetchHistory();
    return () => {
      isMounted = false;
    };
  }, [challengeSlug, token]);

  const handleSendMessage = async (customPrompt?: string, actionType?: string) => {
    const query = (customPrompt || inputMessage).trim();
    if (!query || loading || !token) return;

    setErrorBanner(null);
    setInputMessage("");

    // Append user message immediately
    const userMsg: Message = { role: "user", content: query };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      const payload: any = {
        challenge_slug: challengeSlug,
        message: query,
        user_code: userCode,
      };

      if (lastError) {
        payload.execution_error = lastError;
      }
      if (visualizationData) {
        payload.visualization_state = visualizationData;
      }
      if (actionType === "hint") {
        payload.hint_level = hintLevel;
        // Increment hint level for next time, up to 4
        setHintLevel((prev) => Math.min(4, prev + 1));
      }

      const res = await fetch(`${API_BASE_URL}/tutor/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(payload),
      });

      if (res.status === 429) {
        setErrorBanner("Rate limit reached (15 messages/5 min). Please pause briefly before asking again.");
        setMessages((prev) => [
          ...prev,
          {
            role: "assistant",
            content: "⚠️ Rate limit reached (15 queries per 5 minutes). Please review your code or hints while I refresh!",
          },
        ]);
        return;
      }

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error(errData.detail || "Failed to reach AI Tutor.");
      }

      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.reply || data.content || "Response received.",
        },
      ]);
    } catch (err: any) {
      console.error("AI Tutor error:", err);
      setErrorBanner(err.message || "Failed to get AI Tutor response.");
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "❌ Sorry, I encountered an error analyzing your request. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleClearHistory = async () => {
    if (!token || !challengeSlug) return;
    if (!window.confirm("Clear tutor conversation history for this challenge?")) return;

    try {
      await fetch(`${API_BASE_URL}/tutor/conversations/${challengeSlug}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });
      setMessages([]);
      setHintLevel(1);
    } catch (err) {
      console.error("Failed to clear history:", err);
    }
  };

  return (
    <div className="flex flex-col h-full bg-[#070C0A] font-sans text-xs">
      
      {/* Quick Action Toolbar */}
      <div className="p-2.5 bg-[#09100D] border-b border-[#1C2922] flex flex-wrap items-center justify-between gap-2 shrink-0">
        <div className="flex items-center gap-1.5 overflow-x-auto py-0.5 scrollbar-none">
          <button
            onClick={() => handleSendMessage(`Give me a Level ${hintLevel} hint without giving away the full code.`, "hint")}
            disabled={loading}
            className="flex items-center gap-1 text-[10px] font-mono font-bold bg-[#FFD84D]/10 hover:bg-[#FFD84D]/20 text-[#FFD84D] border border-[#FFD84D]/30 px-2.5 py-1 rounded transition-colors disabled:opacity-40 whitespace-nowrap"
            title="Request progressive hint"
          >
            <Lightbulb className="w-3 h-3" />
            Hint L{hintLevel}
          </button>

          <button
            onClick={() => handleSendMessage("Explain the core mathematical concept behind this challenge and what formula I should use.", "concept")}
            disabled={loading}
            className="flex items-center gap-1 text-[10px] font-mono font-bold bg-[#18D7FF]/10 hover:bg-[#18D7FF]/20 text-[#18D7FF] border border-[#18D7FF]/30 px-2.5 py-1 rounded transition-colors disabled:opacity-40 whitespace-nowrap"
          >
            <BookOpen className="w-3 h-3" />
            Explain Concept
          </button>

          <button
            onClick={() => handleSendMessage("Review my current Python implementation line by line and point out any bugs, dimension mismatches, or edge cases.", "code")}
            disabled={loading}
            className="flex items-center gap-1 text-[10px] font-mono font-bold bg-[#FF5DAA]/10 hover:bg-[#FF5DAA]/20 text-[#FF5DAA] border border-[#FF5DAA]/30 px-2.5 py-1 rounded transition-colors disabled:opacity-40 whitespace-nowrap"
          >
            <Code2 className="w-3 h-3" />
            Explain Code
          </button>

          {lastError && (
            <button
              onClick={() => handleSendMessage("Explain this execution/test error and guide me on how to fix it: " + lastError, "error")}
              disabled={loading}
              className="flex items-center gap-1 text-[10px] font-mono font-bold bg-red-500/15 hover:bg-red-500/25 text-red-400 border border-red-500/40 px-2.5 py-1 rounded transition-colors disabled:opacity-40 animate-pulse whitespace-nowrap"
            >
              <AlertCircle className="w-3 h-3" />
              Explain Error
            </button>
          )}

          {visualizationData && (
            <button
              onClick={() => handleSendMessage("Explain what this visualization represents and how my tensor outputs map to it.", "graph")}
              disabled={loading}
              className="flex items-center gap-1 text-[10px] font-mono font-bold bg-[#82E7B0]/10 hover:bg-[#82E7B0]/20 text-[#82E7B0] border border-[#82E7B0]/30 px-2.5 py-1 rounded transition-colors disabled:opacity-40 whitespace-nowrap"
            >
              <BarChart2 className="w-3 h-3" />
              Explain Graph
            </button>
          )}
        </div>

        {messages.length > 0 && (
          <button
            onClick={handleClearHistory}
            className="p-1 text-[#66756D] hover:text-red-400 transition-colors"
            title="Clear Chat History"
          >
            <Trash2 className="w-3.5 h-3.5" />
          </button>
        )}
      </div>

      {/* Error banner if any */}
      {errorBanner && (
        <div className="px-3 py-1.5 bg-red-500/10 border-b border-red-500/20 text-red-400 text-[11px] font-mono flex items-center gap-2 shrink-0">
          <AlertTriangle className="w-3.5 h-3.5 shrink-0" />
          <span>{errorBanner}</span>
        </div>
      )}

      {/* Messages Scroll View */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {fetchingHistory ? (
          <div className="flex flex-col items-center justify-center h-full text-[#66756D] space-y-2 py-8">
            <Loader2 className="w-6 h-6 animate-spin text-[#18D7FF]" />
            <p className="text-[11px] font-mono">Syncing AI Tutor memory...</p>
          </div>
        ) : messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full py-6 text-center text-[#66756D] space-y-3">
            <div className="w-10 h-10 rounded-full bg-[#18D7FF]/10 border border-[#18D7FF]/20 flex items-center justify-center">
              <Bot className="w-5 h-5 text-[#18D7FF]" />
            </div>
            <div className="max-w-xs space-y-1">
              <p className="font-bold text-white font-mono text-xs">NeuraCode Intelligent AI Tutor</p>
              <p className="text-[11px] leading-relaxed text-[#9AA59D]">
                I can guide you through loss backpropagation, tensor shape alignment, or algorithm concepts step-by-step without spoiling solutions.
              </p>
            </div>
            <div className="pt-2 flex flex-wrap justify-center gap-1.5 max-w-sm">
              <button
                onClick={() => handleSendMessage("What approach should I take for " + (challengeTitle || "this challenge") + "?")}
                className="text-[10px] font-mono bg-[#111815] hover:bg-[#18231E] border border-[#24332A] text-[#B8C4BC] px-2.5 py-1 rounded transition-colors"
              >
                💡 How should I start?
              </button>
              <button
                onClick={() => handleSendMessage("Explain the tensor shapes required for this function.")}
                className="text-[10px] font-mono bg-[#111815] hover:bg-[#18231E] border border-[#24332A] text-[#B8C4BC] px-2.5 py-1 rounded transition-colors"
              >
                📐 Tensor shape rules?
              </button>
            </div>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex items-start gap-2.5 ${
                msg.role === "user" ? "flex-row-reverse" : "flex-row"
              }`}
            >
              <div
                className={`w-6 h-6 rounded-full flex items-center justify-center shrink-0 text-[10px] font-bold ${
                  msg.role === "user"
                    ? "bg-[#00E58A]/10 text-[#00E58A] border border-[#00E58A]/30"
                    : "bg-[#18D7FF]/10 text-[#18D7FF] border border-[#18D7FF]/30"
                }`}
              >
                {msg.role === "user" ? <User className="w-3.5 h-3.5" /> : <Bot className="w-3.5 h-3.5" />}
              </div>

              <div
                className={`max-w-[85%] rounded-lg p-3 leading-relaxed text-xs font-mono shadow-sm ${
                  msg.role === "user"
                    ? "bg-[#0D1814] border border-[#1B3026] text-[#E8EEE9]"
                    : "bg-[#0A120E] border border-[#1C2922] text-[#DCE5DF]"
                }`}
              >
                <div className="flex items-center justify-between gap-4 mb-1 border-b border-[#1C2922]/60 pb-1">
                  <span className="text-[9px] font-bold uppercase tracking-wider text-[#66756D]">
                    {msg.role === "user" ? "Researcher" : "AI Tutor"}
                  </span>
                  {msg.created_at && (
                    <span className="text-[9px] text-[#4A5750]">
                      {new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  )}
                </div>

                <div className="whitespace-pre-wrap font-sans text-[12px] leading-relaxed select-text">
                  {msg.content}
                </div>
              </div>
            </div>
          ))
        )}

        {loading && (
          <div className="flex items-start gap-2.5">
            <div className="w-6 h-6 rounded-full bg-[#18D7FF]/10 border border-[#18D7FF]/30 flex items-center justify-center shrink-0">
              <Bot className="w-3.5 h-3.5 text-[#18D7FF]" />
            </div>
            <div className="bg-[#0A120E] border border-[#1C2922] p-3 rounded-lg flex items-center gap-2 text-xs font-mono text-[#82E7B0]">
              <Loader2 className="w-4 h-4 animate-spin text-[#18D7FF]" />
              <span>Analyzing code context & formula rules...</span>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Field */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSendMessage();
        }}
        className="p-3 bg-[#09100D] border-t border-[#1C2922] flex items-center gap-2 shrink-0"
      >
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          placeholder="Ask AI Tutor (e.g. 'Why am I getting a shape mismatch on axis 1?')..."
          disabled={loading}
          className="flex-1 bg-[#050807] border border-[#1C2922] focus:border-[#18D7FF]/50 rounded px-3 py-2 text-xs text-[#E8EEE9] placeholder-[#52615A] focus:outline-none focus:ring-1 focus:ring-[#18D7FF]/20 font-sans transition-all disabled:opacity-50"
        />
        <button
          type="submit"
          disabled={loading || !inputMessage.trim()}
          className="bg-[#18D7FF] hover:bg-[#18D7FF]/90 text-[#050807] px-3.5 py-2 rounded text-xs font-mono font-bold flex items-center gap-1.5 transition-all disabled:opacity-40 shrink-0"
        >
          {loading ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Send className="w-3.5 h-3.5" />}
          <span>Send</span>
        </button>
      </form>

    </div>
  );
};
