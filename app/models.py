from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Any, Optional ,List

class User(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: str  # 'doctor' | 'technician' | 'admin'
    avatar: Optional[str] = None

class UserCreate(BaseModel):
    name: Optional[str] = None
    email: EmailStr = None
    role: Optional[str] = None
    avatar: Optional[str] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    avatar: Optional[str] = None


class ImageFileCreate(BaseModel):
    name: str = None
    size: Optional[int] = None
    type: Optional[str] = None
    last_modified: Optional[int] = None
    url: Optional[str] = None
    thumbnail: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    uploaded_at: Optional[datetime] = None
    status: Optional[str] = None
    error: Optional[str] = None

class ImageFileUpdate(BaseModel):
    name: Optional[str] = None
    size: Optional[int] = None
    type: Optional[str] = None
    last_modified: Optional[int] = None
    url: Optional[str] = None
    thumbnail: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    uploaded_at: Optional[datetime] = None
    status: Optional[str] = None
    error: Optional[str] = None

class ImageFile(BaseModel):
    id: str
    name: str
    size: int
    type: str
    last_modified: int
    url: str
    thumbnail: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    uploaded_at: datetime
    status: str  # 'uploading' | 'uploaded' | 'error' | 'processing'
    error: Optional[str] = None



class AnalysisResultCreate(BaseModel):
    image_id: Optional[str] = None
    pcos_probability: Optional[float] = None
    confidence: Optional[float] = None
    findings: Optional[List[str]] = Field(default_factory=list)
    recommendations: Optional[List[str]] = Field(default_factory=list)
    analyzed_at: Optional[datetime] = None
    status: Optional[str] = None
    error: Optional[str] = None

class AnalysisResultUpdate(BaseModel):
    image_id: Optional[str] = None
    pcos_probability: Optional[float] = None
    confidence: Optional[float] = None
    findings: Optional[List[str]] = Field(default_factory=list)
    recommendations: Optional[List[str]] = Field(default_factory=list)
    analyzed_at: Optional[datetime] = None
    status: Optional[str] = None
    error: Optional[str] = None
class AnalysisResult(BaseModel):
    id: str
    image_id: str
    pcos_probability: float
    confidence: float
    findings: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
    analyzed_at: datetime
    status: str  # 'pending' | 'processing' | 'completed' | 'error'
    error: Optional[str] = None

class PagedResource(BaseModel):
    data: List[Any]
    total_results: int
    total_pages: int