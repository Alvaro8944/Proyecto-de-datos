import adquisicion

#Realizar el web scraping
df = adquisicion.realizarWebScraping()


#Url debe ser actualizado con un directorio local
url = "C:\Universidad\Segundo\datos"
df.DataFrame.to_csv(url)