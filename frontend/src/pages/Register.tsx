import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth, API_BASE_URL } from "../context/AuthContext";
import { BRAND_CONFIG } from "../config/brand";
import { KeyRound, Mail, AlertTriangle, Loader2 } from "lucide-react";

export const Register: React.FC = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !password || !confirmPassword) return;

    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setError(null);
    setSubmitting(true);

    try {
      // 1. Register User
      const regResponse = await fetch(`${API_BASE_URL}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const regData = await regResponse.json();

      if (!regResponse.ok) {
        setError(regData.detail || "Registration failed. Try a different email.");
        setSubmitting(false);
        return;
      }

      // 2. Automatically Login
      const loginResponse = await fetch(`${API_BASE_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const loginData = await loginResponse.json();

      if (loginResponse.ok) {
        await login(loginData.access_token);
        navigate("/dashboard");
      } else {
        setError("Account created, but automatic login failed. Proceed to Login page.");
      }
    } catch (err) {
      setError("Network error. Make sure the backend server is running.");
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-[70svh]">
      <div className="w-full max-w-sm p-6 bg-dark-card border border-dark-border rounded shadow-2xl">
        <div className="text-center mb-6">
          <div className="inline-flex items-center justify-center w-10 h-10 rounded bg-brand/5 border border-brand/20 text-brand text-xl font-mono mb-3">
            {BRAND_CONFIG.logo.symbol}
          </div>
          <h2 className="text-lg font-bold font-mono text-white tracking-tight uppercase">NeuraCode</h2>
          <p className="text-[10px] font-mono tracking-widest text-[#8B958E] uppercase mt-1">AI/ML Coding Laboratory</p>
        </div>

        {error && (
          <div className="flex items-start gap-2.5 p-3 mb-5 bg-brand-red/10 border border-brand-red/20 text-brand-red rounded text-xs">
            <AlertTriangle className="w-4 h-4 shrink-0 text-brand-red" />
            <span>{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-1.5">
            <label className="text-[10px] font-mono font-bold text-[#8B958E] uppercase tracking-wider block">
              Email Address
            </label>
            <div className="relative">
              <Mail className="absolute left-3 top-2.5 w-4 h-4 text-dark-textMuted" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="developer@neuracode.com"
                className="w-full pl-9 pr-3 py-2 bg-[#080C0A] border border-[#28302A] focus:border-brand rounded text-slate-200 placeholder-[#59635D] focus:outline-none focus:ring-1 focus:ring-brand/20 transition-all text-xs font-mono"
              />
            </div>
          </div>

          <div className="space-y-1.5">
            <label className="text-[10px] font-mono font-bold text-[#8B958E] uppercase tracking-wider block">
              Password
            </label>
            <div className="relative">
              <KeyRound className="absolute left-3 top-2.5 w-4 h-4 text-dark-textMuted" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-9 pr-3 py-2 bg-[#080C0A] border border-[#28302A] focus:border-brand rounded text-slate-200 placeholder-[#59635D] focus:outline-none focus:ring-1 focus:ring-brand/20 transition-all text-xs font-mono"
              />
            </div>
          </div>

          <div className="space-y-1.5">
            <label className="text-[10px] font-mono font-bold text-[#8B958E] uppercase tracking-wider block">
              Confirm Password
            </label>
            <div className="relative">
              <KeyRound className="absolute left-3 top-2.5 w-4 h-4 text-dark-textMuted" />
              <input
                type="password"
                required
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-9 pr-3 py-2 bg-[#080C0A] border border-[#28302A] focus:border-brand rounded text-slate-200 placeholder-[#59635D] focus:outline-none focus:ring-1 focus:ring-brand/20 transition-all text-xs font-mono"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={submitting}
            className="w-full flex items-center justify-center gap-2 bg-brand hover:bg-brand-dark disabled:opacity-50 text-dark-deep font-bold py-2 rounded transition-all text-xs font-mono"
          >
            {submitting ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                Registering...
              </>
            ) : (
              "Sign Up"
            )}
          </button>
        </form>

        <p className="text-xs text-center text-[#8B958E] mt-5 font-mono">
          Already registered?{" "}
          <Link to="/login" className="text-brand hover:underline font-semibold transition-colors">
            Sign In
          </Link>
        </p>
      </div>
    </div>
  );
};
