import React from "react";
import { useAuth } from "../context/AuthContext";
import { User, Mail, Shield, Calendar, Award } from "lucide-react";

export const Profile: React.FC = () => {
  const { user } = useAuth();

  if (!user) {
    return (
      <div className="text-center py-20 text-slate-400">
        Please log in to view your profile settings.
      </div>
    );
  }

  const joinDate = user.created_at 
    ? new Date(user.created_at).toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' })
    : "Recently";

  return (
    <div className="max-w-3xl mx-auto space-y-6 select-none">
      {/* Profile summary banner */}
      <div className="p-5 bg-dark-card border border-dark-border rounded flex flex-col md:flex-row items-center gap-6 shadow-xl">
        <img
          src={user.profile?.avatar_url || `https://api.dicebear.com/7.x/bottts/svg?seed=${user.email}`}
          alt="avatar"
          className="w-20 h-20 rounded bg-dark-deep border border-brand/20 shadow-md p-1 shrink-0"
        />
        <div className="space-y-1.5 text-center md:text-left">
          <h2 className="text-lg font-bold text-white tracking-tight font-mono">
            @{user.profile?.display_name || user.email.split("@")[0]}
          </h2>
          <p className="text-xs text-[#8B958E] font-medium font-sans">
            {user.profile?.bio || "No profile bio written yet."}
          </p>
          <div className="flex flex-wrap justify-center md:justify-start gap-4 pt-1.5 text-xs text-dark-muted font-mono">
            <span className="flex items-center gap-1.5">
              <Mail className="w-3.5 h-3.5 text-brand" /> {user.email}
            </span>
            <span className="flex items-center gap-1.5">
              <Calendar className="w-3.5 h-3.5 text-brand-yellow" /> Joined {joinDate}
            </span>
          </div>
        </div>
      </div>

      {/* Stats and Achievements */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        {/* Statistics block */}
        <div className="p-5 bg-dark-card border border-dark-border rounded space-y-4">
          <h3 className="text-sm font-bold text-white flex items-center gap-2 font-mono uppercase tracking-wider">
            <Shield className="w-4 h-4 text-brand" />
            Account Stats
          </h3>
          <div className="grid grid-cols-2 gap-4">
            <div className="p-3 bg-dark-deep border border-[#28302A] rounded">
              <span className="text-[9px] text-[#8B958E] font-bold uppercase tracking-wider block font-mono">XP Level</span>
              <span className="text-base font-bold text-white font-mono mt-0.5 block">{user.profile?.xp} XP</span>
            </div>
            <div className="p-3 bg-dark-deep border border-[#28302A] rounded">
              <span className="text-[9px] text-[#8B958E] font-bold uppercase tracking-wider block font-mono">Best Streak</span>
              <span className="text-base font-bold text-white font-mono mt-0.5 block">{user.streak?.longest_streak ?? 0} days</span>
            </div>
            <div className="p-3 bg-dark-deep border border-[#28302A] rounded col-span-2">
              <span className="text-[9px] text-[#8B958E] font-bold uppercase tracking-wider block font-mono">Role privileges</span>
              <span className="text-xs font-semibold text-slate-200 mt-0.5 block font-mono">
                {user.is_superuser ? "Super Admin Developer" : "Standard Developer"}
              </span>
            </div>
          </div>
        </div>

        {/* Badges showcase */}
        <div className="p-5 bg-dark-card border border-dark-border rounded space-y-4">
          <h3 className="text-sm font-bold text-white flex items-center gap-2 font-mono uppercase tracking-wider">
            <Award className="w-4 h-4 text-brand-pink" />
            Badges Showcase
          </h3>
          <div className="flex flex-col items-center justify-center py-6 text-center text-slate-500 border border-dashed border-[#28302A] rounded p-4 bg-dark-deep/50">
            <Award className="w-8 h-8 text-dark-textMuted mb-1.5" />
            <p className="text-xs font-mono">No badges unlocked yet.</p>
            <p className="text-[10px] text-dark-textMuted mt-1 leading-relaxed font-mono">
              Earn badges by completing challenges on your learning path and retaining streaks!
            </p>
          </div>
        </div>

      </div>
    </div>
  );
};
