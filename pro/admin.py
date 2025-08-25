import csv
from django.http import HttpResponse
from django.contrib import admin
from .models import Cargo, Cidade, LocalTrabalho, Colaborador, Pergunta, RespostaPesquisa

# ---------- Admin para Cargo ----------
@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)

# ---------- Admin para Cidade ----------
@admin.register(Cidade)
class CidadeAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)

# ---------- Admin para LocalTrabalho ----------
@admin.register(LocalTrabalho)
class LocalTrabalhoAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)

# ---------- Admin para Colaborador ----------
@admin.register(Colaborador)
class ColaboradorAdmin(admin.ModelAdmin):
    list_display = (
        'nome_completo',
        'cpf',
        'sexo',
        'data_nascimento',
        'email',
        'escolaridade',
        'estado_civil',
        'cargo',
        'cidade', 
        'local_trabalho',
        'tempo_unicoop',
        'tempo_funcao',
        'is_active'
    )

    list_display_links = (
        'nome_completo',
        'email'
    )

    list_filter = (
        'is_active',
        'cidade', 
        'local_trabalho', 
        'cargo', 
        'sexo', 
        'escolaridade'
    )

    search_fields = (
        'nome_completo', 
        'cpf', 
        'email',
        'cargo'
    )

    ordering = ('nome_completo',)

    def get_local_trabalho(self, obj):
        return obj.local_trabalho or "-"



# ---------- Admin para Pergunta ----------
@admin.register(Pergunta)
class PerguntaAdmin(admin.ModelAdmin):
    list_display = ("texto",)
    search_fields = ("texto",)

# ---------- Admin para RespostaPesquisa ----------
@admin.register(RespostaPesquisa)
class RespostaPesquisaAdmin(admin.ModelAdmin):
    list_display = (
        "cpf",
        "resposta1",
        "resposta2", "resposta2_descricao",
        "resposta3", "resposta3_descricao",
        "resposta4", "resposta4_descricao",
        "resposta5",
        "resposta6",
        "data_resposta",
    )
    search_fields = (
        "cpf",
        "resposta1",
        "resposta2", "resposta2_descricao",
        "resposta3", "resposta3_descricao",
        "resposta4", "resposta4_descricao",
        "resposta5",
        "resposta6",
    )
    list_filter = ("resposta2", "resposta3", "resposta4", "data_resposta")
    date_hierarchy = "data_resposta"
    list_per_page = 25

    actions = ["export_respostas_to_csv"]

    def export_respostas_to_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=respostas.csv"

        writer = csv.writer(response)
        writer.writerow([
            "CPF", "Resposta 1",
            "Resposta 2", "Descrição 2",
            "Resposta 3", "Descrição 3",
            "Resposta 4", "Descrição 4",
            "Resposta 5", "Resposta 6",
            "Data"
        ])

        for r in queryset:
            writer.writerow([
                r.cpf,
                r.resposta1,
                r.resposta2, r.resposta2_descricao,
                r.resposta3, r.resposta3_descricao,
                r.resposta4, r.resposta4_descricao,
                r.resposta5, r.resposta6,
                r.data_resposta.strftime("%Y-%m-%d %H:%M:%S"),
            ])

        return response

    export_respostas_to_csv.short_description = "Exportar selecionadas para CSV"

