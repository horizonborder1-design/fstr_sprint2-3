from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, LargeBinary
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship  # 🔹 ИМПОРТ ОБЯЗАТЕЛЕН
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    fam = Column(String(255))
    name = Column(String(255))
    otc = Column(String(255))
    phone = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 🔹 СВЯЗЬ: пользователь -> перевалы
    passes = relationship("Pass", back_populates="user")

class Pass(Base):
    __tablename__ = "passes"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Основные данные
    beauty_title = Column(String(255))
    title = Column(String(255), nullable=False)
    other_titles = Column(Text)
    connect = Column(Text)
    add_time = Column(DateTime(timezone=True))
    
    # Координаты
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    height = Column(Integer)
    
    # Категории трудности
    level_winter = Column(String(10))
    level_spring = Column(String(10))
    level_summer = Column(String(10))
    level_autumn = Column(String(10))
    
    # Статус модерации
    status = Column(String(20), default="new", server_default="new", nullable=False)
    
    # Связи
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Аудит
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 🔹 СВЯЗЬ: перевал -> пользователь
    user = relationship("User", back_populates="passes")
    
    # 🔹 СВЯЗЬ: перевал -> картинки (обрати внимание на back_populates="pass_rel")
    images = relationship("PassImage", back_populates="pass_rel", cascade="all, delete-orphan")

class PassImage(Base):
    __tablename__ = "pass_images"
    
    id = Column(Integer, primary_key=True, index=True)
    pass_id = Column(Integer, ForeignKey("passes.id", ondelete="CASCADE"), nullable=False)
    data = Column(LargeBinary, nullable=False)
    title = Column(String(255))
    added_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 🔹 СВЯЗЬ: картинка -> перевал
    # ИСПОЛЬЗУЕМ pass_rel, ТАК КАК 'pass' — ЗАРЕЗЕРВИРОВАННОЕ СЛОВО!
    pass_rel = relationship("Pass", back_populates="images")