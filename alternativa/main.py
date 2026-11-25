# -*- coding: utf-8 -*-
# Versao ALTERNATIVA (descartada) - Problema 3.
# Representacao por listas paralelas (vetores simples) sem estruturas prontas no nucleo.
# Recalcula buscas e ordena manualmente a cada consulta (lenta em cargas grandes).
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


# [R3] Cadastro de pontos (PONTO): cadastra ponto e preserva tipo UBS do primeiro cadastro
def op_ponto(parts, point_codes, point_is_ubs, out):
    code = parts[1]
    is_ubs = len(parts) >= 3 and parts[2] == "UBS"
    if find_point(point_codes, code) != -1:
        out.append("DUPLICADO")
    else:
        point_codes.append(code)
        point_is_ubs.append(is_ubs)
        out.append("OK")


# [R4] Cadastro de trechos (TRECHO): valida NAOEXISTE -> INVALIDO -> DUPLICADO e registra bidirecional
def op_trecho(parts, point_codes, edges_u, edges_v, edges_w, flooded, out):
    a_code, b_code = parts[1], parts[2]
    mins = int(parts[3])
    ai = find_point(point_codes, a_code)
    bi = find_point(point_codes, b_code)
    if ai == -1 or bi == -1:
        out.append("NAOEXISTE")
    elif a_code == b_code or mins <= 0:
        out.append("INVALIDO")
    elif find_edge(edges_u, edges_v, ai, bi) != -1:
        out.append("DUPLICADO")
    else:
        edges_u.append(ai)
        edges_v.append(bi)
        edges_w.append(mins)
        flooded.append(False)
        out.append("OK")


# [R5] Controle de alagamento (ALAGA e LIBERA): altera estado sem remover trecho do mapa
def op_alaga_libera(cmd, parts, point_codes, edges_u, edges_v, flooded, out):
    a_code, b_code = parts[1], parts[2]
    ai = find_point(point_codes, a_code)
    bi = find_point(point_codes, b_code)
    ei = find_edge(edges_u, edges_v, ai, bi) if ai != -1 and bi != -1 else -1
    if ei == -1:
        out.append("NAOEXISTE")
    elif cmd == "ALAGA":
        if flooded[ei]:
            out.append("JA")
        else:
            flooded[ei] = True
            out.append("OK")
    else:  # LIBERA
        if not flooded[ei]:
            out.append("JA")
        else:
            flooded[ei] = False
            out.append("OK")


# [R6] Consultas de caminho (PASSOS, TEMPO e ROTA) sobre trechos nao alagados
def op_caminho(cmd, parts, point_codes, edges_u, edges_v, edges_w, flooded, inf_val, out):
    a_code, b_code = parts[1], parts[2]
    ai = find_point(point_codes, a_code)
    bi = find_point(point_codes, b_code)
    if ai == -1 or bi == -1:
        out.append("NAOEXISTE")
        return
    if ai == bi:
        if cmd == "ROTA":
            out.append("0 " + a_code)
        else:
            out.append("0")
        return

    n = len(point_codes)
    m = len(edges_u)

    if cmd == "PASSOS":
        dist = [-1] * n
        q = [ai]
        dist[ai] = 0
        head = 0
        while head < len(q):
            u = q[head]
            head += 1
            if u == bi:
                break
            for ei in range(m):
                if flooded[ei]:
                    continue
                u2 = edges_u[ei]
                v2 = edges_v[ei]
                if u2 == u and dist[v2] == -1:
                    dist[v2] = dist[u] + 1
                    q.append(v2)
                elif v2 == u and dist[u2] == -1:
                    dist[u2] = dist[u] + 1
                    q.append(u2)
        if dist[bi] == -1:
            out.append("SEMCAMINHO")
        else:
            out.append(str(dist[bi]))

    else:  # TEMPO ou ROTA (Dijkstra manual)
        dist = [inf_val] * n
        prev = [-1] * n
        visited = [False] * n
        dist[ai] = 0

        for _ in range(n):
            u = -1
            best_d = inf_val
            for i in range(n):
                if not visited[i] and dist[i] < best_d:
                    best_d = dist[i]
                    u = i
            if u == -1 or u == bi:
                break
            visited[u] = True

            for ei in range(m):
                if flooded[ei]:
                    continue
                u2 = edges_u[ei]
                v2 = edges_v[ei]
                w = edges_w[ei]
                v = -1
                if u2 == u:
                    v = v2
                elif v2 == u:
                    v = u2
                if v != -1 and not visited[v]:
                    nd = dist[u] + w
                    if nd < dist[v]:
                        dist[v] = nd
                        prev[v] = u

        if dist[bi] == inf_val:
            out.append("SEMCAMINHO")
        elif cmd == "TEMPO":
            out.append(str(dist[bi]))
        else:
            path = []
            cur = bi
            while cur != -1:
                path.append(point_codes[cur])
                cur = prev[cur]
            path.reverse()
            out.append(str(dist[bi]) + " " + " ".join(path))


