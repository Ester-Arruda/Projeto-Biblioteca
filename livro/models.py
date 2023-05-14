from django.db import models
from datetime import date
import datetime
from usuarios.models import Usuario

class Categoria(models.Model):
    nome = models.CharField(max_length=30)
    descricao = models.TextField()
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    def __str__(self) -> str:
        return self.nome


class Livros(models.Model):
    img = models.ImageField(upload_to='capa_livro', null=True, blank=True)
    nome = models.CharField(max_length=100)
    autor = models.CharField(max_length=30)
    coautor = models.CharField(max_length=3, blank = True)
    data_cadastro = models.DateField(default=date.today)
    emprestado = models.BooleanField(default=False)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = 'Livro'

    def __str__(self):
        return self.nome
    

class Emprestimos(models.Model):
    choices = (                 #crio tupla de opções para as avaliações
        ('P', 'Péssimo'),       #a letra única é o que vai ser armazenado no BD
        ('R', 'Ruim'),
        ('B', 'Bom'),
        ('O', 'Ótimo')
    )
    nome_emprestado = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING, blank = True, null = True)
    nome_emprestado_anonimo = models.CharField(max_length=30, blank = True, null = True)
    data_emprestimo = models.DateTimeField(default=datetime.datetime.now())
    data_devolucao = models.DateTimeField(blank = True, null = True)
    livro = models.ForeignKey(Livros, on_delete = models.SET_NULL, null=True)
    avaliacao = models.CharField(max_length=1, choices = choices, null = True, blank= True) #P, R, B, O por isso que é 1, chamo a tupla
    class Meta:
        verbose_name = "Emprestimo"

    def __str__(self):
        return f"{self.nome_emprestado} | {self.livro}"
        