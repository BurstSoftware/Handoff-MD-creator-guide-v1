import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Handoff MD Creator Guide", layout="wide", page_icon="🛠️")
st.title("🛠️ Handoff MD Creator Guide")
st.markdown("**Compress context • Spin off clean tasks • Enable DIY sub-agents**")

# Sidebar Navigation
page = st.sidebar.radio("Guide Sections", [
    "Introduction",
    "Why Handoff?",
    "Handoff vs Compact",
    "Real Usage Examples",
    "Powerful Patterns",
    "Creator Tool",
    "Best Practices",
    "The Skill Itself"
])

if page == "Introduction":
    st.header("What is the Handoff Skill?")
    st.write("""
    The **Handoff** skill takes relevant context from your current AI session and compresses it into a clean, focused Markdown document 
    that a fresh agent (in a new session) can pick up and continue from.
    """)
    st.success("Created because the creator was manually writing handoff documents **so often** that it became a reusable skill.")

elif page == "Why Handoff?":
    st.header("Why Create This Skill?")
    st.write("""
    Even with massive context windows (200K–1M tokens), performance drops dramatically once you leave the **Smart Zone** (~120K tokens or less). 
    
    The agent gets "dumber" as attention becomes diffuse.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("The Problem")
        st.write("- One long session → diluted focus\n- Side tasks pollute the main goal\n- Hard to spin off independent work")
    with col2:
        st.subheader("The Solution")
        st.write("- Keep sessions pure and focused\n- Hand off specific slices of work\n- Run multiple independent sessions in parallel")

elif page == "Handoff vs Compact":
    st.header("Handoff vs Compact")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Compact (Built-in)")
        st.write("Summarizes the **entire** conversation. Good for long single-goal sessions (e.g. deep debugging). Creates sediment layers over time.")
    with col2:
        st.subheader("Handoff (Custom Skill)")
        st.write("Extracts a **specific slice** of work into a clean document. Keeps original session pure. Perfect for parallel or side tasks.")

elif page == "Real Usage Examples":
    st.header("Real Usage – Grilling Session Example")
    st.write("""
    **Scenario**: Inside a grilling session for Suncastle (software factory) planning.
    
    While answering questions in **Q2**, you realize:
    > “In the future we may want to move iterations and the completion signal onto a separate API.”
    """)
    
    st.info("""
    **Handoff Prompt Used**:
    “Let’s hand off that task to a separate agent. Create a handoff.md document…”
    """)
    
    st.write("""
    **Benefits observed**:
    - Sharpens the current session (declares the task out-of-scope)
    - Creates a clean, focused starting point for the new session
    """)

elif page == "Powerful Patterns":
    st.header("Powerful Patterns")
    
    st.subheader("1. Grilling → Prototype Handoff")
    st.write("""
    During grilling, when you hit complex UI or logic that needs to be seen in code:
    - Hand off the difficult bits (e.g. window communication, TL drawer, decay aggression)
    - Run a large prototype session (169K tokens in one example)
    - Then create a **return handoff** with learnings back to the original planner
    """)
    
    st.subheader("2. Bidirectional / DIY Sub-Agents")
    st.write("""
    Initial session → Handoff → Prototype session → Return Handoff → Back to original session.
    
    This pattern gives you real sub-agent workflows using only Markdown documents.
    """)
    
    st.subheader("3. Model-Agnostic Collaboration")
    st.write("""
    Because handoffs are plain Markdown, you can:
    - Start in Claude Code
    - Hand off to Cursor, Copilot, or any other agent
    - Do adversarial review between different models
    """)

elif page == "Creator Tool":
    st.header("🎯 Handoff MD Creator Tool")
    st.markdown("Fill the fields below and generate a ready-to-use handoff document.")

    col1, col2 = st.columns([1, 1])
    
    with col1:
        project = st.text_input("Project / Session Name", "Suncastle Q2 Planning")
        main_goal = st.text_area("Main Goal of Original Session", 
            "Planning future features and architecture for Suncastle software factory", height=100)
        task = st.text_area("Task to Handoff", 
            "Split iterations and completion signal into a separate API", height=100)
        purpose = st.text_area("Purpose of Next Session (what the new agent should focus on)", 
            "Create a clean, decoupled API for handling iterations and completion signals.", height=80)
    
    with col2:
        reason = st.text_area("Reason for Handoff", 
            "This is out of scope for the current Q2 grilling session but needed for future modularity.", height=80)
        context = st.text_area("Key Context & Decisions So Far", 
            "• Grilling session currently in Q2\n• Decided to decouple iteration logic\n• Previous prototype covered window communication and TL drawer", height=150)
        suggested_skills = st.text_area("Suggested Skills / Tools for New Agent", 
            "griller, prototype, diagnose, create_issue", height=100)
        pointers = st.text_area("Pointers to Other Artifacts (do not duplicate)", 
            "- See prototype branch: feature/tl-drawer\n- GitHub issue #42\n- Existing API patterns in src/core/", height=100)

    if st.button("Generate Handoff Document", type="primary", use_container_width=True):
        md_content = f"""# Handoff: {task}

## Project
**{project}**

## Original Session Goal
{main_goal}

## Task
{task}

## Purpose of This New Session
{purpose}

## Reason for Handoff
{reason}

## Relevant Context & Decisions
{context}

## Pointers to Existing Artifacts
{pointers or "Refer to existing files / issues instead of duplicating content."}

## Suggested Skills
{suggested_skills or "Use appropriate skills (e.g. prototype, griller, diagnose) as needed."}

## Instructions for New Agent
1. Start fresh with the focus described above.
2. **Do not duplicate** content already captured elsewhere — use pointers.
3. Redact any sensitive information (API keys, passwords, PII).
4. When complete, create a **return handoff** with key learnings, files changed, and non-obvious insights.

---
**Handoff generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Saved to OS temporary directory • Disposable**
"""

        st.success("Handoff document generated!")
        st.code(md_content, language="markdown")
        
        st.download_button(
            label="⬇️ Download handoff.md",
            data=md_content,
            file_name="handoff.md",
            mime="text/markdown"
        )

elif page == "Best Practices":
    st.header("Best Practices")
    st.markdown("""
    - **Always** describe the purpose/reason for the handoff (what the next session should focus on)
    - Include a **Suggested Skills** section (griller, prototype, diagnose, etc.) so the new agent can immediately invoke the right tools
    - **Do not duplicate** content — use pointers to GitHub issues, other markdown files, prototypes, etc.
    - Save handoff files to the **OS temporary directory** (disposable, not part of permanent codebase)
    - **Redact** sensitive information (API keys, passwords, PII)
    - Use handoffs to create clean bidirectional flows between sessions
    """)

elif page == "The Skill Itself":
    st.header("The Handoff Skill")
    st.write("""
    The skill is intentionally simple and powerful:
    
    > “Write a handoff document summarizing the current conversation (or specific slice) so a fresh agent can continue the work. Save it to the temporary directory of the user’s operating system.”
    """)
    
    st.info("""
    **Key Design Decisions in the Skill**:
    - Suggested Skills section for instant tool invocation
    - Emphasis on pointers instead of duplication
    - Temporary directory storage (disposable)
    - Built-in redaction guidance
    - Requires clear purpose of the next session
    """)
    
    st.success("This skill has quickly become essential in the creator’s daily AI coding workflow.")

st.caption("Built as a single-file Streamlit guide • Continuously updated with real usage insights")
