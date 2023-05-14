from django.shortcuts import render
from django.http import HttpResponse
from . models import Usuario
from django.shortcuts import redirect
from hashlib import sha256

def login (request):
    if request.session.get('usuario'):
        redirect('/livro/home/')
    status = request.GET.get('status')
    return render(request, 'login.html', {'status': status})


def cadastro (request):
    if request.session.get('usuario'):
        redirect('/livro/home/')
    status = request.GET.get('status')                            #qdo renderizar pego os status que serão gerados pela def valida_cadastro()
    return render(request, 'cadastro.html', {'status': status})   #crio dict com chave 'status' e o valor é o que o GET pegou, uso essa chave no front


def valida_cadastro(request):
    nome = request.POST.get('nome')                           #recebe os dados do front pelo name -> url > view(def) correspondente > chega aqui
    senha = request.POST.get('senha')
    email = request.POST.get('email')

    usuario = Usuario.objects.filter(email = email)           # instancia e compara valor receb do front com o b.dados

    if len(nome.strip()) == 0 or len(email.strip()) == 0:     #strip() verifica -> se string vazia retorna 0
        return redirect('/auth/cadastro/?status=1')
    
    if len(senha) < 8:
        return redirect('/auth/cadastro/?status=2')

    if len(usuario) > 0:                                      # se 1, verdadeiro, ja tem cadastro 
        return redirect('/auth/login/?status=3')              # então retorna login
    
    try:
        senha = sha256(senha.encode()).hexdigest()
        usuario = Usuario(nome = nome,                        #senão, instancie novo obj (cria cadastro)
                          senha = senha, 
                          email = email) 
        usuario.save()                                        #salve no BD
        return redirect('/auth/login/')
    
    except:
        redirect('/auth/login/')                  #n faz nada e redireciona p login

    return HttpResponse(f"{nome} {senha} {email}")


def valida_login(request):
    email = request.POST.get('email')
    senha = request.POST.get('senha')

    senha = sha256(senha.encode()).hexdigest()

    usuario = Usuario.objects.filter(email = email).filter(senha = senha)

    if len(usuario) == 0:
       return redirect('/auth/login/?status=1')
    elif len(usuario) > 0:
        request.session['usuario'] = usuario[0].id
        return redirect(f'/livro/home/?id_usuario={request.session["usuario"]}')

    return HttpResponse(f"{email} {senha}")
 

def sair(request):
    request.session.flush()
    return redirect('/auth/login')