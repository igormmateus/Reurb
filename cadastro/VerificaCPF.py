from random import randint


def verifica_cpf(cpf):
    if len(cpf) < 11 or len(cpf) > 14:
        return False

    cpf = limpa_cpf(cpf)
    cpf_novo = cpf[:-2]
    reverso = 10
    total = 0
    # print(cpf_novo)
    for index in range(19):  # contar as 19 iterações necessarias, 9 para o primeiro digito e 10 para o segundo
        if index > 8:  # recomeçar o valor do index para calcular o segundo digito
            index -= 9

        total += int(cpf_novo[index]) * reverso

        reverso -= 1
        if reverso < 2:  # quando o multiplicador chegar em 2 reinicia ele em 11
            reverso = 11
            d = 11 - (total % 11)
            if d > 9:
                d = 0
            total = 0
            cpf_novo += str(d)

    sequencia = cpf_novo == str(cpf_novo[0]) * len(cpf)

    if cpf == cpf_novo and not sequencia:
        return True
    else:
        return False


def gera_cpf():
    numero = randint(100000000, 999999999)
    cpf_novo = str(numero)
    reverso = 10
    total = 0

    for index in range(19):  # contar as 19 iterações necessarias, 9 para o primeiro digito e 10 para o segundo
        if index > 8:  # recomeçar o valor do index para calcular o segundo digito
            index -= 9

        total += int(cpf_novo[index]) * reverso

        reverso -= 1
        if reverso < 2:  # quando o multiplicador chegar em 2 reinicia ele em 11
            reverso = 11
            d = 11 - (total % 11)
            if d > 9:
                d = 0
            total = 0
            cpf_novo += str(d)
    return cpf_novo


def limpa_cpf(cpf):
    if len(cpf) > 11:
        cpf = cpf[0:3] + cpf[4:7] + cpf[8:11] + cpf[12:14]  # limpa o cpf deixando apenas os numeros
    return cpf


def imprime_cpf(cpf):
    return f'{cpf[0:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:11]}'
