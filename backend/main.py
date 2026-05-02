from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes.projetos import router as projetos_router
from api.routes.inspecao import router as inspecao_router

app = FastAPI(title="Componentes AOI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projetos_router)
app.include_router(inspecao_router)