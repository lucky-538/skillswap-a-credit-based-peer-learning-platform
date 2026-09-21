export interface User {
  id: number;
  name: string;
  email: string;
  role: 'student' | 'admin';
  college?: string;
  branch?: string;
  year?: number;
  degree_id?: number;
  branch_id?: number;
  bio?: string;
  avatar_url?: string;
  phone?: string;
  credits: number;
  reputation_score: number;
  is_active: boolean;
  created_at?: string;
}

export interface UserProfile extends User {
  degree?: Degree;
  branch_rel?: Branch;
  skills_teach: SkillTeach[];
  skills_learn: SkillLearn[];
  courses_enrolled_count: number;
  courses_completed_count: number;
  certificates_count: number;
  swaps_completed_count: number;
  average_rating: number;
  review_count: number;
}

export interface Category {
  id: number;
  name: string;
  code: string;
  description?: string;
  icon?: string;
  degrees?: Degree[];
}

export interface Degree {
  id: number;
  category_id: number;
  name: string;
  code: string;
  description?: string;
  branches?: Branch[];
}

export interface Branch {
  id: number;
  degree_id: number;
  name: string;
  code: string;
  description?: string;
}

export interface Skill {
  id: number;
  name: string;
  category_id?: number;
  category_name?: string;
  description?: string;
}

export interface SkillTeach {
  id: number;
  user_id: number;
  skill_id: number;
  skill: Skill;
  proficiency_level: 'Beginner' | 'Intermediate' | 'Advanced' | 'Expert';
  experience_description?: string;
}

export interface SkillLearn {
  id: number;
  user_id: number;
  skill_id: number;
  skill: Skill;
  desired_level: 'Beginner' | 'Intermediate' | 'Advanced';
  notes?: string;
}

export interface PeerMatch {
  user: {
    id: number;
    name: string;
    college?: string;
    branch?: string;
    year?: number;
    bio?: string;
    avatar_url?: string;
    reputation_score: number;
    skills_teach: SkillTeach[];
    skills_learn: SkillLearn[];
    swaps_completed_count: number;
    average_rating: number;
    review_count: number;
  };
  matching_skill: Skill;
  match_type: 'direct_swap' | 'tutor';
  match_score: number;
  teaches_skill: string;
  wants_to_learn?: string;
  rating: number;
  same_college: boolean;
}

export interface FallbackCourse {
  id: number;
  title: string;
  slug: string;
  category_name: string;
  difficulty: string;
  duration_hours: number;
  modules_count: number;
  rating: number;
  thumbnail_url?: string;
  description: string;
  certificate_available: boolean;
}

export interface SmartMatchResult {
  requested_skill: string;
  peers_found_count: number;
  matches: PeerMatch[];
  fallback_recommended: boolean;
  fallback_course?: FallbackCourse;
}

export interface SwapRequest {
  id: number;
  sender_id: number;
  receiver_id: number;
  offered_skill_id?: number;
  requested_skill_id?: number;
  message?: string;
  status: 'pending' | 'accepted' | 'rejected' | 'cancelled' | 'completed';
  created_at: string;
  updated_at?: string;
  sender: User;
  receiver: User;
  offered_skill?: Skill;
  requested_skill?: Skill;
}

export interface SwapSession {
  id: number;
  request_id?: number;
  user1_id: number;
  user2_id: number;
  title: string;
  description?: string;
  scheduled_time?: string;
  duration_minutes: number;
  meeting_type: 'online' | 'in-person';
  meeting_link_or_location?: string;
  status: 'scheduled' | 'in-progress' | 'completed' | 'cancelled';
  created_at: string;
  user1: User;
  user2: User;
}

export interface Review {
  id: number;
  session_id?: number;
  reviewer_id: number;
  reviewee_id: number;
  rating: number;
  review_text?: string;
  created_at: string;
  reviewer: User;
}

export interface Lesson {
  id: number;
  module_id: number;
  title: string;
  description?: string;
  content_text: string;
  video_url?: string;
  resource_url?: string;
  duration_minutes: number;
  order_index: number;
  is_completed?: boolean;
}

