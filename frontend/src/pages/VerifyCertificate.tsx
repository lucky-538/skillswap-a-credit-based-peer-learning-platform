import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  ShieldCheck, Search, CheckCircle2, XCircle, Award,
  Building, Calendar, ArrowRight, ExternalLink
} from 'lucide-react';
import { certificatesApi } from '../services/api';
import { CertificateVerify } from '../types';

export const VerifyCertificate: React.FC = () => {
  const { certificateId } = useParams<{ certificateId?: string }>();

  const [inputCertId, setInputCertId] = useState(certificateId || '');
  const [verification, setVerification] = useState<CertificateVerify | null>(null);
  const [loading, setLoading] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  useEffect(() => {
    if (certificateId) {
      setInputCertId(certificateId);
      performVerify(certificateId);
    }
  }, [certificateId]);

  const performVerify = async (idToVerify: string) => {
    if (!idToVerify.trim()) return;

    setLoading(true);
    setHasSearched(true);
    try {
      const res = await certificatesApi.verifyCertificate(idToVerify.trim());
      setVerification(res.data);
    } catch (err) {
      setVerification({
        is_valid: false,
        certificate_id: idToVerify,
        institution: 'SkillSwap Campus Academy',
        status: 'INVALID',
        verification_message: 'Unable to connect to academic verification registry.'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    performVerify(inputCertId);
  };

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-8 animate-fade-in">
      <div className="text-center space-y-3 max-w-2xl mx-auto">
        <div className="w-16 h-16 rounded-3xl bg-blue-100 text-blue-700 flex items-center justify-center mx-auto mb-2 shadow-sm">
          <ShieldCheck className="w-9 h-9" />
        </div>
        <h1 className="text-3xl font-extrabold text-slate-900 tracking-tight">
          Public Certificate Verification Portal
        </h1>
        <p className="text-xs sm:text-sm text-slate-600">
          Verify authentic course completion certificates issued by the SkillSwap Campus Academic Registry.
        </p>

        {/* Search input form */}
        <form onSubmit={handleSearchSubmit} className="max-w-lg mx-auto mt-6">
          <div className="relative rounded-2xl shadow-sm">
            <input
              type="text"
              required
              value={inputCertId}
              onChange={(e) => setInputCertId(e.target.value)}
              placeholder="Enter Certificate ID (e.g. SSC-ML-2026-000001)..."
              className="block w-full pl-4 pr-28 py-3.5 text-sm border border-slate-300 rounded-2xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 font-mono text-slate-900 bg-white"
            />
            <button
              type="submit"
              disabled={loading}
              className="absolute inset-y-1.5 right-1.5 px-5 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-xl shadow-xs transition-colors flex items-center gap-1.5 disabled:opacity-60"
            >
              {loading ? 'Verifying...' : 'Verify'}
            </button>
          </div>
        </form>
      </div>

      {/* VERIFICATION RESULT CARD */}
      {hasSearched && (
        <div className="animate-fade-in">
          {verification?.is_valid ? (
            <div className="bg-white rounded-3xl p-8 sm:p-10 border-2 border-emerald-400 shadow-xl space-y-6 max-w-2xl mx-auto relative overflow-hidden">
              <div className="absolute top-0 right-0 w-32 h-32 bg-emerald-100/60 rounded-bl-full pointer-events-none"></div>

              <div className="flex items-center gap-3 text-emerald-700">
                <CheckCircle2 className="w-8 h-8 shrink-0" />
                <div>
                  <h2 className="text-xl font-extrabold text-slate-900">
                    ✓ Certificate Verified & Authentic
                  </h2>
                  <p className="text-xs text-emerald-800 font-semibold">Official SkillSwap Campus Academic Credential</p>
                </div>
              </div>

              {/* Certificate Details */}
              <div className="p-5 bg-slate-50 rounded-2xl border border-slate-200 space-y-3 text-sm">
                <div className="flex justify-between border-b border-slate-200 pb-2">
                  <span className="text-xs text-slate-500 font-semibold uppercase">Certificate ID</span>
                  <span className="font-mono font-bold text-slate-900">{verification.certificate_id}</span>
                </div>

                <div className="flex justify-between border-b border-slate-200 pb-2">
                  <span className="text-xs text-slate-500 font-semibold uppercase">Student Graduate</span>
                  <span className="font-bold text-slate-900">{verification.student_name}</span>
                </div>

                <div className="flex justify-between border-b border-slate-200 pb-2">
                  <span className="text-xs text-slate-500 font-semibold uppercase">Certified Course</span>
                  <span className="font-bold text-blue-700">{verification.course_title}</span>
                </div>

                <div className="flex justify-between border-b border-slate-200 pb-2">
                  <span className="text-xs text-slate-500 font-semibold uppercase">Issue Date</span>
                  <span className="font-medium text-slate-700">
                    {verification.issue_date ? new Date(verification.issue_date).toLocaleDateString(undefined, { year: 'numeric', month: 'long', day: 'numeric' }) : 'Verified Record'}
                  </span>
                </div>

                <div className="flex justify-between border-b border-slate-200 pb-2">
                  <span className="text-xs text-slate-500 font-semibold uppercase">Grade / Honor</span>
                  <span className="font-bold text-emerald-700">{verification.grade || 'Distinction'}</span>
                </div>

                <div className="flex justify-between pt-1">
                  <span className="text-xs text-slate-500 font-semibold uppercase">Verification Status</span>
                  <span className="px-2.5 py-0.5 bg-emerald-100 text-emerald-800 text-xs font-black rounded-full">
                    {verification.status}
                  </span>
                </div>
              </div>

              <p className="text-xs text-slate-500 text-center italic">
                "{verification.verification_message}"
              </p>
            </div>
          ) : (
            <div className="bg-white rounded-3xl p-8 border-2 border-red-300 shadow-xl space-y-4 max-w-xl mx-auto text-center">
              <XCircle className="w-12 h-12 text-red-600 mx-auto" />
              <h3 className="text-xl font-bold text-slate-900">Certificate Not Found</h3>
              <p className="text-xs text-slate-600 max-w-md mx-auto">
                {verification?.verification_message || 'No active academic record exists matching the provided Certificate ID.'}
              </p>
              <div className="p-3 bg-red-50 text-red-800 font-mono text-xs rounded-xl border border-red-200 inline-block">
                Queried ID: {verification?.certificate_id}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
