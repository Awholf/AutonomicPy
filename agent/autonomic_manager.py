class AutonomicManager:
    """
    Recibe indicadores numéricos y devuelve acciones concretas.
    """
    def __init__(self):
        pass

    def analyze(self, indicators):
        """
        ANALYZER: Evalúa si los números son peligrosos.
        """
        cpu = indicators.get("cpu", 0)
        ram = indicators.get("ram", 0)
        response_time = indicators.get("response_time", 0)
        
        status = "OPTIMAL"
        reasons = []

        # Reglas de Análisis
        if cpu > 80:
            status = "CRITICAL"
            reasons.append(f"CPU usage ({cpu}%) exceeds 80%.")
        
        if ram > 85:
            if status != "CRITICAL": status = "CRITICAL"
            reasons.append(f"RAM usage ({ram}%) exceeds 85%.")
        
        if response_time > 300:
            if status == "OPTIMAL": status = "DEGRADED"
            reasons.append(f"Response time ({response_time}ms) is slow.")

        return status, reasons

    def plan(self, status, indicators):
        """
        OPTIMIZER: Decide qué hacer basándose en el análisis.
        - High CPU -> scale_up
        - High RAM -> restart_service
        - Low Load -> scale_down
        """
        actions = []
        cpu = indicators.get("cpu", 0)
        ram = indicators.get("ram", 0)
        response_time = indicators.get("response_time", 0)
        instances = indicators.get("instances", 1)
        
        # --- REGLAS DE DECISIÓN ---
        
        # 1. Si el CPU explota, necesitamos más manos (Escalar)
        if cpu > 80:
            actions.append({
                "action": "scale_up", 
                "reason": "CPU overload detected."
            })
        
        # 2. Si la RAM explota, suele ser fugas de memoria (Reiniciar)
        if ram > 85:
            actions.append({
                "action": "restart_service", 
                "reason": "Critical RAM usage (Memory Leak)."
            })

        # 3. Si está lento pero el CPU está bien, igual escalamos por si acaso
        if response_time > 300 and cpu < 80:
            actions.append({
                "action": "scale_up", 
                "reason": "Response time degradation mitigation."
            })
            
        # 4. Regla de Ahorro: Si no pasa nada y sobran servidores, apagamos uno
        if cpu < 20 and instances > 1:
             actions.append({
                "action": "scale_down", 
                "reason": "Low traffic - Optimizing resources."
            })

        return actions