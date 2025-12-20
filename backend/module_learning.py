import random
import re

def get_learning_paths():
    return {
        "react": {
            "keywords": ["react", "frontend", "ui developer"],
            "path": [
                {
                    "title": "JavaScript Fundamentals & ES6+",
                    "description": "Master the core of JavaScript, including variables, functions, arrays, objects, and modern ES6+ features like arrow functions and promises.",
                    "difficulty": "Easy",
                    "resources": {
                        "tutorials": ["https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide"],
                        "github_projects": ["https://github.com/getify/You-Dont-Know-JS"],
                        "videos": ["https://www.youtube.com/watch?v=hdI2bqOjy3c&list=PLu0W_9lII9agx66oZnT6GO_s-vLBE-p8s"]
                    }
                },
                {
                    "title": "React Basics: Components, JSX, Props & State",
                    "description": "Learn the fundamental building blocks of React, including how to create components, use JSX for templating, and manage component state.",
                    "difficulty": "Easy",
                    "resources": {
                        "tutorials": ["https://react.dev/learn"],
                        "github_projects": ["https://github.com/react-boilerplate/react-boilerplate"],
                        "videos": ["https://www.youtube.com/watch?v=bMknfKXIFA8&list=PLu0W_9lII9agx66oZnT6GO_s-vLBE-p8s"]
                    }
                },
                {
                    "title": "State Management: Hooks & Context API",
                    "description": "Deep dive into React Hooks like useState, useEffect, and useContext for managing state and side effects in functional components.",
                    "difficulty": "Medium",
                    "resources": {
                        "tutorials": ["https://react.dev/reference/react/hooks"],
                        "github_projects": ["https://github.com/diegohaz/arc"],
                        "videos": ["https://www.youtube.com/watch?v=tn1_whF_pjY&list=PLu0W_9lII9agx66oZnT6GO_s-vLBE-p8s"]
                    }
                },
                {
                    "title": "Advanced State Management: Redux or Zustand",
                    "description": "For larger applications, learn a dedicated state management library like Redux for predictable state container or Zustand for a more minimalistic approach.",
                    "difficulty": "Medium",
                    "resources": {
                        "tutorials": ["https://redux.js.org/introduction/getting-started", "https://github.com/pmndrs/zustand"],
                        "github_projects": ["https://github.com/reduxjs/redux-essentials-example-app"],
                        "videos": ["https://www.youtube.com/watch?v=9jR2B9yv_vY"]
                    }
                },
                {
                    "title": "React Router: Client-Side Routing",
                    "description": "Implement navigation and routing in your single-page application to handle different views and URLs.",
                    "difficulty": "Medium",
                    "resources": {
                        "tutorials": ["https://reactrouter.com/en/main/start/tutorial"],
                        "github_projects": ["https://github.com/remix-run/react-router/tree/main/examples"],
                        "videos": ["https://www.youtube.com/watch?v=M9g_aPGrr-8"]
                    }
                },
                {
                    "title": "API Integration with Axios or Fetch",
                    "description": "Learn to communicate with backend services and APIs to fetch and display dynamic data in your React application.",
                    "difficulty": "Medium",
                    "resources": {
                        "tutorials": ["https://axios-http.com/docs/intro"],
                        "github_projects": ["https://github.com/axios/axios/tree/v1.x/examples"],
                        "videos": ["https://www.youtube.com/watch?v=Ek-EH-0_468"]
                    }
                },
                 {
                    "title": "Build and Deploy a Full-Stack Project",
                    "description": "Apply all your knowledge to build a complete real-world application with a backend and deploy it to a hosting service like Vercel or Netlify.",
                    "difficulty": "Hard",
                    "resources": {
                        "tutorials": ["https://vercel.com/docs/frameworks/react", "https://docs.netlify.com/integrations/frameworks/react/"],
                        "github_projects": ["https://github.com/vercel/next.js/tree/canary/examples"],
                        "videos": ["https://www.youtube.com/watch?v=1v_4dLDuchi"]
                    }
                }
            ]
        },
        "data_science": {
            "keywords": ["data scientist", "data science", "machine learning", "ai specialist"],
            "path": [
                {
                    "title": "Python for Data Science",
                    "description": "Get proficient with Python and key libraries like NumPy for numerical operations, Pandas for data manipulation, and Matplotlib/Seaborn for visualization.",
                    "difficulty": "Easy",
                    "resources": {
                        "tutorials": ["https://pandas.pydata.org/docs/getting_started/index.html"],
                        "github_projects": ["https://github.com/jakevdp/PythonDataScienceHandbook"],
                        "videos": ["https://www.youtube.com/watch?v=gfDE2a7MKjA&list=PLu0W_9lII9agK8e22w0Gf_I_58y-sR4in"]
                    }
                },
                {
                    "title": "Statistics & Probability",
                    "description": "Build a strong foundation in the mathematical concepts that underpin data science, including descriptive and inferential statistics.",
                    "difficulty": "Medium",
                    "resources": {
                        "tutorials": ["https://www.khanacademy.org/math/statistics-probability"],
                        "github_projects": ["https://github.com/seeing-theory/seeing-theory.github.io"],
                        "videos": ["https://www.youtube.com/watch?v=xxpc-3Cba6A"]
                    }
                },
                {
                    "title": "Machine Learning Fundamentals",
                    "description": "Learn about supervised vs. unsupervised learning, and core algorithms like linear regression, logistic regression, and k-means clustering.",
                    "difficulty": "Medium",
                    "resources": {
                        "tutorials": ["https://scikit-learn.org/stable/user_guide.html"],
                        "github_projects": ["https://github.com/scikit-learn/scikit-learn"],
                        "videos": ["https://www.youtube.com/watch?v=JcI5Vnw0b2c&list=PLu0W_9lII9ai6fAMHp-acBmJONT7Y4BSG"]
                    }
                },
                {
                    "title": "Data Wrangling and EDA",
                    "description": "Master the art of cleaning, transforming, and exploring datasets to uncover insights and prepare data for modeling (Exploratory Data Analysis).",
                    "difficulty": "Medium",
                    "resources": {
                        "tutorials": ["https://www.kaggle.com/learn/data-cleaning"],
                        "github_projects": ["https://github.com/TarrySingh/Artificial-Intelligence-Deep-Learning-Machine-Learning-Tutorials"],
                        "videos": ["https://www.youtube.com/watch?v=vmEHCJofslg"]
                    }
                },
                {
                    "title": "Advanced Machine Learning",
                    "description": "Explore more complex topics like deep learning (neural networks), natural language processing (NLP), and computer vision.",
                    "difficulty": "Hard",
                    "resources": {
                        "tutorials": ["https://pytorch.org/tutorials/", "https://www.tensorflow.org/tutorials"],
                        "github_projects": ["https://github.com/huggingface/transformers"],
                        "videos": ["https://www.youtube.com/watch?v=G5e-gjIq6bI"]
                    }
                },
                {
                    "title": "MLOps",
                    "description": "Learn the best practices for deploying, monitoring, and maintaining machine learning models in a production environment.",
                    "difficulty": "Hard",
                    "resources": {
                        "tutorials": ["https://ml-ops.org/"],
                        "github_projects": ["https://github.com/iterative/dvc"],
                        "videos": ["https://www.youtube.com/watch?v=j_pJm33_2i8"]
                    }
                },
                {
                    "title": "Build a Portfolio of Projects",
                    "description": "Create a diverse portfolio of data science projects to showcase your skills to potential employers. Participate in Kaggle competitions to hone your skills.",
                    "difficulty": "Hard",
                    "resources": {
                        "tutorials": ["https://www.kaggle.com/competitions"],
                        "github_projects": ["https://github.com/search?q=data-science-portfolio"],
                        "videos": ["https://www.youtube.com/watch?v=p_T_m1M3p_k"]
                    }
                }
            ]
        }
    }

