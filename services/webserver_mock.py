import random

class WebServerState:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(WebServerState, cls).__new__(cls)
            # Estado Inicial
            cls._instance.cpu_load = 30.0  # % Base
            cls._instance.ram_load = 40.0  # % Base
            cls._instance.instances = 1    # Servidores activos
            cls._instance.requests_per_sec = 10
        return cls._instance

    def get_current_metrics(self):
        """Genera métricas con ligera variación aleatoria para realismo"""
        noise = random.uniform(-2, 2)
        
        # Lógica de simulación: Más instancias = Menos carga por nodo
        effective_cpu = (self.cpu_load / self.instances) + noise
        effective_ram = (self.ram_load / self.instances) + noise
        
        # Calcular tiempo de respuesta basado en carga
        # Si CPU está saturada (>80%), el tiempo de respuesta se dispara exponencialmente
        base_response = 50 # ms
        latency_factor = 1.0
        if effective_cpu > 80:
            latency_factor = 5.0 # Degradación severa
        elif effective_cpu > 60:
            latency_factor = 2.0
            
        response_time = base_response * latency_factor + random.uniform(0, 20)

        return {
            "cpu": max(0, min(100, effective_cpu)), # Clamp 0-100
            "ram": max(0, min(100, effective_ram)),
            "response_time": round(response_time, 2),
            "instances": self.instances,
            "traffic": self.requests_per_sec
        }

    def simulate_traffic_spike(self, intensity: int):
        """Aumenta la carga base simulando usuarios entrando"""
        self.cpu_load += intensity * 2
        self.ram_load += intensity * 1.5
        self.requests_per_sec += intensity

    def reset_state(self):
        self.cpu_load = 30.0
        self.ram_load = 40.0
        self.instances = 1
        self.requests_per_sec = 10

# Instancia global (Singleton)
server_state = WebServerState()