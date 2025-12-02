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
4. **Corre el servidor backend**
    ```bash
   uvicorn main:app --reload
5. **Inicia el Agente Autonómico**
    ```bash
   cd agent
    python run_agent.py
