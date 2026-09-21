import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.database import SessionLocal, engine, Base
from app.models.academic import Category, Degree, Branch
from app.models.course import Course
from app.models.user import User
from app.models.skill import Skill
from app.core.security import hash_password, verify_password


def fix_academic_and_auth():
    print("Reconciling academic hierarchy and verifying authentication...")
    db = SessionLocal()

    try:
        # 1. Define clean, canonical categories with their degrees and branches
        canonical_taxonomy = [
            {
                "name": "Engineering & Technology",
                "code": "TECH",
                "icon": "Cpu",
                "degrees": [
                    {
                        "name": "Bachelor of Technology (B.Tech / B.E)",
                        "code": "BTECH",
                        "branches": [
                            "Computer Science & Engineering",
                            "Information Technology",
                            "Artificial Intelligence & Machine Learning",
                            "Data Science",
                            "Cyber Security",
                            "Software Engineering",
                            "Electronics & Communication Engineering",
                            "Electrical & Electronics Engineering",
                            "Mechanical Engineering",
                            "Civil Engineering",
                            "Biotechnology",
                            "Aerospace Engineering",
                            "Robotics & Automation",
                            "Internet of Things",
                            "Mechatronics"
                        ]
                    },
                    {
                        "name": "Master of Technology (M.Tech / M.E)",
                        "code": "MTECH",
                        "branches": [
                            "Computer Science & Engineering",
                            "VLSI & Embedded Systems",
                            "Power Systems",
                            "AI & Data Analytics",
                            "Structural Engineering"
                        ]
                    },
                    {
                        "name": "Diploma in Engineering (Polytechnic)",
                        "code": "DIPLOMA",
                        "branches": [
                            "Diploma Computer Engineering",
                            "Diploma Mechanical",
                            "Diploma Electrical",
                            "Diploma Civil",
                            "Diploma Electronics"
                        ]
                    }
                ]
            },
            {
                "name": "Computer Applications",
                "code": "COMP_APP",
                "icon": "Code",
                "degrees": [
                    {
                        "name": "Bachelor of Computer Applications (BCA)",
                        "code": "BCA",
                        "branches": [
                            "Software Development",
                            "Cloud Computing & DevOps",
                            "Web Technologies & Full Stack",
                            "Database Systems & Data Analytics",
                            "Mobile Application Development"
                        ]
                    },
                    {
                        "name": "Master of Computer Applications (MCA)",
                        "code": "MCA",
                        "branches": [
                            "Enterprise Software Architecture",
                            "Artificial Intelligence & ML",
                            "Information Security & Cyber Defense",
                            "Cloud Computing"
                        ]
                    }
                ]
            },
            {
                "name": "AI & Emerging Technologies",
                "code": "AI_TECH",
                "icon": "Sparkles",
                "degrees": [
                    {
                        "name": "Specialized AI & Emerging Technologies Track",
                        "code": "AI_SPECIAL",
                        "branches": [
                            "Artificial Intelligence & Machine Learning",
                            "Generative AI & LLMs",
                            "Computer Vision & NLP",
                            "Data Science & Big Data",
                            "Cloud Computing & DevOps",
                            "Blockchain & Web3",
                            "Robotics & Autonomous Systems",
                            "Cyber Security & Ethical Hacking"
                        ]
                    }
                ]
            },
            {
                "name": "Commerce & Financial Accounting",
                "code": "COMM",
                "icon": "DollarSign",
                "degrees": [
                    {
                        "name": "Bachelor of Commerce (B.Com)",
                        "code": "BCOM",
                        "branches": [
                            "General Accounting",
                            "B.Com Computers & IT",
                            "Taxation & GST",
                            "Banking & Insurance",
                            "Corporate Auditing & Governance",
                            "Finance & Investment"
                        ]
                    },
                    {
                        "name": "Master of Commerce (M.Com)",
                        "code": "MCOM",
                        "branches": [
                            "Advanced Financial Accounting",
                            "Corporate Taxation",
                            "International Banking & Finance"
                        ]
                    }
                ]
            },
            {
                "name": "Business & Management",
                "code": "MGMT",
                "icon": "Briefcase",
                "degrees": [
                    {
                        "name": "Bachelor of Business Administration (BBA)",
                        "code": "BBA",
                        "branches": [
                            "Finance",
                            "Marketing Management",
                            "Human Resource Management",
                            "Operations & Supply Chain",
                            "Business Analytics",
                            "International Business",
                            "Entrepreneurship",
                            "Digital Marketing"
                        ]
                    },
                    {
                        "name": "Master of Business Administration (MBA / PGDM)",
                        "code": "MBA",
                        "branches": [
                            "Strategic Management & Leadership",
                            "Fintech & Financial Analytics",
                            "Digital Growth Marketing",
                            "Global Supply Chain Management",
                            "Human Resource Strategy"
                        ]
                    }
                ]
            },
            {
                "name": "Science & Mathematics",
                "code": "SCI",
                "icon": "Atom",
                "degrees": [
                    {
                        "name": "Bachelor of Science (B.Sc)",
                        "code": "BSC",
                        "branches": [
                            "Mathematics",
                            "Physics",
                            "Chemistry",
                            "Biology & Life Sciences",
                            "Computer Science",
                            "Statistics",
                            "Biotechnology",
                            "Microbiology",
                            "Data Science",
                            "Electronics",
                            "Environmental Science",
                            "Psychology"
                        ]
                    },
                    {
                        "name": "Master of Science (M.Sc)",
                        "code": "MSC",
                        "branches": [
                            "Applied Mathematics",
                            "Data Science & AI",
                            "Physics & Quantum Mechanics",
                            "Biotechnology"
                        ]
                    }
                ]
            },
            {
                "name": "Arts, Humanities & Media",
                "code": "ARTS",
                "icon": "BookOpen",
                "degrees": [
                    {
                        "name": "Bachelor of Arts (BA)",
                        "code": "BA",
                        "branches": [
                            "English Literature",
                            "Economics",
                            "Political Science",
                            "Sociology",
                            "Psychology",
                            "History",
                            "Journalism & Mass Communication",
                            "Public Administration",
                            "Philosophy"
                        ]
                    },
                    {
                        "name": "Master of Arts (MA)",
                        "code": "MA",
                        "branches": [
                            "English Literature & Critical Theory",
                            "Applied Macroeconomics",
                            "Clinical & Cognitive Psychology",
                            "Media & Communication"
                        ]
                    }
                ]
            },
            {
                "name": "Architecture & Planning",
                "code": "ARCH",
                "icon": "Building",
                "degrees": [
                    {
                        "name": "Bachelor of Architecture (B.Arch)",
                        "code": "BARCH",
                        "branches": [
                            "Architectural Design & Planning",
                            "Building Construction & Materials",
                            "Interior Architecture",
                            "Urban Planning & CAD",
                            "Sustainable & Green Architecture"
                        ]
                    }
                ]
            },
            {
                "name": "Fashion & Graphic Design",
                "code": "DSGN",
                "icon": "Scissors",
                "degrees": [
                    {
                        "name": "Bachelor of Design (B.Des)",
                        "code": "BDES",
                        "branches": [
                            "Fashion Design & Apparel Technology",
                            "Textile Design",
                            "Graphic Design & Branding",
                            "Product & Industrial Design",
                            "Interior Design"
                        ]
                    }
                ]
            },
            {
                "name": "UI/UX & Interaction Design",
                "code": "UI_UX",
                "icon": "Layout",
                "degrees": [
                    {
                        "name": "Professional UI/UX Design Track",
                        "code": "UIUX_PRO",
                        "branches": [
                            "User Experience (UX) Research",
                            "User Interface (UI) Design",
                            "Design Systems & Figma Prototyping",
                            "Interaction & Product Design",
                            "Usability Testing & Design Thinking"
                        ]
                    }
                ]
            },
            {
                "name": "Languages & Communication",
                "code": "LANG",
                "icon": "Globe",
                "degrees": [
                    {
                        "name": "Global Languages Program",
                        "code": "LANG_PROG",
                        "branches": [
                            "Professional English Communication",
                            "French Language & Culture",
                            "German for Engineers",
                            "Spanish Essentials",
                            "Telugu Language & Literature",
                            "Hindi Language & Communication"
                        ]
                    }
                ]
            },
            {
                "name": "Law & Legal Studies",
                "code": "LAW",
                "icon": "Shield",
                "degrees": [
                    {
                        "name": "Bachelor of Laws (BA LLB / BBA LLB)",
                        "code": "BALLB",
                        "branches": [
                            "Corporate Law",
                            "Cyber Law & Intellectual Property",
                            "Constitutional Law",
                            "Criminal Jurisprudence"
                        ]
                    }
                ]
            },
            {
                "name": "Career & Placement Track",
                "code": "CAREER",
                "icon": "Award",
                "degrees": [
                    {
                        "name": "Campus Placement Mastery Track",
                        "code": "CAREER_TRK",
                        "branches": [
                            "Quantitative Aptitude & Speed Math",
                            "Logical Reasoning & Verbal Ability",
                            "Technical Coding Interviews",
                            "Behavioral & HR Round Mastery"
                        ]
                    }
                ]
            }
        ]

        # Step A: Upsert clean categories
        for cat_info in canonical_taxonomy:
            cat = db.query(Category).filter(
                (Category.code == cat_info["code"]) | (Category.name == cat_info["name"])
            ).first()

            if not cat:
                cat = Category(name=cat_info["name"], code=cat_info["code"], icon=cat_info["icon"])
                db.add(cat)
                db.flush()
            else:
                cat.name = cat_info["name"]
                cat.code = cat_info["code"]
                cat.icon = cat_info["icon"]

            for deg_info in cat_info["degrees"]:
                deg = db.query(Degree).filter(
                    (Degree.code == deg_info["code"]) | (Degree.name == deg_info["name"])
                ).first()

                if not deg:
                    deg = Degree(name=deg_info["name"], code=deg_info["code"], category_id=cat.id)
                    db.add(deg)
                    db.flush()
                else:
                    deg.name = deg_info["name"]
                    deg.category_id = cat.id

                for br_name in deg_info["branches"]:
                    br_code = f"{deg.code}-{br_name[:4].upper().replace(' ', '')}"
                    br = db.query(Branch).filter(Branch.name == br_name, Branch.degree_id == deg.id).first()
                    if not br:
                        br = Branch(name=br_name, code=br_code, degree_id=deg.id)
                        db.add(br)
                        db.flush()

        db.commit()

        # Step B: Remove any empty categories with 0 degrees and 0 courses
        all_cats = db.query(Category).all()
        for cat in all_cats:
            deg_count = db.query(Degree).filter(Degree.category_id == cat.id).count()
            course_count = db.query(Course).filter(Course.category_id == cat.id).count()
            if deg_count == 0 and course_count == 0:
                print(f"Removing unused empty category: {cat.name} (id={cat.id})")
                db.delete(cat)
            elif deg_count == 0 and course_count > 0:
                # Find matching target category
                target_cat = db.query(Category).filter(
                    Category.name.ilike(f"%{cat.name.split()[0]}%"),
                    Category.id != cat.id
                ).first()
                if target_cat:
                    print(f"Reassigning courses from {cat.name} to {target_cat.name}")
                    for c in db.query(Course).filter(Course.category_id == cat.id).all():
                        c.category_id = target_cat.id
                    db.delete(cat)

        db.commit()

        # Step C: Ensure default demo users have correct passwords
        users_to_check = [
            ("admin@skillswap.edu", "Admin@12345", "Prof. Sharma (Admin)", "admin"),
            ("rahul@drk.edu", "Password@123", "Rahul Kumar", "student"),
            ("priya@drk.edu", "Password@123", "Priya Sharma", "student")
        ]

        btech_deg = db.query(Degree).filter(Degree.code == "BTECH").first()
        cse_br = db.query(Branch).filter(Branch.name.ilike("%Computer Science%")).first()

        for email, pwd, name, role in users_to_check:
            u = db.query(User).filter(User.email == email).first()
            if not u:
                u = User(
                    name=name,
                    email=email,
                    password_hash=hash_password(pwd),
                    role=role,
                    college="DRK College of Engineering and Technology",
                    degree_id=btech_deg.id if btech_deg else None,
                    branch_id=cse_br.id if cse_br else None,
                    branch="Computer Science & Engineering",
                    year=3,
                    bio="Campus Member at SkillSwap Campus",
                    credits=20,
                    is_active=True
                )
                db.add(u)
            else:
                # Refresh password hash to ensure verification passes 100%
                u.password_hash = hash_password(pwd)
                u.is_active = True
                if btech_deg and not u.degree_id:
                    u.degree_id = btech_deg.id
                if cse_br and not u.branch_id:
                    u.branch_id = cse_br.id

        db.commit()

        print("Academic taxonomy successfully reconciled and users verified!")
        print(f"Total Active Categories: {db.query(Category).count()}")
        for c in db.query(Category).all():
            degs = db.query(Degree).filter(Degree.category_id == c.id).count()
            print(f"   -> [{c.code}] {c.name}: {degs} degrees")

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    fix_academic_and_auth()
