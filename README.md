## Instalación

1. **Abrir el proyecto en un IDE**
   ```bash
   # Para VsCode en la terminal del directorio
   .code 
2. **Crear un Entorno Virtual**
   ```bash
   python -m venv env
   source env/bin/activate  # En Windows usa `env\Scripts\activate`
3. **Instala Dependencias**
   ```bash
   pip install -r requirements.txt
4. **Corre la aplicacion**
    ```bash
   python main.py
    
## Guía de Pruebas

Para probar la lógica autonómica sin necesidad de configurar el agente externo, puedes utilizar la interfaz visual integrada **Swagger UI**.

**Acceder al Dashboard:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Sigue este flujo paso a paso para validar el ciclo **MAPE-K**:

### Paso 1: Ver Estado Inicial (Monitor)
* **Endpoint:** `GET /metrics`
* **Acción:** Clic en *Try it out* → *Execute*.
* **Resultado Esperado:** Verás que el servidor opera en estado basal.
    * `instances`: **1**
    * `cpu`: **~30%** (Carga baja)

### Paso 2: Simular un "Desastre" (Load Injection)
* **Endpoint:** `POST /simulate_load`
* **Parámetro:** Establece `intensity` en **50**.
* **Acción:** *Execute*.
* **Efecto:** Al volver a consultar `/metrics`, notarás el cambio drástico:
    * `cpu`: **>80%** (Saturado)
    * `status`: **"CRITICAL"**

### Paso 3: Ejecutar Acción Autonómica (Executor)
Simulamos la decisión que tomaría el optimizador enviando una orden manual.

* **Endpoint:** `POST /execute_action`
* **Body:** Copia y pega el siguiente JSON en la solicitud:
    ```json
    {
      "action": "scale_up",
      "source": "Manual Test"
    }
    ```
* **Efecto:** El sistema aprovisiona un nuevo nodo/instancia para manejar la carga.

### Paso 4: Validar Recuperación (Self-Healing)
* **Endpoint:** `GET /metrics`
* **Resultado Final:** Aunque la carga de tráfico sigue siendo alta, la carga se ha distribuido entre los nodos.
    * `instances`: **2**
    * `cpu`: **~40-45%** (El uso de CPU por nodo bajó a la mitad)
    * **Conclusión:** El sistema ha recuperado la estabilidad del servicio automáticamente.
