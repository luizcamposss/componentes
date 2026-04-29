from pathlib import Path
import shutil
from fastapi import UploadFile

from core.config import DATA_DIR, OUTPUT_DIR, PROJETO_KICAD_DIR
from app.kicad.extractor import preparar_arquivos_kicad
from app.pipeline import run_overlay_referencia


def salvar_upload(upload: UploadFile, caminho_destino: Path):
    with open(caminho_destino, "wb") as buffer:
        shutil.copyfileobj(upload.file, buffer)


def processar_uploads(imagem: UploadFile, kicad_zip: UploadFile):
    caminho_img = DATA_DIR / "arduino.jpeg"
    caminho_zip = PROJETO_KICAD_DIR / "projeto_kicad.zip"
    caminho_saida = OUTPUT_DIR / "overlay_ref.png"

    salvar_upload(imagem, caminho_img)
    salvar_upload(kicad_zip, caminho_zip)

    caminho_pcb, caminho_csv = preparar_arquivos_kicad(
        caminho_zip=caminho_zip,
        pasta_data=DATA_DIR
    )

    run_overlay_referencia(
        caminho_img=str(caminho_img),
        caminho_csv=str(caminho_csv),
        caminho_pcb=str(caminho_pcb),
        caminho_saida=str(caminho_saida),
    )

    return {
        "mensagem": "Processamento concluído",
        "imagem_resultado": "http://localhost:8000/processar/resultado"
    }