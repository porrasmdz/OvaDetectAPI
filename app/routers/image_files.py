import os
from fastapi import APIRouter, File, HTTPException, Query, Path, UploadFile
from typing import Any, List, Optional, Dict
from app.repository import image_file as image_file_repositories 
from app.models import ImageFile, ImageFileCreate, ImageFileUpdate, PagedResource
from datetime import datetime
from app.config import settings
from keras.applications.vgg19 import preprocess_input, VGG19
from keras.preprocessing import image
from keras.layers import Dense, Flatten, Dropout
from app.repository import analysis_results
from keras.models import Model, load_model
import cv2
import numpy as np

mime_types = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "gif": "image/gif",
    "bmp": "image/bmp",
    "tiff": "image/tiff",
}
router = APIRouter()
IMG_SIZE = 224
UPLOAD_FOLDER = "uploads"
AI_FOLDER = "ai"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = load_model(f"ai/{settings.MODEL_NAME}")

def apply_clahe(image_array):
    if image_array.dtype != np.uint8:
        image_array = (image_array * 255).astype(np.uint8)
    if len(image_array.shape) == 3:
        clahe_img = np.zeros_like(image_array)
        for i in range(image_array.shape[2]):
            clahe = cv2.createCLAHE(clipLimit=0.03, tileGridSize=(8,8))
            clahe_img[:,:,i] = clahe.apply(image_array[:,:,i])
        return clahe_img / 255.0
    else:
        clahe = cv2.createCLAHE(clipLimit=0.03, tileGridSize=(8,8))
        return clahe.apply(image_array) / 255.0

def enhanced_preprocessing(x):
    x_clahe = apply_clahe(x)
    return preprocess_input(x_clahe * 255.0)




@router.get("/image_files",  response_model=PagedResource)
def list_image_files_api(
     fields: Optional[List[str]] = ["*"],
    limit: int = 10,
    page: int = 1,
    order_by: str = "id",
    order_dir: str = "ASC",
    filters: Optional[Dict[str, str]] = None
):
    return image_file_repositories.list_image_files(
        fields=fields,
        filters=filters or {},
        order_by=order_by,
        order_dir=order_dir,
        limit=limit,
        page=page
    )
@router.post("/image_files/upload", response_model=Any)
async def upload_files(files: List[UploadFile] = File(...)):
    saved_files = {}
    created_results = []
    for file in files:
        ext = os.path.splitext(file.filename)[1]  
        timestamp = int(datetime.now().timestamp() * 1_000_000)
        new_filename = f"{timestamp}{ext}"

        file_path = os.path.join(UPLOAD_FOLDER, new_filename)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        saved_files[file.filename] = new_filename
        
    for original_file, file in saved_files.items():
        img_path = f"uploads/{file}"
        ext = os.path.splitext(img_path)[1]
        img = image.load_img(img_path, target_size=(IMG_SIZE, IMG_SIZE))  
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)

        img_array = enhanced_preprocessing(img_array[0])
        img_array = np.expand_dims(img_array, axis=0) 

        pred_prob = model.predict(img_array)[0][0]
        threshold = 0.35
        pred_class = int(pred_prob > threshold)
        result = {}
        # --- Guardar en image_files ---
        file_size = os.path.getsize(img_path)
        last_modified = int(os.path.getmtime(img_path))  # timestamp unix
        file_type = mime_types.get(ext, "application/octet-stream")
        image_data = {
            "name": original_file,
            "size": file_size,
            "type": file_type,  # o detectarlo dinámicamente
            "last_modified": last_modified,
            "url": img_path,
            "thumbnail": None,
            "width": IMG_SIZE,
            "height": IMG_SIZE,
            "uploaded_at": datetime.now().isoformat(),
            "status": "uploaded",
            "error": None
        }
        print(image_data)
        created_image = image_file_repositories.create_image_files([image_data])
        print("CREATED IMAGe", created_image)
        result["image"] = created_image
        # --- Guardar en analysis_results ---
        findings = {"class": "Infectedo" if pred_class==1 else "No Infectado"}
        recommendations = ["Repetir ecografía en fase folicular temprana", "Análisis hormonal para confirmar diagnóstico", "Evaluación de síntomas clínicos asociados"]

        analysis_data = {
            "image_id": int(created_image[0]["id"]),
            "pcos_probability": float(pred_prob),
            "confidence": float(pred_prob),
            "findings": str(findings),
            "recommendations": str(recommendations),
            "analyzed_at": datetime.now().isoformat(),
            "status": "completed",
            "error": None
        }
        a_result = analysis_results.create_analysis_results([analysis_data])
        result["result"] = a_result

        created_results.append(result) 
        # print(f"Prediction for {original_file}")
        # print(f"Predicted probability: {pred_prob:.4f}")
        # print(f"Predicted class: {pred_class} ({'Infected' if pred_class==1 else 'Not Infected'})")

    return created_results

@router.get("/image_files/{image_id}", response_model=ImageFile)
def get_image_file_api(image_id: int):
    image_file = image_file_repositories.get_one_image_file({"id": image_id})
    if not image_file:
        raise HTTPException(status_code=404, detail="image_file not found")
    return image_file

@router.post("/image_files", response_model=List[ImageFile])
def create_image_files_api(image_files: List[ImageFileCreate]):
    
    data_rows = [image_file.model_dump(exclude_unset=True) for image_file in image_files]
    created = image_file_repositories.create_image_files(data_rows)
    return created

@router.put("/image_files/{image_id}", response_model=ImageFile)
def update_image_file_api(image_id: int, image_file_update: ImageFileUpdate):
    updated = image_file_repositories.update_image_file(image_id, image_file_update.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="image_file not found")
    return updated

@router.delete("/image_files", response_model=int)
def delete_image_files_api(ids: List[int] = Query(...)):
    deleted_count = image_file_repositories.delete_image_files(ids)
    return deleted_count
