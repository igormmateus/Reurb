def convertDate(data):
    dia = str(data.day)
    mes = str(data.month)
    meses = {
        '1': 'janeiro',
        '2': 'fevereiro',
        '3': 'março',
        '4': 'abril',
        '5': 'maio',
        '6': 'junho',
        '7': 'julho',
        '8': 'agosto',
        '9': 'setembro',
        '10': 'outubro',
        '11': 'novembro',
        '12': 'dezembro',
    }
    for m in meses:
        if m == mes:
            mes = meses[m]

    ano = str(data.year)

    return dia, mes, ano


def escolha(opcoes, escolha):
    for opcao in opcoes:
        if opcao[0] == escolha:
            return opcao[1]


def limpa_telefone(telefone):
    telefone = telefone.replace('-', '')
    telefone = telefone.replace(' ', '')
    telefone = telefone.replace('(', '')
    telefone = telefone.replace(')', '')
    if len(telefone) != 11:
        return False
    else:
        return f'({telefone[0:2]}) {telefone[2:7]}-{telefone[7:12]} '
