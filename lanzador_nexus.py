import subprocess
import sys
import os

# CONFIGURACIÓN MAESTRA
PROJ_DIR = r"c:\Users\carla\Desktop\Stuff!\Estadística"
PY_EXE = os.path.join(PROJ_DIR, "scout_env", "Scripts", "python.exe")
MISSION = "Gender Gap in ICT specialists (NUTS2) vs Internet usage women >65."

def run_agent(name, script, args=[]):
    print(f"\n>>> [NEXUS] INICIANDO AGENTE: {name} <<<")
    full_script = os.path.join(PROJ_DIR, script)
    cmd = [PY_EXE, full_script] + args
    
    # Entorno forzado a UTF-8
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    
    try:
        # Ejecutamos con el CWD correcto para que las rutas relativas funcionen
        proc = subprocess.run(cmd, cwd=PROJ_DIR, env=env, capture_output=True, text=True, encoding='utf-8', errors='replace')
        if proc.returncode != 0:
            print(f"❌ Error en {name}: {proc.stderr}")
            return False
        print(f"✅ {name} completado exitosamente.")
        # Opcional: imprimir un poco de la salida para ver progreso
        if proc.stdout:
            lines = proc.stdout.strip().split('\n')
            for line in lines[-3:]: # Solo las últimas 3 líneas
                print(f"  | {line}")
        return True
    except Exception as e:
        print(f"💣 Crash sistémico en {name}: {e}")
        return False

def main():
    print("************************************************************")
    print("🚀 LANZADOR MAESTRO NEXUS v6.3 — SISTEMA AGÉNTICO ADAPTATIVO")
    print("************************************************************")
    
    # PASO 1: EXTRACCIÓN REAL (Scout Captura)
    if not run_agent("SCOUT (The Hunter)", "scout.py"): return
    
    # PASO 2: LIMPIEZA Y MÉTRICAS (Cleaner Alchemist)
    if not run_agent("CLEANER (The Alchemist)", "cleaner.py"): return
    
    # PASO 3: DEBATE Y REFINAMIENTO (Loop de 2 Rondas)
    for i in range(1, 3):
        print(f"\n--- RONDA DE AUDITORÍA #{i} ---")
        if not run_agent("SKEPTIC (The Auditor)", "skeptic.py"): break
        if not run_agent("SCOUT (Refine Mode)", "scout.py", ["REFINE_MODE"]): break
        if not run_agent("CLEANER (Reprocess)", "cleaner.py"): break
        if not run_agent("STORYTELLER (The Narrator)", "storyteller.py"): break

    print("\n************************************************************")
    print("✨ INVESTIGACIÓN FINALIZADA CON ÉXITO ✨")
    print("Consulta 'reports/final_conclusions.txt' y abre el Dashboard.")
    print("************************************************************")

if __name__ == "__main__":
    main()
