from django import template    #importa modulo dos templates
from datetime import date, datetime

register = template.Library()  #puxa a biblioteca do template

@register.filter                                                             #coloca o filtro criado na biblioteca
def mostra_duracao(value1, value2):                                          #esse é o filtro de duração do livro
    if all((isinstance(value1, datetime), isinstance(value2, datetime))):    #verifica se tem valor a data de emprestimo e devolução
        return f"{(value1 - value2).days} dias."
    
    return 'Livro ainda não devolvido'                                           #.day passa para dia, ex: 1