# [R7] Busca da UBS mais proxima (UBSPROX): menor tempo e desempate por menor codigo
def op_ubsprox(parts, point_codes, point_is_ubs, edges_u, edges_v, edges_w, flooded, inf_val, out):
    a_code = parts[1]
    ai = find_point(point_codes, a_code)
    if ai == -1:
        out.append("NAOEXISTE")
        return
    if point_is_ubs[ai]:
        out.append(a_code + " 0")
        return

    n = len(point_codes)
    m = len(edges_u)
    dist = [inf_val] * n
    visited = [False] * n
    dist[ai] = 0

    for _ in range(n):
        u = -1
        best_d = inf_val
        for i in range(n):
            if not visited[i] and dist[i] < best_d:
                best_d = dist[i]
                u = i
        if u == -1:
            break
        visited[u] = True

        for ei in range(m):
            if flooded[ei]:
                continue
            u2 = edges_u[ei]
            v2 = edges_v[ei]
            w = edges_w[ei]
            v = -1
            if u2 == u:
                v = v2
            elif v2 == u:
                v = u2
            if v != -1 and not visited[v]:
                nd = dist[u] + w
                if nd < dist[v]:
                    dist[v] = nd

    best_idx = -1
    for i in range(n):
        if point_is_ubs[i] and dist[i] < inf_val:
            if (
                best_idx == -1
                or dist[i] < dist[best_idx]
                or (
                    dist[i] == dist[best_idx]
                    and point_codes[i] < point_codes[best_idx]
                )
            ):
                best_idx = i

    if best_idx == -1:
        out.append("NENHUMA")
    else:
        out.append(point_codes[best_idx] + " " + str(dist[best_idx]))


# [R8] Identificacao de pontos isolados (ISOLADOS): sem caminho ate nenhuma UBS
def op_isolados(point_codes, point_is_ubs, edges_u, edges_v, flooded, out):
    n = len(point_codes)
    m = len(edges_u)
    reached = [False] * n
    q = []
    for i in range(n):
        if point_is_ubs[i]:
            reached[i] = True
            q.append(i)

    head = 0
    while head < len(q):
        u = q[head]
        head += 1
        for ei in range(m):
            if flooded[ei]:
                continue
            u2 = edges_u[ei]
            v2 = edges_v[ei]
            if u2 == u and not reached[v2]:
                reached[v2] = True
                q.append(v2)
            elif v2 == u and not reached[u2]:
                reached[u2] = True
                q.append(u2)

    isolated_codes = []
    for i in range(n):
        if not reached[i]:
            isolated_codes.append(point_codes[i])
    isolated_codes = sort_strings(isolated_codes)

    out.append(str(len(isolated_codes)))
    for c in isolated_codes:
        out.append(c)


# [R9] Trechos criticos (CRITICOS - opcional): pontes no subgrafo nao alagado
def op_criticos(point_codes, edges_u, edges_v, flooded, out):
    n = len(point_codes)
    m = len(edges_u)
    adj = [[] for _ in range(n)]
    for ei in range(m):
        if flooded[ei]:
            continue
        u = edges_u[ei]
        v = edges_v[ei]
        adj[u].append(v)
        adj[v].append(u)

    disc = [-1] * n
    low = [0] * n
    visited = [False] * n
    bridges = []
    timer = [0]

    def dfs(u, parent):
        visited[u] = True
        disc[u] = timer[0]
        low[u] = timer[0]
        timer[0] += 1
        for v in adj[u]:
            if not visited[v]:
                dfs(v, u)
                if low[v] < low[u]:
                    low[u] = low[v]
                if low[v] > disc[u]:
                    ca = point_codes[u]
                    cb = point_codes[v]
                    if cb < ca:
                        ca, cb = cb, ca
                    bridges.append((ca, cb))
            elif v != parent:
                if disc[v] < low[u]:
                    low[u] = disc[v]

    for i in range(n):
        if not visited[i]:
            dfs(i, -1)

    pairs = sort_pairs(bridges)
    out.append(str(len(pairs)))
    for a, b in pairs:
        out.append(a + " " + b)


if __name__ == "__main__":
    main()