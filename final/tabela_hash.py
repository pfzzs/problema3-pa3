# Tabela hash propria: mapeia o codigo de um ponto (string) para o seu
# indice interno (inteiro). Substitui o dict do Python, proibido no nucleo.
#
# Tecnica: enderecamento aberto com sondagem linear.
#   - Os dados ficam em dois vetores simples: chaves[] e valores[].
#   - A funcao hash percorre o codigo caractere a caractere.
#   - Se a posicao calculada estiver ocupada, tenta a seguinte (circular).
#   - Quando a ocupacao passa de 70%, a tabela dobra de tamanho e
#     todas as chaves sao reinseridas (redimensionamento).
#
# Custo: buscar e inserir sao O(1) em media; o redimensionamento e O(n),
# mas acontece cada vez mais raramente (custo amortizado O(1)).

CAPACIDADE_INICIAL = 16      # sempre potencia de 2 (permite usar & no lugar de %)
CARGA_MAXIMA_NUM = 7         # ocupacao maxima = 7/10 = 70%
CARGA_MAXIMA_DEN = 10
NAO_ENCONTRADO = -1


def calcular_hash(texto):
    # Hash polinomial: h = h * 31 + codigo_do_caractere, para cada caractere.
    # O "& 0x7FFFFFFF" limita o numero a 31 bits para ele nao crescer sem fim.
    h = 0
    for c in texto:
        h = (h * 31 + ord(c)) & 0x7FFFFFFF
    return h


class TabelaHash:
    def __init__(self, capacidade=CAPACIDADE_INICIAL):
        self.capacidade = capacidade
        self.tamanho = 0                      # quantas chaves estao guardadas
        self.chaves = [None] * capacidade     # None = posicao livre
        self.valores = [0] * capacidade

    def _posicao(self, chave):
        # Devolve a posicao onde a chave esta OU a posicao livre onde ela
        # deveria entrar. capacidade - 1 funciona como mascara porque a
        # capacidade e potencia de 2 (equivale a hash % capacidade).
        mascara = self.capacidade - 1
        i = calcular_hash(chave) & mascara
        chaves = self.chaves
        while chaves[i] is not None and chaves[i] != chave:
            i = (i + 1) & mascara             # sondagem linear
        return i

    def buscar(self, chave):
        # Devolve o valor associado a chave, ou NAO_ENCONTRADO (-1).
        i = self._posicao(chave)
        if self.chaves[i] is None:
            return NAO_ENCONTRADO
        return self.valores[i]

    def inserir(self, chave, valor):
        # Insere a chave se ela ainda nao existe.
        # Devolve True se inseriu, False se a chave ja estava na tabela
        # (nesse caso o valor antigo e mantido).
        i = self._posicao(chave)
        if self.chaves[i] is not None:
            return False
        self.chaves[i] = chave
        self.valores[i] = valor
        self.tamanho += 1
        if self.tamanho * CARGA_MAXIMA_DEN > self.capacidade * CARGA_MAXIMA_NUM:
            self._redimensionar()
        return True

    def _redimensionar(self):
        # Dobra a capacidade e reinsere tudo (as posicoes mudam porque
        # dependem da capacidade).
        chaves_antigas = self.chaves
        valores_antigos = self.valores
        self.capacidade *= 2
        self.chaves = [None] * self.capacidade
        self.valores = [0] * self.capacidade
        for j in range(len(chaves_antigas)):
            if chaves_antigas[j] is not None:
                i = self._posicao(chaves_antigas[j])
                self.chaves[i] = chaves_antigas[j]
                self.valores[i] = valores_antigos[j]
