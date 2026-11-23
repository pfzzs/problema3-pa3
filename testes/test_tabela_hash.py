# Testes da tabela hash e do cadastro de pontos.
# Uso: python testes/test_tabela_hash.py
#
# Codigo de teste esta fora do nucleo, entao aqui PODE usar dict/random:
# o dict serve de "gabarito" para conferir a tabela hash propria.

import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "final"))

from tabela_hash import TabelaHash, NAO_ENCONTRADO  # noqa: E402
from grafo import Grafo  # noqa: E402


def teste_basico():
    t = TabelaHash()
    assert t.buscar("A") == NAO_ENCONTRADO
    assert t.inserir("A", 0) is True
    assert t.inserir("B", 1) is True
    assert t.inserir("A", 99) is False          # duplicado nao sobrescreve
    assert t.buscar("A") == 0
    assert t.buscar("B") == 1
    assert t.buscar("C") == NAO_ENCONTRADO
    assert t.tamanho == 2


def teste_maiusculas_e_minusculas_sao_diferentes():
    t = TabelaHash()
    t.inserir("ubs1", 0)
    t.inserir("UBS1", 1)
    assert t.buscar("ubs1") == 0
    assert t.buscar("UBS1") == 1


def teste_redimensionamento_com_gabarito():
    # Insere 50 mil codigos aleatorios (forca varios redimensionamentos)
    # e compara tudo com um dict.
    random.seed(42)
    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"
    t = TabelaHash()
    gabarito = {}
    for i in range(50000):
        codigo = "".join(random.choice(letras) for _ in range(random.randint(1, 12)))
        inseriu = t.inserir(codigo, i)
        assert inseriu == (codigo not in gabarito)
        if inseriu:
            gabarito[codigo] = i
    assert t.tamanho == len(gabarito)
    for codigo, valor in gabarito.items():
        assert t.buscar(codigo) == valor
    assert t.buscar("NAOEXISTE123") == gabarito.get("NAOEXISTE123", NAO_ENCONTRADO)


def teste_ponto():
    g = Grafo()
    assert g.adicionar_ponto("CASA1", False) == "OK"
    assert g.adicionar_ponto("UBS_A", True) == "OK"
    assert g.adicionar_ponto("UBS_A", False) == "DUPLICADO"
    assert g.adicionar_ponto("CASA1", True) == "DUPLICADO"
    assert g.num_pontos == 2
    assert g.eh_ubs[g.indice_de("UBS_A")] is True    # mantem o 1o cadastro
    assert g.eh_ubs[g.indice_de("CASA1")] is False
    assert g.indice_de("XYZ") == -1


if __name__ == "__main__":
    testes = [teste_basico, teste_maiusculas_e_minusculas_sao_diferentes,
              teste_redimensionamento_com_gabarito, teste_ponto]
    for teste in testes:
        teste()
        print("ok  ", teste.__name__)
    print("todos os %d testes passaram" % len(testes))
