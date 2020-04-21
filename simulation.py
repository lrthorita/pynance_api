#!/usr/bin/python
# -- coding: utf-8 --
"""
Author: Luiz Ricardo Takeshi Horita
Date: 2020-04-18
"""

from bc.bancocentral import Inflacao, Selic, Poupanca
from pynance.my_financial_plan import MyFinancialPlan
from pynance.utils import *
from time import time

import colorama
colorama.init()

class PlanSimulator:
    def __init__(self):
        super().__init__()
        self.income = {}
        self.outcome = {}

    def _wait_user(self):
        display_msg(format_printable_string("\n============================================"+\
                                            "\n|  Py Nance: - Vou esperar você ler... :)  |"+\
                                            "\n============================================",CYAN))
        input_or_timeout(10, "[Aperte ENTER quando quiser continuar...]")

    def starting_message(self):
        display_msg("\nOlá! Sou o {}, e vou te ajudar a planejar sua liberdade financeira!".format(
            format_printable_string("PyNance", CYAN)
        ))

        display_msg("\nQual seu {}?".format(format_printable_string("nome",is_underlined=True)))
        self.name = input("Resposta: ")
        if self.name == "":
            display_msg("\nPerdoe-me. Pode repetir seu {}?".format(format_printable_string(
                                                                    "nome",is_underlined=True)))
            self.name = input("Resposta: ")
        display_msg("{}".format(format_printable_string("\nMuito prazer, {}!".format(self.name),GREEN)))
        display_msg("Bora começar? :D\n{}".format(format_printable_string("[Aperte ENTER para continuar]",CYAN)))
        input()

    def knowing_the_user_income(self):
        print("\n***********************")
        while True:
            display_msg("\nQual sua(s) {} atualmente?".format(format_printable_string("fonte(s) de renda",
                                                                                    is_underlined=True))+\
                        "\n[Digite o número da opção]\n"+\
                        "\n  (1) salário"+\
                        "\n  (2) algum tipo de bolsa isento de imposto"+\
                        "\n  (3) ambos\n")
            self.income_source = int("0"+input("Resposta: "))
            if self.income_source in [1,2,3]:
                break
            display_msg("\nDesculpe. {}".format(format_printable_string(
                    "Poderia tentar novamente?",RED)))

    def _getting_incomes(self):
        if self.income_source == 1:
            display_msg("\nQual seu {}?".format(format_printable_string("salário bruto",
                                                                        is_underlined=True)))
            self.gross_salary = float(convert_number_abrev(input("Resposta: R$")))
            self.income["Salário bruto"] = self.gross_salary
            self.aid_grant = 0.0
        if self.income_source == 2:
            self.gross_salary = 0.0
            display_msg("\nQual valor da sua {}?".format(format_printable_string("bolsa/auxílio",
                                                                        is_underlined=True)))
            self.aid_grant = float(convert_number_abrev(input("Resposta: R$")))
            self.income["Bolsa/auxílio"] = self.aid_grant
        if self.income_source == 3:
            display_msg("\nQual seu {}?".format(format_printable_string("salário bruto",
                                                                        is_underlined=True)))
            self.gross_salary = float(convert_number_abrev(input("Resposta: R$")))
            self.income["Salário bruto"] = self.gross_salary
            display_msg("\nQual valor da sua {}?".format(format_printable_string("bolsa/auxílio",
                                                                        is_underlined=True)))
            self.aid_grant = float(convert_number_abrev(input("Resposta: R$")))
            self.income["Bolsa/auxílio"] = self.aid_grant

    def knowing_the_finance_situation(self):
        display_msg("\n***********************"+\
            "\nCerto, {}. Primeiro, vamos descobrir sua {} hoje."\
                .format(self.name, format_printable_string("situação financeira",BLUE,is_bold=True)))
        
        display_msg("\nQuanto você tem de {} hoje?".format(format_printable_string(
                                                            "patrimônio", is_underlined=True)))
        self.patrimony = float(convert_number_abrev(input("Resposta: R$")))

        display_msg("\nE quanto você tem de {}?".format(format_printable_string(
                                            "dívida", is_underlined=True)))
        self.debt = float(convert_number_abrev(input("Resposta: -R$")))
        self.capital = self.patrimony - self.debt

        self._getting_incomes()

        display_msg("\nVocê possui {} (filhos, pais, avós ou bisavós)?".format(format_printable_string(
                                                                    "dependentes",is_underlined=True))+\
                    "\n[Responda com sim(s) ou não(n)]")
        self.is_parent = input("Resposta: ")
        while self.is_parent[0].lower() not in ['s', 'n', '0']:
            self.is_parent = input("\nPor favor, responda sim(s) ou não(n): ")
        if self.is_parent[0].lower() == 's':
            while True:
                try:
                    display_msg("\nQuantos {}?".format(format_printable_string("dependentes",
                                                                            is_underlined=True)))
                    self.dependents = int(input("Resposta: "))
                    break
                except:
                    display_msg("Desculpe, não entendi...")
                    continue
            
            display_msg("\nVocê paga {}?\nColoque R$0 se não for o caso.".format(format_printable_string(
                                                                    "pensão alimentícia",is_underlined=True)))
            self.pensions = float(convert_number_abrev(\
                                input("Resposta: R$")))
            self.outcome["Pensão alimentícia"] = self.pensions
        else:
            self.dependents = 0
            self.pensions = 0

        display_msg("\nQual o {} que você precisaria {} todo mês?".format(
                                                    format_printable_string(
                                                        "mínimo",is_underlined=True),
                                                    format_printable_string(
                                                        "para se manter",is_underlined=True)))
        self.life_cost = float(convert_number_abrev(\
                            input("Resposta: R$")))
        self.outcome["Custo de vida mensal"] = self.life_cost

        display_msg("\nTodos nós costumamos gastar um pouco com lazer nos fins de semana, certo?"+\
                    "\nQuanto você costuma gastar todo mês {}?".format(format_printable_string(
                                                    "além do valor necessário",is_underlined=True)))
        self.consumption = float(convert_number_abrev(input("Resposta: R$")))
        self.outcome["Consumos extras"] = self.consumption

    def analyzing_profile(self):
        # Time to analyze and give some tips!
        display_msg("\n***********************"+\
            "\nAcho que já consigo traçar seu {} atual. Vamos lá..."\
                .format(format_printable_string("perfil",GREEN)))

        self.fin_planner = MyFinancialPlan(
                            name=self.name, 
                            capital=self.capital, 
                            gross_salary=self.gross_salary,
                            aid_grant=self.aid_grant,
                            life_cost=self.life_cost, 
                            consumption=self.consumption,
                            dependents=self.dependents,
                            pensions=self.pensions)
        self.outcome["INSS"] = self.fin_planner.income_tax.inss
        self.outcome["Imposto de renda"] = self.fin_planner.income_tax.valor_ir

        # Status Summary
        income_summary = "\nTodo mês você recebe:"
        for k in self.income.keys():
            item = "\n\t- {}: ".format(k)
            while len(item) < 29:
                j = item.find(":")
                item = item[:j]+' '+item[j:]
            item = item + print_currency(self.income[k])
            while len(item) < 39:
                j = item.find("$")+1
                item = item[:j]+' '+item[j:]
            income_summary += item
        
        display_msg(income_summary)
        display_msg("Isso totaliza um fluxo positivo de {}/mês".format(
            format_printable_string(print_currency(self.fin_planner.income),GREEN)))

        outcome_summary = "\nTodo mês você gasta com:"
        for k in self.outcome.keys():
            item = "\n\t- {}: ".format(k)
            while len(item) < 29:
                j = item.find(":")
                item = item[:j]+' '+item[j:]
            item = item + print_currency(self.outcome[k])
            while len(item) < 39:
                j = item.find("$")+1
                item = item[:j]+' '+item[j:]
            outcome_summary += item

        display_msg(outcome_summary)
        display_msg("Isso totaliza um fluxo negativo de {}/mês.".format(
            format_printable_string(
                print_currency(self.fin_planner.outcome),RED)))

        result_str = format_printable_string(print_currency(self.fin_planner.income),GREEN)+\
        	 " - " + format_printable_string(print_currency(self.fin_planner.outcome),RED)+" = "
        if self.fin_planner.revenue > 0.0:
            display_msg("\nPelo que vejo, todo mês você consegue um saldo de:\n\t"+\
            			result_str + format_printable_string(print_currency(
            				self.fin_planner.revenue),GREEN,is_bold=True)+"/mês")
        elif self.fin_planner.revenue < 0.0:
            display_msg("\nPelo que vejo, todo mês você gera um prejuízo de:\n\t"+\
            			result_str + format_printable_string(print_currency(
            				self.fin_planner.revenue),RED,is_bold=True)+"/mês")
        else:
            display_msg("\nPelo que vejo, todo mês você fica no {}."\
                .format(format_printable_string("zero a zero",RED,is_bold=True)))

        display_msg("\nAlém disso, você possui:"+\
        			"\n\t- Patrimônio\t: {}".format(format_printable_string(
        				print_currency(self.patrimony),GREEN))+\
        			"\n\t- Dívida\t: -{}".format(format_printable_string(
        				print_currency(self.debt),RED)))
        
        if self.debt > 0:
            if self.capital >= 0:
                display_msg("\nVocê possui patrimônio para pagar suas dívidas. Quite-as!\n"+\
                            "Fazendo isso, você ficará com um capital de {}".format(format_printable_string(
                                print_currency(self.capital),GREEN)))
            else:
                if self.fin_planner.revenue > 0:
                    display_msg("\n{}, foque em pagar suas dívidas!\nUse seu patrimônio para pagar o que conseguir, "\
                                    .format(self.name)+\
                                "\ne depois use seu saldo mensal para ir quitando elas aos poucos.")
                else:
                    if self.consumption > 0:
                        display_msg("\n{} do céu! o.O\"\nEste não é um bom momento para continuar gastando {}".format(
                                        self.name, format_printable_string(print_currency(self.consumption),RED))+\
                                    "\ncom supérfluos! Minimize seus gastos, procure meios de ganhar mais, e"+\
                                    "\n{}!".format(format_printable_string("pague suas dívidas",RED)))
                    else:
                        display_msg("\nEita, {}! o.o\nPrecisaremos que você busque formas de aumentar sua renda, corte gastos e"+\
                                    "\nfoque em {}.".format(format_printable_string("pagar suas dívidas",RED)))

        display_msg("\nLEMBRETE: {}".format(
            format_printable_string(
                self.fin_planner.financial_state.phase_goal(), GREEN, is_underlined=True,)))
        
        self._wait_user()

    def planning_debt_pay_off(self):
        """TODO: Implement this! It may be related to """
        pass

    def planning_emergency_fund(self):
        display_msg("\n***********************")

        if self.capital < 0:
            display_msg("\n{}, vamos começar nossos planos...\n".format(self.name)+\
                        "Mas, por tudo que é mais sagrado, {} de pagar suas dívidas antes!\n".format(
                        format_printable_string("não se esqueça",RED)))
        else:
            display_msg("\n{}, vamos começar nossos planos!\n".format(self.name))

        display_msg("\nEm primeiro lugar, precisamos estar {}, certo?\nPor isso, precisamos ter um {}."\
            .format(format_printable_string("preparados para imprevistos",BLUE),
                    format_printable_string("fundo de emergência",BLUE)))
        display_msg("O recomendável é que você esteja preparado para {} de crise."\
            .format(format_printable_string("6 a 12 meses",RED)))
        
        display_msg("Caso ocorra uma crise, você quer estar preparado para {}?"\
                    .format(format_printable_string("quantos meses",is_underlined=True)))
        self.secure_period = int(convert_number_abrev(input("Resposta: ")))
        if self.secure_period < 6:
            display_msg("\nNão acha {} meses muito pouco?\nVamos...coloque {}.".format(
                        convert_dot_to_comma(self.secure_period),
                        format_printable_string("pelo menos 6 meses",is_underlined=True)))
            self.secure_period = int(convert_number_abrev(input("Resposta: ")))
        self.fin_planner.secure_period = self.secure_period

        display_msg("\nOk. Isso quer dizer que você precisa ter um {} de pelo menos {}."\
            .format(format_printable_string("fundo de emergência", is_bold=True), 
                    format_printable_string(print_currency(
                        self.fin_planner.plan_emergency_fund()),BLUE)))
        
        self._wait_user()

    def planning_manumission(self):
        display_msg("\n***********************\n{}. Agora vamos falar sobre sua {}!".format(
                self.name,
                format_printable_string("liberdade financeira",GREEN)))
        display_msg("\nPara planejarmos com quantos anos você alcançará este objetivo,"+\
                    " precisamos saber sua idade atual.\nQual sua {}?".format(
                        format_printable_string("idade",is_underlined=True)))
        self.age = int(convert_number_abrev(input("Resposta: ")))
        self.fin_planner.update_age(self.age)

        display_msg("\nA {} é quando seus rendimentos passivos conseguem suprir "\
                .format(format_printable_string("liberdade financeira", is_bold=True))+\
              "seus gastos.\nOu seja, você conseguiria {}!".format(
                format_printable_string("se manter mesmo sem trabalhar", GREEN))+\
              "\nSendo assim, poderíamos usar seu próprio valor de custo de vida mensal"+\
              " como sua renda passiva desejada.")
        self.desired_income = self.life_cost

        self._try_new_manumission_plan()

    def _try_new_manumission_plan(self):
        display_msg("\nSua renda passiva desejada está em {} por mês".format(
                        format_printable_string(print_currency(self.desired_income),BLUE))+\
                    "\nDeseja alterar este valor?\n[sim(s) ou não(n)]")
        future_income_option = input("Resposta: ")
        
        # Change desired income
        if future_income_option[0].lower() == "s":
            display_msg("\nCerto. Quanto você quer {} lá no futuro?".format(
                            format_printable_string("receber mensalmente",
                                                    is_underlined=True))+\
                        "\nLembre-se de que tem que ser pelo menos o valor de seu "+\
                        "custo mensal de vida ({})."\
                                            .format(print_currency(self.life_cost)))
            self.desired_income = float(convert_number_abrev(input("Resposta: R$")))

        while self.desired_income < self.life_cost:
            display_msg("\nNa liberdade financeira, "+\
                                    "você tem que receber o suficiente pelo menos para se manter."+\
                                    "\nPor favor, coloque um valor {}.".format(format_printable_string(
                                        "maior que {}".format(format_printable_string(print_currency(
                                            self.life_cost),RED)),
                                        is_underlined=True)))
            self.desired_income = float(convert_number_abrev(input("Resposta: R$")))
        self.fin_planner.update_desired_income(self.desired_income)
        
        # 2 options for planning
        while True:
            display_msg("\nTemos duas maneiras de planejar a sua {}:"\
                    .format(format_printable_string("liberdade financeira",GREEN))+\
                "\n   (1) definindo a idade com qual você gostaria de atingir seu objetivo;"+\
                "\n   (2) definindo quanto você irá investir mensalmente para atingir seu objetivo."+\
                "\n\nDiga-me qual opção você prefere.\n[Digite o número 1 ou 2]")
            plan_option = int(input("Resposta: "))
            if plan_option in [1,2]:
                break
            display_msg("\nOk, vamos lá...")
        
        self._get_manumission_projection(plan_option=plan_option)
    
    def _get_manumission_projection(self, plan_option:int=1):
        if plan_option == 1:
            self.monthly_investment = None
            while True:
                display_msg("\nCerto. Com {} ".format(format_printable_string("quantos anos",
                                                                                is_underlined=True))+\
                            "você gostaria de atingir sua liberdade financeira?")
                self.desired_age = int(input("Resposta: "))
                if self.desired_age > self.age:
                    break
                display_msg("\nUai? Você não deveria escolher uma idade {}?".format(
                    format_printable_string("maior que a sua idade atual",RED)
                ))
        else:
            self.desired_age = None

            if self.fin_planner.revenue <= 0:
                display_msg("\nVocê está sem condições de investir agora..."+\
                            "\nMas, supondo que você consiga enxugar seus gastos e aumentar um pouco "+\
                            "\nsua renda, qual {} ".format(format_printable_string("valor",
                                                                        is_underlined=True))+\
                                "você acredita que seria possível investir todo mês?")
                self.monthly_investment = float(convert_number_abrev(input("Resposta: R$")))
            else:
                while True:
                    display_msg("\nCerto. Qual {} ".format(format_printable_string("valor",
                                                                        is_underlined=True))+\
                                "você gostaria de investir todo mês?")
                    self.monthly_investment = float(convert_number_abrev(input("Resposta: R$")))
                    if self.monthly_investment < self.fin_planner.revenue:
                        break
                    display_msg("\nCuidado, {}. ".format(self.name)+\
                            "Você não pode investir {} todo mês, ".format(format_printable_string(
                                print_currency(self.monthly_investment),RED))+\
                            "sendo que seu saldo mensal é de {}.".format(format_printable_string(
                                print_currency(self.fin_planner.revenue),BLUE)))

        self.desired_patrimony, self.monthly_investment, self.desired_age = \
            self.fin_planner.manumission_point.get_desired_manumission(
                                                    desired_income=self.desired_income,
                                                    monthly_investment=self.monthly_investment,
                                                    desired_age=self.desired_age, 
                                                    start_today=True)

        # Summarizing the plan
        display_msg("\nVocê disse que no futuro, você quer uma renda passiva de {}.".format(
            format_printable_string(print_currency(self.desired_income)))+\
            "\nConsiderando que a taxa de retorno seja em torno da taxa Selic atual ({}%), "\
                .format(str(Selic().get_selic_meta()).replace('.',','))+\
            "\nentão você teria que alcançar um patrimônio de {}".format(format_printable_string(
                print_currency(self.desired_patrimony), GREEN, is_bold=True))
        )
        if plan_option == 1:
            display_msg("\nSe você quer atingir sua liberdade financeira com {} de idade, ".format(
                    format_printable_string("{} anos".format(self.desired_age),BLUE))+\
                "\nentão você terá que investir mensalmente {}".format(format_printable_string(
                    print_currency(self.monthly_investment),GREEN))
            )
        else:
            display_msg("\nSe você vai investir {} mensalmente, ".format(
                format_printable_string(print_currency(self.monthly_investment),BLUE))+\
                "\nentão você atingirá sua liberdade financeira com {}.".format(
                    format_printable_string("{} anos".format(self.desired_age),GREEN)))
                
        self._wait_user()
        
        diff = self.monthly_investment - self.fin_planner.revenue
        if diff > 0:
            display_msg("\nParece que você teria que investir {} além do seu saldo mensal."\
                            .format(format_printable_string(print_currency(diff),RED))+\
                        "\nPara isso, você precisará focar em {}.".format(
                            format_printable_string("aumentar sua renda mensal", GREEN))+\
                        "\nEnquanto isso, podemos projetar em quanto tempo você conseguiria"+\
                        " \n a sua meta se investisse uma quantia dentro de sua realidade."+\
                        "\n\nVocê quer descobrir isso?\n[Responda com sim(s) ou não(n)]")
            decision = input("Resposta: ")
            if decision[0].lower() == "s":
                self._get_manumission_projection(plan_option=2)


