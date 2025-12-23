import sys
from enum import Enum

# I found this online from a reddit thread..
def found_online_input(prompt: str) -> str:
    print(f"{prompt}", end="")
    return sys.stdin.readline().rstrip("")

# decided to make a list of colors
class Color(Enum):
    BLACK   = "\033[30m"
    RED     = "\033[31m"
    GREEN   = "\033[32m"
    YELLOW  = "\033[33m"
    BLUE    = "\033[34m"
    PURPLE  = "\033[35m"
    CYAN    = "\033[36m"
    WHITE   = "\033[37m"
    LIGHT_BLACK   = "\033[90m"
    LIGHT_RED     = "\033[91m"
    LIGHT_GREEN   = "\033[92m"
    LIGHT_YELLOW  = "\033[93m"
    LIGHT_BLUE    = "\033[94m"
    LIGHT_PURPLE  = "\033[95m"
    LIGHT_CYAN    = "\033[96m"
    LIGHT_WHITE   = "\033[97m"
    RESET = "\033[0m"

    def __init__(self, color: str):
        self.color = color

class Logger:
    class LogLevel(Enum):
        DEBUG = (1, Color.PURPLE.color)
        INFO = (2, Color.CYAN.color)
        WARNING = (3, Color.YELLOW.color)
        ERROR = (4, Color.RED.color)

        def __init__(self, level: int, color: str):
            self.level = level
            self.color = color

    def __init__(self, level: LogLevel):
        self.logLevel = level.value

    def log(self, tag: str, message: str, level: LogLevel):
        if level.value > self.logLevel:
            print(f"[{tag}] [{level.name}] {level.color}{message} {Color.RESET.color}")

    def cleaning(self, tag: str, message: str, level: LogLevel, lines_above: int = 1):
        if level.value > self.logLevel:
            new_message = ""
            for _ in range(lines_above):
                new_message += "\033[F"
            print(f"{new_message}\033[2K[{tag}] [{level.name}] {level.color}{message} {Color.RESET.color}", flush=True)

    def info(self, tag: str, message: str):
        self.log(tag, message, self.LogLevel.INFO)

    def error(self, tag: str, message: str):
        self.log(tag, message, self.LogLevel.ERROR)

    def debug(self, tag: str, message: str):
        self.log(tag, message, self.LogLevel.DEBUG)

    def warning(self, tag: str, message: str):
        self.log(tag, message, self.LogLevel.WARNING)

    def info_cleaning(self, tag: str, message: str, lines_above: int = 1):
        self.cleaning(tag, message, self.LogLevel.INFO, lines_above)

    def error_cleaning(self, tag: str, message: str, lines_above: int = 1):
        self.cleaning(tag, message, self.LogLevel.ERROR, lines_above)

    def debug_cleaning(self, tag: str, message: str, lines_above: int = 1):
        self.cleaning(tag, message, self.LogLevel.DEBUG, lines_above)

    def warning_cleaning(self, tag: str, message: str, lines_above: int = 1):
        self.cleaning(tag, message, self.LogLevel.WARNING, lines_above)

    def input(self, tag: str, message: str) -> str:
        print(f"[{tag}] [INPUT] {self.LogLevel.INFO.color}{message} {Color.RESET.color}")
        return input(f"[{tag}] >> ")


logger = Logger(Logger.LogLevel.DEBUG)


class FillingStatus(Enum):
    SINGLE = 0
    JOINT_MARRIED_OR_QUALIFIED_WIDOWER = 1
    SEPARATE_MARRIED = 2
    HEAD_OF_THE_HOUSE = 3


