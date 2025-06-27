import subprocess
import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import psutil
import imc
import imcDB
# import catalogoIMC


class GUI:
    def __init__(self):
        self.__ventana = tk.Tk()
        self.__ventana.title("Calculadora de IMC")
        self.__ventana.configure(bg="#E8F0FE")
        self.__ventana.geometry("700x500")
        self.__ventana.resizable(False, False)

        fuente = ("Segoe UI", 10)

        # Frame principal para dividir en dos columnas
        main_frame = tk.Frame(self.__ventana, bg="#E8F0FE")
        main_frame.pack(fill="both", expand=True)

        # Frame izquierdo para los controles
        frame_izq = tk.Frame(main_frame, bg="#E8F0FE")
        frame_izq.place(relx=0, rely=0, relwidth=0.55, relheight=1)

        # Frame derecho para la imagen
        frame_der = tk.Frame(main_frame, bg="#E8F0FE")
        frame_der.place(relx=0.55, rely=0, relwidth=0.45, relheight=1)

        # Variables
        self.__nombre = tk.StringVar()
        self.__edad = tk.IntVar(value=18)
        self.__estatura = tk.DoubleVar(value=1.70)
        self.__peso = tk.DoubleVar(value=70.0)
        self.__info = tk.StringVar()
        self.__mensaje_bienvenida = tk.StringVar()

        self.__nombre.trace_add("write", self.__activar_campos)

        # --- Controles en frame_izq ---
        tk.Label(frame_izq, text="Nombre:", font=fuente, bg="#E8F0FE").grid(
            row=0, column=0, sticky="e", pady=5, padx=5)
        self.__entrada_nombre = ttk.Entry(
            frame_izq, textvariable=self.__nombre, font=fuente, width=25)
        self.__entrada_nombre.grid(row=0, column=1, padx=5)

        self.__etiqueta_bienvenida = tk.Label(
            frame_izq,
            textvariable=self.__mensaje_bienvenida,
            font=("Segoe UI", 10, "italic"),
            bg="#E8F0FE",
            fg="#003366",
            justify="center",
            anchor="center"
        )
        self.__etiqueta_bienvenida.grid(
            row=1, column=0, columnspan=2, pady=5, sticky="ew")

        tk.Label(frame_izq, text="Edad:", font=fuente, bg="#E8F0FE").grid(
            row=2, column=0, sticky="e", pady=5, padx=5)
        self.__spin_edad = tk.Spinbox(
            frame_izq, from_=1, to=120, textvariable=self.__edad, font=fuente, width=5, state="disabled", bg="#E8F0FE")
        self.__spin_edad.grid(row=2, column=1, sticky="w", padx=5)

        tk.Label(frame_izq, text="Estatura (m):", font=fuente, bg="#E8F0FE").grid(
            row=3, column=0, sticky="ne", pady=5, padx=5)
        self.__scale_estatura = tk.Scale(
            frame_izq, from_=0.30, to=2.50, resolution=0.01,
            orient="horizontal", variable=self.__estatura,
            length=250, state="disabled", bg="#E8F0FE", highlightthickness=0)
        self.__scale_estatura.grid(row=3, column=1, sticky="w", pady=5)

        tk.Label(frame_izq, text="Peso (kg):", font=fuente, bg="#E8F0FE").grid(
            row=4, column=0, sticky="ne", pady=5, padx=5)
        self.__scale_peso = tk.Scale(
            frame_izq, from_=5, to=200, resolution=0.5,
            orient="horizontal", variable=self.__peso,
            length=250, state="disabled", bg="#E8F0FE", highlightthickness=0)
        self.__scale_peso.grid(row=4, column=1, sticky="w", pady=5)

        ttk.Button(frame_izq, text="Calcular IMC", command=self.__calcular).grid(
            row=5, column=0, pady=10, padx=5)
        ttk.Button(frame_izq, text="Limpiar", command=self.__limpiar).grid(
            row=5, column=1, padx=5, sticky="w")

        self.__resumen = tk.LabelFrame(frame_izq, text="Resultado", font=("Segoe UI", 9, "bold"),
                                       bg="#F7FBFF", padx=10, pady=10)
        self.__resumen.grid(row=6, column=0, columnspan=2,
                            pady=10, padx=10, sticky="ew")
        self.__resumen.grid_remove()

        tk.Label(self.__resumen, textvariable=self.__info,
                 justify="left", bg="#F7FBFF", font=("Segoe UI", 9)).pack()

        marco_extra = tk.Frame(frame_izq, bg="#E8F0FE")
        marco_extra.grid(row=7, column=0, columnspan=2, pady=10)

        tk.Button(marco_extra, text="Ver Registros",
                  command=self.__abrir_catalogo, bg="#E8F0FE", font=fuente).pack(side="left", padx=10)
        tk.Button(marco_extra, text="Cerrar",
                  command=self.__confirmar_cierre, bg="#E8F0FE", font=fuente).pack(side="right", padx=10)

        # --- Imagen en frame_der ---
        ruta_img = os.path.join("resources", "imc.jpg")
        ruta_img = os.path.abspath(os.path.join("resources", "imc.jpg"))
        print("Ruta imagen:", ruta_img)  # Esto mostrará la ruta en la terminal
        try:
            imagen = Image.open(ruta_img)
            imagen = imagen.resize((280, 350), Image.Resampling.LANCZOS)
            self.__imgtk = ImageTk.PhotoImage(imagen)
            label_img = tk.Label(frame_der, image=self.__imgtk, bg="#E8F0FE")
            label_img.place(relx=0.5, rely=0.5, anchor="center")
        except Exception as e:
            label_img = tk.Label(
                frame_der, text="No se pudo cargar la imagen.", bg="#E8F0FE")
            label_img.place(relx=0.5, rely=0.5, anchor="center")

        self.__centrar_ventana()

    def mostrar(self):
        self.__ventana.mainloop()

    def __centrar_ventana(self):
        self.__ventana.update_idletasks()
        ancho = self.__ventana.winfo_width()
        alto = self.__ventana.winfo_height()
        pantalla_ancho = self.__ventana.winfo_screenwidth()
        pantalla_alto = self.__ventana.winfo_screenheight()
        x = (pantalla_ancho // 2) - (ancho // 2)
        y = (pantalla_alto // 2) - (alto // 2)
        self.__ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

    def __activar_campos(self, *args):
        nombre = self.__nombre.get().strip()
        if nombre:
            self.__mensaje_bienvenida.set(
                f"Hola {nombre}\n¡Bienvenido a la Calculadora del Índice de Masa Corporal!")
            self.__spin_edad.config(state="normal")
            self.__scale_estatura.config(state="normal")
            self.__scale_peso.config(state="normal")
        else:
            self.__mensaje_bienvenida.set("")
            self.__spin_edad.config(state="disabled")
            self.__scale_estatura.config(state="disabled")
            self.__scale_peso.config(state="disabled")

    def __calcular(self):
        try:
            est = self.__estatura.get()
            pes = self.__peso.get()
        except Exception:
            messagebox.showerror("Error", "Estatura y peso deben ser válidos.")
            return

        try:
            persona = imc.IMC(
                self.__nombre.get(),
                self.__edad.get(),
                est,
                pes
            )
            datos = persona.obtener_datos()
            imcDB.insertar(datos)
            resumen = (
                f"Nombre: {datos['nombre']}\n"
                f"Edad: {datos['edad']} años\n"
                f"Estatura: {datos['estatura']} m\n"
                f"Peso: {datos['peso']} kg\n"
                f"IMC: {datos['imc']}\n"
                f"Clasificación: {datos['clasificacion']}"
            )
            self.__info.set(resumen)
            self.__resumen.grid()
            self.__ventana.update_idletasks()
            self.__centrar_ventana()
            messagebox.showinfo("Éxito", "Datos guardados correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def __limpiar(self):
        self.__nombre.set("")
        self.__edad.set(18)
        self.__estatura.set(1.70)
        self.__peso.set(70.0)
        self.__mensaje_bienvenida.set("")
        self.__info.set("")
        self.__resumen.grid_remove()
        self.__centrar_ventana()
        self.__spin_edad.config(state="disabled")
        self.__scale_estatura.config(state="disabled")
        self.__scale_peso.config(state="disabled")

    def __abrir_catalogo(self):
        if not self.__catalogo_ya_abierto("catalogoIMC.py"):
            try:
                subprocess.Popen(["python", "catalogoIMC.py"])
            except Exception as e:
                messagebox.showerror(
                    "Error", f"No se pudo abrir el catálogo:\n{str(e)}")
        else:
            messagebox.showinfo("Atención", "El catálogo ya está abierto.")

    def __catalogo_ya_abierto(self, nombre_script):
        for p in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if any(nombre_script in str(c) for c in p.info['cmdline']):
                    return True
            except Exception:
                continue
        return False

    def __confirmar_cierre(self):
        if messagebox.askyesno("Confirmar salida", "¿Deseas cerrar la aplicación?"):
            self.__ventana.destroy()

    # Elimina también el método __abrir_catalogo_interno si no se usará más
    # def __abrir_catalogo_interno(self):
    #     ...


# Ejecución directa
if __name__ == "__main__":
    app = GUI()
    app.mostrar()
