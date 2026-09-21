import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import {
  Award, CheckCircle2, XCircle, ArrowLeft, RotateCcw,
  Sparkles, ArrowRight, Clock, AlertCircle
} from 'lucide-react';
import confetti from 'canvas-confetti';
import { assessmentsApi } from '../services/api';
import { AssessmentDetail, AssessmentResult } from '../types';

export const FinalAssessment: React.FC = () => {
  const { courseId } = useParams<{ courseId: string }>();
  const navigate = useNavigate();

  const [assessment, setAssessment] = useState<AssessmentDetail | null>(null);
  const [selectedAnswers, setSelectedAnswers] = useState<{ [questionId: number]: number }>({});
  const [result, setResult] = useState<AssessmentResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (courseId) {
      loadFinalAssessment();
    }
  }, [courseId]);

  const loadFinalAssessment = async () => {
    setLoading(true);
    try {
      const res = await assessmentsApi.getFinalAssessment(Number(courseId));
      setAssessment(res.data);
    } catch (e: any) {
      setError(e.response?.data?.detail || 'Final assessment questions not found.');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectOption = (questionId: number, optionId: number) => {
    if (result) return;
    setSelectedAnswers(prev => ({
      ...prev,
      [questionId]: optionId
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!assessment) return;

    if (Object.keys(selectedAnswers).length < assessment.questions.length) {
      setError(`Please answer all ${assessment.questions.length} questions before submitting.`);
      return;
    }

    setError(null);
    setSubmitting(true);

    const answersPayload = Object.entries(selectedAnswers).map(([qId, optId]) => ({
      question_id: Number(qId),
      selected_option_id: Number(optId)
    }));

    try {
      const res = await assessmentsApi.submitFinalAssessment(Number(courseId), answersPayload);
      setResult(res.data);

      if (res.data.is_passed) {
        // Fire celebration confetti!
        confetti({
          particleCount: 120,
          spread: 80,
          origin: { y: 0.6 }
        });
      }
    } catch (e: any) {
      setError(e.response?.data?.detail || 'Failed to submit final assessment.');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) {
    return (
      <div className="py-20 text-center text-sm text-slate-400">Loading comprehensive final examination...</div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-fade-in">
      <div className="flex items-center justify-between border-b border-slate-200 pb-4">
        <button
          onClick={() => navigate(`/learn/${courseId}`)}
          className="inline-flex items-center gap-1 text-xs font-bold text-slate-600 hover:text-slate-900"
        >
          <ArrowLeft className="w-4 h-4" /> Return to Course Player
        </button>

        <span className="px-3 py-1 bg-indigo-50 text-indigo-900 border border-indigo-200 text-xs font-bold rounded-full flex items-center gap-1">
          <Award className="w-3.5 h-3.5 text-indigo-600" /> Certificate Qualification Exam
        </span>
      </div>

      {/* Hero Exam Banner */}
      <div className="bg-gradient-to-r from-indigo-900 via-blue-900 to-slate-900 rounded-3xl p-8 text-white shadow-xl space-y-2">
        <span className="text-xs font-bold text-teal-300 uppercase tracking-wider">
          Final Examination
        </span>
        <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
          {assessment?.title}
        </h1>
        <p className="text-xs sm:text-sm text-slate-300 max-w-2xl">
          Pass with $\ge 70\%$ to complete the course curriculum and generate your verified digital Certificate of Completion.
        </p>
      </div>

      {/* Result Card */}
      {result && (
        <div className={`rounded-3xl p-8 border shadow-lg space-y-6 animate-fade-in ${
          result.is_passed
            ? 'bg-emerald-50 border-emerald-300 text-emerald-950'
            : 'bg-red-50 border-red-300 text-red-950'
        }`}>
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <div className={`w-14 h-14 rounded-2xl flex items-center justify-center text-white ${
                result.is_passed ? 'bg-emerald-600' : 'bg-red-600'
              }`}>
                {result.is_passed ? <Award className="w-8 h-8" /> : <XCircle className="w-8 h-8" />}
              </div>
              <div>
                <h2 className="text-2xl font-black">
                  {result.is_passed ? 'CONGRATULATIONS! COURSE COMPLETED 🎓' : 'EXAMINATION FAILED'}
                </h2>
                <p className="text-xs mt-1">{result.feedback_message}</p>
              </div>
            </div>

            <div className="text-right">
              <div className="text-3xl font-black">{result.percentage}%</div>
              <div className="text-xs font-bold opacity-80">Final Score: {result.score} / {result.total_marks}</div>
            </div>
          </div>

          {result.is_passed && result.certificate_id && (
            <div className="p-4 bg-white/80 rounded-2xl border border-emerald-200 flex flex-col sm:flex-row items-center justify-between gap-4">
              <div>
                <div className="text-xs font-bold text-slate-700">Official Certificate ID Issued:</div>
                <div className="text-sm font-mono font-black text-emerald-700">{result.certificate_id}</div>
              </div>
              <Link
                to="/certificates"
                className="px-6 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-xl shadow-md transition-all flex items-center gap-1.5"
              >
                <Award className="w-4 h-4" />
                View & Download Certificate
              </Link>
            </div>
          )}

          {!result.is_passed && (
            <div className="flex justify-end">
              <button
                onClick={() => {
                  setResult(null);
                  setSelectedAnswers({});
                  window.scrollTo({ top: 0, behavior: 'smooth' });
                }}
                className="px-5 py-2.5 bg-red-600 hover:bg-red-700 text-white font-bold text-xs rounded-xl shadow-xs transition-colors flex items-center gap-1.5"
              >
                <RotateCcw className="w-4 h-4" />
                Retake Final Examination
              </button>
            </div>
          )}
        </div>
      )}

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 text-red-700 text-xs font-semibold rounded-2xl flex items-center gap-2">
          <AlertCircle className="w-4 h-4 text-red-600 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* Questions */}
      <form onSubmit={handleSubmit} className="space-y-6">
        {assessment?.questions.map((q, qIdx) => (
          <div key={q.id} className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-xs space-y-4">
            <h3 className="text-sm sm:text-base font-bold text-slate-900">
              <span className="text-indigo-600 mr-2">Q{qIdx + 1}.</span>
              {q.question_text}
            </h3>

            <div className="space-y-2.5">
              {q.options.map(opt => {
                const isSelected = selectedAnswers[q.id] === opt.id;
                return (
                  <label
                    key={opt.id}
                    onClick={() => handleSelectOption(q.id, opt.id)}
                    className={`w-full p-3.5 rounded-2xl border text-xs sm:text-sm font-medium flex items-center gap-3 cursor-pointer transition-all ${
                      isSelected
                        ? 'bg-indigo-50 border-indigo-500 text-indigo-950 font-semibold'
                        : 'bg-slate-50/80 border-slate-200 hover:bg-slate-50 text-slate-800'
                    }`}
                  >
                    <div className={`w-4 h-4 rounded-full border-2 flex items-center justify-center ${
                      isSelected ? 'border-indigo-600 bg-indigo-600' : 'border-slate-400'
                    }`}>
                      {isSelected && <div className="w-1.5 h-1.5 rounded-full bg-white"></div>}
                    </div>
                    <span>{opt.option_text}</span>
                  </label>
                );
              })}
            </div>
          </div>
        ))}

        {!result && (
          <div className="pt-4 flex justify-end">
            <button
              type="submit"
              disabled={submitting}
              className="px-8 py-3.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm rounded-2xl shadow-lg shadow-indigo-600/25 transition-all flex items-center gap-2"
            >
              {submitting ? 'Evaluating Final Examination...' : 'Submit Final Examination & Qualify'}
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        )}
      </form>
    </div>
  );
};
