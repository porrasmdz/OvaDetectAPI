from __future__ import annotations
import math
import sqlite3
from typing import Any, Dict, List

from app.config import settings
from app.migrations import SCHEMA
from app.models import PagedResource

LIKE_FIELDS = ['name', 'description']


def ensure_db(path: str | None = None):
    db_path = path or settings.DATABASE_PATH
    conn = sqlite3.connect(db_path)
    try:
        conn.executescript(SCHEMA)
        conn.commit()
    finally:
        conn.close()

def list_all(
        table_name: str, fields: List[str], filters : Dict[str, str], 
        order_by = 'updated_at', order_dir = "ASC", limit: int  = 10,
        page: int = 1) -> PagedResource:
    ensure_db()
    conn = sqlite3.connect(settings.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        select_fields = ", ".join(fields) if fields else "*"
        base_query = f"FROM {table_name}"
        params: list = []
        like_fields = LIKE_FIELDS

        if filters:
            conditions = []
            for col, value in filters.items():
                if value is None:
                    conditions.append(f"{col} IS NULL")
                elif col in like_fields:
                    conditions.append(f"{col} LIKE ?")
                    params.append(f"%{value}%")
                else:
                    conditions.append(f"{col} = ?")
                    params.append(value)
            base_query += " WHERE " + " AND ".join(conditions)

        count_query = f"SELECT COUNT(*) {base_query}"
        total_results = conn.execute(count_query, params).fetchone()[0]
        total_pages = math.ceil(total_results / limit) if limit > 0 else 1

        query = f"SELECT {select_fields} {base_query} ORDER BY {order_by} {order_dir.upper()} LIMIT ? OFFSET ?"
        offset = (page - 1) * limit
        params_with_pagination = params + [limit, offset]
        
        rows = list(conn.execute(query, params_with_pagination))

        return PagedResource(
            data=[dict(r) for r in rows],
            total_results=total_results,
            total_pages=total_pages
        ) 
    finally:
        conn.close()

def get_one(table_name: str, filters : Dict[str, str]) -> Dict[str, Any]:
    ensure_db()
    conn = sqlite3.connect(settings.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    like_fields = LIKE_FIELDS
    try:
        query = f"SELECT * FROM {table_name}"
        params: list = []

        if filters:
            conditions = []
            for col, value in filters.items():
                if value is None:
                    conditions.append(f"{col} IS NULL")
                elif col in like_fields:
                    conditions.append(f"{col} LIKE ?")
                    params.append(f"%{value}%")
                else:
                    conditions.append(f"{col} = ?")
                    params.append(value)
            query += " WHERE " + " AND ".join(conditions)

        query += " LIMIT 1"
        row = conn.execute(query, params).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def create_many(table_name: str, data_rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not data_rows:
        return []

    ensure_db()
    conn = sqlite3.connect(settings.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        columns = list(data_rows[0].keys())
        placeholders = ", ".join(["?"] * len(columns))
        col_names = ", ".join(columns)

        inserted_ids = []

        for row in data_rows:
            values = tuple(row[col] for col in columns)
            cur = conn.execute(
                f"INSERT INTO {table_name} ({col_names}) VALUES ({placeholders})",
                values
            )
            inserted_ids.append(cur.lastrowid)

        conn.commit()

        placeholders_ids = ", ".join(["?"] * len(inserted_ids))
        select_query = f"SELECT * FROM {table_name} WHERE id IN ({placeholders_ids})"
        rows = conn.execute(select_query, inserted_ids).fetchall()

        return [dict(r) for r in rows]
    finally:
        conn.close()


def update_one(table_name: str, id: int, new_values: Dict[str, Any]):
    if not new_values:
        return {}  

    ensure_db()
    conn = sqlite3.connect(settings.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    try:
        set_clause = ", ".join([f"{col} = ?" for col in new_values.keys()])
        params = list(new_values.values())

        if not id:
            raise ValueError("Se requiere un id para actualizar.")
        
        update_query = f"UPDATE {table_name} SET {set_clause} WHERE id = ?"
        params.append(id)
        cur = conn.execute(update_query, params)
        conn.commit()

        if cur.rowcount == 0:
            return {}  
        select_query = f"SELECT * FROM {table_name} WHERE id = ? LIMIT 1"
        row = conn.execute(select_query, (id,)).fetchone()
        return dict(row) if row else {}
    finally:
        conn.close()

def delete_many(table_name: str, ids: List[int]):
    if not ids:
        return 0

    ensure_db()
    conn = sqlite3.connect(settings.DATABASE_PATH)
    try:
        placeholders = ", ".join(["?"] * len(ids))
        query = f"DELETE FROM {table_name} WHERE id IN ({placeholders})"
        cur = conn.execute(query, ids)
        conn.commit()
        return cur.rowcount
    finally:
        conn.close()
