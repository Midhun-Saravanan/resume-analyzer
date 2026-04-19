import re

QUESTION_BANK = {
    'Python Developer': [
        "Explain the difference between a list and a tuple in Python.",
        "What are decorators in Python and how do you use them?",
        "How does Python's garbage collection work?",
        "What is the difference between *args and **kwargs?",
        "Explain list comprehensions with an example.",
        "What is the GIL in Python and how does it affect multithreading?",
        "How do you handle exceptions in Python?",
        "What is the difference between deep copy and shallow copy?",
        "Explain generators and yield in Python.",
        "How do you manage virtual environments in Python?",
    ],
    'Web Developer': [
        "What is the difference between GET and POST requests?",
        "Explain the CSS Box Model.",
        "What is CORS and how do you handle it?",
        "What is the difference between localStorage and sessionStorage?",
        "Explain how Flexbox works.",
        "What are semantic HTML elements?",
        "What is the difference between == and === in JavaScript?",
        "Explain event bubbling and capturing in JavaScript.",
        "What is a REST API and how does it work?",
        "How does async/await work in JavaScript?",
    ],
    'Java Developer': [
        "What is the difference between JDK, JRE, and JVM?",
        "Explain OOP principles with examples in Java.",
        "What is the difference between an interface and an abstract class?",
        "How does Java handle memory management?",
        "What are Java Streams and how do you use them?",
        "Explain the difference between HashMap and HashTable.",
        "What is multithreading in Java?",
        "What are checked and unchecked exceptions?",
        "Explain the Singleton design pattern.",
        "What is Spring Boot and why is it used?",
    ],
    'Data Analyst': [
        "What is the difference between INNER JOIN and LEFT JOIN in SQL?",
        "How do you handle missing data in a dataset?",
        "Explain the difference between OLAP and OLTP.",
        "What is normalization in databases?",
        "How do you identify outliers in data?",
        "What is the difference between mean, median, and mode?",
        "Explain what a pivot table is and when you use it.",
        "What tools have you used for data visualization?",
        "What is correlation vs causation?",
        "How do you validate the accuracy of your data analysis?",
    ],
    'Data Scientist': [
        "What is the difference between supervised and unsupervised learning?",
        "Explain overfitting and how to prevent it.",
        "What is cross-validation and why is it important?",
        "Explain the bias-variance tradeoff.",
        "What is the difference between precision and recall?",
        "How does a Random Forest algorithm work?",
        "What is gradient descent?",
        "Explain the concept of feature engineering.",
        "What is regularization in machine learning?",
        "How do you handle imbalanced datasets?",
    ],
    'General IT Role': [
        "Tell me about yourself and your technical background.",
        "What projects have you worked on recently?",
        "How do you stay updated with new technologies?",
        "Describe a challenging technical problem you solved.",
        "What is your approach to debugging a complex issue?",
        "How do you prioritize tasks when working on multiple projects?",
        "What version control tools have you used?",
        "Describe your experience working in a team.",
        "What are your strongest technical skills?",
        "Where do you see yourself in 3 years?",
    ]
}

BEHAVIORAL_QUESTIONS = [
    "Tell me about a time you faced a tight deadline. How did you handle it?",
    "Describe a situation where you had to learn a new technology quickly.",
    "Tell me about a project you're most proud of.",
    "How do you handle disagreements with teammates?",
    "Describe a time when you had to explain a technical concept to a non-technical person.",
]

def generate_questions(jd_text, role):
    jd_lower = jd_text.lower()

    # Get role-specific questions
    role_questions = QUESTION_BANK.get(role, QUESTION_BANK['General IT Role'])

    # Generate JD-specific questions from keywords
    jd_questions = []
    if 'sql' in jd_lower or 'database' in jd_lower:
        jd_questions.append("Write a SQL query to find the second highest salary from an Employee table.")
    if 'git' in jd_lower or 'github' in jd_lower:
        jd_questions.append("What is the difference between git merge and git rebase?")
    if 'api' in jd_lower or 'rest' in jd_lower:
        jd_questions.append("How would you design a RESTful API for a user management system?")
    if 'agile' in jd_lower or 'scrum' in jd_lower:
        jd_questions.append("What is the Agile methodology and what is your experience with Scrum?")
    if 'docker' in jd_lower or 'kubernetes' in jd_lower:
        jd_questions.append("What is containerization and what are the benefits of using Docker?")
    if 'react' in jd_lower or 'angular' in jd_lower or 'vue' in jd_lower:
        jd_questions.append("What is the virtual DOM and how does React use it?")
    if 'machine learning' in jd_lower or 'ml' in jd_lower:
        jd_questions.append("How would you choose between different ML algorithms for a classification problem?")

    return {
        "role": role,
        "technical": role_questions[:8],
        "jd_specific": jd_questions[:5],
        "behavioral": BEHAVIORAL_QUESTIONS[:5]
    }