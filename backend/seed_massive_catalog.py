import os
import sys

# Add backend directory to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.database import SessionLocal, engine, Base
from app.core.security import hash_password
import app.models
from app.models.academic import Category, Degree, Branch
from app.models.user import User
from app.models.skill import Skill
from app.models.user_skill import UserSkillTeach, UserSkillLearn
from app.models.course import Course, CourseModule, Lesson
from app.models.assessment import ModuleAssessment, AssessmentQuestion, AssessmentOption


def seed_massive_catalog():
    print("Starting massive multi-disciplinary course catalog seeding...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # =========================================================================
        # 1. ACADEMIC CATEGORIES, DEGREES, AND BRANCHES (Comprehensive Definition)
        # =========================================================================
        categories_data = [
            {
                "name": "Engineering & Technology",
                "code": "ENG_TECH",
                "icon": "Cpu",
                "degrees": [
                    {
                        "name": "Bachelor of Technology (B.Tech / B.E)",
                        "code": "BTECH",
                        "branches": [
                            "Computer Science & Engineering",
                            "Information Technology",
                            "Artificial Intelligence",
                            "Artificial Intelligence & Machine Learning",
                            "Data Science",
                            "Cyber Security",
                            "Software Engineering",
                            "Electronics & Communication Engineering",
                            "Electrical & Electronics Engineering",
                            "Electrical Engineering",
                            "Mechanical Engineering",
                            "Civil Engineering",
                            "Chemical Engineering",
                            "Biotechnology",
                            "Aerospace Engineering",
                            "Automobile Engineering",
                            "Biomedical Engineering",
                            "Robotics & Automation",
                            "Internet of Things",
                            "Information Science",
                            "Instrumentation Engineering",
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
                            "Thermal Engineering",
                            "Structural Engineering",
                            "AI & Data Analytics"
                        ]
                    },
                    {
                        "name": "Diploma in Engineering (Polytechnic)",
                        "code": "DIPLOMA_ENG",
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
                        "name": "Specialized AI & Emerging Technologies Program",
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
                "name": "Commerce",
                "code": "COMMERCE",
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
                "code": "MGMT_BIZ",
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
                "name": "Science",
                "code": "SCIENCE",
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
                "name": "Arts & Humanities",
                "code": "ARTS_HUM",
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
                            "Geography",
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
                "name": "Architecture",
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
                "name": "Fashion & Design",
                "code": "FASHION_DSGN",
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
                "name": "UI/UX Design",
                "code": "UI_UX",
                "icon": "Layout",
                "degrees": [
                    {
                        "name": "Professional UI/UX & Interaction Design Track",
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
                "code": "LANG_COMM",
                "icon": "Globe",
                "degrees": [
                    {
                        "name": "Global Languages & Programming Syntax Program",
                        "code": "LANG_PROG",
                        "branches": [
                            "Programming Languages Mastery",
                            "Professional English Communication",
                            "French Language & Culture",
                            "German for Engineers",
                            "Spanish Essentials",
                            "Hindi & Regional Languages"
                        ]
                    }
                ]
            }
        ]

        created_categories = {}
        created_degrees = {}
        created_branches = {}

        for cat_info in categories_data:
            cat = db.query(Category).filter(
                (Category.code == cat_info["code"]) | (Category.name == cat_info["name"])
            ).first()
            if not cat:
                cat = Category(name=cat_info["name"], code=cat_info["code"], icon=cat_info["icon"])
                db.add(cat)
                db.flush()
            else:
                cat.icon = cat_info["icon"]
            created_categories[cat_info["code"]] = cat
            created_categories[cat.code] = cat

            for deg_info in cat_info["degrees"]:
                deg = db.query(Degree).filter(
                    (Degree.code == deg_info["code"]) | (Degree.name == deg_info["name"])
                ).first()
                if not deg:
                    deg = Degree(name=deg_info["name"], code=deg_info["code"], category_id=cat.id)
                    db.add(deg)
                    db.flush()
                else:
                    deg.category_id = cat.id
                created_degrees[deg_info["code"]] = deg
                created_degrees[deg.code] = deg

                for br_name in deg_info["branches"]:
                    br_code = f"{deg.code}-{br_name[:4].upper().replace(' ', '')}"
                    br = db.query(Branch).filter(Branch.name == br_name, Branch.degree_id == deg.id).first()
                    if not br:
                        br = Branch(name=br_name, code=br_code, degree_id=deg.id)
                        db.add(br)
                        db.flush()
                    created_branches[br_name] = br

        db.commit()

        # =========================================================================
        # 2. EXTENSIVE SKILLS SEEDING
        # =========================================================================
        skills_catalog = [
            # Programming & Tech
            ("Python", "Engineering & Technology", "Python 3, OOP, scripting, data manipulation, automation"),
            ("Java", "Engineering & Technology", "Core Java, OOPs, Collections, Multi-threading, Spring Boot"),
            ("C Programming", "Engineering & Technology", "Pointers, memory management, structures, low-level algorithms"),
            ("C++", "Engineering & Technology", "STL, templates, OOP, performance systems engineering"),
            ("Data Structures & Algorithms", "Engineering & Technology", "Arrays, Trees, Graphs, Dynamic Programming, Big-O"),
            ("DBMS & SQL", "Engineering & Technology", "Relational database design, normalization, ACID, indexing"),
            ("MySQL", "Engineering & Technology", "MySQL server configuration, query optimization, indexing"),
            ("PostgreSQL", "Engineering & Technology", "Advanced relational modeling, JSONB, concurrency"),
            ("Computer Networks", "Engineering & Technology", "OSI model, TCP/IP, routing protocols, socket programming"),
            ("Operating Systems", "Engineering & Technology", "Process scheduling, virtual memory, concurrency, file systems"),
            ("Software Engineering", "Engineering & Technology", "SDLC, Agile/Scrum, design patterns, software testing"),
            ("Web Development", "Computer Applications", "HTML5, CSS3, JavaScript ES6+, responsive web layouts"),
            ("Full Stack Development", "Computer Applications", "Frontend React, Backend FastAPI/Node, REST APIs, databases"),
            ("React", "Computer Applications", "React 19 hooks, Fiber architecture, state management, Vite"),
            ("Node.js", "Computer Applications", "Event loop, asynchronous I/O, Express.js, RESTful microservices"),
            ("FastAPI", "Engineering & Technology", "Async Python web APIs, Pydantic v2 validation, OpenAPI docs"),
            ("Django", "Engineering & Technology", "MTV architecture, ORM, authentication, Django REST framework"),
            ("Cloud Computing & DevOps", "Engineering & Technology", "Docker, Kubernetes, AWS infrastructure, CI/CD pipelines"),
            ("Cyber Security", "Engineering & Technology", "Network defense, vulnerability assessments, security auditing"),
            ("Ethical Hacking", "Engineering & Technology", "Penetration testing, OWASP Top 10, Burp Suite, exploit analysis"),
            ("Blockchain & Web3", "AI & Emerging Technologies", "Smart contracts, Solidity, Ethereum, decentralized consensus"),
            ("Internet of Things (IoT)", "Engineering & Technology", "Microcontrollers, Arduino, Raspberry Pi, MQTT, sensor networks"),
            ("Embedded Systems", "Engineering & Technology", "Microcontroller architecture, real-time operating systems (RTOS)"),

            # AI & Emerging Technologies
            ("Artificial Intelligence", "AI & Emerging Technologies", "Search algorithms, heuristic evaluation, knowledge representation"),
            ("Machine Learning", "AI & Emerging Technologies", "Supervised/Unsupervised learning, gradient descent, Scikit-Learn"),
            ("Deep Learning", "AI & Emerging Technologies", "Neural networks, backpropagation, CNNs, RNNs, PyTorch"),
            ("Generative AI & LLMs", "AI & Emerging Technologies", "Transformers, multi-head attention, LLM fine-tuning, RAG"),
            ("Prompt Engineering", "AI & Emerging Technologies", "Few-shot prompting, chain-of-thought, system prompts, agents"),
            ("Natural Language Processing (NLP)", "AI & Emerging Technologies", "Tokenization, word embeddings, BERT, transformer models"),
            ("Computer Vision", "AI & Emerging Technologies", "OpenCV, convolutional networks, object detection, YOLO"),
            ("Reinforcement Learning", "AI & Emerging Technologies", "Markov decision processes, Q-learning, policy gradients"),
            ("Data Science & Analytics", "AI & Emerging Technologies", "Pandas, NumPy, statistical modeling, data visualization"),
            ("Big Data Analytics", "AI & Emerging Technologies", "Apache Spark, Hadoop, distributed data pipelines"),
            ("Robotics", "Engineering & Technology", "Kinematics, ROS (Robot Operating System), sensor fusion, control systems"),

            # Commerce & Finance
            ("Financial Accounting", "Commerce", "Double-entry bookkeeping, ledger accounts, trial balance, balance sheets"),
            ("Corporate Accounting", "Commerce", "Share capital accounting, debentures, corporate cash flows"),
            ("Cost & Management Accounting", "Commerce", "Cost sheets, marginal costing, standard costing, budgeting"),
            ("Business Economics", "Commerce", "Demand forecasting, price elasticity, market structures, cost analysis"),
            ("Taxation & GST", "Commerce", "Direct tax deductions, indirect tax, GST input tax credits, return filing"),
            ("Income Tax", "Commerce", "Heads of income, assessment procedures, TDS, tax planning"),
            ("Corporate Auditing", "Commerce", "Internal control systems, audit sampling, statutory compliance"),
            ("Banking & Financial Services", "Commerce", "Commercial banking, credit appraisal, RBI regulations, fintech"),
            ("Business Statistics", "Commerce", "Measures of central tendency, regression, time-series forecasting"),
            ("Entrepreneurship", "Business & Management", "Business models, startup pitch decks, venture capital, Lean Startup"),
            ("E-Commerce Management", "Commerce", "E-commerce business models, payment gateways, supply logistics"),

            # Business & Management
            ("Marketing Management", "Business & Management", "STP framework, marketing mix 4Ps, brand equity, consumer behavior"),
            ("Financial Management", "Business & Management", "Capital budgeting, DCF valuation, working capital, leverage"),
            ("Human Resource Management", "Business & Management", "Talent acquisition, KPI frameworks, organizational culture"),
            ("Operations Management", "Business & Management", "Supply chain logistics, inventory modeling, Lean Six Sigma"),
            ("Strategic Management", "Business & Management", "Porter's 5 Forces, Blue Ocean strategy, corporate governance"),
            ("Business Analytics & Power BI", "Business & Management", "Business intelligence, DAX formulas, interactive dashboards"),
            ("Digital Marketing & SEO", "Business & Management", "Google Ads, SEO keywords, CAC/LTV funnels, social campaigns"),
            ("Project Management", "Business & Management", "Agile methodologies, Gantt scheduling, risk management, PMP"),
            ("Business Communication", "Business & Management", "Executive proposals, Minto Pyramid Principle, cross-cultural diplomacy"),

            # Science & Mathematics
            ("Calculus & Linear Algebra", "Science", "Derivatives, integrals, matrix transformations, eigenvalues, SVD"),
            ("Probability & Mathematical Statistics", "Science", "Distributions, hypothesis testing, Bayes theorem, ANOVA"),
            ("Applied Physics", "Science", "Classical mechanics, wave optics, quantum foundations, thermodynamics"),
            ("Biotechnology & Genetic Engineering", "Science", "Recombinant DNA, PCR, CRISPR gene editing, bioprocessing"),
            ("Microbiology", "Science", "Bacterial genetics, immunology, virology, microbial fermentation"),
            ("Environmental Science", "Science", "Ecosystem dynamics, climate modeling, environmental impact assessments"),

            # Arts & Humanities
            ("Macroeconomics & Fiscal Policy", "Arts & Humanities", "National income GDP, central banking, inflation dynamics"),
            ("Journalism & Mass Communication", "Arts & Humanities", "Investigative reporting, digital media production, media ethics"),
            ("Cognitive Psychology", "Arts & Humanities", "Human cognition, memory models, behavioral neuroscience"),
            ("English Literature & Critical Theory", "Arts & Humanities", "Literary analysis, prose composition, rhetorical analysis"),
            ("Political Science & Governance", "Arts & Humanities", "Constitutional structures, international relations, policy analysis"),
            ("Sociology", "Arts & Humanities", "Social stratification, cultural anthropology, sociological research"),

            # Architecture & Design
            ("Architectural Design & CAD", "Architecture", "Spatial planning, AutoCAD, Revit 3D modeling, building codes"),
            ("Sustainable Architecture", "Architecture", "Passive solar design, green building materials, LEED compliance"),
            ("Fashion Illustration & Apparel Design", "Fashion & Design", "Draping, moodboards, garment pattern engineering"),
            ("Graphic Design & Branding", "Fashion & Design", "Adobe Illustrator, Photoshop, visual identity systems, typography"),

            # UI/UX Design
            ("UI/UX Design", "UI/UX Design", "User-centered design, Double Diamond, Figma prototyping, design systems"),
            ("UX Research & Usability Testing", "UI/UX Design", "User interviews, card sorting, heuristic evaluation, metrics"),
            ("Figma & Design Systems", "UI/UX Design", "Auto-layout, component variants, design tokens, responsive UI"),

            # Languages
            ("Professional English Communication", "Languages & Communication", "Executive presentation, corporate negotiation, technical writing"),
            ("French Language Essentials", "Languages & Communication", "A1-B1 vocabulary, conversational fluency, business French"),
            ("German for Engineers", "Languages & Communication", "Technical German vocabulary, conversational grammar"),
            ("Spanish Essentials", "Languages & Communication", "Everyday conversational Spanish, Latin business culture"),
            ("Telugu Language & Literature", "Languages & Communication", "Classical & contemporary Telugu composition, grammar"),
            ("Hindi Language & Communication", "Languages & Communication", "Official Hindi correspondence, grammar, public speaking")
        ]

        created_skills = {}
        for s_name, cat_name, desc in skills_catalog:
            skill = db.query(Skill).filter(Skill.name == s_name).first()
            if not skill:
                skill = Skill(name=s_name, category_name=cat_name, description=desc)
                db.add(skill)
                db.flush()
            created_skills[s_name] = skill

        db.commit()

        # =========================================================================
        # 3. MASSIVE MULTI-DISCIPLINARY COURSE CATALOG WITH DEEP SYLLABUS & LESSONS
        # =========================================================================
        massive_courses = [
            # ---------------------------------------------------------------------
            # 1. ENGINEERING & TECH: Python Programming Masterclass
            # ---------------------------------------------------------------------
            {
                "title": "Python Programming: Complete Engineering & Architecture",
                "slug": "python-programming-complete-engineering",
                "category_code": "ENG_TECH",
                "degree_code": "BTECH",
                "branch_name": "Computer Science & Engineering",
                "skill_name": "Python",
                "difficulty": "Beginner",
                "duration_hours": 36,
                "thumbnail_url": "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=600",
                "description": "Exhaustive engineering course on Python 3 covering CPython runtime, variable reference model, mutable/immutable data structures, functional paradigms, OOP SOLID design, exception handling, and database integration.",
                "what_you_will_learn": "• CPython execution model, bytecode compilation, and memory references\n• Advanced data structures: lists, dicts, tuples, sets, queues, and heaps\n• Functional programming: lambda, map, filter, closures, and custom decorators with arguments\n• OOP in Python: Dunder methods, inheritance, polymorphism, Abstract Base Classes, and SOLID\n• Exception handling patterns, custom exceptions, and context managers (__enter__/__exit__)\n• Relational database connectivity with MySQL, SQLite, and connection pooling",
                "requirements": "No prior programming experience required. Motivation to master production Python.",
                "modules": [
                    {
                        "title": "Module 1: Python Runtime Architecture, Data Types & Memory Model",
                        "description": "CPython execution, reference counting, variable binding, integer caching, and complex data structures.",
                        "order_index": 1,
                        "lessons": [
                            {
                                "title": "1.1 CPython Bytecode & Dynamic Object References",
                                "content_text": """### 1. CPython Bytecode & Dynamic Object References

Python code is compiled into bytecode (`.pyc`) before execution on the CPython Virtual Machine. Every variable in Python is a reference (pointer) to an object allocated on the heap.

```python
# CPython Memory Optimization: Integer Caching (-5 to 256)
x = 250
y = 250
print(x is y)  # True -> Same memory address

x_large = 1000
y_large = 1000
print(x_large is y_large)  # False -> Distinct heap allocations
```

#### Mutability vs Immutability:
- **Immutable:** `int`, `float`, `str`, `tuple`, `frozenset`.
- **Mutable:** `list`, `dict`, `set`. Mutating a mutable object affects all referencing variables.""",
                                "duration_minutes": 25
                            },
                            {
                                "title": "1.2 Lists, Dicts & Hash Table Time Complexity",
                                "content_text": """### 2. Built-in Data Structures & Big-O Complexity

| Collection | Underlying Structure | Access Time | Insertion (Avg) | Search Time |
| :--- | :--- | :--- | :--- | :--- |
| **List** | Dynamic Array | $O(1)$ | $O(1)$ amortized | $O(N)$ |
| **Tuple** | Fixed Array | $O(1)$ | Immutable | $O(N)$ |
| **Dict** | Compact Hash Map | $O(1)$ | $O(1)$ | $O(1)$ |
| **Set** | Hash Table | N/A | $O(1)$ | $O(1)$ |

#### High-Performance Dict Comprehension:
```python
students = [("Rahul", 88), ("Priya", 95), ("Ananya", 91)]
top_scorers = {name: score for name, score in students if score >= 90}
print(top_scorers)  # {'Priya': 95, 'Ananya': 91}
```""",
                                "duration_minutes": 25
                            }
                        ],
                        "questions": [
                            {"text": "What is the average time complexity for key lookup in a Python dictionary?", "explanation": "Python dictionaries use hash tables offering O(1) average lookup.", "options": [("O(1)", True), ("O(N)", False), ("O(log N)", False), ("O(N^2)", False)]},
                            {"text": "Which built-in Python type is mutable?", "explanation": "Lists, dictionaries, and sets are mutable.", "options": [("List", True), ("Tuple", False), ("String", False), ("Integer", False)]}
                        ]
                    },
                    {
                        "title": "Module 2: Object-Oriented Architecture, Dunder Methods & Design Patterns",
                        "description": "Classes, encapsulation, inheritance MRO, dunder protocols (__str__, __repr__, __eq__), and Abstract Base Classes.",
                        "order_index": 2,
                        "lessons": [
                            {
                                "title": "2.1 Magic Methods & Object Protocols",
                                "content_text": """### 1. Magic Methods (Dunder Protocols) in Python

Python classes customize operator behavior by implementing special dunder methods:

```python
class Vector2D:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __add__(self, other: 'Vector2D') -> 'Vector2D':
        return Vector2D(self.x + other.x, self.y + other.y)

    def __repr__(self) -> str:
        return f"Vector2D(x={self.x}, y={self.y})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector2D):
            return False
        return self.x == other.x and self.y == other.y

v1 = Vector2D(3, 4)
v2 = Vector2D(1, 2)
print(v1 + v2)  # Vector2D(x=4, y=6)
```""",
                                "duration_minutes": 30
                            }
                        ],
                        "questions": [
                            {"text": "Which dunder method enables the addition operator (+) between custom objects?", "explanation": "__add__ implements the binary addition protocol.", "options": [("__add__", True), ("__plus__", False), ("__sum__", False), ("__concat__", False)]}
                        ]
                    }
                ]
            },

            # ---------------------------------------------------------------------
            # 2. ENGINEERING & TECH: Java Enterprise & Spring Boot
            # ---------------------------------------------------------------------
            {
                "title": "Java Enterprise Programming: Core to Spring Boot Microservices",
                "slug": "java-enterprise-spring-boot-microservices",
                "category_code": "ENG_TECH",
                "degree_code": "BTECH",
                "branch_name": "Computer Science & Engineering",
                "skill_name": "Java",
                "difficulty": "Intermediate",
                "duration_hours": 34,
                "thumbnail_url": "https://images.unsplash.com/photo-1517694712202-14dd9538aa97?w=600",
                "description": "Complete enterprise Java curriculum covering JVM architecture, memory model, Java Collections framework, Streams API, multi-threading, concurrency, Spring Boot REST APIs, and JPA/Hibernate.",
                "what_you_will_learn": "• JVM memory structure: Heap, Stack, Metaspace, and Garbage Collection algorithms\n• Java Collections Framework: ArrayList, LinkedList, HashMap, ConcurrentHashMap\n• Functional programming in Java: Lambdas, Functional Interfaces, and Stream API pipelines\n• Multi-threading and Concurrency: Executors, synchronized, ReentrantLocks, and CompletableFuture\n• Spring Boot framework: Dependency Injection, Spring MVC REST controllers, and Spring Data JPA",
                "requirements": "Basic programming fundamentals in any object-oriented language.",
                "modules": [
                    {
                        "title": "Module 1: JVM Memory Architecture & Collections Framework",
                        "description": "Heap vs Stack, Garbage Collection, and Collections Framework internals.",
                        "order_index": 1,
                        "lessons": [
                            {
                                "title": "1.1 JVM Architecture: Heap, Stack & Garbage Collectors",
                                "content_text": """### 1. JVM Architecture & Memory Segments

The Java Virtual Machine (JVM) divides runtime data into:
- **Stack Memory:** Allocates primitive local variables and method call stack frames (thread-private).
- **Heap Memory:** Allocates all objects and instance fields (shared across all threads).
- **Metaspace:** Stores class metadata, bytecode, and method definitions.

```java
// Java Stream API filtering & mapping pipeline
List<String> names = List.of("Rahul", "Priya", "Ananya", "David");
List<String> filtered = names.stream()
    .filter(name -> name.startsWith("P") || name.startsWith("R"))
    .map(String::toUpperCase)
    .toList();
System.out.println(filtered); // [RAHUL, PRIYA]
```""",
                                "duration_minutes": 30
                            }
                        ],
                        "questions": [
                            {"text": "Where are object instances stored in Java runtime memory?", "explanation": "All objects in Java are dynamically allocated on the Heap.", "options": [("Heap Memory", True), ("Stack Memory", False), ("CPU Registers", False), ("Disk Cache", False)]}
                        ]
                    }
                ]
            },

            # ---------------------------------------------------------------------
            # 3. ENGINEERING & TECH: Database Management Systems (DBMS & SQL)
            # ---------------------------------------------------------------------
            {
                "title": "Database Management Systems (DBMS), SQL & Query Optimization",
                "slug": "dbms-sql-mysql-query-optimization",
                "category_code": "ENG_TECH",
                "degree_code": "BTECH",
                "branch_name": "Information Technology",
                "skill_name": "DBMS & SQL",
                "difficulty": "Beginner",
                "duration_hours": 28,
                "thumbnail_url": "https://images.unsplash.com/photo-1544383835-bda2bc66a55d?w=600",
                "description": "Essential database engineering curriculum covering relational modeling, ER diagrams, 1NF to BCNF normalization, ACID transactions, indexing (B+ Trees), complex joins, and query optimization.",
                "what_you_will_learn": "• Relational algebra and Entity-Relationship (ER) architectural modeling\n• Normalization forms: 1NF, 2NF, 3NF, and Boyce-Codd Normal Form (BCNF)\n• SQL mastery: Aggregations, Window Functions, Subqueries, and CTEs\n• Transaction management: Atomicity, Consistency, Isolation, and Durability (ACID)\n• Database indexing: B-Tree and B+ Tree structures, composite indices, and EXPLAIN query plans",
                "requirements": "None.",
                "modules": [
                    {
                        "title": "Module 1: Relational Modeling, Normalization & ACID Transactions",
                        "description": "Functional dependencies, 3NF/BCNF decomposition, and ACID isolation levels.",
                        "order_index": 1,
                        "lessons": [
                            {
                                "title": "1.1 Database Normalization & Functional Dependencies",
                                "content_text": """### 1. Database Normalization (1NF to BCNF)

Normalization eliminates data redundancy and prevents insertion, update, and deletion anomalies.

#### Normal Forms Breakdown:
1. **1NF:** Eliminate repeating groups; ensure all columns contain atomic values.
2. **2NF:** Be in 1NF and ensure every non-prime attribute is fully functionally dependent on the entire primary key (no partial dependencies).
3. **3NF:** Be in 2NF and ensure no transitive functional dependencies ($X \\to Y$ and $Y \\to Z$).
4. **BCNF:** For every non-trivial functional dependency $X \\to Y$, $X$ must be a super key.

```sql
-- Advanced SQL: Window Function for Campus Department Ranking
SELECT 
    student_id,
    name,
    department,
    gpa,
    DENSE_RANK() OVER (PARTITION BY department ORDER BY gpa DESC) AS dept_rank
FROM students;
```""",
                                "duration_minutes": 30
                            }
                        ],
                        "questions": [
                            {"text": "What type of dependency is eliminated in Third Normal Form (3NF)?", "explanation": "3NF removes transitive functional dependencies.", "options": [("Transitive functional dependencies", True), ("Partial dependencies", False), ("Atomic values", False), ("Foreign keys", False)]}
                        ]
                    }
                ]
            },

            # ---------------------------------------------------------------------
            # 4. AI & EMERGING TECH: Generative AI, LLMs & Prompt Engineering
            # ---------------------------------------------------------------------
            {
                "title": "Generative AI, Large Language Models & Prompt Engineering",
                "slug": "generative-ai-large-language-models-prompt-engineering",
                "category_code": "AI_TECH",
                "degree_code": "AI_SPECIAL",
                "branch_name": "Generative AI & LLMs",
                "skill_name": "Generative AI & LLMs",
                "difficulty": "Intermediate",
                "duration_hours": 30,
                "thumbnail_url": "https://images.unsplash.com/photo-1677442136019-21780efad99a?w=600",
                "description": "Cutting-edge curriculum covering Transformer self-attention, Decoder-only architectures (GPT), Prompt Engineering frameworks, Retrieval-Augmented Generation (RAG), and Vector Databases.",
                "what_you_will_learn": "• Transformer architecture: Token embeddings, Positional Encodings, and Self-Attention\n• Prompt engineering strategies: Zero-shot, Few-shot, Chain-of-Thought (CoT), ReAct framework\n• Retrieval-Augmented Generation (RAG): Vector embeddings, Cosine Similarity, and Vector DBs\n• LLM Fine-Tuning: LoRA, QLoRA, and RLHF (Reinforcement Learning from Human Feedback)\n• Autonomous AI Agents: Tool calling, memory systems, and multi-agent orchestration",
                "requirements": "Basic Python and machine learning intuition.",
                "modules": [
                    {
                        "title": "Module 1: Attention Mechanisms & Transformer Decoders",
                        "description": "Scaled dot-product attention, multi-head attention, and autoregressive text generation.",
                        "order_index": 1,
                        "lessons": [
                            {
                                "title": "1.1 The Scaled Dot-Product Attention Equation",
                                "content_text": """### 1. Transformer Self-Attention Architecture

The core of modern LLMs is the Scaled Dot-Product Attention mechanism:

$$\\text{Attention}(\\mathbf{Q}, \\mathbf{K}, \\mathbf{V}) = \\text{softmax}\\left(\\frac{\\mathbf{Q}\\mathbf{K}^T}{\\sqrt{d_k}}\\right)\\mathbf{V}$$

#### Components:
- **Queries ($\\mathbf{Q}$):** Current token representation seeking context.
- **Keys ($\\mathbf{K}$):** Available token representations in the sequence.
- **Values ($\\mathbf{V}$):** The semantic feature payload.
- **$\\sqrt{d_k}$ Scaling:** Prevents softmax saturation in high dimensions.""",
                                "duration_minutes": 30
                            }
                        ],
                        "questions": [
                            {"text": "Why are dot-products scaled by 1/sqrt(d_k) in the Transformer attention mechanism?", "explanation": "Scaling prevents dot products from growing excessively large in high dimensions, preventing small gradients during softmax backprop.", "options": [("To prevent gradients from vanishing in the softmax function", True), ("To convert words to numbers", False), ("To reduce dataset size", False), ("To enable GPU acceleration only", False)]}
                        ]
                    }
                ]
            },

            # ---------------------------------------------------------------------
            # 5. COMMERCE: Taxation, Income Tax & GST Compliance
            # ---------------------------------------------------------------------
            {
                "title": "Taxation, Direct Income Tax & GST Compliance",
                "slug": "taxation-income-tax-gst-compliance",
                "category_code": "COMMERCE",
                "degree_code": "BCOM",
                "branch_name": "Taxation & GST",
                "skill_name": "Taxation & GST",
                "difficulty": "Beginner",
                "duration_hours": 26,
                "thumbnail_url": "https://images.unsplash.com/photo-1554224155-8d04cb21cd6c?w=600",
                "description": "Comprehensive taxation curriculum covering the Indian Income Tax Act, Five Heads of Income, Chapter VI-A deductions, Goods and Services Tax (GST) framework, Input Tax Credit (ITC), and corporate tax filings.",
                "what_you_will_learn": "• The Five Heads of Income: Salaries, House Property, Business/Profession, Capital Gains, Other Sources\n• Chapter VI-A tax deductions (80C, 80D, 80G) and tax rebate calculations\n• Dual GST structure: CGST, SGST, IGST, and taxable event definitions\n• Input Tax Credit (ITC) reconciliation and reverse charge mechanism (RCM)\n• Corporate tax computations, advance tax, TDS, and e-filing return procedures",
                "requirements": "Commerce basics or interest in taxation.",
                "modules": [
                    {
                        "title": "Module 1: Direct Income Tax & Heads of Income",
                        "description": "Residential status, taxable salary computations, and standard deductions.",
                        "order_index": 1,
                        "lessons": [
                            {
                                "title": "1.1 The Five Heads of Income & Taxable Computations",
                                "content_text": """### 1. The Five Heads of Income

Under the Income Tax Act, total gross income is classified into five categories:
1. **Income from Salaries:** Basic pay, allowances, perquisites, less standard deductions.
2. **Income from House Property:** Net Annual Value (NAV) of let-out or self-occupied property less 30% standard deduction and interest on home loans (Section 24).
3. **Profits and Gains of Business or Profession (PGBP):** Revenue minus allowable commercial expenses.
4. **Capital Gains:** Short-term and Long-term gains on transfer of capital assets.
5. **Income from Other Sources:** Interest, dividends, lottery winnings, gifts.""",
                                "duration_minutes": 25
                            }
                        ],
                        "questions": [
                            {"text": "Under the Income Tax framework, what is the standard deduction percentage on Net Annual Value for House Property?", "explanation": "Section 24(a) provides a statutory 30% standard deduction on Net Annual Value.", "options": [("30%", True), ("20%", False), ("50%", False), ("10%", False)]}
                        ]
                    }
                ]
            },

            # ---------------------------------------------------------------------
            # 6. BUSINESS & MANAGEMENT: Marketing Management & Consumer Behavior
            # ---------------------------------------------------------------------
            {
                "title": "Marketing Management, Consumer Behavior & Digital Growth",
                "slug": "marketing-management-consumer-behavior-digital-growth",
                "category_code": "MGMT_BIZ",
                "degree_code": "BBA",
                "branch_name": "Marketing Management",
                "skill_name": "Marketing Management",
                "difficulty": "Beginner",
                "duration_hours": 24,
                "thumbnail_url": "https://images.unsplash.com/photo-1533750516457-a7f992034fec?w=600",
                "description": "BBA & MBA curriculum covering STP strategy (Segmentation, Targeting, Positioning), the 4Ps marketing mix, psychological drivers of consumer decision making, digital growth funnels, and brand equity building.",
                "what_you_will_learn": "• STP Marketing Strategy: Demographic, psychographic, and behavioral segmentation\n• The 4Ps (Product, Price, Place, Promotion) and 7Ps service marketing frameworks\n• Consumer decision-making journeys: Need recognition to post-purchase cognitive dissonance\n• Digital performance marketing: CAC (Customer Acquisition Cost), LTV (Lifetime Value), and ROAS\n• Brand positioning maps, brand identity prisms, and omnichannel campaign design",
                "requirements": "None.",
                "modules": [
                    {
                        "title": "Module 1: Market Segmentation, Targeting & Positioning (STP)",
                        "description": "Market opportunity analysis, positioning statements, and competitive perceptual mapping.",
                        "order_index": 1,
                        "lessons": [
                            {
                                "title": "1.1 The STP Framework & Perceptual Mapping",
                                "content_text": """### 1. Segmentation, Targeting & Positioning (STP)

The STP process creates targeted marketing campaigns:
1. **Segmentation:** Grouping a heterogeneous market into homogeneous clusters (e.g., age, income, lifestyle).
2. **Targeting:** Selecting the most profitable and strategically aligned market segments.
3. **Positioning:** Designing the brand image and value proposition to occupy a distinctive place in the consumer's mind.

$$\\text{Positioning Statement:} \\quad \\text{For } [\\text{Target}], [\\text{Brand}] \\text{ is the } [\\text{Category}] \\text{ that } [\\text{Key Benefit}] \\text{ because } [\\text{Reason to Believe}].$$""",
                                "duration_minutes": 25
                            }
                        ],
                        "questions": [
                            {"text": "What does the 'T' represent in the classic STP marketing framework?", "explanation": "STP stands for Segmentation, Targeting, and Positioning.", "options": [("Targeting", True), ("Technology", False), ("Testing", False), ("Tracking", False)]}
                        ]
                    }
                ]
            },

            # ---------------------------------------------------------------------
            # 7. SCIENCE: Probability & Mathematical Statistics
            # ---------------------------------------------------------------------
            {
                "title": "Probability & Mathematical Statistics for Science & Data",
                "slug": "probability-mathematical-statistics-science-data",
                "category_code": "SCIENCE",
                "degree_code": "BSC",
                "branch_name": "Statistics",
                "skill_name": "Probability & Mathematical Statistics",
                "difficulty": "Intermediate",
                "duration_hours": 28,
                "thumbnail_url": "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=600",
                "description": "B.Sc & M.Sc statistics curriculum covering probability axioms, random variables, discrete and continuous probability distributions (Binomial, Poisson, Gaussian), Central Limit Theorem, and hypothesis testing.",
                "what_you_will_learn": "• Probability axioms, conditional probability, and Bayes' Theorem\n• Discrete distributions: Bernoulli, Binomial, Poisson, and Geometric\n• Continuous distributions: Uniform, Exponential, and Normal (Gaussian) distributions\n• Central Limit Theorem (CLT) and sampling distributions\n• Hypothesis testing: Null vs Alternative hypotheses, Type I/II errors, p-values, t-tests, and ANOVA",
                "requirements": "High school algebra and calculus basics.",
                "modules": [
                    {
                        "title": "Module 1: Probability Foundations, Bayes Theorem & Random Variables",
                        "description": "Sample spaces, independence, Bayes theorem, expected value, and variance.",
                        "order_index": 1,
                        "lessons": [
                            {
                                "title": "1.1 Bayes' Theorem & Conditional Probability",
                                "content_text": """### 1. Bayes' Theorem & Conditional Probability

Bayes' Theorem updates the probability of an event based on new evidence:

$$P(A|B) = \\frac{P(B|A) \\cdot P(A)}{P(B)}$$

- **$P(A)$ (Prior Probability):** Initial belief before observing evidence.
- **$P(B|A)$ (Likelihood):** Probability of observing evidence $B$ given hypothesis $A$.
- **$P(B)$ (Marginal Likelihood):** Total probability of observing evidence $B$.
- **$P(A|B)$ (Posterior Probability):** Updated probability after observing evidence.""",
                                "duration_minutes": 25
                            }
                        ],
                        "questions": [
                            {"text": "What does P(A|B) represent in Bayes' Theorem?", "explanation": "P(A|B) is the posterior probability: the updated probability of event A occurring given that B has occurred.", "options": [("Posterior probability of A given B", True), ("Prior probability of A", False), ("Independent probability of B", False), ("Joint probability of A and B", False)]}
                        ]
                    }
                ]
            },

            # ---------------------------------------------------------------------
            # 8. ARCHITECTURE: Architectural Design, Spatial Planning & CAD
            # ---------------------------------------------------------------------
            {
                "title": "Architectural Design, Spatial Planning & 3D CAD Modeling",
                "slug": "architectural-design-spatial-planning-cad",
                "category_code": "ARCH",
                "degree_code": "BARCH",
                "branch_name": "Architectural Design & Planning",
                "skill_name": "Architectural Design & CAD",
                "difficulty": "Beginner",
                "duration_hours": 30,
                "thumbnail_url": "https://images.unsplash.com/photo-1503387762-592deb58ef4e?w=600",
                "description": "B.Arch curriculum covering spatial layout composition, architectural drawings (plans, elevations, sections), building materials, structural loads, zoning regulations, AutoCAD, and Revit 3D modeling.",
                "what_you_will_learn": "• Architectural design principles: Proportion, scale, rhythm, hierarchy, and harmony\n• Technical drafting: Floor plans, site layouts, elevations, cross-sections, and isometric projections\n• Building materials & construction: Reinforced concrete (RCC), timber, steel, and masonry\n• CAD & BIM workflows: 2D drafting in AutoCAD and parametric 3D modeling in Revit\n• Sustainable passive design: Solar orientation, natural ventilation, and daylighting strategies",
                "requirements": "None.",
                "modules": [
                    {
                        "title": "Module 1: Principles of Spatial Design & Technical Drafting",
                        "description": "Architectural graphics, orthographic projections, and anthropometrics.",
                        "order_index": 1,
                        "lessons": [
                            {
                                "title": "1.1 Orthographic Projections: Plans, Elevations & Sections",
                                "content_text": """### 1. Architectural Orthographic Projections

Architects communicate 3D structures using coordinated 2D orthographic projections:
1. **Floor Plan:** A horizontal cut made at approximately 1.2 meters (4 feet) above the floor looking downward.
2. **Elevation:** An exterior or interior vertical plane projection showing height, materials, and facade fenestration.
3. **Cross-Section:** A vertical cut through the building revealing interior spatial relationships, ceiling heights, and structural thickness.""",
                                "duration_minutes": 25
                            }
                        ],
                        "questions": [
                            {"text": "At what standard height is a building floor plan imaginary horizontal cut line drawn?", "explanation": "Standard architectural drafting convention places the floor plan cutting plane at 1.2 meters (4 feet) above the finished floor.", "options": [("1.2 meters (4 feet)", True), ("3.0 meters (10 feet)", False), ("0.1 meters", False), ("At roof level", False)]}
                        ]
                    }
                ]
            },

            # ---------------------------------------------------------------------
            # 9. FASHION & DESIGN: Fashion Illustration & Apparel Technology
            # ---------------------------------------------------------------------
            {
                "title": "Fashion Illustration, Apparel Design & Textile Engineering",
                "slug": "fashion-illustration-apparel-design-textiles",
                "category_code": "FASHION_DSGN",
                "degree_code": "BDES",
                "branch_name": "Fashion Design & Apparel Technology",
                "skill_name": "Fashion Illustration & Apparel Design",
                "difficulty": "Beginner",
                "duration_hours": 24,
                "thumbnail_url": "https://images.unsplash.com/photo-1558769132-cb1aea458c5e?w=600",
                "description": "B.Des Fashion curriculum covering the 9-head & 10-head fashion croquis figure, moodboard development, textile weave structures (knits vs wovens), garment draping, and trend forecasting.",
                "what_you_will_learn": "• Fashion croquis sketching: 9-head and 10-head proportion figures\n• Textile fundamentals: Natural vs synthetic fibers, plain/twill/satin weaves, and knits\n• Garment pattern making: Flat pattern drafting, dart manipulation, and grading\n• Color palettes, moodboards, and thematic collection storyboarding",
                "requirements": "Drawing tools or digital tablet.",
                "modules": [
                    {
                        "title": "Module 1: The 9-Head Fashion Figure & Textile Fibers",
                        "description": "Croquis proportions, textile classifications, and garment silhouettes.",
                        "order_index": 1,
                        "lessons": [
                            {
                                "title": "1.1 The 9-Head Fashion Croquis Proportion System",
                                "content_text": """### 1. The 9-Head Fashion Croquis Proportion System

Standard human proportion is 7.5 to 8 heads tall. Fashion illustration elongates the figure to 9 heads for dramatic visual silhouette:
- **Head 1:** Crown to Chin.
- **Head 2:** Chin to Bust/Chest line.
- **Head 3:** Bust to Natural Waist.
- **Head 4:** Waist to Hip line / Crotch.
- **Head 5 & 6:** Hip to Knee line.
- **Head 7 & 8:** Knee to Ankle.
- **Head 9:** Ankle to Feet/Toes.""",
                                "duration_minutes": 25
                            }
                        ],
                        "questions": [
                            {"text": "Why do fashion designers use a 9-head proportion system instead of the realistic 7.5 heads?", "explanation": "Elongated proportions emphasize garment drape, flow, and runway silhouette.", "options": [("To create an elongated silhouette emphasizing garment drape", True), ("To match doll dimensions", False), ("Because humans have 9 heads", False), ("To reduce paper usage", False)]}
                        ]
                    }
                ]
            },

            # ---------------------------------------------------------------------
            # 10. UI/UX: Interaction Design & Figma Systems
            # ---------------------------------------------------------------------
            {
                "title": "UI/UX Interaction Design & Figma Systems Mastery",
                "slug": "ui-ux-interaction-design-figma-systems",
                "category_code": "UI_UX",
                "degree_code": "UIUX_PRO",
                "branch_name": "Design Systems & Figma Prototyping",
                "skill_name": "Figma & Design Systems",
                "difficulty": "Beginner",
                "duration_hours": 28,
                "thumbnail_url": "https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?w=600",
                "description": "Complete UI/UX curriculum covering the Double Diamond design process, user personas, wireframing, typography scales, 8pt spatial grids, Figma auto-layout, component variants, and interactive prototyping.",
                "what_you_will_learn": "• The Double Diamond process: Discover, Define, Develop, and Deliver\n• User empathy mapping, persona synthesis, and customer journey mapping\n• Color theory, contrast ratios, and typographic scales for WCAG accessibility\n• Figma mastery: Auto-Layout 5.0, component variants, variables, and design tokens\n• Usability testing heuristics, prototype micro-interactions, and developer handoff",
                "requirements": "Free Figma account.",
                "modules": [
                    {
                        "title": "Module 1: UX Discovery, Information Architecture & Wireframing",
                        "description": "User interviews, affinity mapping, card sorting, and low-fidelity wireframes.",
                        "order_index": 1,
                        "lessons": [
                            {
                                "title": "1.1 Jakob Nielsen's 10 Usability Heuristics",
                                "content_text": """### 1. Jakob Nielsen's 10 Usability Heuristics

Foundational rules for intuitive user interfaces:
1. **Visibility of System Status:** Keep users informed with timely feedback (progress bars, spinners).
2. **Match Between System and Real World:** Use familiar language and real-world metaphors.
3. **User Control and Freedom:** Support undo and redo for accidental actions.
4. **Consistency and Standards:** Follow platform conventions (e.g. standard icons).
5. **Error Prevention:** Eliminate error-prone conditions or confirm before destructive actions.""",
                                "duration_minutes": 25
                            }
                        ],
                        "questions": [
                            {"text": "Which usability heuristic emphasizes providing users with clear undo/redo mechanisms?", "explanation": "User Control and Freedom provides emergency exits for mistaken actions.", "options": [("User Control and Freedom", True), ("Aesthetic and Minimalist Design", False), ("Flexibility of Use", False), ("Help and Documentation", False)]}
                        ]
                    }
                ]
            }
        ]

        for c_info in massive_courses:
            course = db.query(Course).filter(Course.slug == c_info["slug"]).first()
            cat = created_categories.get(c_info["category_code"])
            deg = created_degrees.get(c_info["degree_code"])
            br = created_branches.get(c_info["branch_name"])
            skill = created_skills.get(c_info["skill_name"])

            if not course:
                course = Course(
                    title=c_info["title"],
                    slug=c_info["slug"],
                    category_id=cat.id if cat else 1,
                    degree_id=deg.id if deg else None,
                    branch_id=br.id if br else None,
                    skill_id=skill.id if skill else None,
                    difficulty=c_info["difficulty"],
                    duration_hours=c_info["duration_hours"],
                    thumbnail_url=c_info["thumbnail_url"],
                    description=c_info["description"],
                    what_you_will_learn=c_info["what_you_will_learn"],
                    requirements=c_info["requirements"],
                    instructor_name="SkillSwap Campus Faculty",
                    rating=4.9,
                    enrollment_count=50
                )
                db.add(course)
                db.flush()

                for m_info in c_info["modules"]:
                    mod = CourseModule(
                        course_id=course.id,
                        title=m_info["title"],
                        description=m_info["description"],
                        order_index=m_info["order_index"]
                    )
                    db.add(mod)
                    db.flush()

                    for l_idx, l_info in enumerate(m_info["lessons"], start=1):
                        lesson = Lesson(
                            module_id=mod.id,
                            title=l_info["title"],
                            description=f"Lesson {l_idx} in {mod.title}",
                            content_text=l_info["content_text"],
                            duration_minutes=l_info["duration_minutes"],
                            order_index=l_idx
                        )
                        db.add(lesson)

                    # Module Assessment Mock Test
                    assessment = ModuleAssessment(
                        module_id=mod.id,
                        title=f"Assessment: {mod.title}",
                        description=f"Evaluate your mastery of {mod.title}. Passing score: 70%.",
                        passing_percentage=70.0,
                        time_limit_minutes=15
                    )
                    db.add(assessment)
                    db.flush()

                    for q_idx, q_info in enumerate(m_info["questions"], start=1):
                        question = AssessmentQuestion(
                            assessment_id=assessment.id,
                            question_text=q_info["text"],
                            explanation=q_info["explanation"],
                            marks=1,
                            order_index=q_idx
                        )
                        db.add(question)
                        db.flush()

                        for opt_text, is_corr in q_info["options"]:
                            opt = AssessmentOption(
                                question_id=question.id,
                                option_text=opt_text,
                                is_correct=is_corr
                            )
                            db.add(opt)

        db.commit()
        print("Massive multi-disciplinary course catalog seeding completed successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding catalog: {e}")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed_massive_catalog()
