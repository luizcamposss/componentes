
import re
import numpy as np


def carregar_edgecuts_pcb(caminho_pcb):
    with open(caminho_pcb, "r", encoding="utf-8") as f:
        conteudo = f.read()

    pontos = []

    blocos = re.findall(
        r"\((?:gr_line|gr_rect|gr_arc|gr_circle)[\s\S]*?\(layer\s+\"?Edge\.Cuts\"?\)[\s\S]*?\)",
        conteudo
    )

    for bloco in blocos:
        starts = re.findall(r"\(start\s+([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)\)", bloco)
        ends = re.findall(r"\(end\s+([-+]?\d*\.?\d+)\s+([-+]?\d*\.?\d+)\)", bloco)

        for x, y in starts:
            pontos.append((float(x), float(y)))

        for x, y in ends:
            pontos.append((float(x), float(y)))

        if "gr_rect" in bloco and len(starts) >= 1 and len(ends) >= 1:
            x1, y1 = map(float, starts[0])
            x2, y2 = map(float, ends[0])

            pontos.extend([
                (x1, y1),
                (x2, y1),
                (x2, y2),
                (x1, y2),
            ])

    if len(pontos) < 4:
        raise Exception("Não encontrou pontos suficientes de Edge.Cuts no arquivo .kicad_pcb")

    return np.array(pontos, dtype=np.float32)


def extrair_bbox_edgecuts_para_csv_original(pontos_edge):
    pontos_edge = pontos_edge.copy()

    # KiCad PCB veio com Y positivo, CSV original vem com Y negativo
    pontos_edge[:, 1] *= -1

    xs = pontos_edge[:, 0]
    ys = pontos_edge[:, 1]

    min_x, max_x = np.min(xs), np.max(xs)
    min_y, max_y = np.min(ys), np.max(ys)

    return np.float32([
        [min_x, max_y],  # topo-esquerda
        [max_x, max_y],  # topo-direita
        [max_x, min_y],  # baixo-direita
        [min_x, min_y],  # baixo-esquerda
    ])