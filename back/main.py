from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.sequential import routes_sequential
from routes.highd import routes_highd
from routes.rtree import routes_rtree
from routes.invidx import routes_invidx
from routes.gin import routes_gin
from routes.music import routes_music
from handlers.SequentialHandler import SequentialHandler
from handlers.RTreeHandler import RTreeHandler
from handlers.HighdHandler import HighdHandler
from handlers.InvIdxHandler import InvIdxHandler
from handlers.GinHandler import GinHandler
from handlers.handlers_dict import handlers

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

async def on_startup():
    try:
        handlers['highd'] = HighdHandler()
        handlers['sequential'] = SequentialHandler()
        handlers['rtree'] = RTreeHandler()
        handlers['invidx'] = InvIdxHandler()
        handlers['gin'] = GinHandler()
    except Exception as e:
        print(f"Error: {e}")

async def on_shutdown():
    handlers.clear()

app.add_event_handler("startup", on_startup)
app.add_event_handler("shutdown", on_shutdown)

app.include_router(routes_sequential, prefix="/sequential")
app.include_router(routes_rtree, prefix="/rtree")
app.include_router(routes_highd, prefix="/highd")
app.include_router(routes_invidx, prefix="/invidx")
app.include_router(routes_gin, prefix="/gin")
app.include_router(routes_music, prefix="/music")
