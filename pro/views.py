from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import Colaborador
from datetime import datetime
from django.db.models import Count, Q
from django.http import HttpResponse   # <-- ADICIONA ISSO
import csv
import pandas as pd
from django.conf import settings
import os
from django.contrib import messages


# Create your views here.
def home(request):
    return render(request,'usuarios/home.html')

def questionario(request):
    return render(request, 'usuarios/questionario.html')

def area(request):
    return render(request, 'usuarios/area.html')

def responder(request):
    
    if request.method == "POST":
        cpf = normalizar_cpf(request.POST.get("cpf", "").strip())

        if not Colaborador.objects.filter(cpf=cpf).exists():
            messages.error(request, "❌ CPF não cadastrado. Cadastre-se primeiro para responder.")
            return render(request, "usuarios/responder.html", {"valores": request.POST}) 
        
        # 🔹 1) Verifica se já respondeu
        if RespostaPesquisa.objects.filter(cpf=cpf).exists():
            messages.error(request, "❌ Este CPF já respondeu ao questionário.")
            return redirect("responder")

        # 🔹 2) Coleta as respostas
        resposta1 = request.POST.get("resposta1", "").strip()
        resposta2 = request.POST.get("resposta2", "").strip()
        resposta2_descricao = request.POST.get("resposta2_descricao", "").strip()
        resposta3 = request.POST.get("resposta3", "").strip()
        resposta3_descricao = request.POST.get("resposta3_descricao", "").strip()
        resposta4 = request.POST.get("resposta4", "").strip()
        resposta4_descricao = request.POST.get("resposta4_descricao", "").strip()
        resposta5 = request.POST.get("resposta5", "").strip()
        resposta6 = request.POST.get("resposta6", "").strip()

        # 🔹 3) Cria o registro da pesquisa
        RespostaPesquisa.objects.create(
            cpf=cpf,
            resposta1=resposta1,
            resposta2=resposta2,
            resposta2_descricao=resposta2_descricao if resposta2 == "Sim" else "",
            resposta3=resposta3,
            resposta3_descricao=resposta3_descricao if resposta3 == "Não" else "",
            resposta4=resposta4,
            resposta4_descricao=resposta4_descricao,
            resposta5=resposta5,
            resposta6=resposta6,
        )
        request.session['respondeu'] = True

        # 🔹 4) Mensagem de sucesso e redirecionamento
        messages.success(request, "✅ Obrigado! Suas respostas foram salvas.")
        return redirect("conclusaoform")  # página de agradecimento

    # 🔹 Caso seja GET, só renderiza o formulário
    return render(request, "usuarios/responder.html")

def cadastro(request):
    return render(request, 'usuarios/cadastro.html')

def login(request):
    if request.method == "POST":
        cpf = request.POST.get("cepefe", "").strip()
        senha = request.POST.get("senha", "").strip()

        LOGIN_CORRETO = "levegestao"
        SENHA_CORRETA = "Silviosantos1!1234"

        if cpf == LOGIN_CORRETO and senha == SENHA_CORRETA:
            request.session["logado"] = True
            return redirect("dash")  
        else:
            messages.error(request, "❌ CPF ou senha incorretos.")

    return render(request, "usuarios/login.html")

def normalizar_cpf(cpf):
    return "".join(filter(str.isdigit, str(cpf or "")))

def validar_cpf(cpf: str) -> bool:
    """
    Valida um CPF pelo cálculo dos dígitos verificadores.
    Retorna True se for válido, False caso contrário.
    """
    cpf = "".join(filter(str.isdigit, str(cpf)))  # mantém só números

    if len(cpf) != 11:
        return False

    # elimina CPFs com todos os dígitos iguais (ex: 11111111111)
    if cpf == cpf[0] * 11:
        return False

    # calcula os 2 dígitos verificadores
    for i in range(9, 11):
        soma = sum(int(cpf[num]) * ((i+1) - num) for num in range(0, i))
        digito = ((soma * 10) % 11) % 10
        if digito != int(cpf[i]):
            return False

    return True


