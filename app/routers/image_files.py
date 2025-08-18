from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Optional, Dict
from app.repository import image_file as image_file_repositories 
from app.models import ImageFile, ImageFileCreate, ImageFileUpdate, PagedResource

router = APIRouter()

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
