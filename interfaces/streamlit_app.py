'''import streamlit as st
from services.agent_orchestration import AgentOrchestrator
import re

def main():
    st.title("AI-powered Virtual Development Pod")
    st.subheader("Project Manager Dashboard")
    
    st.markdown("### Enter High-Level Business Requirements")
    business_requirements = st.text_area("Business Requirements", height=200, 
                                         placeholder="Provide your high-level business requirements here...")
    
    if st.button("Run Project Workflow"):
        if not business_requirements.strip():
            st.error("Please enter valid business requirements.")
        else:
            st.info("Orchestrating the agents... Please wait.")
            orchestrator = AgentOrchestrator()
            results = orchestrator.orchestrate_pipeline(business_requirements)
            
            st.success("Workflow Execution Completed!")
            
            st.markdown("#### Generated User Stories")
            st.text_area("User Stories", value=results.get("user_stories", ""), height=150)
            
            st.markdown("#### Generated Design Artifact")
            st.text_area("Design Artifact", value=results.get("design_artifact", ""), height=150)
            
            st.markdown("#### Generated Source Code")
            st.text_area("Source Code", value=results.get("code", ""), height=150)
            
            st.markdown("#### Generated Test Cases")
            st.text_area("Test Cases", value=results.get("test_cases", ""), height=150)
            
            st.markdown("#### Test Execution Results")
            st.text_area("Test Results", value=results.get("test_results", ""), height=150)

if __name__ == '__main__':
    main()
'''

