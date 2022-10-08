from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Value
from django.db.models.functions import Concat
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView

from .models import Formprecadastro, Formcadastropessoa, Formconjugue, PreCadastroImovel, CadastroPessoa, Conjuge
from .VerificaCPF import verifica_cpf


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
    return render(request, 'cadastro/ver_imovel.html', {
        'imovel': imovel
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

    titular = get_object_or_404(CadastroPessoa, id=request.POST.get('proprietario'))
    imovel.proprietario = titular


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

    form.save()

    estado_civil = request.POST.get('estado_civil')
    titular = get_object_or_404(CadastroPessoa, nome=request.POST.get('nome'))

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

        conjugue.save()
        return redirect('precadastro')

    # def conjugue(request):
    #     # titular = get_object_or_404(CadastroPessoa)
    #     # print(titular)
    #     if request.method != 'POST':
    #         form = Formconjugue()
    #         return render(request, 'cadastro/conjugue.html', {
    #             'form': form
    #         })
    #     form = Formconjugue(request.POST)
    #     titular = CadastroPessoa(**form.cleaned_data)
    #     print('O titular é: ' + titular)
    #
    #
    #     if not form.is_valid():
    #         form = Formconjugue(request.POST)
    #         return render(request, 'cadastro/conjugue.html', {
    #             'form': form,
    #         })
    #
    #     form.save()
    #     messages.add_message(request, messages.SUCCESS, 'cadastro feito!')
    #     return redirect('precadastro')
