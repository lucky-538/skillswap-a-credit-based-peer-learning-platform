import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Award, Download, ShieldCheck, Eye, BookOpen, ExternalLink } from 'lucide-react';
import { certificatesApi } from '../services/api';
import { Certificate } from '../types';

export const Certificates: React.FC = () => {
  const [certificates, setCertificates] = useState<Certificate[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    certificatesApi.getMyCertificates()
      .then(res => setCertificates(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-fade-in">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Earned Certificates of Completion
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Official academic credentials verified and recorded in the SkillSwap Campus registry.
          </p>
        </div>

        <Link
          to="/verify-certificate"
          className="inline-flex items-center px-4 py-2 text-xs font-bold text-blue-700 bg-blue-50 hover:bg-blue-100 border border-blue-200 rounded-xl transition-colors"
        >
          <ShieldCheck className="w-4 h-4 mr-1.5" />
          Public Verification Tool
        </Link>
      </div>

      {loading ? (
        <div className="py-20 text-center text-sm text-slate-400">Loading your verified certificates...</div>
      ) : certificates.length === 0 ? (
        <div className="py-16 text-center bg-white rounded-3xl border border-dashed border-slate-200 shadow-xs space-y-4">
          <Award className="w-12 h-12 text-slate-300 mx-auto" />
          <h3 className="text-base font-bold text-slate-700">No certificates earned yet</h3>
          <p className="text-xs text-slate-500 max-w-md mx-auto">
            Complete all modules in an enrolled course and pass the final assessment with $\ge 70\%$ to receive your official certificate.
          </p>
          <Link
            to="/courses"
            className="inline-flex items-center px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-xl shadow-md transition-colors"
          >
            Start a Course
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {certificates.map(cert => (
            <div
              key={cert.id}
              className="bg-white rounded-3xl border-2 border-emerald-200 p-6 shadow-xs hover:shadow-lg transition-all space-y-5 flex flex-col justify-between relative overflow-hidden"
            >
              <div className="absolute top-0 right-0 w-24 h-24 bg-gradient-to-br from-emerald-100/50 to-transparent rounded-bl-full pointer-events-none"></div>

              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <div className="w-10 h-10 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center">
                    <Award className="w-5 h-5" />
                  </div>
                  <span className="px-2.5 py-1 bg-emerald-100 text-emerald-800 text-[10px] font-extrabold rounded-full">
                    {cert.grade}
                  </span>
                </div>

                <div>
                  <h3 className="text-base font-bold text-slate-900 line-clamp-1">{cert.course_title}</h3>
                  <div className="text-xs text-slate-500 mt-0.5">Recipient: <b>{cert.student_name}</b></div>
                </div>

                <div className="p-3 bg-slate-50 rounded-xl border border-slate-100 space-y-1 text-xs font-mono">
                  <div className="text-slate-400 text-[10px] uppercase">Certificate ID:</div>
                  <div className="text-slate-800 font-bold break-all">{cert.certificate_id}</div>
                </div>
              </div>

              <div className="pt-3 border-t border-slate-100 flex items-center justify-between gap-2">
                <Link
                  to={`/verify-certificate/${cert.certificate_id}`}
                  className="px-3 py-2 text-xs font-bold text-slate-600 hover:text-blue-700 hover:bg-slate-100 rounded-xl transition-colors flex items-center gap-1"
                >
                  <Eye className="w-3.5 h-3.5" /> Verify
                </Link>

                <a
                  href={certificatesApi.getDownloadUrl(cert.id)}
                  target="_blank"
                  rel="noreferrer"
                  className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-xl shadow-xs transition-colors flex items-center gap-1.5"
                >
                  <Download className="w-3.5 h-3.5" /> Download PDF
                </a>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
