from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


app = FastAPI()

app.mount("/tiles", StaticFiles(directory="tiles"), name="tiles")
