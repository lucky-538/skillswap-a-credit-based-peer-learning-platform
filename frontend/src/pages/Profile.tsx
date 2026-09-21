import React, { useState, useEffect } from 'react';
import {
  User as UserIcon, Building, GraduationCap, Award,
  Plus, Trash2, CheckCircle2, Star, Sparkles, BookOpen
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { usersApi, skillsApi, academicApi } from '../services/api';
import { UserProfile, SkillTeach, SkillLearn, Skill, Category, Degree, Branch } from '../types';

export const Profile: React.FC = () => {
  const { user, refreshProfile } = useAuth();

  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [activeTab, setActiveTab] = useState<'info' | 'teach' | 'learn'>('teach');

  // Edit Info Form state
  const [name, setName] = useState('');
  const [college, setCollege] = useState('');
  const [year, setYear] = useState(3);
  const [bio, setBio] = useState('');
  const [phone, setPhone] = useState('');
  const [isUpdating, setIsUpdating] = useState(false);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  // Teach Skill state
  const [teachSkillName, setTeachSkillName] = useState('');
  const [teachCategory, setTeachCategory] = useState('Technology & Computing');
  const [teachProficiency, setTeachProficiency] = useState<'Beginner' | 'Intermediate' | 'Advanced' | 'Expert'>('Advanced');
  const [teachDesc, setTeachDesc] = useState('');

  // Learn Skill state
  const [learnSkillName, setLearnSkillName] = useState('');
  const [learnCategory, setLearnCategory] = useState('Design & Creative Arts');
  const [learnLevel, setLearnLevel] = useState<'Beginner' | 'Intermediate' | 'Advanced'>('Beginner');
  const [learnNotes, setLearnNotes] = useState('');

  const [skillsCatalog, setSkillsCatalog] = useState<Skill[]>([]);

  useEffect(() => {
    loadProfile();
    skillsApi.getSkills().then(res => setSkillsCatalog(res.data)).catch(() => {});
  }, []);

  const loadProfile = async () => {
    try {
      const res = await usersApi.getProfile();
      setProfile(res.data);
      setName(res.data.name);
      setCollege(res.data.college || '');
      setYear(res.data.year || 3);
      setBio(res.data.bio || '');
      setPhone(res.data.phone || '');
    } catch (e) {
      console.error('Failed to load profile:', e);
    }
  };

  const handleUpdateInfo = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsUpdating(true);
    setSuccessMsg(null);

    try {
      await usersApi.updateProfile({
        name,
        college,
        year: Number(year),
        bio,
        phone
      });
      await refreshProfile();
      await loadProfile();
      setSuccessMsg('Profile updated successfully!');
      setTimeout(() => setSuccessMsg(null), 3000);
    } catch (e) {
      console.error(e);
    } finally {
      setIsUpdating(false);
    }
  };

  const handleAddTeachSkill = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!teachSkillName.trim()) return;

    try {
      await skillsApi.addTeachSkill({
        skill_name: teachSkillName.trim(),
        category_name: teachCategory,
        proficiency_level: teachProficiency,
        experience_description: teachDesc
      });
      setTeachSkillName('');
      setTeachDesc('');
      await loadProfile();
      await refreshProfile();
    } catch (e) {
      console.error(e);
    }
  };

  const handleRemoveTeachSkill = async (id: number) => {
    try {
      await skillsApi.removeTeachSkill(id);
      await loadProfile();
      await refreshProfile();
    } catch (e) {
      console.error(e);
    }
  };

  const handleAddLearnSkill = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!learnSkillName.trim()) return;

    try {
      await skillsApi.addLearnSkill({
        skill_name: learnSkillName.trim(),
        category_name: learnCategory,
        desired_level: learnLevel,
        notes: learnNotes
      });
      setLearnSkillName('');
      setLearnNotes('');
      await loadProfile();
      await refreshProfile();
    } catch (e) {
      console.error(e);
    }
  };

  const handleRemoveLearnSkill = async (id: number) => {
    try {
      await skillsApi.removeLearnSkill(id);
      await loadProfile();
      await refreshProfile();
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-fade-in">
      {/* Header Profile Card */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm flex flex-col sm:flex-row items-center sm:items-start gap-6">
        <div className="w-24 h-24 rounded-full bg-gradient-to-tr from-blue-700 to-indigo-600 text-white flex items-center justify-center text-3xl font-extrabold shadow-md ring-4 ring-blue-50 shrink-0">
          {profile?.avatar_url ? (
            <img src={profile.avatar_url} alt={profile.name} className="w-full h-full object-cover rounded-full" />
          ) : (
            profile?.name?.charAt(0) || 'S'
          )}
        </div>

        <div className="flex-1 text-center sm:text-left space-y-2">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <h1 className="text-2xl font-extrabold text-slate-900">{profile?.name}</h1>
              <p className="text-xs text-slate-500 font-mono mt-0.5">{profile?.email}</p>
            </div>
            <div className="flex items-center gap-2 justify-center sm:justify-end">
              <span className="px-3 py-1 bg-amber-50 text-amber-800 border border-amber-200 rounded-full text-xs font-bold flex items-center gap-1">
                <Star className="w-3.5 h-3.5 fill-amber-500 text-amber-500" />
                {profile?.average_rating || 5.0} Rating ({profile?.review_count || 0} reviews)
              </span>
              <span className="px-3 py-1 bg-indigo-50 text-indigo-700 border border-indigo-200 rounded-full text-xs font-bold">
                {profile?.credits || 10} Credits
              </span>
            </div>
          </div>

          <div className="text-xs text-slate-600 flex flex-wrap items-center gap-x-4 gap-y-1">
            <span className="flex items-center gap-1"><Building className="w-3.5 h-3.5 text-slate-400" /> {profile?.college || 'University'}</span>
            <span className="flex items-center gap-1"><GraduationCap className="w-3.5 h-3.5 text-slate-400" /> {profile?.branch || 'General'} (Year {profile?.year})</span>
          </div>

          {profile?.bio && (
            <p className="text-xs text-slate-600 italic bg-slate-50 p-3 rounded-xl border border-slate-100 max-w-2xl">
              "{profile.bio}"
            </p>
          )}
        </div>
      </div>

      {/* Tabs Switcher */}
      <div className="flex border-b border-slate-200 space-x-4">
        <button
          onClick={() => setActiveTab('teach')}
          className={`pb-3 text-sm font-bold border-b-2 transition-colors flex items-center gap-2 ${
            activeTab === 'teach'
              ? 'border-blue-600 text-blue-700'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <Sparkles className="w-4 h-4 text-blue-600" />
          Skills I Can Teach ({profile?.skills_teach?.length || 0})
        </button>

        <button
          onClick={() => setActiveTab('learn')}
          className={`pb-3 text-sm font-bold border-b-2 transition-colors flex items-center gap-2 ${
            activeTab === 'learn'
              ? 'border-teal-600 text-teal-700'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <BookOpen className="w-4 h-4 text-teal-600" />
          Skills I Want to Learn ({profile?.skills_learn?.length || 0})
        </button>

        <button
          onClick={() => setActiveTab('info')}
          className={`pb-3 text-sm font-bold border-b-2 transition-colors flex items-center gap-2 ${
            activeTab === 'info'
              ? 'border-slate-800 text-slate-900'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <UserIcon className="w-4 h-4" />
          Edit Profile Information
        </button>
      </div>

      {/* TAB 1: SKILLS I CAN TEACH */}
      {activeTab === 'teach' && (
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-xs">
            <h3 className="text-base font-bold text-slate-900 mb-1">Add Skill You Can Teach</h3>
            <p className="text-xs text-slate-500 mb-4">
              Share your skills with fellow campus students to earn credits and match for peer exchanges.
            </p>

            <form onSubmit={handleAddTeachSkill} className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Skill Name</label>
                  <input
                    type="text"
                    required
                    value={teachSkillName}
                    onChange={(e) => setTeachSkillName(e.target.value)}
                    placeholder="e.g. Python, UI/UX, Java, Public Speaking"
                    className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-xl text-slate-900"
                    list="skills-list"
                  />
                  <datalist id="skills-list">
                    {skillsCatalog.map(s => <option key={s.id} value={s.name} />)}
                  </datalist>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Proficiency Level</label>
                  <select
                    value={teachProficiency}
                    onChange={(e: any) => setTeachProficiency(e.target.value)}
                    className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-xl text-slate-900"
                  >
                    <option value="Beginner">Beginner (Fundamentals)</option>
                    <option value="Intermediate">Intermediate (Project Experience)</option>
                    <option value="Advanced">Advanced (Extensive Experience)</option>
                    <option value="Expert">Expert (Mastery / Mentor)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Category</label>
                  <select
                    value={teachCategory}
                    onChange={(e) => setTeachCategory(e.target.value)}
                    className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-xl text-slate-900"
                  >
                    <option value="Technology & Computing">Technology & Computing</option>
                    <option value="Design & Creative Arts">Design & Creative Arts</option>
                    <option value="Commerce & Finance">Commerce & Finance</option>
                    <option value="Business & Management">Business & Management</option>
                    <option value="Arts & Humanities">Arts & Humanities</option>
                    <option value="Career & Professional Development">Career & Placement</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Experience / Notes</label>
                <input
                  type="text"
                  value={teachDesc}
                  onChange={(e) => setTeachDesc(e.target.value)}
                  placeholder="e.g. Built 5 full-stack apps, happy to tutor 1-on-1"
                  className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-xl text-slate-900"
                />
              </div>

              <button
                type="submit"
                className="inline-flex items-center px-5 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-xl shadow-sm transition-all"
              >
                <Plus className="w-4 h-4 mr-1.5" />
                Add Teaching Skill
              </button>
            </form>
          </div>

          <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-xs">
            <h3 className="text-base font-bold text-slate-900 mb-4">Your Active Teaching Portfolio</h3>

            {profile?.skills_teach?.length === 0 ? (
              <div className="py-8 text-center text-xs text-slate-400 bg-slate-50 rounded-2xl border border-dashed border-slate-200">
                You haven't listed any teaching skills yet. Add at least one above!
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {profile?.skills_teach?.map(st => (
                  <div key={st.id} className="p-4 rounded-2xl border border-slate-200 bg-slate-50 flex items-start justify-between">
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-bold text-slate-900 text-sm">{st.skill.name}</span>
                        <span className="px-2 py-0.5 bg-blue-100 text-blue-800 text-[10px] font-bold rounded-md">
                          {st.proficiency_level}
                        </span>
                      </div>
                      <div className="text-xs text-slate-500 mt-1">{st.skill.category_name}</div>
                      {st.experience_description && (
                        <p className="text-xs text-slate-600 mt-2 italic bg-white p-2 rounded-lg border border-slate-100">
                          "{st.experience_description}"
                        </p>
                      )}
                    </div>
                    <button
                      onClick={() => handleRemoveTeachSkill(st.id)}
                      className="p-1.5 text-slate-400 hover:text-red-600 rounded-lg hover:bg-red-50 transition-colors"
                      title="Remove"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* TAB 2: SKILLS I WANT TO LEARN */}
      {activeTab === 'learn' && (
        <div className="space-y-6">
          <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-xs">
            <h3 className="text-base font-bold text-slate-900 mb-1">Add Skill You Want to Learn</h3>
            <p className="text-xs text-slate-500 mb-4">
              Adding topics here powers the <b>Smart Matching Engine</b> and <b>Course Fallback system</b>!
            </p>

            <form onSubmit={handleAddLearnSkill} className="space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Skill Name</label>
                  <input
                    type="text"
                    required
                    value={learnSkillName}
                    onChange={(e) => setLearnSkillName(e.target.value)}
                    placeholder="e.g. Machine Learning, Figma, SQL, Spanish"
                    className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-xl text-slate-900"
                    list="skills-list-2"
                  />
                  <datalist id="skills-list-2">
                    {skillsCatalog.map(s => <option key={s.id} value={s.name} />)}
                  </datalist>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Target Level</label>
                  <select
                    value={learnLevel}
                    onChange={(e: any) => setLearnLevel(e.target.value)}
                    className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-xl text-slate-900"
                  >
                    <option value="Beginner">Beginner (Foundations)</option>
                    <option value="Intermediate">Intermediate (Hands-on)</option>
                    <option value="Advanced">Advanced</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Category</label>
                  <select
                    value={learnCategory}
                    onChange={(e) => setLearnCategory(e.target.value)}
                    className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-xl text-slate-900"
                  >
                    <option value="Technology & Computing">Technology & Computing</option>
                    <option value="Design & Creative Arts">Design & Creative Arts</option>
                    <option value="Commerce & Finance">Commerce & Finance</option>
                    <option value="Business & Management">Business & Management</option>
                    <option value="Arts & Humanities">Arts & Humanities</option>
                    <option value="Career & Professional Development">Career & Placement</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Learning Goals</label>
                <input
                  type="text"
                  value={learnNotes}
                  onChange={(e) => setLearnNotes(e.target.value)}
                  placeholder="e.g. Preparing for upcoming semester exams & hackathon"
                  className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-xl text-slate-900"
                />
              </div>

              <button
                type="submit"
                className="inline-flex items-center px-5 py-2.5 bg-teal-600 hover:bg-teal-700 text-white font-bold text-xs rounded-xl shadow-sm transition-all"
              >
                <Plus className="w-4 h-4 mr-1.5" />
                Add Learning Goal
              </button>
            </form>
          </div>

          <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-xs">
            <h3 className="text-base font-bold text-slate-900 mb-4">Your Learning Wishlist</h3>

            {profile?.skills_learn?.length === 0 ? (
              <div className="py-8 text-center text-xs text-slate-400 bg-slate-50 rounded-2xl border border-dashed border-slate-200">
                You haven't listed any learning topics yet. Add a skill above to start matching with peers!
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                {profile?.skills_learn?.map(sl => (
                  <div key={sl.id} className="p-4 rounded-2xl border border-teal-100 bg-teal-50/40 flex items-start justify-between">
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-bold text-slate-900 text-sm">{sl.skill.name}</span>
                        <span className="px-2 py-0.5 bg-teal-100 text-teal-800 text-[10px] font-bold rounded-md">
                          Wants {sl.desired_level}
                        </span>
                      </div>
                      <div className="text-xs text-slate-500 mt-1">{sl.skill.category_name}</div>
                      {sl.notes && (
                        <p className="text-xs text-slate-600 mt-2 italic bg-white p-2 rounded-lg border border-slate-100">
                          "{sl.notes}"
                        </p>
                      )}
                    </div>
                    <button
                      onClick={() => handleRemoveLearnSkill(sl.id)}
                      className="p-1.5 text-slate-400 hover:text-red-600 rounded-lg hover:bg-red-50 transition-colors"
                      title="Remove"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* TAB 3: EDIT PROFILE INFO */}
      {activeTab === 'info' && (
        <div className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200 shadow-xs">
          <h3 className="text-base font-bold text-slate-900 mb-4">Edit Student Details</h3>

          {successMsg && (
            <div className="mb-4 p-3 bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-semibold rounded-xl flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              {successMsg}
            </div>
          )}

          <form onSubmit={handleUpdateInfo} className="space-y-4 max-w-xl">
            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Full Name</label>
              <input
                type="text"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-xl text-slate-900"
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase mb-1">College / University</label>
              <input
                type="text"
                value={college}
                onChange={(e) => setCollege(e.target.value)}
                className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-xl text-slate-900"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Academic Year</label>
                <select
                  value={year}
                  onChange={(e) => setYear(Number(e.target.value))}
                  className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-xl text-slate-900"
                >
                  <option value={1}>1st Year</option>
                  <option value={2}>2nd Year</option>
                  <option value={3}>3rd Year</option>
                  <option value={4}>4th Year</option>
                  <option value={5}>Postgraduate</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Phone (Optional)</label>
                <input
                  type="text"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  placeholder="+91 9876543210"
                  className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-xl text-slate-900"
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold text-slate-700 uppercase mb-1">Bio / About Me</label>
              <textarea
                rows={3}
                value={bio}
                onChange={(e) => setBio(e.target.value)}
                className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-xl text-slate-900"
              />
            </div>

            <button
              type="submit"
              disabled={isUpdating}
              className="px-6 py-2.5 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-xl shadow-md transition-all"
            >
              {isUpdating ? 'Saving...' : 'Save Profile Changes'}
            </button>
          </form>
        </div>
      )}
    </div>
  );
};
