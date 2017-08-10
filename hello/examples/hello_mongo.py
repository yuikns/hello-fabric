
from ..io.mongoclient import MongoAgent
from ..config import DefaultConfig


class HelloMongo(object):
    def __init__(self):
        self.mgo = MongoAgent(DefaultConfig.MONGO_ADDRESS, DefaultConfig.MONGO_PORT, DefaultConfig.MONGO_DB, "", "")
        self.cnt = 0

    def iter(self):
        self.mgo.iter_all(self.mgo.calls_col, lambda d: self.call_proc(d))

    def call_proc(self, doc):
        self.cnt += 1
        from bson.objectid import ObjectId
        seg = self.mgo.find_one_by_key_value(self.mgo.segments_col, "call_id", ObjectId(doc["_id"]))
        print(doc["_id"], self.cnt)
        if seg is not None:
            cap = seg["caption"]
            print("seg:", cap)
        return self.cnt < 10

if __name__ == "__main__":
    hm = HelloMongo()
    hm.iter()

