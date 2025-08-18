from fastapi import APIRouter, HTTPException, Query, Path
from typing import List, Optional, Dict, Any
from app.repository import users as user_repository  # tu repository de users
from app.models import User, UserCreate, UserUpdate, PagedResource

users = APIRouter()

@users.get("/users", response_model=PagedResource)
def list_users_api(
    fields: Optional[List[str]] = ["*"],
    limit: int = 10,
    page: int = 1,
    order_by: str = "id",
    order_dir: str = "ASC",
    filters: Optional[Dict[str, str]] = None
):
    return user_repository.list_users(
        fields=fields,
        filters=filters or {},
        order_by=order_by,
        order_dir=order_dir,
        limit=limit,
        page=page
    )

@users.get("/users/{user_id}", response_model=User)
def get_user_api(user_id: int = Path(...)):
    user = user_repository.get_one_user({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@users.post("/users", response_model=List[User])
def create_users_api(users: List[UserCreate]):
  
    data_rows = [user.model_dump(exclude_unset=True) for user in users]
    created = user_repository.create_users(data_rows)
    return created

@users.put("/users/{user_id}", response_model=User)
def update_user_api(user_id: int, user_update: UserUpdate):
    updated = user_repository.update_user(user_id, user_update.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@users.delete("/users", response_model=int)
def delete_users_api(ids: List[int] = Query(...)):
    deleted_count = user_repository.delete_users(ids)
    return deleted_count
