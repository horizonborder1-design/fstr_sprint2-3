from pydantic import BaseModel, EmailStr, Field, model_validator, ConfigDict
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    fam: Optional[str] = None
    name: Optional[str] = None
    otc: Optional[str] = None
    phone: Optional[str] = None

class CoordsCreate(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    height: Optional[int] = Field(None, ge=0)

class LevelCreate(BaseModel):
    winter: Optional[str] = None
    summer: Optional[str] = None
    autumn: Optional[str] = None
    spring: Optional[str] = None

class ImageCreate(BaseModel):
    data: str
    title: Optional[str] = None

class PassCreate(BaseModel):
    beauty_title: Optional[str] = None
    title: str
    other_titles: Optional[str] = None
    connect: Optional[str] = None
    add_time: Optional[datetime] = None
    user: UserCreate
    coords: CoordsCreate
    level: Optional[LevelCreate] = None
    images: Optional[List[ImageCreate]] = None

    @model_validator(mode='after')
    def check_title(self):
        if not self.title or not self.title.strip():
            raise ValueError('Название перевала не может быть пустым')
        return self

class UserRead(BaseModel):
    email: str
    fam: Optional[str] = None
    name: Optional[str] = None
    otc: Optional[str] = None
    phone: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class ImageRead(BaseModel):
    id: int
    data: str
    title: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class PassRead(BaseModel):
    id: int
    beauty_title: Optional[str] = None
    title: str
    other_titles: Optional[str] = None
    connect: Optional[str] = None
    add_time: Optional[datetime] = None
    latitude: float
    longitude: float
    height: Optional[int] = None
    level_winter: Optional[str] = None
    level_spring: Optional[str] = None
    level_summer: Optional[str] = None
    level_autumn: Optional[str] = None
    status: str
    user: UserRead
    images: List[ImageRead] = []
    model_config = ConfigDict(from_attributes=True)

class SubmitResponse(BaseModel):
    status: int
    message: Optional[str] = None
    id: Optional[int] = None

class UpdateResponse(BaseModel):
    state: int
    message: str