# SKILLSWAP CAMPUS 🎓
### Multi-Disciplinary E-Learning + Peer-to-Peer Skill Exchange + Assessment + Certification Platform

> **Core Philosophy**: *"Learn from people when possible. Learn from courses when a peer is unavailable. Prove your learning through assessments and certificates."*

---

## 1. System Overview

**SkillSwap Campus** is an all-in-one student-focused full-stack web platform combining:
1. **Multi-Disciplinary E-Learning Platform** across 17 Academic Categories, 23 Degrees, and 186 Branches (Engineering, Arts, Commerce, Management, Science, Architecture, Design, UI/UX, AI, Languages).
2. **Peer-to-Peer Skill Swap & Smart Matching Engine** (100% Reciprocal match detection & direct peer sessions).
3. **Module-Wise Learning & MCQ Mock Tests** with strict sequential module unlocking ($\ge 70\%$ pass requirement).
4. **Official Certification & Public Verification** with unique certificate identifiers (`SSC-PY-2026-000123`), ReportLab PDF generation, and public verification registry (`/verify-certificate/{certificateId}`).
5. **Personalized Recommendations** tailored to the student's degree, branch, and learning wishlist.

---

## 2. Multi-Disciplinary Academic Disciplines Supported

| Faculty / Category | Supported Degrees | Example Branches & Subjects | Example Courses |
| :--- | :--- | :--- | :--- |
| **Engineering & Technology** | B.Tech, BE, M.Tech, ME, Diploma | CSE, IT, AI, AI&ML, Data Science, Cyber Security, Software Engineering, ECE, EEE, Mechanical, Civil, Chemical, Biotech, Aerospace, Automobile, Robotics, IoT, Mechatronics | Python Programming, Java Enterprise, DBMS & SQL, Data Structures & Algorithms, Computer Networks, Operating Systems |
| **AI & Emerging Technologies** | Specialized AI Track | Generative AI, LLMs, Computer Vision, NLP, Prompt Engineering, Reinforcement Learning, Blockchain, Big Data | Generative AI & Large Language Models, Deep Learning with PyTorch, Machine Learning Foundations |
| **Commerce** | B.Com, M.Com | General Accounting, Computers & IT, Taxation & GST, Banking & Insurance, Corporate Auditing, Finance & Investment | Corporate Financial Accounting, Taxation & Income Tax with GST, Auditing & Banking Governance |
| **Business & Management** | BBA, MBA, PGDM | Finance, Marketing Management, Human Resources, Operations, Business Analytics, International Business, Entrepreneurship, Digital Marketing | Strategic Business Leadership, Marketing Management & Consumer Behavior, Business Analytics & Power BI |
| **Science** | B.Sc, M.Sc | Mathematics, Physics, Chemistry, Biology, Computer Science, Statistics, Biotechnology, Microbiology, Data Science, Environmental Science | Applied Calculus & Linear Algebra, Probability & Mathematical Statistics, Quantum Physics |
| **Arts & Humanities** | BA, MA | English Literature, Economics, Political Science, Sociology, Psychology, History, Journalism, Public Administration, Philosophy | Modern Macroeconomics & Fiscal Policy, Journalism & Digital Media, Cognitive Psychology |
| **Architecture** | B.Arch, M.Arch | Architectural Design, Building Construction, Interior Architecture, Urban Planning, CAD, Sustainable Architecture | Architectural Design & 3D CAD Modeling, Sustainable Green Architecture |
| **Fashion & Design** | B.Des | Fashion Design, Apparel Technology, Textile Design, Graphic Design & Branding, Product & Industrial Design | Fashion Illustration & Apparel Technology, Graphic Design & Brand Identity |
| **UI/UX Design** | UI/UX Pro Track | UX Research, UI Design, Design Systems, Figma Prototyping, Usability Testing, Design Thinking | UI/UX Interaction Design & Figma Systems, UX Research & Usability Testing |
| **Computer Applications** | BCA, MCA | Software Development, Cloud Computing, Full Stack Web, Database Systems, Mobile App Development | Full-Stack Web Development (React & FastAPI), Mobile App Engineering |
| **Languages** | Global Languages | Professional English, French, German, Spanish, Telugu, Hindi | Executive Business English & Cross-Cultural Negotiation, German for Engineers |

