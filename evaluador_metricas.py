import os
import json
import pandas as pd
from datetime import datetime
from google import genai
from google.genai import types

METRICAS_SCHEMA = {
    "type": "object",
    "properties": {
        "total_nodos": {"type": "integer"},
        "nodos_exitosos": {"type": "integer"},
        "nodos_fallidos": {"type": "integer"},
        "tokens_totales_consumidos": {"type": "integer"},
        "latencia_promedio_exitosos_ms": {"type": "number"},
        "pico_memoria_mb": {"type": "integer"},
        "errores_detectados": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": [
        "total_nodos",
        "nodos_exitosos",
        "nodos_fallidos",
        "tokens_totales_consumidos",
        "latencia_promedio_exitosos_ms",
        "pico_memoria_mb",
        "errores_detectados"
    ]
}

def procesar_y_guardar_metricas(log_crudo: str, csv_path: str = "metricas_cawi.csv") -> dict:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Variable GEMINI_API_KEY no encontrada en el entorno.")

    client = genai.Client(api_key=api_key)

    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=METRICAS_SCHEMA,
    )

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=log_crudo,
        config=config,
    )

    datos = json.loads(response.text)

    fila = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_nodos": datos["total_nodos"],
        "nodos_exitosos": datos["nodos_exitosos"],
        "nodos_fallidos": datos["nodos_fallidos"],
        "tokens_totales": datos["tokens_totales_consumidos"],
        "latencia_promedio_ms": datos["latencia_promedio_exitosos_ms"],
        "pico_memoria_mb": datos["pico_memoria_mb"],
        "errores": "; ".join(datos["errores_detectados"]) if datos["errores_detectados"] else "NINGUNO"
    }

    df_nuevo = pd.DataFrame([fila])

    if not os.path.exists(csv_path):
        df_nuevo.to_csv(csv_path, index=False, encoding="utf-8")
    else:
        df_nuevo.to_csv(csv_path, mode="a", header=False, index=False, encoding="utf-8")

    print(f"[OK] Metricas registradas en {csv_path}")
    return datos

if __name__ == "__main__":
    log_prueba = "Nodo A: status 200, 28ms, 512MB, in 80, out 120. Nodo B: status 500, error 'CUDA OOM', 1100ms, 1024MB, in 40, out 0."
    resultado = procesar_y_guardar_metricas(log_prueba)
    print(json.dumps(resultado, indent=2))
