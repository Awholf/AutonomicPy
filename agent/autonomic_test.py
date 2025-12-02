import json
from autonomic_manager import AutonomicManager

def run_test_cycle(case_name, indicators):
    print(f"\n--- {case_name} ---")
    print(f"1. INPUT: {json.dumps(indicators, indent=2)}")
    
    manager = AutonomicManager()
    
    # Analyzer
    status, reasons = manager.analyze(indicators)
    print(f"2. ANALYZER: Status={status}")
    
    # Optimizer
    actions = manager.plan(status, indicators)
    print(f"3. OPTIMIZER ACTIONS: {json.dumps(actions, indent=2)}")
    return actions

# --- CASOS DE PRUEBA ---

# Caso 1: Todo normal
run_test_cycle("TEST 1: Normal Operation", {
    "cpu": 30, "ram": 40, "response_time": 50, "instances": 1
})

# Caso 2: Pánico de CPU (Debería escalar)
run_test_cycle("TEST 2: High CPU (Black Friday)", {
    "cpu": 95, "ram": 60, "response_time": 400, "instances": 1
})

# Caso 3: El caso mixto de Josue (RAM Alta + Lento)
# Debería sugerir Reiniciar (por RAM) y Escalar (por Lento)
run_test_cycle("TEST 3: Critical RAM + Slow", {
    "cpu": 55.0,
    "ram": 90.0,
    "response_time": 450.0,
    "instances": 2
})