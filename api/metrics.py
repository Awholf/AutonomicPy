from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db
from db.models import SystemMetric
from services.webserver_mock import server_state

router = APIRouter()

@router.get("/metrics")
def get_metrics(db: Session = Depends(get_db)):
    """
    Endpoint consultado por el MONITOR (Josue).
    Retorna estado actual y lo guarda en historial.
    """
    data = server_state.get_current_metrics()
    
    # Guardar métrica para análisis histórico
    metric_entry = SystemMetric(
        cpu_usage=data["cpu"],
        ram_usage=data["ram"],
        response_time=data["response_time"],
        active_instances=data["instances"]
    )
    db.add(metric_entry)
    db.commit()
    
    return data

@router.get("/status")
def get_status():
    return {"status": "operational", "config": "autonomic-mode-enabled"}