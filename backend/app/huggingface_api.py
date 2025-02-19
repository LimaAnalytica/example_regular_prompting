import os
import requests
import time
from pathlib import Path
from typing import Dict, Optional
from dotenv import load_dotenv

# Cargar variables de entorno
# load_dotenv()

class HuggingFaceAPI:
    def __init__(self):
        """
        Inicializa el cliente de Hugging Face usando el token del .env
        """
        
        env_paths = [
            Path('.env'),  # Actual directory
            Path('../.env'),  # Parent directory
            Path('app/.env'),  # app subdirectory
            Path('/app/.env'),  # Docker WORKDIR
        ]

        for env_path in env_paths:
            if env_path.exists():
                print(f"Archivo .env encontrado en: {env_path.absolute()}")
                print(str(env_path))
                load_dotenv(env_path, override=True)
                break
            else:
                print("No se encontró archivo .env en ninguna ubicación")

        self.api_url = "https://api-inference.huggingface.co/models/"
        try:
            self.token = str(os.environ.get("HUGGINGFACE_TOKEN"))
            print("token visual:",self.token)
            print(len(str(os.getenv("HUGGINGFACE_TOKEN"))))
            print(len(self.token))
        except Exception as e:
            print(f"Error al obtener token: {e}")
            self.token = ''

        print(f"Ruta actual: {os.getcwd()}")
        print(f"Contenido del directorio: {os.listdir('.')}")
        # load_dotenv(env_path, override=True)
        print(f"Variables de entorno disponibles: {[k for k in os.environ.keys() if 'HUGGING' in k]}")
        print(f"Token encontrado: {'Sí' if self.token else 'No'}")
        if self.token:
            print(f"Longitud del token: {len(self.token)}")

        if not self.token:
            print("Warning: HUGGINGFACE_TOKEN no encontrado en variables de entorno")
        
        self.headers = {"Authorization": f"Bearer {self.token}",
                        "Content-Type": "application/json",
                        "X-Use-Cache": "true"} if self.token else {}
        
        self.models = {
            "general": "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
            "spanish": "bertin-project/bertin-roberta-base-spanish",
            "code": "Salesforce/codegen-350M-mono"
        }

    def regular_prompt(self, prompt: str, model_type: str = "general", max_retries=5, retry_delay=80):
        """
        Envía un prompt al modelo con reintentos si el modelo está cargando.
        
        Args:
            prompt: El texto del prompt
            model_type: Tipo de modelo a usar ('general', 'spanish', 'code')
            max_retries: Número máximo de reintentos
            retry_delay: Segundos a esperar entre reintentos
        """
        try:
            # Validación explícita del modelo
            if model_type not in self.models:
                return {
                    "status": "error",
                    "message": f"Modelo '{model_type}' no válido",
                    "details": f"Modelos disponibles: {list(self.models.keys())}"
                }
                
            # Obtener el modelo (ahora sin valor por defecto)
            model = self.models[model_type]
            print(f"Usando modelo: {model} ({model_type})")
            
            # Configuración específica por tipo de modelo
            if model_type == "general":
                payload = {
                    "inputs": prompt,
                    "parameters": {
                        "max_length": 100,
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "do_sample": True,
                        "return_full_text": False
                    }
                }
            elif model_type == "spanish":
                payload = {
                            "inputs": prompt
                            # "parameters": {
                            #     "max_length": 100,  # Mantenemos parámetros básicos
                            #     "temperature": 0.7,
                            #     "top_p": 0.9,
                            #     "do_sample": True
                            # }
                        }
            elif model_type == "code":
                payload = {
                    "inputs": prompt,
                    "parameters": {
                        "max_length": 150,
                        "temperature": 0.2,
                        "top_p": 0.95,
                        "do_sample": True,
                        "num_return_sequences": 1
                    }
                }
            
            # Intentar la petición varias veces
            for attempt in range(max_retries):
                print(f"Intento {attempt + 1} de {max_retries}")
                
                response = requests.post(
                    f"{self.api_url}{model}",
                    headers=self.headers,
                    json=payload
                )
                
                print(f"Response status: {response.status_code}")
                
                if response.status_code == 200:
                    if model_type == "spanish":
                        try:
                            results = response.json()
                            # Como la respuesta es una lista de diccionarios directamente
                            if isinstance(results, list) and len(results) > 0:
                                best_result = max(results, key=lambda x: x['score'])
                                print(best_result)
                                return {"status": "success", "response": best_result['sequence']}
                            else:
                                return {"status": "error", "message": "Respuesta vacía o inválida"}
                        except Exception as e:
                            return {"status": "error", "message": f"Error procesando respuesta: {str(e)}"}
                    return {"status": "success", "response": response.json()[0]["generated_text"]}
                
                # Si el modelo está cargando, esperar y reintentar
                if response.status_code == 503 and "loading" in response.text.lower():
                    error_data = response.json()
                    estimated_time = error_data.get('estimated_time', retry_delay)
                    wait_time = min(float(estimated_time), retry_delay)  # Convertir a float y no esperar más que retry_delay
                    
                    print(f"Modelo {model} cargando, esperando {wait_time} segundos...")
                    time.sleep(wait_time)
                    continue
                
                # Si es otro tipo de error, devolverlo inmediatamente
                return {
                    "status": "error",
                    "message": f"Error en la API: {response.status_code}",
                    "details": response.json()
                }
            
            # Si llegamos aquí, se agotaron los reintentos
            return {
                "status": "error",
                "message": "Tiempo de espera agotado",
                "details": f"El modelo {model} no terminó de cargar después de {max_retries} intentos"
            }

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_available_models(self):
        """
        Retorna la lista de modelos disponibles y sus descripciones
        """
        return {
            "general": "Modelo general en inglés (deepseek-ai/DeepSeek-R1-Distill-Qwen-32B)",
            "spanish": "Modelo optimizado para español (bertin-project/bertin-roberta-base-spanish)",
            "code": "Modelo para generación de código (Salesforce/codegen-350M-mono)"
        }