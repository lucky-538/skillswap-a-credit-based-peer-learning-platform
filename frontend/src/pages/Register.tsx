import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ArrowLeftRight, Lock, Mail, User, Building, GraduationCap, AlertCircle, ArrowRight, Loader2 } from 'lucide-react';
import { authApi, academicApi } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { Category, Degree, Branch } from '../types';

export const Register: React.FC = () => {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [college, setCollege] = useState('DRK College of Engineering and Technology');
  const [year, setYear] = useState<number>(3);
  const [bio, setBio] = useState('');

  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<number | ''>('');
  const [degrees, setDegrees] = useState<Degree[]>([]);
  const [selectedDegree, setSelectedDegree] = useState<number | ''>('');
  const [branches, setBranches] = useState<Branch[]>([]);
  const [selectedBranch, setSelectedBranch] = useState<number | ''>('');

  const [loadingTaxonomy, setLoadingTaxonomy] = useState(true);
  const [loadingDegrees, setLoadingDegrees] = useState(false);
  const [loadingBranches, setLoadingBranches] = useState(false);

  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  // Load all faculties / categories on mount
  useEffect(() => {
    setLoadingTaxonomy(true);
    academicApi.getCategories()
      .then(res => {
        const cats = res.data;
        setCategories(cats);
        if (cats.length > 0) {
          // Default to Engineering & Technology or the first category
          const engCat = cats.find((c: Category) => c.name.toLowerCase().includes('engineering')) || cats[0];
          setSelectedCategory(engCat.id);
        }
      })
      .catch(err => {
        console.error('Failed to load academic categories:', err);
      })
      .finally(() => {
        setLoadingTaxonomy(false);
      });
  }, []);

  // When Category changes, fetch its degrees
  useEffect(() => {
    if (selectedCategory) {
      setLoadingDegrees(true);
      academicApi.getDegrees(Number(selectedCategory))
        .then(res => {
          const degs = res.data;
          setDegrees(degs);
          if (degs.length > 0) {
            setSelectedDegree(degs[0].id);
          } else {
            setSelectedDegree('');
            setBranches([]);
            setSelectedBranch('');
          }
        })
        .catch(err => {
          console.error('Failed to load degrees:', err);
          setDegrees([]);
          setSelectedDegree('');
        })
        .finally(() => {
          setLoadingDegrees(false);
        });
    }
  }, [selectedCategory]);

  // When Degree changes, fetch its branches
  useEffect(() => {
    if (selectedDegree) {
      setLoadingBranches(true);
      academicApi.getBranches(Number(selectedDegree))
        .then(res => {
          const brs = res.data;
          setBranches(brs);
          if (brs.length > 0) {
            setSelectedBranch(brs[0].id);
          } else {
            setSelectedBranch('');
          }
        })
        .catch(err => {
          console.error('Failed to load branches:', err);
          setBranches([]);
          setSelectedBranch('');
        })
        .finally(() => {
          setLoadingBranches(false);
        });
    }
  }, [selectedDegree]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (password.length < 6) {
      setError('Password must be at least 6 characters long');
      return;
    }

    setLoading(true);

    const selectedBranchObj = branches.find(b => b.id === Number(selectedBranch));

    try {
      await authApi.register({
        name,
        email,
        password,
        college,
        degree_id: selectedDegree ? Number(selectedDegree) : null,
        branch_id: selectedBranch ? Number(selectedBranch) : null,
        branch: selectedBranchObj ? selectedBranchObj.name : 'General',
        year: Number(year),
        bio
      });

      // Auto-login newly registered student
      try {
        const loginRes = await authApi.login({ email, password });
        login(loginRes.data.access_token, loginRes.data.user);
        navigate('/dashboard', { replace: true });
      } catch (loginErr) {
        // Fallback to login screen with success banner
        navigate('/login', { state: { message: 'Registration successful! Please sign in with your credentials.' } });
      }
    } catch (err: any) {
      if (!err.response) {
        setError('Cannot connect to backend server. Please verify the FastAPI backend is running on port 8000.');
      } else if (err.response.data?.detail) {
        if (typeof err.response.data.detail === 'string') {
          setError(err.response.data.detail);
        } else if (Array.isArray(err.response.data.detail)) {
          const detailMsg = err.response.data.detail.map((d: any) => `${d.loc ? d.loc[d.loc.length - 1] + ': ' : ''}${d.msg}`).join(', ');
          setError(detailMsg || 'Please provide valid registration details.');
        } else {
          setError('Failed to create student account. Please check your details.');
        }
      } else {
        setError('Failed to create student account. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-xl">
        <div className="flex justify-center">
          <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-blue-700 to-indigo-600 flex items-center justify-center text-white shadow-lg shadow-blue-500/30">
            <ArrowLeftRight className="w-6 h-6" />
          </div>
        </div>
        <h2 className="mt-4 text-center text-2xl sm:text-3xl font-extrabold text-slate-900">
          Join SkillSwap Campus
        </h2>
        <p className="mt-2 text-center text-xs text-slate-600">
          Open to students from all degrees, faculties, and universities
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-xl px-4">
        <div className="bg-white py-8 px-6 sm:px-10 shadow-xl shadow-slate-200/50 rounded-3xl border border-slate-200">
          {error && (
            <div className="mb-6 p-3.5 bg-red-50 border border-red-200 rounded-xl flex items-start gap-2 text-xs text-red-700">
              <AlertCircle className="w-4 h-4 text-red-600 shrink-0 mt-0.5" />
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
                  Full Name *
                </label>
                <div className="relative rounded-xl shadow-xs">
                  <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                    <User className="w-4 h-4" />
                  </div>
                  <input
                    type="text"
                    required
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Ananya Roy"
                    className="block w-full pl-10 pr-3.5 py-2 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-slate-900"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
                  Email Address *
                </label>
                <div className="relative rounded-xl shadow-xs">
                  <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                    <Mail className="w-4 h-4" />
                  </div>
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="student@college.edu"
                    className="block w-full pl-10 pr-3.5 py-2 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-slate-900"
                  />
                </div>
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
                Password *
              </label>
              <div className="relative rounded-xl shadow-xs">
                <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                  <Lock className="w-4 h-4" />
                </div>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="At least 6 characters"
                  className="block w-full pl-10 pr-3.5 py-2 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-slate-900"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
                  College / University *
                </label>
                <div className="relative rounded-xl shadow-xs">
                  <div className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-slate-400">
                    <Building className="w-4 h-4" />
                  </div>
                  <input
                    type="text"
                    required
                    value={college}
                    onChange={(e) => setCollege(e.target.value)}
                    placeholder="University Name"
                    className="block w-full pl-10 pr-3.5 py-2 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-slate-900"
                  />
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
                  Academic Year
                </label>
                <select
                  value={year}
                  onChange={(e) => setYear(Number(e.target.value))}
                  className="block w-full px-3.5 py-2 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 text-slate-900"
                >
                  <option value={1}>1st Year (Freshman)</option>
                  <option value={2}>2nd Year (Sophomore)</option>
                  <option value={3}>3rd Year (Junior)</option>
                  <option value={4}>4th Year (Senior)</option>
                  <option value={5}>Postgraduate / Master's</option>
                </select>
              </div>
            </div>

            {/* Academic Field Dropdowns */}
            <div className="p-4 bg-slate-50 rounded-2xl border border-slate-200 space-y-3">
              <div className="text-xs font-bold text-slate-700 uppercase flex items-center justify-between">
                <div className="flex items-center gap-1.5">
                  <GraduationCap className="w-4 h-4 text-blue-600" />
                  <span>Educational Discipline & Major *</span>
                </div>
                {(loadingTaxonomy || loadingDegrees || loadingBranches) && (
                  <div className="flex items-center gap-1 text-[11px] text-blue-600 font-medium animate-pulse">
                    <Loader2 className="w-3 h-3 animate-spin" />
                    <span>Updating options...</span>
                  </div>
                )}
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div>
                  <label className="block text-[11px] font-semibold text-slate-600 mb-1">Faculty / Category</label>
                  <select
                    value={selectedCategory}
                    onChange={(e) => setSelectedCategory(Number(e.target.value))}
                    disabled={loadingTaxonomy}
                    className="block w-full px-2.5 py-2 text-xs font-medium border border-slate-300 rounded-xl bg-white text-slate-900 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all disabled:opacity-50"
                  >
                    {categories.length === 0 ? (
                      <option value="">Loading faculties...</option>
                    ) : (
                      categories.map(c => (
                        <option key={c.id} value={c.id}>{c.name}</option>
                      ))
                    )}
                  </select>
                </div>

                <div>
                  <label className="block text-[11px] font-semibold text-slate-600 mb-1">Degree Program</label>
                  <select
                    value={selectedDegree}
                    onChange={(e) => setSelectedDegree(Number(e.target.value))}
                    disabled={loadingDegrees || degrees.length === 0}
                    className="block w-full px-2.5 py-2 text-xs font-medium border border-slate-300 rounded-xl bg-white text-slate-900 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all disabled:opacity-50"
                  >
                    {loadingDegrees ? (
                      <option value="">Loading degrees...</option>
                    ) : degrees.length === 0 ? (
                      <option value="">No degree programs found</option>
                    ) : (
                      degrees.map(d => (
                        <option key={d.id} value={d.id}>{d.name}</option>
                      ))
                    )}
                  </select>
                </div>

                <div>
                  <label className="block text-[11px] font-semibold text-slate-600 mb-1">Branch / Specialization</label>
                  <select
                    value={selectedBranch}
                    onChange={(e) => setSelectedBranch(Number(e.target.value))}
                    disabled={loadingBranches || branches.length === 0}
                    className="block w-full px-2.5 py-2 text-xs font-medium border border-slate-300 rounded-xl bg-white text-slate-900 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all disabled:opacity-50"
                  >
                    {loadingBranches ? (
                      <option value="">Loading branches...</option>
                    ) : branches.length === 0 ? (
                      <option value="">General Specialization</option>
                    ) : (
                      branches.map(b => (
                        <option key={b.id} value={b.id}>{b.name}</option>
                      ))
                    )}
                  </select>
                </div>
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
                Short Bio / Learning Goals
              </label>
              <textarea
                rows={2}
                value={bio}
                onChange={(e) => setBio(e.target.value)}
                placeholder="What topics are you excited to teach or learn?"
                className="block w-full px-3.5 py-2 text-sm border border-slate-300 rounded-xl focus:ring-2 focus:ring-blue-500 text-slate-900"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full mt-2 py-3 px-4 text-sm font-bold text-white bg-blue-600 hover:bg-blue-700 rounded-xl shadow-md shadow-blue-500/20 transition-all flex items-center justify-center disabled:opacity-60"
            >
              {loading ? (
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              ) : (
                <>
                  Create Student Profile
                  <ArrowRight className="w-4 h-4 ml-2" />
                </>
              )}
            </button>
          </form>

          <div className="mt-6 text-center text-xs text-slate-600">
            Already registered?{' '}
            <Link to="/login" className="font-bold text-blue-600 hover:text-blue-700">
              Sign in
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};
