from django import forms        #importa o modulo form
from . models import Livros     


class CadastroLivro(forms.ModelForm):       #ModelForm = usaremos campos de uma model já existente (Livros)
    class Meta:                              #Meta referencia infos do nosso form
        model = Livros                       
        fields = "__all__"               #pegue a models Livros e use 'all' todos os campos

    def __init__(self, *args, **kwargs):    #crio os param do meu obj
        super().__init__(*args, **kwargs)   #puxo os param do pai do ModelForm para funcionar ok
        self.fields['usuario'].widget = forms.HiddenInput()      #pega o campo usuario e sua tag:select e esconda


class CategoriaLivro(forms.Form):
    nome = forms.CharField(max_length=30)
    descricao = forms.CharField(max_length=60)

    def __ini__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descricao'].widget = forms.Textarea()