def generate_learning_path(prompt: str):
    """
    Simulates an AI generating a learning path based on a prompt.
    In a real application, this would call a generative AI model.
    """
    
    prompt_lower = prompt.lower()
    
    all_paths = get_learning_paths()
    
    # More sophisticated keyword matching
    matched_path = None
    for path_name, path_data in all_paths.items():
        if any(keyword in prompt_lower for keyword in path_data["keywords"]):
            matched_path = path_data["path"]
            break

    # Generic fallback
    if not matched_path:
        matched_path = [
            {"title": "Define Your Goal", "description": "Clearly articulate what you want to learn and why.", "difficulty": "Easy", "resources": {}},
            {"title": "Break It Down", "description": "Divide the topic into smaller, manageable sub-skills or concepts.", "difficulty": "Easy", "resources": {}},
            {"title": "Find Resources", "description": "Gather tutorials, courses, books, and documentation.", "difficulty": "Easy", "resources": {}},
            {"title": "Practice Consistently", "description": "Apply what you learn through exercises and small projects.", "difficulty": "Medium", "resources": {}},
            {"title": "Build Something Real", "description": "Create a larger project that solves a real-world problem.", "difficulty": "Hard", "resources": {}},
            {"title": "Teach Others", "description": "Explaining the concepts to others is a great way to solidify your understanding.", "difficulty": "Hard", "resources": {}},
        ]
        
    return {
        "prompt": prompt,
        "path": matched_path,
        "estimated_duration": f"{random.randint(4, 12)} weeks"
    }