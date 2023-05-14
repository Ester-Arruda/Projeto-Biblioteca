from datetime import date, datetime
from django.shortcuts import redirect, render
from django.http import HttpResponse
from usuarios.models import Usuario
from .models import Livros, Categoria, Emprestimos
from .forms import CadastroLivro, CategoriaLivro
from django import forms
from django.db.models import Q


def home(request):
    if request.session.get('usuario'):
        usuario = Usuario.objects.get(id = request.session['usuario'])
        status_categoria = request.GET.get('cadastro_categoria')
        livros = Livros.objects.filter(usuario = usuario)           #pega todos os livros do usuario logado
        total_livros = livros.count()
        form = CadastroLivro()  #vem de forms.py
        form.fields['usuario'].initial = request.session['usuario'] #pega campo usuario q está hidden e define o value como ID do user
        form.fields['categoria'].queryset = Categoria.objects.filter(usuario = usuario) # user logado igual ao user da tabela de categoria
        form_categoria = CategoriaLivro()
        usuarios = Usuario.objects.all()  #traga todos os usuarios existentes

        livros_emprestar = Livros.objects.filter(usuario = usuario).filter(emprestado = False)
        livros_emprestados = Livros.objects.filter(usuario = usuario).filter(emprestado = True)
        
        return render(request, 'home.html', {'livros': livros,
                                             'usuario':usuario,
                                             'usuario_logado':request.session.get('usuario'),
                                             'form': form,
                                             'status_categoria': status_categoria,
                                             'form_categoria': form_categoria,
                                             'usuarios': usuarios,
                                             'livros_emprestar': livros_emprestar,
                                             'total_livros': total_livros,
                                             'livros_emprestados': livros_emprestados})
    else:
        return redirect('/auth/login/?status=2')


def ver_livros(request, id):             #chamada qdo quer ver infods do livro
    if request.session.get('usuario'):   #se user logado
        livro = Livros.objects.get(id = id)   #pega no banco o id que é igual o id da requi - do livro
        if request.session.get('usuario') == livro.usuario.id:  #id do user da req == ao id do user do livro
            usuario = Usuario.objects.get(id = request.session['usuario'])
            categoria_livro = Categoria.objects.filter(usuario = request.session.get('usuario'))
            emprestimos = Emprestimos.objects.filter(livro = livro)
            form = CadastroLivro()
            form.fields['usuario'].initial = request.session['usuario'] #pega campo usuario q está hidden e define o value como ID do user
            form.fields['categoria'].queryset = Categoria.objects.filter(usuario = usuario) # user logado igual ao user da tabela de categoria

            form_categoria = CategoriaLivro()
            usuarios = Usuario.objects.all()  #traga todos os usuarios

            livros_emprestar = Livros.objects.filter(usuario = usuario).filter(emprestado = False)
            livros_emprestados = Livros.objects.filter(usuario = usuario).filter(emprestado = True)

            return render(request, 'ver_livro.html', {'livro': livro, 
                                                      'usuario': usuario,
                                                      'categoria_livro': categoria_livro, 
                                                      'emprestimos': emprestimos,
                                                      'usuario_logado': request.session.get('usuario'),
                                                      'form': form,
                                                      'id_livro': id,  #é o ID que vem da requisição, sendo o ID do livro, tbm será usado p excluir livro
                                                      'form_categoria': form_categoria,
                                                      'usuarios':  usuarios,
                                                      'livros_emprestar': livros_emprestar,
                                                      'livros_emprestados': livros_emprestados})
        else:
            return HttpResponse('Esse livro não é seu!')
    return redirect('/auth/login/?status=2')


def cadastrar_livro(request):
    if request.method == 'POST':                   #permite acessar a url somente quando for um POST
        form = CadastroLivro(request.POST, request.FILES)         #vai receber os dados preenchidos

        if form.is_valid():
            form.save()
            return redirect('/livro/home')
        else:
            return HttpResponse('formulário invalido')
    

def excluir_livro(request, id):
    livro = Livros.objects.get(id = id).delete()
    return redirect('/livro/home')


