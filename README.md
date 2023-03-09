Se recomienda crear un ambiente virtual para cada script.

Pasos para crear el ambiente virtual e instalar las dependencias requeridas: (hacer esto en cada carpeta)

1) python -m venv venv (crear ambiente virtual)
2) source venv/bin/activate (activar ambiente virtual en mac) / venv\Scripts\activate (en windows)
nota: se sabe que el ambiente virtual esta activado porque en el promt de la terminal aparece (venv) antes de el nombre del usuario.
3) pip install -r requirements.txt (instalar dependencias)

--> para desactivar el ambiente virtual cuando no se use mas el proyecto <--

4) deactivate 


Para ejecutar el proceso etl y poblar la base de datos: 
nota: ejecutar esto con el ambiente virtual activado y las dependencias instaladas.
1) cd etl 
2) python main.py 

Para levantar el servidor donde se veran las graficas (Dash):
1) cd analysis
2) python main.py
  Esto levantara un servidor y para ver las graficas dirigirse a la direccion que muestra en la terminal.
  
