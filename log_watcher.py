import time
import sys
from log_ingestion import procesar_cola

INTERVALO_SEGUNDOS = 5

def iniciar_observador():
    print("===================================================")
    print("       CAWI - LOG WATCHER ACTIVO (ThinkPad)        ")
    print("===================================================")
    print(f"Monitoreando carpeta 'logs_inbox' cada {INTERVALO_SEGUNDOS}s...")
    print("Presiona Ctrl + C en cualquier momento para detener.")
    print("---------------------------------------------------")
    
    try:
        while True:
            procesados = procesar_cola()
            if procesados > 0:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Lote completado. Esperando nuevos logs...")
            time.sleep(INTERVALO_SEGUNDOS)
    except KeyboardInterrupt:
        print("\n[STOP] Observador detenido por el usuario.")
        sys.exit(0)

if __name__ == "__main__":
    iniciar_observador()
