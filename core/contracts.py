import pandas as pd
import hashlib
from datetime import datetime

class DataValidator:
    """
    Motor Estricto de Contratos de Datos Multi-Agente (Scientific-Grade).
    Garantiza reproducibilidad, versionado criptográfico y prevención de errores silenciosos.
    """
    
    @staticmethod
    def generate_metadata(df, dataset_id):
        """Genera metadata inmutable para un dataset."""
        if df.empty:
            return None
        # Hash basado en el contenido persistente
        hash_obj = hashlib.md5(pd.util.hash_pandas_object(df, index=True).values)
        digest = hash_obj.hexdigest()
        return {
            "dataset_id": dataset_id,
            "version": digest[:8],
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "rows": len(df),
            "signature": digest
        }

    @staticmethod
    def validate_dataset(df, value_col, geo_col):
        """
        Hard-Stop Validation Rule Engine.
        Solo devuelve True si el dataframe es matemáticamente y semánticamente puro.
        """
        errors = []
        
        # 1. Null Critical Fields
        if df[value_col].isnull().any():
            count = df[value_col].isnull().sum()
            errors.append(f"NULL_POLLUTION: Detección de {count} nulos en la columna crítica '{value_col}'.")
            
        # 2. Type validation
        if not pd.api.types.is_numeric_dtype(df[value_col]):
            errors.append(f"TYPE_VIOLATION: La columna '{value_col}' presenta tipos de datos impuros (no estrictamente numéricos).")
            
        # 3. Geo-Spatial Hardening
        if df[geo_col].isnull().any() or (df[geo_col].astype(str).str.strip() == '').any():
            count = df[geo_col].isnull().sum()
            errors.append(f"GEO_SPATIAL_BREAKDOWN: {count} registros carecen de anclaje georreferencial válido en '{geo_col}'.")
            
        # 4. Outlier Detection (Z-score > 3 sigma)
        if pd.api.types.is_numeric_dtype(df[value_col]):
            mean = df[value_col].mean()
            std = df[value_col].std()
            if std > 0:
                z_scores = (df[value_col] - mean) / std
                outliers = (z_scores > 3) | (z_scores < -3)
                if outliers.any():
                    errors.append(f"OUTLIER_ANOMALY: Se detectaron {outliers.sum()} registros fuera del rango (||Z|| > 3). Posible alteración en la captura de API.")

        # 5. Semantic Validation (Cannot have negative demographic counts typically, but indices could. 
        # For Strict Gender Gap, negative counts usually mean missing data flags (-99).)
        if pd.api.types.is_numeric_dtype(df[value_col]):
            if (df[value_col] < 0).any():
                count = (df[value_col] < 0).sum()
                errors.append(f"SEMANTIC_DOMAIN_ERROR: {count} valores son negativos matemáticamente sospechosos en '{value_col}'.")
                
        # 6. Duplication Check (Geo + Time compound key representation check)
        # Warning: Requires time context. We assume external time filter ensures unique geo values.
        if df.duplicated(subset=[geo_col]).any():
            dups = df.duplicated(subset=[geo_col]).sum()
            errors.append(f"DIMENSION_COLLISION: {dups} geometrías duplicadas en el set de datos. Se requiere colapso temporal explícito.")
                
        is_valid = len(errors) == 0
        return is_valid, errors
