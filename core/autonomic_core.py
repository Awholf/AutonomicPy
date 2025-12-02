from services.webserver_mock import server_state
from sqlalchemy.orm import Session
from db.models import ActionLog

class AutonomicManager:
    
    @staticmethod
    def execute_action(action: str, db: Session, source: str = "Optimizer"):
        description = ""
        
        if action == "scale_up":
            # Acción: Agregar un nodo
            server_state.instances += 1
            description = f"Instancias aumentadas a {server_state.instances}. Carga distribuida."
            
        elif action == "scale_down":
            # Acción: Quitar un nodo (si hay más de 1)
            if server_state.instances > 1:
                server_state.instances -= 1
                description = f"Instancias reducidas a {server_state.instances}. Ahorro de recursos."
            else:
                description = "Intento de scale_down fallido: Mínimo 1 instancia requerida."

        elif action == "restart_service":
            # Acción: Reiniciar (baja la RAM acumulada pero mantiene instancias)
            server_state.ram_load = 30.0 # Vuelve a base
            server_state.cpu_load = max(30.0, server_state.cpu_load - 10) # Alivio temporal
            description = "Servicio reiniciado. Memoria liberada."
            
        elif action == "optimize_db":
            # Ejemplo de otra acción
            server_state.cpu_load -= 5
            description = "Consultas DB optimizadas. CPU liberado levemente."

        else:
            return {"status": "error", "message": "Acción desconocida"}

        # Registrar en Base de Datos
        new_log = ActionLog(action_type=action, description=description, triggered_by=source)
        db.add(new_log)
        db.commit()
        
        return {"status": "success", "action": action, "result": description}