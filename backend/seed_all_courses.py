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
from app.models.course import Course, CourseModule, Lesson
from app.models.assessment import ModuleAssessment, AssessmentQuestion, AssessmentOption


def seed_all_courses():
    print("Starting deep seeding of comprehensive multi-disciplinary courses...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Fetch or create Categories
        cat_map = {c.code: c for c in db.query(Category).all()}

        # 1. Prepare Comprehensive Multi-Disciplinary Courses
        courses_data = [
            # -------------------------------------------------------------
            # 1. TECHNOLOGY & COMPUTING / ENGINEERING
            # -------------------------------------------------------------
            {
                "title": "Full-Stack Web Engineering with React, TypeScript & FastAPI",
                "slug": "fullstack-react-typescript-fastapi",
                "category_code": "TECH",
                "skill_name": "React & TypeScript",
                "difficulty": "Intermediate",
                "duration_hours": 32,
                "thumbnail_url": "https://images.unsplash.com/photo-1633356122544-f134324a6cee?w=600",
                "description": "Production-grade full-stack engineering curriculum covering modern React 19 architecture, TypeScript strict type safety, asynchronous FastAPI REST APIs, SQLAlchemy ORM, JWT security, and Docker containerization.",
                "what_you_will_learn": "• Modern React 19 component lifecycle, custom hooks, and state management\n• TypeScript strict interfaces, generics, union types, and utility types\n• Asynchronous Python backend APIs with FastAPI and Pydantic v2 validation\n• Relational database modeling with SQLAlchemy ORM and PyMySQL\n• Secure JWT Bearer authentication, password hashing, and CORS middleware\n• Full-stack integration, error boundaries, and Docker container deployment",
                "requirements": "Basic knowledge of HTML, CSS, and introductory programming.",
                "modules": [
                    {
                        "title": "Module 1: React 19 & TypeScript Strict Architecture",
                        "description": "Component design patterns, custom hooks, generics, and state management.",
                        "order_index": 1,
                        "lessons": [
                            {
                                "title": "1.1 React Hooks Deep Dive: useState, useEffect, useCallback, useMemo",
                                "content_text": """### 1. React Hooks Architecture & Lifecycle

React functional components rely on hooks to manage state and side effects. Understanding re-render triggers and reference identity is critical for performance.

#### The Hook Rules & Fiber Reconciliation:
1. Only call hooks at the top level of functional components.
2. Only call hooks from React function components or custom hooks.

```tsx
import React, { useState, useEffect, useCallback, useMemo } from 'react';

interface StudentData {
  id: number;
  name: string;
  gpa: number;
}

export const StudentAnalytics: React.FC<{ collegeId: number }> = ({ collegeId }) => {
  const [students, setStudents] = useState<StudentData[]>([]);
  const [filterThreshold, setFilterThreshold] = useState<number>(3.5);

  // useCallback memoizes function reference to prevent child re-renders
  const fetchStudents = useCallback(async () => {
    const res = await fetch(`/api/colleges/${collegeId}/students`);
    const data: StudentData[] = await res.json();
    setStudents(data);
  }, [collegeId]);

  useEffect(() => {
    fetchStudents();
  }, [fetchStudents]);

  // useMemo caches expensive computation across re-renders
  const honorRoll = useMemo(() => {
    return students.filter(s => s.gpa >= filterThreshold);
  }, [students, filterThreshold]);

  return (
    <div className="p-4 bg-white rounded-xl shadow-md">
      <h3 className="font-bold text-lg">Honor Roll Students ({honorRoll.length})</h3>
      <ul className="divide-y divide-slate-100">
        {honorRoll.map(s => (
          <li key={s.id} className="py-2 flex justify-between">
            <span>{s.name}</span>
            <span className="font-mono text-blue-600 font-bold">{s.gpa.toFixed(2)}</span>
          </li>
        ))}
      </ul>
    </div>
  );
};
```""",
                                "duration_minutes": 30
                            },
                            {
                                "title": "1.2 TypeScript Generics & Type-Safe API Client Architecture",
                                "content_text": """### 2. TypeScript Generics & Type-Safe API Client Architecture

TypeScript eliminates entire classes of runtime errors by enforcing strict compile-time types.

#### Generic API Client Pattern with Axios:
```typescript
import axios, { AxiosInstance, AxiosResponse } from 'axios';

export interface ApiResponse<T> {
  status: 'success' | 'error';
  data: T;
  message?: string;
}

export class ApiClient {
  private client: AxiosInstance;

  constructor(baseURL: string) {
    this.client = axios.create({ baseURL, timeout: 10000 });
    this.setupInterceptors();
  }

  private setupInterceptors(): void {
    this.client.interceptors.request.use((config) => {
      const token = localStorage.getItem('auth_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
  }

  public async get<T>(url: string, params?: Record<string, any>): Promise<T> {
    const response: AxiosResponse<ApiResponse<T>> = await this.client.get(url, { params });
    return response.data.data;
  }

  public async post<T, B>(url: string, body: B): Promise<T> {
    const response: AxiosResponse<ApiResponse<T>> = await this.client.post(url, body);
    return response.data.data;
  }
}
```""",
                                "duration_minutes": 30
                            }
                        ],
                        "questions": [
                            {"text": "What is the primary purpose of `useMemo` in React?", "explanation": "useMemo caches the result of an expensive calculation between re-renders when dependencies have not changed.", "options": [("To cache the result of an expensive computation", True), ("To trigger side-effects like data fetching", False), ("To mutate the DOM directly", False), ("To store state permanently in localStorage", False)]},
                            {"text": "In TypeScript, what keyword allows defining a reusable component or function that works over multiple types?", "explanation": "Generics (<T>) enable creating type-safe reusable components across varying types.", "options": [("Generics (<T>)", True), ("any", False), ("dynamic", False), ("interface", False)]}
                        ]
                    },
                    {
                        "title": "Module 2: High-Performance Backend APIs with FastAPI & SQLAlchemy",
                        "description": "Async endpoints, Pydantic validation, connection pooling, and JWT bearer security.",
                        "order_index": 2,
                        "lessons": [
                            {
                                "title": "2.1 Pydantic v2 Data Validation & FastAPI Dependency Injection",
                                "content_text": """### 1. Pydantic v2 Data Validation & FastAPI Dependency Injection

FastAPI combines Python type hints with Pydantic v2 and Starlette to deliver blazing-fast asynchronous REST APIs.

#### Dependency Injection Pattern:
```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
from typing import Optional

app = FastAPI(title="Campus API")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

class StudentCreateSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    college: str
    year: int = Field(..., ge=1, le=5)

class StudentResponseSchema(StudentCreateSchema):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

def get_current_active_user(token: str = Depends(oauth2_scheme)) -> dict:
    payload = decode_jwt_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials or expired session"
        )
    return payload
```""",
                                "duration_minutes": 30
                            }
                        ],
                        "questions": [
                            {"text": "How does FastAPI implement dependency injection for request-scoped database sessions?", "explanation": "Using Depends(get_db) provides clean dependency injection that automatically manages session lifecycles.", "options": [("Using the `Depends()` function in route signatures", True), ("Through global variables", False), ("Via metaclasses only", False), ("Using thread-local storage", False)]}
                        ]
                    }
                ]
            },

            # -------------------------------------------------------------
            # 2. DATA STRUCTURES & ALGORITHMS (Placement / CSE / BCA / IT)
            # -------------------------------------------------------------
            {
                "title": "Data Structures, Algorithms & Competitive Coding",
                "slug": "data-structures-algorithms-competitive-coding",
                "category_code": "TECH",
                "skill_name": "Data Structures & Algorithms",
                "difficulty": "Intermediate",
                "duration_hours": 35,
                "thumbnail_url": "https://images.unsplash.com/photo-1516116211227-bbc13c726352?w=600",
                "description": "Essential placement and competitive programming curriculum covering asymptotic complexity, two pointers, sliding window, binary search trees, graph algorithms (Dijkstra, BFS/DFS), and dynamic programming.",
                "what_you_will_learn": "• Master Big-O notation, amortized analysis, and space-time tradeoffs\n• Two pointers, sliding window, and Kadane's algorithm for linear time solutions\n• Stack architectures: Monotonic stacks, postfix evaluation, and LRU Cache\n• Tree algorithms: Binary Search Trees, LCA, tree serialization, and AVL rotations\n• Graph theory: Adjacency representations, BFS, DFS, Dijkstra's algorithm, Topological sort\n• Dynamic Programming: 0/1 Knapsack, Longest Common Subsequence, and memoization",
                "requirements": "Familiarity with any programming language (Python, C++, Java).",
                "modules": [
                    {
                        "title": "Module 1: Array Manipulation, Two Pointers & Sliding Window",
                        "description": "Techniques for optimizing $O(N^2)$ brute force approaches into optimal $O(N)$ linear scans.",
                        "order_index": 1,
                        "lessons": [
                            {
                                "title": "1.1 The Two-Pointer Technique & Dutch National Flag Algorithm",
                                "content_text": """### 1. The Two-Pointer Technique

The two-pointer technique uses two pointer variables traversing a sequence in coordination to achieve $O(N)$ time complexity and $O(1)$ auxiliary space.

#### Problem 1: Container With Most Water ($O(N)$)
```python
def max_area(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    max_water = 0

    while left < right:
        width = right - left
        current_water = min(height[left], height[right]) * width
        max_water = max(max_water, current_water)

        # Move the pointer with the smaller height inward
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return max_water
```

#### Problem 2: Dutch National Flag 3-Way Partitioning ($O(N)$)
```python
def sort_colors(nums: list[int]) -> None:
    # Sort array of 0s, 1s, and 2s in-place
    low, mid, high = 0, 0, len(nums) - 1

    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
```""",
                                "duration_minutes": 30
                            }
                        ],
                        "questions": [
                            {"text": "What is the optimal time complexity of the Two-Pointer technique on a sorted array of size N?", "explanation": "Two pointers traverse the array in a single pass achieving O(N) linear time.", "options": [("O(N)", True), ("O(N^2)", False), ("O(log N)", False), ("O(1)", False)]}
                        ]
                    },
                    {
                        "title": "Module 2: Graph Theory & Shortest Path Algorithms",
                        "description": "Graph representations, topological sorting, Dijkstra's algorithm, and Disjoint Set Union (DSU).",
                        "order_index": 2,
                        "lessons": [
                            {
                                "title": "2.1 Dijkstra's Shortest Path Algorithm with Priority Queue",
                                "content_text": """### 1. Dijkstra's Algorithm with Min-Heap ($O((V + E) \log V)$)

Dijkstra's algorithm finds the shortest path from a single source node to all other nodes in a weighted graph with non-negative edge weights.

```python
import heapq

def dijkstra(graph: dict, source: int, num_nodes: int) -> dict:
    distances = {node: float('inf') for node in range(num_nodes)}
    distances[source] = 0
    min_heap = [(0, source)]  # (distance, node)

    while min_heap:
        current_dist, u = heapq.heappop(min_heap)

        if current_dist > distances[u]:
            continue

        for neighbor, weight in graph.get(u, []):
            distance = current_dist + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(min_heap, (distance, neighbor))

    return distances
```""",
                                "duration_minutes": 35
                            }
                        ],
                        "questions": [
                            {"text": "Under what condition does standard Dijkstra's algorithm fail?", "explanation": "Dijkstra's greedy assumption fails when edges have negative weights (Bellman-Ford is used instead).", "options": [("When graphs contain negative edge weights", True), ("When graphs have cycles", False), ("When graphs are directed", False), ("When graphs have more than 1000 nodes", False)]}
                        ]
                    }
                ]
            },

            # -------------------------------------------------------------
            # 3. CYBERSECURITY & NETWORK DEFENSE
            # -------------------------------------------------------------
            {
                "title": "Cybersecurity Fundamentals, Network Security & Ethical Hacking",
                "slug": "cybersecurity-network-defense-ethical-hacking",
                "category_code": "TECH",
                "skill_name": "Cybersecurity Fundamentals",
                "difficulty": "Beginner",
                "duration_hours": 28,
                "thumbnail_url": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=600",
                "description": "Comprehensive cybersecurity engineering curriculum covering the OSI security model, packet inspection, TLS/SSL cryptographic handshakes, OWASP Top 10 vulnerabilities (SQLi, XSS, CSRF), and defensive incident response.",
                "what_you_will_learn": "• Core security pillars: Confidentiality, Integrity, and Availability (CIA Triad)\n• Network packet analysis with Wireshark and TCP/IP protocol vulnerabilities\n• Public Key Cryptography, RSA, Diffie-Hellman Key Exchange, and digital certificates\n• OWASP Top 10 web vulnerabilities: SQL Injection, XSS, CSRF, and Broken Authentication\n• Security auditing with Nmap, Burp Suite, and defensive firewall configurations\n• Incident response, digital forensics, and secure software development lifecycle (SSDLC)",
                "requirements": "Basic networking and operating system concepts.",
                "modules": [
                    {
                        "title": "Module 1: The CIA Triad, Network Protocols & Cryptography",
                        "description": "Network security layers, packet inspection, symmetric vs asymmetric encryption, and TLS architecture.",
                        "order_index": 1,
                        "lessons": [
                            {
                                "title": "1.1 The CIA Triad & Cryptographic Foundations (Symmetric vs Asymmetric)",
                                "content_text": """### 1. The CIA Triad & Cryptographic Foundations

#### The Three Pillars of Information Security:
1. **Confidentiality:** Ensuring information is inaccessible to unauthorized entities (AES encryption, access controls).
2. **Integrity:** Guaranteeing data has not been modified or corrupted in transit (SHA-256 hashing, HMAC, digital signatures).
3. **Availability:** Ensuring authorized users have reliable access to systems (DDoS mitigation, load balancing, redundancy).

#### Symmetric vs Asymmetric Cryptography:
| Feature | Symmetric Cryptography (AES-256, ChaCha20) | Asymmetric Cryptography (RSA, ECC) |
| :--- | :--- | :--- |
| **Keys** | Single shared secret key for encryption & decryption | Public key (encrypt) + Private key (decrypt) |
| **Speed** | Extremely fast (hardware-accelerated AES-NI) | Computationally expensive |
| **Key Distribution** | Difficult to securely exchange keys across public internet | Public keys can be openly shared via PKI |

#### The Hybrid TLS Handshake:
Modern HTTPS uses **hybrid encryption**:
1. Asymmetric cryptography (ECDHE) securely exchanges a temporary symmetric session key.
2. High-speed symmetric encryption (AES-GCM) encrypts the actual HTTP payload.""",
                                "duration_minutes": 30
                            }
                        ],
                        "questions": [
                            {"text": "Why do modern web protocols (TLS/HTTPS) use hybrid cryptography rather than pure RSA?", "explanation": "Asymmetric encryption is computationally expensive, so it is used only to exchange a temporary symmetric key which encrypts the bulk data at high speed.", "options": [("Asymmetric encryption is too slow for bulk data transfer", True), ("Symmetric encryption cannot encrypt text", False), ("RSA keys expire in 5 seconds", False), ("To avoid using digital certificates", False)]}
                        ]
                    }
                ]
            },

            # -------------------------------------------------------------
            # 4. SCIENCE & APPLIED MATHEMATICS
            # -------------------------------------------------------------
            {
                "title": "Applied Calculus, Linear Algebra & Probability for Data Science",
                "slug": "applied-calculus-linear-algebra-probability",
                "category_code": "SCI",
                "skill_name": "Calculus & Linear Algebra",
                "difficulty": "Intermediate",
                "duration_hours": 30,
                "thumbnail_url": "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=600",
                "description": "B.Sc & Engineering mathematical curriculum covering vector spaces, matrix factorizations (SVD, Eigenvalues), partial derivatives, Jacobian/Hessian matrices, and continuous probability distributions.",
                "what_you_will_learn": "• Matrix transformations, linear independence, rank, and nullspace\n• Eigenvalues, Eigenvectors, and Principal Component Analysis (PCA) derivation\n• Singular Value Decomposition (SVD) and matrix rank reduction\n• Multivariable calculus: Partial derivatives, gradients, directional derivatives, and Hessians\n• Continuous probability distributions: Gaussian, Poisson, Exponential, and Central Limit Theorem",
                "requirements": "High school algebra and calculus basics.",
                "modules": [
                    {
                        "title": "Module 1: Linear Algebra, Eigenvalues & Matrix Decomposition",
                        "description": "Vector spaces, dot products, orthonormal bases, eigenvalues, and Singular Value Decomposition.",
                        "order_index": 1,
                        "lessons": [
                            {
                                "title": "1.1 Eigenvalues, Eigenvectors & Geometric Transformations",
                                "content_text": """### 1. Eigenvalues, Eigenvectors & Geometric Transformations

An eigenvector $\mathbf{v}$ of a square matrix $\mathbf{A} \in \mathbb{R}^{n \times n}$ is a non-zero vector whose direction remains unchanged under the linear transformation $\mathbf{A}$:

$$\mathbf{A}\mathbf{v} = \lambda \mathbf{v}$$

where $\lambda \in \mathbb{R}$ is the corresponding **eigenvalue** (scalar scaling factor).

#### Characteristic Equation:
To compute eigenvalues, we solve for roots where the determinant vanishes:

$$\det(\mathbf{A} - \lambda \mathbf{I}) = 0$$

#### Application in Principal Component Analysis (PCA):
In Data Science and Machine Learning, finding the eigenvectors of a data covariance matrix $\mathbf{\Sigma} = \frac{1}{N} \mathbf{X}^T \mathbf{X}$ identifies the principal directions of maximum data variance, enabling dimensionality reduction.""",
                                "duration_minutes": 30
                            }
                        ],
                        "questions": [
                            {"text": "What equation defines an eigenvalue $\\lambda$ and eigenvector $\\mathbf{v}$ of a matrix $\\mathbf{A}$?", "explanation": "A * v = lambda * v defines an invariant direction scaled by lambda.", "options": [("A * v = lambda * v", True), ("A + v = lambda", False), ("det(A) = v", False), ("A * lambda = v^2", False)]}
                        ]
                    }
                ]
            },

            # -------------------------------------------------------------
            # 5. ARTS, HUMANITIES & JOURNALISM
            # -------------------------------------------------------------
            {
                "title": "Modern Macroeconomics, Fiscal Policy & Market Dynamics",
                "slug": "macroeconomics-fiscal-policy-market-dynamics",
                "category_code": "ARTS",
                "skill_name": "Macroeconomics & Policy",
                "difficulty": "Beginner",
                "duration_hours": 24,
                "thumbnail_url": "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=600",
                "description": "BA Economics curriculum covering national income accounting (GDP), aggregate demand and supply (AD-AS model), central banking, inflation dynamics, monetary policy, and international trade.",
                "what_you_will_learn": "• National income accounting methods: Expenditure, Income, and Output approaches\n• Aggregate Demand (AD) and Aggregate Supply (AS) macroeconomic equilibrium\n• Central Banking monetary tools: Reserve ratios, Repo rates, and Quantitative Easing\n• Inflation measurement (CPI, WPI) and Phillips curve tradeoff\n• Fiscal policy: Government expenditure multipliers and national debt sustainability",
                "requirements": "General interest in economics, finance, or public policy.",
                "modules": [
                    {
                        "title": "Module 1: National Income Accounting & Macroeconomic Equilibrium",
                        "description": "Gross Domestic Product (GDP), inflation indices, and Keynesian multiplier models.",
                        "order_index": 1,
                        "lessons": [
                            {
                                "title": "1.1 Measuring Gross Domestic Product (The Expenditure Method)",
                                "content_text": """### 1. Measuring Gross Domestic Product (GDP)

Gross Domestic Product represents the total monetary value of all finished goods and services produced within a nation's borders in a specific time frame.

#### The Expenditure Equation:
$$Y = C + I + G + (X - M)$$

- **$C$ (Personal Consumption Expenditures):** Household spending on durable goods, non-durable goods, and services.
- **$I$ (Gross Private Domestic Investment):** Business investments in capital goods, residential construction, and inventory changes.
- **$G$ (Government Consumption & Gross Investment):** Public spending on defense, infrastructure, education, and public services.
- **$(X - M)$ (Net Exports):** Total exports ($X$) minus total imports ($M$).

#### Real GDP vs Nominal GDP:
$$\text{Real GDP} = \frac{\text{Nominal GDP}}{\text{GDP Deflator}} \times 100$$
*Real GDP adjusts for inflation by evaluating output at base-year constant prices.*""",
                                "duration_minutes": 25
                            }
                        ],
                        "questions": [
                            {"text": "In national income accounting, what is the formula for GDP using the expenditure approach?", "explanation": "GDP = C + I + G + (X - M).", "options": [("C + I + G + (X - M)", True), ("C + S + T", False), ("Revenue - Expenses", False), ("Exports - Imports", False)]}
                        ]
                    }
                ]
            },

            # -------------------------------------------------------------
            # 6. LAW & LEGAL STUDIES
            # -------------------------------------------------------------
            {
                "title": "Corporate Law, Intellectual Property & Cyber Jurisprudence",
                "slug": "corporate-law-intellectual-property-cyber-jurisprudence",
                "category_code": "LAW",
                "skill_name": "Corporate & Cyber Law",
                "difficulty": "Intermediate",
                "duration_hours": 24,
                "thumbnail_url": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=600",
                "description": "LLB & Legal Studies curriculum covering contract formation, corporate governance, intellectual property rights (patents, trademarks, copyrights), data privacy laws (GDPR), and cybercrime legislation.",
                "what_you_will_learn": "• Elements of valid contract formation: Offer, acceptance, consideration, and capacity\n• Corporate governance, fiduciary duties of directors, and shareholder rights\n• Intellectual property protection: Patent criteria, trademark distinctiveness, and copyright infringement\n• Information Technology laws, electronic evidence admissibility, and cybercrime liability\n• Data privacy principles and international regulatory compliance (GDPR, DPDP Act)",
                "requirements": "No prior legal background required.",
                "modules": [
                    {
                        "title": "Module 1: Contract Law Foundations & Intellectual Property",
                        "description": "Essential contract elements, breaches, remedies, patentability, and copyright law.",
                        "order_index": 1,
                        "lessons": [
                            {
                                "title": "1.1 Essential Elements of a Valid Legal Contract",
                                "content_text": """### 1. Essential Elements of a Valid Legal Contract

Under contract jurisprudence, a legally binding contract requires the confluence of five foundational criteria:
1. **Offer & Acceptance:** A definite proposal made by one party and an unqualified acceptance by the other.
2. **Lawful Consideration:** Quid pro quo ('something in return') that has legal value.
3. **Capacity of Parties:** Parties must be of the age of majority, of sound mind, and not disqualified by law.
4. **Free Consent:** Consent must not be obtained via coercion, undue influence, fraud, or misrepresentation.
5. **Lawful Object:** The objective of the agreement must not be illegal or opposed to public policy.""",
                                "duration_minutes": 25
                            }
                        ],
                        "questions": [
                            {"text": "Which element is essential for an agreement to be legally enforceable as a contract?", "explanation": "A valid contract requires mutual lawful consideration (quid pro quo).", "options": [("Lawful Consideration and Free Consent", True), ("Notarization on gold paper", False), ("Approval by 5 witnesses", False), ("A minimum value of $10,000", False)]}
                        ]
                    }
                ]
            },

            # -------------------------------------------------------------
            # 7. LANGUAGES & GLOBAL COMMUNICATION
            # -------------------------------------------------------------
            {
                "title": "Executive Business English & Global Cross-Cultural Communication",
                "slug": "executive-business-english-communication",
                "category_code": "LANG",
                "skill_name": "Professional English Communication",
                "difficulty": "Beginner",
                "duration_hours": 20,
                "thumbnail_url": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=600",
                "description": "Curriculum covering formal business writing, executive proposals, cross-cultural corporate negotiation, diplomatic language, and persuasive public keynote delivery.",
                "what_you_will_learn": "• Precision business writing for executive proposals, RFPs, and corporate briefings\n• Cross-cultural communication nuances and global business etiquette\n• High-stakes negotiation frameworks and diplomatic de-escalation vocabulary\n• Structural storytelling: The Minto Pyramid Principle in corporate presentations",
                "requirements": "Basic English proficiency.",
                "modules": [
                    {
                        "title": "Module 1: Executive Writing & The Minto Pyramid Principle",
                        "description": "Top-down communication structuring, executive summaries, and formal proposals.",
                        "order_index": 1,
                        "lessons": [
                            {
                                "title": "1.1 The Minto Pyramid Principle for Executive Communications",
                                "content_text": """### 1. The Minto Pyramid Principle

Developed by Barbara Minto at McKinsey & Company, the Pyramid Principle structures executive communications top-down:

#### Structure:
1. **Top (The Answer / Core Recommendation):** State your primary conclusion or call-to-action first.
2. **Middle (Key Supporting Arguments):** Group 3-4 mutually exclusive, collectively exhaustive (MECE) reasons.
3. **Bottom (Supporting Data & Evidence):** Provide detailed facts, data points, and operational specifics.

*Busy executives need the conclusion upfront before evaluating supporting rationale.*""",
                                "duration_minutes": 20
                            }
                        ],
                        "questions": [
                            {"text": "What is the core rule of the Minto Pyramid Principle in executive communication?", "explanation": "Start with the main answer/recommendation first before providing supporting details.", "options": [("State the core recommendation first, followed by supporting evidence", True), ("Provide 50 pages of raw data before any conclusions", False), ("Use informal slang to appear friendly", False), ("Avoid giving actionable conclusions", False)]}
                        ]
                    }
                ]
            }
        ]

        for c_info in courses_data:
            course = db.query(Course).filter(Course.slug == c_info["slug"]).first()
            cat = cat_map.get(c_info["category_code"])
            skill = db.query(Skill).filter(Skill.name == c_info["skill_name"]).first()

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
                    enrollment_count=45
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
        print("Deep multi-disciplinary seeding completed successfully!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding courses: {e}")
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed_all_courses()
