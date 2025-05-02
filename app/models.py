from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    pass


class ModelDevice(BaseModel):
    """
        Информация о секвенаторах ДНК.
    """

    __tablename__ = "device"

    id = Column(Integer, primary_key=True)
    name: Column(String, nullable=False)
    country: Column(String, nullable=False)


class ModelArticle(BaseModel):
    """
        Информация о статьях.
    """

    __tablename__ = "article"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)


class ModelApplication(BaseModel):
    """
        Информация о применённых в статьях секвинированиях.
    """

    __tablename__ = "application"

    device_id = Column(Integer, nullable=False)
    article_id = Column(Integer, nullable=False)
    seq_obj = Column(String, nullable=False)