def cadastrar_categoria(request):
    form = CategoriaLivro(request.POST)  #instancio o form criado em forms.py
    nome = form.data['nome']
    descricao = form.data['descricao']
    id_usuario = request.POST.get('usuario')   #id user do formulario

    if int(id_usuario) == int(request.session.get('usuario')):   #id form == id logado
        user = Usuario.objects.get(id = id_usuario)    #pego o id do form para buscar o Id do usuario na tabela Usuario
        categoria = Categoria(nome = nome, descricao = descricao, usuario = user)         #aqui envio para a tabela de categoria
        categoria.save()
        return redirect('/livro/home?cadastro_categoria=1')
    else:
        return HttpResponse("ERROR")
    

def cadastrar_emprestimo(request):
    if request.method == 'POST':
        nome_emprestado = request.POST.get('nome_emprestado')                            #select de usuarios cadastrados  - pego pelo attr name
        nome_emprestado_anonimo = request.POST.get('nome_emprestado_anonimo')            #input de usuarios não cadastrados - pego pelo attr name
        livro_emprestado = request.POST.get('livro_emprestado')                          #livro que será empretado - pego pelo attr name

        if nome_emprestado_anonimo:
            emprestimo = Emprestimos(nome_emprestado_anonimo = nome_emprestado_anonimo, 
                                    livro_id = livro_emprestado)
        else:
            emprestimo = Emprestimos(nome_emprestado_id = nome_emprestado, 
                                    livro_id = livro_emprestado)            
        emprestimo.save()

        livro = Livros.objects.get(id = livro_emprestado)
        livro.emprestado = True
        livro.save()

        return redirect("/livro/home")
    

def devolver_livro(request):
    id = request.POST.get('id_livro_devolver')       #pega o livro do front
    livro_devolver = Livros.objects.get(id = id)     #acha no BD
    livro_devolver.emprestado = False                #muda estado p false
    livro_devolver.save()

    emprestimo_devolver = Emprestimos.objects.get(Q(livro = livro_devolver) & Q(data_devolucao = None))
    emprestimo_devolver.data_devolucao = datetime.now()
    emprestimo_devolver.save()

    return redirect('/livro/home')


def alterar_livro(request):
    livro_id = request.POST.get('livro_id')
    nome_livro = request.POST.get('nome_livro')        #pego os dados que vem do form do front pelo name, será enviado para a instancia
    autor = request.POST.get('autor')
    co_autor = request.POST.get('co_autor')
    categoria_id = request.POST.get('categoria_id')

    categoria = Categoria.objects.get(id = categoria_id)
    livro = Livros.objects.get(id = livro_id)            #instancio a tabela livro

    if livro.usuario.id == request.session['usuario']:   #verifico se o usuario da instancia é o usuario logado
        livro.nome = nome_livro
        livro.autor = autor
        livro.coautor = co_autor                          #pego a instancia + coluna e atribuo a var gerada acima
        livro.categoria = categoria
        livro.save()
        return redirect(f'/livro/ver_livro/{livro_id}')
    else:
        return redirect('/auth/sair')


def seus_emprestimos(request):
    usuario = Usuario.objects.get(id = request.session['usuario']) #busquei o usuario
    emprestimos = Emprestimos.objects.filter(nome_emprestado = usuario) #traga todos os livros q foram emprestados para esse user

    form = CadastroLivro()  #vem de forms.py
    form.fields['usuario'].initial = request.session['usuario'] #pega campo usuario q está hidden e define o value como ID do user
    form.fields['categoria'].queryset = Categoria.objects.filter(usuario = usuario) # user logado igual ao user da tabela de categoria
    form_categoria = CategoriaLivro()

    return render(request, 'seus_emprestimos.html', {'usuario_logado': request.session['usuario'],
                                                     'emprestimos': emprestimos,
                                                     'form': form,
                                                     'form_categoria': form_categoria})


def processa_avaliacao(request):
    id_emprestimo = request.POST.get('id_emprestimo')
    opcoes = request.POST.get('opcoes')
    id_livro = request.POST.get('id_livro')

    emprestimo = Emprestimos.objects.get(id = id_emprestimo)  #ato de pegar a linha na tabela desse emprestimo, p gravar as novas alterações

    if emprestimo.livro.usuario.id == request.session['usuario']:
        emprestimo.avaliacao = opcoes
        emprestimo.save()
    else:
        HttpResponse("esse emprestimo nao é seu")

    return redirect(f'/livro/ver_livro/{id_livro}')





    
    

