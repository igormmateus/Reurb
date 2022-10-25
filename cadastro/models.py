from django.db import models
from django.utils import timezone
from django import forms
from django.contrib.auth.models import User
from .VerificaCPF import verifica_cpf


class CadastroPessoa(models.Model):
    opcao_estado_civil = (
        ('C', 'Casado(a)'),
        ('S', 'Solteiro(a)'),
        ('V', 'Viuvo(a)'),
        ('D', 'Divorciada(a)'),

    )
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=30)
    orgao_rg = models.CharField(max_length=10)
    estado_rg = models.CharField(max_length=2)
    nome_pai = models.CharField(max_length=255)
    nome_mae = models.CharField(max_length=255)
    telefone = models.CharField(max_length=15)
    profissao = models.CharField(max_length=50)
    estado_civil = models.CharField(max_length=1, choices=opcao_estado_civil)

    def __str__(self):
        return self.nome


class Conjuge(models.Model):
    nome_conj = models.CharField(max_length=255)
    cpf_conj = models.CharField(max_length=14, unique=True)
    rg_conj = models.CharField(max_length=30)
    orgao_rg_conj = models.CharField(max_length=10)
    estado_rg_conj = models.CharField(max_length=2)
    nome_pai_conj = models.CharField(max_length=255)
    nome_mae_conj = models.CharField(max_length=255)
    profissao_conj = models.CharField(max_length=50)
    titular = models.ForeignKey(CadastroPessoa, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome_conj


class Bairro(models.Model):
    bairro = models.CharField(max_length=30)

    def __str__(self):
        return self.bairro


class PreCadastroImovel(models.Model):
    opcao_status = (
        ('I', 'Iniciado'),
        ('E', 'Enviado para cartorio'),
        ('M', 'Medição'),
        ('S', 'Suspenso'),
        ('A', 'Arquivado'),
        ('G', 'Aguardando registro'),
        ('R', 'Registrado'),

    )


    logradouro = models.CharField(max_length=100)
    quadra = models.CharField(max_length=3)
    lote = models.CharField(max_length=3)
    bairro = models.ForeignKey(Bairro, on_delete=models.DO_NOTHING, null=True)
    proprietario = models.ForeignKey(CadastroPessoa, on_delete=models.CASCADE)
    data_cadastro = models.DateField(auto_now_add=True)
    medicao = models.CharField(max_length=10, blank=True)
    cartorio = models.CharField(max_length=10, blank=True)
    conferido = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=1, choices=opcao_status, default='I')
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=4)

    observacao = models.TextField(blank=True)


class Formcadastropessoa(forms.ModelForm):
    class Meta:
        model = CadastroPessoa
        exclude = ()


class Formprecadastro(forms.ModelForm):
   class Meta:
        model = PreCadastroImovel

        exclude = ('data_cadastro', 'medicao', 'cartorio', 'conferido', 'status', 'proprietario', 'usuario')


class Formconjugue(forms.ModelForm):
    def clean(self):
        data = self.cleaned_data
        cpf = data.get('cpf_conj')
        if not verifica_cpf(cpf):
            self.add_error(
                'cpf_conj',
                'CPF inválido'
            )
    class Meta:
        model = Conjuge
        exclude = ('titular',)
