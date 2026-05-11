import streamlit as st
import time
from agents import OrchestrationAgent

# Initialize the orchestration agent
@st.cache_resource
def get_orchestrator():
    return OrchestrationAgent()

orchestrator = get_orchestrator()

# --- Custom Styling (Rich Aesthetics) ---
st.set_page_config(
    page_title="Seminar Sensei",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Use some custom CSS for a premium look
st.markdown("""
<style>
    .main-header {
        font-size: 3rem !important;
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #888;
        margin-bottom: 2rem;
    }
    .agent-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #1E1E1E;
        border-left: 5px solid #4ECDC4;
        margin-bottom: 15px;
    }
    .agent-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #4ECDC4;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- UI Setup ---
st.markdown('<p class="main-header">Seminar Sensei 🎓</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Your Agentic AI Assistant for Research Paper Seminars.</p>', unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Configuration")
    st.info("Upload a research paper and select the action you want the agents to perform.")
    
    # 1. Input Agent Simulation
    st.subheader("1. Input Document")
    uploaded_file = st.file_uploader("Upload IEEE Paper (PDF/TXT)", type=["pdf", "txt"])
    
    # 2. Action Selection
    st.subheader("2. Select Action")
    action = st.selectbox("What would you like to do?", [
        "Understand paper",
        "Presentation Script",
        "PPT creation",
        "Q&A generation"
    ])
    
    # 3. Action-Specific Options
    translate = False
    language = "English"
    if action == "Understand paper":
        st.subheader("Options")
        translate = st.checkbox("Translate explanation?")
        if translate:
            language = st.selectbox("Select Language", ["Spanish", "French", "Hindi", "Malayalam", "Tamil", "German"])
            
    start_button = st.button("🚀 Run Workflow", use_container_width=True, type="primary")

# --- Main Workflow Execution ---
if start_button:
    if not uploaded_file:
        st.error("Please upload a document to proceed.")
    else:
        st.write("---")
        
        # We will use mock text if it's a PDF to avoid complex parsing in the prototype
        # Or read text if it's a TXT file
        if uploaded_file.name.endswith(".txt"):
            doc_text = str(uploaded_file.read(), "utf-8")
        else:
            doc_text = "Mock extracted text from PDF..."
            
        doc_name = uploaded_file.name
        
        with st.status("Running Seminar Sensei Agentic Workflow...", expanded=True) as status:
            
            # Simulated workflow output placeholder
            st.markdown("### Agent Processing Log")
            log_container = st.container()
            
            # Step 1: Input Agent
            with log_container:
                st.markdown('<div class="agent-box"><div class="agent-header">📥 Input Agent</div>Validating document...</div>', unsafe_allow_html=True)
            
            # Call Orchestrator
            results = orchestrator.handle_request(
                document_name=doc_name,
                document_text=doc_text,
                action=action,
                translate=translate,
                language=language
            )
            
            # Check Input Validation
            if not results["input"]["is_valid"]:
                status.update(label="Workflow stopped.", state="error", expanded=True)
                st.error(results["input"]["message"])
            else:
                with log_container:
                    st.success(f"Input Agent: {results['input']['message']}")
                
                # Step 2: Segmentation Agent
                time.sleep(1) # Visual delay
                with log_container:
                    st.markdown('<div class="agent-box"><div class="agent-header">🔪 Segmentation Agent</div>Splitting paper into topics...</div>', unsafe_allow_html=True)
                    st.success(f"Segmentation Agent: {results['segmentation']['message']}")
                    with st.expander("View Segments"):
                        for sec in results['segmentation']['sections']:
                            st.write(f"- **{sec['title']}**")
                            
                # Step 3: Propagated Agent
                time.sleep(1)
                agent_name_map = {
                    "understanding": "🧠 Understanding Agent",
                    "presentation_script": "📝 Presentation Script Agent",
                    "ppt_creation": "📊 PPT Creation Agent",
                    "qa": "❓ Q&A Agent"
                }
                
                action_type = results["action_type"]
                agent_title = agent_name_map.get(action_type, "Unknown Agent")
                
                with log_container:
                    st.markdown(f'<div class="agent-box"><div class="agent-header">{agent_title}</div>Executing requested action...</div>', unsafe_allow_html=True)
                
                status.update(label="Workflow completed successfully!", state="complete", expanded=False)
                
        # --- Display Final Results ---
        st.header("🎯 Final Output")
        
        action_result = results["action_result"]
        
        if action_type == "understanding":
            st.info(action_result["message"])
            for summary in action_result["summaries"]:
                with st.expander(f"Section: {summary['title']}", expanded=True):
                    st.write(summary['simplified_content'])
                    
        elif action_type == "presentation_script":
            st.success(action_result["message"])
            st.subheader("Introduction")
            st.write(action_result["introduction"])
            
            st.subheader("Key Highlights")
            for h in action_result["highlights"]:
                st.write(f"- {h}")
                
            st.subheader("Script Draft")
            st.write(action_result["final_script"])
            
        elif action_type == "ppt_creation":
            st.success(action_result["message"])
            # Display slides as cards
            cols = st.columns(3)
            for i, slide in enumerate(action_result["slides"]):
                col = cols[i % 3]
                with col:
                    st.markdown(f"""
                    <div style="border: 1px solid #4ECDC4; border-radius: 8px; padding: 15px; margin-bottom: 15px; background: #2A2A2A; min-height: 200px;">
                        <h4 style="color: white; margin-top: 0;">Slide {slide['slide_number']}: {slide['title']}</h4>
                        <ul style="color: #DDD; padding-left: 20px;">
                            {''.join([f'<li>{item}</li>' for item in slide['content']])}
                        </ul>
                    </div>
                    """, unsafe_allow_html=True)
                    
        elif action_type == "qa":
            st.success(action_result["message"])
            
            st.subheader("Potential Questions & Answers")
            for qa in action_result["questions_answers"]:
                with st.expander(f"Q: {qa['q']}"):
                    st.write(f"**A:** {qa['a']}")
                    
            st.subheader("Theory & Proof Verification")
            if action_result["proof_present"]:
                st.success(f"✅ Proofs found: {action_result['proof_details']}")
            else:
                st.warning("⚠️ No mathematical proofs explicitly found. Highlight theories that may require further explanation.")

else:
    # Landing page state
    st.info("👈 Please upload a document and select an action from the sidebar to begin.")
    
    st.markdown("### Agent Architecture Diagram")
    st.caption("The tool follows the agentic orchestration flow requested:")
    
    # Text-based flowchart to represent the system visually for now
    st.code("""
    [User Uploads Paper] -> (Input Agent) 
                                 | Validates IEEE/Publication
                                 v
                        (Orchestration Agent)
                                 |
                                 +-> (Segmentation Agent) -> Splits into topics
                                 |
                                 +---> If "Understand": (Understanding Agent)
                                 |
                                 +---> If "Script": (Presentation Script Agent)
                                 |
                                 +---> If "PPT": (PPT Creation Agent)
                                 |
                                 +---> If "Q&A": (Q&A Agent)
    """, language="text")
