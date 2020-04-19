"""
Author: Luiz Ricardo Takeshi Horita
Date: 2020-04-18
"""

import signal

PURPLE = "\033[95m"
CYAN = "\033[96m"
DARKCYAN = "\033[36m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
END = "\033[0m"

def format_printable_string(string, color=None, is_bold=False, is_underlined=False):
    format_flags = ""
    if is_bold:
        format_flags += BOLD
    if is_underlined:
        format_flags += UNDERLINE
    if color:
        format_flags += color
    return format_flags + string + END

def print_currency(value, currency_symbol="R$"):
    amount = convert_dot_to_comma("{:.2f}".format(value))
    i = amount.find(",")
    while True:
        i -= 3
        if i <= 0:
            break
        amount = amount[:i]+"."+amount[i:]
    return currency_symbol+amount

def separate_digit_and_nondigit(str_value):
    d = 0
    while (str_value[d].isdigit() or str_value[d] == "."):
        d += 1
        if d >= len(str_value):
            break
        continue
    return str_value[:d], str_value[d:]

def convert_number_abrev(str_value):
    if str_value == "":
        return 0.0
    
    str_value.replace(" ","")
    str_value = convert_comma_to_dot(str_value)
    value, abrev_str  = separate_digit_and_nondigit(str_value)
    
    if abrev_str == "":
        return float(str_value)
    elif abrev_str in ["k", "mil"]:
        return float(value)*(10**3)
    elif abrev_str in ["M", "Mi", "mi"]:
        return float(value)*(10**6)
    elif abrev_str in ["G", "B", "Bi", "bi"]:
        return float(value)*(10**9)
    elif abrev_str in ["T", "Tri", "tri"]:
        return float(value)*(10**12)
    return None

def convert_comma_to_dot(value):
    return str(value).replace(",",".")

def convert_dot_to_comma(value):
    return str(value).replace(".",",")

def input_or_timeout(timeout, msg=""):
    def nothing(sig, frame): pass
    signal.signal(signal.SIGALRM, nothing)
    signal.alarm(timeout)
    try:
        input(msg)
        signal.alarm(0)
    except (IOError, EOFError): pass