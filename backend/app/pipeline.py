import os
import json
import cv2
import numpy as np

from app.draw import (
    calcular_caixa_componente_px,
    desenhar_footprint_status,
    desenhar_box_yolo_status,
)

from app.parser import carregar_componentes
from app.mm_to_pixel import mm_para_pixel_perspectiva
from app.align import carregar_imagem, detectar_contorno_pcb
from app.kicad.pcb_parser import carregar_edgecuts_pcb, extrair_bbox_edgecuts_para_csv_original

from app.yolo_detector import detectar_yolo
from app.validation import validar_componente

def run_overlay_referencia(
    caminho_img: str,
    caminho_csv: str,
    caminho_pcb: str,
    caminho_saida: str,
):
    os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)

    img = carregar_imagem(caminho_img)
    componentes = carregar_componentes(caminho_csv)

    pontos_img = detectar_contorno_pcb(img)

    pontos_edge = carregar_edgecuts_pcb(caminho_pcb)
    pontos_csv_mm = extrair_bbox_edgecuts_para_csv_original(pontos_edge)

    matriz = cv2.getPerspectiveTransform(
        np.float32(pontos_csv_mm),
        np.float32(pontos_img)
    )

    # 1) YOLO roda na imagem ORIGINAL e limpa
    detections = detectar_yolo(img)

    # 2) imagem final só para desenhar o resultado
    img_resultado = img.copy()

    # 3) controla quais detecções YOLO já foram usadas
    deteccoes_usadas = set()

    for comp in componentes:
        caixa_info = calcular_caixa_componente_px(
            comp=comp,
            matriz_transformacao=matriz,
            padding_px=2
        )

        validacao = validar_componente(
            img_original=img,
            comp=comp,
            caixa_info=caixa_info,
            detections=detections,
            deteccoes_usadas=deteccoes_usadas,
        )

        nome_comp = comp["ref"]  # se quiser trocar para comp["val"], troque aqui
        texto = f"{nome_comp} {validacao['status']}"

        if validacao["status"] == "presente":
            # Desenha SOMENTE a caixa da YOLO
            desenhar_box_yolo_status(
                img_resultado,
                validacao["yolo"]["box"],
                (0, 255, 0),   # verde
                None
            )

        elif validacao["status"] == "incerto":
            # Desenha o footprint esperado em amarelo
            desenhar_footprint_status(
                img_resultado,
                caixa_info["pontos"],
                (0, 255, 255),   # amarelo
                texto
            )

        else:
            # Desenha o footprint esperado em vermelho
            desenhar_footprint_status(
                img_resultado,
                caixa_info["pontos"],
                (0, 0, 255),   # vermelho
                texto
            )

    cv2.imwrite(caminho_saida, img_resultado)
    print(f"[OK] Overlay + validação salvo em: {caminho_saida}")