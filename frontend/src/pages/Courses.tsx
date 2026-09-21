import React, { useState, useEffect } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import {
  Search, BookOpen, Star, Clock, Award, Filter,
  ArrowRight, ShieldCheck, Sparkles, GraduationCap,
  Layers, CheckCircle2, RotateCcw
} from 'lucide-react';
import { coursesApi, academicApi } from '../services/api';
import { Course, Category, Degree, Branch } from '../types';

export const Courses: React.FC = () => {
  const [searchParams] = useSearchParams();

  const [courses, setCourses] = useState<Course[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [degrees, setDegrees] = useState<Degree[]>([]);
  const [branches, setBranches] = useState<Branch[]>([]);

  // Filter states
  const [selectedCatId, setSelectedCatId] = useState<number | ''>(
    searchParams.get('category') ? Number(searchParams.get('category')) : ''
  );
  const [selectedDegreeId, setSelectedDegreeId] = useState<number | ''>(
    searchParams.get('degree') ? Number(searchParams.get('degree')) : ''
  );
  const [selectedBranchId, setSelectedBranchId] = useState<number | ''>('');
  const [selectedDifficulty, setSelectedDifficulty] = useState<string>('');
  const [search, setSearch] = useState(searchParams.get('search') || '');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Load academic taxonomy
    academicApi.getCategories().then(res => setCategories(res.data)).catch(() => {});
    academicApi.getDegrees().then(res => setDegrees(res.data)).catch(() => {});
  }, []);

  useEffect(() => {
    if (selectedDegreeId) {
      academicApi.getBranches(Number(selectedDegreeId))
        .then(res => setBranches(res.data))
        .catch(() => setBranches([]));
    } else {
      setBranches([]);
      setSelectedBranchId('');
    }
  }, [selectedDegreeId]);

  useEffect(() => {
    fetchCourses();
  }, [selectedCatId, selectedDegreeId, selectedBranchId, selectedDifficulty]);

  const fetchCourses = async () => {
    setLoading(true);
    try {
      const res = await coursesApi.getCourses({
        category_id: selectedCatId ? Number(selectedCatId) : undefined,
        degree_id: selectedDegreeId ? Number(selectedDegreeId) : undefined,
        branch_id: selectedBranchId ? Number(selectedBranchId) : undefined,
        difficulty: selectedDifficulty || undefined,
        search: search.trim() || undefined
      });
      setCourses(res.data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    fetchCourses();
  };

  const handleClearFilters = () => {
    setSelectedCatId('');
    setSelectedDegreeId('');
    setSelectedBranchId('');
    setSelectedDifficulty('');
    setSearch('');
    setTimeout(() => fetchCourses(), 50);
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-fade-in">
      {/* Catalog Hero Banner */}
      <div className="bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 rounded-3xl p-8 text-white shadow-xl shadow-blue-950/20 flex flex-col md:flex-row items-center justify-between gap-6">
        <div className="space-y-2 max-w-2xl text-center md:text-left">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-blue-500/20 text-blue-300 text-xs font-semibold">
            <BookOpen className="w-3.5 h-3.5" />
            Accredited Multi-Disciplinary Curriculum
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight">
            Explore University Courses & Certifications
          </h1>
          <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
            Master engineering, management, commerce, arts, sciences, architecture, design, UI/UX, and language curricula with progressive mock tests and verified completion credentials.
          </p>
        </div>

        <Link
          to="/skills"
          className="inline-flex items-center justify-center px-5 py-3 bg-teal-400 hover:bg-teal-300 text-slate-950 font-bold text-xs rounded-xl shadow-md transition-all gap-1.5 shrink-0"
        >
          <Sparkles className="w-4 h-4" />
          Want Peer Tutoring Instead?
        </Link>
      </div>

      {/* SEARCH & ADVANCED FILTER CONTROLS */}
      <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-xs space-y-5">
        {/* Search Bar */}
        <form onSubmit={handleSearchSubmit} className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search course title, subject, technology, syllabus topic..."
              className="w-full pl-10 pr-4 py-2.5 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 text-slate-900"
            />
          </div>
          <button
            type="submit"
            className="px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-xl shadow-sm transition-colors shrink-0"
          >
            Search Catalog
          </button>
        </form>

        {/* Dropdowns Row: Degree, Branch, Level */}
        <div className="grid grid-cols-1 sm:grid-cols-4 gap-3 pt-2 border-t border-slate-100">
          <div>
            <label className="block text-[11px] font-bold text-slate-600 uppercase mb-1">Degree Program</label>
            <select
              value={selectedDegreeId}
              onChange={(e) => setSelectedDegreeId(e.target.value ? Number(e.target.value) : '')}
              className="w-full px-3 py-2 text-xs border border-slate-300 rounded-xl bg-white text-slate-900 font-medium"
            >
              <option value="">All Degree Programs</option>
              {degrees.map(d => (
                <option key={d.id} value={d.id}>{d.name} ({d.code})</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-[11px] font-bold text-slate-600 uppercase mb-1">Branch / Specialization</label>
            <select
              value={selectedBranchId}
              onChange={(e) => setSelectedBranchId(e.target.value ? Number(e.target.value) : '')}
              disabled={!selectedDegreeId || branches.length === 0}
              className="w-full px-3 py-2 text-xs border border-slate-300 rounded-xl bg-white text-slate-900 font-medium disabled:opacity-50"
            >
              <option value="">All Branches</option>
              {branches.map(b => (
                <option key={b.id} value={b.id}>{b.name}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-[11px] font-bold text-slate-600 uppercase mb-1">Difficulty Level</label>
            <select
              value={selectedDifficulty}
              onChange={(e) => setSelectedDifficulty(e.target.value)}
              className="w-full px-3 py-2 text-xs border border-slate-300 rounded-xl bg-white text-slate-900 font-medium"
            >
              <option value="">All Levels</option>
              <option value="Beginner">Beginner</option>
              <option value="Intermediate">Intermediate</option>
              <option value="Advanced">Advanced</option>
            </select>
          </div>

          <div className="flex items-end">
            <button
              onClick={handleClearFilters}
              type="button"
              className="w-full py-2 text-xs font-bold text-slate-600 hover:text-slate-900 bg-slate-100 hover:bg-slate-200 rounded-xl transition-colors flex items-center justify-center gap-1"
            >
              <RotateCcw className="w-3.5 h-3.5" /> Reset Filters
            </button>
          </div>
        </div>

        {/* Category Pills */}
        <div className="flex flex-wrap items-center gap-2 pt-2 border-t border-slate-100">
          <button
            onClick={() => setSelectedCatId('')}
            className={`px-3 py-1.5 text-xs font-bold rounded-xl transition-colors ${
              selectedCatId === ''
                ? 'bg-blue-600 text-white shadow-xs'
                : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
            }`}
          >
            All Categories ({courses.length})
          </button>
          {categories.map(c => (
            <button
              key={c.id}
              onClick={() => setSelectedCatId(c.id)}
              className={`px-3 py-1.5 text-xs font-bold rounded-xl transition-colors ${
                selectedCatId === c.id
                  ? 'bg-blue-600 text-white shadow-xs'
                  : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
              }`}
            >
              {c.name}
            </button>
          ))}
        </div>
      </div>

      {/* COURSE CARDS GRID */}
      {loading ? (
        <div className="py-20 text-center text-sm text-slate-400">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
          Loading multi-disciplinary course catalog...
        </div>
      ) : courses.length === 0 ? (
        <div className="py-16 text-center bg-white rounded-3xl border border-dashed border-slate-200 shadow-xs space-y-3">
          <BookOpen className="w-12 h-12 text-slate-300 mx-auto" />
          <h3 className="text-base font-bold text-slate-700">No courses match the selected filters</h3>
          <p className="text-xs text-slate-500 max-w-md mx-auto">
            Try resetting the degree, branch, or category filters to explore the entire catalog.
          </p>
          <button
            onClick={handleClearFilters}
            className="px-4 py-2 bg-blue-600 text-white text-xs font-bold rounded-xl"
          >
            View All Courses
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {courses.map(c => (
            <div
              key={c.id}
              className="bg-white rounded-3xl border border-slate-200 overflow-hidden shadow-xs hover:shadow-lg transition-all flex flex-col justify-between group"
            >
              <div>
                <div className="h-44 bg-slate-900 overflow-hidden relative">
                  {c.thumbnail_url ? (
                    <img
                      src={c.thumbnail_url}
                      alt={c.title}
                      className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center text-white">
                      <BookOpen className="w-12 h-12 text-blue-400" />
                    </div>
                  )}
                  <span className="absolute top-3 left-3 px-2.5 py-1 bg-slate-900/80 backdrop-blur-xs text-white text-[10px] font-bold rounded-lg uppercase">
                    {c.difficulty}
                  </span>
                  <span className="absolute bottom-3 right-3 px-2 py-0.5 bg-amber-500 text-white text-xs font-bold rounded-md flex items-center gap-1">
                    <Star className="w-3 h-3 fill-white" />
                    {c.rating}
                  </span>
                </div>

                <div className="p-6 space-y-2">
                  <div className="flex items-center justify-between gap-2 text-[10px] font-bold">
                    <span className="text-blue-600 uppercase tracking-wider">
                      {c.category?.name || 'Academic Faculty'}
                    </span>
                    {c.degree && (
                      <span className="px-2 py-0.5 bg-indigo-50 text-indigo-700 rounded-md border border-indigo-100">
                        {c.degree.code}
                      </span>
                    )}
                  </div>

                  <h3 className="text-base font-bold text-slate-900 group-hover:text-blue-600 transition-colors line-clamp-1">
                    {c.title}
                  </h3>

                  <p className="text-xs text-slate-600 line-clamp-2 leading-relaxed">
                    {c.description}
                  </p>

                  <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                    <span className="flex items-center gap-1">
                      <Clock className="w-3.5 h-3.5" /> {c.duration_hours}h duration
                    </span>
                    <span className="flex items-center gap-1 text-emerald-700 font-semibold">
                      <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" /> Certificate
                    </span>
                  </div>
                </div>
              </div>

              <div className="px-6 pb-6 pt-2">
                <Link
                  to={`/courses/${c.id}`}
                  className="w-full py-2.5 bg-blue-50 hover:bg-blue-600 text-blue-700 hover:text-white font-bold text-xs rounded-xl transition-all flex items-center justify-center gap-1.5"
                >
                  View Syllabus & Enroll
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
