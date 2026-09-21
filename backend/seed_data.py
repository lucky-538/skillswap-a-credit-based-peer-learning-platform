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


def seed_database():
    print("Seeding database with comprehensive multi-disciplinary academic disciplines, skills, courses, modules, and lessons...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. ACADEMIC CATEGORIES, DEGREES, AND BRANCHES (Supporting all 15+ disciplines)
        categories_data = [
            {
                "name": "Technology & Engineering",
                "code": "TECH",
                "icon": "Code",
                "degrees": [
                    {"name": "Bachelor of Technology (B.Tech)", "code": "BTECH", "branches": ["Computer Science & Engineering", "Information Technology", "Artificial Intelligence & ML", "Cybersecurity", "Data Science", "Electronics & Communication (ECE)", "Electrical Engineering (EEE)", "Mechanical Engineering", "Civil Engineering"]},
                    {"name": "Bachelor of Computer Applications (BCA)", "code": "BCA", "branches": ["Software Development", "Cloud Computing", "Web Technologies", "Database Systems"]},
                    {"name": "Master of Computer Applications (MCA)", "code": "MCA", "branches": ["Enterprise Software Architecture", "Artificial Intelligence", "Information Security"]}
                ]
            },
            {
                "name": "Commerce & Financial Accounting",
                "code": "COMM",
                "icon": "DollarSign",
                "degrees": [
                    {"name": "Bachelor of Commerce (B.Com)", "code": "BCOM", "branches": ["General Accounting", "Computers & IT", "Taxation & GST", "Banking & Insurance", "Corporate Auditing"]},
                    {"name": "Master of Commerce (M.Com)", "code": "MCOM", "branches": ["Advanced Accounting", "Financial Economics", "International Taxation"]}
                ]
            },
            {
                "name": "Business & Management",
                "code": "MGMT",
                "icon": "Briefcase",
                "degrees": [
                    {"name": "Bachelor of Business Administration (BBA)", "code": "BBA", "branches": ["Finance", "Marketing Management", "Human Resources", "International Business", "Business Analytics", "Operations & Supply Chain"]},
                    {"name": "Master of Business Administration (MBA)", "code": "MBA", "branches": ["Strategic Leadership", "Fintech & Analytics", "Digital Marketing", "Entrepreneurship"]}
                ]
            },
            {
                "name": "Science & Mathematics",
                "code": "SCI",
                "icon": "Atom",
                "degrees": [
                    {"name": "Bachelor of Science (B.Sc)", "code": "BSC", "branches": ["Mathematics", "Physics", "Chemistry", "Statistics", "Computer Science", "Data Analytics"]},
                    {"name": "Master of Science (M.Sc)", "code": "MSC", "branches": ["Applied Mathematics", "Data Science & AI", "Quantum Physics"]}
                ]
            },
            {
                "name": "Design, Arts & Architecture",
                "code": "DSGN",
                "icon": "Palette",
                "degrees": [
                    {"name": "Bachelor of Design (B.Des)", "code": "BDES", "branches": ["UI/UX Interaction Design", "Graphic & Brand Design", "Fashion & Apparel Design", "Animation & VFX", "Product Design"]},
                    {"name": "Bachelor of Architecture (B.Arch)", "code": "BARCH", "branches": ["Architectural Design", "Interior Architecture", "Urban Planning & CAD"]}
                ]
            },
            {
                "name": "Arts, Humanities & Media",
                "code": "ARTS",
                "icon": "BookOpen",
                "degrees": [
                    {"name": "Bachelor of Arts (BA)", "code": "BA", "branches": ["English Literature", "Economics", "Psychology", "Political Science", "Sociology", "History"]},
                    {"name": "BA in Journalism & Mass Communication (BJMC)", "code": "BJMC", "branches": ["Print & Digital Journalism", "Broadcasting & Podcasting", "Content Strategy & PR"]}
                ]
            },
            {
                "name": "Law & Legal Studies",
                "code": "LAW",
                "icon": "Shield",
                "degrees": [
                    {"name": "Bachelor of Laws (BA LLB / BBA LLB)", "code": "BALLB", "branches": ["Corporate Law", "Cyber Law & Intellectual Property", "Constitutional Law", "Criminal Jurisprudence"]}
                ]
            },
            {
                "name": "Career & Placement Development",
                "code": "CAREER",
                "icon": "Award",
                "degrees": [
                    {"name": "Campus Placement & Career Track", "code": "CAREER_TRK", "branches": ["Quantitative Aptitude", "Logical Reasoning & Verbal Ability", "Technical Coding Interviews", "Executive Communication"]}
                ]
            },
            {
                "name": "Languages & Communication",
                "code": "LANG",
                "icon": "Globe",
                "degrees": [
                    {"name": "Global Languages Program", "code": "GLANG", "branches": ["Professional English", "German", "French", "Spanish", "Hindi", "Telugu"]}
                ]
            }
        ]

        created_categories = {}
        created_degrees = {}
        created_branches = {}

        for cat_info in categories_data:
            cat = db.query(Category).filter(Category.code == cat_info["code"]).first()
            if not cat:
                cat = Category(name=cat_info["name"], code=cat_info["code"], icon=cat_info["icon"])
                db.add(cat)
                db.flush()
            created_categories[cat.code] = cat

            for deg_info in cat_info["degrees"]:
                deg = db.query(Degree).filter(Degree.code == deg_info["code"]).first()
                if not deg:
                    deg = Degree(name=deg_info["name"], code=deg_info["code"], category_id=cat.id)
                    db.add(deg)
                    db.flush()
                created_degrees[deg.code] = deg

                for br_name in deg_info["branches"]:
                    br_code = f"{deg.code}-{br_name[:4].upper().replace(' ', '')}"
                    br = db.query(Branch).filter(Branch.name == br_name, Branch.degree_id == deg.id).first()
                    if not br:
                        br = Branch(name=br_name, code=br_code, degree_id=deg.id)
                        db.add(br)
                        db.flush()
                    created_branches[br_name] = br

        # 2. SKILLS CATALOG (Expanded across all disciplines)
        skills_seed = [
            ("Python", "Technology & Engineering", "Python 3, OOP, scripting, data manipulation, automation"),
            ("Java", "Technology & Engineering", "Core Java, OOPs, Collections, Spring Framework"),
            ("C & C++", "Technology & Engineering", "Memory management, pointers, STL, low-level systems programming"),
            ("SQL & MySQL", "Technology & Engineering", "Relational database queries, indexing, normalization"),
            ("React & TypeScript", "Technology & Engineering", "Frontend development, React hooks, state management, Vite"),
            ("FastAPI & Python Web", "Technology & Engineering", "Modern asynchronous Python backend API framework"),
            ("Machine Learning", "Technology & Engineering", "Supervised learning, neural networks, Scikit-Learn, PyTorch"),
            ("Cybersecurity Fundamentals", "Technology & Engineering", "Network security, cryptography, vulnerability assessment"),
            ("Cloud Computing & DevOps", "Technology & Engineering", "Docker, Kubernetes, AWS fundamentals, CI/CD pipelines"),
            ("Data Structures & Algorithms", "Technology & Engineering", "Arrays, Trees, Graphs, Dynamic Programming, Complexity Analysis"),
            ("UI/UX Design", "Design, Arts & Architecture", "Figma, wireframing, user research, interaction design"),
            ("Graphic Design", "Design, Arts & Architecture", "Adobe Photoshop, Illustrator, visual branding, typography"),
            ("Fashion Illustration & Styling", "Design, Arts & Architecture", "Apparel design sketching, mood boards, fabric styling"),
            ("Architectural CAD & 3D Modeling", "Design, Arts & Architecture", "AutoCAD, Revit, spatial layouts, 3D architectural rendering"),
            ("Financial Accounting", "Commerce & Financial Accounting", "Balance sheets, ledger entries, financial statements"),
            ("Taxation & GST", "Commerce & Financial Accounting", "Direct tax, indirect tax, GST compliance, returns"),
            ("Corporate Auditing & Governance", "Commerce & Financial Accounting", "Internal controls, risk auditing, compliance standards"),
            ("Digital Marketing & SEO", "Business & Management", "Google Ads, SEO optimization, social media strategy"),
            ("Business Analytics & Excel", "Business & Management", "Excel modeling, Power BI, data-driven decision making"),
            ("Strategic Leadership & Entrepreneurship", "Business & Management", "Business models, venture creation, team leadership"),
            ("Macroeconomics & Policy", "Arts, Humanities & Media", "Market dynamics, monetary policy, GDP, inflation"),
            ("Journalism & Content Strategy", "Arts, Humanities & Media", "Investigative reporting, podcasting, digital storytelling"),
            ("Cognitive Psychology", "Arts, Humanities & Media", "Human behavior, perception, cognition, social dynamics"),
            ("Corporate & Cyber Law", "Law & Legal Studies", "Contract drafting, IP law, cyber jurisprudence, compliance"),
            ("Calculus & Linear Algebra", "Science & Mathematics", "Derivatives, integrals, matrix transformations, vector calculus"),
            ("Probability & Statistics", "Science & Mathematics", "Distributions, hypothesis testing, regression analysis"),
            ("Quantitative Aptitude & Reasoning", "Career & Placement Development", "Speed math, logical reasoning, competitive exams"),
            ("Interview Preparation & Resume Building", "Career & Placement Development", "ATS resumes, behavioral interview mastery, HR rounds"),
            ("Professional English Communication", "Languages & Communication", "Business writing, executive presentations, professional vocabulary"),
            ("Public Speaking & Presentation", "Languages & Communication", "Confidence building, pitch delivery, stage presence")
        ]

        created_skills = {}
        for s_name, cat_name, desc in skills_seed:
            skill = db.query(Skill).filter(Skill.name == s_name).first()
            if not skill:
                skill = Skill(name=s_name, category_name=cat_name, description=desc)
                db.add(skill)
                db.flush()
            created_skills[s_name] = skill

        # 3. USERS (Admin + Demo Students)
        admin_user = db.query(User).filter(User.email == "admin@skillswap.edu").first()
        if not admin_user:
            admin_user = User(
                name="Prof. Sharma (Admin)",
                email="admin@skillswap.edu",
                password_hash=hash_password("Admin@12345"),
                role="admin",
                college="DRK College of Engineering and Technology",
                branch="Computer Science & Engineering",
                year=4,
                bio="Administrator & Academic Dean of SkillSwap Campus platform.",
                credits=100
            )
            db.add(admin_user)

        # Student A: Rahul Kumar
        rahul = db.query(User).filter(User.email == "rahul@drk.edu").first()
        if not rahul:
            rahul = User(
                name="Rahul Kumar",
                email="rahul@drk.edu",
                password_hash=hash_password("Password@123"),
                role="student",
                college="DRK College of Engineering and Technology",
                branch="Computer Science & Engineering",
                year=3,
                bio="Passionate Python developer building web and data applications. Love teaching programming fundamentals.",
                avatar_url="https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150",
                credits=15,
                reputation_score=4.9
            )
            db.add(rahul)
            db.flush()
            db.add(UserSkillTeach(user_id=rahul.id, skill_id=created_skills["Python"].id, proficiency_level="Advanced", experience_description="Built 10+ projects in Python and Django/FastAPI"))
            db.add(UserSkillTeach(user_id=rahul.id, skill_id=created_skills["SQL & MySQL"].id, proficiency_level="Intermediate", experience_description="Database design and complex query optimization"))
            db.add(UserSkillLearn(user_id=rahul.id, skill_id=created_skills["UI/UX Design"].id, desired_level="Beginner", notes="Want to learn Figma and design clean mobile apps"))
            db.add(UserSkillLearn(user_id=rahul.id, skill_id=created_skills["Public Speaking & Presentation"].id, desired_level="Intermediate", notes="Preparing for college fest presentations"))

        # Student B: Priya Sharma
        priya = db.query(User).filter(User.email == "priya@drk.edu").first()
        if not priya:
            priya = User(
                name="Priya Sharma",
                email="priya@drk.edu",
                password_hash=hash_password("Password@123"),
                role="student",
                college="DRK College of Engineering and Technology",
                branch="Computer Science & Engineering",
                year=3,
                bio="UI/UX and visual designer passionate about user-centric product interfaces and prototyping.",
                avatar_url="https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150",
                credits=20,
                reputation_score=4.8
            )
            db.add(priya)
            db.flush()
            db.add(UserSkillTeach(user_id=priya.id, skill_id=created_skills["UI/UX Design"].id, proficiency_level="Expert", experience_description="Designed design systems in Figma and published case studies"))
            db.add(UserSkillTeach(user_id=priya.id, skill_id=created_skills["Graphic Design"].id, proficiency_level="Advanced", experience_description="Adobe Illustrator, branding, and typography"))
            db.add(UserSkillLearn(user_id=priya.id, skill_id=created_skills["Python"].id, desired_level="Beginner", notes="Want to learn Python for backend integration and data visualization"))

        # 4. COMPREHENSIVE COURSES ACROSS ALL DISCIPLINES WITH IN-DEPTH CONTENT
        courses_database = [
            # --- 1. TECHNOLOGY & COMPUTING ---
            {
                "title": "Python Programming: Core to Advanced Architecture",
                "slug": "python-programming-core-architecture",
                "category_code": "TECH",
                "skill_name": "Python",
                "difficulty": "Beginner",
                "duration_hours": 30,
                "thumbnail_url": "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=600",
                "description": "Comprehensive engineering curriculum covering Python syntax, memory model, data structures, functional paradigms, OOP, generators, decorators, and asynchronous programming.",
                "what_you_will_learn": "• Deep understanding of Python runtime, CPython memory allocation, and GIL\n• Mastery of built-in data structures: lists, dicts, sets, tuples, and heaps\n• Functional programming with lambda, map, filter, functools, and closures\n• Metaprogramming, decorators with arguments, and custom context managers\n• Object-Oriented architecture: SOLID principles, Dunder methods, and Abstract Base Classes\n• Asynchronous programming using AsyncIO, coroutines, and event loops",
                "requirements": "No prior programming experience required. Motivation to master production Python.",
                "modules": [
                    {
                        "title": "Module 1: Python Fundamentals, Memory Architecture & Data Structures",
                        "description": "Exploration of Python execution model, reference counting, variable binding, mutable vs immutable types, and list/dict comprehensions.",
                        "order_index": 1,
                        "lessons": [
                            {
                                "title": "1.1 The CPython Execution Model & Variable Binding",
                                "content_text": """### 1. The CPython Execution Model & Variable Binding

Python is an interpreted, dynamically-typed language executed by the CPython virtual machine. When a script runs, Python first compiles the source code (`.py`) into bytecode (`.pyc`), which is subsequently interpreted by the virtual machine stack.

#### Variables as Pointers to Objects
In Python, variables are not memory containers with fixed addresses; they are **names (references)** bound to objects allocated on the heap:

```python
# a and b point to the exact same integer object in memory
a = 256
b = 256
print(a is b)  # True (Integer caching optimization for -5 to 256)

c = 1000
d = 1000
print(c is d)  # False (Distinct objects created in memory)
```

#### Mutability vs Immutability
Understanding mutability is crucial for bug-free code:
- **Immutable Types:** `int`, `float`, `str`, `tuple`, `frozenset`, `bytes`. Modifying them creates a new object.
- **Mutable Types:** `list`, `dict`, `set`, `bytearray`. They can be altered in-place.

```python
def append_item(item, target_list=[]):  # DANGEROUS: Default mutable argument!
    target_list.append(item)
    return target_list

print(append_item(1))  # [1]
print(append_item(2))  # [1, 2] -> Shared across function calls!

# CORRECT IDIOM:
def safe_append(item, target_list=None):
    if target_list is None:
        target_list = []
    target_list.append(item)
    return target_list
```""",
                                "duration_minutes": 25
                            },
                            {
                                "title": "1.2 Advanced Data Structures & Memory Complexity",
                                "content_text": """### 2. Advanced Data Structures & Memory Complexity

Python provides high-performance built-in collections. Understanding their time and space complexity is foundational for writing scalable applications.

#### Lists vs Tuples vs Sets vs Dictionaries
| Data Structure | Underlying Architecture | Access Time | Insertion (Avg) | Search Time |
| :--- | :--- | :--- | :--- | :--- |
| **List** | Dynamic Array | $O(1)$ | $O(1)$ amortized | $O(N)$ |
| **Tuple** | Fixed-size Array | $O(1)$ | N/A (Immutable) | $O(N)$ |
| **Set** | Hash Table | N/A | $O(1)$ | $O(1)$ |
| **Dict** | Compact Hash Table | $O(1)$ | $O(1)$ | $O(1)$ |

#### High-Performance Comprehensions
Comprehensions execute in C-speed inside the interpreter loop:

```python
# Matrix transposition using list comprehension
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
transposed = [[row[i] for row in matrix] for i in range(3)]
print(transposed)  # [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

# Dictionary comprehension for fast lookups
users = [{"id": 1, "name": "Rahul"}, {"id": 2, "name": "Priya"}]
user_lookup = {u["id"]: u["name"] for u in users}
print(user_lookup[2])  # "Priya" (Instant O(1) hash lookup)
```""",
                                "duration_minutes": 30
                            }
                        ],
                        "questions": [
                            {"text": "What happens in Python when you define a default mutable argument like `def func(x=[])`?", "explanation": "Default arguments are evaluated once at function definition time, so the list object is shared across all subsequent invocations.", "options": [("The list is shared across all calls causing state leakage", True), ("A new list is created on every call", False), ("Python raises a SyntaxError", False), ("The argument is deleted after execution", False)]},
                            {"text": "Which collection provides $O(1)$ average time complexity for element lookup?", "explanation": "Sets and Dictionaries utilize hash tables allowing constant time O(1) key lookups.", "options": [("Set / Dictionary", True), ("List", False), ("Tuple", False), ("Linked Array", False)]},
                            {"text": "What operator tests whether two variables point to the exact same object in memory?", "explanation": "The 'is' keyword evaluates identity (memory address), while '==' evaluates equality of values.", "options": [("is", True), ("==", False), ("equals()", False), ("matches", False)]}
                        ]
                    },
                    {
                        "title": "Module 2: Functional Paradigms, Closures & Custom Decorators",
                        "description": "Deep dive into closures, higher-order functions, custom decorators with arguments, `functools.wraps`, and context managers.",
                        "order_index": 2,
                        "lessons": [
                            {
                                "title": "2.1 Closures & Higher-Order Functions",
                                "content_text": """### 1. Closures & Higher-Order Functions

A function in Python is a **first-class citizen**, meaning it can be passed as an argument, returned from other functions, and assigned to variables.

#### What is a Closure?
A closure is an inner function that remembers and retains access to variables in its enclosing lexical scope even after the outer function has finished executing:

```python
def make_multiplier(factor):
    # 'factor' is enclosed in the inner function's environment
    def multiplier(number):
        return number * factor
    return multiplier

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(10))  # 20
print(triple(10))  # 30
```""",
                                "duration_minutes": 25
                            },
                            {
                                "title": "2.2 Production Decorators with Arguments & Context Managers",
                                "content_text": """### 2. Production Decorators & Context Managers

Decorators provide clean metaprogramming by wrapping functions with reusable cross-cutting concerns (logging, authentication, timing, caching).

#### Implementing a Parameterized Execution Timer Decorator:
```python
import time
from functools import wraps

def retry(max_attempts=3, delay_seconds=1):
    def decorator(func):
        @wraps(func)  # Preserves function name, docstring and signature
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as err:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise err
                    time.sleep(delay_seconds)
        return wrapper
    return decorator

@retry(max_attempts=3, delay_seconds=0.5)
def fetch_campus_database():
    print("Attempting connection...")
    # Network or database call
    return "Connected!"
```

#### Custom Context Managers (`__enter__` and `__exit__`)
```python
class DatabaseTransaction:
    def __init__(self, session):
        self.session = session

    def __enter__(self):
        print("Starting transaction...")
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print("Exception detected! Rolling back changes.")
            self.session.rollback()
            return False  # Propagate exception
        print("Committing transaction...")
        self.session.commit()
```""",
                                "duration_minutes": 30
                            }
                        ],
                        "questions": [
                            {"text": "Why should you always apply `@functools.wraps(func)` inside a decorator wrapper?", "explanation": "@wraps preserves the original function's name, docstring, and metadata which would otherwise be overwritten by the wrapper.", "options": [("To preserve the original function's name and metadata", True), ("To make the function run 10x faster", False), ("To prevent memory allocation", False), ("To enable async execution", False)]},
                            {"text": "Which two dunder methods are required to implement a custom Context Manager class?", "explanation": "__enter__ and __exit__ define the entry and cleanup protocols for 'with' statements.", "options": [("__enter__ and __exit__", True), ("__init__ and __del__", False), ("__start__ and __stop__", False), ("__open__ and __close__", False)]}
                        ]
                    }
                ]
            },

            # --- 2. MACHINE LEARNING & AI FOUNDATIONS ---
            {
                "title": "Machine Learning, Deep Learning & Generative AI",
                "slug": "machine-learning-ai-fundamentals",
                "category_code": "TECH",
                "skill_name": "Machine Learning",
                "difficulty": "Intermediate",
                "duration_hours": 35,
                "thumbnail_url": "https://images.unsplash.com/photo-1555255707-c07966088b7b?w=600",
                "description": "Engineering curriculum spanning linear models, gradient descent calculus, tree ensembles (XGBoost), neural network backpropagation, PyTorch tensors, Transformers, and Retrieval-Augmented Generation (RAG).",
                "what_you_will_learn": "• Mathematical foundations of Cost Functions, Convex Optimization, and Gradient Descent\n• Regularization techniques: L1 (Lasso) for sparsity and L2 (Ridge) for weight decay\n• Tree ensembles: Decision Trees, Random Forests, Gradient Boosted Trees (XGBoost)\n• Deep Neural Networks: Activation functions (ReLU, GELU), Backpropagation, Adam optimizer\n• Transformer architecture: Multi-Head Self-Attention, Positional Encodings, and LLMs\n• Practical RAG pipelines using Vector Databases and embedding models",
                "requirements": "Basic Python and foundational linear algebra / calculus.",
                "modules": [
                    {
                        "title": "Module 1: Supervised Learning Foundations, Cost Functions & Gradient Descent",
                        "description": "Mathematical derivation of Mean Squared Error, Binary Cross-Entropy, Convex Optimization, and Learning Rate dynamics.",
                        "order_index": 1,
                        "lessons": [
                            {
                                "title": "1.1 Mathematical Formulation of Linear & Logistic Regression",
                                "content_text": """### 1. Mathematical Formulation of Linear & Logistic Regression

#### 1. Linear Regression & Ordinary Least Squares
In linear regression, we model the relationship between $d$-dimensional input features $\mathbf{x} \in \mathbb{R}^d$ and a continuous target $y \in \mathbb{R}$ via the hypothesis:

$$\hat{y} = h_{\mathbf{w}}(\mathbf{x}) = \mathbf{w}^T \mathbf{x} + b$$

The Mean Squared Error (MSE) loss function over $N$ training samples is:

$$J(\mathbf{w}, b) = \frac{1}{2N} \sum_{i=1}^N \left( \hat{y}^{(i)} - y^{(i)} \right)^2$$

#### 2. Gradient Descent Optimization
Weights are iteratively updated in the direction of the negative gradient:

$$\mathbf{w} \leftarrow \mathbf{w} - \alpha \nabla_{\mathbf{w}} J(\mathbf{w})$$

where $\alpha$ is the learning rate.

#### 3. Logistic Regression & Binary Cross-Entropy
For binary classification, predictions are mapped to probabilities using the Sigmoid activation:

$$\sigma(z) = \frac{1}{1 + e^{-z}}$$

The Binary Cross-Entropy (Log-Loss) cost function is:

$$J(\mathbf{w}) = -\frac{1}{N} \sum_{i=1}^N \left[ y^{(i)} \log(\hat{y}^{(i)}) + (1 - y^{(i)}) \log(1 - \hat{y}^{(i)}) \right]$$""",
                                "duration_minutes": 30
                            },
                            {
                                "title": "1.2 Bias-Variance Tradeoff & Regularization (L1 / L2)",
                                "content_text": """### 2. Bias-Variance Tradeoff & Regularization (L1 / L2)

#### Understanding Model Generalization
- **High Bias (Underfitting):** The model is too simple to capture underlying patterns.
- **High Variance (Overfitting):** The model fits training noise and generalizes poorly to unseen test sets.

#### L1 Regularization (Lasso):
Adds the sum of absolute weight values to the cost function:

$$J_{\text{Lasso}}(\mathbf{w}) = J(\mathbf{w}) + \lambda \sum_{j=1}^d |w_j|$$

*Key Property:* Drives unimportant feature weights strictly to zero, performing automatic feature selection.

#### L2 Regularization (Ridge):
Adds the sum of squared weight values to the cost function:

$$J_{\text{Ridge}}(\mathbf{w}) = J(\mathbf{w}) + \lambda \sum_{j=1}^d w_j^2$$

*Key Property:* Penalizes large weights smoothly, preventing any single feature from dominating.""",
                                "duration_minutes": 30
                            }
                        ],
                        "questions": [
                            {"text": "Which regularization technique can drive feature coefficients exactly to zero for feature selection?", "explanation": "L1 Regularization (Lasso) creates sparse weight vectors by zeroing out non-contributing features.", "options": [("L1 Regularization (Lasso)", True), ("L2 Regularization (Ridge)", False), ("Dropout", False), ("Batch Normalization", False)]},
                            {"text": "What is the primary objective of Gradient Descent in machine learning?", "explanation": "Gradient descent minimizes the objective cost/loss function by iteratively updating weights.", "options": [("To minimize the model's loss/cost function", True), ("To increase model complexity", False), ("To calculate accuracy scores", False), ("To compress data size", False)]}
                        ]
                    },
                    {
                        "title": "Module 2: Deep Neural Networks, Backpropagation & Transformers",
                        "description": "Multi-layer perceptrons, forward propagation, gradient backpropagation via chain rule, and attention mechanisms.",
                        "order_index": 2,
                        "lessons": [
                            {
                                "title": "2.1 Neural Network Forward Propagation & Backpropagation",
                                "content_text": """### 1. Neural Network Forward Propagation & Backpropagation

A Deep Neural Network consists of stacked linear matrix multiplications interspersed with non-linear activation functions.

#### Layer Computation:
$$\mathbf{z}^{[l]} = \mathbf{W}^{[l]} \mathbf{a}^{[l-1]} + \mathbf{b}^{[l]}$$
$$\mathbf{a}^{[l]} = g(\mathbf{z}^{[l]})$$

where $g(z)$ is an activation function such as ReLU: $g(z) = \max(0, z)$ or GELU.

#### The Chain Rule & Backpropagation:
Backpropagation calculates the gradient of the loss with respect to every weight tensor in the network using the calculus chain rule:

$$\frac{\partial \mathcal{L}}{\partial \mathbf{W}^{[l]}} = \frac{\partial \mathcal{L}}{\partial \mathbf{z}^{[l]}} \cdot (\mathbf{a}^{[l-1]})^T$$""",
                                "duration_minutes": 35
                            },
                            {
                                "title": "2.2 The Transformer Architecture & Self-Attention Mechanisms",
                                "content_text": """### 2. The Transformer Architecture & Self-Attention Mechanisms

Transformers replaced recurrent networks by processing entire sequences in parallel using **Scaled Dot-Product Self-Attention**:

$$\text{Attention}(\mathbf{Q}, \mathbf{K}, \mathbf{V}) = \text{softmax}\left(\frac{\mathbf{Q}\mathbf{K}^T}{\sqrt{d_k}}\right)\mathbf{V}$$

- **Query ($\mathbf{Q}$):** What a token is looking for.
- **Key ($\mathbf{K}$):** What a token offers.
- **Value ($\mathbf{V}$):** The actual information content.
- **$\sqrt{d_k}$ Scaling:** Prevents dot products from exploding in high dimensions, stabilizing gradients.""",
                                "duration_minutes": 35
                            }
                        ],
                        "questions": [
                            {"text": "What formula defines Scaled Dot-Product Attention in the Transformer architecture?", "explanation": "Attention(Q, K, V) = softmax(Q * K^T / sqrt(d_k)) * V.", "options": [("softmax(Q * K^T / sqrt(d_k)) * V", True), ("sigmoid(Q + K) * V", False), ("relu(Q * V) + K", False), ("tanh(Q * K) / V", False)]}
                        ]
                    }
                ]
            },

            # --- 3. COMMERCE & FINANCIAL ACCOUNTING ---
            {
                "title": "Corporate Financial Accounting, Taxation & Auditing",
                "slug": "corporate-accounting-taxation-auditing",
                "category_code": "COMM",
                "skill_name": "Financial Accounting",
                "difficulty": "Beginner",
                "duration_hours": 28,
                "thumbnail_url": "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?w=600",
                "description": "Accredited commerce curriculum covering double-entry accounting systems, balance sheet architecture, profit & loss construction, GST taxation, and corporate auditing standards.",
                "what_you_will_learn": "• Golden rules of accounting and general ledger journalizing\n• Trial balance reconciliation and adjustment entries\n• Comprehensive Balance Sheet and Profit & Loss statement construction\n• Corporate tax laws, GST calculations, and input tax credit reconciliation\n• Auditing evidence, internal control systems, and statutory audit reports",
                "requirements": "High school arithmetic and commerce basics.",
                "modules": [
                    {
                        "title": "Module 1: Principles of Double-Entry Bookkeeping & Financial Statements",
                        "description": "The fundamental accounting equation, journal entries, ledger posting, and balance sheet preparation.",
                        "order_index": 1,
                        "lessons": [
                            {
                                "title": "1.1 The Golden Rules of Accounting & Journalizing",
                                "content_text": """### 1. The Golden Rules of Accounting & Journalizing

Financial accounting operates on the fundamental balance sheet equation:

$$\text{Assets} = \text{Liabilities} + \text{Owner's Equity}$$

#### The Three Golden Rules:
1. **Personal Accounts:** Debit the Receiver, Credit the Giver.
2. **Real Accounts (Assets):** Debit what comes in, Credit what goes out.
3. **Nominal Accounts (Expenses & Incomes):** Debit all expenses and losses, Credit all incomes and gains.

#### Step-by-Step Transaction Flow:
$$\text{Source Document} \longrightarrow \text{Journal Entry} \longrightarrow \text{Ledger Posting} \longrightarrow \text{Trial Balance} \longrightarrow \text{Financial Statements}$$""",
                                "duration_minutes": 25
                            },
                            {
                                "title": "1.2 Constructing the Balance Sheet & P&L Statement",
                                "content_text": """### 2. Constructing the Balance Sheet & P&L Statement

#### Profit & Loss Statement (Income Statement):
Measures financial performance over a reporting period:

$$\text{Gross Profit} = \text{Revenue from Operations} - \text{Cost of Goods Sold (COGS)}$$
$$\text{Net Profit} = \text{Gross Profit} + \text{Other Income} - \text{Operating Expenses} - \text{Taxes}$$

#### Balance Sheet Classification:
- **Current Assets:** Cash, Accounts Receivable, Inventory (liquid within 12 months).
- **Non-Current Assets:** Property, Plant, Equipment (PPE), Intangibles (Patents, Software).
- **Current Liabilities:** Accounts Payable, Short-term debt.
- **Long-Term Liabilities:** Bonds payable, term loans.
- **Equity:** Share capital, retained earnings.""",
                                "duration_minutes": 30
                            }
                        ],
                        "questions": [
                            {"text": "Under the Golden Rules of Accounting, how are Nominal Accounts handled?", "explanation": "Nominal accounts represent expenses, losses, revenues, and gains (Debit expenses, Credit incomes).", "options": [("Debit all expenses & losses, Credit all incomes & gains", True), ("Debit what comes in, Credit what goes out", False), ("Debit the giver, Credit the receiver", False), ("Debit assets, Credit liabilities", False)]}
                        ]
                    }
                ]
            },

            # --- 4. BUSINESS & MANAGEMENT ---
            {
                "title": "Strategic Business Leadership, Marketing & Analytics",
                "slug": "strategic-business-leadership-marketing-analytics",
                "category_code": "MGMT",
                "skill_name": "Business Analytics & Excel",
                "difficulty": "Intermediate",
                "duration_hours": 26,
                "thumbnail_url": "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=600",
                "description": "BBA & MBA curriculum covering Porter's Five Forces, competitive strategy, customer acquisition frameworks, digital marketing analytics, and financial valuation.",
                "what_you_will_learn": "• Strategic analysis frameworks: Porter's 5 Forces, SWOT, and PESTLE\n• Unit economics: Customer Acquisition Cost (CAC), Lifetime Value (LTV), Churn Rate\n• Data-driven growth marketing, SEO, and paid ad optimization\n• Discounted Cash Flow (DCF) valuation and corporate finance decision-making",
                "requirements": "Interest in business, startups, or corporate strategy.",
                "modules": [
                    {
                        "title": "Module 1: Strategic Frameworks & Competitive Advantage",
                        "description": "Porter's Five Forces, Blue Ocean strategy, and business model canvas.",
                        "order_index": 1,
                        "lessons": [
                            {
                                "title": "1.1 Porter's Five Forces & Industry Attractiveness",
                                "content_text": """### 1. Porter's Five Forces Framework

Developed by Michael Porter at Harvard Business School, this framework analyzes industry profitability:
1. **Threat of New Entrants:** Barriers to entry (economies of scale, capital requirements).
2. **Bargaining Power of Buyers:** Customer price sensitivity and switching costs.
3. **Bargaining Power of Suppliers:** Concentration of key raw material or talent providers.
4. **Threat of Substitutes:** Alternative technologies satisfying the same core customer need.
5. **Industry Rivalry:** Intensity of competition among existing players.""",
                                "duration_minutes": 25
                            }
                        ],
                        "questions": [
                            {"text": "Which framework evaluates industry attractiveness and competitive intensity?", "explanation": "Porter's Five Forces analyzes suppliers, buyers, substitutes, new entrants, and industry rivals.", "options": [("Porter's Five Forces", True), ("BCG Matrix", False), ("Ansoff Matrix", False), ("DuPont Analysis", False)]}
                        ]
                    }
                ]
            },

            # --- 5. DESIGN & CREATIVE ARTS ---
            {
                "title": "UI/UX Design, Figma Systems & Interaction Design",
                "slug": "ui-ux-design-figma-prototyping",
                "category_code": "DSGN",
                "skill_name": "UI/UX Design",
                "difficulty": "Beginner",
                "duration_hours": 24,
                "thumbnail_url": "https://images.unsplash.com/photo-1581291518857-4e27b48ff24e?w=600",
                "description": "B.Des & UI/UX curriculum covering human-computer interaction, user research, wireframing, typography, color harmony, Figma Auto-Layout, and design systems.",
                "what_you_will_learn": "• Double Diamond design process (Discover, Define, Develop, Deliver)\n• User empathy mapping, persona development, and journey mapping\n• Color theory, 8pt spatial grids, and typographic hierarchy\n• Figma component architectures, variants, variables, and auto-layout\n• Interactive prototyping, micro-interactions, and accessibility standards (WCAG)",
                "requirements": "Free Figma account.",
                "modules": [
                    {
                        "title": "Module 1: User Experience Research & Information Architecture",
                        "description": "Qualitative research, user journeys, card sorting, and wireframing.",
                        "order_index": 1,
                        "lessons": [
                            {
                                "title": "1.1 The Double Diamond Design Process",
                                "content_text": """### 1. The Double Diamond Design Process

The British Design Council's Double Diamond divides product design into four distinct iterative stages:
1. **Discover (Divergent):** Gathering raw user insights through contextual interviews, surveys, and competitive audits.
2. **Define (Convergent):** Synthesizing findings into clear problem statements, personas, and success metrics.
3. **Develop (Divergent):** Brainstorming, sketching wireframes, and exploring multiple design directions.
4. **Deliver (Convergent):** Testing high-fidelity prototypes, validating usability, and finalizing developer handoff specifications.""",
                                "duration_minutes": 25
                            }
                        ],
                        "questions": [
                            {"text": "What are the four phases of the Double Diamond design framework?", "explanation": "Discover, Define, Develop, Deliver.", "options": [("Discover, Define, Develop, Deliver", True), ("Plan, Code, Test, Deploy", False), ("Research, Prototype, Sell, Profit", False), ("Sketch, Color, Export, Print", False)]}
                        ]
                    }
                ]
            },

            # --- 6. CAREER & PLACEMENT DEVELOPMENT ---
            {
                "title": "Campus Placement Mastery: Quantitative Aptitude & Technical Coding",
                "slug": "campus-placement-aptitude-interviews",
                "category_code": "CAREER",
                "skill_name": "Quantitative Aptitude & Reasoning",
                "difficulty": "Beginner",
                "duration_hours": 20,
                "thumbnail_url": "https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=600",
                "description": "Comprehensive placement training for campus recruitments covering arithmetic speed math, logical puzzles, data interpretation, resume engineering, and STAR interview techniques.",
                "what_you_will_learn": "• Speed calculation techniques: Vedic math shortcuts and percentage fractions\n• Profit & Loss, Simple & Compound Interest, Time-Speed-Distance formulas\n• Permutations, Combinations, and Probability algorithms\n• Data Interpretation charts (Bar, Pie, Radar, Line graphs)\n• STAR behavioral interview framework (Situation, Task, Action, Result)",
                "requirements": "Basic high school mathematics.",
                "modules": [
                    {
                        "title": "Module 1: High-Speed Arithmetic & Quantitative Aptitude",
                        "description": "Percentages, ratios, profit & loss shortcuts, and time-speed-distance.",
                        "order_index": 1,
                        "lessons": [
                            {
                                "title": "1.1 Fraction-to-Percentage Memorization & Shortcuts",
                                "content_text": """### 1. Fraction-to-Percentage Memorization

In timed campus placement aptitude tests, converting fractions instantly saves precious seconds:

$$\\frac{1}{2} = 50\\%, \\quad \\frac{1}{3} = 33.33\\%, \\quad \\frac{1}{4} = 25\\%, \\quad \\frac{1}{5} = 20\\%$$
$$\\frac{1}{6} = 16.66\\%, \\quad \\frac{1}{7} = 14.28\\%, \\quad \\frac{1}{8} = 12.5\\%, \\quad \\frac{1}{9} = 11.11\\%$$
$$\\frac{1}{12} = 8.33\\%, \\quad \\frac{1}{16} = 6.25\\%$$

#### Example Problem:
Find $16.66\\%$ of $720$:
$$\\text{Solution:} \\quad \\frac{1}{6} \\times 720 = 120 \\quad (\\text{Computed in 2 seconds!})$$""",
                                "duration_minutes": 20
                            }
                        ],
                        "questions": [
                            {"text": "What is the fractional equivalent of 12.5%?", "explanation": "12.5% = 12.5 / 100 = 1/8.", "options": [("1/8", True), ("1/6", False), ("1/12", False), ("1/7", False)]}
                        ]
                    }
                ]
            }
        ]

        for c_info in courses_database:
            course = db.query(Course).filter(Course.slug == c_info["slug"]).first()
            cat = created_categories.get(c_info["category_code"])
            skill = created_skills.get(c_info["skill_name"])

            if not course:
                course = Course(
                    title=c_info["title"],
                    slug=c_info["slug"],
                    category_id=cat.id if cat else 1,
                    skill_id=skill.id if skill else None,
                    difficulty=c_info["difficulty"],
                    duration_hours=c_info["duration_hours"],
                    thumbnail_url=c_info["thumbnail_url"],
                    description=c_info["description"],
                    what_you_will_learn=c_info["what_you_will_learn"],
                    requirements=c_info["requirements"],
                    instructor_name="SkillSwap Campus Faculty",
                    rating=4.9,
                    enrollment_count=32
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
        print("Database seeding completed successfully with all rich multi-disciplinary curriculum!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
