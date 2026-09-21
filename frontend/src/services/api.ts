import axios from 'axios';
import {
  UserProfile, User, Category, Degree, Branch,
  Skill, SkillTeach, SkillLearn, SmartMatchResult, SwapRequest,
  SwapSession, Review, Course, CourseDetail, Enrollment,
  LearningCourseView, AssessmentDetail, AssessmentResult,
  Certificate, CertificateVerify, Notification, AdminStats
} from '../types';

const API_BASE_URL = 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
});

// Attach JWT Bearer Token to all requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('skillswap_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle 401 unauthorized
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // Clear token if invalid credentials
      const currentPath = window.location.pathname;
      if (currentPath !== '/login' && currentPath !== '/register') {
        localStorage.removeItem('skillswap_token');
        localStorage.removeItem('skillswap_user');
      }
    }
    return Promise.reject(error);
  }
);

// API Service Methods
export const authApi = {
  login: (data: { email: string; password: string }) =>
    api.post<{ access_token: string; token_type: string; user: any }>('/auth/login', data),
  register: (data: any) =>
    api.post<any>('/auth/register', data),
  getMe: () =>
    api.get<UserProfile>('/auth/me'),
};

export const academicApi = {
  getCategories: () => api.get<Category[]>('/academic/categories'),
  getDegrees: (categoryId?: number) => api.get<Degree[]>('/academic/degrees', { params: { category_id: categoryId } }),
  getBranches: (degreeId?: number) => api.get<Branch[]>('/academic/branches', { params: { degree_id: degreeId } }),
};

export const usersApi = {
  getProfile: () => api.get<UserProfile>('/users/me'),
  updateProfile: (data: any) => api.put<UserProfile>('/users/me', data),
  getStudents: (params?: { search?: string; college?: string; degree_id?: number }) =>
    api.get<any[]>('/users', { params }),
  getStudentById: (id: number) => api.get<any>(`/users/${id}`),
};

export const skillsApi = {
  getSkills: (params?: { category_name?: string; search?: string }) =>
    api.get<Skill[]>('/skills', { params }),
  createSkill: (data: { name: string; category_name?: string; description?: string }) =>
    api.post<Skill>('/skills', data),
  getMyTeachSkills: () => api.get<SkillTeach[]>('/skills/user/teach'),
  addTeachSkill: (data: { skill_id?: number; skill_name?: string; category_name?: string; proficiency_level: string; experience_description?: string }) =>
    api.post<SkillTeach>('/skills/user/teach', data),
  removeTeachSkill: (id: number) => api.delete(`/skills/user/teach/${id}`),
  getMyLearnSkills: () => api.get<SkillLearn[]>('/skills/user/learn'),
  addLearnSkill: (data: { skill_id?: number; skill_name?: string; category_name?: string; desired_level: string; notes?: string }) =>
    api.post<SkillLearn>('/skills/user/learn', data),
  removeLearnSkill: (id: number) => api.delete(`/skills/user/learn/${id}`),
};

export const matchesApi = {
  getSmartMatches: (params?: { skill_id?: number; skill_name?: string }) =>
    api.get<SmartMatchResult>('/matches', { params }),
};

export const swapsApi = {
  createRequest: (data: { receiver_id: number; offered_skill_id?: number; requested_skill_id?: number; message?: string }) =>
    api.post<SwapRequest>('/swaps/requests', data),
  getRequests: (params?: { type?: 'all' | 'incoming' | 'outgoing'; status_filter?: string }) =>
    api.get<SwapRequest[]>('/swaps/requests', { params }),
  acceptRequest: (id: number) => api.put<SwapRequest>(`/swaps/requests/${id}/accept`),
  rejectRequest: (id: number) => api.put<SwapRequest>(`/swaps/requests/${id}/reject`),
  cancelRequest: (id: number) => api.put<SwapRequest>(`/swaps/requests/${id}/cancel`),
  getSessions: () => api.get<SwapSession[]>('/swaps/sessions'),
  completeSession: (id: number) => api.put<SwapSession>(`/swaps/sessions/${id}/complete`),
  createReview: (data: { session_id?: number; reviewee_id: number; rating: number; review_text?: string }) =>
    api.post<Review>('/swaps/reviews', data),
};

export const coursesApi = {
  getCourses: (params?: { search?: string; category_id?: number; degree_id?: number; branch_id?: number; skill_id?: number; difficulty?: string }) =>
    api.get<Course[]>('/courses', { params }),
  getRecommended: () => api.get<Course[]>('/courses/recommended'),
  getCourseDetail: (id: number) => api.get<CourseDetail>(`/courses/${id}`),
  createCourse: (data: any) => api.post<Course>('/courses', data),
  updateCourse: (id: number, data: any) => api.put<Course>(`/courses/${id}`, data),
  deleteCourse: (id: number) => api.delete(`/courses/${id}`),
};

export const enrollmentsApi = {
  enrollCourse: (courseId: number) => api.post<Enrollment>(`/enrollments/courses/${courseId}/enroll`),
  getMyCourses: () => api.get<Enrollment[]>('/enrollments/my-courses'),
  getCourseLearningView: (courseId: number) => api.get<LearningCourseView>(`/enrollments/courses/${courseId}/learn`),
  completeLesson: (lessonId: number) => api.post<{ status: string; lesson_id: number; is_completed: boolean; progress_percentage: number }>(`/enrollments/lessons/${lessonId}/complete`),
};

export const assessmentsApi = {
  getModuleAssessment: (moduleId: number) => api.get<AssessmentDetail>(`/assessments/module/${moduleId}`),
  submitModuleAssessment: (assessmentId: number, answers: { question_id: number; selected_option_id: number }[]) =>
    api.post<AssessmentResult>(`/assessments/module/${assessmentId}/submit`, { answers }),
  getFinalAssessment: (courseId: number) => api.get<AssessmentDetail>(`/assessments/final/${courseId}`),
  submitFinalAssessment: (courseId: number, answers: { question_id: number; selected_option_id: number }[]) =>
    api.post<AssessmentResult>(`/assessments/final/${courseId}/submit`, { answers }),
};

export const certificatesApi = {
  getMyCertificates: () => api.get<Certificate[]>('/certificates'),
  getCertificateDetail: (id: number) => api.get<Certificate>(`/certificates/${id}`),
  getDownloadUrl: (id: number) => `${API_BASE_URL}/certificates/${id}/download`,
  verifyCertificate: (certificateId: string) => api.get<CertificateVerify>(`/certificates/verify/${certificateId}`),
};

export const notificationsApi = {
  getNotifications: () => api.get<Notification[]>('/notifications'),
  markRead: (id: number) => api.put<Notification>(`/notifications/${id}/read`),
  markAllRead: () => api.put<{ status: string; message: string }>('/notifications/read-all'),
};

export const adminApi = {
  getStats: () => api.get<AdminStats>('/admin/stats'),
  getUsers: (params?: { role?: string; search?: string }) => api.get<any[]>('/admin/users', { params }),
  updateUserStatus: (userId: number, data: { is_active: boolean; role?: string }) =>
    api.put<any>(`/admin/users/${userId}/status`, data),
  getCertificates: () => api.get<Certificate[]>('/admin/certificates'),
  createModule: (data: { course_id: number; title: string; description?: string; order_index?: number }) =>
    api.post<any>('/admin/modules', data),
  createLesson: (data: { module_id: number; title: string; content_text: string; description?: string; duration_minutes?: number; order_index?: number }) =>
    api.post<any>('/admin/lessons', data),
  createAssessment: (data: any) =>
    api.post<any>('/admin/assessments', data),
};
