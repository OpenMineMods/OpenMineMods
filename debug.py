from API.CurseAPI import *
from CurseMetaDB.DB import DB

c = CurseAPI(DB({"projects": [], "files": [], "categories": [], "authors": []}))
