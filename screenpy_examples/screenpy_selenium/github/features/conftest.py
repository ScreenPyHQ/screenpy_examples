from screenpy.pacing import the_narrator
from screenpy_adapter_allure import AllureAdapter

the_narrator.adapters.append(AllureAdapter())