'''import streamlit as st
from services.agent_orchestration import AgentOrchestrator
from services.language_model_integration import gemini_generate
import re
import datetime

# Set page configuration for a wide layout
st.set_page_config(page_title="AI-powered Virtual Development Pod", layout="wide")

# Custom CSS for a professional, colorful interface with containerized boxes and bold headings
st.markdown("""
    <style>
    body {
        background-color: #f0f4f7;
    }
    .main-container {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 20px;
        margin: 20px auto;
        max-width: 1200px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .artifact-box {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        font-size: 16px;
        line-height: 1.6;
    }
    .artifact-box h4 {
        margin-top: 0;
        color: #1565c0;
        font-weight: bold;
    }
    .artifact-box p {
        margin: 10px 0;
    }
    .stCodeBlock pre {
        background-color: #fce4ec !important;
        border: 2px solid #f48fb1 !important;
        border-radius: 6px !important;
        font-size: 15px !important;
        padding: 15px !important;
        white-space: pre-wrap;
    }
    .conversation-box {
        background-color: #e8f5e9;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        font-size: 16px;
        line-height: 1.6;
    }
    .conversation-box h4 {
        margin-top: 0;
        color: #2e7d32;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

def clean_text(text: str) -> str:
    """
    Remove unwanted characters (#, *, -) while preserving newline characters.
    """
    cleaned = re.sub(r"[#\*\-]+", "", text)
    cleaned = re.sub(r"[ ]{2,}", " ", cleaned)
    return cleaned.strip()

def display_artifact(title: str, content: str, language: str = None):
    """
    Displays a title (bold) and its associated content within one containerized box.
    If language is provided, content is rendered as syntax-highlighted code.
    """
    heading_html = f"<h4><strong>{title}</strong></h4>"
    if language:
        st.markdown(f"<div class='artifact-box'>{heading_html}</div>", unsafe_allow_html=True)
        st.code(content, language=language)
    else:
        paragraphs = content.splitlines()
        html_content = f"<div class='artifact-box'>{heading_html}"
        for p in paragraphs:
            if p.strip():
                html_content += f"<p>{p.strip()}</p>"
        html_content += "</div>"
        st.markdown(html_content, unsafe_allow_html=True)

def chat_with_agent(agent_role: str, message: str) -> str:
    """
    Simulate a conversation with the specified agent.
    The prompt is constructed to include a respectful greeting, a clear and direct question,
    and instructions to respond in a confident, professional tone without uncertainty.
    """
    # Determine greeting based on current time (morning/afternoon/evening)
    current_hour = datetime.datetime.now().hour
    if current_hour < 12:
        greeting = "Good morning"
    elif current_hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    
    # Construct a prompt that forces a professional, direct response
    prompt = (f"Respected Sir, {greeting}. I am the Project Manager. "
              f"My question for you, as the {agent_role}, is: '{message}'.\n"
              "Please provide a detailed, confident update on your progress and quality, "
              "with no tentative language. Your response should be clear, direct, and professional. "
              "Conclude your response with 'Thank you, with regards.'")
    response = gemini_generate(prompt)
    return response

def display_conversation(agent_role: str):
    """
    Display the conversation history for the specified agent with the most recent chat on top.
    """
    history = st.session_state.conversation_history.get(agent_role, [])
    if history:
        # Reverse the history list so the most recent chat is on top.
        history = history[::-1]
        conversation_html = f"<div class='conversation-box'><h4><strong>Conversation with {agent_role}</strong></h4>"
        for entry in history:
            speaker, msg = entry
            conversation_html += f"<p><strong>{speaker}:</strong> {msg}</p>"
        conversation_html += "</div>"
        st.markdown(conversation_html, unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='conversation-box'><h4><strong>Conversation with {agent_role}</strong></h4><p>No conversation yet.</p></div>", unsafe_allow_html=True)

# Initialize conversation history in session_state if not already present
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = {role: [] for role in ["Business Analyst Agent", "Design Agent", "Developer Agent", "Testing Agent"]}

def main():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.title("AI-powered Virtual Development Pod")
    st.subheader("Project Manager Dashboard")
    
    st.markdown("### Enter High-Level Business Requirements")
    business_requirements = st.text_area(
        "Business Requirements", 
        height=250, 
        placeholder="Provide your high-level business requirements here..."
    )
    
    if st.button("Run Project Workflow"):
        if not business_requirements.strip():
            st.error("Please enter valid business requirements.")
        else:
            st.info("Orchestrating the agents... Please wait.")
            orchestrator = AgentOrchestration = AgentOrchestrator()
            results = AgentOrchestration.orchestrate_pipeline(business_requirements)
            st.success("Workflow Execution Completed!")
            
            # Clean the results text to remove unwanted symbols
            user_stories = clean_text(results.get("user_stories", ""))
            design_artifact = clean_text(results.get("design_artifact", ""))
            code_result = clean_text(results.get("code", ""))
            test_cases = clean_text(results.get("test_cases", ""))
            test_results = clean_text(results.get("test_results", ""))
            
            # Display each artifact within its containerized box
            display_artifact("Generated User Stories", user_stories)
            display_artifact("Generated Design Artifact", design_artifact)
            display_artifact("Generated Source Code", code_result, language='python')
            display_artifact("Generated Test Cases", test_cases)
            display_artifact("Test Execution Results", test_results)
    
    st.markdown("### Chat with an Agent")
    agent_choice = st.selectbox("Choose an Agent", list(st.session_state.conversation_history.keys()))
    user_message = st.text_input("Your Message to the Agent", placeholder="Type your message here...")
    if st.button("Send Message"):
        if not user_message.strip():
            st.error("Please enter a message.")
        else:
            # Append the Project Manager's message to the conversation history
            st.session_state.conversation_history[agent_choice].append(("Project Manager", user_message))
            # Get the agent's response
            response = chat_with_agent(agent_choice, user_message)
            st.session_state.conversation_history[agent_choice].append((agent_choice, response))
    
    # Display conversation history for the selected agent (most recent on top)
    display_conversation(agent_choice)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()
'''

import streamlit as st
from services.agent_orchestration import AgentOrchestrator
from services.language_model_integration import gemini_generate
from dotenv import load_dotenv
import re
import datetime
import warnings

# Suppress specific numpy RuntimeWarnings to reduce log clutter.
warnings.filterwarnings("ignore", category=RuntimeWarning)

# Load environment variables from .env.
load_dotenv()

# Set page configuration for a wide layout.
st.set_page_config(page_title="AI-powered Virtual Development Pod", layout="wide")

