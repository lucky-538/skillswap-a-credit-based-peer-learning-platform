import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import {
  HelpCircle, CheckCircle2, XCircle, ArrowLeft,
  RotateCcw, Award, ArrowRight, Clock, AlertCircle
} from 'lucide-react';
import { assessmentsApi } from '../services/api';
import { AssessmentDetail, AssessmentResult } from '../types';

export const ModuleAssessment: React.FC = () => {
  const { id } = useParams<{ id: string }>(); // module_id
  const navigate = useNavigate();

  const [assessment, setAssessment] = useState<AssessmentDetail | null>(null);
  const [selectedAnswers, setSelectedAnswers] = useState<{ [questionId: number]: number }>({});
  const [result, setResult] = useState<AssessmentResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (id) {
      loadAssessment();
    }
  }, [id]);

  const loadAssessment = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    setSelectedAnswers({});

    try {
      const res = await assessmentsApi.getModuleAssessment(Number(id));
      setAssessment(res.data);
    } catch (e: any) {
      setError(e.response?.data?.detail || 'Assessment not found for this module.');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectOption = (questionId: number, optionId: number) => {
    if (result) return; // Locked once submitted
    setSelectedAnswers(prev => ({
      ...prev,
      [questionId]: optionId
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!assessment) return;

    // Verify all answered
    const answeredCount = Object.keys(selectedAnswers).length;
    if (answeredCount < assessment.questions.length) {
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
      const res = await assessmentsApi.submitModuleAssessment(assessment.id, answersPayload);
      setResult(res.data);
    } catch (e: any) {
      setError(e.response?.data?.detail || 'Failed to evaluate assessment.');
    } finally {
      setSubmitting(false);
    }
  };

  const handleRetake = () => {
    setResult(null);
    setSelectedAnswers({});
    setError(null);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  if (loading) {
    return (
      <div className="py-20 text-center text-sm text-slate-400">Loading module mock assessment...</div>
    );
  }

  if (error && !assessment) {
    return (
      <div className="max-w-2xl mx-auto py-16 px-4 text-center space-y-4">
        <AlertCircle className="w-10 h-10 text-red-500 mx-auto" />
        <h2 className="text-lg font-bold text-slate-900">{error}</h2>
        <button
          onClick={() => navigate(-1)}
          className="px-4 py-2 bg-slate-800 text-white font-bold text-xs rounded-xl"
        >
          Return to Learning
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-fade-in">
      {/* Top Header */}
      <div className="flex items-center justify-between border-b border-slate-200 pb-4">
        <button
          onClick={() => navigate(`/learn/${assessment?.course_id}`)}
          className="inline-flex items-center gap-1 text-xs font-bold text-slate-600 hover:text-slate-900"
        >
          <ArrowLeft className="w-4 h-4" /> Back to Lessons
        </button>

        <div className="flex items-center gap-3">
          <span className="px-3 py-1 bg-amber-50 text-amber-900 border border-amber-200 text-xs font-bold rounded-full flex items-center gap-1">
            <Clock className="w-3.5 h-3.5" /> 70% Required to Pass
          </span>
        </div>
      </div>

      {/* Assessment Info Banner */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-xs space-y-2">
        <span className="text-xs font-bold text-blue-600 uppercase tracking-wider">
          Module Assessment
        </span>
        <h1 className="text-2xl font-extrabold text-slate-900">
          {assessment?.title}
        </h1>
        <p className="text-xs text-slate-500">
          Course: <b>{assessment?.course_title}</b> • {assessment?.total_questions} Questions • Passing Threshold: {assessment?.passing_percentage}%
        </p>
      </div>

      {/* RESULT EVALUATION CARD (ON SUBMISSION) */}
      {result && (
        <div className={`rounded-3xl p-6 sm:p-8 border shadow-md space-y-4 animate-fade-in ${
          result.is_passed
            ? 'bg-emerald-50/80 border-emerald-300 text-emerald-950'
            : 'bg-red-50/80 border-red-300 text-red-950'
        }`}>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              {result.is_passed ? (
                <div className="w-12 h-12 rounded-2xl bg-emerald-600 text-white flex items-center justify-center">
                  <CheckCircle2 className="w-6 h-6" />
                </div>
              ) : (
                <div className="w-12 h-12 rounded-2xl bg-red-600 text-white flex items-center justify-center">
                  <XCircle className="w-6 h-6" />
                </div>
              )}
              <div>
                <h2 className="text-xl font-extrabold">
                  {result.is_passed ? 'ASSESSMENT PASSED ✓' : 'ASSESSMENT FAILED'}
                </h2>
                <p className="text-xs mt-0.5 opacity-90">{result.feedback_message}</p>
              </div>
            </div>

            <div className="text-right">
              <div className="text-2xl font-black">{result.percentage}%</div>
              <div className="text-[11px] opacity-80 font-semibold">Score: {result.score} / {result.total_marks}</div>
            </div>
          </div>

          {/* Action Button after result */}
          <div className="pt-4 border-t border-slate-200/60 flex items-center justify-end gap-3">
            {!result.is_passed ? (
              <button
                onClick={handleRetake}
                className="px-5 py-2.5 bg-red-600 hover:bg-red-700 text-white font-bold text-xs rounded-xl shadow-xs transition-colors flex items-center gap-1.5"
              >
                <RotateCcw className="w-4 h-4" />
                Retake Assessment
              </button>
            ) : (
              <Link
                to={`/learn/${assessment?.course_id}`}
                className="px-6 py-2.5 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-xl shadow-xs transition-colors flex items-center gap-1.5"
              >
                Continue to Next Module
                <ArrowRight className="w-4 h-4" />
              </Link>
            )}
          </div>
        </div>
      )}

      {error && (
        <div className="p-4 bg-red-50 border border-red-200 text-red-700 text-xs font-semibold rounded-2xl flex items-center gap-2">
          <AlertCircle className="w-4 h-4 text-red-600 shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {/* QUESTIONS FORM */}
      <form onSubmit={handleSubmit} className="space-y-6">
        {assessment?.questions.map((q, qIdx) => {
          const resultDetail = result?.question_results.find(r => r.question_id === q.id);

          return (
            <div
              key={q.id}
              className={`bg-white rounded-3xl p-6 sm:p-8 border shadow-xs space-y-4 ${
                resultDetail
                  ? resultDetail.is_correct
                    ? 'border-emerald-200 bg-emerald-50/20'
                    : 'border-red-200 bg-red-50/20'
                  : 'border-slate-200'
              }`}
            >
              <div className="flex items-start justify-between gap-4">
                <h3 className="text-sm sm:text-base font-bold text-slate-900">
                  <span className="text-blue-600 mr-2">Q{qIdx + 1}.</span>
                  {q.question_text}
                </h3>
                <span className="text-xs font-semibold text-slate-400 shrink-0">
                  {q.marks} Mark
                </span>
              </div>

              {/* Options List */}
              <div className="space-y-2.5">
                {q.options.map(opt => {
                  const isSelected = selectedAnswers[q.id] === opt.id;
                  const isCorrect = resultDetail?.correct_option_id === opt.id;
                  const isWrongSelected = isSelected && !resultDetail?.is_correct && resultDetail !== undefined;

                  return (
                    <label
                      key={opt.id}
                      onClick={() => handleSelectOption(q.id, opt.id)}
                      className={`w-full p-3.5 rounded-2xl border text-xs sm:text-sm font-medium flex items-center justify-between cursor-pointer transition-all ${
                        isCorrect && result
                          ? 'bg-emerald-100 border-emerald-400 text-emerald-950 font-bold'
                          : isWrongSelected
                          ? 'bg-red-100 border-red-400 text-red-950'
                          : isSelected
                          ? 'bg-blue-50 border-blue-500 text-blue-900 shadow-xs'
                          : 'bg-slate-50/80 border-slate-200 hover:bg-slate-50 text-slate-800'
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <div className={`w-4 h-4 rounded-full border-2 flex items-center justify-center ${
                          isSelected ? 'border-blue-600 bg-blue-600' : 'border-slate-400'
                        }`}>
                          {isSelected && <div className="w-1.5 h-1.5 rounded-full bg-white"></div>}
                        </div>
                        <span>{opt.option_text}</span>
                      </div>

                      {result && isCorrect && (
                        <span className="text-xs text-emerald-700 font-bold">Correct Answer ✓</span>
                      )}
                    </label>
                  );
                })}
              </div>

              {/* Explanation after submission */}
              {resultDetail?.explanation && (
                <div className="p-3 bg-slate-50 rounded-xl border border-slate-100 text-xs text-slate-600">
                  <b>Explanation:</b> {resultDetail.explanation}
                </div>
              )}
            </div>
          );
        })}

        {/* Submit Action */}
        {!result && (
          <div className="pt-4 flex justify-end">
            <button
              type="submit"
              disabled={submitting}
              className="px-8 py-3.5 bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm rounded-2xl shadow-md shadow-blue-500/20 transition-all flex items-center gap-2"
            >
              {submitting ? 'Evaluating Mock Test...' : 'Submit Assessment'}
              <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        )}
      </form>
    </div>
  );
};
