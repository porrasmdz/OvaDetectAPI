from typing import Any, Dict, List
from app import database as db

def list_users(fields: List[str], filters: Dict[str, str], order_by='updated_at',
               order_dir='ASC', limit: int = 50, page: int = 1) -> db.PagedResource:
    return db.list_all(
        "users",
        fields=fields,
        filters=filters,
        order_by=order_by,
        order_dir=order_dir,
        limit=limit,
        page=page
    )

def get_one_user(filters: Dict[str, str]) -> Dict[str, Any]:
    return db.get_one("users", filters)

def create_users(data_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return db.create_many("users", data_rows)

def update_user(id: int, new_values: Dict[str, Any]) -> Dict[str, Any]:
    return db.update_one("users", id, new_values)

def delete_users(ids: List[int]) -> int:
    return db.delete_many("users", ids)
