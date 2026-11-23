# -*- coding: utf-8 -*-
# Versao ALTERNATIVA (descartada) - Problema 3.
import sys
import time

sys.setrecursionlimit(1000000)


# [R1] Leitura do arquivo, filtragem de linhas, execucao e medicao de tempo
def main():
    if len(sys.argv) < 2:
        print("usage: main.py <input>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    ops = []
    for s in lines:
        s = s.strip()
        if s and not s.startswith("#"):
            ops.append(s)

    t0 = time.perf_counter()

    # Vetores simples que armazenam o estado do bairro
    point_codes = []
    point_is_ubs = []
    edges_u = []
    edges_v = []
    edges_w = []
    flooded = []

    out = []
    inf_val = float("inf")

    for op in ops:
        parts = op.split()
        cmd = parts[0]

        if cmd == "PONTO":
            op_ponto(parts, point_codes, point_is_ubs, out)
        elif cmd == "TRECHO":
            op_trecho(parts, point_codes, edges_u, edges_v, edges_w, flooded, out)
        elif cmd in ("ALAGA", "LIBERA"):
            op_alaga_libera(cmd, parts, point_codes, edges_u, edges_v, flooded, out)
        elif cmd in ("PASSOS", "TEMPO", "ROTA"):
            op_caminho(cmd, parts, point_codes, edges_u, edges_v, edges_w, flooded, inf_val, out)
        elif cmd == "UBSPROX":
            op_ubsprox(parts, point_codes, point_is_ubs, edges_u, edges_v, edges_w, flooded, inf_val, out)
        elif cmd == "ISOLADOS":
            op_isolados(point_codes, point_is_ubs, edges_u, edges_v, flooded, out)
        elif cmd == "CRITICOS":
            op_criticos(point_codes, edges_u, edges_v, flooded, out)
        else:
            out.append("")

    t1 = time.perf_counter()
    sys.stdout.write("\n".join(out) + ("\n" if out else ""))
    sys.stderr.write("TEMPO_MS %d\n" % int((t1 - t0) * 1000))


# [R2] Estruturas de dados em vetores simples e auxiliares manuais do nucleo
def find_point(point_codes, code):
    for i in range(len(point_codes)):
        if point_codes[i] == code:
            return i
    return -1


def find_edge(edges_u, edges_v, a, b):
    for ei in range(len(edges_u)):
        u = edges_u[ei]
        v = edges_v[ei]
        if (u == a and v == b) or (u == b and v == a):
            return ei
    return -1


def sort_strings(arr):
    a = arr[:]
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            tmp = a[i]
            a[i] = a[min_idx]
            a[min_idx] = tmp
    return a


def sort_pairs(arr):
    a = arr[:]
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if a[j][0] < a[min_idx][0] or (
                a[j][0] == a[min_idx][0] and a[j][1] < a[min_idx][1]
            ):
                min_idx = j
        if min_idx != i:
            tmp = a[i]
            a[i] = a[min_idx]
            a[min_idx] = tmp
    return a


