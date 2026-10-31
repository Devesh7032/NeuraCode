import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { useAuth, API_BASE_URL } from "../context/AuthContext";
import { 
  Search, 
  Loader2, 
  RefreshCw, 
  AlertCircle, 
  CheckCircle2, 
  Circle, 
  HelpCircle,
  Star,
  Tag,
  BookOpen,
  ChevronRight,
  ChevronDown
} from "lucide-react";

interface Challenge {
  id: string;
  title: string;
  slug: string;
  difficulty: string;
  category: string;
  subcategory?: string;
  tags?: string;
  status: string;
}

const CURRICULUM_TREE: Record<string, string[]> = {
  "Python for AI": ["Python for AI"],
  "Mathematics": ["Linear Algebra", "Calculus", "Probability & Statistics"],
  "Machine Learning": ["Regression", "Classification", "Clustering", "Dimensionality Reduction", "Evaluation"],
  "Deep Learning": ["Neural Networks", "Activations", "Loss Functions", "Backpropagation", "Optimization"],
  "Computer Vision": ["Image Processing", "Convolution", "CNNs"],
  "NLP": ["Tokenization", "TF-IDF", "Embeddings", "Text Classification"],
  "Transformers": ["Token Embeddings", "Positional Encoding", "Q/K/V", "Attention", "Multi-Head Attention"],
  "Generative AI": ["Embeddings", "Similarity", "Chunking", "Retrieval"],
  "RAG": ["Document Chunking", "Retrieval", "Context Construction", "Evaluation"],
  "AI Agents": ["Tool Calling", "Agent Loops", "Planning", "Memory"],
  "MLOps": ["Model Serialization", "Inference", "Model Serving", "Monitoring"]
};

const DIFFICULTIES = ["All", "Easy", "Medium", "Hard"];
const STATUS_OPTIONS = ["All", "Solved", "Attempted", "Not Started", "Saved"];

