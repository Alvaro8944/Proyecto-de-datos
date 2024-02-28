import adquisicion
import pandas as pd

#Realizar el web scraping
df = adquisicion.realizarWebScraping()

pd.DataFrame.to_csv(df)