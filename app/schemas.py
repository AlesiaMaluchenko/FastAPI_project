import pydantic


class SchemaIdentifier(pydantic.BaseModel):
    id: int