# Custom CSS for a professional, colorful interface with containerized boxes and scroll bars.
st.markdown("""
    <style>
    body {
        background-color: #f0f4f7;
    }
    .main-container {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 20px;
        margin: 20px auto;
        max-width: 1200px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .artifact-box {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        font-size: 16px;
        line-height: 1.6;
        overflow-y: auto;
        max-height: 400px;
    }
    .artifact-box h4 {
        margin-top: 0;
        color: #1565c0;
        font-weight: bold;
        text-decoration: underline;
    }
    .artifact-box p {
        margin: 10px 0;
    }
    .stCodeBlock pre {
        background-color: #fce4ec !important;
        border: 2px solid #f48fb1 !important;
        border-radius: 6px !important;
        font-size: 15px !important;
        padding: 15px !important;
        white-space: pre-wrap;
    }
    .conversation-box {
        background-color: #e8f5e9;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        font-size: 16px;
        line-height: 1.6;
        overflow-y: auto;
        max-height: 400px;
    }
    .conversation-box h4 {
        margin-top: 0;
        color: #2e7d32;
        font-weight: bold;
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)

# Define agent roles with their precise responsibilities.
AGENT_ROLES = {
    "Business Analyst Agent": "is responsible for creating detailed and structured user stories from high-level business requirements.",
    "Design Agent": "is responsible for generating precise software design artifacts and corresponding flow charts based on the user stories.",
    "Developer Agent": "is responsible for producing well-indented, production-quality source code and providing a clear folder structure for the project.",
    "Testing Agent": "is responsible for generating comprehensive test cases and delivering definitive test execution results in an industry-standard format.",
    "Security Analyst Agent": "is responsible for reviewing the source code for vulnerabilities and potential threats, and providing a comprehensive security analysis.",
    "Performance Agent": "is responsible for identifying performance bottlenecks and suggesting specific, measurable optimization strategies."
}

def clean_text(text: str) -> str:
    """
    Remove unwanted characters (#, *, -) while preserving newline characters.
    """
    # The asterisk (*) does not need escaping inside a character set.
    cleaned = re.sub(r"[#*\-]+", "", text)
    cleaned = re.sub(r"[ ]{2,}", " ", cleaned)
    return cleaned.strip()

def display_artifact(title: str, content: str, language: str = None):
    """
    Display the artifact in a containerized box.
    For the design artifact, render as preformatted text (ideal for diagrams).
    For source code, render using syntax highlighting.
    Otherwise, render the content as plain paragraphs.
    """
    heading_html = f"<h4><strong>{title}</strong></h4>"
    
    if title == "Generated Design Artifact":
        full_html = f"<div class='artifact-box'>{heading_html}<pre>{content}</pre></div>"
        st.markdown(full_html, unsafe_allow_html=True)
    elif language:
        st.markdown(f"<div class='artifact-box'>{heading_html}</div>", unsafe_allow_html=True)
        st.code(content, language=language)
    else:
        paragraphs = content.splitlines()
        html_content = f"<div class='artifact-box'>{heading_html}"
        for p in paragraphs:
            if p.strip():
                html_content += f"<p>{p.strip()}</p>"
        html_content += "</div>"
        st.markdown(html_content, unsafe_allow_html=True)

def chat_with_agent(agent_role: str, message: str) -> str:
    """
    Simulate a conversation with the specified agent.
    Constructs a prompt that includes a respectful greeting, the global project context,
    and explicit domain instructions to ensure that the agent responds only within its area.
    """
    current_hour = datetime.datetime.now().hour
    if current_hour < 12:
        greeting = "Good morning"
    elif current_hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    
    global_context = st.session_state.get("project_context", "")
    
    domain_instructions = {
        "Business Analyst Agent": "You are a Business Analyst. Answer only questions about requirements, user stories, acceptance criteria, and story points.",
        "Design Agent": "You are a Design Agent. Answer only questions about system design, architecture, and diagrams.",
        "Developer Agent": "You are a Developer Agent. Answer only questions about source code, coding practices, and folder structure.",
        "Testing Agent": "You are a Testing Agent. Answer only questions about test cases and execution results.",
        "Security Analyst Agent": "You are a Security Analyst. Answer only questions about security vulnerabilities and recommendations.",
        "Performance Agent": "You are a Performance Agent. Answer only questions about performance optimization and code efficiency."
    }
    instruction = domain_instructions.get(agent_role, "")
    
    prompt = (
        f"Respected Sir, {greeting}. I am the Project Manager. "
        f"The project is defined as: {global_context}. "
        f"My question for you, as the {agent_role}, is: '{message}'. "
        f"{instruction} "
        "Provide a detailed and definitive update on the quality, progress, and results of your artifact. "
        "Your response must be complete, professional, and entirely free of any placeholders, uncertainty, or fill-in blanks. "
        "Respond with absolute clarity and certainty. End your response with 'Thank you, with regards.'"
    )
    response = gemini_generate(prompt)
    return response

def display_conversation(agent_role: str):
    """
    Display the conversation history for the specified agent with the most recent message on top.
    Each conversation is shown in a scrollable container.
    """
    # Initialize conversation_history if not present.
    st.session_state.setdefault("conversation_history", {role: [] for role in AGENT_ROLES.keys()})
    history = st.session_state["conversation_history"].get(agent_role, [])
    if history:
        reversed_history = history[::-1]
        conversation_html = f"<div class='conversation-box'><h4><strong>Conversation with {agent_role}</strong></h4>"
        for speaker, msg in reversed_history:
            conversation_html += f"<p><strong>{speaker}:</strong> {msg}</p>"
        conversation_html += "</div>"
        st.markdown(conversation_html, unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='conversation-box'><h4><strong>Conversation with {agent_role}</strong></h4><p>No conversation yet.</p></div>", unsafe_allow_html=True)

def main():
    # Initialize session state keys if not present.
    st.session_state.setdefault("conversation_history", {role: [] for role in AGENT_ROLES.keys()})
    st.session_state.setdefault("project_context", "")
    st.session_state.setdefault("master_output", {})

    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.title("AI-powered Virtual Development Pod")
    st.subheader("Project Manager Dashboard")
    
    st.markdown("### Enter High-Level Business Requirements")
    business_requirements = st.text_area(
        "Business Requirements",
        height=250,
        placeholder="Provide your high-level business requirements here..."
    )
    
    # Run master workflow and store output and context.
    if st.button("Run Project Workflow"):
        if not business_requirements.strip():
            st.error("Please enter valid business requirements.")
        else:
            st.info("Coordinating the agents... Please wait.")
            from services.agent_orchestration import AgentOrchestrator
            orchestrator = AgentOrchestrator()
            results = orchestrator.orchestrate_pipeline(business_requirements)
            st.success("Workflow Execution Completed!")
            st.session_state["project_context"] = business_requirements.strip()
            st.session_state["master_output"] = results
    
    # Always display the master output if available.
    if st.session_state.get("master_output"):
        master = st.session_state["master_output"]
        user_stories = clean_text(master.get("user_stories", ""))
        design_artifact = clean_text(master.get("design_artifact", ""))
        code_result = clean_text(master.get("code", ""))
        test_cases = clean_text(master.get("test_cases", ""))
        test_results = clean_text(master.get("test_results", ""))
        security_analysis = clean_text(master.get("security_report", ""))
        performance_optimization = clean_text(master.get("performance_report", ""))
        
        display_artifact("Generated User Stories", user_stories)
        display_artifact("Generated Design Artifact", design_artifact)
        display_artifact("Generated Source Code", code_result, language='python')
        display_artifact("Generated Test Cases", test_cases)
        display_artifact("Test Execution Results", test_results)
        display_artifact("Security Analysis Report", security_analysis)
        display_artifact("Performance Optimization Suggestions", performance_optimization)
    
    st.markdown("### Chat with an Agent")
    conversation_dict = st.session_state.get("conversation_history", {})
    agent_choice = st.selectbox("Choose an Agent", list(conversation_dict.keys()))
    user_message = st.text_input("Your Message to the Agent", placeholder="Type your message here...")
    if st.button("Send Message"):
        if not user_message.strip():
            st.error("Please enter a message.")
        else:
            st.session_state["conversation_history"][agent_choice].append(("Project Manager", user_message))
            response = chat_with_agent(agent_choice, user_message)
            st.session_state["conversation_history"][agent_choice].append((agent_choice, response))
    
    display_conversation(agent_choice)
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()
