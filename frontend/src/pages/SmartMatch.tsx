import React, { useState, useEffect } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import {
  Sparkles, Search, ArrowLeftRight, CheckCircle2, Star,
  BookOpen, Building, User, Send, AlertCircle, ArrowRight, ShieldCheck
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { matchesApi, swapsApi, skillsApi } from '../services/api';
import { SmartMatchResult, PeerMatch, Skill } from '../types';

export const SmartMatch: React.FC = () => {
  const { user } = useAuth();
  const [searchParams] = useSearchParams();

  const [searchQuery, setSearchQuery] = useState(searchParams.get('skill') || '');
  const [matchResult, setMatchResult] = useState<SmartMatchResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [skillsCatalog, setSkillsCatalog] = useState<Skill[]>([]);

  // Request Modal State
  const [selectedPeer, setSelectedPeer] = useState<PeerMatch | null>(null);
  const [requestMsg, setRequestMsg] = useState('');
  const [selectedOfferSkillId, setSelectedOfferSkillId] = useState<number | ''>('');
  const [isSending, setIsSending] = useState(false);
  const [sendSuccess, setSendSuccess] = useState(false);

  useEffect(() => {
    skillsApi.getSkills().then(res => setSkillsCatalog(res.data)).catch(() => {});
    performSearch(searchParams.get('skill') || '');
  }, []);

  const performSearch = async (query: string) => {
    setLoading(true);
    try {
      const res = await matchesApi.getSmartMatches({
        skill_name: query.trim() || undefined
      });
      setMatchResult(res.data);
    } catch (err) {
      console.error('Error fetching matches:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    performSearch(searchQuery);
  };

  const openRequestModal = (peer: PeerMatch) => {
    setSelectedPeer(peer);
    setRequestMsg(`Hi ${peer.user.name.split(' ')[0]}, I'd love to swap skills with you! Let's connect for a learning session.`);
    if (user && 'skills_teach' in user && user.skills_teach.length > 0) {
      setSelectedOfferSkillId(user.skills_teach[0].skill_id);
    }
    setSendSuccess(false);
  };

  const handleSendRequest = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedPeer) return;

    setIsSending(true);
    try {
      await swapsApi.createRequest({
        receiver_id: selectedPeer.user.id,
        offered_skill_id: selectedOfferSkillId ? Number(selectedOfferSkillId) : undefined,
        requested_skill_id: selectedPeer.matching_skill.id,
        message: requestMsg
      });
      setSendSuccess(true);
      setTimeout(() => {
        setSelectedPeer(null);
        setSendSuccess(false);
      }, 2000);
    } catch (err) {
      console.error(err);
    } finally {
      setIsSending(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-fade-in">
      {/* Search Header */}
      <div className="text-center max-w-3xl mx-auto space-y-3">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-50 text-teal-800 border border-teal-200 text-xs font-bold uppercase tracking-wider">
          <Sparkles className="w-3.5 h-3.5 text-teal-600" />
          Intelligent Peer Skill Matching Engine
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
          Find Your Ideal Skill Swap Partner
        </h1>
        <p className="text-sm text-slate-600">
          Search any skill you wish to learn. We match reciprocal peer teachers first, with instant course fallback recommendations.
        </p>

        {/* Search Bar */}
        <form onSubmit={handleSearchSubmit} className="max-w-xl mx-auto mt-4">
          <div className="relative rounded-2xl shadow-md">
            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-slate-400">
              <Search className="w-5 h-5" />
            </div>
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search skill (e.g. Python, UI/UX Design, Machine Learning, SQL)..."
              className="block w-full pl-11 pr-28 py-3.5 text-sm border border-slate-300 rounded-2xl focus:ring-2 focus:ring-teal-500 focus:border-teal-500 bg-white text-slate-900 shadow-inner"
            />
            <button
              type="submit"
              className="absolute inset-y-1.5 right-1.5 px-4 bg-teal-600 hover:bg-teal-700 text-white text-xs font-bold rounded-xl shadow-xs transition-all flex items-center gap-1"
            >
              <Sparkles className="w-3.5 h-3.5" />
              Match
            </button>
          </div>
        </form>

        {/* Quick Suggestion Pills */}
        <div className="flex flex-wrap items-center justify-center gap-2 pt-2">
          <span className="text-xs text-slate-400">Popular:</span>
          {['UI/UX Design', 'Python', 'Machine Learning', 'Financial Accounting', 'SQL & MySQL'].map(sk => (
            <button
              key={sk}
              onClick={() => {
                setSearchQuery(sk);
                performSearch(sk);
              }}
              className="px-3 py-1 bg-white hover:bg-slate-100 text-slate-700 text-xs font-semibold rounded-full border border-slate-200 transition-colors"
            >
              {sk}
            </button>
          ))}
        </div>
      </div>

      {/* MATCH RESULTS SECTION */}
      <div className="space-y-6">
        <div className="flex items-center justify-between border-b border-slate-200 pb-3">
          <div>
            <h2 className="text-lg font-bold text-slate-900">
              Results for <span className="text-teal-700">"{matchResult?.requested_skill || searchQuery || 'Selected Skills'}"</span>
            </h2>
            <p className="text-xs text-slate-500">
              {matchResult?.peers_found_count || 0} peer student(s) available
            </p>
          </div>
        </div>

        {loading ? (
          <div className="py-20 text-center">
            <div className="w-10 h-10 border-4 border-teal-600 border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
            <p className="text-sm font-medium text-slate-600">Analyzing campus skills matrix and computing match scores...</p>
          </div>
        ) : matchResult?.peers_found_count && matchResult.peers_found_count > 0 ? (
          /* PEERS FOUND GRID */
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {matchResult.matches.map((peer, idx) => (
              <div
                key={idx}
                className={`bg-white rounded-3xl p-6 border transition-all hover:shadow-lg space-y-4 flex flex-col justify-between ${
                  peer.match_type === 'direct_swap'
                    ? 'border-emerald-300 ring-2 ring-emerald-500/20 shadow-emerald-500/5'
                    : 'border-slate-200 shadow-sm'
                }`}
              >
                <div>
                  {/* Top Badges */}
                  <div className="flex items-center justify-between gap-2 mb-3">
                    {peer.match_type === 'direct_swap' ? (
                      <span className="inline-flex items-center gap-1 px-2.5 py-1 bg-emerald-100 text-emerald-800 text-xs font-extrabold rounded-full border border-emerald-300">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                        Direct Skill Swap (100% Match)
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 px-2.5 py-1 bg-blue-100 text-blue-800 text-xs font-bold rounded-full">
                        {peer.match_score}% Match Score
                      </span>
                    )}

                    <div className="flex items-center gap-1 text-xs font-bold text-amber-600 bg-amber-50 px-2 py-0.5 rounded-md border border-amber-200">
                      <Star className="w-3 h-3 fill-amber-500 text-amber-500" />
                      {peer.rating}
                    </div>
                  </div>

                  {/* Student Header */}
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 rounded-full bg-gradient-to-tr from-teal-600 to-blue-600 text-white font-bold flex items-center justify-center text-base shadow-sm ring-2 ring-teal-100 shrink-0">
                      {peer.user.avatar_url ? (
                        <img src={peer.user.avatar_url} alt={peer.user.name} className="w-full h-full object-cover rounded-full" />
                      ) : (
                        peer.user.name.charAt(0)
                      )}
                    </div>
                    <div>
                      <h3 className="text-base font-bold text-slate-900">{peer.user.name}</h3>
                      <p className="text-xs text-slate-500 flex items-center gap-1">
                        <Building className="w-3 h-3 text-slate-400" /> {peer.user.college}
                      </p>
                      {peer.same_college && (
                        <span className="text-[10px] text-teal-700 font-bold bg-teal-50 px-1.5 py-0.5 rounded-sm">Same Campus</span>
                      )}
                    </div>
                  </div>

                  {/* Skill Swap Matrix Breakdown */}
                  <div className="mt-4 p-3.5 rounded-2xl bg-slate-50 border border-slate-100 space-y-2 text-xs">
                    <div className="flex items-start gap-2">
                      <span className="px-1.5 py-0.5 bg-blue-100 text-blue-800 text-[10px] font-bold rounded-md shrink-0">
                        Teaches
                      </span>
                      <span className="font-bold text-slate-900">{peer.teaches_skill}</span>
                    </div>

                    <div className="flex items-start gap-2">
                      <span className="px-1.5 py-0.5 bg-teal-100 text-teal-800 text-[10px] font-bold rounded-md shrink-0">
                        Wants
                      </span>
                      <span className="text-slate-700">{peer.wants_to_learn || 'Open to learn'}</span>
                    </div>
                  </div>

                  {peer.user.bio && (
                    <p className="text-xs text-slate-600 italic mt-3 line-clamp-2">
                      "{peer.user.bio}"
                    </p>
                  )}
                </div>

                <button
                  onClick={() => openRequestModal(peer)}
                  className={`w-full py-2.5 px-4 text-xs font-bold text-white rounded-xl shadow-sm transition-all flex items-center justify-center gap-1.5 ${
                    peer.match_type === 'direct_swap'
                      ? 'bg-emerald-600 hover:bg-emerald-700 shadow-emerald-500/20'
                      : 'bg-teal-600 hover:bg-teal-700 shadow-teal-500/20'
                  }`}
                >
                  <Send className="w-3.5 h-3.5" />
                  Request Skill Swap
                </button>
              </div>
            ))}
          </div>
        ) : (
          /* NO PEER MATCH FOUND -> OFFICIAL FALLBACK RECOMMENDATION BANNER */
          <div className="space-y-6">
            <div className="p-6 sm:p-8 bg-gradient-to-r from-amber-50 via-orange-50 to-blue-50 rounded-3xl border border-amber-200/80 shadow-sm">
              <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
                <div className="space-y-2">
                  <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-100 text-amber-900 text-xs font-bold uppercase tracking-wider">
                    <AlertCircle className="w-3.5 h-3.5 text-amber-700" />
                    No Peer Match Found
                  </div>
                  <h3 className="text-xl sm:text-2xl font-extrabold text-slate-900">
                    No suitable skill partner found.
                  </h3>
                  <p className="text-sm text-slate-700 max-w-2xl leading-relaxed">
                    Don't worry! You can master this topic immediately through one of our structured, accredited curriculum courses with mock assessments and verified completion certificates.
                  </p>
                </div>
              </div>
            </div>

            {/* Recommended Fallback Course Card */}
            {matchResult?.fallback_course && (
              <div className="bg-white rounded-3xl p-6 sm:p-8 border border-blue-200 shadow-md flex flex-col md:flex-row gap-6 items-center">
                <div className="w-full md:w-56 h-36 rounded-2xl bg-slate-900 overflow-hidden relative shrink-0">
                  {matchResult.fallback_course.thumbnail_url ? (
                    <img
                      src={matchResult.fallback_course.thumbnail_url}
                      alt={matchResult.fallback_course.title}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center text-white">
                      <BookOpen className="w-10 h-10 text-blue-400" />
                    </div>
                  )}
                  <div className="absolute top-2 left-2 px-2 py-0.5 bg-blue-600/90 text-white text-[10px] font-bold rounded-md backdrop-blur-xs">
                    Recommended Course
                  </div>
                </div>

                <div className="flex-1 space-y-2">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-bold text-blue-700 uppercase tracking-wider">
                      {matchResult.fallback_course.category_name}
                    </span>
                    <span className="text-slate-300">•</span>
                    <span className="text-xs text-slate-500">{matchResult.fallback_course.difficulty}</span>
                    <span className="text-slate-300">•</span>
                    <span className="text-xs text-slate-500">{matchResult.fallback_course.duration_hours} Hours</span>
                  </div>

                  <h3 className="text-xl font-bold text-slate-900">
                    {matchResult.fallback_course.title}
                  </h3>

                  <p className="text-xs text-slate-600 line-clamp-2">
                    {matchResult.fallback_course.description}
                  </p>

                  <div className="flex flex-wrap items-center gap-4 text-xs text-slate-600 pt-1">
                    <div className="flex items-center gap-1 font-bold text-amber-600">
                      <Star className="w-3.5 h-3.5 fill-amber-500 text-amber-500" />
                      {matchResult.fallback_course.rating} Rating
                    </div>
                    <div>{matchResult.fallback_course.modules_count} Progressive Modules</div>
                    <div className="flex items-center gap-1 text-emerald-700 font-bold">
                      <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                      Certificate Available
                    </div>
                  </div>
                </div>

                <div className="w-full md:w-auto shrink-0">
                  <Link
                    to={`/courses/${matchResult.fallback_course.id}`}
                    className="w-full md:w-auto inline-flex items-center justify-center px-6 py-3.5 bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs rounded-xl shadow-md transition-all gap-2"
                  >
                    Start Learning Course
                    <ArrowRight className="w-4 h-4" />
                  </Link>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* SWAP REQUEST MODAL */}
      {selectedPeer && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4 animate-fade-in">
          <div className="bg-white rounded-3xl max-w-lg w-full p-6 sm:p-8 shadow-2xl border border-slate-200 relative">
            <h3 className="text-lg font-bold text-slate-900 mb-1">
              Request Skill Swap with {selectedPeer.user.name}
            </h3>
            <p className="text-xs text-slate-500 mb-4">
              Send a message proposing a learning session. Once accepted, an interactive session schedule is created.
            </p>

            {sendSuccess ? (
              <div className="py-8 text-center space-y-2">
                <div className="w-12 h-12 bg-emerald-100 text-emerald-700 rounded-full flex items-center justify-center mx-auto">
                  <CheckCircle2 className="w-6 h-6" />
                </div>
                <h4 className="text-base font-bold text-slate-900">Request Sent Successfully!</h4>
                <p className="text-xs text-slate-500">{selectedPeer.user.name} will be notified immediately.</p>
              </div>
            ) : (
              <form onSubmit={handleSendRequest} className="space-y-4">
                <div className="p-3 bg-slate-50 rounded-2xl border border-slate-100 text-xs space-y-1">
                  <div><b>Skill you want to learn:</b> {selectedPeer.matching_skill.name}</div>
                  <div><b>Taught by:</b> {selectedPeer.user.name} ({selectedPeer.user.college})</div>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
                    Skill you can offer in return:
                  </label>
                  <select
                    value={selectedOfferSkillId}
                    onChange={(e) => setSelectedOfferSkillId(Number(e.target.value))}
                    className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-xl text-slate-900"
                  >
                    {user && 'skills_teach' in user && user.skills_teach.length > 0 ? (
                      user.skills_teach.map(st => (
                        <option key={st.id} value={st.skill_id}>{st.skill.name} ({st.proficiency_level})</option>
                      ))
                    ) : (
                      <option value="">General Peer Knowledge Exchange</option>
                    )}
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
                    Introduction Message
                  </label>
                  <textarea
                    rows={3}
                    required
                    value={requestMsg}
                    onChange={(e) => setRequestMsg(e.target.value)}
                    className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-xl text-slate-900"
                  />
                </div>

                <div className="flex items-center justify-end gap-3 pt-2">
                  <button
                    type="button"
                    onClick={() => setSelectedPeer(null)}
                    className="px-4 py-2 text-xs font-bold text-slate-600 hover:bg-slate-100 rounded-xl"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={isSending}
                    className="px-5 py-2 bg-teal-600 hover:bg-teal-700 text-white text-xs font-bold rounded-xl shadow-sm transition-all"
                  >
                    {isSending ? 'Sending...' : 'Send Request'}
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