---

## 3. Technology Stack

- **Frontend**: React 19, Vite, TypeScript, Tailwind CSS v4, Lucide React, Axios, React Router v7, Canvas Confetti.
- **Backend**: Python 3.12+, FastAPI, SQLAlchemy ORM, Pydantic v2, ReportLab (PDF generation), Uvicorn.
- **Database**: MySQL 8 (`skillswap_db`) with PyMySQL driver.
- **Security**: Direct Bcrypt password hashing, JWT Bearer tokens, CORS middleware.

---

## 4. Setup & Running Instructions

### Backend Setup
1. Open PowerShell and navigate to `backend`:
   ```powershell
   cd backend
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
2. Verify `.env` configuration:
   ```env
   DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/skillswap_db
   SECRET_KEY=skillswap-campus-development-secret-key
   ```
3. Seed the massive multi-disciplinary course catalog:
   ```powershell
   python seed_massive_catalog.py
   ```
4. Run the integration test suite:
   ```powershell
   python test_complete_platform.py
   ```
5. Start the FastAPI backend server:
   ```powershell
   uvicorn app.main:app --reload --port 8000
   ```
   *Interactive API Docs: `http://localhost:8000/docs`*

---

### Frontend Setup
1. Open PowerShell and navigate to `frontend`:
   ```powershell
   cd frontend
   npm install
   ```
2. Start the Vite development server:
   ```powershell
   npm run dev
   ```
   *Frontend Application: `http://localhost:5173`*

---

## 5. Demo Accounts & Test Scenarios

The Login page (`/login`) includes **1-Click Quick-Fill Demo Buttons**:

| Role | Name | Email | Password | Scenario Highlights |
| :--- | :--- | :--- | :--- | :--- |
| **Admin Dean** | Prof. Sharma | `admin@skillswap.edu` | `Admin@12345` | Access to `/admin` control center, Course CRUD, Student activation, and Certificate ledger. |
| **Student A** | Rahul Kumar | `rahul@drk.edu` | `Password@123` | **Scenario A**: Teaches Python & SQL; Wants UI/UX Design.<br>**Scenario B**: Fallback recommendations when searching skills with 0 peers. |
| **Student B** | Priya Sharma | `priya@drk.edu` | `Password@123` | **Scenario A**: Teaches UI/UX Design; Wants Python (100% Reciprocal Swap). |

---

## 6. Verification Results

All 15 automated integration tests passed with 100% success:
- `[PASS] 1. System Health Check: 200 OK`
- `[PASS] 2. Student Authentication (Rahul): 200 OK`
- `[PASS] 3. Administrator Authentication: 200 OK`
- `[PASS] 4. Course Catalog Listing & Filtering: 200 OK`
- `[PASS] 5. Personalized Course Recommendations: 200 OK`
- `[PASS] 6. Scenario A (100% Reciprocal Skill Swap): 200 OK`
- `[PASS] 7. Scenario B (Course Fallback): 200 OK`
- `[PASS] 8. Course Enrollment: 200 OK`
- `[PASS] 9. LMS Sequential Learning View: 200 OK`
- `[PASS] 10. Lesson Progress Marked Complete: 200 OK`
- `[PASS] 11. Module MCQ Mock Test Evaluated (70% Pass Required): 200 OK`
- `[PASS] 12. Final Comprehensive Exam & Certificate Generated: 200 OK`
- `[PASS] 13. Public Certificate Registry Verification: 200 OK`
- `[PASS] 14. ReportLab PDF Certificate Download: 200 OK`
- `[PASS] 15. Admin Control Center Stats: 200 OK`
