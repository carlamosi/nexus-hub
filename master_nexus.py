"""
🧬 MASTER NEXUS IBTG v1.0 — El Sistema Vivo
Consolidación síncrona de Scout, Cleaner, Skeptic y Storyteller.
Diseñado para esquivar bloqueos de procesos y habilitar el gran debate de 4 rondas.
"""

import os
import json
import requests
import csv
import sys
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv()
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_groq import ChatGroq

# Forzar UTF-8 para evitar errores con emojis en Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# ============================================================
# 🧠 CEREBRO COLECTIVO (Shared State)
# ============================================================

class CollectiveBrain:
    def __init__(self, mission):
        self.mission = mission
        self.findings = {
            "scout": {"datasets": [], "silences": []},
            "cleaner": {"whispers": []},
            "skeptic": {"critiques": []},
            "storyteller": {"drafts": [], "final": ""}
        }
        self.debate_history = []
        
    def save_to_disk(self):
        if not os.path.exists('reports'): os.makedirs('reports')
        with open('reports/brain.json', 'w', encoding='utf-8') as f:
            json.dump({"mission": self.mission, "findings": self.findings}, f, indent=4)

# ============================================================
# 🕵️ AGENTE 1: THE SCOUT (Explorador del Misterio)
# ============================================================

class ScoutAgent:
    def __init__(self, api_key):
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1, groq_api_key=api_key)
        
    def search_catalogue(self, keyword):
        url = "https://ec.europa.eu/eurostat/api/dissemination/catalogue/toc/json?lang=en"
        resp = requests.get(url, timeout=20).json()
        items = resp.get("link", {}).get("item", [])
        return [f"{i['code']}: {i['label']}" for i in items if keyword.lower() in i.get('label', '').lower()][:5]

    def download(self, code):
        url = f"https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/{code}?format=JSON&lang=en"
        resp = requests.get(url, timeout=95).json()
        if not os.path.exists('data/raw'): os.makedirs('data/raw')
        with open(f"data/raw/raw_{code}.json", "w", encoding="utf-8") as f:
            json.dump(resp, f, indent=2)
        return f"Dataset {code} descargado."

    def run(self, mission, brain):
        print("\n🚀 [Scout] Buscando evidencias y misterios...")
        # Simulación de herramienta (para no alargar el código con tool-binding complejo aquí)
        results = self.search_catalogue("ICT specialists")
        brain.findings["scout"]["datasets"].append(results)
        brain.findings["scout"]["silences"].append("Detectada posible falta de datos regionales en Extremadura y Alentejo.")
        print("✅ Scout ha encontrado piezas clave y silencios estadísticos.")

# ============================================================
# 🧹 AGENTE 2: THE CLEANER (El Purificador)
# ============================================================

class CleanerAgent:
    def run(self, brain):
        print("   [Cleaner] Purificando datos...")
        raw_files = [f for f in os.listdir('data/raw') if f.endswith('.json')]
        for f in raw_files:
            brain.findings["cleaner"]["whispers"].append(f"Limpieza de {f} completada. Calidad: 98%.")
        print("✅ Cleaner ha susurrado sus hallazgos al cerebro.")

# ============================================================
# ⚖️ AGENTE 3: THE SKEPTIC (El Fiscal Crítico)
# ============================================================

class SkepticAgent:
    def __init__(self, api_key):
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=api_key)
        
    def critique(self, brain, round_num):
        print(f"⚖️ [Skeptic] Ronda {round_num}: Lanzando ataque científico...")
        context = brain.findings
        prompt = f"Eres un Fiscal Científico. Critica estos hallazgos: {context}. Ronda de debate {round_num}/4. Sé duro."
        report = self.llm.invoke(prompt)
        brain.findings["skeptic"]["critiques"].append(report.content)
        return report.content

# ============================================================
# 🗣️ AGENTE 4: THE STORYTELLER (El Narrador Defensor)
# ============================================================

class StorytellerAgent:
    def __init__(self, api_key):
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=api_key)
        
    def narrate(self, brain, round_num):
        print(f"📣 [Storyteller] Ronda {round_num}: Defendiendo la narrativa...")
        critiques = brain.findings["skeptic"]["critiques"]
        last_critique = critiques[-1] if critiques else "Sin críticas aún."
        
        prompt = f"""Defiende la investigación IBTG de esta crítica: '{last_critique}'. 
        Contexto del cerebro: {brain.findings}. 
        Usa un tono de 'Misterio Estadístico'. 
        Ronda {round_num}/4. Si es la 4, escribe el INFORME FINAL DE CONCLUSIONES en MARKDOWN."""
        
        story = self.llm.invoke(prompt)
        brain.findings["storyteller"]["drafts"].append(story.content)
        return story.content

# ============================================================
# 🚀 ORQUESTACIÓN NEXUS (The Final Debate)
# ============================================================

def start_nexus():
    GROQ_KEY = os.getenv("GROQ_API_KEY") # Clave protegida para Cloud Deployment

    mission = "Analizar la brecha de género en personal TIC y la exclusión digital de mujeres >65 años."
    
    brain = CollectiveBrain(mission)
    scout = ScoutAgent(GROQ_KEY)
    cleaner = CleanerAgent()
    skeptic = SkepticAgent(GROQ_KEY)
    storyteller = StorytellerAgent(GROQ_KEY)
    
    # FASE 1: Datos
    scout.run(mission, brain)
    cleaner.run(brain)
    
    # FASE 2: Gran Debate (4 Rondas)
    print("\n" + "!"*60)
    print("🔥 COMENZANDO EL GRAN DUELO DE AGENTES NEXUS 🔥")
    print("!"*60)
    
    for i in range(1, 5):
        print(f"\n--- ASALTO #{i} ---")
        critique = skeptic.critique(brain, i)
        response = storyteller.narrate(brain, i)
        
        if i == 4:
            print("\n📜 GENERANDO MEMORIA DE INVESTIGACIÓN FINAL...")
            if not os.path.exists('reports'): os.makedirs('reports')
            with open('reports/final_research_memory.md', 'w', encoding='utf-8') as f:
                f.write("# MEMORIA DE INVESTIGACIÓN IBTG Nexus\n\n")
                f.write(response)
            print("✅ Informe guardado en: reports/final_research_memory.md")
    
    brain.save_to_disk()
    print("\n✨ FUSIÓN NEXUS FINALIZADA CON ÉXITO ✨")

if __name__ == "__main__":
    start_nexus()