def calculate_income(status: FillingStatus, taxable_income: int):
    """
    The calculate method I used to calculate tax from taxable income based on the taxable_income
        status:
          The filling status used by the function to know the ranges of income to use for the tax percentage
        taxable_income:
          The income to us teh tax percentage on to get the tax
    """
    global logger
    logger.info("CALC", f"Calculating tax using filling status: "
                        f"{Color.YELLOW.color}{status.name}{Color.RESET.color} "
                        f"{Color.CYAN.color}and taxable income:{Color.RESET.color} "
                        f"{Color.YELLOW.color}${taxable_income:,}{Color.RESET.color}")
    tax_percentage: int = None
    match status:
        case FillingStatus.SINGLE:
            # didn't know this format [x < var < y] existed, my ide (pycharm) showed it to me
            if 0 <= taxable_income <= 8350:
                tax_percentage = 10
            elif 8350 < taxable_income <= 33950:
                tax_percentage = 15
            elif 33950 < taxable_income <= 82250:
                tax_percentage = 20
            elif 82250 < taxable_income <= 171550:
                tax_percentage = 28
            elif 171550 < taxable_income <= 372950:
                tax_percentage = 33
            elif 372950 < taxable_income:
                tax_percentage = 35
        case FillingStatus.JOINT_MARRIED_OR_QUALIFIED_WIDOWER:
            if 0 <= taxable_income <= 16700:
                tax_percentage = 10
            elif 16700 < taxable_income <= 67900:
                tax_percentage = 15
            elif 67900 < taxable_income <= 137050:
                tax_percentage = 20
            elif 137050 < taxable_income <= 208850:
                tax_percentage = 28
            elif 208850 < taxable_income <= 372950:
                tax_percentage = 33
            elif 372950 < taxable_income:
                tax_percentage = 35
        case FillingStatus.SEPARATE_MARRIED:
            if 0 <= taxable_income <= 8350:
                tax_percentage = 10
            elif 8350 < taxable_income <= 33950:
                tax_percentage = 15
            elif 33950 < taxable_income <= 68525:
                tax_percentage = 20
            elif 68525 < taxable_income <= 104425:
                tax_percentage = 28
            elif 104425 < taxable_income <= 186475:
                tax_percentage = 33
            elif 186475 < taxable_income:
                tax_percentage = 35
        case FillingStatus.HEAD_OF_THE_HOUSE:
            if 0 <= taxable_income <= 11950:
                tax_percentage = 10
            elif 11950 < taxable_income <= 45500:
                tax_percentage = 15
            elif 45500 < taxable_income <= 117450:
                tax_percentage = 20
            elif 117450 < taxable_income <= 190200:
                tax_percentage = 28
            elif 190200 < taxable_income <= 372950:
                tax_percentage = 33
            elif 372950 < taxable_income:
                tax_percentage = 35

    logger.debug("CALC", f"Using tax percentage {tax_percentage}")
    personal_income_tax : float = (tax_percentage / 100) * taxable_income
    logger.info("CALC", f"Your personal income tax is: `${personal_income_tax:,}`")
    main(False)


def main(should_intro: bool = True):
    global logger
    if should_intro:
        logger.info("MAIN", "  Welcome to BU24SEN1050's Tax Calculator  ")
        logger.info("MAIN", "Type exit at any input to stop the program.")
    else:
        print("")
        answer = logger.input("MAIN", "Would like to calculate another person income tax [(Y, YES, y, yes, Yes) / (N, NO, n, no, No)]")
        if answer.lower() != "y" and answer.lower() != "yes" and answer.lower() != "no" and answer.lower() != "n":
            logger.warning_cleaning("MAIN", f"`{answer}` isn't an option so I'll take that as a yes...")
        elif not (answer.lower() == "yes" or answer.lower() == "y"):
            return
    logger.info("MAIN", "-" * len("Type exit at any input to stop the program."))
    unformatted_filling_status = logger.input("MAIN", f"What is your filling status. Options (You can use the number of the word): {[m.name + " - " + str(m.value) for m in FillingStatus]}")
    filling_status: FillingStatus = None
    if unformatted_filling_status.lower() == "exit":
        logger.info_cleaning("MAIN", "Exiting project...")
        return
    while True:
        if unformatted_filling_status.isdigit():
            try:
                filling_status = FillingStatus(int(unformatted_filling_status))
                break
            except ValueError:
                while unformatted_filling_status not in [m.name for m in FillingStatus]:
                    logger.error_cleaning("MAIN", f"`{unformatted_filling_status}` is not a valid filling status", 2)
                    unformatted_filling_status = logger.input("MAIN",
                                                  f"What is your filling status. Options: {[m.name + " - " + str(m.value) for m in FillingStatus]}")
        else:
            while unformatted_filling_status not in [m.name for m in FillingStatus]:
                logger.error_cleaning("MAIN", f"`{unformatted_filling_status}` is not a valid filling status", 2)
                unformatted_filling_status = logger.input("MAIN",
                                              f"What is your filling status. Options: {[m.name + " - " + str(m.value) for m in FillingStatus]}")
            filling_status = FillingStatus[unformatted_filling_status]
            break
    logger.info_cleaning("MAIN", f"You chose status `{filling_status.name}`")
    not_int_taxable_income = (
        logger.input("MAIN", f"What is your taxable income (should be an integer no commas or all-that)"))
    if not_int_taxable_income.lower() == "exit":
        logger.info_cleaning("MAIN", "Exiting project...")
        return
    # I found out isdigit existed from geeks for geeks
    while not not_int_taxable_income.isdigit():
        logger.error_cleaning("MAIN", f"`{not_int_taxable_income}` is not a valid integer", 2)
        not_int_taxable_income = (
            logger.input("MAIN", f"What is your taxable income (should be an integer no commas or all-that)"))
    while int(not_int_taxable_income) < 0:
        logger.error_cleaning("MAIN", f"`{not_int_taxable_income}` is a negative integer, Income cannot be negative.",
                              2)
        not_int_taxable_income = (
            logger.input("MAIN", f"What is your taxable income (should be an integer no commas or all-that)"))
    taxable_income = int(not_int_taxable_income)
    # found out how to format integers
    logger.info_cleaning("MAIN", f"Your chosen taxable income is `${taxable_income:,}`")
    calculate_income(filling_status, taxable_income)


if __name__ == "__main__":
    main()