from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect

from .forms import Contatoform, ProdutoModelForm
from .models import Produto


def index(request):
    context = {
        'produtos': Produto.objects.all()
    }
    return render(request, 'index.html', context)


def contato(request):
    form = Contatoform(request.POST or None) #formulario tem dados ou nao
    if str(request.method) == 'POST':
        if form.is_valid():
            form.send_mail()
            """
            nome = form.cleaned_data['nome']
            email = form.cleaned_data['email']
            assunto = form.cleaned_data['assunto']
            mensagem = form.cleaned_data['mensagem']
            """

            messages.success(request, 'E-mail enviado com sucesso!')
            form = Contatoform() # limpa o formulario depois que envia os dados
        else:
            messages.error(request, 'Erro ao enviar e-mail')

    context = {
        'form': form
    }
    return render(request, 'contato.html', context)


def produto(request):
    if str(request.user) != 'AnonymousUser':
        if str(request.method) == 'POST':
            form = ProdutoModelForm(request.POST, request.FILES)
            if form.is_valid():
                form.save() # se o form estiver valido, salva
                messages.success(request, 'Produto salvo com sucesso.')
                form = ProdutoModelForm()
            else:
                messages.error(request, 'Erro ao salvar o produto.')

        else:
             form = ProdutoModelForm()
        context = {
           'form': form
        }
        return render(request, 'produto.html', context)
    else:
        return redirect('index')