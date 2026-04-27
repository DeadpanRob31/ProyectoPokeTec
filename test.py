from tkinter import *
from os import path

print("Iniciando programa...") # Mensaje de control

ventana = Tk()
ventana.title("Título de prueba")
ventana.minsize(640,480)

def cargar_img(nombre):
    print(f"Intentando cargar: {nombre}") # Mensaje de control
    ruta = path.join('assets', nombre)
    return PhotoImage(file=ruta)

C_principal = Canvas(ventana, width=640, height=480, bg='blue') # Azul para ver si el canvas carga
C_principal.place(x=0, y=0)

try:
    C_principal.fondo = cargar_img('FondoInicio.png')
    C_principal.create_image(0, 0, anchor=NW, image=C_principal.fondo)
    print("Imagen cargada con éxito")
except Exception as e:
    print(f"Error crítico: {e}")

print("Entrando al loop principal...")
ventana.mainloop()