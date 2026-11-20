def cadastrar_ponto(mapa_pontos, codigo, eh_ubs=False):
    #FUNÇAO 1: Cadastrar um ponto no mapa

    if codigo is None or " " in codigo or len(codigo) == 0 or len(codigo) > 12:
        raise ValueError("Código de ponto inválido: deve ter de 1 a 12 caracteres sem espaços.")

    if codigo in mapa_pontos:
        return "DUPLICADO"

    mapa_pontos[codigo] = {
        "codigo": codigo,
        "eh_ubs": bool(eh_ubs),
    }
    return "OK"
