import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import {
  BookOpen, Star, Clock, CheckCircle2, ShieldCheck,
  User, Layers, PlayCircle, Award, ArrowRight
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { coursesApi, enrollmentsApi } from '../services/api';
import { CourseDetail as CourseDetailType } from '../types';

export const CourseDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  const [course, setCourse] = useState<CourseDetailType | null>(null);
  const [loading, setLoading] = useState(true);
  const [enrolling, setEnrolling] = useState(false);

  useEffect(() => {
    if (id) {
      coursesApi.getCourseDetail(Number(id))
        .then(res => setCourse(res.data))
        .catch(err => console.error(err))
        .finally(() => setLoading(false));
    }
  }, [id]);

  const handleEnroll = async () => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    if (!course) return;

    setEnrolling(true);
    try {
      await enrollmentsApi.enrollCourse(course.id);
      navigate(`/learn/${course.id}`);
    } catch (e) {
      console.error(e);
      navigate(`/learn/${course.id}`);
    } finally {
      setEnrolling(false);
    }
  };

  if (loading) {
    return (
      <div className="py-20 text-center text-sm text-slate-400">Loading course curriculum...</div>
    );
  }

  if (!course) {
    return (
      <div className="py-20 text-center text-sm text-slate-600">Course not found.</div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-fade-in">
      {/* Course Overview Header */}
      <div className="bg-slate-900 rounded-3xl p-8 text-white shadow-xl flex flex-col lg:flex-row gap-8 items-center lg:items-start justify-between">
        <div className="space-y-4 max-w-2xl">
          <div className="flex flex-wrap items-center gap-2">
            <span className="px-3 py-1 bg-blue-600/40 text-blue-300 text-xs font-bold rounded-full border border-blue-400/30 uppercase">
              {course.category?.name || 'Curriculum'}
            </span>
            <span className="px-3 py-1 bg-white/10 text-slate-300 text-xs font-semibold rounded-full">
              {course.difficulty}
            </span>
            <span className="px-3 py-1 bg-white/10 text-slate-300 text-xs font-semibold rounded-full flex items-center gap-1">
              <Clock className="w-3 h-3" /> {course.duration_hours} Total Hours
            </span>
          </div>

          <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight">
            {course.title}
          </h1>

          <p className="text-sm text-slate-300 leading-relaxed">
            {course.description}
          </p>

          <div className="flex items-center gap-4 text-xs text-slate-400 pt-2">
            <span className="flex items-center gap-1"><User className="w-3.5 h-3.5 text-blue-400" /> Instructor: {course.instructor_name}</span>
            <span className="flex items-center gap-1 text-amber-400 font-bold"><Star className="w-3.5 h-3.5 fill-amber-400" /> {course.rating} Rating</span>
          </div>
        </div>

        {/* Enrollment Card */}
        <div className="bg-white rounded-3xl p-6 text-slate-900 shadow-2xl w-full lg:w-80 shrink-0 space-y-4 border border-slate-200">
          <div className="h-36 bg-slate-900 rounded-2xl overflow-hidden relative">
            {course.thumbnail_url ? (
              <img src={course.thumbnail_url} alt={course.title} className="w-full h-full object-cover" />
            ) : (
              <div className="w-full h-full flex items-center justify-center text-white">
                <BookOpen className="w-10 h-10 text-blue-400" />
              </div>
            )}
          </div>

          <div className="space-y-2 text-xs text-slate-600">
            <div className="flex items-center justify-between">
              <span>Modules</span>
              <span className="font-bold text-slate-900">{course.modules.length} Modules</span>
            </div>
            <div className="flex items-center justify-between">
              <span>Assessment</span>
              <span className="font-bold text-slate-900">70% Pass Required</span>
            </div>
            <div className="flex items-center justify-between">
              <span>Certificate</span>
              <span className="font-bold text-emerald-600">Included</span>
            </div>
          </div>

          <button
            onClick={handleEnroll}
            disabled={enrolling}
            className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-bold text-sm rounded-xl shadow-md transition-all flex items-center justify-center gap-2"
          >
            {enrolling ? (
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            ) : (
              <>
                <PlayCircle className="w-4 h-4" />
                Enroll & Start Learning
              </>
            )}
          </button>
        </div>
      </div>

      {/* Syllabus & Learning Goals */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column (2/3 width): Modules Syllabus */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-xs space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
                <Layers className="w-5 h-5 text-blue-600" />
                Course Curriculum & Modules
              </h2>
              <span className="text-xs font-semibold text-slate-500">
                {course.modules.length} Progressive Modules
              </span>
            </div>

            <div className="space-y-4">
              {course.modules.map((mod, idx) => (
                <div key={mod.id} className="p-4 rounded-2xl border border-slate-200 bg-slate-50/50 space-y-2">
                  <div className="flex items-center justify-between">
                    <h3 className="text-sm font-bold text-slate-900">
                      {mod.title}
                    </h3>
                    <span className="px-2 py-0.5 bg-amber-100 text-amber-900 text-[10px] font-bold rounded-md">
                      Mock Test Included
                    </span>
                  </div>
                  <p className="text-xs text-slate-600">{mod.description}</p>
                  <div className="pt-2 text-[11px] text-slate-500 font-medium">
                    {mod.lessons.length} Lessons • Sequential Unlocking
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column (1/3 width): What You Will Learn & Requirements */}
        <div className="space-y-6">
          {course.what_you_will_learn && (
            <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-xs space-y-3">
              <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider text-blue-700">
                What You Will Learn
              </h3>
              <p className="text-xs text-slate-600 whitespace-pre-line leading-relaxed">
                {course.what_you_will_learn}
              </p>
            </div>
          )}

          {course.requirements && (
            <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-xs space-y-2">
              <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider">
                Course Requirements
              </h3>
              <p className="text-xs text-slate-600">
                {course.requirements}
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
