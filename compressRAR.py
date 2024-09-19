import os
import subprocess
from pathlib import Path
from tkinter import Tk, Label, Button, filedialog, StringVar, DoubleVar, messagebox
from threading import Thread

class CompresorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Compresor de Carpetas en RAR")
        
        # Variables para mostrar información en el GUI
        self.directorio = StringVar()
        self.nombre_archivo = StringVar(value="Archivo: Ninguno")
        self.progreso = DoubleVar(value=0)
        self.cancelar = False

        # Descripción del programa
        descripcion = Label(root, text="Este programa comprime subcarpetas en archivos RAR y los divide en partes de 1GB.", wraplength=300)
        descripcion.pack(pady=10)

        # Botón para seleccionar la carpeta
        self.btn_seleccion_carpeta = Button(root, text="Seleccionar Carpeta", command=self.selecciona_directorio)
        self.btn_seleccion_carpeta.pack(pady=5)

        # Mostrar nombre del archivo que se está comprimiendo
        self.label_archivo = Label(root, textvariable=self.nombre_archivo)
        self.label_archivo.pack(pady=5)

        # Barra de progreso
        self.label_progreso = Label(root, text="Progreso:")
        self.label_progreso.pack(pady=5)
        self.label_porcentaje = Label(root, textvariable=self.progreso)
        self.label_porcentaje.pack(pady=5)

        # Botón para cancelar
        self.btn_cancelar = Button(root, text="Cancelar", command=self.cancelar_compresion, state="disabled")
        self.btn_cancelar.pack(pady=10)

    def selecciona_directorio(self):
        # Abre el diálogo para seleccionar el directorio
        carpeta = filedialog.askdirectory(title="Selecciona la carpeta principal")
        if carpeta:
            self.directorio.set(carpeta)
            self.iniciar_compresion()

    def iniciar_compresion(self):
        self.cancelar = False
        self.btn_cancelar.config(state="normal")  # Activar el botón de cancelar
        # Ejecutar la compresión en un hilo separado para evitar bloquear la GUI
        thread = Thread(target=self.comprimir_carpeta_en_rar)
        thread.start()

    def comprimir_carpeta_en_rar(self):
        directorio = self.directorio.get()
        if not os.path.isdir(directorio):
            messagebox.showerror("Error", f"El directorio {directorio} no existe.")
            return

        rar_path = 'C:/Program Files/WinRAR/rar.exe'  # Cambia esta ruta a la ubicación de rar.exe en tu sistema
        subcarpetas = [carpeta for carpeta in Path(directorio).iterdir() if carpeta.is_dir()]

        total = len(subcarpetas)
        if total == 0:
            messagebox.showinfo("Información", "No hay subcarpetas para comprimir.")
            return

        for i, carpeta in enumerate(subcarpetas, 1):
            if self.cancelar:
                break

            nombre_rar = f"{carpeta.name}.rar"
            ruta_rar = os.path.join(directorio, nombre_rar)  # Guarda el archivo .rar en el directorio principal
            comando = [
                rar_path, 'a',  # Añadir archivos a un archivo rar
                '-v1g',         # Tamaño máximo de cada parte
                ruta_rar,       # Ruta del archivo rar
                str(carpeta)    # Carpeta a comprimir
            ]
            
            self.nombre_archivo.set(f"Archivo: {carpeta.name}")
            try:
                # Inicia el proceso de compresión
                subprocess.run(comando, check=True)
                # Actualiza el porcentaje después de comprimir cada carpeta
                porcentaje = (i / total) * 100
                self.progreso.set(porcentaje)
                self.root.update_idletasks()  # Actualiza la interfaz gráfica
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"Error al comprimir {carpeta}: {e}")
        
        self.btn_cancelar.config(state="disabled")  # Desactiva el botón de cancelar al finalizar
        self.nombre_archivo.set("Archivo: Ninguno")
        self.progreso.set(0)
    
    def cancelar_compresion(self):
        self.cancelar = True
        messagebox.showinfo("Cancelado", "La compresión ha sido cancelada.")

if __name__ == '__main__':
    root = Tk()
    app = CompresorApp(root)
    root.mainloop()
