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
        await cls._collection.find_one_and_update({'_id': id}, {'$set': kwargs})
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
    def set_collection(cls, collection: MotorCollection):
        cls._collection = db[collection]
