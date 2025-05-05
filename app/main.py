from typing import Annotated
from fastapi import FastAPI, Depends, Response
from sqlalchemy.ext.asyncio import(
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)
from contextlib import asynccontextmanager
from . import models, schemas
from sqlalchemy import select, insert, delete, update
from authx import AuthX, AuthXConfig
from fastapi.security import OAuth2PasswordRequestForm
from . import secrets

Engine = create_async_engine("sqlite+aiosqlite:///database.db")
Session = async_sessionmaker(Engine, expire_on_commit=False)
App = FastAPI()

async def get_session():
    async with Session() as session:
        yield session

SessionDependency = Annotated[AsyncSession, Depends(get_session)]

authx_config = AuthXConfig()
authx_config.JWT_CSRF_METHODS = []
authx_config.JWT_SECRET_KEY = secrets.SecretKey
authx_config.JWT_ACCESS_COOKIE_NAME = "access_cookie"
authx_config.JWT_TOKEN_LOCATION = ["cookies"]
security = AuthX(config=authx_config)
AuthLogin = secrets.Login
AuthPass = secrets.Pass

SecurityDependency = [Depends(security.access_token_required)]


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    """
    Startup and shutdown events processors
    """
    async with Engine.begin() as con:
        await con.run_sync(models.BaseModel.metadata.drop_all)
        await con.run_sync(models.BaseModel.metadata.create_all)
    
    yield
    
    return


@App.post("/signin", tags=["signin"])
async def signin_handler(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response):
    if form_data.username == AuthLogin and form_data.password == AuthPass:
        response.set_cookie(authx_config.JWT_ACCESS_COOKIE_NAME, security.create_access_token(uid=AuthLogin))

@App.get("/")
async def welcome_page():
    return "Welcome!"

@App.get("/article", tags=["article"])
async def article_get_handler(params: Annotated[schemas.SchemaIdentifier, Depends()], session: SessionDependency):
    """
        Получение данных о статье по её идентификатору
    """
    stmt = select(models.ModelArticle).where(models.ModelArticle.id == params.id)
    objs = await session.execute(stmt)
    return objs.scalar()


@App.put("/article_change", tags=["article"], dependencies=SecurityDependency)
async def article_change_handler(params: Annotated[schemas.SchemaArticle, Depends()], session: SessionDependency):
    """
        Изменение данных о существующей статье
    """
    obj = await session.get(models.ModelArticle, params.id)
    if obj:
        obj.title = params.title
        await session.commit()


@App.put("/article_add", tags=["article"], dependencies=SecurityDependency)
async def article_add_handler(params: Annotated[schemas.SchemaArticle, Depends()], session: SessionDependency):
    """
        Добавление новой статьи
    """
    await session.execute(
        insert(models.ModelArticle),
        {
            "id": params.id,
            "title": params.title
        }
    )
    await session.commit()


@App.delete("/article_delete", tags=["article"], dependencies=SecurityDependency)
async def article_delete_handler(params: Annotated[schemas.SchemaIdentifier, Depends()], session: SessionDependency):
    """
        Удаление статьи
    """
    stmt = delete(models.ModelArticle).where(models.ModelArticle.id == params.id)
    objs = await session.execute(stmt)
    return objs.rowcount



@App.get("/device", tags=["device"])
async def device_get_handler(params: Annotated[schemas.SchemaIdentifier, Depends()], session: SessionDependency):
    """
        Получение данных о секвенаторе по его идентификатору
    """
    stmt = select(models.ModelDevice).where(models.ModelDevice.id == params.id)
    objs = await session.execute(stmt)
    return objs.scalar()


@App.put("/device_change", tags=["device"], dependencies=SecurityDependency)
async def device_change_handler(params: Annotated[schemas.SchemaDevice, Depends()], session: SessionDependency):
    """
        Изменение данных о существующем секвенаторе
    """
    obj = await session.get(models.ModelDevice, params.id)
    if obj:
        obj.name = params.name
        obj.country = params.country
        await session.commit()


@App.put("/device_add", tags=["device"], dependencies=SecurityDependency)
async def device_add_handler(params: Annotated[schemas.SchemaDevice, Depends()], session: SessionDependency):
    """
        Добавление нового секвенатора
    """
    await session.execute(
        insert(models.ModelDevice),
        {
            "id": params.id,
            "name": params.name,
            "country": params.country
        }
    )
    await session.commit()


@App.delete("/device_delete", tags=["device"], dependencies=SecurityDependency)
async def device_delete_handler(params: Annotated[schemas.SchemaIdentifier, Depends()], session: SessionDependency):
    """
        Удаление секвенатора
    """
    stmt = delete(models.ModelDevice).where(models.ModelDevice.id == params.id)
    objs = await session.execute(stmt)
    return objs.rowcount



@App.get("/application", tags=["application"])
async def application_get_handler(params: Annotated[schemas.SchemaIdentifier, Depends()], session: SessionDependency):
    """
        Получение данных о применении секвенатора по идентификатору записи
    """
    stmt = select(models.ModelApplication).where(models.ModelApplication.record_id == params.id)
    objs = await session.execute(stmt)
    return objs.scalar()


@App.put("/application_change", tags=["application"], dependencies=SecurityDependency)
async def application_change_handler(params: Annotated[schemas.SchemaApplication, Depends()], session: SessionDependency):
    """
        Изменение данных о существующем применении секвенатора
    """
    obj = await session.get(models.ModelApplication, params.record_id)
    if obj:
        obj.device_id = params.device_id
        obj.article_id = params.article_id
        obj.seq_obj = params.seq_obj
        await session.commit()


@App.put("/application_add", tags=["application"], dependencies=SecurityDependency)
async def application_add_handler(params: Annotated[schemas.SchemaApplication, Depends()], session: SessionDependency):
    """
        Добавление новой записи о применении секвенатора
    """
    await session.execute(
        insert(models.ModelApplication),
        {
            "record_id": params.record_id,
            "device_id": params.device_id,
            "article_id": params.article_id,
            "seq_obj": params.seq_obj
        }
    )
    await session.commit()


@App.delete("/application_delete", tags=["application"], dependencies=SecurityDependency)
async def application_delete_handler(params: Annotated[schemas.SchemaIdentifier, Depends()], session: SessionDependency):
    """
        Удаление записи о применении секвенатора
    """
    stmt = delete(models.ModelApplication).where(models.ModelApplication.record_id == params.record_id)
    objs = await session.execute(stmt)
    return objs.rowcount


@App.get("/devices_for_obj", tags=["stats"])
async def devices_for_obj(params: Annotated[schemas.SchemaObj, Depends()], session: SessionDependency):
    stmt = select(models.ModelApplication).where(models.ModelApplication.seq_obj == params.obj)
    cases = await session.execute(stmt)
    
    result = []
    for case in cases.scalars():
        stmt = select(models.ModelDevice).where(models.ModelDevice.id == case.device_id)
        device = await session.execute(stmt)
        if device:
            result.append(device)

    return result


@App.get("/objs_on_device", tags=["stats"])
async def objs_on_device(params: Annotated[schemas.SchemaIdentifier, Depends()], session: SessionDependency):
    stmt = select(models.ModelApplication).where(models.ModelApplication.device_id == params.id)
    cases = await session.execute(stmt)
    return list(map(lambda x: x.seq_obj, cases.scalars()))
