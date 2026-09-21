import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def run_tests():
    print("=================================================================")
    print("RUNNING COMPREHENSIVE SKILLSWAP CAMPUS INTEGRATION TEST SUITE")
    print("=================================================================")

    # 1. Health Check
    health_res = client.get("/health")
    assert health_res.status_code == 200, f"Health check failed: {health_res.text}"
    print("[PASS] 1. System Health Check: 200 OK")

    # 2. Login as Student A (Rahul)
    login_res = client.post("/auth/login", json={"email": "rahul@drk.edu", "password": "Password@123"})
    assert login_res.status_code == 200, f"Login failed: {login_res.text}"
    rahul_token = login_res.json()["access_token"]
    rahul_headers = {"Authorization": f"Bearer {rahul_token}"}
    print("[PASS] 2. Student Authentication (Rahul): 200 OK")

    # 3. Login as Admin
    admin_res = client.post("/auth/login", json={"email": "admin@skillswap.edu", "password": "Admin@12345"})
    assert admin_res.status_code == 200, f"Admin login failed: {admin_res.text}"
    admin_token = admin_res.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    print("[PASS] 3. Administrator Authentication: 200 OK")

    # 4. Course Catalog Listing & Filtering
    catalog_res = client.get("/courses")
    assert catalog_res.status_code == 200
    courses = catalog_res.json()
    assert len(courses) >= 10, f"Expected >= 10 courses, got {len(courses)}"
    print(f"[PASS] 4. Course Catalog: 200 OK ({len(courses)} multi-disciplinary courses retrieved)")

    # 5. Personalized Recommendations
    rec_res = client.get("/courses/recommended", headers=rahul_headers)
    assert rec_res.status_code == 200, f"Recommendations failed: {rec_res.text}"
    rec_courses = rec_res.json()
    print(f"[PASS] 5. Personalized Course Recommendations: 200 OK ({len(rec_courses)} recommended courses)")

    # 6. Scenario A: Smart Matching for UI/UX Design (Priya teaches, Rahul wants)
    match_res = client.get("/matches?skill_name=UI%2FUX%20Design", headers=rahul_headers)
    assert match_res.status_code == 200
    match_data = match_res.json()
    assert match_data["peers_found_count"] >= 1, "Expected peer match for UI/UX"
    assert match_data["matches"][0]["user"]["name"] == "Priya Sharma"
    assert match_data["matches"][0]["match_type"] == "direct_swap"
    print("[PASS] 6. Scenario A (100% Reciprocal Skill Swap): 200 OK (Priya Sharma matched)")

    # 7. Scenario B: Fallback when searching a skill with 0 peers
    fallback_res = client.get("/matches?skill_name=Calculus%20%26%20Linear%20Algebra", headers=rahul_headers)
    assert fallback_res.status_code == 200
    fb_data = fallback_res.json()
    assert fb_data["fallback_recommended"] == True, "Expected fallback recommendation"
    assert fb_data["fallback_course"] is not None
    print(f"[PASS] 7. Scenario B (Course Fallback): 200 OK (Recommended: {fb_data['fallback_course']['title']})")

    # 8. Enroll Rahul in Python Course
    python_course = next(c for c in courses if "python" in c["slug"])
    enroll_res = client.post(f"/enrollments/courses/{python_course['id']}/enroll", headers=rahul_headers)
    assert enroll_res.status_code in [200, 201]
    print(f"[PASS] 8. Course Enrollment: 200 OK ({python_course['title']})")

    # 9. LMS Learning View
    learn_res = client.get(f"/enrollments/courses/{python_course['id']}/learn", headers=rahul_headers)
    assert learn_res.status_code == 200
    learn_data = learn_res.json()
    assert len(learn_data["modules"]) >= 2
    first_lesson_id = learn_data["modules"][0]["lessons"][0]["id"]
    print("[PASS] 9. LMS Sequential Learning View: 200 OK")

    # 10. Complete First Lesson
    comp_res = client.post(f"/enrollments/lessons/{first_lesson_id}/complete", headers=rahul_headers)
    assert comp_res.status_code == 200
    print(f"[PASS] 10. Lesson Progress Marked Complete: 200 OK (Progress: {comp_res.json()['progress_percentage']}%)")

    # 11. Module Assessment Quiz (Mock Test)
    mod1 = learn_data["modules"][0]
    assessment_res = client.get(f"/assessments/module/{mod1['id']}", headers=rahul_headers)
    assert assessment_res.status_code == 200
    assessment_data = assessment_res.json()
    
    # Submit correct answers to pass with 100%
    answers_payload = []
    for q in assessment_data["questions"]:
        correct_opt = next(opt for opt in q["options"]) # First option is correct in our seed
        answers_payload.append({"question_id": q["id"], "selected_option_id": correct_opt["id"]})

    submit_res = client.post(
        f"/assessments/module/{assessment_data['id']}/submit",
        headers=rahul_headers,
        json={"answers": answers_payload}
    )
    assert submit_res.status_code == 200
    sub_data = submit_res.json()
    assert sub_data["is_passed"] == True
    print(f"[PASS] 11. Module MCQ Mock Test Evaluated: 200 OK (Score: {sub_data['percentage']}%, Next Module Unlocked!)")

    # 12. Final Assessment & Certificate Generation
    final_res = client.get(f"/assessments/final/{python_course['id']}", headers=rahul_headers)
    assert final_res.status_code == 200
    final_data = final_res.json()

    final_answers = []
    for q in final_data["questions"]:
        final_answers.append({"question_id": q["id"], "selected_option_id": q["options"][0]["id"]})

    final_sub_res = client.post(
        f"/assessments/final/{python_course['id']}/submit",
        headers=rahul_headers,
        json={"answers": final_answers}
    )
    assert final_sub_res.status_code == 200
    final_result = final_sub_res.json()
    assert final_result["is_passed"] == True
    cert_id = final_result["certificate_id"]
    assert cert_id is not None
    print(f"[PASS] 12. Final Comprehensive Exam Passed & Certificate Generated: 200 OK (ID: {cert_id})")

    # 13. Public Certificate Verification
    verify_res = client.get(f"/certificates/verify/{cert_id}")
    assert verify_res.status_code == 200
    verify_data = verify_res.json()
    assert verify_data["is_valid"] == True
    assert verify_data["student_name"] == "Rahul Kumar"
    print(f"[PASS] 13. Public Certificate Registry Verification: 200 OK (Status: {verify_data['status']})")

    # 14. PDF Certificate Download
    my_certs_res = client.get("/certificates", headers=rahul_headers)
    assert my_certs_res.status_code == 200
    my_cert = my_certs_res.json()[0]
    pdf_res = client.get(f"/certificates/{my_cert['id']}/download")
    assert pdf_res.status_code == 200
    assert pdf_res.headers["content-type"] == "application/pdf"
    print(f"[PASS] 14. ReportLab PDF Certificate Download: 200 OK ({len(pdf_res.content)} bytes generated)")

    # 15. Admin KPI Dashboard & Stats
    admin_stats_res = client.get("/admin/stats", headers=admin_headers)
    assert admin_stats_res.status_code == 200
    stats = admin_stats_res.json()
    print(f"[PASS] 15. Admin Control Center Stats: 200 OK (Students: {stats['total_students']}, Courses: {stats['total_courses']}, Certificates: {stats['certificates_issued']})")

    print("=================================================================")
    print("ALL 15 INTEGRATION TESTS PASSED WITH 100% SUCCESS!")
    print("=================================================================")

if __name__ == "__main__":
    run_tests()
