from typing import Any, Dict, List
from app import database as db

def list_image_files(fields: List[str], filters: Dict[str, str], order_by='updated_at',
               order_dir='ASC', limit: int = 50, page: int = 1) -> db.PagedResource:
    return db.list_all(
        "image_files",
        fields=fields,
        filters=filters,
        order_by=order_by,
        order_dir=order_dir,
        limit=limit,
        page=page
    )

def get_one_image_file(filters: Dict[str, str]) -> Dict[str, Any]:
    return db.get_one("image_files", filters)

def create_image_files(data_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return db.create_many("image_files", data_rows)

def update_image_file(id: int, new_values: Dict[str, Any]) -> Dict[str, Any]:
    return db.update_one("image_files", id, new_values)

def delete_image_files(ids: List[int]) -> int:
    return db.delete_many("image_files", ids)
