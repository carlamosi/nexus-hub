import sys
import io
import os
import subprocess
import json

# BLINDAJE UNICODE TOTAL
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

os.environ["PYTHONIOENCODING"] = "utf-8"

def setup_folders():
    for f in ['data/raw', 'data/clean', 'agents', 'reports']:
        os.makedirs(f, exist_ok=True)

def init_brain(mission):
    brain_path = 'reports/brain.json'
    brain_data = {
        "mission": mission,
        "findings": {
            "scout": {"datasets": [], "silences": [], "refinements": []},
            "cleaner": {"whispers": []},
            "skeptic": {"critiques": [], "anomalies": []},
            "storyteller": {"drafts": [], "final": ""}
        }
    }
    with open(brain_path, 'w', encoding='utf-8') as f:
        json.dump(brain_data, f, indent=4)

def run_agent(name, script, py_cmd, args=[]):
    # Sin caracteres especiales en el print inicial
    print(f"--- AGENTE: {name} ---")
    cmd = [py_cmd, script] + args
    
    # Capturamos salida con codificación robusta
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    
    if result.returncode != 0:
        print(f"FAILED: {name}")
        return False
    print(f"DONE: {name}")
    return True

def main():
    setup_folders()
    # MOTOR DE PYTHON DE CARLA
    PY_CMD = r"c:\Users\carla\Desktop\Stuff!\Estadística\scout_env\Scripts\python.exe"
    mission = "Gender Gap in ICT specialists (NUTS2) vs Internet usage women >65."
    
    init_brain(mission)
    
    # SECUENCIA END-TO-END
    if not run_agent("SCOUT", "scout.py", PY_CMD, [mission]): return
    if not run_agent("CLEANER", "cleaner.py", PY_CMD): return
    
    # 2 RONDAS DE REFINAMIENTO (Feedback Loop)
    for i in range(1, 3):
        print(f"ROUND {i}")
        if not run_agent("SKEPTIC", "skeptic.py", PY_CMD): break
        if not run_agent("SCOUT_REFINE", "scout.py", PY_CMD, ["REFINE_MODE"]): break
        if not run_agent("CLEANER_REPROCESS", "cleaner.py", PY_CMD): break
        if not run_agent("STORYTELLER", "storyteller.py", PY_CMD): break

    print("RESEARCH COMPLETE.")

if __name__ == "__main__":
    main()
