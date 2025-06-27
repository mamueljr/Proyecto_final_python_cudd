# 🧮 Calculadora de IMC / BMI Calculator - Python Project

Este proyecto es una aplicación de escritorio desarrollada en **Python** con **Tkinter**, que permite calcular el **Índice de Masa Corporal (IMC)**, guardar los datos en una base de datos local y consultar un historial de registros.  
This project is a desktop application built with **Python** and **Tkinter**, which calculates the **Body Mass Index (BMI)**, stores user data in a local database, and allows reviewing a history of entries.

---

## 🚀 Funcionalidades / Features

- 🧑 Ingreso de nombre, edad, estatura y peso  
  Input name, age, height, and weight  
- 📏 Cálculo automático del IMC y su clasificación  
  Automatic BMI calculation and classification  
- 💾 Almacenamiento en base de datos SQLite (`imc.db`)  
  Local storage using SQLite database  
- 📊 Consulta de registros en ventana externa  
  External window to view historical records  
- 📤 Exportación de registros a CSV  
  Export historical records to CSV  
- 🎨 Interfaz visual intuitiva y amigable  
  Clean and intuitive graphical interface  
- 🛡️ Evita abrir múltiples instancias del catálogo  
  Prevents multiple catalog instances from opening

---


## 📁 Estructura del Proyecto / Project Structure

ProyectoIMC/
├── imcGUI.py # Interfaz principal
├── imc.py # Clase para el cálculo del IMC
├── imcDB.py # Operaciones con la base de datos SQLite
├── catalogoIMC.py # Ventana de consulta de registros
├── imc.db # Base de datos local
└── resources/
└── imc.jpg # Imagen ilustrativa


---

## 🛠️ Requisitos

- Python 3.6 o superior

### Librerías necesarias:

```bash
pip install pillow psutil
```
## Cómo ejecutar:

Desde tu terminal, ubícate en la carpeta del proyecto y ejecuta:

python imcGUI.py


## Autores:

Adalberto Emmanuel Rojas Perea

Francisco Aldrete

