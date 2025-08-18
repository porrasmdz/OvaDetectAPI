from typing import Any, Dict, List
from app import database as db

def list_analysis_results(fields: List[str], filters: Dict[str, str], order_by='updated_at',
               order_dir='ASC', limit: int = 50, page: int = 1) -> db.PagedResource:
    return db.list_all(
        "analysis_results",
        fields=fields,
        filters=filters,
        order_by=order_by,
        order_dir=order_dir,
        limit=limit,
        page=page
    )

def get_one_analysis_result(filters: Dict[str, str]) -> Dict[str, Any]:
    return db.get_one("analysis_results", filters)

def create_analysis_results(data_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return db.create_many("analysis_results", data_rows)

def update_analysis_result(id: int, new_values: Dict[str, Any]) -> Dict[str, Any]:
    return db.update_one("analysis_results", id, new_values)

def delete_analysis_results(ids: List[int]) -> int:
    return db.delete_many("analysis_results", ids)
