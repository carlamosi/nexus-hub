"""
⚖️ THE SKEPTIC — Agent v3 (Scientific Correlation & Debate Auditor)
Scientific rigor control for the IBTG Pipeline.
Critiques findings and engages in 4 rounds of debate.
"""

import csv
import os
import json
import sys
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv()

# Forzar UTF-8 para evitar errores con emojis en Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
from langchain_groq import ChatGroq

class SkepticAgent:
    def __init__(self, groq_key):
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=groq_key)

    def read_brain(self):
        """Lee el estado actual de la investigación."""
        brain_path = 'reports/brain.json'
        if not os.path.exists(brain_path): return {}
        with open(brain_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def detect_outliers(self):
        """Auditoría matemática: Busca desvíos en los datos limpios."""
        print("📏 [SKEPTIC] Iniciando auditoría matemática (Outliers Z-Score)...")
        clean_path = 'data/clean/'
        anomalies = []
        if not os.path.exists(clean_path): return anomalies
        
        for f in os.listdir(clean_path):
            if f.endswith('.csv'):
                with open(os.path.join(clean_path, f), 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    values = [float(row['Value']) for row in reader if row['Value'] and row['Value'] != 'None']
                    
                if len(values) > 2:
                    avg = sum(values) / len(values)
                    std = (sum((v - avg)**2 for v in values) / len(values))**0.5
                    for v in values:
                        if std > 0 and abs(v - avg) / std > 1.5: # Umbral de sospecha
                            anomalies.append(f"Outlier en {f}: detectado valor de {v}.")
        return anomalies

    def save_audit(self, critique, anomalies):
        """Guarda la auditoría completa en el cerebro."""
        brain_path = 'reports/brain.json'
        try:
            with open(brain_path, 'r', encoding='utf-8') as f:
                brain = json.load(f)
            brain["findings"]["skeptic"]["critiques"].append(critique)
            brain["findings"]["skeptic"]["anomalies"].extend(anomalies)
            with open(brain_path, 'w', encoding='utf-8') as f:
                json.dump(brain, f, indent=4)
        except: pass

    def audit_research(self, brain):
        print("\n" + "="*70)
        print("⚖️ THE SKEPTIC AGENT ESTÁ AUDITANDO LA FRESCOCURA Y CALIDAD...")
        print("="*70)

        anomalies = self.detect_outliers()
        findings = brain.get("findings", {})
        whispers = findings.get("cleaner", {}).get("whispers", [])
        
        # Auditoría de Frescura (si hay advertencias del Cleaner)
        is_stale = any("DATO ANTIGUO" in w for w in whispers)
        if is_stale:
            anomalies.append("CRITICAL: El dataset es anterior a 2021. Requiere búsqueda de actualización.")

        prompt = f"""
        Eres un AUDITOR MATEMÁTICO SENIOR. 
        Analiza los hallazgos: {findings}
        Anomalías físicas detectadas: {anomalies}
        
        TU MISIÓN:
        1. Emite un veredicto sobre la calidad científica de la investigación.
        2. Si hay anomalías de frescura: '{[a for a in anomalies if 'CRITICAL' in a]}', ordena al Scout qué buscar exactamente.
        3. No aceptes datos de baja resolución regional. 
        """

        report = self.llm.invoke(prompt)
        print(report.content)
        self.save_audit(report.content, anomalies)

if __name__ == "__main__":
    GROQ_KEY = os.getenv("GROQ_API_KEY") # Clave protegida para Cloud Deployment

    agent = SkepticAgent(GROQ_KEY)
    brain = agent.read_brain()
    if brain:
        agent.audit_research(brain)
