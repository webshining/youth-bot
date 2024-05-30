from copy import deepcopy
from typing import get_origin, get_args

from bson.objectid import ObjectId as BsonObjectId
from motor.motor_tornado import MotorCollection
from pydantic import BaseModel

from loader import db


class ObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, BsonObjectId):
            raise TypeError('ObjectId required')
        return str(v)


class Base(BaseModel):
    _collection: MotorCollection = None

    @classmethod
    async def count(cls):
        num = await cls._collection.count_documents({})
        return num

    @classmethod
    async def nextid(cls):
        obj = await cls._collection.find().limit(1).sort({"$natural": -1}).to_list(1)
        return int(obj[0]['_id']) + 1 if obj else 1

    @classmethod
    async def get(cls, id: int):
        obj = await cls._collection.find_one({'_id': id})
        return cls(**obj) if obj else None

    @classmethod
    async def get_by(cls, **kwargs):
        if 'id' in kwargs:
            kwargs['_id'] = kwargs.pop('id')
        obj = await cls._collection.find_one(kwargs)
        return cls(**obj) if obj else None

    @classmethod
    async def get_all(cls):
        objs = await cls._collection.find().to_list(10000)
        return [cls(**u) for u in objs]

    @classmethod
    async def update(cls, id: int, **kwargs):
        if 'id' in kwargs:
            del kwargs['id']
        if '_id' in kwargs:
            del kwargs['_id']
        await cls._collection.find_one_and_update({'_id': id}, {'$set': kwargs}, return_document=True)
        return await cls.get(id)

    @classmethod
    async def create(cls, **kwargs):
        if '_id' not in kwargs:
            kwargs["_id"] = await cls.nextid()
        obj = cls(**kwargs)
        obj = await cls._collection.insert_one(obj.model_dump(by_alias=True))
        return await cls.get(obj.inserted_id)

    @classmethod
    async def delete(cls, id: int):
        await cls._collection.find_one_and_delete({'_id': id})
        return True

    @classmethod
    def set_collection(cls, collection: str):
        cls._collection = db[collection]


def without_alias(model):
    model = deepcopy(model)

    new_fields = {}
    new_annotations = {}
    for name, field in model.__fields__.items():
        field_type = field.annotation
        origin_type = get_origin(field_type)
        if origin_type is None and issubclass(field_type, BaseModel):
            new_fields[name] = without_alias(field_type)
            new_annotations[name] = new_fields[name]
        elif origin_type:
            sub_field = get_args(field_type)[0]
            if issubclass(sub_field, BaseModel):
                new_fields[name] = origin_type[without_alias(sub_field)]
                new_annotations[name] = new_fields[name]
        if name not in new_fields:
            if field.alias != name:
                field.alias = name
                field.validation_alias = name
                field.serialization_alias = name
                field.alias_priority = 1
            new_fields[name] = field
            new_annotations[name] = field_type

    model = type(f"{model.__name__}WithoutAliases", (BaseModel,), {
        "__fields__": new_fields,
        '__annotations__': new_annotations,
        '__module__': model.__module__,
    })

    return model
