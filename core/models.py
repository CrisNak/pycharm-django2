from django.db import models
from stdimage import StdImageField

# SIGNALS
from django.db.models import signals
from django.template.defaultfilters import slugify
# slug pega o titulo do html e coloca na url por traços


class Base(models.Model):
    criado = models.DateField('Data de Criação', auto_now_add=True)
    modificado = models.DateField('Data de Atualização', auto_now=True)
    ativo = models.BooleanField("Ativo?", default=True)

    class Meta:
        abstract = True


class Produto(Base):# já contendo as informações da class base
    nome = models.CharField('Nome', max_length=100)
    preco = models.DecimalField('Preço', max_digits=8, decimal_places=2)
    estoque = models.IntegerField('Estoque')
    imagem = StdImageField('Imagem', upload_to='produtos', variations={'thumb': (124, 124)})
    slug = models.SlugField('Slug', max_length=100, blank=True, editable=False)
    # blank=True: pode ser em branco e editable = False: não pode ser editado

    def __str__(self):
        return self.nome


def produto_pre_save(signal, instance, sender, **kwargs):
    instance.slug = slugify(instance.nome)
    # slugify: Maria Mole -> maria-mole

signals.pre_save.connect(produto_pre_save, sender=Produto)
#quando der o sinal: produto for salvo , executar produto_pre_save


