from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Optional, Dict
from app.repository import analysis_results as analysis_repo 
from app.models import ImageFile, ImageFileCreate, ImageFileUpdate, PagedResource

router = APIRouter()

@router.get("/analysis_results", response_model=PagedResource)
def list_analysis_results_api(
    fields: Optional[List[str]] = ["*"],
    limit: int = 10,
    page: int = 1,
    order_by: str = "id",
    order_dir: str = "ASC",
    filters: Optional[Dict[str, str]] = None
):
    return analysis_repo.list_analysis_results(
        fields=fields,
        filters=filters or {},
        order_by=order_by,
        order_dir=order_dir,
        limit=limit,
        page=page
    )

@router.get("/analysis_results/{image_id}", response_model=ImageFile)
def get_analysis_result_api(image_id: int):
    analysis_result = analysis_repo.get_one_analysis_result({"id": image_id})
    if not analysis_result:
        raise HTTPException(status_code=404, detail="analysis_result not found")
    return analysis_result

@router.post("/analysis_results", response_model=List[ImageFile])
def create_analysis_results_api(analysis_results: List[ImageFileCreate]):
    
    data_rows = [analysis_result.model_dump(exclude_unset=True) for analysis_result in analysis_results]
    created = analysis_repo.create_analysis_results(data_rows)
    return created

@router.put("/analysis_results/{image_id}", response_model=ImageFile)
def update_analysis_result_api(image_id: int, analysis_result_update: ImageFileUpdate):
    updated = analysis_repo.update_analysis_result(image_id, analysis_result_update.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="analysis_result not found")
    return updated

@router.delete("/analysis_results", response_model=int)
def delete_analysis_results_api(ids: List[int] = Query(...)):
    deleted_count = analysis_repo.delete_analysis_results(ids)
    return deleted_count