export interface CourseModule {
  id: number;
  course_id: number;
  title: string;
  description?: string;
  order_index: number;
  has_assessment: boolean;
  lessons: Lesson[];
}

export interface Course {
  id: number;
  title: string;
  slug: string;
  category_id: number;
  degree_id?: number;
  branch_id?: number;
  skill_id?: number;
  description: string;
  what_you_will_learn?: string;
  requirements?: string;
  instructor_name?: string;
  difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
  duration_hours: number;
  thumbnail_url?: string;
  is_published: boolean;
  rating: number;
  enrollment_count: number;
  modules_count: number;
  category?: Category;
  degree?: Degree;
  branch?: Branch;
  skill?: Skill;
  created_at?: string;
}

export interface CourseDetail extends Course {
  modules: CourseModule[];
  has_final_assessment: boolean;
  certificate_available: boolean;
}

export interface Enrollment {
  id: number;
  user_id: number;
  course_id: number;
  enrolled_at: string;
  progress_percentage: number;
  status: 'enrolled' | 'in-progress' | 'completed';
  completed_at?: string;
  course: Course;
}

export interface LearningLesson extends Lesson {
  is_completed: boolean;
}

export interface LearningModule {
  id: number;
  course_id: number;
  title: string;
  description?: string;
  order_index: number;
  is_unlocked: boolean;
  is_completed: boolean;
  lessons_completed_count: number;
  total_lessons_count: number;
  assessment_id?: number;
  assessment_passed: boolean;
  assessment_score?: number;
  lessons: LearningLesson[];
}

export interface LearningCourseView {
  course: Course;
  enrollment: Enrollment;
  modules: LearningModule[];
  final_assessment_unlocked: boolean;
  final_assessment_passed: boolean;
  certificate_id?: string;
}

export interface AssessmentOption {
  id: number;
  question_id: number;
  option_text: string;
}

export interface AssessmentQuestion {
  id: number;
  assessment_id: number;
  question_text: string;
  marks: number;
  order_index: number;
  options: AssessmentOption[];
}

export interface AssessmentDetail {
  id: number;
  module_id: number;
  module_title?: string;
  course_id?: number;
  course_title?: string;
  title: string;
  description?: string;
  passing_percentage: number;
  time_limit_minutes: number;
  questions: AssessmentQuestion[];
  total_questions: number;
  total_marks: number;
}

export interface QuestionResultDetail {
  question_id: number;
  question_text: string;
  selected_option_id?: number;
  correct_option_id: number;
  is_correct: boolean;
  explanation?: string;
}

export interface AssessmentResult {
  attempt_id: number;
  assessment_id: number;
  score: number;
  total_marks: number;
  percentage: number;
  passing_percentage: number;
  is_passed: boolean;
  attempt_number: number;
  next_module_unlocked: boolean;
  course_completed: boolean;
  certificate_id?: string;
  feedback_message: string;
  question_results: QuestionResultDetail[];
  attempted_at?: string;
}

export interface Certificate {
  id: number;
  certificate_id: string;
  user_id: number;
  course_id: number;
  issue_date: string;
  student_name: string;
  course_title: string;
  grade: string;
  verification_url: string;
  pdf_path?: string;
}

export interface CertificateVerify {
  is_valid: boolean;
  certificate_id: string;
  student_name?: string;
  course_title?: string;
  issue_date?: string;
  grade?: string;
  institution: string;
  status: 'VALID' | 'INVALID';
  verification_message: string;
}

export interface Notification {
  id: number;
  user_id: number;
  title: string;
  message: string;
  type: string;
  link_url?: string;
  is_read: boolean;
  created_at: string;
}

export interface AdminStats {
  total_students: number;
  total_courses: number;
  total_enrollments: number;
  total_skill_swaps: number;
  completed_courses: number;
  certificates_issued: number;
  total_skills: number;
  total_categories: number;
}
