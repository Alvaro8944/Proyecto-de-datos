# Intelligent Real Estate

<code> GIDIA - Proyecto de Datos </code>

## 1- Descripción del proyecto

El objetivo de este proyecto es realizar un proyecto de datos y desarrollar un modelo de aprendizaje automatico que permita desarrollar un producto con el fin de predecir y tasar el precio de propiedades inmobiliarias en Madrid. 

Para realizar este trabajo, se han recopilado los datos de las propiedades en venta de la pagina web de "www.tecnocasa.es" a fecha 20/02/2024. Nuevos datos serán recopilados en el futuro dado que habrá propiedades que serán vendidas y nuevas propiedades puestas a la venta, permitiendonos recopilar más datos sin coste alguno reutilizando todo el codigo de adquisición de datos.

El objetivo principal del proyecto sera lograr distintos modelos que puedan realizar la tarea de predecir los precios de las viviendas y discutir acerca de estos modelos. Finalmente utilizaremos el modelo que mejores resultados logre para desarrollar una pequeña DEMO de página web en donde planeamos desplegar el modelo y poder ofrecer nuestro servicio de tasación de viviendas a usuarios que lo deseen.


## 2- Instrucciones para trabajar con el proyecto

En primer lugar, se debe clonar el repositorio de este proyecto en tu dispositivo. Recomendamos usar como entorno de desarrollo Pycharm ya que ha sido el IDE que el equipo ha utilizado para trabajar.

Se deben instalar ciertas librerias (listadas en "requirements.txt") para poder ejecutar el código desarrollado. El código esta dividido en 3 principales apartados. Cada modulo tiene un .py con todas las funciones necesarias y un main.py que ejecuta las funciones para lograr nuestros objetivos. 


En el modulo de adquisición está todo lo necesario para realizar web scraping en la web de "www.tecnocasa.es", pero no es necesario ejecutar su main a menos que se quieran obtener nuevos datos (en cuyo caso habria que unificar y asegurarse de no guardar datos duplicados que ya estuvieran en anteriores archivos). 



En el módulo de limpieza se realiza todo el preprocesado de los datos raw obtenidos de la web. Para ejecutar el main en limpieza se debe verificar antes que se dispone del archivo "archivo_info.txt" y que se ha modificado con tus rutas locales para poder utilizarlo. Este archivo será utilizado para descargar desde el drive de nuestro proyecto todos los archivos necesarios para realizar el preprocesamiento de los datos. Hay 2 caminos que hemos tomado en el tratamiento de datos y es necesario comentar en el código uno de ellos al ejecutarlo. Manteniendo siempre 1 de las 2 formas comentadas nos aseguramos que el archivo que exportamos finalmente sea correcto (revisar los comentarios del main para más informacion). 



En el módulo de exploracion se exploran los datos y se realizan algunas visualizaciones que ayudan a comprender mejor los datos. Para poder ejecutar el main es necesario haber descargado los datos preprocesados del drive del proyecto y modificar la ruta en el codigo con tu ruta local de los datos.


## 3- Integrantes del equipo

- Hamza Triki
- Diego Alonso Arceiz
- Álvaro Fereño Iglesias


