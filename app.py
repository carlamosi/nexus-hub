"""
app.py — The Streamlit orchestrator.
Initializes memory, executes agents sequentially, handles state.
"""

import sys
import os

from memory.shared_memory import SharedMemory
import streamlit as st

# MUST BE THE FIRST CALL
st.set_page_config(
    page_title="Qui queda fora del futur?",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

from agents.scout import ScoutAgent
from agents.cleaner import CleanerAgent
from agents.skeptic import SkepticAgent
from agents.storyteller import StorytellerAgent
from agents.web_builder import WebBuilderAgent

def initialize_memory():
    if "memory" not in st.session_state:
        st.session_state.memory_obj = SharedMemory()
        st.session_state.pipeline_run = False

def run_pipeline():
    memory = st.session_state.memory_obj
    
    # Empty memory container
    memory = SharedMemory()
    st.session_state.memory_obj = memory
    
    status_box = st.sidebar.empty()
    
    with st.spinner("⏳ ScoutAgent: Obtenint dades..."):
        ScoutAgent().run(memory)
        
    with st.spinner("⏳ CleanerAgent: Netejant metadades..."):
        CleanerAgent().run(memory)
        
    with st.spinner("⏳ SkepticAgent: Audit statistica..."):
        SkepticAgent().run(memory)
        
    # Feedback loop: if instructions, apply them
        fb = memory.get("feedback_loop")
        if fb:
            with st.spinner("⏳ CleanerAgent: Aplicant correccions del feedback loop..."):
                CleanerAgent().apply_feedback(memory)
                
    with st.spinner("⏳ StorytellerAgent: Generant resultats..."):
        StorytellerAgent().run(memory)
        
    st.session_state.pipeline_run = True


def main():
    initialize_memory()
    memory = st.session_state.memory_obj

    # Render sidebar controls
    st.sidebar.markdown("# Qui queda fora del futur?")
    st.sidebar.markdown("### Exclusió Femenina en la Tecnologia")
    
    st.sidebar.markdown("---")
    
    if st.sidebar.button("RUN PIPELINE", use_container_width=True, type="primary"):
        run_pipeline()
        
    if st.sidebar.button("CLEAR AND RERUN", use_container_width=True):
        st.session_state.memory_obj = SharedMemory()
        run_pipeline()
    
    st.sidebar.markdown("---")
    
    # Sidebar Pipeline Status
    st.sidebar.markdown("### Estat del Pipeline")
    logs = memory.get("pipeline_log", [])
    
    agents = ['ScoutAgent', 'CleanerAgent', 'SkepticAgent', 'StorytellerAgent', 'WebBuilderAgent']
    
    for agent_name in agents:
        agent_logs = [l for l in logs if l['agent'] == agent_name]
        if agent_logs:
            last_lvl = agent_logs[-1]['level']
            icon = "✅" if last_lvl == "SUCCESS" else ("⚠️" if last_lvl in ["WARN", "ERROR"] else "🔄")
            st.sidebar.markdown(f"{icon} **{agent_name}**")
        else:
            st.sidebar.markdown(f"⏳ **{agent_name}**")
            
    # Source coverage
    cov = memory.get("coverage_score", 0)
    st.sidebar.metric("Cobertura de Dades", f"{cov:.0f}%")
    
    # Alerts
    alerts = memory.get("alerts", [])
    if alerts:
        st.sidebar.markdown("### Alertes Detectades")
        for a in alerts:
            st.sidebar.error(f"⚠️ {a['message']}")
            
    # Feedback loop log
    fb = memory.get("feedback_loop", [])
    if fb:
        st.sidebar.markdown("### 🔄 Feedback Loop")
        for f in fb:
            st.sidebar.warning(f"SKEPTIC → CLEANER: {f['instruction']}")

    # Delegate main body rendering to the WebBuilderAgent
    WebBuilderAgent().run(memory)

if __name__ == "__main__":
    main()
