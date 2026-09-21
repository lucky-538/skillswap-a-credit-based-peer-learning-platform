import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { BookOpen, PlayCircle, Award, CheckCircle2, Clock } from 'lucide-react';
import { enrollmentsApi } from '../services/api';
import { Enrollment } from '../types';

export const MyCourses: React.FC = () => {
  const [enrollments, setEnrollments] = useState<Enrollment[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    enrollmentsApi.getMyCourses()
      .then(res => setEnrollments(res.data))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-fade-in">
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          My Enrolled Courses & Learning Progress
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1">
          Continue your modules, pass mock assessments, and unlock course completion certificates.
        </p>
      </div>

      {loading ? (
        <div className="py-20 text-center text-sm text-slate-400">Loading your courses...</div>
      ) : enrollments.length === 0 ? (
        <div className="py-16 text-center bg-white rounded-3xl border border-dashed border-slate-200 shadow-xs space-y-4">
          <BookOpen className="w-12 h-12 text-slate-300 mx-auto" />
          <h3 className="text-base font-bold text-slate-700">No course enrollments yet</h3>
          <p className="text-xs text-slate-500 max-w-md mx-auto">
            Browse our multi-disciplinary courses or find a course through smart skill matching.
          </p>
          <Link
            to="/courses"
            className="inline-flex items-center px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-xl shadow-md transition-colors"
          >
            Explore Course Catalog
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {enrollments.map(item => {
            const isCompleted = item.status === 'completed';

            return (
              <div
                key={item.id}
                className="bg-white rounded-3xl border border-slate-200 overflow-hidden shadow-xs hover:shadow-md transition-all flex flex-col justify-between"
              >
                <div>
                  <div className="h-40 bg-slate-900 overflow-hidden relative">
                    {item.course.thumbnail_url ? (
                      <img src={item.course.thumbnail_url} alt={item.course.title} className="w-full h-full object-cover" />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center text-white">
                        <BookOpen className="w-10 h-10 text-blue-400" />
                      </div>
                    )}
                    <span className={`absolute top-3 left-3 px-2.5 py-1 text-[10px] font-bold rounded-lg uppercase ${
                      isCompleted ? 'bg-emerald-600 text-white' : 'bg-blue-600 text-white'
                    }`}>
                      {item.status.toUpperCase()}
                    </span>
                  </div>

                  <div className="p-6 space-y-3">
                    <h3 className="text-base font-bold text-slate-900 line-clamp-1">
                      {item.course.title}
                    </h3>

                    <div className="space-y-1.5">
                      <div className="flex justify-between text-xs font-semibold text-slate-700">
                        <span>Course Progress</span>
                        <span>{item.progress_percentage}%</span>
                      </div>
                      <div className="w-full h-2.5 bg-slate-100 rounded-full overflow-hidden">
                        <div
                          className={`h-full rounded-full transition-all duration-500 ${
                            isCompleted ? 'bg-emerald-600' : 'bg-blue-600'
                          }`}
                          style={{ width: `${item.progress_percentage}%` }}
                        ></div>
                      </div>
                    </div>

                    <div className="text-xs text-slate-500 flex items-center justify-between pt-2 border-t border-slate-100">
                      <span>{item.course.difficulty}</span>
                      <span className="flex items-center gap-1"><Clock className="w-3.5 h-3.5" /> {item.course.duration_hours}h</span>
                    </div>
                  </div>
                </div>

                <div className="px-6 pb-6 pt-2">
                  <Link
                    to={`/learn/${item.course_id}`}
                    className="w-full py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-xl shadow-xs transition-colors flex items-center justify-center gap-2"
                  >
                    <PlayCircle className="w-4 h-4" />
                    {isCompleted ? 'Review Modules' : 'Continue Learning'}
                  </Link>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
