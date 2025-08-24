from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'usuarios/home.html')

def questionario(request):
    return render(request, 'usuarios/questionario.html')

def area(request):
    return render(request, 'usuarios/area.html')

def responder(request):
    return render(request, 'usuarios/responder.html')

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
    if request.method == "POST":
        # 1) Coleta dos dados do formulário
        dados = {
            "cpf": request.POST.get("cpf", "").strip(),
            "resposta1": request.POST.get("resposta1", "").strip(),
            "pergunta2": request.POST.get("pergunta2"),
            "resposta2": request.POST.get("resposta2", "").strip(),
            "pergunta3": request.POST.get("pergunta3"),
            "resposta3": request.POST.get("resposta3", "").strip(),
            "pergunta4": request.POST.get("pergunta4"),
            "resposta4": request.POST.get("resposta4", "").strip(),
            "resposta5": request.POST.get("resposta5", "").strip(),
            "resposta6": request.POST.get("resposta6", "").strip(),
        }

        # 2) Validações mínimas
        erros = []
        if not dados["cpf"]:
            erros.append("Informe seu CPF.")
        if not dados["resposta1"]:
            erros.append("Responda a Pergunta 1.")
        if dados["pergunta2"] not in ["Sim", "Não"]:
            erros.append("Escolha uma opção na Pergunta 2.")
        if dados["pergunta3"] not in ["Sim", "Não"]:
            erros.append("Escolha uma opção na Pergunta 3.")
        if dados["pergunta4"] not in ["Positivamente", "Negativamente"]:
            erros.append("Escolha uma opção na Pergunta 4.")
        if not dados["resposta5"]:
            erros.append("Responda a Pergunta 5.")

        # Validação extra: descrição obrigatória quando marcar "Sim"
        if dados["pergunta2"] == "Sim" and not dados["resposta2"]:
            erros.append("Descreva a Pergunta 2 (você marcou Sim).")
        if dados["pergunta3"] == "Sim" and not dados["resposta3"]:
            erros.append("Descreva a Pergunta 3 (você marcou Sim).")

        # Se houver erros, volta para o formulário mostrando mensagens
        if erros:
            for e in erros:
                messages.error(request, e)
            return redirect(request.META.get("HTTP_REFERER", "/"))

        # 3) Salva no banco
        RespostaPesquisa.objects.create(**dados)

        # 4) Renderiza página de agradecimento
        return render(request, "conclusaoform.html")

    # Se for GET, manda para a home (ou para o formulário)
    return redirect("home")

#view que salva o cadastro do usuario no banco de dados 
from django.shortcuts import render, redirect
from .models import Colaborador, Cargo, LocalTrabalho
from datetime import datetime

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




