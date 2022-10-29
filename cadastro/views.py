from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Value
from django.db.models.functions import Concat
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from reurb.bibliotecas.formulario import escolha
from .VerificaCPF import limpa_cpf, verifica_cpf
from reurb.bibliotecas.formulario import limpa_telefone
from django.contrib.auth.models import User


from .models import Formprecadastro, Formcadastropessoa, Formconjugue, PreCadastroImovel, CadastroPessoa, Conjuge



@login_required(redirect_field_name='index_login')
def index(request):
    imoveis = PreCadastroImovel.objects.order_by('bairro').exclude(
        status='A' or 'S' or 'R'
    )
    return render(request, 'cadastro/index.html', {
        'imoveis': imoveis
    })


@login_required(redirect_field_name='index_login')
def ver_imovel(request, imovel_id):
    imovel = get_object_or_404(PreCadastroImovel, id=imovel_id)
    status = escolha(imovel.opcao_status,imovel.status)
    return render(request, 'cadastro/ver_imovel.html', {
        'imovel': imovel, 'status' : status
    })


@login_required(redirect_field_name='index_login')
def busca(request):
    termo = request.GET.get('termo')
    qdlt = Concat('quadra', Value('/'), 'lote')
    imoveis = PreCadastroImovel.objects.annotate(
        quadralote=qdlt
    ).filter(
        quadralote__icontains=termo
    ).exclude(
        status='A' or 'S' or 'R'
    )
    return render(request, 'cadastro/busca.html', {
        'imoveis': imoveis
    })


@login_required(redirect_field_name='index_login')
def precadastro(request):
    titulares = CadastroPessoa.objects.order_by('id')

    if request.method != 'POST':
        form = Formprecadastro()
        return render(request, 'cadastro/precadastro.html', {'form': form, 'titulares': titulares})

    form = Formprecadastro(request.POST)
    if not form.is_valid():
        form = Formprecadastro(request.POST)
        return render(request, 'cadastro/precadastro.html', {'form': form, 'titulares': titulares})

    imovel = PreCadastroImovel(**form.cleaned_data)

    slug = f'{imovel.logradouro}-{imovel.quadra}/{imovel.lote}'
    imovel.slug = slug

    imovelexiste = PreCadastroImovel.objects.filter(
        slug__icontains=slug)

    if imovelexiste:
        messages.add_message(request, messages.ERROR, 'Imovel ja cadastrado')
        form = Formprecadastro(request.POST)
        return render(request, 'cadastro/precadastro.html', {'form': form, 'titulares': titulares})

    titular = get_object_or_404(CadastroPessoa, id=request.POST.get('proprietario'))
    if titular.estado_civil == 'C' or titular.estado_civil == 'U':
        conjugue = get_object_or_404(Conjuge, titular=request.POST.get('proprietario'))
    imovel.proprietario = titular
    imovel.usuario = request.user
    observacao = ''
    if titular.profissao == 'não declarado':
        observacao += 'falta profissão do(a) titular. \n'
        imovel.status = 'P'
    if titular.estado_civil == 'C' or titular.estado_civil == 'U':
        conjugue = get_object_or_404(Conjuge, titular=request.POST.get('proprietario'))
        if conjugue.profissao_conj == 'não declarado':
            observacao += 'falta profissão do(a) conjugue'
            imovel.status = 'P'
    imovel.observacao = observacao

    imovel.save()

    return redirect('cadastro_beneficiario')


@login_required(redirect_field_name='index_login')
def cadastro_beneficiario(request):
    if request.method != 'POST':
        form = Formcadastropessoa()
        return render(request, 'cadastro/cadastro_beneficiario.html', {'form': form})

    form = Formcadastropessoa(request.POST)

    if not form.is_valid():
        messages.add_message(request, messages.ERROR, 'Formulário invalido!')
        form = Formcadastropessoa(request.POST)
        return render(request, 'cadastro/cadastro_beneficiario.html', {'form': form})

    cpf = request.POST.get('cpf')
    if not verifica_cpf(cpf):
        messages.add_message(request, messages.ERROR, 'CPF invalido!')
        form = Formcadastropessoa(request.POST)
        return render(request, 'cadastro/cadastro_beneficiario.html', {'form': form})

    # form.save()

    estado_civil = request.POST.get('estado_civil')
    titular = CadastroPessoa(**form.cleaned_data)
    if not request.POST.get('profissao'):
        titular.profissao = 'não declarado'
    # titular = get_object_or_404(CadastroPessoa, cpf=request.POST.get('cpf'))
    if not limpa_telefone(request.POST.get('telefone')):
        messages.add_message(request, messages.ERROR, 'telefone incorreto')
        form = Formcadastropessoa(request.POST)
        return render(request, 'cadastro/cadastro_beneficiario.html', {'form': form})
    else:
        titular.telefone = limpa_telefone(request.POST.get('telefone'))

    titular.cpf = limpa_cpf(request.POST.get('cpf'))
    titular.save()

    if estado_civil == 'C':
        return redirect('conjugue', pk=titular.id)

    return redirect('precadastro')


# @login_required(redirect_field_name='index_login')
class CadastroConjugue(UpdateView):
    template_name = 'cadastro/conjugue.html'
    model = CadastroPessoa
    form_class = Formconjugue
    context_object_name = 'Titular'

    def form_valid(self, form):
        titular = self.get_object()
        conjugue = Conjuge(**form.cleaned_data)
        conjugue.titular = titular
        conjugue.cpf_conj = limpa_cpf(conjugue.cpf_conj)
        if not self.request.POST.get('profissao_conj'):
            conjugue.profissao_conj = 'não declarado'

        conjugue.save()
        return redirect('precadastro')
