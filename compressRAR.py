import os
import subprocess
from pathlib import Path
from tkinter import Tk
from tkinter.filedialog import askdirectory

def selecciona_directorio():
    # Configura la ventana de Tkinter
    root = Tk()
    root.withdraw()  # Oculta la ventana principal
    # Abre el diálogo para seleccionar el directorio
    directorio = askdirectory(title='Selecciona la carpeta principal')
    return directorio

def comprimir_carpeta_en_rar(directorio):
    # Asegúrate de que el directorio existe
    if not os.path.isdir(directorio):
        print(f"El directorio {directorio} no existe.")
        return

    rar_path = 'C:/Program Files/WinRAR/rar.exe'  # Cambia esta ruta a la ubicación de rar.exe en tu sistema

    # Recorre cada carpeta en el directorio dado
    for carpeta in Path(directorio).iterdir():
        if carpeta.is_dir():
            nombre_rar = f"{carpeta.name}.rar"
            ruta_rar = os.path.join(directorio, nombre_rar)  # Guarda el archivo .rar en el directorio principal
            # Ejecuta el comando rar para comprimir la carpeta y dividir el archivo en partes de 1GB
            comando = [
                rar_path, 'a',  # Añadir archivos a un archivo rar
                '-v1g',         # Tamaño máximo de cada parte
                ruta_rar,       # Ruta del archivo rar
                str(carpeta)    # Carpeta a comprimir
            ]
            try:
                subprocess.run(comando, check=True)
                print(f"Comprimido {carpeta} en {ruta_rar}")
            except subprocess.CalledProcessError as e:
                print(f"Error al comprimir {carpeta}: {e}")

if __name__ == '__main__':
    # Selecciona la carpeta principal mediante el diálogo
    directorio_principal = selecciona_directorio()
    if directorio_principal:
        comprimir_carpeta_en_rar(directorio_principal)
    else:
        print("No se seleccionó ningún directorio.")
