import React, { useState, useEffect } from 'react';
import {
  Shield, Users, BookOpen, ArrowLeftRight, Award,
  CheckCircle2, XCircle, Search, ToggleLeft, ToggleRight,
  TrendingUp, Download, Eye, Plus, Trash2, Edit3, Clock,
  HelpCircle, Layers
} from 'lucide-react';
import { adminApi, coursesApi, academicApi } from '../services/api';
import { AdminStats, Certificate, User, Course, Category, Degree } from '../types';

export const AdminDashboard: React.FC = () => {
  const [stats, setStats] = useState<AdminStats | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [certificates, setCertificates] = useState<Certificate[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [degrees, setDegrees] = useState<Degree[]>([]);

  const [activeTab, setActiveTab] = useState<'stats' | 'courses' | 'users' | 'certificates'>('stats');
  const [userSearch, setUserSearch] = useState('');
  const [courseSearch, setCourseSearch] = useState('');
  const [loading, setLoading] = useState(true);

  // New Course Modal State
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newTitle, setNewTitle] = useState('');
  const [newCategoryId, setNewCategoryId] = useState<number | ''>('');
  const [newDegreeId, setNewDegreeId] = useState<number | ''>('');
  const [newDifficulty, setNewDifficulty] = useState('Beginner');
  const [newDuration, setNewDuration] = useState(20);
  const [newDescription, setNewDescription] = useState('');
  const [newWhatLearn, setNewWhatLearn] = useState('');
  const [newRequirements, setNewRequirements] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    loadAdminData();
  }, []);

  const loadAdminData = async () => {
    setLoading(true);
    try {
      const [statsRes, usersRes, certsRes, coursesRes, catsRes, degsRes] = await Promise.all([
        adminApi.getStats(),
        adminApi.getUsers(),
        adminApi.getCertificates(),
        coursesApi.getCourses(),
        academicApi.getCategories(),
        academicApi.getDegrees()
      ]);
      setStats(statsRes.data);
      setUsers(usersRes.data);
      setCertificates(certsRes.data);
      setCourses(coursesRes.data);
      setCategories(catsRes.data);
      setDegrees(degsRes.data);
      if (catsRes.data.length > 0) setNewCategoryId(catsRes.data[0].id);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleUserStatus = async (user: User) => {
    try {
      await adminApi.updateUserStatus(user.id, {
        is_active: !user.is_active
      });
      setUsers(prev => prev.map(u => u.id === user.id ? { ...u, is_active: !u.is_active } : u));
    } catch (e) {
      console.error(e);
    }
  };

  const handleCreateCourse = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTitle.trim() || !newCategoryId) return;

    setIsSubmitting(true);
    try {
      await coursesApi.createCourse({
        title: newTitle.trim(),
        category_id: Number(newCategoryId),
        degree_id: newDegreeId ? Number(newDegreeId) : undefined,
        difficulty: newDifficulty,
        duration_hours: Number(newDuration),
        description: newDescription.trim(),
        what_you_will_learn: newWhatLearn.trim(),
        requirements: newRequirements.trim() || 'None',
        instructor_name: 'SkillSwap Campus Faculty'
      });
      setShowCreateModal(false);
      setNewTitle('');
      setNewDescription('');
      setNewWhatLearn('');
      setNewRequirements('');
      await loadAdminData();
    } catch (e) {
      console.error('Failed to create course:', e);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDeleteCourse = async (id: number) => {
    if (!window.confirm('Are you sure you want to delete this course? This action cannot be undone.')) return;
    try {
      await coursesApi.deleteCourse(id);
      setCourses(prev => prev.filter(c => c.id !== id));
    } catch (e) {
      console.error(e);
    }
  };

  const filteredUsers = users.filter(u =>
    u.name.toLowerCase().includes(userSearch.toLowerCase()) ||
    u.email.toLowerCase().includes(userSearch.toLowerCase()) ||
    (u.college && u.college.toLowerCase().includes(userSearch.toLowerCase()))
  );

  const filteredCourses = courses.filter(c =>
    c.title.toLowerCase().includes(courseSearch.toLowerCase()) ||
    (c.category?.name && c.category.name.toLowerCase().includes(courseSearch.toLowerCase())) ||
    (c.degree?.name && c.degree.name.toLowerCase().includes(courseSearch.toLowerCase()))
  );

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-fade-in">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-100 text-amber-900 text-xs font-bold uppercase mb-2">
            <Shield className="w-3.5 h-3.5 text-amber-700" />
            Dean & Administrator Control Center
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Academic Operations & Governance
          </h1>
        </div>

        {activeTab === 'courses' && (
          <button
            onClick={() => setShowCreateModal(true)}
            className="inline-flex items-center px-4 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-xl shadow-md transition-all gap-1.5 shrink-0"
          >
            <Plus className="w-4 h-4" /> Create New Course
          </button>
        )}
      </div>

      {/* Tabs Switcher */}
      <div className="flex border-b border-slate-200 space-x-4">
        <button
          onClick={() => setActiveTab('stats')}
          className={`pb-3 text-sm font-bold border-b-2 transition-colors flex items-center gap-2 ${
            activeTab === 'stats'
              ? 'border-amber-600 text-amber-700'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <TrendingUp className="w-4 h-4" />
          Overview & KPI Metrics
        </button>

        <button
          onClick={() => setActiveTab('courses')}
          className={`pb-3 text-sm font-bold border-b-2 transition-colors flex items-center gap-2 ${
            activeTab === 'courses'
              ? 'border-blue-600 text-blue-700'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <BookOpen className="w-4 h-4" />
          Course Catalog ({courses.length})
        </button>

        <button
          onClick={() => setActiveTab('users')}
          className={`pb-3 text-sm font-bold border-b-2 transition-colors flex items-center gap-2 ${
            activeTab === 'users'
              ? 'border-amber-600 text-amber-700'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <Users className="w-4 h-4" />
          Students & Users ({users.length})
        </button>

        <button
          onClick={() => setActiveTab('certificates')}
          className={`pb-3 text-sm font-bold border-b-2 transition-colors flex items-center gap-2 ${
            activeTab === 'certificates'
              ? 'border-emerald-600 text-emerald-700'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <Award className="w-4 h-4" />
          Issued Certificates ({certificates.length})
        </button>
      </div>

      {loading ? (
        <div className="py-20 text-center text-sm text-slate-400">Loading admin operations...</div>
      ) : activeTab === 'stats' ? (
        /* STATS TAB */
        <div className="space-y-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-xs">
              <div className="text-xs font-bold text-slate-500 uppercase">Total Students</div>
              <div className="text-3xl font-black text-slate-900 mt-2">{stats?.total_students}</div>
              <div className="text-xs text-blue-600 font-semibold mt-1">Across 17 faculties</div>
            </div>

            <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-xs">
              <div className="text-xs font-bold text-slate-500 uppercase">Total Courses</div>
              <div className="text-3xl font-black text-slate-900 mt-2">{stats?.total_courses}</div>
              <div className="text-xs text-indigo-600 font-semibold mt-1">With modular mock tests</div>
            </div>

            <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-xs">
              <div className="text-xs font-bold text-slate-500 uppercase">Skill Swaps</div>
              <div className="text-3xl font-black text-slate-900 mt-2">{stats?.total_skill_swaps}</div>
              <div className="text-xs text-teal-600 font-semibold mt-1">Peer sessions completed</div>
            </div>

            <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-xs">
              <div className="text-xs font-bold text-slate-500 uppercase">Certificates Issued</div>
              <div className="text-3xl font-black text-slate-900 mt-2">{stats?.certificates_issued}</div>
              <div className="text-xs text-emerald-600 font-semibold mt-1">Verified records</div>
            </div>
          </div>

          <div className="bg-white p-8 rounded-3xl border border-slate-200 shadow-xs space-y-4">
            <h3 className="text-lg font-bold text-slate-900">Academic Infrastructure Summary</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-sm">
              <div className="p-4 bg-slate-50 rounded-2xl border border-slate-100">
                <div className="font-bold text-slate-800">Academic Faculties</div>
                <div className="text-xs text-slate-600 mt-1">
                  17 Categories covering Engineering, Arts, Commerce, Management, Science, Architecture, Design, UI/UX, AI, Languages
                </div>
              </div>

              <div className="p-4 bg-slate-50 rounded-2xl border border-slate-100">
                <div className="font-bold text-slate-800">Skills Matrix</div>
                <div className="text-xs text-slate-600 mt-1">
                  {stats?.total_skills} Standardized Campus Skills with Smart Matching
                </div>
              </div>

              <div className="p-4 bg-slate-50 rounded-2xl border border-slate-100">
                <div className="font-bold text-slate-800">Assessment Integrity</div>
                <div className="text-xs text-slate-600 mt-1">
                  Automatic MCQ evaluation with 70% threshold, progressive module unlocking & ReportLab PDF certificates
                </div>
              </div>
            </div>
          </div>
        </div>
      ) : activeTab === 'courses' ? (
        /* COURSE MANAGEMENT TAB */
        <div className="bg-white rounded-3xl border border-slate-200 shadow-xs overflow-hidden">
          <div className="p-6 border-b border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <h3 className="text-lg font-bold text-slate-900">Curriculum & Course Management</h3>
              <p className="text-xs text-slate-500">Add, edit, and oversee course syllabi, modules, and mock assessments.</p>
            </div>
            <div className="relative w-full sm:w-72">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type="text"
                value={courseSearch}
                onChange={(e) => setCourseSearch(e.target.value)}
                placeholder="Search courses..."
                className="w-full pl-9 pr-3 py-2 text-xs border border-slate-300 rounded-xl text-slate-900"
              />
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-500 uppercase tracking-wider font-bold border-b border-slate-200">
                <tr>
                  <th className="p-4">Course Title</th>
                  <th className="p-4">Faculty / Degree</th>
                  <th className="p-4">Level</th>
                  <th className="p-4">Duration</th>
                  <th className="p-4">Modules</th>
                  <th className="p-4">Enrollments</th>
                  <th className="p-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredCourses.map(c => (
                  <tr key={c.id} className="hover:bg-slate-50/50">
                    <td className="p-4">
                      <div className="font-bold text-slate-900">{c.title}</div>
                      <div className="text-slate-400 text-[11px] font-mono">slug: {c.slug}</div>
                    </td>
                    <td className="p-4 text-slate-700">
                      <div>{c.category?.name || 'Academic'}</div>
                      <div className="text-[10px] text-indigo-600 font-semibold">{c.degree?.name || 'All Degrees'}</div>
                    </td>
                    <td className="p-4">
                      <span className="px-2 py-0.5 bg-slate-100 text-slate-800 text-[10px] font-bold rounded-md uppercase">
                        {c.difficulty}
                      </span>
                    </td>
                    <td className="p-4 text-slate-600">{c.duration_hours}h</td>
                    <td className="p-4 font-bold text-slate-800">{c.modules_count || 0} Modules</td>
                    <td className="p-4 text-slate-700">{c.enrollment_count} Students</td>
                    <td className="p-4 text-right">
                      <button
                        onClick={() => handleDeleteCourse(c.id)}
                        className="p-1.5 text-slate-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                        title="Delete Course"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : activeTab === 'users' ? (
        /* USERS MANAGEMENT TAB */
        <div className="bg-white rounded-3xl border border-slate-200 shadow-xs overflow-hidden">
          <div className="p-6 border-b border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <h3 className="text-lg font-bold text-slate-900">Student Directory & Governance</h3>
            <div className="relative w-full sm:w-72">
              <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
              <input
                type="text"
                value={userSearch}
                onChange={(e) => setUserSearch(e.target.value)}
                placeholder="Search students by name or email..."
                className="w-full pl-9 pr-3 py-2 text-xs border border-slate-300 rounded-xl text-slate-900"
              />
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-500 uppercase tracking-wider font-bold border-b border-slate-200">
                <tr>
                  <th className="p-4">Student</th>
                  <th className="p-4">Role</th>
                  <th className="p-4">College / Branch</th>
                  <th className="p-4">Credits</th>
                  <th className="p-4">Status</th>
                  <th className="p-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredUsers.map(u => (
                  <tr key={u.id} className="hover:bg-slate-50/50">
                    <td className="p-4">
                      <div className="font-bold text-slate-900">{u.name}</div>
                      <div className="text-slate-400 font-mono text-[11px]">{u.email}</div>
                    </td>
                    <td className="p-4">
                      <span className={`px-2 py-0.5 text-[10px] font-bold rounded-md capitalize ${
                        u.role === 'admin' ? 'bg-amber-100 text-amber-800' : 'bg-blue-100 text-blue-800'
                      }`}>
                        {u.role}
                      </span>
                    </td>
                    <td className="p-4 text-slate-600">
                      <div>{u.college || '—'}</div>
                      <div className="text-[10px] text-slate-400">{u.branch || 'General'} (Year {u.year || 1})</div>
                    </td>
                    <td className="p-4 font-bold text-slate-800">{u.credits}</td>
                    <td className="p-4">
                      <span className={`px-2 py-0.5 text-[10px] font-bold rounded-full ${
                        u.is_active ? 'bg-emerald-100 text-emerald-800' : 'bg-red-100 text-red-800'
                      }`}>
                        {u.is_active ? 'Active' : 'Deactivated'}
                      </span>
                    </td>
                    <td className="p-4 text-right">
                      {u.role !== 'admin' && (
                        <button
                          onClick={() => handleToggleUserStatus(u)}
                          className={`px-3 py-1 text-xs font-bold rounded-lg transition-colors ${
                            u.is_active
                              ? 'bg-red-50 text-red-700 hover:bg-red-100'
                              : 'bg-emerald-50 text-emerald-700 hover:bg-emerald-100'
                          }`}
                        >
                          {u.is_active ? 'Deactivate' : 'Activate'}
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ) : (
        /* CERTIFICATES TAB */
        <div className="bg-white rounded-3xl border border-slate-200 shadow-xs overflow-hidden">
          <div className="p-6 border-b border-slate-200">
            <h3 className="text-lg font-bold text-slate-900">Official Certificate Ledger</h3>
            <p className="text-xs text-slate-500">All issued digital completion credentials with verifiable identifiers.</p>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 text-slate-500 uppercase tracking-wider font-bold border-b border-slate-200">
                <tr>
                  <th className="p-4">Certificate ID</th>
                  <th className="p-4">Student Graduate</th>
                  <th className="p-4">Course Title</th>
                  <th className="p-4">Issue Date</th>
                  <th className="p-4">Grade</th>
                  <th className="p-4 text-right">Verification</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {certificates.map(c => (
                  <tr key={c.id} className="hover:bg-slate-50/50">
                    <td className="p-4 font-mono font-bold text-blue-700">{c.certificate_id}</td>
                    <td className="p-4 font-bold text-slate-900">{c.student_name}</td>
                    <td className="p-4 text-slate-700">{c.course_title}</td>
                    <td className="p-4 text-slate-500">
                      {c.issue_date ? new Date(c.issue_date).toLocaleDateString() : '—'}
                    </td>
                    <td className="p-4 font-bold text-emerald-700">{c.grade}</td>
                    <td className="p-4 text-right">
                      <a
                        href={`/verify-certificate/${c.certificate_id}`}
                        target="_blank"
                        rel="noreferrer"
                        className="px-2.5 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold rounded-lg inline-flex items-center gap-1"
                      >
                        <Eye className="w-3.5 h-3.5" /> Registry
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* CREATE COURSE MODAL */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4 animate-fade-in overflow-y-auto">
          <div className="bg-white rounded-3xl max-w-2xl w-full p-6 sm:p-8 shadow-2xl border border-slate-200 relative my-8">
            <div className="flex items-center justify-between pb-3 border-b border-slate-100 mb-4">
              <h3 className="text-lg font-bold text-slate-900">Add New Academic Course</h3>
              <button
                onClick={() => setShowCreateModal(false)}
                className="text-slate-400 hover:text-slate-700 text-sm font-bold"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleCreateCourse} className="space-y-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Course Title</label>
                <input
                  type="text"
                  required
                  value={newTitle}
                  onChange={(e) => setNewTitle(e.target.value)}
                  placeholder="e.g. Cloud Architecture & Kubernetes Masterclass"
                  className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-xl text-slate-900"
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Academic Category</label>
                  <select
                    required
                    value={newCategoryId}
                    onChange={(e) => setNewCategoryId(Number(e.target.value))}
                    className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-xl text-slate-900"
                  >
                    {categories.map(c => (
                      <option key={c.id} value={c.id}>{c.name}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Degree Program</label>
                  <select
                    value={newDegreeId}
                    onChange={(e) => setNewDegreeId(e.target.value ? Number(e.target.value) : '')}
                    className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-xl text-slate-900"
                  >
                    <option value="">General (All Degrees)</option>
                    {degrees.map(d => (
                      <option key={d.id} value={d.id}>{d.name} ({d.code})</option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Difficulty Level</label>
                  <select
                    value={newDifficulty}
                    onChange={(e) => setNewDifficulty(e.target.value)}
                    className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-xl text-slate-900"
                  >
                    <option value="Beginner">Beginner</option>
                    <option value="Intermediate">Intermediate</option>
                    <option value="Advanced">Advanced</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Duration (Hours)</label>
                  <input
                    type="number"
                    min={1}
                    value={newDuration}
                    onChange={(e) => setNewDuration(Number(e.target.value))}
                    className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-xl text-slate-900"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Course Description</label>
                <textarea
                  rows={3}
                  required
                  value={newDescription}
                  onChange={(e) => setNewDescription(e.target.value)}
                  placeholder="Comprehensive description of the curriculum..."
                  className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-xl text-slate-900"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase mb-1">What You Will Learn (Bullet points)</label>
                <textarea
                  rows={2}
                  value={newWhatLearn}
                  onChange={(e) => setNewWhatLearn(e.target.value)}
                  placeholder="• Concept A&#10;• Concept B&#10;• Concept C"
                  className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-xl text-slate-900"
                />
              </div>

              <div className="flex items-center justify-end gap-3 pt-3 border-t border-slate-100">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="px-4 py-2 text-xs font-bold text-slate-600 hover:bg-slate-100 rounded-xl"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting}
                  className="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold rounded-xl shadow-md transition-all"
                >
                  {isSubmitting ? 'Creating...' : 'Create Course'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
