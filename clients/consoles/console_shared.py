from colorama import Fore, Style
from datetime import date
from exceptions import exceptions


def decorate_message(func):
    def wrapper(message, type="informative", option=""):
        if type == "debug":
            print(f"{Fore.YELLOW}{Style.BRIGHT}{func(message, type='success')}{Style.RESET_ALL}")
        elif type == "error":
            print(f"{Fore.RED}{Style.BRIGHT}{func(message, type='error')}{Style.RESET_ALL}")
        elif type == "explore":
            print(f"{Fore.MAGENTA}{Style.BRIGHT}{func(message, type='explore')}{Style.RESET_ALL}")
        elif type == "success":
            print(f"{Fore.GREEN}{Style.BRIGHT}{func(message, type='success')}{Style.RESET_ALL}")
        else:
            if option == "end":
                print(f"{Fore.CYAN}{Style.BRIGHT}{func(message)}{Style.RESET_ALL}", end="")
            else:
                return f"{Fore.CYAN}{Style.BRIGHT}{func(message)}{Style.RESET_ALL}"
    return wrapper


@decorate_message
def print_message(message, type="informative", option=""):
    return message


def set_a_date():
    temp_date_dict = {"year": "", "month": "", "day": ""}
    for key in temp_date_dict.keys():
        answer = input(f"{key}: ")
        if not answer.isdigit():
            raise exceptions.NotDigitException()
        temp_date_dict[key] = int(answer)
    return date(
        year=temp_date_dict["year"],
        month=temp_date_dict["month"],
        day=temp_date_dict["day"])
