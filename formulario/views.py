from django.shortcuts import render
from docx import Document
from rest_framework.views import APIView
from django.http import StreamingHttpResponse
from cadastro.VerificaCPF import imprime_cpf
import io
from django.shortcuts import get_object_or_404
from cadastro.models import PreCadastroImovel, Conjuge
from reurb.bibliotecas.formulario import convertDate, escolha, limpa_telefone



class ExportDocx(APIView):
    def get(self, request, pk):
        # nome, cpf, telefone, logradouro, quadra, lote, bairro, estado_civil, profissao1, profissao2):
        document = Document('formulario/requerimento.docx')
        imovel = get_object_or_404(PreCadastroImovel, id=pk)
        if imovel.proprietario.estado_civil == 'C':
            conjugue = get_object_or_404(Conjuge, nome=imovel.proprietario.id)
            profissaoC = conjugue.profissao
        else:
            profissaoC = ''

        cpf = imprime_cpf(imovel.proprietario.cpf)

        dia, mes, ano = convertDate(imovel.data_cadastro)

        estado_civil = escolha(imovel.proprietario.opcao_estado_civil,imovel.proprietario.estado_civil)

        referencias = {
            'Nome.benefiario': imovel.proprietario.nome,
            'cpf.beneficiario': cpf,
            '(62) telefone.beneficiario': imovel.proprietario.telefone,
            'rua.beneficiario': imovel.logradouro,
            'qd.beneficiario': imovel.quadra,
            'lt.beneficiario': imovel.lote,
            'bairro.beneficiario': imovel.bairro.bairro,



        }

        referencias2 = {
            'estado_civil.beneficiario': estado_civil,
            'profissão.beneficiario': imovel.proprietario.profissao,
            'profissão.conjugue': profissaoC,
            'dia': dia,
            'mes': mes,
            'ano': ano,
        }

        for paragrafo in document.paragraphs:
            for codigo in referencias:
                paragrafo.text = paragrafo.text.replace(codigo, referencias[codigo].upper())
            for codigo in referencias2:
                paragrafo.text = paragrafo.text.replace(codigo, referencias2[codigo])

            if profissaoC == '':
                paragrafo.text = paragrafo.text.replace('OCUPAÇÃO DO CONJUGE:', '')
        buffer = io.BytesIO()
        document.save(buffer)
        buffer.seek(0)
        resposta = StreamingHttpResponse(
            streaming_content=buffer,
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        resposta['Content-Disposition'] = f'attachment;Filename=Requerimento - {imovel.proprietario.nome}.docx'
        resposta['Content-Encoding'] = 'UTF-8'

        return resposta




