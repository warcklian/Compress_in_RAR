import os
import subprocess
from pathlib import Path
from tkinter import Tk, Label, Button, filedialog, StringVar, DoubleVar, messagebox
from threading import Thread

class DescompresorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Descompresor de Archivos RAR")

        # Variables para mostrar información en el GUI
        self.directorio = StringVar()
        self.destino = StringVar()
        self.nombre_archivo = StringVar(value="Archivo: Ninguno")
        self.progreso = DoubleVar(value=0)
        self.cancelar = False

        # Descripción del programa
        descripcion = Label(root, text="Este programa descomprime archivos RAR, incluyendo archivos fraccionados.", wraplength=300)
        descripcion.pack(pady=10)

        # Botón para seleccionar la carpeta que contiene los archivos RAR
        self.btn_seleccion_carpeta = Button(root, text="Seleccionar Carpeta con Archivos RAR", command=self.selecciona_directorio)
        self.btn_seleccion_carpeta.pack(pady=5)

        # Botón para seleccionar la carpeta destino donde se descomprimirán los archivos
        self.btn_seleccion_destino = Button(root, text="Seleccionar Carpeta de Destino", command=self.selecciona_destino)
        self.btn_seleccion_destino.pack(pady=5)

        # Mostrar nombre del archivo que se está descomprimiendo
        self.label_archivo = Label(root, textvariable=self.nombre_archivo)
        self.label_archivo.pack(pady=5)

        # Barra de progreso
        self.label_progreso = Label(root, text="Progreso:")
        self.label_progreso.pack(pady=5)
        self.label_porcentaje = Label(root, textvariable=self.progreso)
        self.label_porcentaje.pack(pady=5)

        # Botón para cancelar
        self.btn_cancelar = Button(root, text="Cancelar", command=self.cancelar_descompresion, state="disabled")
        self.btn_cancelar.pack(pady=10)

    def selecciona_directorio(self):
        # Abre el diálogo para seleccionar el directorio
        carpeta = filedialog.askdirectory(title="Selecciona la carpeta que contiene los archivos RAR")
        if carpeta:
            self.directorio.set(carpeta)

    def selecciona_destino(self):
        # Abre el diálogo para seleccionar el directorio destino
        carpeta_destino = filedialog.askdirectory(title="Selecciona la carpeta de destino")
        if carpeta_destino:
            self.destino.set(carpeta_destino)
            self.iniciar_descompresion()

    def iniciar_descompresion(self):
        self.cancelar = False
        self.btn_cancelar.config(state="normal")  # Activar el botón de cancelar
        thread = Thread(target=self.descomprimir_archivos_rar)  # Ejecutar la descompresión en un hilo separado
        thread.start()

    def es_archivo_fraccionado(self, archivo):
        # Detectar si el archivo es parte de un archivo fraccionado (part1.rar)
        return archivo.suffix == '.rar' and 'part1' in archivo.stem

    def descomprimir_archivos_rar(self):
        directorio = self.directorio.get()
        destino = self.destino.get()

        if not os.path.isdir(directorio):
            messagebox.showerror("Error", f"El directorio {directorio} no existe.")
            return
        if not os.path.isdir(destino):
            messagebox.showerror("Error", f"El directorio de destino {destino} no existe.")
            return

        rar_path = 'C:/Program Files/WinRAR/rar.exe'  # Cambia esta ruta a la ubicación de rar.exe en tu sistema
        archivos_rar = sorted([archivo for archivo in Path(directorio).iterdir() if archivo.suffix == '.rar'])

        procesados = set()  # Para evitar procesar partes adicionales de archivos fraccionados
        total = len(archivos_rar)

        for i, archivo in enumerate(archivos_rar, 1):
            if self.cancelar:
                break

            # Saltar partes adicionales si ya se ha procesado la parte principal
            if archivo in procesados:
                continue

            # Comprobar si es parte de un archivo fraccionado
            if self.es_archivo_fraccionado(archivo):
                # Encontrar todas las partes de este archivo fraccionado
                partes = list(archivo.parent.glob(f"{archivo.stem[:-6]}*.rar"))  # Tomar todas las partes
                procesados.update(partes)  # Marcar todas las partes como procesadas

                self.nombre_archivo.set(f"Descomprimiendo archivo fraccionado: {archivo.stem[:-6]}")
                comando = [
                    rar_path, 'x',  # Comando para extraer archivos
                    str(archivo),    # Solo la parte 1 es necesaria para la descompresión
                    destino          # Carpeta destino
                ]
            else:
                # Procesar archivos .rar únicos
                self.nombre_archivo.set(f"Descomprimiendo archivo único: {archivo.name}")
                comando = [
                    rar_path, 'x',  # Comando para extraer archivos
                    str(archivo),    # Archivo RAR a descomprimir
                    destino          # Carpeta destino
                ]

            try:
                subprocess.run(comando, check=True)
                self.progreso.set((i / total) * 100)
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Error al descomprimir {archivo}: {e}")
        
        self.btn_cancelar.config(state="disabled")  # Desactivar el botón de cancelar al finalizar
        self.nombre_archivo.set("Archivo: Ninguno")
        self.progreso.set(0)

    def cancelar_descompresion(self):
        self.cancelar = True
        messagebox.showinfo("Cancelado", "La descompresión ha sido cancelada.")

if __name__ == '__main__':
    root = Tk()
    app = DescompresorApp(root)
    root.mainloop()
