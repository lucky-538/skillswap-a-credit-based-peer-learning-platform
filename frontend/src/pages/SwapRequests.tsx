import React, { useState, useEffect } from 'react';
import {
  ArrowLeftRight, Check, X, Clock, Calendar, Video,
  CheckCircle2, Star, User, Building, MessageSquare
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { swapsApi } from '../services/api';
import { SwapRequest, SwapSession } from '../types';

export const SwapRequests: React.FC = () => {
  const { user } = useAuth();

  const [activeTab, setActiveTab] = useState<'incoming' | 'outgoing' | 'sessions'>('incoming');
  const [requests, setRequests] = useState<SwapRequest[]>([]);
  const [sessions, setSessions] = useState<SwapSession[]>([]);
  const [loading, setLoading] = useState(true);

  // Review Modal
  const [reviewingSession, setReviewingSession] = useState<SwapSession | null>(null);
  const [rating, setRating] = useState<number>(5);
  const [reviewText, setReviewText] = useState('');
  const [reviewSuccess, setReviewSuccess] = useState(false);

  useEffect(() => {
    loadData();
  }, [activeTab]);

  const loadData = async () => {
    setLoading(true);
    try {
      if (activeTab === 'sessions') {
        const res = await swapsApi.getSessions();
        setSessions(res.data);
      } else {
        const res = await swapsApi.getRequests({ type: activeTab });
        setRequests(res.data);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleAccept = async (id: number) => {
    try {
      await swapsApi.acceptRequest(id);
      loadData();
    } catch (e) {
      console.error(e);
    }
  };

  const handleReject = async (id: number) => {
    try {
      await swapsApi.rejectRequest(id);
      loadData();
    } catch (e) {
      console.error(e);
    }
  };

  const handleCancel = async (id: number) => {
    try {
      await swapsApi.cancelRequest(id);
      loadData();
    } catch (e) {
      console.error(e);
    }
  };

  const handleCompleteSession = async (id: number) => {
    try {
      await swapsApi.completeSession(id);
      loadData();
    } catch (e) {
      console.error(e);
    }
  };

  const handleSubmitReview = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!reviewingSession || !user) return;

    const revieweeId = reviewingSession.user1_id === user.id ? reviewingSession.user2_id : reviewingSession.user1_id;

    try {
      await swapsApi.createReview({
        session_id: reviewingSession.id,
        reviewee_id: revieweeId,
        rating,
        review_text: reviewText
      });
      setReviewSuccess(true);
      setTimeout(() => {
        setReviewingSession(null);
        setReviewSuccess(false);
        setReviewText('');
        loadData();
      }, 1500);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-fade-in">
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          Skill Swap Hub & Sessions
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1">
          Coordinate peer learning requests, attend video sessions, and leave trusted reviews.
        </p>
      </div>

      {/* Tabs Switcher */}
      <div className="flex border-b border-slate-200 space-x-4">
        <button
          onClick={() => setActiveTab('incoming')}
          className={`pb-3 text-sm font-bold border-b-2 transition-colors flex items-center gap-2 ${
            activeTab === 'incoming'
              ? 'border-blue-600 text-blue-700'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <ArrowLeftRight className="w-4 h-4" />
          Incoming Requests
        </button>

        <button
          onClick={() => setActiveTab('outgoing')}
          className={`pb-3 text-sm font-bold border-b-2 transition-colors flex items-center gap-2 ${
            activeTab === 'outgoing'
              ? 'border-blue-600 text-blue-700'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <Clock className="w-4 h-4" />
          Outgoing Requests
        </button>

        <button
          onClick={() => setActiveTab('sessions')}
          className={`pb-3 text-sm font-bold border-b-2 transition-colors flex items-center gap-2 ${
            activeTab === 'sessions'
              ? 'border-emerald-600 text-emerald-700'
              : 'border-transparent text-slate-500 hover:text-slate-800'
          }`}
        >
          <Calendar className="w-4 h-4" />
          Swap Sessions & Reviews
        </button>
      </div>

      {/* CONTENT LIST */}
      {loading ? (
        <div className="py-16 text-center text-sm text-slate-400">Loading requests and sessions...</div>
      ) : activeTab === 'sessions' ? (
        /* SESSIONS VIEW */
        sessions.length === 0 ? (
          <div className="py-12 text-center bg-slate-50 rounded-3xl border border-dashed border-slate-200 text-xs text-slate-400">
            No active learning sessions. Accept a swap request to schedule a session!
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {sessions.map(s => {
              const partner = s.user1_id === user?.id ? s.user2 : s.user1;
              const isCompleted = s.status === 'completed';

              return (
                <div key={s.id} className="bg-white rounded-3xl p-6 border border-slate-200 shadow-xs space-y-4">
                  <div className="flex items-center justify-between">
                    <span className={`px-2.5 py-1 text-[10px] font-bold rounded-full ${
                      isCompleted ? 'bg-emerald-100 text-emerald-800' : 'bg-blue-100 text-blue-800'
                    }`}>
                      {s.status.toUpperCase()}
                    </span>
                    <span className="text-xs text-slate-400 font-mono">{s.duration_minutes} Minutes</span>
                  </div>

                  <div>
                    <h3 className="text-base font-bold text-slate-900">{s.title}</h3>
                    <p className="text-xs text-slate-500 mt-1">Learning Partner: <b>{partner?.name}</b> ({partner?.college})</p>
                  </div>

                  <div className="p-3 bg-slate-50 rounded-2xl border border-slate-100 space-y-2 text-xs">
                    <div className="flex items-center justify-between text-slate-700">
                      <span className="flex items-center gap-1"><Video className="w-3.5 h-3.5 text-blue-600" /> Mode: {s.meeting_type}</span>
                      {s.meeting_link_or_location && (
                        <a
                          href={s.meeting_link_or_location}
                          target="_blank"
                          rel="noreferrer"
                          className="font-bold text-blue-600 hover:text-blue-700 underline"
                        >
                          Join Google Meet
                        </a>
                      )}
                    </div>
                  </div>

                  <div className="flex items-center justify-end gap-2 pt-2 border-t border-slate-100">
                    {!isCompleted ? (
                      <button
                        onClick={() => handleCompleteSession(s.id)}
                        className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs rounded-xl shadow-xs transition-colors flex items-center gap-1.5"
                      >
                        <CheckCircle2 className="w-4 h-4" />
                        Mark Completed (+5 Credits)
                      </button>
                    ) : (
                      <button
                        onClick={() => setReviewingSession(s)}
                        className="px-4 py-2 bg-amber-500 hover:bg-amber-600 text-white font-bold text-xs rounded-xl shadow-xs transition-colors flex items-center gap-1.5"
                      >
                        <Star className="w-4 h-4" />
                        Leave Peer Review
                      </button>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )
      ) : (
        /* REQUESTS VIEW (INCOMING / OUTGOING) */
        requests.length === 0 ? (
          <div className="py-12 text-center bg-slate-50 rounded-3xl border border-dashed border-slate-200 text-xs text-slate-400">
            No {activeTab} skill swap requests found.
          </div>
        ) : (
          <div className="space-y-4">
            {requests.map(req => {
              const otherUser = activeTab === 'incoming' ? req.sender : req.receiver;

              return (
                <div
                  key={req.id}
                  className="bg-white rounded-3xl p-6 border border-slate-200 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-6"
                >
                  <div className="space-y-3">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded-full bg-blue-600 text-white font-bold flex items-center justify-center text-sm">
                        {otherUser.name.charAt(0)}
                      </div>
                      <div>
                        <div className="text-sm font-bold text-slate-900">{otherUser.name}</div>
                        <div className="text-xs text-slate-500">{otherUser.college} • {otherUser.branch}</div>
                      </div>
                      <span className={`px-2 py-0.5 text-[10px] font-bold rounded-full ml-auto sm:ml-2 ${
                        req.status === 'accepted'
                          ? 'bg-emerald-100 text-emerald-800'
                          : req.status === 'rejected'
                          ? 'bg-red-100 text-red-800'
                          : 'bg-amber-100 text-amber-800'
                      }`}>
                        {req.status.toUpperCase()}
                      </span>
                    </div>

                    <div className="flex flex-wrap items-center gap-2 text-xs">
                      {req.offered_skill && (
                        <span className="px-2 py-1 bg-blue-50 text-blue-800 border border-blue-200 rounded-lg">
                          <b>Offers:</b> {req.offered_skill.name}
                        </span>
                      )}
                      {req.requested_skill && (
                        <span className="px-2 py-1 bg-teal-50 text-teal-800 border border-teal-200 rounded-lg">
                          <b>Requests:</b> {req.requested_skill.name}
                        </span>
                      )}
                    </div>

                    {req.message && (
                      <p className="text-xs text-slate-600 italic bg-slate-50 p-2.5 rounded-xl border border-slate-100">
                        "{req.message}"
                      </p>
                    )}
                  </div>

                  {/* Actions */}
                  {req.status === 'pending' && (
                    <div className="flex items-center gap-2 shrink-0">
                      {activeTab === 'incoming' ? (
                        <>
                          <button
                            onClick={() => handleAccept(req.id)}
                            className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 text-white text-xs font-bold rounded-xl shadow-xs transition-colors flex items-center gap-1"
                          >
                            <Check className="w-4 h-4" /> Accept
                          </button>
                          <button
                            onClick={() => handleReject(req.id)}
                            className="px-4 py-2 bg-slate-100 hover:bg-red-50 text-slate-700 hover:text-red-700 text-xs font-bold rounded-xl transition-colors flex items-center gap-1"
                          >
                            <X className="w-4 h-4" /> Reject
                          </button>
                        </>
                      ) : (
                        <button
                          onClick={() => handleCancel(req.id)}
                          className="px-3 py-1.5 text-xs text-slate-500 hover:text-red-600"
                        >
                          Cancel Request
                        </button>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )
      )}

      {/* REVIEW & RATING MODAL */}
      {reviewingSession && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4 animate-fade-in">
          <div className="bg-white rounded-3xl max-w-md w-full p-6 sm:p-8 shadow-2xl border border-slate-200 relative">
            <h3 className="text-lg font-bold text-slate-900 mb-1">
              Rate Peer Learning Session
            </h3>
            <p className="text-xs text-slate-500 mb-4">
              Help build campus trust by reviewing your exchange experience.
            </p>

            {reviewSuccess ? (
              <div className="py-6 text-center space-y-2">
                <CheckCircle2 className="w-10 h-10 text-emerald-600 mx-auto" />
                <h4 className="text-sm font-bold text-slate-900">Review Submitted! Thank you.</h4>
              </div>
            ) : (
              <form onSubmit={handleSubmitReview} className="space-y-4">
                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase mb-2">
                    Star Rating (1 to 5)
                  </label>
                  <div className="flex items-center gap-2">
                    {[1, 2, 3, 4, 5].map(st => (
                      <button
                        key={st}
                        type="button"
                        onClick={() => setRating(st)}
                        className="p-1 text-2xl hover:scale-110 transition-transform"
                      >
                        <Star className={`w-7 h-7 ${st <= rating ? 'fill-amber-400 text-amber-400' : 'text-slate-300'}`} />
                      </button>
                    ))}
                    <span className="text-sm font-bold text-slate-700 ml-2">{rating} / 5</span>
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-bold text-slate-700 uppercase mb-1">
                    Feedback & Comments
                  </label>
                  <textarea
                    rows={3}
                    required
                    value={reviewText}
                    onChange={(e) => setReviewText(e.target.value)}
                    placeholder="Describe how helpful the peer session was..."
                    className="w-full px-3.5 py-2 text-sm border border-slate-300 rounded-xl text-slate-900"
                  />
                </div>

                <div className="flex items-center justify-end gap-3 pt-2">
                  <button
                    type="button"
                    onClick={() => setReviewingSession(null)}
                    className="px-4 py-2 text-xs font-bold text-slate-600 hover:bg-slate-100 rounded-xl"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-5 py-2 bg-amber-500 hover:bg-amber-600 text-white text-xs font-bold rounded-xl shadow-xs transition-colors"
                  >
                    Submit Review
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
