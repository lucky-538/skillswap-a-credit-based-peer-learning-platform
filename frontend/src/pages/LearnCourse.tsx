import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import {
  BookOpen, CheckCircle2, Lock, PlayCircle, Award,
  ArrowLeft, ArrowRight, Check, HelpCircle, AlertCircle
} from 'lucide-react';
import { enrollmentsApi } from '../services/api';
import { LearningCourseView, LearningModule, LearningLesson } from '../types';

export const LearnCourse: React.FC = () => {
  const { courseId } = useParams<{ courseId: string }>();
  const navigate = useNavigate();

  const [learningView, setLearningView] = useState<LearningCourseView | null>(null);
  const [activeModuleIndex, setActiveModuleIndex] = useState(0);
  const [activeLesson, setActiveLesson] = useState<LearningLesson | null>(null);
  const [loading, setLoading] = useState(true);
  const [completing, setCompleting] = useState(false);

  useEffect(() => {
    if (courseId) {
      loadLearningView();
    }
  }, [courseId]);

  const loadLearningView = async () => {
    try {
      const res = await enrollmentsApi.getCourseLearningView(Number(courseId));
      setLearningView(res.data);

      // Set initial active lesson if not set
      if (res.data.modules.length > 0) {
        const firstUnlocked = res.data.modules.find(m => m.is_unlocked) || res.data.modules[0];
        const modIdx = res.data.modules.indexOf(firstUnlocked);
        setActiveModuleIndex(modIdx);
        if (firstUnlocked.lessons.length > 0) {
          const firstIncomplete = firstUnlocked.lessons.find(l => !l.is_completed) || firstUnlocked.lessons[0];
          setActiveLesson(firstIncomplete);
        }
      }
    } catch (err) {
      console.error('Failed to load learning view:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleMarkLessonComplete = async () => {
    if (!activeLesson) return;
    setCompleting(true);

    try {
      await enrollmentsApi.completeLesson(activeLesson.id);
      await loadLearningView();
    } catch (e) {
      console.error(e);
    } finally {
      setCompleting(false);
    }
  };

  const handleSelectLesson = (mod: LearningModule, modIdx: number, les: LearningLesson) => {
    if (!mod.is_unlocked) return;
    setActiveModuleIndex(modIdx);
    setActiveLesson(les);
  };

  if (loading) {
    return (
      <div className="py-20 text-center text-sm text-slate-400">Loading LMS Course Player...</div>
    );
  }

  if (!learningView) {
    return (
      <div className="py-20 text-center text-sm text-slate-600">Course content not found.</div>
    );
  }

  const currentModule = learningView.modules[activeModuleIndex];

  return (
    <div className="min-h-[calc(100vh-4rem)] bg-slate-100 flex flex-col">
      {/* Top Learning Bar */}
      <div className="bg-slate-900 text-white px-4 sm:px-8 py-3.5 flex items-center justify-between border-b border-slate-800">
        <div className="flex items-center gap-3">
          <Link to="/my-courses" className="text-slate-400 hover:text-white p-1 rounded-lg">
            <ArrowLeft className="w-5 h-5" />
          </Link>
          <div>
            <h2 className="text-sm sm:text-base font-bold text-white line-clamp-1">
              {learningView.course.title}
            </h2>
            <div className="text-[11px] text-slate-400">
              Progress: <b>{learningView.enrollment.progress_percentage}%</b> Completed
            </div>
          </div>
        </div>

        {/* Progress Bar & Certificate Shortcut */}
        <div className="flex items-center gap-4">
          {learningView.certificate_id && (
            <Link
              to={`/certificates`}
              className="px-3 py-1 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-lg flex items-center gap-1"
            >
              <Award className="w-3.5 h-3.5" /> View Certificate
            </Link>
          )}

          <div className="hidden sm:block w-36">
            <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
              <div
                className="h-full bg-blue-500 rounded-full transition-all duration-500"
                style={{ width: `${learningView.enrollment.progress_percentage}%` }}
              ></div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Split Player View */}
      <div className="flex-1 flex flex-col md:flex-row">
        {/* Left Module Syllabus Sidebar (1/3 width) */}
        <div className="w-full md:w-80 lg:w-96 bg-white border-r border-slate-200 p-4 space-y-4 overflow-y-auto max-h-[calc(100vh-8rem)]">
          <h3 className="text-xs font-bold text-slate-500 uppercase tracking-wider px-2">
            Course Modules & Tests
          </h3>

          <div className="space-y-3">
            {learningView.modules.map((mod, modIdx) => (
              <div
                key={mod.id}
                className={`rounded-2xl border p-3 transition-all ${
                  !mod.is_unlocked
                    ? 'bg-slate-50 border-slate-200 opacity-65'
                    : activeModuleIndex === modIdx
                    ? 'bg-blue-50/40 border-blue-300 ring-1 ring-blue-400/20'
                    : 'bg-white border-slate-200'
                }`}
              >
                <div className="flex items-center justify-between gap-2 mb-2">
                  <div className="flex items-center gap-2">
                    {mod.is_completed ? (
                      <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                    ) : mod.is_unlocked ? (
                      <div className="w-4 h-4 rounded-full border-2 border-blue-600 shrink-0"></div>
                    ) : (
                      <Lock className="w-4 h-4 text-slate-400 shrink-0" />
                    )}
                    <h4 className="text-xs font-bold text-slate-900 leading-tight">
                      {mod.title}
                    </h4>
                  </div>
                  {!mod.is_unlocked && (
                    <span className="text-[10px] font-bold text-slate-500 bg-slate-200 px-1.5 py-0.5 rounded-sm">
                      Locked
                    </span>
                  )}
                </div>

                {/* Lessons in Module */}
                <div className="space-y-1 pl-6">
                  {mod.lessons.map(les => (
                    <button
                      key={les.id}
                      disabled={!mod.is_unlocked}
                      onClick={() => handleSelectLesson(mod, modIdx, les)}
                      className={`w-full text-left p-1.5 rounded-lg text-xs flex items-center justify-between transition-colors ${
                        activeLesson?.id === les.id
                          ? 'bg-blue-600 text-white font-bold'
                          : les.is_completed
                          ? 'text-slate-700 hover:bg-slate-100 font-medium'
                          : 'text-slate-600 hover:bg-slate-100'
                      }`}
                    >
                      <span className="truncate">{les.title}</span>
                      {les.is_completed && (
                        <Check className={`w-3.5 h-3.5 ${activeLesson?.id === les.id ? 'text-white' : 'text-emerald-600'}`} />
                      )}
                    </button>
                  ))}

                  {/* Module Mock Test Trigger */}
                  {mod.assessment_id && (
                    <div className="pt-2">
                      <Link
                        to={mod.is_unlocked ? `/assessment/${mod.id}` : '#'}
                        className={`w-full p-2 text-xs font-bold rounded-xl flex items-center justify-between transition-colors ${
                          !mod.is_unlocked
                            ? 'bg-slate-100 text-slate-400 cursor-not-allowed pointer-events-none'
                            : mod.assessment_passed
                            ? 'bg-emerald-50 text-emerald-800 border border-emerald-200'
                            : 'bg-amber-500 text-white hover:bg-amber-600 shadow-xs'
                        }`}
                      >
                        <span className="flex items-center gap-1.5">
                          <HelpCircle className="w-3.5 h-3.5" />
                          {mod.assessment_passed ? `Mock Test (Passed: ${mod.assessment_score}%)` : 'Take Mock Test (70% Pass)'}
                        </span>
                        <ArrowRight className="w-3.5 h-3.5" />
                      </Link>
                    </div>
                  )}
                </div>
              </div>
            ))}

            {/* Final Assessment Card in Sidebar */}
            <div className={`p-4 rounded-2xl border text-center space-y-2 ${
              learningView.final_assessment_unlocked
                ? 'bg-gradient-to-tr from-indigo-50 to-blue-50 border-indigo-200'
                : 'bg-slate-50 border-slate-200 opacity-60'
            }`}>
              <Award className="w-8 h-8 text-indigo-600 mx-auto" />
              <div className="text-xs font-bold text-slate-900">Final Comprehensive Exam</div>
              <p className="text-[11px] text-slate-500">
                Unlock certified completion by scoring $\ge 70\%$ on the final assessment.
              </p>
              {learningView.final_assessment_unlocked ? (
                <Link
                  to={`/final-assessment/${learningView.course.id}`}
                  className="block w-full py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs rounded-xl shadow-sm transition-colors"
                >
                  Start Final Exam
                </Link>
              ) : (
                <div className="text-[10px] text-slate-400 font-semibold">
                  Complete and pass all preceding modules first
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Right Main Content Viewer (2/3 width) */}
        <div className="flex-1 p-6 sm:p-10 overflow-y-auto max-h-[calc(100vh-8rem)]">
          {activeLesson ? (
            <div className="max-w-3xl mx-auto bg-white rounded-3xl p-6 sm:p-10 border border-slate-200 shadow-sm space-y-6">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-4">
                <div>
                  <span className="text-[11px] font-bold text-blue-600 uppercase tracking-wider">
                    {currentModule?.title}
                  </span>
                  <h1 className="text-2xl font-extrabold text-slate-900 mt-1">
                    {activeLesson.title}
                  </h1>
                </div>

                <div className="flex items-center gap-2">
                  <span className="text-xs text-slate-500 font-medium">
                    {activeLesson.duration_minutes} min read
                  </span>
                </div>
              </div>

              {/* Lesson Text Body */}
              <div className="prose prose-slate max-w-none text-slate-800 text-sm sm:text-base leading-relaxed whitespace-pre-line">
                {activeLesson.content_text}
              </div>

              {/* Lesson Actions */}
              <div className="pt-6 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div>
                  {activeLesson.is_completed ? (
                    <span className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-emerald-50 text-emerald-800 border border-emerald-200 rounded-xl text-xs font-bold">
                      <CheckCircle2 className="w-4 h-4 text-emerald-600" /> Lesson Completed
                    </span>
                  ) : (
                    <span className="text-xs text-slate-500">Read the lesson carefully before completing.</span>
                  )}
                </div>

                <div className="flex items-center gap-3">
                  {!activeLesson.is_completed && (
                    <button
                      onClick={handleMarkLessonComplete}
                      disabled={completing}
                      className="px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-xl shadow-md transition-all flex items-center gap-1.5"
                    >
                      {completing ? 'Updating...' : (
                        <>
                          <Check className="w-4 h-4" />
                          Mark as Completed
                        </>
                      )}
                    </button>
                  )}

                  {/* If all lessons in module are complete, prompt mock test */}
                  {currentModule?.assessment_id && currentModule.lessons_completed_count === currentModule.total_lessons_count && (
                    <Link
                      to={`/assessment/${currentModule.id}`}
                      className="px-5 py-2.5 bg-amber-500 hover:bg-amber-600 text-white font-bold text-xs rounded-xl shadow-md transition-all flex items-center gap-1.5"
                    >
                      <HelpCircle className="w-4 h-4" />
                      Take Module Assessment
                    </Link>
                  )}
                </div>
              </div>
            </div>
          ) : (
            <div className="py-20 text-center text-sm text-slate-400">Select a lesson from the left sidebar to start learning.</div>
          )}
        </div>
      </div>
    </div>
  );
};
