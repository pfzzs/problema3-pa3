# Problema 3 — Quando chove, por onde se chega à UBS?

Repositório da solução do Problema 3. Sistema que modela o bairro Vila Nova Esperança como um grafo dinâmico de pontos e trechos de rua, com operações de consulta de alcance, menor tempo, rota, UBS mais próxima, pontos isolados e trechos críticos, respeitando alagamentos que mudam a cada chuva.

## Integrantes

1. Nome: Igor Cunha — Matrícula: <matrícula>  
2. Nome: Isadora Amancio — Matrícula: <matrícula>  
3. Nome: Joaquim Ferreira — Matrícula: <matrícula>  
4. Nome: Pedro  — Matrícula: <matrícula>  

## Linguagem e versão

- Linguagem: Python
- Versão: Python 3.11

## Organização do repositório

```
executar.txt
README.md
alternativa/   <- versão descartada (implementada, medida e descartada)
final/         <- versão final
testes/        <- arquivos de carga e casos de teste
medicoes/
  medicoes.csv <- medições (separado por ponto e vírgula)
```

`executar.txt`: primeira linha = versão alternativa; segunda linha = versão final; terceira linha = versão final. Cada linha contém o comando de execução da respectiva versão. O histórico de commits faz parte da entrega, e cada integrante faz commits com o próprio usuário.

## Contrato de operações (entrada/saída)

O programa lê um arquivo com uma operação por linha e escreve uma resposta por operação na saída padrão. O tempo gasto é escrito na saída de erro como `TEMPO_MS valor`. Linhas em branco e iniciadas por `#` são ignoradas.

| Operação | Significado | Respostas possíveis |
|----------|-------------|---------------------|
| `PONTO codigo` ou `PONTO codigo UBS` | Cadastra ponto (opcionalmente porta de UBS) | `OK`, `DUPLICADO` |
| `TRECHO a b minutos` | Cadastra trecho bidirecional entre a e b | `OK`, `NAOEXISTE`, `INVALIDO`, `DUPLICADO` |
| `ALAGA a b` | Marca trecho como alagado | `OK`, `NAOEXISTE`, `JA` |
| `LIBERA a b` | Libera trecho alagado | `OK`, `NAOEXISTE`, `JA` |
| `PASSOS a b` | Menor número de trechos de a até b | inteiro, `SEMCAMINHO`, `NAOEXISTE` |
| `TEMPO a b` | Menor tempo de caminhada (minutos) | inteiro, `SEMCAMINHO`, `NAOEXISTE` |
| `ROTA a b` | Menor tempo + pontos do caminho | `tempo ponto ponto ...`, `SEMCAMINHO`, `NAOEXISTE` |
| `UBSPROX a` | UBS mais próxima de a | `codigo minutos`, `NENHUMA`, `NAOEXISTE` |
| `ISOLADOS` | Pontos sem caminho para nenhuma UBS | `k` seguido de k códigos, um por linha |
| `CRITICOS` (extra) | Trechos cuja remoção desconecta regiões alcançáveis | `k` seguido de k linhas `a b` |

Regras: `PASSOS` e `TEMPO` de um ponto para ele mesmo respondem `0`; `ROTA` responde `0` seguido do próprio ponto; `UBSPROX` de uma UBS responde a ela mesma com `0`. Códigos são comparados caractere por caractere. Até 12 caracteres por código; tempo é inteiro de minutos.

## Como compilar e executar

Veja `executar.txt` para os comandos exatos de cada versão. Exemplo genérico:

```sh
# versão alternativa
<comando-compilacao-alternativa>
<comando-execucao-alternativa> <arquivo-entrada>

# versão final
<comando-compilacao-final>
<comando-execucao-final> <arquivo-entrada>
```

## medicoes.csv

Cabeçalho e colunas: `arquivo;versao;execucao;tempo_ms;memoria_mb`. `versao` recebe `alternativa` ou `final`. Cada arquivo de carga é executado 3 vezes por versão; se não terminar em 5 minutos, registra-se `NAO_TERMINOU`.

## Método de medição de memória

- O que é medido: <descreva, ex. pico de memória residente do processo durante a execução das operações>
- Ferramenta: <descreva, ex. GetProcessMemoryInfo no Windows, /usr/bin/time -v, etc.>
- Momento da medição: <descreva, ex. após leitura completa do arquivo e antes de escrever respostas, ou pico durante toda a execução>
- O mesmo método é aplicado às duas versões (alternativa e final).

## Reutilização de código dos Problemas 1 e 2

<Descreva aqui o que foi reaproveitado, de qual problema e de qual grupo veio, e onde entra no código. Se nada foi reaproveitado, escreva "Nenhum código dos Problemas 1 e 2 foi reaproveitado.">
