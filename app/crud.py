from sqlalchemy.orm import Session, joinedload
from . import models, schemas
import base64
from typing import Optional, List

class DatabaseManager:
    @staticmethod
    def create_or_get_user(db: Session, user_data: schemas.UserCreate) -> models.User:
        db_user = db.query(models.User).filter(models.User.email == user_data.email).first()
        if db_user:
            return db_user
        new_user = models.User(**user_data.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def create_pass(db: Session, pass_data: schemas.PassCreate, user_id: int) -> models.Pass:
        level = pass_data.level or schemas.LevelCreate()
        new_pass = models.Pass(
            beauty_title=pass_data.beauty_title,
            title=pass_data.title,
            other_titles=pass_data.other_titles,
            connect=pass_data.connect,
            add_time=pass_data.add_time,
            latitude=pass_data.coords.latitude,
            longitude=pass_data.coords.longitude,
            height=pass_data.coords.height,
            level_winter=level.winter,
            level_spring=level.spring,
            level_summer=level.summer,
            level_autumn=level.autumn,
            status="new",
            user_id=user_id
        )
        db.add(new_pass)
        db.commit()
        db.refresh(new_pass)
        return new_pass

    @staticmethod
    def create_images(db: Session, pass_id: int, images: List[schemas.ImageCreate]) -> List[models.PassImage]:
        if not images:
            return []
        db_images = []
        for img in images:
            data_bytes = base64.b64decode(img.data.split(',')[1]) if img.data.startswith('data:image') else img.data.encode('utf-8')
            db_img = models.PassImage(pass_id=pass_id, data=data_bytes, title=img.title)
            db.add(db_img)
            db_images.append(db_img)
        db.commit()
        return db_images

    @staticmethod
    def submit_pass(db: Session, pass_data: schemas.PassCreate) -> tuple[bool, str, int]:
        try:
            user = DatabaseManager.create_or_get_user(db, pass_data.user)
            new_pass = DatabaseManager.create_pass(db, pass_data, user.id)
            if pass_data.images:
                DatabaseManager.create_images(db, new_pass.id, pass_data.images)
            return True, "Отправлено успешно", new_pass.id
        except Exception as e:
            db.rollback()
            return False, f"Ошибка при выполнении операции: {str(e)}", None

    
    @staticmethod
    def get_pass_by_id(db: Session, pass_id: int) -> Optional[models.Pass]:
        """Получить одну запись по ID с подгрузкой пользователя и картинок"""
        return (
            db.query(models.Pass)
            .options(
                joinedload(models.Pass.user),
                joinedload(models.Pass.images)
            )
            .filter(models.Pass.id == pass_id)
            .first()
        )

    @staticmethod
    def update_pass(db: Session, pass_id: int, pass_data: schemas.PassCreate) -> tuple[int, str]:
        """
        Редактировать запись, если статус 'new'.
        Возвращает (state: 1/0, message: str)
        """
        db_pass = db.query(models.Pass).filter(models.Pass.id == pass_id).first()
        if not db_pass:
            return 0, "Перевал не найден"
        if db_pass.status != "new":
            return 0, f"Редактирование невозможно. Текущий статус: {db_pass.status}"

        db_pass.beauty_title = pass_data.beauty_title
        db_pass.title = pass_data.title
        db_pass.other_titles = pass_data.other_titles
        db_pass.connect = pass_data.connect
        db_pass.add_time = pass_data.add_time
        db_pass.latitude = pass_data.coords.latitude
        db_pass.longitude = pass_data.coords.longitude
        db_pass.height = pass_data.coords.height

        if pass_data.level:
            db_pass.level_winter = pass_data.level.winter
            db_pass.level_spring = pass_data.level.spring
            db_pass.level_summer = pass_data.level.summer
            db_pass.level_autumn = pass_data.level.autumn

        db.commit()
        db.refresh(db_pass)
        return 1, "Запись успешно обновлена"

    @staticmethod
    def get_passes_by_user_email(db: Session, email: str) -> List[models.Pass]:
        """Список всех объектов пользователя с подгрузкой связанных данных"""
        return (
            db.query(models.Pass)
            .options(
                joinedload(models.Pass.user),
                joinedload(models.Pass.images)
            )
            .join(models.User, models.Pass.user_id == models.User.id)
            .filter(models.User.email == email)
            .all()
        )