def dash(request):
    
    f_cargo  = (request.GET.get("cargo") or "").strip()
    f_local  = (request.GET.get("local_trabalho") or "").strip()
    f_cidade = (request.GET.get("cidade") or "").strip()
    f_p2 = (request.GET.get("p2") or "").strip()
    f_p3 = (request.GET.get("p3") or "").strip()
    f_p4 = (request.GET.get("p4") or "").strip()

    respostas_list = RespostaPesquisa.objects.order_by('-data_resposta')
    
    col_qs = Colaborador.objects.all()
    if f_cargo:
        col_qs = col_qs.filter(cargo=f_cargo)
    if f_local:
        col_qs = col_qs.filter(local_trabalho=f_local)
    if f_cidade:
        col_qs = col_qs.filter(cidade=f_cidade)

    if f_cargo or f_local or f_cidade:
        cpfs_filtrados = list(col_qs.values_list('cpf', flat=True))
        respostas_list = respostas_list.filter(cpf__in=cpfs_filtrados)


    

    if f_p2:
        respostas_list = respostas_list.filter(resposta2=f_p2)

    if f_p3:
        respostas_list = respostas_list.filter(resposta3=f_p3)

    if f_p4:
        respostas_list = respostas_list.filter(resposta4=f_p4)

    # Cria um atributo extra em cada resposta
    colaboradores = {normalizar_cpf(c.cpf): c for c in Colaborador.objects.all()}

    for r in respostas_list:
        r.colaborador = colaboradores.get(normalizar_cpf(r.cpf))


    # 🔹 Ajustado: garantir valores únicos sem duplicar lógica
    cargos = sorted(set(
        (c or "").strip()
        for c in Colaborador.objects.values_list("cargo", flat=True)
        if c and c.strip()
    ))

    locais = sorted(set(
        (l or "").strip()
        for l in Colaborador.objects.values_list("local_trabalho", flat=True)
        if l and l.strip()
    ))

    cidades = sorted(set(
        (ci or "").strip()
        for ci in Colaborador.objects.values_list("cidade", flat=True)
        if ci and ci.strip()
    ))

    # 2. Calcula as estatísticas agregadas
    total_respostas = respostas_list.count()
    total_cargo = Colaborador.objects.values("cargo").distinct().count()
    total_local = Colaborador.objects.values("local_trabalho").distinct().count()

    # Contagem para a Pergunta 2 (Sinais de sobrecarga)
    stats_resposta2 = RespostaPesquisa.objects.aggregate(
        sim=Count('pk', filter=Q(resposta2="Sim")),
        nao=Count('pk', filter=Q(resposta2="Não"))
    )

    # Contagem para a Pergunta 3 (Liderança e saúde mental)
    stats_resposta3 = RespostaPesquisa.objects.aggregate(
        sim=Count('pk', filter=Q(resposta3="Sim")),
        nao=Count('pk', filter=Q(resposta3="Não"))
    )

    # Contagem para a Pergunta 4 (Impacto do ambiente)
    stats_resposta4 = RespostaPesquisa.objects.aggregate(
        positivo=Count('pk', filter=Q(resposta4="Positivamente")),
        negativo=Count('pk', filter=Q(resposta4="Negativamente"))
    )

    colaboradores = carregar_planilha()

    
    # Busca CPFs que já responderam
    responded_cpfs = RespostaPesquisa.objects.values_list("cpf", flat=True)

    # Normaliza todos os CPFs (deixa só dígitos)
    responded_cpfs = {
        "".join(filter(str.isdigit, str(cpf)))
        for cpf in responded_cpfs
    }

    # Monta a lista de pendentes com CPFs normalizados
    pendentes_list = [
        c for c in colaboradores
        if "".join(filter(str.isdigit, str(c["cpf"]))) not in responded_cpfs
    ]

    # 3. Monta o contexto para enviar ao template
    context = {
        'respostas': respostas_list, 
        'pendentes': pendentes_list,
        'total_respostas': total_respostas,
        'total_cargo': total_cargo,
        'total_local': total_local,
        'cargos': cargos,
        'locais': locais,
        'cidades': cidades,
        'stats_r2': stats_resposta2,
        'stats_r3': stats_resposta3,
        'stats_r4': stats_resposta4,
        'f_cargo': f_cargo,
        'f_local': f_local,
        'f_cidade': f_cidade,
        'f_p2': f_p2,
        'f_p3': f_p3,
        'f_p4': f_p4,
    }

    # 4. Renderiza o template com todos os dados
    return render(request, 'usuarios/dash.html', context)



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import RespostaPesquisa

def conclusaoform(request):
    if not request.session.get('respondeu'):
        return redirect('responder')
    
    return render(request, "usuarios/conclusaoform.html")


from django.contrib import messages
from django.db import IntegrityError

