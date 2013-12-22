

from pymongo import MongoClient
import json

c = MongoClient()
db = c.bus_shapes.Collections

def go():
    db.remove()
    a = json.loads(open("shapes").read())

    for x in a.keys():
        db.insert({"route":x,"points":a[x]})


if __name__ == "__main__":
    go()
