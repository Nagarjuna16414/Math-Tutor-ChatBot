import streamlit as st
import google.generativeai as genai
import re

# Set up the Gemini API key
genai.configure(api_key="AIzaSyCCGB2lJLonpK7oEfWYe1V76k3f4oQ5rOk")

# Function to check if a query is math-related
def is_math_related(query):
    math_keywords = [
        'equation', 'solve', 'derivative', 'integral', 'algebra', 'calculus',
        'function', 'x', 'y', 'limit', 'sum', 'multiply', 'divide',
        'solve for', 'quadratic', 'geometry', 'calculate', 'area', 'perimeter',
        'volume', 'radius', 'diameter', 'matrix', 'vector', 'mean', 'median', 'mode',
        'standard deviation', 'trigonometry', 'sine', 'cosine', 'tangent', 'angle',
        'pi', 'value of pi', 'pi value', 'approximation of pi', 'integration',
        'tan', 'sin', 'cos', 'log', 'ln', 'factorial', 'probability', 'statistics'
    ]

    # Adding simple arithmetic operators and expressions
    arithmetic_keywords = ['+', '-', '*', '/', '=', 'plus', 'minus', 'times', 'divided by']

    # Adding patterns for trigonometric functions and other math expressions
    math_patterns = [
        r'\btan\b', r'\bsin\b', r'\bcos\b', r'\blog\b', r'\bln\b', r'\bfactorial\b',
        r'\d+\s*[\+\-\*/]\s*\d+',  # Matches simple arithmetic like "2 + 3"
        r'\d+\s*=\s*\d+',          # Matches equations like "2 = 2"
        r'\b\d+\b',                # Matches standalone numbers
    ]

    # Combine keywords and patterns
    all_keywords = math_keywords + arithmetic_keywords
    escaped_keywords = [re.escape(keyword) for keyword in all_keywords]
    all_patterns = escaped_keywords + math_patterns

    # Check if any keyword or pattern is found in the query
    return any(re.search(pattern, query.lower()) for pattern in all_patterns)

# Function to handle math queries using Gemini
def handle_math_query(user_query):
    try:
        if is_math_related(user_query):
            # Initialize the Gemini model
            model = genai.GenerativeModel('models/gemini-1.5-pro-latest')

            # Generate a response
            response = model.generate_content(
                f"You are a math tutor, providing step-by-step solutions to math problems. {user_query}"
            )
            return response.text
        else:
            return "This is a math tutor assistant. Please ask a math-related question only."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Streamlit App Interface
st.set_page_config(page_title="Math Tutor Chatbot", page_icon="🧮", layout="wide")

# Custom CSS for better styling
st.markdown("""
    <style>
        .stApp {
            background-color: #f5f5f5;
            color: #333333;
        }
        .stTextInput input {
            background-color: #ffffff;
            color: #333333;
            border: 1px solid #cccccc;
            border-radius: 5px;
            padding: 10px;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 16px;
            transition: background-color 0.3s ease;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        .chat-bot {
            background-color: #e6f7ff;
            color: #333333;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .user-msg {
            background-color: #ffe0f5;
            color: #333333;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #333333;
        }
        .sidebar .sidebar-content {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title("🧮 Math Tutor Chatbot")
st.markdown("""
    Welcome to the Math Tutor Chatbot! This assistant is here to help you with all your math-related questions. 
    Whether it's algebra, calculus, geometry, or statistics, feel free to ask anything!
""")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.title("Math Tutor Instructions")
    st.markdown("""
        ### How to Use:
        Ask any math-related question, such as solving equations, derivatives, or geometry problems.

        **Examples**:
        1. Solve '2x + 5 = 15'  
        2. What is the derivative of 'x^2'?  
        3. Calculate the area of a circle with radius 7.  

        ### Supported Topics:
        - Algebra  
        - Calculus  
        - Geometry  
        - Trigonometry  
        - Statistics  
        - Probability  
    """)

    # Clear Chat History Button
    if st.button("Clear Chat History", help="Click to clear the chat history"):
        st.session_state.messages = []
        st.rerun()

    # Download Chat History Button
    if st.button("Download Chat History", help="Click to download the chat history as a text file"):
        chat_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])
        st.download_button(
            label="Download Chat",
            data=chat_history,
            file_name="chat_history.txt",
            mime="text/plain"
        )

    # Feedback System
    feedback = st.radio("Was this response helpful?", ("Yes", "No"), help="Provide feedback on the bot's response")
    if feedback:
        st.write(f"Thank you for your feedback: {feedback}")

    # Dark Mode Toggle
    dark_mode = st.checkbox("Dark Mode", help="Toggle between light and dark mode")
    if dark_mode:
        st.markdown("""
            <style>
                .stApp {
                    background-color: #1e1e1e;
                    color: #ffffff;
                }
                .stTextInput input {
                    background-color: #333333;
                    color: #ffffff;
                    border: 1px solid #555555;
                }
                .stButton button {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    padding: 10px 20px;
                    font-size: 16px;
                    transition: background-color 0.3s ease;
                }
                .stButton button:hover {
                    background-color: #45a049;
                }
                .chat-bot {
                    background-color: #2d2d2d;
                    color: #ffffff;
                    padding: 15px;
                    border-radius: 10px;
                    margin-bottom: 10px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }
                .user-msg {
                    background-color: #3d3d3d;
                    color: #ffffff;
                    padding: 15px;
                    border-radius: 10px;
                    margin-bottom: 10px;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }
                .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
                    color: #ffffff;
                }
            </style>
        """, unsafe_allow_html=True)

# Session state for storing messages
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Welcome Message
if not st.session_state.messages:
    st.session_state.messages.append({"role": "bot", "content": "Welcome! I'm your math tutor. Ask me anything math-related."})

# Display conversation history
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'<div class="user-msg"><strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bot"><strong>Bot:</strong> {message["content"]}</div>', unsafe_allow_html=True)

# User input
user_input = st.text_input("Ask a math question:", placeholder="Type your math question here...")

# Submit button with loading spinner
if st.button("Send", help="Click to send your question"):
    if user_input:
        # Add user input to session state
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Get response with loading spinner
        with st.spinner("Generating response..."):
            bot_response = handle_math_query(user_input)
            st.session_state.messages.append({"role": "bot", "content": bot_response})
        st.rerun()  # Refresh to display the new message