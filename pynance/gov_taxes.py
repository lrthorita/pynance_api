#!/usr/bin/python
# -- coding: utf-8 --
"""
Author: Luiz Ricardo Takeshi Horita
Date: 2020-04-12
"""
from typing import Dict, List, Union
from collections import defaultdict
from math import *

# Tabela de incidência mensal
#############################
BASE_SALARIO = [1903.99, 2826.66, 3751.06, 4664.69]
ALIQUOTA_SALARIO = [0.0, 0.075, 0.15, 0.225, 0.275]
PARCELA_DEDUZIR_SALARIO = [0.0, 142.80, 354.80, 636.13, 869.36]

def aliquota_ir_salario(salario_base:float):
    """
    Com base no salário base e a base de cálculo mensal, esta
    função retorna a taxa de alíquota e o valor da parcela a
    deduzir do imposto de renda.
    """
    for i, base in enumerate(BASE_SALARIO):
        if salario_base < base:
            return ALIQUOTA_SALARIO[i], PARCELA_DEDUZIR_SALARIO[i]
    return ALIQUOTA_SALARIO[-1], PARCELA_DEDUZIR_SALARIO[-1]

# Rendimentos de capital
########################
# Renda Fixa (RF)
DIAS_RF = [181, 361, 721]
IR_RF = [0.225, 0.20, 0.175, 0.15]

def aliquota_ir_rf(periodo_aplicacao:int):
    """
    Com base no tempo de investimento em renda fixa, esta função
    retorna a taxa de alíquota do imposto de renda de acordo com
    a tabela regressiva.
    """
    for i, dias in enumerate(DIAS_RF):
        if periodo_aplicacao < dias:
            return IR_RF[i]
    return IR_RF[-1]

# Fundo de ações (FA)
IR_FA = 0.15

# Participação nos lucros ou resultados (PLR)
#############################################
BASE_PLR = [6677.56, 9922.29, 13167.01, 16380.39]
ALIQUOTA_PLR = [0.0, 0.075, 0.15, 0.225, 0.275]
PARCELA_DEDUZIR_PLR = [0.0, 500.82, 1244.99, 2232.51, 3051.53]

def aliquota_ir_plr(plr_bruto:float):
    """
    Com base no valor bruto referente à participação nos lucros
    ou resultados de um negócio e a base de cálculo mensal, esta
    função retorna a taxa de alíquota e o valor da parcela a
    deduzir do imposto de renda.
    """
    for i, base in enumerate(BASE_PLR):
        if plr_bruto < base:
            return ALIQUOTA_PLR[i], PARCELA_DEDUZIR_PLR[i]
    return ALIQUOTA_PLR[-1], PARCELA_DEDUZIR_PLR[-1]


#Rendimentos recebidos acumuladamente (RRAs)
############################################
BASE_RRA = [1903.99, 2826.66, 3751.06, 4664.69]
ALIQUOTA_RRA = [0.0, 0.075, 0.15, 0.225, 0.275]
PARCELA_DEDUZIR_RRA = [0.0, 142.80, 354.80, 636.13, 869.36]

def aliquota_ir_rra(rra_bruto:float):
    """
    Com base no valor bruto referente à rendimentos recebidos
    acumuladamente por mês e a base de cálculo mensal, esta
    função retorna a taxa de alíquota e o valor da parcela a
    deduzir do imposto de renda.
    """
    for i, base in enumerate(BASE_RRA):
        if rra_bruto < base:
            return ALIQUOTA_RRA[i], PARCELA_DEDUZIR_RRA[i]
    return ALIQUOTA_RRA[-1], PARCELA_DEDUZIR_RRA[-1]

# Dedução mensal por dependente
###############################
PARCELA_DEDUZIR_POR_DEPENDENTE = 189.59

# INSS
######
BASE_INSS = [1045.00, 2089.60, 3134.40, 6101.06]
ALIQUOTA_INSS = [0.075, 0.09, 0.12, 0.14]

def valor_inss(salario_bruto:float):
    """
    Com base no salário bruto e a base de cálculo mensal, esta
    função retorna o valor do INSS a pagar.
    """
    valor = salario_bruto
    val_inss = 0
    base_previa = 0
    for i, base in enumerate(BASE_INSS):
        if salario_bruto <= base:
            val_inss += valor*ALIQUOTA_INSS[i]
            return val_inss
        else:
            val_inss += (base - base_previa)*ALIQUOTA_INSS[i]
            valor -= (base - base_previa)
            base_previa = base
    return val_inss

# Imposto de Renda
##################
class ImpostoDeRenda():
    def __init__(self, 
                salario_bruto:float=1000.0,
                renda_isenta:float=0.0,
                dependentes:int=0,
                pensoes_dependentes:float=0.0,
                tipo:str="simplificado"
                ):
        self.salario_bruto = salario_bruto
        self.renda_isenta = renda_isenta
        self.dependentes = dependentes
        self.tipo = tipo
        
        self.deducao_dependentes = dependentes*PARCELA_DEDUZIR_POR_DEPENDENTE + pensoes_dependentes
        self.inss = valor_inss(salario_bruto)
        self.valor_na_fonte()

    def valor_na_fonte(self):
        base_calculo = (self.salario_bruto - self.deducao_dependentes - self.inss)
        aliquota_salario, dedutivel_salario = aliquota_ir_salario(base_calculo)
        self.valor_ir = base_calculo*aliquota_salario - dedutivel_salario

    def aliquota_efetiva(self):
        return self.valor_ir/self.salario_bruto