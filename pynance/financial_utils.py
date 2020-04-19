#!/usr/bin/python
# -- coding: utf-8 --
"""
Author: Luiz Ricardo Takeshi Horita
Date: 2020-04-12
"""
from typing import Dict, List, Union
from collections import defaultdict
from math import *

class CompoundInterest():
    def __init__(self, interest: float=0.0, period: int=0, time_unit: str='month'):
        self.interest = interest
        self.period = period
        self.time_unit = time_unit
    
    def _get_interest(self, initial_value, interest, period):
        return initial_value*(1 + interest)**period

    def get_fv(self, capital: float=0.0, payments: List[float]=[], period: int=0, interest: float=0.0):
        """
        Returns the computed future value.

        Parameters:
            capital (float):        The initial capital.
            payments (list(float)): The cash flow.
            period (int):           Period of interest.
            interest (float):       Interest (%).
        
        Returns:
            future value (float):   The computed future value.
        """
        if interest == 0.0:
            interest = self.interest
        if period == 0:
            period == self.period
        assert period >= len(payments), \
        'The number of payments ({}) cannot be greater than the period of interest ({}).'.format(len(payments),period)

        # Compute the future value of the capital
        capital_fv = self._get_interest(capital, interest, period)

        # Compute the future value of the cash flow
        payments_fv = 0.0
        for n, p in enumerate(payments):
            payments_fv += self._get_interest(p, interest, period-n)
        
        # Compute total amount of the future value
        return capital_fv + payments_fv

    def get_fv_from_regular_pmt(self, regular_pmts: float=0.0, period: int=0, interest: float=0.0, start_today: bool=False):
        """
        Returns the computed future value.

        Parameters:
            regular_pmts (float):   Value of the regular payments.
            period (int):           Period of interest.
            interest (float):       Interest (%).
            start_today (bool):     If the payments will start today (True) or in the next period (False).
        
        Returns:
            future value (float):   The computed future value.
        """
        if interest == 0.0:
            interest = self.interest
        if period == 0:
            period == self.period
        
        if start_today:
            return self.get_fv(payments=[regular_pmts]*period, period=period, interest=interest)
        else:
            pmt = [0]
            pmt.extend([regular_pmts]*(period-1))
            return self.get_fv(payments=pmt, period=period, interest=interest)
        
    def get_pmt_for_fv(self, desired_fv: float=0.0, capital: float=0.0, period: int=0, interest: float=0.0, start_today: bool=True):
        """
        Returns the computed future value.

        Parameters:
            desired_fv (float):     The desired future value
            capital (float):        Current capital.
            period (int):           Period of interest.
            interest (float):       Interest (%).
            start_today (bool):     If the payments will start today (True) or in the next period (False).
        
        Returns:
            regular payments (float):   The computed regular payments.
        """
        if interest == 0.0:
            interest = self.interest
        if period == 0:
            period == self.period
        assert desired_fv > 0.0, 'The desired future value must be greater than zero.'

        capital_fv = self.get_fv(capital=capital, period=period, interest=interest)
        if start_today:
            return (desired_fv-capital_fv)*interest/(((1+interest)**period - 1)*(1+interest))
        else:
            return (desired_fv-capital_fv)*interest/(((1+interest)**(period-1) - 1)*(1+interest))

    def get_time_for_fv(self, desired_fv: float=0.0, capital: float=0.0, pmt: float=0.0, interest: float=0.0, start_today: bool=True):
        """
        Returns the computed future value.

        Parameters:
            desired_fv (float):     The desired future value
            capital (float):        Current capital.
            pmt (float):            The value of regular payments.
            interest (float):       Interest (%).
            start_today (bool):     If the payments will start today (True) or in the next period (False).
        
        Returns:
            period (float):         The computed period of time to achieve the desired future value.
        """
        if interest == 0.0:
            interest = self.interest
        assert pmt > 0.0, 'The regular payments must be greater than zero.'
        assert desired_fv > 0.0, 'The desired future value must be greater than zero.'

        pmt_factor = pmt*(1+interest)
        period = log((desired_fv*interest+pmt_factor)/(capital*interest+pmt_factor))/log(1+interest)
        if start_today:
            return round(period)
        else:
            return round(period)+1


if __name__ == "__main__":
    
    # CompoundInterest testing
    print('\n*************************')
    ci = CompoundInterest()
    print('Future value: {}'.format(ci.get_fv(0, [10,10,10], 3, 0.1)))
    print('Future value: {}'.format(ci.get_fv_from_regular_pmt(10,3,0.1,True)))
    print('Regular payments: {}'.format(ci.get_pmt_for_fv(1000000,0,10,0.10,False)))
    print('Time of investment: {}'.format(ci.get_time_for_fv(1000000,0,66945.95,0.10,False)))