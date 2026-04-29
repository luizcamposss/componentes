import os
import shutil
from fastapi import UploadFile

from core.config import PROJETOS_DIR, get_project_paths
from services.importador_service import importar_projeto_universal


def listar_csvs():
    projetos = []

    for projeto_dir in PROJETOS_DIR.iterdir():
        if not projeto_dir.is_dir():
            continue

        csv_dir = projeto_dir / "csv"

        if not csv_dir.exists():
            continue

        for arquivo in csv_dir.glob("*.csv"):
            projetos.append({
                "projeto": projeto_dir.name,
                "arquivo": arquivo.name
            })

    return projetos


def listar_formatos_suportados():
    return {
        "formatos": [
            ".kicad_pcb",
            ".zip",
            ".PcbDoc",
            ".brd",
            ".pcb"
        ]
    }


def salvar_upload_temporario(arquivo: UploadFile, nome_projeto: str):
    os.makedirs(PROJETOS_DIR, exist_ok=True)

    caminho_temp = os.path.join(
        PROJETOS_DIR,
        f"{nome_projeto}_{arquivo.filename}"
    )

    with open(caminho_temp, "wb") as buffer:
        shutil.copyfileobj(arquivo.file, buffer)

    return caminho_temp


def salvar_novo_projeto(nome_projeto: str, arquivo_projeto: UploadFile):
    caminho_upload = salvar_upload_temporario(arquivo_projeto, nome_projeto)

    try:
        resultado = importar_projeto_universal(caminho_upload, nome_projeto)

        return {
            "message": "Projeto importado com sucesso.",
            "pcb": resultado.get("pcb"),
            "csv": resultado.get("csv"),
            "pcb_legacy": resultado.get("pcb_legacy"),
            "csv_legacy": resultado.get("csv_legacy")
        }

    finally:
        if os.path.exists(caminho_upload):
            os.remove(caminho_upload)


def criar_novo_projeto(file: UploadFile, nome_projeto: str):
    return salvar_novo_projeto(nome_projeto, file)