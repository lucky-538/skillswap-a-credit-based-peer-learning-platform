import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  BookOpen, Users, Award, ArrowLeftRight, Sparkles, CheckCircle2,
  Clock, ArrowRight, Star, TrendingUp, PlayCircle, Filter, ShieldCheck,
  GraduationCap
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { enrollmentsApi, matchesApi, certificatesApi, swapsApi, coursesApi, academicApi } from '../services/api';
import { Enrollment, SmartMatchResult, Certificate, SwapRequest, Course, Category } from '../types';

export const Dashboard: React.FC = () => {
  const { user } = useAuth();

  const [myCourses, setMyCourses] = useState<Enrollment[]>([]);
  const [recommendedCourses, setRecommendedCourses] = useState<Course[]>([]);
  const [matchData, setMatchData] = useState<SmartMatchResult | null>(null);
  const [certificates, setCertificates] = useState<Certificate[]>([]);
  const [pendingRequests, setPendingRequests] = useState<SwapRequest[]>([]);
  const [allCourses, setAllCourses] = useState<Course[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedCatId, setSelectedCatId] = useState<number | ''>('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const [coursesRes, recRes, certsRes, matchesRes, requestsRes, catalogRes, catRes] = await Promise.all([
          enrollmentsApi.getMyCourses(),
          coursesApi.getRecommended().catch(() => ({ data: [] })),
          certificatesApi.getMyCertificates(),
          matchesApi.getSmartMatches(),
          swapsApi.getRequests({ type: 'incoming', status_filter: 'pending' }),
          coursesApi.getCourses(),
          academicApi.getCategories()
        ]);

        setMyCourses(coursesRes.data);
        setRecommendedCourses(recRes.data);
        setCertificates(certsRes.data);
        setMatchData(matchesRes.data);
        setPendingRequests(requestsRes.data);
        setAllCourses(catalogRes.data);
        setCategories(catRes.data);
      } catch (err) {
        console.error('Error fetching dashboard data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, []);

  const completedCount = myCourses.filter(c => c.status === 'completed').length;
  const filteredCatalogCourses = selectedCatId === ''
    ? allCourses
    : allCourses.filter(c => c.category_id === selectedCatId);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-fade-in">
      {/* Welcome Banner */}
      <div className="relative overflow-hidden bg-gradient-to-r from-blue-700 via-indigo-700 to-slate-900 rounded-3xl p-6 sm:p-8 text-white shadow-xl shadow-blue-900/10">
        <div className="relative z-10 flex flex-col md:flex-row md:items-center md:justify-between gap-6">
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white/10 backdrop-blur-xs text-blue-200 text-xs font-semibold mb-3">
              <Sparkles className="w-3.5 h-3.5" />
              Academic Year {user?.year || 3} • {user?.college || 'Campus Member'}
            </div>
            <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
              Welcome back, {user?.name?.split(' ')[0]} 👋
            </h1>
            <p className="mt-1 text-sm text-blue-100 max-w-xl">
              Ready to exchange skills with campus peers or master accredited multi-disciplinary curriculum?
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <Link
              to="/skills"
              className="inline-flex items-center px-4 py-2.5 bg-teal-400 hover:bg-teal-300 text-slate-950 font-bold text-xs sm:text-sm rounded-xl shadow-md transition-all"
            >
              <Sparkles className="w-4 h-4 mr-1.5" />
              Find Skill Matches
            </Link>
            <Link
              to="/courses"
              className="inline-flex items-center px-4 py-2.5 bg-white/10 hover:bg-white/20 text-white font-semibold text-xs sm:text-sm rounded-xl border border-white/20 transition-all"
            >
              <BookOpen className="w-4 h-4 mr-1.5" />
              Browse All Courses
            </Link>
          </div>
        </div>
      </div>

      {/* KPI Stats Grid */}
      <div className="grid grid-cols-2 lg:grid-cols-5 gap-4">
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-semibold uppercase">Courses Enrolled</span>
            <BookOpen className="w-4 h-4 text-blue-600" />
          </div>
          <div className="text-2xl font-black text-slate-900">{myCourses.length}</div>
          <div className="text-[11px] text-slate-500 mt-1">{completedCount} completed</div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-semibold uppercase">Certificates</span>
            <Award className="w-4 h-4 text-emerald-600" />
          </div>
          <div className="text-2xl font-black text-slate-900">{certificates.length}</div>
          <div className="text-[11px] text-emerald-600 font-medium mt-1">100% Verified</div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-semibold uppercase">Peer Matches</span>
            <Sparkles className="w-4 h-4 text-teal-600" />
          </div>
          <div className="text-2xl font-black text-slate-900">{matchData?.peers_found_count || 0}</div>
          <div className="text-[11px] text-teal-600 font-medium mt-1">Available today</div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-semibold uppercase">Swap Credits</span>
            <ArrowLeftRight className="w-4 h-4 text-indigo-600" />
          </div>
          <div className="text-2xl font-black text-slate-900">{user?.credits || 10}</div>
          <div className="text-[11px] text-indigo-600 font-medium mt-1">+5 per completed swap</div>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs col-span-2 lg:col-span-1">
          <div className="flex items-center justify-between text-slate-500 mb-2">
            <span className="text-xs font-semibold uppercase">Reputation</span>
            <Star className="w-4 h-4 text-amber-500 fill-amber-500" />
          </div>
          <div className="text-2xl font-black text-slate-900">{user?.reputation_score || 5.0} / 5.0</div>
          <div className="text-[11px] text-amber-600 font-medium mt-1">Student rating</div>
        </div>
      </div>

      {/* Pending Swap Requests Alert if any */}
      {pendingRequests.length > 0 && (
        <div className="p-4 bg-amber-50 border border-amber-200 rounded-2xl flex items-center justify-between">
          <div className="flex items-center gap-3 text-amber-900 text-sm">
            <ArrowLeftRight className="w-5 h-5 text-amber-600 shrink-0" />
            <span>You have <b>{pendingRequests.length} pending skill swap request(s)</b> waiting for your response.</span>
          </div>
          <Link
            to="/swap-requests"
            className="px-3.5 py-1.5 bg-amber-600 hover:bg-amber-700 text-white font-bold text-xs rounded-xl transition-colors"
          >
            Review Requests
          </Link>
        </div>
      )}

      {/* Main Dashboard Split View */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column (2/3 width): Continue Learning, Recommendations & Skill Matches */}
        <div className="lg:col-span-2 space-y-8">
          {/* Continue Learning Section */}
          <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-xs">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h2 className="text-lg font-bold text-slate-900">Continue Learning</h2>
                <p className="text-xs text-slate-500">Track your enrolled courses and module progression</p>
              </div>
              <Link to="/my-courses" className="text-xs font-bold text-blue-600 hover:text-blue-700 flex items-center">
                View All <ArrowRight className="w-3.5 h-3.5 ml-1" />
              </Link>
            </div>

            {loading ? (
              <div className="py-12 text-center text-slate-400 text-sm">Loading enrolled courses...</div>
            ) : myCourses.length === 0 ? (
              <div className="py-10 text-center bg-slate-50 rounded-2xl border border-dashed border-slate-200">
                <BookOpen className="w-10 h-10 text-slate-400 mx-auto mb-2" />
                <h4 className="text-sm font-bold text-slate-700">No active course enrollments</h4>
                <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
                  Explore our structured catalog across all faculties or fallback from skill search.
                </p>
                <Link
                  to="/courses"
                  className="mt-4 inline-flex items-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-xl transition-colors"
                >
                  Explore Course Catalog
                </Link>
              </div>
            ) : (
              <div className="space-y-4">
                {myCourses.slice(0, 3).map(item => (
                  <div
                    key={item.id}
                    className="p-4 rounded-2xl border border-slate-100 hover:border-slate-200 bg-slate-50/50 hover:bg-slate-50 transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-4"
                  >
                    <div className="flex items-center gap-3.5">
                      <div className="w-12 h-12 rounded-xl bg-blue-100 text-blue-700 flex items-center justify-center shrink-0">
                        <BookOpen className="w-6 h-6" />
                      </div>
                      <div>
                        <h4 className="text-sm font-bold text-slate-900">{item.course.title}</h4>
                        <div className="text-xs text-slate-500 mt-0.5">
                          {item.course.difficulty} • {item.course.duration_hours} Hours
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center gap-4">
                      <div className="w-32">
                        <div className="flex justify-between text-[11px] font-semibold text-slate-600 mb-1">
                          <span>Progress</span>
                          <span>{item.progress_percentage}%</span>
                        </div>
                        <div className="w-full h-2 bg-slate-200 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-blue-600 rounded-full transition-all duration-500"
                            style={{ width: `${item.progress_percentage}%` }}
                          ></div>
                        </div>
                      </div>

                      <Link
                        to={`/learn/${item.course_id}`}
                        className="px-3.5 py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-xl transition-colors flex items-center gap-1.5 shrink-0"
                      >
                        <PlayCircle className="w-4 h-4" />
                        Learn
                      </Link>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* PERSONALIZED RECOMMENDATIONS SECTION */}
          {recommendedCourses.length > 0 && (
            <div className="bg-gradient-to-tr from-indigo-50/70 via-blue-50/40 to-slate-50 p-6 rounded-3xl border border-indigo-100 shadow-xs space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <div className="inline-flex items-center gap-1 text-[11px] font-bold text-indigo-700 uppercase">
                    <Sparkles className="w-3.5 h-3.5" /> Tailored For You
                  </div>
                  <h3 className="text-base font-bold text-slate-900">Recommended For Your Degree & Wishlist</h3>
                </div>
                <Link to="/courses" className="text-xs font-bold text-indigo-600 hover:text-indigo-700">
                  Explore More →
                </Link>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3.5">
                {recommendedCourses.slice(0, 3).map(rec => (
                  <div key={rec.id} className="p-3.5 bg-white rounded-2xl border border-indigo-100/80 shadow-xs flex flex-col justify-between space-y-2">
                    <div>
                      <span className="text-[10px] font-bold text-indigo-600 uppercase">{rec.category?.name || 'Academic'}</span>
                      <h4 className="text-xs font-bold text-slate-900 mt-1 line-clamp-1">{rec.title}</h4>
                      <p className="text-[11px] text-slate-500 mt-0.5 line-clamp-2">{rec.description}</p>
                    </div>
                    <Link
                      to={`/courses/${rec.id}`}
                      className="mt-2 block w-full text-center py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-[11px] rounded-xl transition-colors"
                    >
                      Start Course
                    </Link>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* EXPLORE COURSES BY ACADEMIC DISCIPLINE */}
          <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-xs space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div>
                <div className="inline-flex items-center gap-1 text-xs font-bold text-blue-600 uppercase mb-0.5">
                  <BookOpen className="w-3.5 h-3.5" /> University Curriculum Catalog
                </div>
                <h2 className="text-lg font-bold text-slate-900">Registered Courses & Academic Subjects</h2>
              </div>
              <Link to="/courses" className="text-xs font-bold text-blue-600 hover:text-blue-700 flex items-center">
                Full Catalog ({allCourses.length}) <ArrowRight className="w-3.5 h-3.5 ml-1" />
              </Link>
            </div>

            {/* Category Filter Pills */}
            <div className="flex flex-wrap items-center gap-2 pt-1 border-t border-slate-100">
              <button
                onClick={() => setSelectedCatId('')}
                className={`px-3 py-1.5 text-xs font-bold rounded-xl transition-colors ${
                  selectedCatId === ''
                    ? 'bg-blue-600 text-white shadow-xs'
                    : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                }`}
              >
                All Faculties ({allCourses.length})
              </button>
              {categories.map(cat => (
                <button
                  key={cat.id}
                  onClick={() => setSelectedCatId(cat.id)}
                  className={`px-3 py-1.5 text-xs font-bold rounded-xl transition-colors ${
                    selectedCatId === cat.id
                      ? 'bg-blue-600 text-white shadow-xs'
                      : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
                  }`}
                >
                  {cat.name}
                </button>
              ))}
            </div>

            {/* Course Grid in Dashboard */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
              {filteredCatalogCourses.slice(0, 4).map(c => (
                <div
                  key={c.id}
                  className="p-4 rounded-2xl border border-slate-200 bg-slate-50/50 hover:bg-slate-50 hover:border-slate-300 transition-all flex flex-col justify-between space-y-3"
                >
                  <div>
                    <div className="flex items-center justify-between text-[10px] font-bold text-blue-600 uppercase">
                      <span>{c.category?.name || 'Academic Course'}</span>
                      <span className="px-2 py-0.5 bg-slate-200 text-slate-800 rounded-md">{c.difficulty}</span>
                    </div>

                    <h4 className="text-sm font-bold text-slate-900 mt-1.5 line-clamp-1">{c.title}</h4>
                    <p className="text-xs text-slate-600 mt-1 line-clamp-2">{c.description}</p>
                  </div>

                  <div className="pt-2 border-t border-slate-200 flex items-center justify-between">
                    <span className="text-[11px] text-slate-500 flex items-center gap-1 font-medium">
                      <Clock className="w-3 h-3" /> {c.duration_hours}h duration
                    </span>
                    <Link
                      to={`/courses/${c.id}`}
                      className="px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-xl transition-colors flex items-center gap-1"
                    >
                      View Syllabus <ArrowRight className="w-3 h-3" />
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Smart Match Highlights */}
          <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-xs">
            <div className="flex items-center justify-between mb-4">
              <div>
                <div className="inline-flex items-center gap-1 text-xs font-bold text-teal-600 uppercase mb-0.5">
                  <Sparkles className="w-3.5 h-3.5" /> Peer Skill Swap
                </div>
                <h2 className="text-lg font-bold text-slate-900">Recommended Peer Matches</h2>
              </div>
              <Link to="/skills" className="text-xs font-bold text-blue-600 hover:text-blue-700 flex items-center">
                Match Hub <ArrowRight className="w-3.5 h-3.5 ml-1" />
              </Link>
            </div>

            {matchData?.matches && matchData.matches.length > 0 ? (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {matchData.matches.slice(0, 2).map((m, idx) => (
                  <div
                    key={idx}
                    className="p-4 rounded-2xl border border-teal-100 bg-teal-50/40 hover:bg-teal-50/70 transition-all space-y-3"
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <div className="w-8 h-8 rounded-full bg-teal-600 text-white font-bold flex items-center justify-center text-xs">
                          {m.user.name.charAt(0)}
                        </div>
                        <div>
                          <div className="text-xs font-bold text-slate-900">{m.user.name}</div>
                          <div className="text-[10px] text-slate-500">{m.user.college}</div>
                        </div>
                      </div>

                      <span className={`px-2 py-0.5 text-[10px] font-bold rounded-full ${
                        m.match_type === 'direct_swap'
                          ? 'bg-emerald-100 text-emerald-800 border border-emerald-300'
                          : 'bg-blue-100 text-blue-800'
                      }`}>
                        {m.match_score}% Match
                      </span>
                    </div>

                    <div className="text-xs text-slate-700 space-y-1 bg-white p-2.5 rounded-xl border border-slate-100">
                      <div><span className="font-semibold text-teal-700">Teaches:</span> {m.teaches_skill}</div>
                      <div><span className="font-semibold text-slate-600">Wants:</span> {m.wants_to_learn}</div>
                    </div>

                    <Link
                      to="/skills"
                      className="block w-full text-center py-2 bg-teal-600 hover:bg-teal-700 text-white font-bold text-xs rounded-xl transition-colors"
                    >
                      Request Skill Swap
                    </Link>
                  </div>
                ))}
              </div>
            ) : (
              <div className="p-4 bg-slate-50 rounded-2xl text-center text-xs text-slate-500">
                Add skills you want to learn in your profile to trigger instant smart matchmaking!
                <div className="mt-2">
                  <Link to="/profile" className="font-bold text-blue-600 hover:text-blue-700">
                    Update Skills Wishlist →
                  </Link>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Right Column (1/3 width): Verified Credentials & Quick Actions */}
        <div className="space-y-6">
          {/* Verified Certificates Card */}
          <div className="bg-white rounded-3xl p-6 border border-slate-200 shadow-xs">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <Award className="w-5 h-5 text-emerald-600" />
                Earned Certificates
              </h3>
              <Link to="/certificates" className="text-xs font-bold text-blue-600">
                View ({certificates.length})
              </Link>
            </div>

            {certificates.length === 0 ? (
              <div className="py-6 text-center text-xs text-slate-500">
                Complete all course modules and pass the final exam ($\ge 70\%$) to earn your official credentials.
              </div>
            ) : (
              <div className="space-y-3">
                {certificates.slice(0, 2).map(cert => (
                  <div key={cert.id} className="p-3 bg-emerald-50/50 border border-emerald-100 rounded-2xl">
                    <div className="text-xs font-bold text-slate-900">{cert.course_title}</div>
                    <div className="text-[10px] text-emerald-700 font-mono mt-0.5">ID: {cert.certificate_id}</div>
                    <div className="text-[10px] text-slate-500 mt-1">Grade: {cert.grade}</div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Quick Shortcuts */}
          <div className="bg-slate-900 text-white rounded-3xl p-6 space-y-4 shadow-xl">
            <h3 className="text-sm font-bold tracking-wider uppercase text-blue-400">Platform Features</h3>
            <ul className="space-y-2.5 text-xs text-slate-300">
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-teal-400 shrink-0" />
                <span>100% Reciprocal Skill Swap algorithm</span>
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-teal-400 shrink-0" />
                <span>Automatic Fallback to course catalog</span>
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-teal-400 shrink-0" />
                <span>MCQ Mock Tests with 70% passing threshold</span>
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-teal-400 shrink-0" />
                <span>Sequential module unlocking logic</span>
              </li>
              <li className="flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-teal-400 shrink-0" />
                <span>Public tamper-evident certificate verification</span>
              </li>
            </ul>

            <Link
              to="/verify-certificate"
              className="block w-full text-center py-2.5 bg-white/10 hover:bg-white/20 border border-white/20 rounded-xl text-xs font-bold text-white transition-all"
            >
              Public Certificate Validator
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};
