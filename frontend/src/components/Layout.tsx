import React from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { BRAND_CONFIG } from "../config/brand";
import { 
  LayoutDashboard, 
  Code2, 
  BookOpen, 
  Trophy, 
  User as UserIcon, 
  LogOut, 
  Zap, 
  ChevronRight,
  ChevronDown,
  Menu,
  X,
  History,
  Star,
  Settings as SettingsIcon,
  Bell,
  HelpCircle,
  Sun
} from "lucide-react";

export const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = React.useState(false);

  const sidebarItems = [
    { label: "Home", path: "/dashboard", icon: LayoutDashboard },
    { label: "Problems", path: "/problems", icon: Code2 },
    { label: "Submissions", path: "/leaderboard", icon: History },
    { label: "Bookmarks", path: "/problems", icon: Star },
    { label: "Progress", path: "/dashboard", icon: Zap },
    { label: "Profile", path: "/profile", icon: UserIcon },
    { label: "Settings", path: "/profile", icon: SettingsIcon },
  ];

  const handleLogout = async () => {
    await logout();
    navigate("/login");
  };

  const getActiveHeaderTab = () => {
    if (location.pathname.startsWith("/learn")) return "learn";
    if (location.pathname.startsWith("/leaderboard")) return "leaderboard";
    if (location.pathname.startsWith("/profile")) return "profile";
    return "challenges"; // default
  };
  const activeHeaderTab = getActiveHeaderTab();

  const userInitial = user?.profile?.display_name?.[0]?.toUpperCase() || user?.email?.[0]?.toUpperCase() || "U";

  return (
    <div className="flex flex-col min-h-screen bg-[#050807] text-[#E8EEE9] font-sans">
      {/* Top Header */}
      <header className="sticky top-0 z-40 flex items-center justify-between px-6 h-[60px] border-b border-[#1C2922] bg-[#0B120F] shrink-0">
        {/* Left branding */}
        <div className="flex items-center gap-3">
          <Link to="/" className="flex items-center gap-2 text-sm font-bold tracking-tight text-white hover:opacity-90">
            <span className="flex items-center justify-center w-6 h-6 rounded bg-[#12DFFF]/5 border border-[#12DFFF]/20 text-[#12DFFF] font-mono">
              {BRAND_CONFIG.logo.symbol}
            </span>
            <span className="font-mono text-sm tracking-wider uppercase font-bold text-white">{BRAND_CONFIG.name}</span>
          </Link>
        </div>

        {/* Center Navbar Navigation */}
        <nav className="hidden md:flex items-center gap-6 text-[11px] font-mono uppercase tracking-widest text-[#AAB4AC] select-none">
          <Link to="/learn" className={`hover:text-white transition-all pb-1.5 pt-0.5 px-0.5 ${activeHeaderTab === "learn" ? "text-white border-b-2 border-[#12DFFF]" : ""}`}>Learn</Link>
          <Link to="/problems" className={`hover:text-white transition-all pb-1.5 pt-0.5 px-0.5 ${activeHeaderTab === "challenges" ? "text-white border-b-2 border-[#12DFFF]" : ""}`}>Challenges</Link>
          <Link to="/problems" className="hover:text-white transition-all pb-1.5 pt-0.5 px-0.5">Paths</Link>
          <Link to="/leaderboard" className={`hover:text-white transition-all pb-1.5 pt-0.5 px-0.5 ${activeHeaderTab === "leaderboard" ? "text-white border-b-2 border-[#12DFFF]" : ""}`}>Leaderboard</Link>
          <a href="#" className="hover:text-white transition-all pb-1.5 pt-0.5 px-0.5">Blog</a>
        </nav>

        {/* Right Nav Actions */}
        <div className="hidden md:flex items-center gap-5 select-none">
          {user && (
            <div className="flex items-center gap-1.5 text-xs text-[#FFD84D] font-mono">
              <span>🔥</span>
              <span>{user?.streak?.current_streak ?? 0} day streak</span>
            </div>
          )}

          <button className="text-[#8B958E] hover:text-white transition-colors p-1" title="Notifications">
            <Bell className="w-4 h-4" />
          </button>

          {user ? (
            <div className="flex items-center gap-3">
              <Link to="/profile" className="flex items-center gap-2 group">
                <div className="w-7 h-7 rounded-full bg-[#FF4FA3] text-white font-bold flex items-center justify-center text-xs border border-white/10 shadow-sm font-mono">
                  {userInitial}
                </div>
                <div className="text-left hidden lg:block">
                  <p className="text-xs text-slate-200 font-semibold leading-none group-hover:text-white transition-colors">{user.profile?.display_name}</p>
                </div>
                <ChevronDown className="w-3.5 h-3.5 text-slate-400 group-hover:text-white transition-colors" />
              </Link>
              <button 
                onClick={handleLogout}
                className="p-1.5 text-[#8B958E] hover:text-brand-red hover:bg-brand-red/10 rounded transition-all"
                title="Logout"
              >
                <LogOut className="w-3.5 h-3.5" />
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-3">
              <Link to="/login" className="text-xs font-semibold text-[#8B958E] hover:text-white transition-colors font-mono uppercase">
                Log in
              </Link>
              <Link to="/register" className="text-xs font-semibold bg-[#00E58A] hover:bg-[#00E58A]/90 text-[#050807] px-3.5 py-1.5 rounded transition-all font-mono font-bold">
                Register
              </Link>
            </div>
          )}
        </div>

        {/* Mobile Menu Button */}
        <button 
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="p-2 md:hidden text-slate-400 hover:text-white hover:bg-dark-hover rounded transition-colors"
        >
          {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
        </button>
      </header>

      {/* Main Container */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left Sidebar - Desktop */}
        <aside className="hidden md:flex flex-col w-16 border-r border-[#1C2922] bg-[#080F0C] py-4 select-none shrink-0 justify-between">
          <div className="flex flex-col space-y-1">
            {sidebarItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname.startsWith(item.path) || (item.path === "/dashboard" && (location.pathname === "/" || location.pathname === "/dashboard"));
              return (
                <Link
                  key={item.label}
                  to={item.path}
                  className={`flex flex-col items-center justify-center py-2.5 text-[9px] font-mono tracking-wider transition-all border-l-2 select-none gap-1 ${
                    isActive 
                      ? "bg-[#12DFFF]/5 text-[#12DFFF] border-[#12DFFF] font-bold" 
                      : "text-[#8B958E] hover:text-white hover:bg-dark-hover/10 border-transparent"
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span className="scale-[0.95]">{item.label}</span>
                </Link>
              );
            })}
          </div>

          <div className="flex flex-col items-center space-y-3 pt-4 border-t border-[#1C2922]/50">
            <Link to="/profile" className="flex flex-col items-center gap-0.5 text-[9px] font-mono text-[#8B958E] hover:text-white">
              <HelpCircle className="w-4 h-4" />
              <span>Help</span>
            </Link>
            <button className="p-1.5 text-[#FFD84D] hover:text-white transition-colors" title="Toggle theme mode">
              <Sun className="w-4 h-4 fill-[#FFD84D]/15" />
            </button>
          </div>
        </aside>

        {/* Mobile Nav Overlay */}
        {mobileMenuOpen && (
          <div className="fixed inset-0 top-[60px] z-30 flex flex-col bg-[#080D0B]/95 backdrop-blur-md p-6 space-y-4 md:hidden">
            {sidebarItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname.startsWith(item.path) || (item.path === "/dashboard" && location.pathname === "/");
              return (
                <Link
                  key={item.label}
                  to={item.path}
                  onClick={() => setMobileMenuOpen(false)}
                  className={`flex items-center gap-3 px-4 py-3 rounded text-sm font-semibold ${
                    isActive 
                      ? "bg-[#12DFFF]/15 text-[#12DFFF]" 
                      : "text-slate-300 hover:text-white hover:bg-dark-hover"
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span>{item.label}</span>
                </Link>
              );
            })}

            <div className="border-t border-[#1C2922] pt-6 flex flex-col gap-4 mt-auto">
              {user ? (
                <button
                  onClick={() => {
                    setMobileMenuOpen(false);
                    handleLogout();
                  }}
                  className="w-full flex items-center justify-center gap-2 bg-red-500/10 hover:bg-red-500/25 border border-red-500/20 text-red-400 py-3 rounded font-semibold transition-all"
                >
                  <LogOut className="w-5 h-5" />
                  Log Out
                </button>
              ) : (
                <div className="grid grid-cols-2 gap-3">
                  <Link 
                    to="/login" 
                    onClick={() => setMobileMenuOpen(false)}
                    className="flex justify-center items-center text-center font-semibold text-slate-300 border border-dark-border hover:text-white py-3 rounded"
                  >
                    Log In
                  </Link>
                  <Link 
                    to="/register" 
                    onClick={() => setMobileMenuOpen(false)}
                    className="flex justify-center items-center text-center font-semibold bg-[#00E58A] text-[#050807] py-3 rounded"
                  >
                    Register
                  </Link>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Content Area */}
        <main className={`flex-1 bg-[#050807] ${
          location.pathname.includes("/problems/") && location.pathname.split("/").filter(Boolean).length >= 2
            ? "overflow-hidden p-0"
            : "overflow-y-auto p-4 md:p-6"
        }`}>
          {children}
        </main>
      </div>
    </div>
  );
};
