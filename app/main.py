from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
import io
import os
from PIL import Image


from fastapi.staticfiles import StaticFiles

# Configuración para servir archivos estáticos (imágenes, por ejemplo)


# Cargar el modelo entrenado (una sola vez cuando inicia la aplicación)
model_path = os.path.join(os.path.dirname(__file__), "model", "dog_vs_cat_model_v2.h5")
model = tf.keras.models.load_model(model_path)
print(f"Modelo cargado desde: {model_path}")

# Configuración de la app y plantillas
app = FastAPI()
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))
@app.get("/test/")
def test():
    return {"message": "Test route is working"}




# Función para preprocesar la imagen antes de la predicción
def preprocess_image(image: Image.Image, img_size=256):
    image = image.resize((img_size, img_size))  # Redimensionar al tamaño esperado por el modelo
    image = img_to_array(image) / 255.0  # Normalizar la imagen entre 0 y 1
    image = np.expand_dims(image, axis=0)  # Añadir la dimensión del batch
    return image



@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """
    Renderiza la página de inicio con un formulario HTML para cargar imágenes.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict-image/")
async def predict_image(request: Request, file: UploadFile = File(...)):
    """
    Recibe una imagen, realiza una predicción y devuelve el resultado.
    """
    try:
        # Leer la imagen subida
        image = Image.open(io.BytesIO(await file.read()))
        
        filename = f"{file.filename}"
        output_path = os.path.join(static_dir, filename)
        image.save(output_path)
        
        # Preprocesar la imagen
        preprocessed_image = preprocess_image(image)
        
        # Realizar la predicción
        prediction = model.predict(preprocessed_image)
        
        # Determinar la clase predicha
        class_label = 'Perro' if prediction[0][0] > 0.5 else 'Gato'

        return templates.TemplateResponse(
            "index.html", 
            {"request": request, "filename": file.filename, "prediction": class_label}
        )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html", 
            {"request": request, "error": f"Error al procesar la imagen: {e}"}
        )
