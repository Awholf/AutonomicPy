from fastapi import FastAPI
from db.connection import engine, Base
from api import metrics, events, simulate

# Crear tablas en BD al inicio
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Autonomic Web Server Core",
    description="Sistema Backend con capacidades de auto-optimización simulada",
    version="1.0.0"
)

# Incluir rutas
app.include_router(metrics.router, tags=["Monitoring"])
app.include_router(events.router, tags=["Autonomic Actions"])
app.include_router(simulate.router, tags=["Simulation"])

@app.get("/")
def root():
    return {"message": "Autonomic Server Online. Go to /docs for interface."}