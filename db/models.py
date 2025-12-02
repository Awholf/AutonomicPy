from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from .connection import Base

class SystemMetric(Base):
    __tablename__ = "metrics"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.now)
    cpu_usage = Column(Float)  # %
    ram_usage = Column(Float)  # %
    response_time = Column(Float) # ms
    active_instances = Column(Integer) # Para ver el autoescalado

class ActionLog(Base):
    __tablename__ = "actions"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.now)
    action_type = Column(String) # scale_up, scale_down, restart
    description = Column(String)
    triggered_by = Column(String) # "Manual", "Optimizer", "Simulation"