"""
Author:Luiz Ricardo Takeshi Horita
Date:2020-04-12
"""
from typing import Dict, List, Union
from collections import defaultdict
from math import *

from bc.bancocentral import Inflacao, Selic, Poupanca
from pynance.financial_utils import CompoundInterest
from pynance.utils import print_currency



class FinancialState(object):
    def __init__(self, income:float, outcome:float, capital:float, debt:float):
        super().__init__()
        self.income = income
        self.outcome = outcome
        self.revenue = income - outcome
        self.capital = capital - debt

    def phase(self):
        if (self.revenue <= 0 and self.capital < 0) \
        or (self.revenue > 0 and self.capital < 0):
            return 1
        elif self.revenue < 0 and self.capital >= 0:
            return 2
        elif self.revenue > 0 and self.revenue <= 2*self.outcome \
        and  self.capital >= 0:
            return 3
        else:
            return 4


    def phase_goal(self):
        goals = {
            1: "seu objetivo principal é ganhar mais e liquidar suas dívidas!",
            2: "seu objetivo principal é ganhar mais!",
            3: "seu objetivo principal é ganhar mais e investir melhor!",
            4: "seu objetivo principal é investir e gastar melhor!",
        } 
        return goals[self.phase()]

class EmergencyFund(object):
    def __init__(self, life_cost:float=0.0, secure_period:int=12):
        super().__init__()
        self.life_cost = life_cost
        self.secure_period = secure_period
        self.emergency_fund = self.life_cost*self.secure_period
    
    def __str__(self):
        return "Meu custo mensal: {}.\n".format(print_currency(self.life_cost))+\
               "Período de segurança: {} meses.\n".format(self.secure_period)+\
               "Fundo de emergência: {}.\n".format(print_currency(self.emergency_fund))

    def __call__(self, life_cost, secure_period:int=12):
        return life_cost*secure_period
    
    def print_goal(self):
        print("Objetivo: {}x(Custo de Vida)".format(self.secure_period))

    def print_characteristics(self):
        print("Aplicação de:"+\
            "\n   * Baixo risco;"+\
            "\n   * Alta liquidez;"+\
            "\n   * Baixa rentabilidade.")

    def options(self):
        print("Opções:"+\
            "\n   * Tesouro Direto (TD);"+\
            "\n   * Conta corrente remunerada;"+\
            "\n   * Crédito de Depósito Bancário (CDB)"+\
            "\n   * Fundos de investimento")

