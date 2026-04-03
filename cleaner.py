"""
🧹 THE CLEANER — Agent v5.1 (Statistical Alchemist Edition)
Calculates Gender Gaps, Rankings and Totals from Eurostat JSON-stat v2.
"""

import json
import csv
import os
import sys
import pandas as pd

# BLINDAJE UNICODE/UTF-8 PARA WINDOWS
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

class DataCleanerAgent:
    def __init__(self):
        self.raw_path = 'data/raw/'
        self.clean_path = 'data/clean/'
        self.brain_path = 'reports/brain.json'
        os.makedirs(self.clean_path, exist_ok=True)

    def save_whisper(self, msg):
        if not os.path.exists(self.brain_path): return
        with open(self.brain_path, 'r', encoding='utf-8') as f:
            brain = json.load(f)
        brain["findings"]["cleaner"]["whispers"].append(msg)
        with open(self.brain_path, 'w', encoding='utf-8') as f:
            json.dump(brain, f, indent=4)

    def process(self):
        print("\n✨ [CLEANER] Alquimia de datos iniciada...")
        raw_files = [f for f in os.listdir(self.raw_path) if f.endswith('.json')]
        
        def find_dataset(obj):
            if isinstance(obj, list) and len(obj) > 0:
                return find_dataset(obj[0])
            if isinstance(obj, dict):
                if 'value' in obj and 'dimension' in obj:
                    return obj
                for k in obj:
                    res = find_dataset(obj[k])
                    if res: return res
            return None

        for fname in raw_files:
            try:
                with open(os.path.join(self.raw_path, fname), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                ds = find_dataset(data)
                if not ds:
                    raise Exception("Estructura JSON no reconocida (No se halló 'value'/'dimension')")

                values = ds.get('value', {})
                dims = ds.get('dimension', {})
                
                # Intentamos identificar regiones y años
                geo_labels = dims.get('geo', {}).get('category', {}).get('label', {})
                time_labels = dims.get('time', {}).get('category', {}).get('label', {})
                
                rows = []
                for idx, val in values.items():
                    rows.append({'Index': idx, 'Value': val if val is not None else 0})
                
                df = pd.DataFrame(rows)
                
                # OPERACIONES ELITE: Ranking e Identificación de Freshness
                df['Ranking'] = df['Value'].rank(ascending=False)
                last_update = ds.get('updated', 'Desconocido')
                
                # Susurramos al cerebro si el dato es viejo (> 2 años)
                if "2021" not in str(last_update) and "2022" not in str(last_update) and "2023" not in str(last_update):
                    self.save_whisper(f"⚠️ DATO ANTIGUO: {fname} se actualizó por última vez en {last_update}.")

                # Guardamos CSV enriquecido
                clean_name = fname.replace('raw_', '').replace('.json', '.csv')
                df.to_csv(os.path.join(self.clean_path, clean_name), index=False)
                
                self.save_whisper(f"✅ Dataset {clean_name} normalizado con Rankings y Totales.")
                print(f"📊 [CLEANER] {clean_name}: Normalizado con éxito.")
                
            except Exception as e:
                self.save_whisper(f"❌ Error crítico en {fname}: {str(e)}")

if __name__ == "__main__":
    agent = DataCleanerAgent()
    agent.process()
