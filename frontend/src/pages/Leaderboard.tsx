import React from "react";
import { Trophy, Medal, Search, Flame, ArrowUp } from "lucide-react";

export const Leaderboard: React.FC = () => {
  const leaderBoardUsers = [
    { rank: 1, name: "grad_descent_master", xp: 12450, streak: 42, solved: 18 },
    { rank: 2, name: "backprop_pioneer", xp: 10890, streak: 31, solved: 15 },
    { rank: 3, name: "transformer_attention", xp: 9540, streak: 19, solved: 13 },
    { rank: 4, name: "optimizer_adam", xp: 8200, streak: 12, solved: 11 },
    { rank: 5, name: "sgd_coder", xp: 7600, streak: 27, solved: 10 }
  ];

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-2">
          <Trophy className="w-6 h-6 text-brand" />
          Global Leaderboard
        </h1>
        <p className="text-sm text-dark-muted mt-1">
          Compete with other engineers on implementing AI/ML algorithms and scoring XP.
        </p>
      </div>

      <div className="bg-dark-card border border-dark-border rounded overflow-hidden shadow-xl select-none">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-dark-border bg-[#070B0A]/40 text-[10px] font-bold text-[#8B958E] uppercase tracking-wider font-mono">
                <th className="py-3 px-5 text-center w-16">Rank</th>
                <th className="py-3 px-5">User</th>
                <th className="py-3 px-5 text-right">Kernels Solved</th>
                <th className="py-3 px-5 text-right">Streak</th>
                <th className="py-3 px-5 text-right">Experience</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-dark-border text-xs text-[#E8EEE9]">
              {leaderBoardUsers.map((item) => (
                <tr key={item.rank} className="hover:bg-dark-deep/30 transition-colors">
                  <td className="py-3 px-5 text-center font-bold font-mono">
                    {item.rank <= 3 ? (
                      <span className="inline-flex items-center justify-center w-5 h-5 rounded bg-brand/5 border border-brand/20 text-brand">
                        {item.rank}
                      </span>
                    ) : (
                      item.rank
                    )}
                  </td>
                  <td className="py-3 px-5 font-semibold text-white font-mono">
                    @{item.name}
                  </td>
                  <td className="py-3 px-5 text-right font-mono font-semibold">
                    {item.solved}
                  </td>
                  <td className="py-3 px-5 text-right">
                    <span className="inline-flex items-center gap-1 text-brand-yellow font-semibold font-mono">
                      <Flame className="w-3.5 h-3.5 fill-brand-yellow/10" />
                      {item.streak}d
                    </span>
                  </td>
                  <td className="py-3 px-5 text-right font-mono font-bold text-brand">
                    {item.xp} XP
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
