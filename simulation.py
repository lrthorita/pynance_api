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

class PlanSimulator:
    def __init__(self):
        super().__init__()
        self.income = {}
        self.outcome = {}

    def starting_message(self):
        print("\nOlá! Sou o {}, e vou te ajudar a planejar sua liberdade financeira!".format(
            format_printable_string("PyNance", BLUE)
        ))
        input("Bora? :D\n[Aperte ENTER para continuar]")

    def knowing_the_user(self):
        self.name = input("\n***********************"+\
                        "\nQual seu nome?\nResposta: ")
        print("{}".format(format_printable_string("\nMuito prazer, {}!".format(self.name),BLUE)))

        while True:
            self.income_source = int(input("\nQual sua(s) fonte(s) de renda atualmente?"+\
                                        "\n[Digite o número da opção]\n"+\
                                        "\n  (1) salário"+\
                                        "\n  (2) algum tipo de bolsa isento de imposto"+\
                                        "\n  (3) ambos\n\nResposta: "))
            if self.income_source in [1,2,3]:
                break
            print("\nDesculpe. {}".format(format_printable_string(
                    "Poderia tentar novamente?",RED)))

    def _getting_incomes(self):
        if self.income_source == 1:
            self.gross_salary = float(convert_number_abrev(
                                        input("\nQual seu {}?\nResposta: R$"\
                                            .format(format_printable_string(
                                                "salário bruto",is_underlined=True)))))
            self.income["Salário bruto"] = self.gross_salary
            self.aid_grant = 0.0
        if self.income_source == 2:
            self.gross_salary = 0.0
            self.aid_grant = float(convert_number_abrev(
                                        input("\nQual valor da sua {}?\nResposta: R$"\
                                            .format(format_printable_string(
                                                "bolsa/auxílio",is_underlined=True)))))
            self.income["Bolsa/auxílio"] = self.aid_grant
        if self.income_source == 3:
            self.gross_salary = float(convert_number_abrev(
                                        input("\nQual seu {}?\nResposta: R$"\
                                            .format(format_printable_string(
                                                "salário bruto",is_underlined=True)))))
            self.income["Salário bruto"] = self.gross_salary
            self.aid_grant = float(convert_number_abrev(
                                        input("\nQual valor da sua {}?\nResposta: R$"\
                                            .format(format_printable_string(
                                                "bolsa/auxílio",is_underlined=True)))))
            self.income["Bolsa/auxílio"] = self.aid_grant

    def knowing_the_finance_situation(self):
        print("\n***********************"+\
            "\nCerto, {}. Primeiro, vamos descobrir sua {} hoje."\
                .format(self.name, format_printable_string("situação financeira",BLUE,is_bold=True)))
        self.patrimony = float(convert_number_abrev(
                                input("\nQuanto você tem de {} hoje?\nResposta: R$"\
                                    .format(format_printable_string(
                                            "patrimônio", is_underlined=True)))))
        self.debt = float(convert_number_abrev(
                            input("\nE quanto você tem de {}?\nResposta: -R$"\
                                    .format(format_printable_string(
                                            "dívida", is_underlined=True)))))
        self.capital = self.patrimony - self.debt

        self._getting_incomes()

        self.is_parent = input("\nVocê possui {} (filhos, pais, avós ou bisavós)?"\
                                   .format(format_printable_string(
                                       "dependentes",is_underlined=True))+\
                               "\n[Responda com sim(s) ou não(n)]\nResposta: ")
        while self.is_parent[0].lower() not in ['s', 'n']:
            self.is_parent = input("\nPor favor, responda sim(s) ou não(n): ")
        if self.is_parent[0].lower() == 's':
            while True:
                try:
                    self.dependents = int(input("\nQuantos dependentes?\nResposta: "))
                    break
                except:
                    print("Desculpe, não entendi...")
                    continue
            self.pensions = float(convert_number_abrev(\
                                input("\nVocê paga {}?\nColoque R$0 se não for o caso."\
                                      .format(format_printable_string(
                                            "pensão alimentícia",is_underlined=True))+\
                                      "\nResposta: R$")))
            self.outcome["Pensão alimentícia"] = self.pensions
        else:
            self.dependents = 0
            self.pensions = 0

        self.life_cost = float(convert_number_abrev(\
                            input("\nQual o {} que você precisaria {} todo mês?\nResposta: R$"\
                                .format(
                                    format_printable_string(
                                        "mínimo",is_underlined=True),
                                    format_printable_string(
                                        "para se manter",is_underlined=True)))))
        self.outcome["Custo de vida mensal"] = self.life_cost

        print("\nTodos nós costumamos gastar um pouco com lazer nos fins de semana, certo?")
        self.consumption = float(convert_number_abrev(
                                input("Quanto você costuma gastar todo mês {}?\nResposta: R$"\
                                    .format(format_printable_string(
                                        "além do valor necessário",is_underlined=True)))))
        self.outcome["Consumos extras"] = self.consumption

    def analyzing_profile(self):
        # Time to analyze and give some tips!
        print("\n***********************"+\
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
        print("\nSeu salário bruto é de: {}".format(
            format_printable_string(print_currency(self.gross_salary),GREEN)))

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

        print(outcome_summary)
        print("Isso totaliza um fluxo negativo de {} por mês.".format(
            format_printable_string(
                print_currency(self.fin_planner.outcome),RED)))

        if self.fin_planner.revenue > 0.0:
            print("\nPelo que vejo, todo mês você consegue um saldo de {}."\
                .format(format_printable_string(
                    print_currency(self.fin_planner.revenue),GREEN,is_bold=True)))
        elif self.fin_planner.revenue < 0.0:
            print("\nPelo que vejo, todo mês você gera um prejuízo de {}."\
                .format(format_printable_string(
                    print_currency(self.fin_planner.revenue).replace('-',''),RED,is_bold=True)))
        else:
            print("\nPelo que vejo, todo mês você fica no {}."\
                .format(format_printable_string("zero a zero",RED,is_bold=True)))

        print("Isso quer dizer que, atualmente, {}.".format(
            format_printable_string(
                self.fin_planner.financial_state.phase_goal(), GREEN, is_underlined=True,)))
        
        input_or_timeout(10, "\nVou esperar você ler... :)\n[Aperte ENTER quando quiser continuar...]")

    def planning_debt_pay_off(self):
        """TODO: Implement this! It may be related to """
        pass

    def planning_emergency_fund(self):
        print("\n***********************"+\
            "\n{}, vamos começar nossos planos!\n".format(self.name)+\
            "\nEm primeiro lugar, precisamos estar {}, certo? Por isso, precisamos ter um {}."\
            .format(format_printable_string("preparados para imprevistos",BLUE),
                    format_printable_string("fundo de emergência",BLUE)))
        print("O recomendável é que você esteja preparado para {} de crise."\
            .format(format_printable_string("6 a 12 meses",RED)))
        
        self.secure_period = int(convert_number_abrev(
                             input("Caso ocorra uma crise, você quer estar preparado para {}?"\
                                 .format(format_printable_string(
                                        "quantos meses",is_underlined=True))+\
                                "\nResposta: ")))
        if self.secure_period < 6:
            self.secure_period = int(convert_number_abrev(
                input("\nNão acha {} meses muito pouco?\nVamos...coloque {}."\
                    .format(convert_dot_to_comma(self.secure_period),
                            format_printable_string("pelo menos 6 meses",is_underlined=True))+\
                    "\nResposta: ")))
        self.fin_planner.secure_period = self.secure_period

        print("\nOk. Isso quer dizer que você precisa ter um {} de pelo menos {}."\
            .format(format_printable_string("fundo de emergência", is_bold=True), 
                    format_printable_string(print_currency(
                        self.fin_planner.plan_emergency_fund()),BLUE)))
        
        input_or_timeout(5, "\nVou esperar você ler... :)\n[Aperte ENTER quando quiser continuar...]")

    def planning_manumission(self):
        print("\n***********************\n{}. Agora vamos falar sobre sua {}!".format(
                self.name,
                format_printable_string("liberdade financeira",GREEN)))
        print("\nPara planejarmos com quantos anos você alcançará este objetivo,"\
                +" precisamos saber sua idade atual.")
        self.age = int(convert_number_abrev(
                        input("Qual sua {}?\nResposta: "\
                            .format(format_printable_string("idade",is_underlined=True)))))
        self.fin_planner.update_age(self.age)

        print("\nA {} é quando seus rendimentos passivos conseguem suprir "\
                .format(format_printable_string("liberdade financeira", is_bold=True))+\
              "seus gastos.\nOu seja, você conseguiria {}!".format(
                format_printable_string("se manter mesmo sem trabalhar", GREEN)))
        future_income_option = input("Sendo assim, poderíamos manter o valor do seu custo"+\
                                    " de vida mensal como sua renda passiva desejada?"+\
                                    "\n[sim(s) ou não(n)] [Caso queira alterar sua "+\
                                    "renda passiva desejada, responda 'n']\nResposta: ")

        if future_income_option[0].lower() == "s":
            self.desired_income = self.life_cost
        else:
            self.desired_income = float(convert_number_abrev(\
                                    input("\nLá no futuro, quanto você quer receber mensalmente de {}?"\
                                            .format(format_printable_string(
                                                    "renda passiva",
                                                    is_underlined=True))+\
                                        "\nLembre-se de que tem que ser pelo menos "+\
                                        "o valor de seu custo mensal de vida ({})."\
                                            .format(print_currency(self.life_cost))+\
                                        "\nResposta: R$")))

        while self.desired_income < self.life_cost:
            self.desired_income = float(convert_number_abrev(\
                                    input("\nNa liberdade financeira, "+\
                                    "você tem que receber o suficiente pelo menos para se manter."+\
                                    "\nPor favor, coloque um valor {}.\nResposta: R$".format(
                                        format_printable_string(
                                            "maior que {}".format(
                                                format_printable_string(
                                                    print_currency(self.life_cost),RED)),
                                            is_underlined=True)))))
        self.fin_planner.update_desired_income(self.desired_income)

        self._plan_manumission()

    def _plan_manumission(self):
        while True:
            print("\nTemos duas maneiras de planejar a sua {}:"\
                    .format(format_printable_string("liberdade financeira",GREEN))+\
                "\n   (1) definindo a idade com qual você gostaria de atingir seu objetivo;"+\
                "\n   (2) definindo quanto você irá investir mensalmente para atingir seu objetivo.")
            plan_option = int(input("\nDiga-me qual opção você prefere."+\
                                    "\n[Digite o número 1 ou 2]\nResposta: "))
            if plan_option in [1,2]:
                break
            print("\nOk, vamos lá...")

        if plan_option == 1:
            self.monthly_investment = None
            while True:
                self.desired_age = int(input("\nCerto. Com {} ".format(
                                        format_printable_string("quantos anos",is_underlined=True))+\
                                    "você gostaria de atingir sua liberdade financeira?\nResposta: "))
                if self.desired_age > self.age:
                    break
                print("\nUai? Você não deveria escolher uma idade {}?".format(
                    format_printable_string("maior que a sua idade atual",RED)
                ))
        else:
            self.desired_age = None
            while True:
                self.monthly_investment = float(convert_number_abrev(input(
                                        "\nCerto. Qual {} ".format(format_printable_string(
                                            "valor",is_underlined=True))+\
                                        "você gostaria de investir todo mês?\nResposta: R$")))
                if self.monthly_investment < self.fin_planner.revenue:
                    break
                print("\nCuidado, {}.".format(self.name)+\
                        "Você não pode investir {} todo mês, ".format(format_printable_string(
                            print_currency(self.monthly_investment),RED))+\
                        "sendo que seu saldo mensal é de {}".format(format_printable_string(
                            print_currency(self.fin_planner.revenue),BLUE)))

        # self.manumission_patrimony, self.monthly_investment, self.manumission_age = \
        #     self.fin_planner.manumission_point.get_manumission(
        #                                             monthly_investment=self.monthly_investment,
        #                                             desired_age=self.desired_age, 
        #                                             start_today=True)

        self.desired_patrimony, self.monthly_investment, self.desired_age = \
            self.fin_planner.manumission_point.get_desired_manumission(
                                                    desired_income=self.desired_income,
                                                    monthly_investment=self.monthly_investment,
                                                    desired_age=self.desired_age, 
                                                    start_today=True)

        # Summarizing the plan
        print("\nVocê disse que no futuro, você quer uma renda passiva de {}.".format(
            format_printable_string(print_currency(self.desired_income)))+\
            "\nConsiderando que a taxa de retorno seja em torno da taxa Selic atual ({}%), "\
                .format(str(Selic().get_selic_meta()).replace('.',','))+\
            "\nentão você teria que alcançar um patrimônio de {}".format(format_printable_string(
                print_currency(self.desired_patrimony), GREEN, is_bold=True))
        )
        if plan_option == 1:
            print("\nSe você quer atingir sua liberdade financeira com {}, ".format(
                    format_printable_string("{} anos".format(self.desired_age),BLUE))+\
                "\nentão você terá que investir mensalmente {}".format(format_printable_string(
                    print_currency(self.monthly_investment),GREEN))
            )
        else:
            print("\nSe você vai investir {} mensalmente, ".format(
                format_printable_string(print_currency(self.monthly_investment),BLUE))+\
                "\nentão você atingirá sua liberdade financeira com {}.".format(
                    format_printable_string("{} anos".format(self.desired_age),GREEN)))
                
        input_or_timeout(10, "\nVou esperar você ler... :)\n[Aperte ENTER quando quiser continuar...]")

def main():
    simulation = PlanSimulator()

    # Sequence
    simulation.starting_message()
    simulation.knowing_the_user()
    simulation.knowing_the_finance_situation()
    simulation.analyzing_profile()
    simulation.planning_emergency_fund()
    simulation.planning_manumission()

if __name__ == "__main__":
    main()