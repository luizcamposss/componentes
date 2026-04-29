from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
from services.inspecao_service import inspecionar_placa
from core.config import get_project_paths, normalizar_nome_projeto

router = APIRouter(tags=["Inspeção"])


@router.post("/inspecionar-placa/")
async def inspecionar(
    imagem: UploadFile = File(...),
    projeto_csv: str = Form(...),
    nome_projeto: str = Form(...)
):
    return inspecionar_placa(imagem, projeto_csv, nome_projeto)


@router.get("/resultado/{nome_projeto}/{nome_arquivo}")
def resultado(nome_projeto: str, nome_arquivo: str):
    nome_projeto = normalizar_nome_projeto(nome_projeto)
    paths = get_project_paths(nome_projeto)

    caminho = paths["output"] / nome_arquivo

    if not caminho.exists():
        return {"erro": "Resultado não encontrado"}

    return FileResponse(caminho, media_type="image/png")