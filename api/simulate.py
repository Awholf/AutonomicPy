from fastapi import APIRouter
from services.webserver_mock import server_state

router = APIRouter()

@router.post("/simulate_load")
def simulate_load(intensity: int = 10):
    """
    Simula un pico de tráfico (ej. Black Friday).
    Esto degradará el rendimiento y forzará al sistema autonómico a reaccionar.
    """
    server_state.simulate_traffic_spike(intensity)
    return {"message": f"Carga aumentada. Intensidad: {intensity}"}

@router.post("/reset_simulation")
def reset_sim():
    server_state.reset_state()
    return {"message": "Simulación reiniciada a valores base."}