class MyManumission(CompoundInterest):
    def __init__(self, 
                current_capital:float,
                life_cost:float,
                desired_income:float=None, 
                monthly_investment:float=None,
                current_age:int=0, 
                passive_interest:float=None):
        super().__init__()
        self.current_capital = current_capital
        self.life_cost = life_cost
        if desired_income == None:
            desired_income = life_cost
        assert desired_income >= life_cost,\
            "Sua renda passiva desejada ({}) deve cobrir pelo menos seu custo de vida ({})!"\
            .format(print_currency(desired_income), print_currency(life_cost))
        self.desired_income = desired_income
        self.current_age = current_age
        if passive_interest:
            self.passive_interest = passive_interest
        else:
            # Get the current Selic goal
            self.passive_interest = (1+Selic.get_selic_meta()/100)**(1/12) - 1
    
    def __str__(self):
        return "Renda passiva desejada: {}.\n".format(print_currency(self.desired_income))+\
               "Patrimônio necessário: {}.\n".format(print_currency(self.desired_patrimony))+\
               "Taxa de retorno estimado: {:.2f}%.\n".format(self.passive_interest*100)
    
    def get_manumission(self,
                        monthly_investment:float=None,
                        desired_age:int=None,
                        current_capital:float=None,
                        life_cost:float=None,
                        passive_interest:float=None,
                        investment_interest:float=None,
                        start_today:bool=True):
        assert (monthly_investment != None or desired_age != None),\
               "Por favor, me diga quanto você pretende investir mensalmente "+\
               "ou com quantos anos você pretende atingir sua liberdade financeira."
        if current_capital == None:
            current_capital = self.current_capital
        if life_cost == None:
            life_cost = self.life_cost
        if passive_interest == None:
            passive_interest = self.passive_interest
        if investment_interest == None:
            investment_interest = self.passive_interest

        return self.get_desired_manumission(
            desired_income=life_cost,
            monthly_investment=monthly_investment,
            desired_age=desired_age,
            current_capital=current_capital,
            life_cost=life_cost,
            passive_interest=passive_interest,
            investment_interest=investment_interest,
            start_today=start_today
        )
    
    def get_desired_manumission(self,
                                desired_income:float,
                                monthly_investment:float=None,
                                desired_age:int=None,
                                current_capital:float=None,
                                life_cost:float=None,
                                passive_interest:float=None,
                                investment_interest:float=None,
                                start_today:bool=True):
        assert (monthly_investment != None or desired_age != None),\
               "Por favor, me diga quanto você pretende investir mensalmente "+\
               "ou com quantos anos você pretende atingir seu objetivo."
        if life_cost == None:
            life_cost = self.life_cost
        assert desired_income >= life_cost,\
            "Sua renda passiva desejada ({}) deve cobrir pelo menos seu custo de vida ({})!"\
            .format(print_currency(desired_income), print_currency(life_cost))
        if current_capital == None:
            current_capital = self.current_capital
        if passive_interest == None:
            passive_interest = self.passive_interest
        if investment_interest == None:
            investment_interest = self.passive_interest
        desired_patrimony = self.get_my_desired_value(desired_income, passive_interest)

        if monthly_investment:
            desired_age = self.get_age_of_achievement(
                                                    pmt=monthly_investment,
                                                    capital=current_capital,
                                                    desired_patrimony=desired_patrimony,
                                                    interest=investment_interest,
                                                    start_today=start_today)
        elif desired_age:
            monthly_investment = self.get_pmt_for_fv(
                                                    desired_fv=desired_patrimony,
                                                    capital=current_capital,
                                                    period=(desired_age-self.current_age),
                                                    interest=investment_interest,
                                                    start_today=start_today)
        return desired_patrimony, monthly_investment, desired_age

    def get_my_desired_value(self, 
                                desired_income:float=None, 
                                passive_interest:float=None):
        if desired_income == None:
            desired_income = self.desired_income
        if passive_interest == None:
            # Get the current Selic goal
            passive_interest = self.passive_interest
        return (1/passive_interest)*desired_income

    def get_age_of_achievement(self,  
                                pmt:float, 
                                capital:float=None, 
                                current_age:int=None,
                                desired_patrimony:float=None, 
                                interest:float=None, 
                                start_today:bool=True):
        """
        Returns the age when you will achieve your manumission.

        Parameters:
            current_age (int):         Your current age.
            desired_patrimony (float): The desired future patrimony.
            capital (float):           The current capital.
            pmt (float):               The value of regular investiments.
            interest (float):          Interest (%).
            start_today (bool):        If the payments will start today (True) or in the next period (False).
        
        Returns:
            final age (float):     The age that the desired patrimony will be achieved.
        """
        if capital == None:
            capital = self.current_capital
        if current_age == None:
            current_age = self.current_age
        if desired_patrimony == None:
            desired_patrimony = self.desired_patrimony
        if interest == None:
            interest = self.passive_interest
        period_of_investiment = self.get_time_for_fv(desired_fv=desired_patrimony,
                                                     capital=capital, 
                                                     pmt=pmt, 
                                                     interest=interest, 
                                                     start_today=start_today)
        if self.time_unit == "month":
            period_of_investiment = period_of_investiment/12
        return (current_age + int(period_of_investiment))


if __name__ == "__main__":
    # EmergencyFund testing
    print("\n*************************")
    my_emergency_fund = EmergencyFund()
    print(my_emergency_fund.__str__())
    print("Fundo de emergência recalculado: R${:.2f}".format(my_emergency_fund(2000,12)))

    # MyManumission testing
    print("\n*************************")
    my_manumission = MyManumission(desired_income=5000, passive_interest=0.003333)
    print(my_manumission.__str__())
    print("Você alcançará sua alforria aos {:.2f} anos.".\
            format(my_manumission.age_of_retirement(current_age=30, pmt=3000, capital=100000)))