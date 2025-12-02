import time
import requests
import sys
from autonomic_manager import AutonomicManager

API_URL = "http://127.0.0.1:8000"
POLLING_INTERVAL = 2  # Segundos entre lecturas

def run_agent():
    print("--- AGENTE AUTONÓMICO ---")
    print(f"Backend cnonecting...: {API_URL}")
    
    manager = AutonomicManager()

    while True:
        try:
            # 1. MONITOR: Obtener datos reales
            response = requests.get(f"{API_URL}/metrics")
            
            if response.status_code != 200:
                print(f"❌ Error leyendo métricas: {response.text}")
                time.sleep(POLLING_INTERVAL)
                continue
                
            indicators = response.json()
            
            # Mostrar estado actual (Log bonito)
            status_emoji = "🟢"
            if indicators['cpu'] > 80: status_emoji = "🔥"
            elif indicators['instances'] > 1: status_emoji = "🔵"
            
            print(f"\n{status_emoji} [MONITOR] CPU: {indicators['cpu']}% | RAM: {indicators['ram']}% | Nodos: {indicators['instances']}")

            # 2. ANALYZER: ¿Estamos bien?
            status, reasons = manager.analyze(indicators)
            
            if status != "OPTIMAL":
                print(f"⚠️ [ANALYZER] Detectado estado {status}: {reasons}")

            # 3. OPTIMIZER: ¿Qué hacemos?
            actions_list = manager.plan(status, indicators)

            # 4. EXECUTOR: Enviar órdenes
            if actions_list:
                for plan in actions_list:
                    action_cmd = plan["action"]
                    print(f"🚀 [EXECUTOR] Ejecutando: {action_cmd} ({plan['reason']})")
                    
                    # ENVIAR POST AL BACKEND
                    payload = {
                        "action": action_cmd,
                        "source": "Agent_Automated"
                    }
                    try:
                        res = requests.post(f"{API_URL}/execute_action", json=payload)
                        print(f"   ✅ Backend respondió: {res.json()['message']}")
                    except Exception as e:
                        print(f"   ❌ Fallo al enviar acción: {e}")
                    
                    # Esperar un momento para no spammear acciones
                    time.sleep(3) 
            else:
                # Si no hay acciones, solo pasamos
                pass

        except requests.exceptions.ConnectionError:
            print("❌ No se encuentra el servidor. ¿Ejecutaste 'uvicorn app.main:app'?")
            time.sleep(5)
        except KeyboardInterrupt:
            print("\n🛑 Agente detenido por el usuario.")
            sys.exit()
        except Exception as e:
            print(f"❌ Error inesperado: {e}")

        time.sleep(POLLING_INTERVAL)

if __name__ == "__main__":
    run_agent()