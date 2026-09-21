import React from 'react';
import { Link } from 'react-router-dom';
import {
  ArrowLeftRight, BookOpen, Award, CheckCircle2, Sparkles,
  Users, ShieldCheck, ArrowRight, BookMarked, BrainCircuit, GraduationCap
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const Home: React.FC = () => {
  const { isAuthenticated } = useAuth();

  return (
    <div className="bg-slate-50 min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-blue-900 via-indigo-950 to-slate-900 text-white pt-20 pb-28">
        <div className="absolute inset-0 opacity-10 bg-[radial-gradient(#fff_1px,transparent_1px)] [background-size:16px_16px]"></div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-blue-500/20 border border-blue-400/30 text-blue-300 text-xs font-semibold uppercase tracking-wider mb-6 animate-fade-in">
            <Sparkles className="w-3.5 h-3.5 text-blue-400" />
            Next-Gen Higher Education Ecosystem
          </div>

          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight max-w-4xl mx-auto leading-tight">
            Learn from <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-teal-300">Peers</span> when possible. <br />
            Learn from <span className="text-transparent bg-clip-text bg-gradient-to-r from-amber-300 to-orange-400">Courses</span> when unavailable.
          </h1>

          <p className="mt-6 text-lg sm:text-xl text-slate-300 max-w-2xl mx-auto font-normal leading-relaxed">
            SkillSwap Campus connects students across 15+ disciplines to trade skills, complete structured modules, pass mock assessments, and earn verifiable certificates.
          </p>

          <div className="mt-10 flex flex-col sm:flex-row items-center justify-center gap-4">
            {isAuthenticated ? (
              <Link
                to="/dashboard"
                className="w-full sm:w-auto inline-flex items-center justify-center px-8 py-3.5 text-base font-bold text-slate-900 bg-gradient-to-r from-teal-300 to-blue-400 hover:from-teal-200 hover:to-blue-300 rounded-xl shadow-lg shadow-blue-500/25 transition-all"
              >
                Go to Dashboard
                <ArrowRight className="w-5 h-5 ml-2" />
              </Link>
            ) : (
              <>
                <Link
                  to="/register"
                  className="w-full sm:w-auto inline-flex items-center justify-center px-8 py-3.5 text-base font-bold text-slate-900 bg-gradient-to-r from-teal-300 to-blue-400 hover:from-teal-200 hover:to-blue-300 rounded-xl shadow-lg shadow-blue-500/25 transition-all"
                >
                  Join Campus for Free
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Link>
                <Link
                  to="/courses"
                  className="w-full sm:w-auto inline-flex items-center justify-center px-8 py-3.5 text-base font-semibold text-white bg-slate-800/80 hover:bg-slate-800 border border-slate-700 rounded-xl transition-all"
                >
                  Browse Course Catalog
                </Link>
              </>
            )}
          </div>

          {/* Quick Pillars */}
          <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-6 max-w-5xl mx-auto text-left">
            <div className="bg-white/5 border border-white/10 backdrop-blur-xs rounded-2xl p-6">
              <div className="w-12 h-12 rounded-xl bg-blue-500/20 text-blue-400 flex items-center justify-center mb-4">
                <ArrowLeftRight className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-white mb-2">1. Peer Skill Swapping</h3>
              <p className="text-sm text-slate-300 leading-relaxed">
                Add skills you can teach and skills you want to learn. Our engine identifies complementary 100% reciprocal matches!
              </p>
            </div>

            <div className="bg-white/5 border border-white/10 backdrop-blur-xs rounded-2xl p-6">
              <div className="w-12 h-12 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center mb-4">
                <BrainCircuit className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-white mb-2">2. Intelligent Fallback</h3>
              <p className="text-sm text-slate-300 leading-relaxed">
                If no student peer is found for your desired topic, the platform instantly recommends an accredited structured course.
              </p>
            </div>

            <div className="bg-white/5 border border-white/10 backdrop-blur-xs rounded-2xl p-6">
              <div className="w-12 h-12 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center mb-4">
                <Award className="w-6 h-6" />
              </div>
              <h3 className="text-lg font-bold text-white mb-2">3. Tests & Certification</h3>
              <p className="text-sm text-slate-300 leading-relaxed">
                Complete modules, score $\ge 70\%$ on mock tests to unlock progressive chapters, and earn publicly verifiable certificates.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Multi-disciplinary Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-xs font-bold text-blue-600 uppercase tracking-wider mb-2">Universal Higher Education</h2>
            <h3 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
              Supporting Every Degree & Educational Field
            </h3>
            <p className="mt-4 text-base text-slate-600">
              From Engineering and Computer Applications to Commerce, Arts, Business, Law, Design, and Career Development.
            </p>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
            {[
              { name: 'Technology & Computing', desc: 'Python, React, AI/ML, Cloud', icon: '💻' },
              { name: 'Commerce & Accounting', desc: 'B.Com, Taxation, Corporate Finance', icon: '📊' },
              { name: 'Business & Management', desc: 'BBA, MBA, Marketing Strategy', icon: '📈' },
              { name: 'Arts & Humanities', desc: 'English, Economics, Psychology', icon: '📚' },
              { name: 'Design & Creative Arts', desc: 'UI/UX, Figma, Fashion Design', icon: '🎨' },
              { name: 'Science & Mathematics', desc: 'B.Sc, Calculus, Data Science', icon: '🔬' },
              { name: 'Cybersecurity', desc: 'Network Security, Ethical Hacking', icon: '🛡️' },
              { name: 'Career & Placement', desc: 'Aptitude, Resume, Interview Prep', icon: '🎯' },
            ].map((cat, idx) => (
              <div
                key={idx}
                className="p-5 rounded-2xl bg-slate-50 border border-slate-200/80 hover:border-blue-300 hover:shadow-md transition-all group"
              >
                <div className="text-3xl mb-3">{cat.icon}</div>
                <h4 className="font-bold text-slate-800 text-sm group-hover:text-blue-600 transition-colors">{cat.name}</h4>
                <p className="text-xs text-slate-500 mt-1">{cat.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Demonstration Scenarios Preview */}
      <section className="py-20 bg-slate-100 border-y border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            {/* Scenario A Card */}
            <div className="bg-white rounded-3xl p-8 border border-slate-200 shadow-sm">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-100 text-emerald-800 text-xs font-bold mb-4">
                <CheckCircle2 className="w-3.5 h-3.5" /> Scenario A: Direct Peer Swap
              </div>
              <h3 className="text-2xl font-bold text-slate-900 mb-3">
                Complementary Matchmaking
              </h3>
              <p className="text-sm text-slate-600 mb-6 leading-relaxed">
                Rahul teaches <b>Python</b> and wants <b>UI/UX Design</b>. Priya teaches <b>UI/UX Design</b> and wants <b>Python</b>. The system matches them with a 100% reciprocal score, enabling instant swap session booking!
              </p>

              <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 flex items-center justify-between text-xs">
                <div>
                  <div className="font-bold text-slate-800">Rahul Kumar</div>
                  <div className="text-slate-500">Teaches: Python | Wants: UI/UX</div>
                </div>
                <div className="w-8 h-8 rounded-full bg-emerald-600 text-white flex items-center justify-center font-bold">
                  ↔
                </div>
                <div className="text-right">
                  <div className="font-bold text-slate-800">Priya Sharma</div>
                  <div className="text-slate-500">Teaches: UI/UX | Wants: Python</div>
                </div>
              </div>
            </div>

            {/* Scenario B Card */}
            <div className="bg-white rounded-3xl p-8 border border-slate-200 shadow-sm">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-100 text-blue-800 text-xs font-bold mb-4">
                <Sparkles className="w-3.5 h-3.5" /> Scenario B: Course Fallback
              </div>
              <h3 className="text-2xl font-bold text-slate-900 mb-3">
                Automated Course Fallback
              </h3>
              <p className="text-sm text-slate-600 mb-6 leading-relaxed">
                A student searches for <b>Machine Learning</b>. When no peer tutor is currently available, the system immediately presents the official <b>Machine Learning & AI Fundamentals</b> course with locked progression and mock assessments.
              </p>

              <div className="p-4 bg-blue-50/60 rounded-2xl border border-blue-200 flex items-center justify-between text-xs">
                <div>
                  <div className="font-bold text-blue-950">Machine Learning Fundamentals</div>
                  <div className="text-blue-700">3 Modules • Mock Tests (70% Pass) • Certificate</div>
                </div>
                <Link
                  to="/courses"
                  className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-lg transition-colors"
                >
                  Start Course
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Public Verification Callout */}
      <section className="py-16 bg-white text-center">
        <div className="max-w-4xl mx-auto px-4">
          <div className="w-14 h-14 rounded-2xl bg-blue-100 text-blue-700 flex items-center justify-center mx-auto mb-4">
            <ShieldCheck className="w-8 h-8" />
          </div>
          <h3 className="text-2xl sm:text-3xl font-bold text-slate-900 mb-2">
            Verify Academic Credentials Instantly
          </h3>
          <p className="text-sm text-slate-600 max-w-xl mx-auto mb-6">
            Every course completion generates a tamper-evident Certificate ID verified directly against our MySQL academic registry.
          </p>
          <Link
            to="/verify-certificate"
            className="inline-flex items-center px-6 py-3 text-sm font-bold text-blue-700 bg-blue-50 hover:bg-blue-100 border border-blue-200 rounded-xl transition-all"
          >
            Check Certificate Registry
          </Link>
        </div>
      </section>
    </div>
  );
};
