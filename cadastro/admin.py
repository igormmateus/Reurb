from django.contrib import admin
from .models import CadastroPessoa, PreCadastroImovel, Conjuge, Bairro


class PreCadastroImovelAdmin(admin.ModelAdmin):
    list_display = ('proprietario', 'quadra', 'lote', 'bairro', 'status')
    list_filter = ('bairro',)
    list_per_page = 10


class BairrosAdmin(admin.ModelAdmin):
    pass

class CadastroPessoaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome')
    list_display_links = ('nome',)

admin.site.register(Conjuge)
admin.site.register(CadastroPessoa, CadastroPessoaAdmin)
admin.site.register(PreCadastroImovel, PreCadastroImovelAdmin)
admin.site.register(Bairro)
