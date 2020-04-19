"""
Author: Luiz Ricardo Takeshi Horita
Date: 2020-04-18
"""
from typing import Dict, List, Union
from collections import defaultdict
from math import *

from bc.bancocentral import Inflacao, Selic, Poupanca
from pynance.financial_utils import *
from pynance.base_classes import *
from pynance.gov_taxes import *

class MyFinancialPlan():
    def __init__(self, 
                name:str="",
                age:int=0,
                capital:float=0.0,
                debt:float=0.0,
                gross_salary:float=0.0,
                aid_grant:float=0.0,
                dependents:int=0,
                pensions:float=0.0,
                tax_type:str="simplificado", 
                life_cost:float=0.0,
                consumption:float=0.0,
                desired_income:float=None,
                secure_period:int=12,
                passive_interest:float=None
                ):
        super().__init__()
        self.name = name
        self.age = age

        # Financial Status
        self.capital = capital
        self.debt = debt
        self.gross_salary = gross_salary
        self.aid_grant = aid_grant
        self.dependents = dependents
        self.pensions = pensions
        self.tax_type = tax_type
        self.life_cost = life_cost
        self.consumption = consumption

        # Emergency Fund
        self.secure_period = secure_period

        # Manumission Plan
        self.desired_income = desired_income
        if passive_interest:
            self.passive_interest = passive_interest
        else:
            # Get the current Selic goal
            self.passive_interest = (1+Selic().get_selic_meta()/100)**(1/12) - 1

        self.update_finance_status()

    def update_finance_status(self):
        self.income_tax = ImpostoDeRenda(salario_bruto=self.gross_salary, 
                                        renda_isenta=self.aid_grant,
                                        dependentes=self.dependents, 
                                        pensoes_dependentes=self.pensions, 
                                        tipo=self.tax_type)
        self.gov_taxes = self.income_tax.inss + self.income_tax.valor_ir
        self.income = self.gross_salary + self.aid_grant
        self.outcome = self.gov_taxes + self.life_cost + self.pensions + self.consumption
        self.revenue = self.get_revenue()

        self.financial_state = FinancialState(
                                            income=self.revenue, 
                                            outcome=(self.life_cost+self.consumption),
                                            capital=self.capital,
                                            debt=self.debt)

        self.plan_emergency_fund()

        self.manumission_point = MyManumission( 
                                               current_capital=self.capital,
                                               life_cost=self.life_cost,
                                               desired_income=self.desired_income, 
                                               current_age=self.age,
                                               passive_interest=self.passive_interest)

    def update_age(self, age):
        self.age = age
        self.manumission_point.current_age = age
    
    def update_desired_income(self, desired_income):
        self.desired_income = desired_income
        self.manumission_point.desired_income = desired_income
    
    def update_life_cost(self, life_cost):
        self.life_cost = life_cost
        self.manumission_point.life_cost
    
    def update_capital(self, capital):
        self.capital = capital
        self.manumission_point.current_capital = capital
    
    def update_debt(self, debt):
        self.debt = debt
    
    def update_secure_period(self, secure_period):
        self.secure_period = secure_period

    def get_revenue(self):
        return (self.income - self.outcome)
    
    def _there_is_debt(self):
        return (self.debt > 0)
    
    def pay_off_debts(self):
        """TODO: Implement method to plan debt pay off."""
        # if self._there_is_debt():
        #     return self.capital - self.debt
        pass

    def get_financial_state(self):
        return self.financial_state.phase_goal()
    
    def plan_emergency_fund(self, secure_period=None):
        if secure_period == None:
            secure_period = self.secure_period
        self.emergency_fund = self.life_cost*secure_period
        return self.emergency_fund


