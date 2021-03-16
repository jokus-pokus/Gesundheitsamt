import pandas as pd
from DatenSammlung import DatenVergangenheitHolen, FeiertageHolen



today = date.today()
print("Today's date:", today)

CoronaWerte, Wetter, Restriktionen = DatenVergangenheitHolen()

