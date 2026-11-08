import os
import shutil
from datetime import datetime
from evaluador_metricas import procesar_y_guardar_metricas

INBOX_DIR = "logs_inbox"
PROCESSED_DIR = "logs_procesados"

os.makedirs(INBOX_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

def procesar_cola():
    archivos = [f for f in os.listdir(INBOX_DIR) if f.endswith(('.log', '.txt'))]
    if not archivos:
        print("[INFO] No hay logs pendientes en logs_inbox.")
        return 0

    print(f"[INFO] Se encontraron {len(archivos)} archivo(s) para procesar.")
    for archivo in archivos:
        ruta_origen = os.path.join(INBOX_DIR, archivo)
        with open(ruta_origen, "r", encoding="utf-8") as f:
            contenido = f.read()

        print(f"[PROCESANDO] {archivo}...")
        procesar_y_guardar_metricas(contenido)

        # Mover a procesados con timestamp para auditoría
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_destino = f"{ts}_{archivo}"
        ruta_destino = os.path.join(PROCESSED_DIR, nombre_destino)
        shutil.move(ruta_origen, ruta_destino)
        print(f"[MOVIDO] {archivo} -> {ruta_destino}")

    return len(archivos)

if __name__ == "__main__":
    procesar_cola()
