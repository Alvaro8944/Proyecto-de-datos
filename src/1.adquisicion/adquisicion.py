import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, InvalidSessionIdException
import pandas as pd
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
base_url = 'https://www.tecnocasa.es/venta/inmuebles/comunidad-de-madrid/madrid.html/pag-{}'

# Inicializa el navegador
driver = webdriver.Chrome()

cont = 0
# Lista para almacenar los datos de cada estate-card
data_list = []
for page_num in range(2, 120):
    try:
        url = base_url.format(page_num)
        driver.get(url)
        print('num_pagina ',page_num)

        # Espera implícita para asegurarse de que la página esté completamente cargada
        driver.implicitly_wait(1)

        # Encuentra el div padre que contiene los divs estate-card
        div_padre = driver.find_element(By.CLASS_NAME, 'estates-list')
        for i in range(15):  # Cambia el rango según tus necesidades
            # Encuentra todos los divs estate-card dentro del div padre nuevamente después de la navegación
            divs_hijos = driver.find_elements(By.CLASS_NAME, 'estate-card')
            # Selecciona un div estate-card específico
            if i < len(divs_hijos):
                div_hijo = divs_hijos[i]
                # Encuentra el enlace dentro del div estate-card
                link_element = div_hijo.find_element(By.TAG_NAME, 'a')
                # Obtiene y guarda el atributo href del enlace
                link = link_element.get_attribute('href')

                # Accede al enlace
                driver.get(link)

                # Diccionario con información de la propiedad (inicializado con valores predeterminados)
                estate_info = {
                'Enlace': link,
                'Precio': "No disponible",
                'Dormitorios': "No disponible",
                'Superficie': "No disponible",
                'Num_baños': "No disponible",
                'Localización': "No disponible",
                'Descripción': "No disponible",
                'Metro':0,
                "Renfe":0
                }

            # Actualiza el diccionario con la información encontrada

                try:
                    Descripcion_element = driver.find_element(By.CLASS_NAME, 'estate-description-container')
                    descripcion = Descripcion_element.text
                    estate_info["Descripción"] = descripcion
                except NoSuchElementException:
                    print("No se encontró la descripcion")

                try:
                    price_element = driver.find_element(By.CLASS_NAME, 'current-price')
                    price_text = price_element.text
                    estate_info['Precio'] = price_text
                except NoSuchElementException:
                    print("No se encontró el elemento del precio")

                try:
                    subtitle = driver.find_element(By.CLASS_NAME, 'estate-subtitle')
                    subtitle_text = subtitle.text
                    estate_info['Localización'] = subtitle_text
                except NoSuchElementException:
                    print("No se encontró el elemento del subtitulo")

                try:
                    rooms_element = driver.find_element(By.CLASS_NAME, 'estate-card-rooms')
                    rooms_text = rooms_element.text
                    estate_info['Dormitorios'] = rooms_text
                except NoSuchElementException:
                    print("No se encontró el elemento de dormitorios")
                try:
                    surface_element = driver.find_element(By.CLASS_NAME, 'estate-card-surface')
                    surface_text = surface_element.text
                    estate_info['Superficie'] = surface_text
                except NoSuchElementException:
                    print("No se encontró el elemento de superficie")

                try:
                    bathrooms_element = driver.find_element(By.CLASS_NAME, 'estate-card-bathrooms')
                    bathrooms_text = bathrooms_element.text
                    estate_info['Num_baños'] = bathrooms_text
                except NoSuchElementException:
                    print("No se encontró el elemento de baños")

                features_element = driver.find_element(By.CLASS_NAME, 'estate-features')
                rows = features_element.find_elements(By.CLASS_NAME, 'row')
                for row in rows:
                    title_element = row.find_element(By.CLASS_NAME, 'estate-features-title')
                    value_element = row.find_element(By.CLASS_NAME, 'estate-features-value')
                    title = title_element.text.strip(':')
                    value = value_element.text.strip()

                      # Verifica el título y extrae la información específica
                    if title == 'Calefacción':
                        estate_info['Calefaccion'] = value
                    elif title == 'Jardín':
                        estate_info['Jardin'] = value
                    elif title == 'Tipo de inmueble':
                        estate_info['Tipo_de_inmueble'] = value
                    elif title == 'Año de construcción':
                        estate_info['Año_de_construccion'] = value
                    elif title == 'Planta':
                        estate_info['Planta'] = value
                    elif title == 'Aire acondicionado':
                        estate_info['Aire acondicionado'] = value
                    elif title == 'Ascensor':
                        estate_info['Ascensor'] = value

                try:
                    energy_graph_element = driver.find_element(By.CLASS_NAME, 'energy-graph')
                    # Encuentra el elemento con la clase "square active" dentro del elemento "energy-graph"
                    active_square_element = energy_graph_element.find_element(By.CLASS_NAME, 'square.active')
                    # Extrae el texto del elemento encontrado
                    value = active_square_element.text
                    estate_info['Etiqueta'] = value
                except StaleElementReferenceException:
                    print("El elemento energy_graph_element se volvió obsoleto. Volviendo a encontrar el elemento.")
                    energy_graph_element = driver.find_element(By.CLASS_NAME, 'energy-graph')
                    active_square_element = energy_graph_element.find_element(By.CLASS_NAME, 'square.active')
                    value = active_square_element.text
                    estate_info['Etiqueta'] = value
                except NoSuchElementException:
                    print("No tiene etiqueta")
                try:
                    transportes = driver.find_element(By.CSS_SELECTOR, '.poi-category-data.public_transport')
                    rows = transportes.find_elements(By.CLASS_NAME, 'row')
                    MaximaDistanciaPosible = 2000
                    for row in rows:
                        zona = row.find_element(By.CLASS_NAME, 'col')
                        distancia = row.find_element(By.CLASS_NAME, 'col-auto')
                        imagen_src = row.find_element(By.TAG_NAME, 'img').get_attribute('src')
                        print(imagen_src,distancia.text.split())
                        if distancia.text.split()[1]=="km":
                            cadena = distancia.text.split()[0]
                            Distancia = pd.to_numeric(cadena.replace(",", "."), errors='coerce')* 1000
                        else:
                            Distancia = pd.to_numeric(distancia.text.split()[0],errors='coerce')
                        if(Distancia < MaximaDistanciaPosible):
                            if "subway" in imagen_src:
                                estate_info["Metro"] = 1
                            elif "station" in imagen_src:
                                estate_info["Renfe"] =1
                except:
                    print("No se ha encontrado")

                 # Agrega el diccionario a la lista
                data_list.append(estate_info)

                # Imprime información durante la ejecución para depurar
                print(f"Processed estate-card {cont}: {link}")
                cont+=1
                    # Retrocede a la página principal para procesar la siguiente estate-card
                driver.back()
    except WebDriverException as e:
        print(f"WebDriverException: {e}")
        print("Reloading the page and retrying...")
        driver = webdriver.Chrome()
    except InvalidSessionIdException as e:
        # Handle InvalidSessionIdException
        print(f"InvalidSessionIdException occurred: {e}")
        driver = webdriver.Chrome()

print("Proceso completado.")

# Cierra el navegador
driver.quit()

# Crea un DataFrame a partir de la lista de datos
df = pd.DataFrame(data_list)

# Imprime el DataFrame
print(df)
