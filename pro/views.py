from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Colaborador
from datetime import datetime

# Create your views here.
def home(request):
    return render(request,'usuarios/home.html')

def questionario(request):
    return render(request, 'usuarios/questionario.html')

def area(request):
    return render(request, 'usuarios/area.html')

def responder(request):
    if request.method == "POST":
        cpf = request.POST.get("cpf", "").strip()

        if Colaborador.objects.filter(cpf=cpf).exists():
            messages.error(request, "❌ CPF já utilizado! Não é permitido responder novamente.")
            return render(request, "usuarios/questionario.html", {"valores": request.POST})
        
        resposta1 = request.POST.get("resposta1", "").strip()
        resposta2 = request.POST.get("resposta2", "").strip()
        resposta2_descricao = request.POST.get("resposta2_descricao", "").strip()
        resposta3 = request.POST.get("resposta3", "").strip()
        resposta3_descricao = request.POST.get("resposta3_descricao", "").strip()
        resposta4 = request.POST.get("resposta4", "").strip()
        resposta4_descricao = request.POST.get("resposta4_descricao", "").strip()
        resposta5 = request.POST.get("resposta5", "").strip()
        resposta6 = request.POST.get("resposta6", "").strip()

        # Valida se já existe um registro para este CPF
        # if RespostaPesquisa.objects.filter(cpf=cpf).exists():
        #     messages.error(request, "Você já respondeu o questionário.")
        #     return redirect("responder")

        # Salva os dados no banco
        RespostaPesquisa.objects.create(
            cpf=cpf,
            resposta1=resposta1,
            resposta2=resposta2,
            resposta2_descricao=resposta2_descricao if resposta2 == "Sim" else "",
            resposta3=resposta3,
            resposta3_descricao=resposta3_descricao if resposta3 == "Sim" else "",
            resposta4=resposta4,
            resposta4_descricao=resposta4_descricao,
            resposta5=resposta5,
            resposta6=resposta6,
        )

        messages.success(request, "Obrigado! Suas respostas foram salvas.")
        return redirect("conclusaoform")  # página de agradecimento

    # GET
    return render(request, "usuarios/responder.html")

def cadastro(request):
    return render(request, 'usuarios/cadastro.html')

def login(request):
    return render(request, 'usuarios/login.html')
def dash(request):
    return render(request, "dash.html")

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import RespostaPesquisa

def conclusaoform(request):
    return render(request, "usuarios/conclusaoform.html")


def cadastrar_colaborador(request):
    if request.method == "POST":
        nome_completo = request.POST.get("nome_completo", "")
        cpf = request.POST.get("cpf", "")
        sexo = request.POST.get("sexo", "")
        nascimento = request.POST.get("nascimento", "")
        email = request.POST.get("email", "")
        escolaridade = request.POST.get("escolaridade", "")
        estado_civil = request.POST.get("estado_civil", "")
        cargo = request.POST.get("cargo", "")
        local_trabalho = request.POST.get("local_trabalho", "")
        tempo_unicoop = request.POST.get("tempo_unicoop", "")
        tempo_funcao = request.POST.get("tempo_funcao", "")
        cidade = request.POST.get("cidade", "")

        # Converte data
        try:
            nascimento = datetime.strptime(nascimento, "%d/%m/%Y").date()
        except Exception:
            nascimento = None

        # Salva direto os valores do formulário
        colaborador = Colaborador.objects.create(
            nome_completo=nome_completo,
            cpf=cpf,
            sexo=sexo,
            data_nascimento=nascimento,
            email=email,
            escolaridade=escolaridade,
            estado_civil=estado_civil,
            cargo=cargo,
            local_trabalho=local_trabalho,
            tempo_unicoop=tempo_unicoop,
            tempo_funcao=tempo_funcao,
            cidade=cidade,
        )

        return redirect("responder")

    return render(request, "questionario.html")

        # 3) Salva no banco
#         RespostaPesquisa.objects.create(
#             cpf=cpf,
#             resposta1=resposta1,
#             pergunta2=pergunta2, resposta2=resposta2,
#             pergunta3=pergunta3, resposta3=resposta3,
#             pergunta4=pergunta4, resposta4=resposta4,
#             resposta5=resposta5, resposta6=resposta6
#         )

#         # 4) Renderiza sua página de agradecimento
#         return render(request, "conclusaoform.html")

#     # Se acessarem por GET, redirecione para a home (ou para o formulário)
#     return redirect("home")

# def dash(request):
#     return render(request, 'usuarios/dash.html')