export const Problems: React.FC = () => {
  const { user, token } = useAuth();
  const [challenges, setChallenges] = useState<Challenge[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Bookmarks List state
  const [bookmarkedSlugs, setBookmarkedSlugs] = useState<string[]>([]);
  const [bookmarkingSlugs, setBookmarkingSlugs] = useState<Record<string, boolean>>({});

  // Filter States
  const [search, setSearch] = useState("");
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [selectedSubcategory, setSelectedSubcategory] = useState("All");
  const [selectedDifficulty, setSelectedDifficulty] = useState("All");
  const [selectedStatus, setSelectedStatus] = useState("All");
  const [selectedTag, setSelectedTag] = useState<string | null>(null);

  // Expanded categories in sidebar
  const [expandedCategories, setExpandedCategories] = useState<Record<string, boolean>>({
    "Python for AI": true,
    "Mathematics": true,
    "Machine Learning": true,
    "Deep Learning": true
  });

  const toggleCategoryExpand = (cat: string) => {
    setExpandedCategories(prev => ({ ...prev, [cat]: !prev[cat] }));
  };

  const fetchBookmarks = async () => {
    if (!token) return;
    try {
      const res = await fetch(`${API_BASE_URL}/bookmarks`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        setBookmarkedSlugs(data);
      }
    } catch (err) {
      console.error("Failed to fetch bookmarks:", err);
    }
  };

  const fetchChallenges = async () => {
    setLoading(true);
    setError(null);
    try {
      const url = new URL(`${API_BASE_URL}/challenges`);
      if (search) url.searchParams.append("search", search);
      if (selectedCategory !== "All") url.searchParams.append("category", selectedCategory);
      if (selectedSubcategory !== "All") url.searchParams.append("subcategory", selectedSubcategory);
      if (selectedDifficulty !== "All") url.searchParams.append("difficulty", selectedDifficulty);
      if (selectedTag) url.searchParams.append("tag", selectedTag);

      const res = await fetch(url.toString());
      if (!res.ok) {
        throw new Error("Failed to load challenges from database.");
      }
      const data = await res.json();
      setChallenges(data);
    } catch (err: any) {
      setError(err.message || "An unexpected error occurred.");
    } finally {
      setLoading(false);
    }
  };

  const toggleBookmark = async (e: React.MouseEvent, slug: string) => {
    e.preventDefault();
    e.stopPropagation();
    if (!token) return;

    setBookmarkingSlugs(prev => ({ ...prev, [slug]: true }));
    try {
      const res = await fetch(`${API_BASE_URL}/challenges/${slug}/bookmark`, {
        method: "POST",
        headers: { Authorization: `Bearer ${token}` }
      });
      if (res.ok) {
        const data = await res.json();
        if (data.bookmarked) {
          setBookmarkedSlugs(prev => [...prev, slug]);
        } else {
          setBookmarkedSlugs(prev => prev.filter(s => s !== slug));
        }
      }
    } catch (err) {
      console.error("Failed to toggle bookmark:", err);
    } finally {
      setBookmarkingSlugs(prev => ({ ...prev, [slug]: false }));
    }
  };

  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      fetchChallenges();
    }, 250);

    return () => clearTimeout(delayDebounceFn);
  }, [search, selectedCategory, selectedSubcategory, selectedDifficulty, selectedTag]);

  useEffect(() => {
    if (token) {
      fetchBookmarks();
    }
  }, [token]);

  // Client-side completion status filterings
  const filteredChallenges = challenges.filter(c => {
    if (selectedStatus === "All") return true;
    
    const isSolved = user?.progress?.some(p => p.challenge_id === c.id && p.completed) || false;
    const isAttempted = user?.submissions?.some(s => s.challenge_id === c.id) || false;
    const isSaved = bookmarkedSlugs.includes(c.slug);

    if (selectedStatus === "Solved") return isSolved;
    if (selectedStatus === "Attempted") return isAttempted && !isSolved;
    if (selectedStatus === "Not Started") return !isAttempted && !isSolved;
    if (selectedStatus === "Saved") return isSaved;

    return true;
  });

  const getChallengeStatus = (challengeId: string) => {
    const isSolved = user?.progress?.some(p => p.challenge_id === challengeId && p.completed);
    if (isSolved) return "Solved";
    
    const isAttempted = user?.submissions?.some(s => s.challenge_id === challengeId);
    if (isAttempted) return "Attempted";
    
    return "Not Started";
  };

  // Calculate stats
  const totalCount = challenges.length;
  const solvedCount = challenges.filter(c => getChallengeStatus(c.id) === "Solved").length;
  const solvedPercentage = totalCount > 0 ? Math.round((solvedCount / totalCount) * 100) : 0;

  const easyTotal = challenges.filter(c => c.difficulty === "Easy").length;
  const easySolved = challenges.filter(c => c.difficulty === "Easy" && getChallengeStatus(c.id) === "Solved").length;

  const mediumTotal = challenges.filter(c => c.difficulty === "Medium").length;
  const mediumSolved = challenges.filter(c => c.difficulty === "Medium" && getChallengeStatus(c.id) === "Solved").length;

  const hardTotal = challenges.filter(c => c.difficulty === "Hard").length;
  const hardSolved = challenges.filter(c => c.difficulty === "Hard" && getChallengeStatus(c.id) === "Solved").length;

  const currentCategoryTotal = challenges.filter(c => selectedCategory === "All" || c.category === selectedCategory).length;
  const currentCategorySolved = challenges.filter(c => (selectedCategory === "All" || c.category === selectedCategory) && getChallengeStatus(c.id) === "Solved").length;
  const categoryPercentage = currentCategoryTotal > 0 ? Math.round((currentCategorySolved / currentCategoryTotal) * 100) : 0;

  return (
    <div className="space-y-6 max-w-7xl mx-auto px-4 select-text">
      
      {/* Dashboard Summary Header */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        
        {/* Title Block */}
        <div className="lg:col-span-2 flex flex-col justify-center">
          <h1 className="text-2xl font-bold text-white tracking-tight font-mono">AI/ML Challenges</h1>
          <p className="text-sm text-dark-muted mt-1 leading-relaxed">
            Build machine learning kernels from scratch. Math equations &rarr; NumPy tensors &rarr; sandbox evaluations &rarr; progress tracking.
          </p>
          <div className="flex items-center gap-3 text-[10px] mt-4 font-mono text-dark-muted">
            <span className="flex items-center gap-1"><CheckCircle2 className="w-3.5 h-3.5 text-brand" /> Solved</span>
            <span className="flex items-center gap-1"><Circle className="w-3.5 h-3.5 text-accent-orange fill-accent-orange/10" /> Attempted</span>
            <span className="flex items-center gap-1"><Circle className="w-3.5 h-3.5 text-slate-600" /> Not Started</span>
          </div>
        </div>

        {/* Global Progress Bar */}
        <div className="bg-dark-card border border-dark-border p-4 rounded-lg flex flex-col justify-between">
          <div className="flex justify-between items-center mb-1">
            <span className="text-[10px] font-bold text-slate-400 uppercase font-mono">Overall Progress</span>
            <span className="text-sm font-bold text-brand font-mono">{solvedPercentage}%</span>
          </div>
          <div className="w-full bg-dark-deep rounded-full h-2.5 mb-2 overflow-hidden border border-dark-border">
            <div className="bg-brand h-full rounded-full transition-all duration-500" style={{ width: `${solvedPercentage}%` }} />
          </div>
          <span className="text-[11px] text-slate-500 font-mono">
            {solvedCount} / {totalCount} completed
          </span>
        </div>

        {/* Difficulty Counts Split */}
        <div className="bg-dark-card border border-dark-border p-4 rounded-lg space-y-2 text-xs font-mono">
          <div className="flex justify-between items-center text-[10px] font-bold text-slate-400 uppercase tracking-wider border-b border-dark-border pb-1 mb-2">
            <span>Difficulty</span>
            <span>Ratio</span>
          </div>
          <div className="flex justify-between text-green-400">
            <span>Easy</span>
            <span>{easySolved} / {easyTotal}</span>
          </div>
          <div className="flex justify-between text-yellow-400">
            <span>Medium</span>
            <span>{mediumSolved} / {mediumTotal}</span>
          </div>
          <div className="flex justify-between text-red-400">
            <span>Hard</span>
            <span>{hardSolved} / {hardTotal}</span>
          </div>
        </div>

      </div>

      {/* Main Layout containing Curriculum Sidebar and Table */}
      <div className="flex flex-col lg:flex-row gap-6 items-start">
        
        {/* Left Column Sidebar: Curriculum Tree */}
        <div className="w-full lg:w-64 shrink-0 bg-dark-card border border-dark-border rounded-lg p-4 space-y-4">
          <div className="flex justify-between items-center border-b border-dark-border pb-2.5">
            <span className="text-xs font-bold text-white uppercase tracking-wider font-mono">Curriculum Tree</span>
            {selectedCategory !== "All" && (
              <button 
                onClick={() => {
                  setSelectedCategory("All");
                  setSelectedSubcategory("All");
                }}
                className="text-[10px] text-brand hover:underline font-mono"
              >
                Clear
              </button>
            )}
          </div>
          
          <div className="space-y-2 max-h-[70vh] overflow-y-auto pr-1">
            {Object.entries(CURRICULUM_TREE).map(([catName, subcats]) => {
              const isExpanded = expandedCategories[catName];
              const isSelected = selectedCategory === catName;
              
              return (
                <div key={catName} className="space-y-1">
                  <div 
                    onClick={() => {
                      setSelectedCategory(catName);
                      setSelectedSubcategory("All");
                      toggleCategoryExpand(catName);
                    }}
                    className={`flex items-center justify-between px-2.5 py-1.5 rounded cursor-pointer transition-colors text-xs font-medium ${
                      isSelected && selectedSubcategory === "All"
                        ? "bg-brand/10 text-brand font-bold"
                        : "text-slate-300 hover:bg-dark-hover"
                    }`}
                  >
                    <span className="truncate">{catName}</span>
                    {isExpanded ? <ChevronDown className="w-3.5 h-3.5 shrink-0" /> : <ChevronRight className="w-3.5 h-3.5 shrink-0" />}
                  </div>
                  
                  {isExpanded && (
                    <div className="pl-3.5 space-y-0.5 border-l border-dark-border/40 ml-2">
                      {subcats.map(sub => (
                        <div
                          key={sub}
                          onClick={(e) => {
                            e.stopPropagation();
                            setSelectedCategory(catName);
                            setSelectedSubcategory(sub);
                          }}
                          className={`px-2.5 py-1 rounded cursor-pointer transition-colors text-[11px] font-mono ${
                            selectedCategory === catName && selectedSubcategory === sub
                              ? "text-brand font-bold bg-dark-deep"
                              : "text-slate-500 hover:text-slate-300"
                          }`}
                        >
                          {sub}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Right Column: Filters Toolbar & Problems List */}
        <div className="flex-1 w-full space-y-4">
          
          {/* Active Category Header Progress Card */}
          {selectedCategory !== "All" && (
            <div className="p-4 bg-dark-card border border-dark-border rounded-lg flex flex-col md:flex-row justify-between md:items-center gap-4">
              <div>
                <h2 className="text-sm font-bold text-white font-mono">{selectedCategory}</h2>
                <p className="text-xs text-slate-400 mt-0.5">{selectedSubcategory !== "All" ? `Focus Topic: ${selectedSubcategory}` : "All subcategories"}</p>
              </div>
              <div className="flex items-center gap-3 shrink-0">
                <span className="text-[10px] text-slate-500 font-mono">{currentCategorySolved} / {currentCategoryTotal} Completed</span>
                <div className="w-24 bg-dark-deep h-2 rounded-full overflow-hidden border border-dark-border">
                  <div className="bg-brand h-full rounded-full" style={{ width: `${categoryPercentage}%` }} />
                </div>
                <span className="text-xs font-bold font-mono text-brand">{categoryPercentage}%</span>
              </div>
            </div>
          )}

          {/* Advanced Search & Filtering Toolbar */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 p-4 bg-dark-card border border-dark-border rounded-lg shadow-lg">
            
            {/* Search input */}
            <div className="relative md:col-span-1">
              <Search className="absolute left-3 top-3 w-4 h-4 text-dark-muted" />
              <input
                type="text"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search kernels, gradients, tokens..."
                className="w-full pl-9 pr-4 py-2 bg-dark-deep border border-dark-border focus:border-brand/40 rounded-md text-slate-200 placeholder-slate-600 focus:outline-none focus:ring-1 focus:ring-brand/20 transition-all text-xs font-mono"
              />
            </div>

            {/* Filter selectors */}
            <div className="grid grid-cols-3 gap-3 md:col-span-3">
              {/* Difficulty */}
              <div className="flex items-center gap-2">
                <span className="text-[9px] text-slate-400 font-bold uppercase tracking-wider block shrink-0 font-mono">Difficulty:</span>
                <select
                  value={selectedDifficulty}
                  onChange={(e) => setSelectedDifficulty(e.target.value)}
                  className="w-full bg-dark-deep border border-dark-border text-slate-300 rounded px-2 py-1.5 text-xs focus:outline-none focus:border-brand/40 transition-colors font-mono"
                >
                  {DIFFICULTIES.map((diff) => (
                    <option key={diff} value={diff}>{diff}</option>
                  ))}
                </select>
              </div>

              {/* Status */}
              <div className="flex items-center gap-2">
                <span className="text-[9px] text-slate-400 font-bold uppercase tracking-wider block shrink-0 font-mono">Status:</span>
                <select
                  value={selectedStatus}
                  onChange={(e) => setSelectedStatus(e.target.value)}
                  className="w-full bg-dark-deep border border-dark-border text-slate-300 rounded px-2 py-1.5 text-xs focus:outline-none focus:border-brand/40 transition-colors font-mono"
                >
                  {STATUS_OPTIONS.map((opt) => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              </div>

              {/* Reset active tag filter shortcut */}
              <div className="flex items-center justify-end">
                {(selectedTag || search || selectedDifficulty !== "All" || selectedStatus !== "All") && (
                  <button
                    onClick={() => {
                      setSearch("");
                      setSelectedDifficulty("All");
                      setSelectedStatus("All");
                      setSelectedTag(null);
                    }}
                    className="text-[10px] text-brand hover:underline font-mono"
                  >
                    Reset Filters
                  </button>
                )}
              </div>
            </div>
          </div>

          {/* Active Tag filter indicator */}
          {selectedTag && (
            <div className="flex items-center gap-2 text-xs">
              <span className="text-slate-500 font-mono">Filtering by tag:</span>
              <span className="inline-flex items-center gap-1 text-[10px] text-brand bg-brand/10 border border-brand/20 px-2 py-0.5 rounded font-mono">
                <Tag className="w-3 h-3" />
                {selectedTag}
                <button onClick={() => setSelectedTag(null)} className="hover:text-red-400 ml-1 font-bold font-sans">&times;</button>
              </span>
            </div>
          )}

          {/* Table list container */}
          {loading ? (
            <div className="flex flex-col items-center justify-center py-20 space-y-4">
              <Loader2 className="w-8 h-8 text-brand animate-spin" />
              <p className="text-sm text-slate-400 font-mono">Querying challenge registry...</p>
            </div>
          ) : error ? (
            <div className="flex flex-col items-center justify-center p-12 bg-dark-card border border-red-500/20 text-center rounded-lg space-y-4">
              <AlertCircle className="w-10 h-10 text-red-400" />
              <h3 className="text-base font-bold text-white font-mono">Registry connection failed</h3>
              <p className="text-xs text-slate-400 max-w-sm font-mono">{error}</p>
              <button
                onClick={fetchChallenges}
                className="flex items-center gap-2 bg-brand/10 hover:bg-brand/20 border border-brand/30 text-brand text-xs font-semibold px-4 py-2 rounded-md transition-all font-mono"
              >
                <RefreshCw className="w-3.5 h-3.5" />
                Retry Registry
              </button>
            </div>
          ) : filteredChallenges.length === 0 ? (
            <div className="flex flex-col items-center justify-center p-16 bg-dark-card border border-dark-border text-center rounded-lg space-y-3">
              <BookOpen className="w-8 h-8 text-dark-muted" />
              <h3 className="text-base font-bold text-white font-mono">No matches found</h3>
              <p className="text-xs text-slate-400 max-w-xs leading-normal">
                No active challenges correspond to these search terms or tag filters.
              </p>
            </div>
          ) : (
            <div className="bg-dark-card border border-dark-border rounded-lg overflow-hidden shadow-xl">
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="border-b border-dark-border bg-dark-deep/40 text-[10px] font-bold text-slate-400 uppercase tracking-wider font-mono">
                      <th className="py-4 px-6 text-center w-12">Status</th>
                      <th className="py-4 px-6">Challenge</th>
                      <th className="py-4 px-6">Subcategory</th>
                      <th className="py-4 px-6">Difficulty</th>
                      <th className="py-4 px-6 text-center w-16">Save</th>
                      <th className="py-4 px-6 text-right">Action</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-dark-border text-sm text-slate-300">
                    {filteredChallenges.map((prob, idx) => {
                      const statusVal = getChallengeStatus(prob.id);
                      const isSaved = bookmarkedSlugs.includes(prob.slug);
                      const isSaving = bookmarkingSlugs[prob.slug];
                      const tagsList = prob.tags ? prob.tags.split(",").map(t => t.trim()) : [prob.category.toLowerCase()];

                      return (
                        <tr key={prob.id} className="hover:bg-dark-deep/30 transition-colors group">
                          
                          {/* Completion Dot */}
                          <td className="py-4 px-6 text-center">
                            {statusVal === "Solved" ? (
                              <CheckCircle2 className="w-4 h-4 text-brand mx-auto animate-pulse" />
                            ) : statusVal === "Attempted" ? (
                              <Circle className="w-4 h-4 text-accent-orange fill-accent-orange/15 mx-auto" />
                            ) : (
                              <Circle className="w-4 h-4 text-slate-700 mx-auto" />
                            )}
                          </td>

                          {/* Title & Tags */}
                          <td className="py-4 px-6">
                            <div className="space-y-1">
                              <Link to={`/problems/${prob.slug}`} className="font-semibold text-white hover:text-brand transition-colors text-sm font-mono block">
                                #{String(idx + 1).padStart(3, "0")} — {prob.title}
                              </Link>
                              <div className="flex flex-wrap gap-1.5 pt-0.5">
                                {tagsList.map((tag) => (
                                  <button
                                    key={tag}
                                    onClick={() => setSelectedTag(tag)}
                                    className="inline-flex items-center gap-0.5 text-[9px] text-slate-500 bg-dark-deep hover:bg-dark-hover hover:text-brand border border-dark-border px-1.5 py-0.5 rounded font-mono transition-colors"
                                  >
                                    <Tag className="w-2.5 h-2.5" />
                                    {tag}
                                  </button>
                                ))}
                              </div>
                            </div>
                          </td>

                          {/* Subcategory */}
                          <td className="py-4 px-6">
                            <span className="text-xs text-slate-400 font-mono font-medium">
                              {prob.subcategory || prob.category}
                            </span>
                          </td>

                          {/* Difficulty */}
                          <td className="py-3 px-5">
                            <span className={`inline-block text-[9px] px-2 py-0.5 rounded border uppercase tracking-wider font-mono font-bold ${
                              prob.difficulty === "Easy"
                                ? "bg-dark-panel text-brand-green border-brand-green/20"
                                : prob.difficulty === "Medium"
                                ? "bg-dark-panel text-brand-yellow border-brand-yellow/20"
                                : "bg-dark-panel text-brand-pink border-brand-pink/20"
                            }`}>
                              {prob.difficulty}
                            </span>
                          </td>

                          {/* Bookmark */}
                          <td className="py-3 px-5 text-center">
                            <button
                              onClick={(e) => toggleBookmark(e, prob.slug)}
                              disabled={!token || isSaving}
                              className={`p-1.5 rounded hover:bg-dark-hover transition-colors ${
                                isSaved ? "text-brand-yellow" : "text-slate-600 hover:text-slate-400"
                              }`}
                            >
                              {isSaving ? (
                                <Loader2 className="w-3.5 h-3.5 animate-spin text-slate-400" />
                              ) : (
                                <Star className={`w-3.5 h-3.5 ${isSaved ? "fill-brand-yellow" : ""}`} />
                              )}
                            </button>
                          </td>

                          {/* Action Solve link */}
                          <td className="py-3 px-5 text-right">
                            <Link
                              to={`/problems/${prob.slug}`}
                              className="inline-flex items-center justify-center bg-dark-panel hover:bg-brand text-[#C8D0CA] hover:text-dark-deep border border-dark-border hover:border-brand px-3 py-1 rounded text-[11px] font-bold font-mono transition-all"
                            >
                              Solve
                            </Link>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
