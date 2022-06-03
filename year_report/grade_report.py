from enum import Enum
from typing import Any, List, Tuple
from colorama import Fore, Back, Style


def printc(string: str, end="\n", fore="", back="", style="") -> None:
    print(fore + back + style + string + Style.RESET_ALL, sep="", end=end)


def get_grade_class_and_color(grade: float) -> Tuple[str, Any]:
    if grade >= 70:
        return ("First Class", Fore.GREEN)
    elif grade >= 60:
        return ("Upper Second Class", Fore.YELLOW)
    elif grade >= 50:
        return ("Lower Second Class", Fore.RED)
    elif grade >= 40:
        return ("Third Class", Fore.RED)
    else:
        return ("Failed", Fore.RED)


class Verbosity(Enum):
    OVERALL: int = 1
    PER_MODULE: int = 2
    PER_ACTIVITY: int = 3


class Activity:
    def __init__(self, name: str, pct: int, mark: float, certain: bool = True) -> None:
        self.name = name
        self.pct = pct
        self.mark = mark
        self.certain = certain
        """
        name - name of activity
        pct - percent of module is worth i.e. 70
        mark - mark given out of 100
        certain - false if mark is not in system yet
        """

    def get_worth(self) -> float:
        return self.pct * (self.mark / 100)

    def __repr__(self) -> str:
        return self.name


class Module:
    def __init__(self, name: str, grade: int = None, credits: int = 10, certain: bool = True) -> None:
        self.name = name
        self.grade = grade
        self.credits = credits
        self.activities: List[Activity] = []
        self.certain = certain

    def is_uncertain(self):
        return not self.certain or any([not activity.certain for activity in self.activities])

    def add_activity(self, activity: Activity):
        assert not self.grade, "Grade already given."
        self.activities.append(activity)

    def add_activities(self, *activities):
        for activity in activities:
            self.add_activity(activity)

    def get_credits(self):
        return self.credits

    def get_grade(self):
        if self.grade:
            return self.grade

        achieved = potential = 0
        for activity in self.activities:
            achieved += activity.get_worth()
            potential += activity.pct
        assert potential == 100, (f"{self.name} activities don't add up to 100, is {potential} instead.")
        return achieved

    def __repr__(self) -> str:
        return self.name


class Year:
    def __init__(self, year_number: int) -> None:
        self.year_number = year_number
        self.modules: List[Module] = []

    def add_module(self, module: Module):
        self.modules.append(module)

    def add_modules(self, *modules):
        for module in modules:
            self.add_module(module)

    def get_mark(self) -> float:
        total_credits = achieved_credits = 0
        for module in self.modules:
            total_credits += module.get_credits()
            achieved_credits += module.get_credits() * (module.get_grade() / 100)
        return (achieved_credits / total_credits) * 100

    def get_total_credits(self):
        total_credits = 0
        for module in self.modules:
            total_credits += module.get_credits()
        return total_credits

    def grade_per_module(self):
        for module in self.modules:
            if module:
                print(f"{module.name:32}  |  {module.get_grade():.2f}")

    def report(self, verbosity: Verbosity = Verbosity.PER_MODULE) -> None:
        name_width = max([len(module.name) for module in self.modules])

        if verbosity.value >= Verbosity.PER_ACTIVITY.value:
            grade_witdth = 9
        else:
            grade_witdth = 6

        printc(f"{'Module':{name_width}}", end="", fore=Fore.RED)
        print("  |  ", end="")
        printc(f"{'Grade':^{grade_witdth}}", fore=Fore.RED)

        total_credits = achieved_credits = 0

        for module in self.modules:
            module_credist, module_grade = module.get_credits(), module.get_grade()
            total_credits += module_credist
            achieved_credits += module_credist * (module_grade / 100)
            uncertain = module.is_uncertain()

            if verbosity.value >= Verbosity.PER_MODULE.value:
                # Per module report
                printc(f"{module.name:{name_width}}", fore=Fore.BLUE, end="")
                print("  |  ", end="")

                if uncertain:
                    printc(f"{module_grade:<{grade_witdth}.2f}", fore=Fore.YELLOW, end="")
                else:
                    printc(f"{module_grade:<{grade_witdth}.2f}", fore=Fore.GREEN, end="")

                print("")

                if verbosity.value >= Verbosity.PER_ACTIVITY.value:
                    for i, activity in enumerate(module.activities):
                        if i == len(module.activities) - 1:
                            print(" └ ", end="")
                        else:
                            print(" ├ ", end="")
                        printc(f"{activity.name:{name_width - 3}}", end="", fore=Fore.CYAN)
                        print("  |  ", end="")
                        if i == len(module.activities) - 1:
                            print(" └ ", end="")
                        else:
                            print(" ├ ", end="")
                        if activity.certain:
                            printc(f"{activity.get_worth():<{grade_witdth - 3}.2f}", fore=Fore.GREEN, end="")
                        else:
                            printc(f"{activity.get_worth():<{grade_witdth - 4}.2f}?", fore=Fore.YELLOW, end="")
                        print("")

        grade = (achieved_credits / total_credits) * 100

        message, color = get_grade_class_and_color(grade)

        printc(f"{'Total mark ':{name_width}}", end="", fore=Fore.BLUE)
        print("  |  ", end="")
        grade_str = f"{grade:.2f}"
        printc(f"{grade_str} - {message}", fore=color, end="")
        print("")

    def __str__(self):
        return (f"Year {self.year_number}\n" + f"Total Credits {self.get_total_credits()}")
