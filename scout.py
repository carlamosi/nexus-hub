import os
import json
import requests
import sys
from dotenv import load_dotenv

# Cargar variables de entorno del archivo .env
load_dotenv()

# BLINDAJE UNICODE TOTAL - DEBE SER LA LÍNEA 1
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

class ScoutAgent:
    def __init__(self, api_key):
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, groq_api_key=api_key)
        self.brain_path = 'reports/brain.json'

    def read_brain(self):
        if not os.path.exists(self.brain_path): return {}
        with open(self.brain_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def search_eurostat(self, query):
        """Busca datasets en el catálogo de Eurostat."""
        url = f"https://ec.europa.eu/eurostat/api/dissemination/catalogue/toc/json?lang=en"
        try:
            resp = requests.get(url, timeout=20).json()
            items = resp.get("link", {}).get("item", [])
            matches = [i for i in items if query.lower() in i.get('label', '').lower()][:3]
            return matches
        except: return []

    def download_dataset(self, code):
        """Descarga el JSON-stat v2 directamente de Eurostat."""
        url = f"https://ec.europa.eu/eurostat/api/dissemination/statistics/v1.0/data/{code}?lang=en&format=JSON"
        print(f"📡 [SCOUT] Descargando dataset crítico: {code}...")
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                if not os.path.exists('data/raw'): os.makedirs('data/raw')
                fpath = f"data/raw/raw_{code}.json"
                with open(fpath, 'w', encoding='utf-8') as f:
                    json.dump(resp.json(), f, indent=4)
                print(f"✅ [SCOUT] Archivo guardado: {fpath}")
                return True
        except Exception as e:
            print(f"❌ [SCOUT] Error en descarga: {e}")
        return False

    def run(self, mode="NORMAL"):
        brain = self.read_brain()
        print(f"[SCOUT] MODE: {mode}")
        
        if mode == "REFINE_MODE":
            # REACCIÓN A LA CRÍTICA: Scout inteligente
            critiques = brain.get("findings", {}).get("skeptic", {}).get("critiques", [])
            last_critique = critiques[-1] if critiques else "No hay críticas aún."
            print(f"[SCOUT] Analyzing scientific critique for refinement...")
            
            # IA Refinadora: Traduce queja a Keyword técnica de Eurostat
            prompt = f"""
            El Auditor ha lanzado esta crítica: '{last_critique[:200]}'.
            Tu misión es buscar un dataset que llene ese vacío. 
            Responde SOLO con una palabra o código técnico de Eurostat (ej: 'ICT', 'ISOC', 'BDE', 'Digital').
            """
            keyword = self.llm.invoke(prompt).content.strip().replace("'", "").replace('"', '')
            print(f"[SCOUT] Keyword: {keyword}")
            
            # Nueva búsqueda técnica
            refinements = self.search_eurostat(keyword)
            brain["findings"]["scout"]["refinements"].append(f"Feedback focus: {keyword} -> Result: {refinements}")
        else:
            # Búsqueda inicial normal: Usamos términos más amplios (ICT o ISOC)
            print("[SCOUT] Mapping initial terrain (Eurostat)...")
            initial_finds = self.search_eurostat("ICT") # Término más genérico para asegurar éxito
            
            # ACCIÓN CRÍTICA: Descargamos el más relevante 
            if not initial_finds:
                print("⚠️ [SCOUT] Búsqueda fallida. Intentando descarga directa de dataset maestro 'isoc_sks_itp'...")
                self.download_dataset("isoc_sks_itp") # Fallback a dataset conocido
            else:
                target_code = initial_finds[0]['code']
                self.download_dataset(target_code)
                
            brain.setdefault("findings", {}).setdefault("scout", {"datasets": [], "silences": [], "refinements": []})
            brain["findings"]["scout"]["datasets"].append([f"{i['code']}: {i['label']}" for i in initial_finds])
            brain["findings"]["scout"]["silences"].append("Note: Missing regional breakdown in some Baltic countries.")

        # Asegurar carpetas y guardar en el cerebro
        if not os.path.exists('reports'): os.makedirs('reports')
        with open(self.brain_path, 'w', encoding='utf-8') as f:
            json.dump(brain, f, indent=4)

if __name__ == "__main__":
    GROQ_KEY = os.getenv("GROQ_API_KEY") # Clave protegida para Cloud Deployment

    agent = ScoutAgent(GROQ_KEY)
    mode = sys.argv[1] if len(sys.argv) > 1 else "NORMAL"
    agent.run(mode)
