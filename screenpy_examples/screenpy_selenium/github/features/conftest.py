from screenpy_adapter_allure import AllureAdapter

from screenpy.pacing import the_narrator

the_narrator.adapters.append(AllureAdapter())
