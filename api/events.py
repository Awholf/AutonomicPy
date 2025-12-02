from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from db.connection import get_db
from core.autonomic_core import AutonomicManager

router = APIRouter()

@router.post("/execute_action")
def trigger_action(
    action: str = Body(..., embed=True), 
    source: str = Body("Manual", embed=True),
    db: Session = Depends(get_db)
):
    """
    Endpoint usado por el OPTIMIZER (Josue) para ejecutar cambios.
    """
    return AutonomicManager.execute_action(action, db, source)