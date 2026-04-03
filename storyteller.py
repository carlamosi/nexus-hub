"""
🗣️ THE STORYTELLER — Agent v4 (The Defensive Narrator)
Impact narrative generator for the IBTG Pipeline.
Engages in 4 rounds of debate and generates the final conclusions.
"""

import csv
import json
import os
import sys

# Forzar UTF-8 para evitar errores con emojis en Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
from langchain_groq import ChatGroq

class StorytellerAgent:
    def __init__(self, groq_key):
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=groq_key)

    def read_brain(self):
        """Lee el estado actual de la investigación."""
        brain_path = 'reports/brain.json'
        if not os.path.exists(brain_path): return {}
        with open(brain_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def save_draft(self, draft):
        """Guarda la defensa de la narrativa en el cerebro."""
        brain_path = 'reports/brain.json'
        try:
            with open(brain_path, 'r', encoding='utf-8') as f:
                brain = json.load(f)
            brain["findings"]["storyteller"]["drafts"].append(draft)
            with open(brain_path, 'w', encoding='utf-8') as f:
                json.dump(brain, f, indent=4)
        except: pass

    def write_story(self, brain):
        print("\n" + "*"*60)
        print("📣 EL STORYTELLER ESTÁ DEFIENDO LA NARRATIVA FRENTE AL CRÍTICO...")
        print("*"*60)

        # Contexto del debate completo
        findings = brain.get("findings", {})
        critiques = findings.get("skeptic", {}).get("critiques", [])
        anomalies = findings.get("skeptic", {}).get("anomalies", [])
        whispers = findings.get("cleaner", {}).get("whispers", [])
        refinements = findings.get("scout", {}).get("refinements", [])
        latest_critique = critiques[-1] if critiques else "Aún no hay críticas."
        
        prompt = f"""
        Eres un SINTETIZADOR DE NARRATIVAS DE INVESTIGACIÓN (El Alquimista). 
        Tu misión es defender y elevar la investigación de Carla usando estos inputs:
        
        CRÍTICA ACTUAL: "{latest_critique}"
        ANOMALÍAS MATEMÁTICAS: {anomalies}
        SUSURROS DEL CLEANER (Vacíos): {whispers}
        REFINAMIENTOS DEL SCOUT: {refinements}
        
        INSTRUCCIONES:
        1. Responde al ataque científico sin negar los fallos, sino integrándolos como 'Lunas Nuevas' (datos ocultos).
        2. Mantén el tono de 'Misterio Estadístico'.
        3. Crea una síntesis: ¿Por qué esas anomalías demuestran que la brecha de género es más compleja de lo que parece?
        4. Si es la Ronda Final, genera un informe Markdown de alto impacto.
        """

        story = self.llm.invoke(prompt)
        print(story.content)
        self.save_draft(story.content)
        
        # Guardar en archivo de texto final si es necesario
        if not os.path.exists('reports'): os.makedirs('reports')
        with open('reports/final_conclusions.txt', 'w', encoding='utf-8') as f:
            f.write(story.content)

if __name__ == "__main__":
    GROQ_KEY = os.getenv("GROQ_API_KEY") # Clave protegida para Cloud Deployment

    agent = StorytellerAgent(GROQ_KEY)
    brain = agent.read_brain()
    if brain: agent.write_story(brain)
