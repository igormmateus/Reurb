from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')

    user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.error(request, 'Usuário ou senha inválidos.')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user)
        messages.success(request, 'Login feito com sucesso.')
        return redirect('cadastro_usuario')


def cadastro_usuario(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method != 'POST':
        return render(request, 'accounts/cadastro_usuario.html')

    nome = request.POST.get('nome')
    sobrenome = request.POST.get('sobrenome')
    email = request.POST.get('email')
    usuario = request.POST.get('usuario')
    senha = request.POST.get('senha')
    senha2 = request.POST.get('senha2')

    if not nome or not sobrenome or not email or not usuario or not senha or not senha2:
        messages.error(request, 'Nenhum Campo pode estar vazio')
        return render(request, 'accounts/cadastro_usuario.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'Email inválido')
        return render(request, 'accounts/cadastro_usuario.html')

    if len(senha) < 6:
        messages.error(request, 'Senha muito curta, minimo 6 caracteres')
        return render(request, 'accounts/cadastro_usuario.html')

    if User.objects.filter(username=usuario).exists():
        messages.error(request, 'Usuario ja cadastrado')
        return render(request, 'accounts/cadastro_usuario.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, 'Usuario ja cadastrado')
        return render(request, 'accounts/cadastro_usuario.html')

    if senha != senha2:
        messages.error(request, 'Senhas diferentes.')
        return render(request, 'accounts/cadastro_usuario.html')

    messages.success(request, 'Cadastro feito com sucesso')
    user = User.objects.create_user(username=usuario, email=email,
                                    password=senha, first_name=nome,
                                    last_name=sobrenome)
    user.save()
    return redirect('index_login')


@login_required(redirect_field_name='index_login')
def dashboard(request):
    return render(request, 'cadastro/index.html')
    # return redirect('cadastro/index.html')


def logout(request):
    auth.logout(request)
    return redirect('dashboard')
