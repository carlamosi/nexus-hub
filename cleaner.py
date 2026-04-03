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
        print("\\n✨ [CLEANER] Alquimia de datos iniciada...")
        raw_files = [f for f in os.listdir(self.raw_path) if f.endswith('.json')]
        
        from pyjstat import pyjstat
        
        for fname in raw_files:
            try:
                # Utilizar pyjstat para decodificar Eurostat JSON-stat
                with open(os.path.join(self.raw_path, fname), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                dataset = pyjstat.from_json_stat(data)
                if not dataset:
                    raise Exception("Estructura JSON-stat no reconocida por pyjstat")
                
                # from_json_stat retorna una lista de DataFrames
                df = dataset[0]
                
                # Renombramos la columna 'value' a 'Value' para ser compatibles con web_builder
                df = df.rename(columns={'value': 'Value'})
                
                # Eliminamos nulos
                df = df.dropna(subset=['Value'])
                
                # OPERACIONES ELITE: Ranking global
                df['Ranking'] = df['Value'].rank(ascending=False)
                
                # Guardamos CSV enriquecido multidimensional 
                clean_name = fname.replace('raw_', '').replace('.json', '.csv')
                df.to_csv(os.path.join(self.clean_path, clean_name), index=False)
                
                self.save_whisper(f"✅ Dataset {clean_name} decodificado con dimensiones geográficas reales.")
                print(f"📊 [CLEANER] {clean_name}: Normalización multidimensional con éxito.")
                
            except Exception as e:
                self.save_whisper(f"❌ Error crítico en {fname}: {str(e)}")

if __name__ == "__main__":
    agent = DataCleanerAgent()
    agent.process()
