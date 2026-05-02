from pathlib import Path
import zipfile
import subprocess

from services.footprint_service import gerar_csv_footprints


KICAD_CLI = r"C:\Program Files\KiCad\9.0\bin\kicad-cli.exe"


def extrair_pcb_do_zip(caminho_zip, pasta_output, nome_pcb="placa"):
    caminho_zip = Path(caminho_zip)
    pasta_output = Path(pasta_output)
    pasta_output.mkdir(parents=True, exist_ok=True)

    with zipfile.ZipFile(caminho_zip, "r") as zip_ref:
        arquivos_pcb = [
            arquivo for arquivo in zip_ref.namelist()
            if arquivo.endswith(".kicad_pcb")
            and "__MACOSX" not in arquivo
            and "backup" not in arquivo.lower()
            and "cache" not in arquivo.lower()
        ]

        if not arquivos_pcb:
            raise FileNotFoundError("Nenhum .kicad_pcb encontrado no ZIP.")

        arquivo_pcb = arquivos_pcb[0]
        caminho_final = pasta_output / f"{nome_pcb}.kicad_pcb"

        with zip_ref.open(arquivo_pcb) as origem, open(caminho_final, "wb") as destino:
            destino.write(origem.read())

        return caminho_final


def extrair_csv_posicoes(caminho_pcb, pasta_output, nome_csv="top.csv"):
    caminho_pcb = Path(caminho_pcb)
    pasta_output = Path(pasta_output)
    pasta_output.mkdir(parents=True, exist_ok=True)

    caminho_csv = pasta_output / nome_csv

    comando = [
        KICAD_CLI,
        "pcb",
        "export",
        "pos",
        "--format", "csv",
        "--units", "mm",
        "--side", "both",
        "--bottom-negate-x",
        "--use-drill-file-origin",
        "--output", str(caminho_csv),
        str(caminho_pcb)
    ]

    subprocess.run(comando, check=True)

    return caminho_csv


def preparar_arquivos_kicad(caminho_zip, pasta_data):
    caminho_pcb = extrair_pcb_do_zip(caminho_zip, pasta_data, nome_pcb="placa")

    pasta_csv = Path(pasta_data) / "csv"
    pasta_csv.mkdir(parents=True, exist_ok=True)

    caminho_csv_footprints = pasta_csv / "footprints.csv"

    gerar_csv_footprints(
        caminho_pcb=caminho_pcb,
        caminho_csv_saida=caminho_csv_footprints
    )

    # caminho_csv = extrair_csv_posicoes(caminho_pcb, pasta_data, nome_csv="top.csv")

    return caminho_pcb, caminho_csv_footprints