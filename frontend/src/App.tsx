import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { Navbar } from './components/Navbar';
import { Footer } from './components/Footer';
import { ProtectedRoute } from './components/ProtectedRoute';

// Pages
import { Home } from './pages/Home';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Dashboard } from './pages/Dashboard';
import { Profile } from './pages/Profile';
import { SmartMatch } from './pages/SmartMatch';
import { SwapRequests } from './pages/SwapRequests';
import { Courses } from './pages/Courses';
import { CourseDetail } from './pages/CourseDetail';
import { MyCourses } from './pages/MyCourses';
import { LearnCourse } from './pages/LearnCourse';
import { ModuleAssessment } from './pages/ModuleAssessment';
import { FinalAssessment } from './pages/FinalAssessment';
import { Certificates } from './pages/Certificates';
import { VerifyCertificate } from './pages/VerifyCertificate';
import { AdminDashboard } from './pages/AdminDashboard';

export function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <div className="flex flex-col min-h-screen">
          <Navbar />
          <main className="flex-1">
            <Routes>
              {/* Public Routes */}
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/courses" element={<Courses />} />
              <Route path="/courses/:id" element={<CourseDetail />} />
              <Route path="/verify-certificate" element={<VerifyCertificate />} />
              <Route path="/verify-certificate/:certificateId" element={<VerifyCertificate />} />

              {/* Protected Student Routes */}
              <Route
                path="/dashboard"
                element={
                  <ProtectedRoute>
                    <Dashboard />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/profile"
                element={
                  <ProtectedRoute>
                    <Profile />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/skills"
                element={
                  <ProtectedRoute>
                    <SmartMatch />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/skill-matches"
                element={
                  <ProtectedRoute>
                    <SmartMatch />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/swap-requests"
                element={
                  <ProtectedRoute>
                    <SwapRequests />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/my-courses"
                element={
                  <ProtectedRoute>
                    <MyCourses />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/learn/:courseId"
                element={
                  <ProtectedRoute>
                    <LearnCourse />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/assessment/:id"
                element={
                  <ProtectedRoute>
                    <ModuleAssessment />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/final-assessment/:courseId"
                element={
                  <ProtectedRoute>
                    <FinalAssessment />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/certificates"
                element={
                  <ProtectedRoute>
                    <Certificates />
                  </ProtectedRoute>
                }
              />

              {/* Protected Admin Routes */}
              <Route
                path="/admin"
                element={
                  <ProtectedRoute adminOnly>
                    <AdminDashboard />
                  </ProtectedRoute>
                }
              />

              {/* Catch-all fallback */}
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
