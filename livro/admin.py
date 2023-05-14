from django.contrib import admin
from . models import Livros, Categoria, Emprestimos

admin.site.register(Livros)
admin.site.register(Categoria)
admin.site.register(Emprestimos)