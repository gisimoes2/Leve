from django.db import models


class Cargo(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Cargo")

    def __str__(self):
        return self.nome

#cidade
class Cidade(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Cidade")

    def __str__(self):
        return self.nome

#antigo hospital 
class LocalTrabalho(models.Model):
    nome = models.CharField(max_length=150, verbose_name="Local")

    def __str__(self):
        return self.nome


class Colaborador(models.Model):
    SEXO_CHOICES = [
        ("M", "Masculino"),
        ("F", "Feminino"),
        ("O", "Outro"),
    ]

    ESTADO_CIVIL_CHOICES = [
        ("solteiro", "Solteiro(a)"),
        ("casado", "Casado(a)"),
        ("divorciado", "Divorciado(a)"),
        ("viuvo", "Viúvo(a)"),
        ("outro", "Outro"),
    ]

    ESCOLARIDADE_CHOICES = [
        ("fundamental", "Ensino Fundamental"),
        ("medio", "Ensino Médio"),
        ("tecnico", "Técnico"),
        ("superior", "Ensino Superior"),
        ("pos", "Pós-graduação"),
        ("mestrado", "Mestrado"),
        ("doutorado", "Doutorado"),
    ]

    CARGO_CHOICES = [

    ]


    LOCAL_TRABALHO_CHOICES =[
        
    ]

    TEMPO_UNICOOP_CHOICES = [

    ]

    CIDADE_CHOICES = [ ("Maceió"), ("Fortaleza"), 
    ("Campina Grande"),("João Pessoa"), ("Bezerros"), 
    ("Cabo de Santo Agostinho"), ("Camaragibe"), 
    ("Caruaru"), ("Garanhuns")

]
    
    nome_completo = models.CharField(max_length=150, verbose_name="Nome completo")
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")  # 000.000.000-00
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES, verbose_name="Sexo")
    data_nascimento = models.DateField(verbose_name="Data de nascimento")
    email = models.EmailField(unique=True, verbose_name="E-mail")

    escolaridade = models.CharField(max_length=20, choices=ESCOLARIDADE_CHOICES, verbose_name="Escolaridade")
    estado_civil = models.CharField(max_length=20, choices=ESTADO_CIVIL_CHOICES, verbose_name="Estado Civil")

    cargo = models.CharField(max_length=100)           # agora como string
    funcao = models.CharField(max_length=150, null=True, blank=True, verbose_name="Função")
    local_trabalho = models.CharField(max_length=100)

    

    tempo_unicoop = models.CharField(max_length=50, verbose_name="Tempo na Unicoop")
    tempo_funcao = models.CharField(max_length=50, verbose_name="Tempo na função atual")
    cidade = models.CharField(max_length=100, verbose_name="Cidade")

    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        ordering = ["nome_completo"]
        verbose_name = "Colaborador"
        verbose_name_plural = "Colaboradores"

    def __str__(self):
        return self.nome_completo

class Pergunta(models.Model):
    texto = models.TextField(verbose_name="Pergunta")

    def __str__(self):
        return self.texto[:50]


from django.db import models

class RespostaPesquisa(models.Model):
    cpf = models.CharField("CPF", max_length=14, unique=True)

    # Pergunta 1 - Texto aberto obrigatório
    resposta1 = models.TextField("Situações de estresse ou insegurança")

    # Pergunta 2 - Sim/Não + texto obrigatório
    resposta2 = models.CharField("Sinais de sobrecarga ou assédio", max_length=3, choices=[("Sim", "Sim"), ("Não", "Não")])
    resposta2_descricao = models.TextField("Descrição se respondeu Sim")  # obrigatório

    # Pergunta 3 - Sim/Não + texto obrigatório
    resposta3 = models.CharField("Como a liderança lida com saúde mental?", max_length=3, choices=[("Sim", "Sim"), ("Não", "Não")])
    resposta3_descricao = models.TextField("Descrição se respondeu Sim")  # obrigatório

    # Pergunta 4 - Positivo/Negativo + texto obrigatório
    resposta4 = models.CharField("Impacto do ambiente no trabalho", max_length=50, choices=[("Positivamente", "Positivamente"), ("Negativamente", "Negativamente")])
    resposta4_descricao = models.TextField("Descrição do impacto")  # obrigatório

    # Pergunta 5 - Texto aberto obrigatório
    resposta5 = models.TextField("Sugestões de melhorias")

    # Pergunta 6 - Texto aberto obrigatório
    resposta6 = models.TextField("Comentários adicionais")

    data_resposta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Respostas de {self.cpf}"

    # def __str__(self):
    #     resposta_texto = "Sim" if self.valor else "Não"
    #     return f"{self.colaborador.nome_completo} - {self.pergunta.texto[:30]}: {resposta_texto}"