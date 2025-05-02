from typing import Annotated
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import(
    create_async_engine,
    async_sessionmaker
)
from . import models, schemas

Engine = create_async_engine("sqlite+aiosqlite:///database.db")
Session = async_sessionmaker(Engine, expire_on_commit=False)
App = FastAPI()


@App.on_event("startup")
async def setup_models():
    async with Engine.begin() as con:
        con.run_sync(models.BaseModel.metadata.drop_all)
        con.run_sync(models.BaseModel.metadata.create_all)


@App.get("/article")
async def article_get_handler(params: Annotated[schemas.SchemaIdentifier, Depends()]):
    return "Hello world"
