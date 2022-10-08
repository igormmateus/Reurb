from django.shortcuts import render
from docx import Document
from rest_framework.views import APIView
from django.http import StreamingHttpResponse
from cadastro.VerificaCPF import imprime_cpf
import io
from django.shortcuts import get_object_or_404
from cadastro.models import PreCadastroImovel, CadastroPessoa, Conjuge


class ExportDocx(APIView):
    def get(self, request, pk):
        # nome, cpf, telefone, logradouro, quadra, lote, bairro, estado_civil, profissao1, profissao2):
        document = Document('formulario/Requerimento.docx')
        imovel = get_object_or_404(PreCadastroImovel, id=pk)
        proprietario = get_object_or_404(CadastroPessoa, nome=imovel.proprietario)

        cpf = imprime_cpf(proprietario.cpf)
        referencias = {
            'Nome.benefiario': proprietario.nome,
            'cpf.beneficiario': cpf,
            'telefone.beneficiario': proprietario.telefone,
            'rua.beneficiario': imovel.logradouro,
            'qd.beneficiario': imovel.quadra,
            'lt.beneficiario': imovel.lote,
            'bairro.beneficiario': imovel.bairro.bairro,
            'estado_civil.beneficiario': proprietario.estado_civil,
            'profissão.beneficiario': proprietario.profissao,
            # 'profissão.conjugue': profissao2,

        }

        for paragrafo in document.paragraphs:
            for codigo in referencias:
                paragrafo.text = paragrafo.text.replace(codigo, referencias[codigo].upper())
        buffer = io.BytesIO()
        document.save(buffer)
        buffer.seek(0)
        resposta = StreamingHttpResponse(
            streaming_content=buffer,
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
        resposta['Content-Disposition'] = f'attachment;Filename=Requerimento - {proprietario.nome}.docx'
        resposta['Content-Encoding'] = 'UTF-8'

        return resposta

