from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse

from core.config import OUTPUT_DIR
from services.processamento_service import processar_uploads

router = APIRouter(prefix="/processar", tags=["Processamento"])


@router.post("/")
async def processar_placa(
    imagem: UploadFile = File(...),
    kicad_zip: UploadFile = File(...)
):
    return processar_uploads(imagem, kicad_zip)


@router.get("/resultado")
def obter_resultado():
    caminho_saida = OUTPUT_DIR / "overlay_ref.png"

    if not caminho_saida.exists():
        return {"erro": "Nenhum resultado gerado ainda."}

    return FileResponse(caminho_saida, media_type="image/png")