import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeftRight, Award, ShieldCheck, Heart } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-slate-900 text-slate-300 pt-12 pb-8 border-t border-slate-800">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          <div className="md:col-span-1">
            <div className="flex items-center gap-2 mb-3">
              <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white font-bold">
                <ArrowLeftRight className="w-4 h-4" />
              </div>
              <span className="text-lg font-bold text-white">SkillSwap Campus</span>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Empowering university & college students across all disciplines to exchange skills, enroll in structured curricula, pass mock assessments, and earn verified certificates.
            </p>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-white uppercase tracking-wider mb-3">Peer Exchange</h4>
            <ul className="space-y-2 text-xs">
              <li><Link to="/skills" className="hover:text-white transition-colors">Smart Match Finder</Link></li>
              <li><Link to="/swap-requests" className="hover:text-white transition-colors">Swap Hub & Sessions</Link></li>
              <li><Link to="/profile" className="hover:text-white transition-colors">Manage Teaching Portfolio</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-white uppercase tracking-wider mb-3">E-Learning & LMS</h4>
            <ul className="space-y-2 text-xs">
              <li><Link to="/courses" className="hover:text-white transition-colors">Course Catalog</Link></li>
              <li><Link to="/my-courses" className="hover:text-white transition-colors">My Learning Dashboard</Link></li>
              <li><Link to="/certificates" className="hover:text-white transition-colors">Earned Certificates</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-white uppercase tracking-wider mb-3">Trust & Validation</h4>
            <ul className="space-y-2 text-xs">
              <li>
                <Link to="/verify-certificate" className="inline-flex items-center gap-1.5 text-blue-400 hover:text-blue-300">
                  <ShieldCheck className="w-3.5 h-3.5" /> Public Certificate Verification
                </Link>
              </li>
              <li><span className="text-slate-400">Passing Score: 70% MCQ Mock Tests</span></li>
              <li><span className="text-slate-400">Institutional Registry Integration</span></li>
            </ul>
          </div>
        </div>

        <div className="pt-6 border-t border-slate-800 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500">
          <p>© {new Date().getFullYear()} SkillSwap Campus Platform. All rights reserved.</p>
          <p className="flex items-center gap-1 mt-2 sm:mt-0">
            Engineered with <Heart className="w-3.5 h-3.5 text-red-500 fill-red-500" /> for collaborative higher education.
          </p>
        </div>
      </div>
    </footer>
  );
};
