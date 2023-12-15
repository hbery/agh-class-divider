from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pozwala na wszystkie źródła
    allow_credentials=True,
    allow_methods=["*"],  # Pozwala na wszystkie metody
    allow_headers=["*"],  # Pozwala na wszystkie nagłówki
)

@app.get("/")
def read_root():
    return {"Hello": "World"}
