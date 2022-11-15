from fastapi import FastAPI
from fastapi.routing import Mount
from fastapi.staticfiles import StaticFiles


app = FastAPI(routes=[Mount("/tiles", app=StaticFiles(directory="tiles"), name="tiles")])