def _routine(simulator):
    simulator.knowing_the_user_income()
    simulator.knowing_the_finance_situation()
    simulator.analyzing_profile()
    simulator.planning_emergency_fund()
    simulator.planning_manumission()

    display_msg("\nDepois desta simulação, você pode ter notado que é sim {}.".format(
                    format_printable_string("possível alcançar a liberdade financeira",GREEN)
                )+\
                "\nTambém, você viu a importância de saber {}, de {} e,\nlogicamente, esforçar-se para {}. "\
                    .format(
                        format_printable_string("gastar bem",BLUE),
                        format_printable_string("investir com consistência",BLUE),
                        format_printable_string("ganhar mais",BLUE)
                    )+\
                "Porém, nunca vá pela {}, e seja {}!".format(
                    format_printable_string("ganância",RED),
                    format_printable_string("paciente",BLUE)
                ))
    
    display_msg("\nGostaria de tentar fazer {}? :D".format(format_printable_string("mais uma simulação",BLUE))+\
                "\nFicarei muito feliz de continuar te ajudando!\n[Responda com sim(s) ou não(n)]")
    decision = input("Resposta: ")
    if decision[0].lower() == "s":
        _routine(simulator)

def main():
    simulator = PlanSimulator()
    simulator.starting_message()
    _routine(simulator)

if __name__ == "__main__":
    main()