def cadastrar_colaborador(request):
    if request.method == "POST":
        cpf = "".join(filter(str.isdigit, request.POST.get("cpf", "")))

        if not validar_cpf(cpf):
            messages.error(request, "❌ CPF inválido! Verifique os números digitados.")
            return render(request, "usuarios/questionario.html", {"valores": request.POST})
        
        # 1) Verifica se já existe
        if Colaborador.objects.filter(cpf=cpf).exists():
            messages.error(request, "❌ Este CPF já está cadastrado!")
            return render(request, "usuarios/questionario.html", {"valores": request.POST})
        
        # 2) Pega os outros dados
        nome_completo = request.POST.get("nome_completo", "")
        sexo = request.POST.get("sexo", "")
        nascimento = request.POST.get("nascimento", "")
        email = request.POST.get("email", "")

        if Colaborador.objects.filter(email=email).exists():
            messages.error(request, "❌ Este email já está cadastrado!")
            return render(request, "usuarios/questionario.html", {"valores": request.POST})
        
        escolaridade = request.POST.get("escolaridade", "")
        estado_civil = request.POST.get("estado_civil", "")
        cargo = request.POST.get("cargo", "")
        local_trabalho = request.POST.get("local_trabalho", "")
        tempo_unicoop = request.POST.get("tempo_unicoop", "")
        tempo_funcao = request.POST.get("tempo_funcao", "")
        cidade = request.POST.get("cidade", "")

        # 3) Converte data
        try:
            nascimento = datetime.strptime(nascimento, "%d/%m/%Y").date()
        except Exception:
            nascimento = None

        # 4) Cria o colaborador
        Colaborador.objects.create(
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

        messages.success(request, "✅ Cadastro realizado com sucesso!")
        return redirect(f"/responder?cpf={cpf}")

    # GET
    return render(request, "usuarios/questionario.html")

def exportar_csv(request):
    # Cria a resposta HTTP com cabeçalho de arquivo CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="respostas_pesquisa.csv"'

    writer = csv.writer(response)
    
    # Cabeçalho do CSV
    writer.writerow([
        'CPF', 'Nome', 'Sexo','Escolaridade','Dt.Nasc','Cargo', 
        'Local de trabalho','T.UNICOOP','T.func Atual','Cidade', 'Data Resp',
        'P1: Estresse/Insegurança',
        'P2: Sobrecarga', 'P2 Descrição',
        'P3: Liderança', 'P3 Descrição',
        'P4: Ambiente', 'P4 Descrição',
        'P5: Sugestões',
        'P6: Comentários'
    ])

    # Mapeia colaboradores
    colaboradores = {c.cpf: c for c in Colaborador.objects.all()}

    # Escreve cada linha
    for r in RespostaPesquisa.objects.order_by('-data_resposta'):
        colaborador = colaboradores.get(r.cpf)
        writer.writerow([
            r.cpf,
            colaborador.nome_completo if colaborador else "-",
            colaborador.sexo if colaborador else "-",
            colaborador.escolaridade if colaborador else "-",
            colaborador.data_nascimento if colaborador else "-",
            colaborador.cargo if colaborador else "-",
            colaborador.local_trabalho if colaborador else "-",
            colaborador.tempo_unicoop if colaborador else "-",
            colaborador.tempo_funcao if colaborador else "-",
            colaborador.cidade if colaborador else "-",
            r.data_resposta.strftime("%d/%m/%Y") if r.data_resposta else "",
            r.resposta1,
            r.resposta2,
            r.resposta2_descricao,
            r.resposta3,
            r.resposta3_descricao,
            r.resposta4,
            r.resposta4_descricao,
            r.resposta5,
            r.resposta6
        ])

    return response

def carregar_planilha():
    """
    Lê a planilha de colaboradores (apenas a aba 'TODOS') e devolve uma lista de dicts.
    """
    caminho = os.path.join(settings.BASE_DIR, "dados", "colaboradores.xlsx")
    
    # Lê apenas a aba 'TODOS'
    df = pd.read_excel(caminho, sheet_name="TODOS", dtype=str)  # tudo como string para evitar problema no CPF
    
    df.columns = df.columns.str.strip()

    # Normaliza nomes das colunas para o sistema
    df = df.rename(columns={
        "NOME COMPLETO": "nome_completo2",
        "CARGO": "cargo2",
        "CPF": "cpf",
        "TELEFONE": "telefone",
        "CIDADE": "cidade2",
        "MODALIDADE": "modalidade",
    })

    # Remove espaços extras dos CPFs (importante para comparar com banco)
    df["cpf"] = df["cpf"].str.replace(r"\D", "", regex=True)  # só números

    return df.to_dict(orient="records")

   


