from tkinter import *
from tkinter import messagebox
from os import path
import vlc
import sys
import ctypes
import random

'''
Creando ambiente virtual de Python para este proyecto:
0. Instalar VLC Media Player para que funcione la librería de Python https://www.videolan.org/vlc/download-windows.html
1. Abrir terminal en vscode
2. Cambia a Command Prompt (cmd)
3. Click en la flechita de la terminal → Select Default Profile → elige Command Prompt
4. Activa:
5. Escribir python -m venv env_vlc
6. Activar el ambiente virtual:
7. .\env_vlc\Scripts\activate
8. Instalar la librería para reproducir música:
9. pip install python-vlc
'''
#Ventana Inicial
ventana = Tk()
ventana.title("PokeTec")
ventana.minsize(1470,790)
ventana.resizable(width=NO, height=NO)

#Pokemons
pokemons=[
    {
        "nombre": "Pikachu",
        "vida": 100,
        "ataque": 65,
        "defensa": 40,
        "img_front": "pikachuFront.png",
        "img_back": "pikachuBack.png",
        "img_mini": "pikachuMini.png",
        

    },
    {
        "nombre": "Charmander", 
        "vida": 100, 
        "ataque": 52, 
        "defensa": 43, 
        "img_front": "charmanderFront.png",
        "img_back": "charmanderBack.png",
        "img_mini": "charmanderMini.png"
    },
    {
        "nombre": "Charizard", 
        "vida": 100, 
        "ataque": 52, 
        "defensa": 43, 
        "img_front": "charizardFront.png",
        "img_back": "charizardBack.png",
        "img_mini": "charizardMini.png"
    },
    {
        "nombre": "Jigglypuff", 
        "vida": 100, 
        "ataque": 52, 
        "defensa": 43, 
        "img_front": "jigglypuffFront.png",
        "img_back": "jigglypuffBack.png",
        "img_mini": "jigglypuffMini.png"
    },
    {
        "nombre": "Cubone", 
        "vida": 100, 
        "ataque": 52, 
        "defensa": 43, 
        "img_front": "cuboneFront.png",
        "img_back": "cuboneBack.png",
        "img_mini": "cuboneMini.png"
    },
    {
        "nombre": "Mewtwo", 
        "vida": 100, 
        "ataque": 52, 
        "defensa": 43, 
        "img_front": "mewtwoFront.png"
        ,"img_back": "mewtwoBack.png",
        "img_mini": "mewtwoMini.png"
    },
    {
        "nombre": "VaporeonFront", 
        "vida": 100, 
        "ataque": 52, 
        "defensa": 43, 
        "img_front": "vaporeonFront.png",
        "img_back": "vaporeonBack.png",
        "img_mini": "vaporeonMini.png"
    },
    {
        "nombre": "Psyduck", 
        "vida": 100, 
        "ataque": 52, 
        "defensa": 43, 
        "img_front": "psyduckFront.png",
        "img_back": "psyduckBack.png",
        "img_mini": "psyduckMini.png"
    },
    {
        "nombre": "Squirtle", 
        "vida": 100, 
        "ataque": 52, 
        "defensa": 43, 
        "img_front": "squirtleFront.png",
        "img_back": "squirtleBack.png",
        "img_mini": "squirtleMini.png"
    },
    {
        "nombre": "Snorlax", 
        "vida": 100, 
        "ataque": 52, 
        "defensa": 43, 
        "img_front": "snorlaxFront.png",
        "img_back": "snorlaxBack.png",
        "img_mini": "snorlaxMini.png"
    },
]

avatar=[
    "Personaje1.png","Personaje2.png","Personaje3.png","Personaje4.png","Personaje5.png"
]
equipo_Jugador=[]
equipo_bot=[]
nombreBot=""
avatarBot=""
#Variables Globales
indice_actual = 0
indice_avatars=0
capturas_jugador = 0
capturas_bot = 0
turno_jugador = True

#Cargar imagenes
CarpetaAssets = path.dirname(path.abspath(__file__))
def cargar_img(nombre):
    ruta = path.join(CarpetaAssets, 'assets', nombre) 
    img = PhotoImage(file=ruta)
    return img

#Cargar Fuente
def cargar_fuente_sistema(ruta_fuente):
    ctypes.windll.gdi32.AddFontResourceExW(ruta_fuente, 0x10, 0)

rutaFuente = path.join(CarpetaAssets, 'assets', 'pokemon-emerald.ttf')
cargar_fuente_sistema(rutaFuente)

#Cargar Musica
def cargarMP3(nombre):
    return path.join(CarpetaAssets, 'assets', nombre)

reproductor = vlc.MediaPlayer()

def reproducir_cancion(mp3):
    global reproductor
    reproductor = vlc.MediaPlayer(mp3)
    reproductor.audio_set_volume(50)
    reproductor.play()

def reproducir_effecto(mp3):
    vlc.MediaPlayer(mp3).play()

def detener_musica():
    global reproductor
    if isinstance(reproductor, vlc.MediaPlayer):
        reproductor.stop()

#=====================================================Ventanas===========================================================================

def generar_rival():
    global equipo_bot, nombreBot, avatarBot

    nombres_randoms = ["Kai", "Alex", "Frankie", "Giovanni", "Lance"]
    nombreBot = random.choice(nombres_randoms)
    
    avatarBot = random.choice(avatar) 
    
    equipo_bot = random.sample(pokemons, 3) 
    
    print(f"Rival {nombreBot} generado con {len(equipo_bot)} pokémons.")

def preparar_interfaz_pelea():
    global C_Seleccion, VentanadeBatalla
    C_Seleccion.delete("botones_seleccion") 

    btn_atacar = Button(VentanadeBatalla, text="ATACAR", font=("Pokemon Emerald", 25),
                        command=lambda: ejecutar_accion("atacar"),height=1,width=12)
    C_Seleccion.create_window(1100, 600, window=btn_atacar)

    btn_defender = Button(VentanadeBatalla, text="DEFENDER", font=("Pokemon Emerald", 25),
                          command=lambda: ejecutar_accion("defender"), width=12,height=1)
    C_Seleccion.create_window(1300, 600, window=btn_defender) 
    actualizar_barras_vida()

def ejecutar_accion(accion_jugador):
    global pokemon_actual_jugador, pokemon_actual_bot, p_aliado,p_rival,lbl_prueba
    
    p_aliado = pokemon_actual_jugador
    p_rival = pokemon_actual_bot
    
    if accion_jugador == "atacar":
        danio = max(5, p_aliado["ataque"] - p_rival["defensa"])
        p_rival["vida"] -= danio
        lbl_prueba.config(text=f"{pokemon_actual_jugador['nombre']} usó ATACAR! Hizo {danio} de daño.")
        print(f"¡Atacaste! Daño causado: {danio}")
    
    if p_rival["vida"] <= 0:
        print(f"¡Has capturado a {p_rival['nombre']}!")
        equipo_Jugador.append(p_rival) # Te adueñas de él
        capturas_jugador += 1
        verificar_final()
        return # Termina el turno porque hay que sacar otro pokemon
def verificar_final():
    global capturas_jugador, capturas_bot
    
    if capturas_jugador == 3:
        messagebox.showinfo("VICTORIA", "¡Has capturado los 3 Pokémon del rival! Eres el maestro.")
        # Volver al menú o cerrar
    elif capturas_bot == 3:
        messagebox.showerror("DERROTA", "El bot te ha ganado y se llevó a tus Pokémon...")
    accion_bot = random.choice(["atacar", "defender"])
    if accion_bot == "atacar":
        danio_bot = max(5, p_rival["ataque"] - p_aliado["defensa"])
        p_aliado["vida"] -= danio_bot
    
    actualizar_barras_vida() # Función para refrescar el Canvas
def actualizar_barras_vida():
    global pokemon_actual_jugador, pokemon_actual_bot, C_Batalla
    
    # Borramos las barras anteriores para redibujarlas
    C_Seleccion.delete("barras")

    # --- BARRA DEL JUGADOR ---
    hp_max_jugador = 100 
    porcentaje_jugador = pokemon_actual_jugador["vida"] / hp_max_jugador
    color_j = "green" if porcentaje_jugador > 0.5 else "yellow" if porcentaje_jugador > 0.2 else "red"
    
    C_Seleccion.create_rectangle(500, 520, 100, 470, fill="gray", tags="barras")
    C_Seleccion.create_rectangle(500, 520, 1000 + (300 * porcentaje_jugador), 470, fill=color_j, tags="barras")

    # --- BARRA DEL BOT ---
    hp_max_bot = 100
    porcentaje_bot = pokemon_actual_bot["vida"] / hp_max_bot
    color_b = "green" if porcentaje_bot > 0.5 else "yellow" if porcentaje_bot > 0.2 else "red"
    
    C_Seleccion.create_rectangle(1000, 150, 1300, 170, fill="gray", tags="barras")
    C_Seleccion.create_rectangle(1000, 150, 1000 + (300 * porcentaje_bot), 170, fill=color_b, tags="barras")

def elegir_inicial(indice_equipo): 
    global pokemon_actual_jugador, pokemon_actual_bot, equipo_Jugador, equipo_bot, C_Seleccion, lbl_prueba, nombreBot,lbl_nombrePokemonBot,lbl_nombrePokemon
    
    pokemon_actual_jugador = equipo_Jugador[indice_equipo]
    pokemon_actual_bot = equipo_bot[0] 
    
    C_Seleccion.imgPokeAliado = cargar_img(pokemon_actual_jugador['img_back'])
    C_Seleccion.create_image(440, 440, anchor=CENTER, image=C_Seleccion.imgPokeAliado)
    
    # El Pokémon del Rival de frente
    C_Seleccion.imgPokeRival = cargar_img(pokemon_actual_bot['img_front'])
    C_Seleccion.create_image(980, 190, anchor=N, image=C_Seleccion.imgPokeRival)

    #Actualizar burbujas de textooo
    texto_batalla = f"{nombreBot} envió a {pokemon_actual_bot['nombre']}!"
    lbl_prueba.config(text=texto_batalla)

    texto_pokemonAliado=pokemon_actual_jugador['nombre']
    lbl_nombrePokemon.config(text=texto_pokemonAliado)

    texto_pokemonBot=pokemon_actual_bot['nombre']
    lbl_nombrePokemonBot.config(text=texto_pokemonBot)

    preparar_interfaz_pelea()

#VentanaBatalla
def VentanaBatalla():
    global ent_nombre,equipo_Jugador,equipo_bot,avatarBot,nombreBot,avatar,indice_avatars,C_Seleccion,VentanadeBatalla,lbl_prueba,lbl_nombrePokemon,lbl_nombrePokemonBot
    detener_musica()
    VentanadeBatalla=Toplevel(ventana)
    VentanadeBatalla.title("Seleccion de personaje")
    VentanadeBatalla.minsize(1470,790)
    VentanadeBatalla.resizable(width=NO, height=NO)
    VentanadeBatalla.protocol("WM_DELETE_WINDOW", cierreTotaldeVentanas)
    ventana.withdraw()
    
    C_Seleccion = Canvas(VentanadeBatalla, width=1470, height=790, highlightthickness=0)
    C_Seleccion.place(x=0, y=0)
    #-----------FONDO----------------------
    C_Seleccion.fondo = cargar_img('FondoVerde.png')
    C_Seleccion.create_image(0, 0, anchor=NW, image=C_Seleccion.fondo)

    C_Seleccion.zacate1 = cargar_img('Zacate1.png')
    C_Seleccion.create_image(400, 480, anchor=N, image=C_Seleccion.zacate1)

    C_Seleccion.zacate2 = cargar_img('Zacate2.png')
    C_Seleccion.create_image(1080, 300, anchor=N, image=C_Seleccion.zacate2)
    #-----------FONDO----------------------


    #------------JUGADOR-------------------


    C_Seleccion.imgAvatarJugador = cargar_img(avatar[indice_avatars])
    C_Seleccion.create_image(300, 400, anchor=CENTER, image=C_Seleccion.imgAvatarJugador)

    #------------JUGADOR-------------------

    #------------BOT-------------------
    # 1. Cargar la imagen del rival
    C_Seleccion.imgAvatarRival = cargar_img(avatarBot)

    # 2. Dibujarla en el Canvas (posición superior, cerca del Pokémon rival)
    # Ajusta x=1100, y=200 según tu fondo
    C_Seleccion.create_image(1150, 200, anchor=CENTER, image=C_Seleccion.imgAvatarRival)
    #------------BOT-------------------


    #------------BURBUJAS DE TEXTO------------
    C_Seleccion.textoGrande = cargar_img('TextoPrueba.png')
    C_Seleccion.create_image(530, 555, anchor=N, image=C_Seleccion.textoGrande)

    C_Seleccion.textoPeque1 = cargar_img('TextoPeque1.png')
    C_Seleccion.create_image(1100, 410, anchor=N, image=C_Seleccion.textoPeque1)
    lbl_nombrePokemon=Label(VentanadeBatalla, text="Pokemon1", font=("Pokemon Emerald", 35), fg="#2b2b2b", bg="#f5f5f5")
    C_Seleccion.create_window(1020, 480, window=lbl_nombrePokemon)

    C_Seleccion.textoPeque2 = cargar_img('TextoPeque2.png')
    C_Seleccion.create_image(600, 100, anchor=N, image=C_Seleccion.textoPeque2)
    lbl_nombrePokemonBot=Label(VentanadeBatalla, text="PokemonBot", font=("Pokemon Emerald", 35), fg="#2b2b2b", bg="#f5f5f5")
    C_Seleccion.create_window(520, 170, window=lbl_nombrePokemonBot)
    
    
    lbl_prueba=Label(VentanadeBatalla, text=f"Has sido retado por el entrenador {nombreBot}!", font=("Pokemon Emerald", 35), fg="#2b2b2b", bg="#f5f5f5",border=1)
    C_Seleccion.create_window(500, 620, window=lbl_prueba)
    #------------BURBUJAS DE TEXTO------------


    #------------BOTONES----------------------
    coords_botones=[(1100,605),(1100,680),(1300,605)]
    for i in range(3):
        posX,posY=coords_botones[i]
        btn1 = Button(VentanadeBatalla, text=equipo_Jugador[i]["nombre"], 
                     command=lambda idx=i: elegir_inicial(idx), font=("Pokemon Emerald", 30), height=1)
        
        C_Seleccion.create_window(posX,posY,window=btn1,tags="botones_seleccion",)
    #------------BOTONES----------------------
    
    #Musica
    reproducir_cancion(cargarMP3("BatallaMusica.mp3"))

#Actualizar sliders
def cambiar_avatar(n):
    global indice_avatars
    indice_avatars = (indice_avatars + n) % len(avatar)
    actualizar_avatar()

def actualizar_avatar():
    global indice_avatars,lbl_img_avatar
    img_name = avatar[indice_avatars % len(avatar)]
    img = cargar_img(img_name)
    
    # 2. Configurar el Label
    lbl_img_avatar.config(image=img)
    lbl_img_avatar.image = img

def actualizar_interfaz():
    global lbl_nombre, lbl_atribAtaque, lbl_atribDefensa, lbl_hp, panel_img, indice_actual
    
    p = pokemons[indice_actual]
    
    # Actualizar textos
    lbl_nombre.config(text=p["nombre"].upper())
    lbl_hp.config(text=f"HP: {p['vida']}")
    lbl_atribAtaque.config(text=f"Ataque: {p['ataque']}")
    lbl_atribDefensa.config(text=f"Defensa: {p['defensa']}")
    
    # Actualizar imagen
    nueva_img = cargar_img(p["img_front"])
    panel_img.config(image=nueva_img)
    panel_img.image = nueva_img

def cambiar_pokemon(direccion):
    global indice_actual
    
    indice_actual += direccion
    
    if indice_actual >= len(pokemons):
        indice_actual = 0
    elif indice_actual < 0:
        indice_actual = len(pokemons) - 1
        
    actualizar_interfaz()

def elegir_para_equipo():
    global indice_actual, equipo_Jugador
    
    pokemon_seleccionado = pokemons[indice_actual]
    
    if len(equipo_Jugador) < 3:
        equipo_Jugador.append(pokemon_seleccionado)
        print(f"Añadido: {pokemon_seleccionado['nombre']}. Llevas {len(equipo_Jugador)}/3")
        
        if len(equipo_Jugador) == 3:
            print("¡Equipo completo! Ya puedes iniciar la batalla.")
    else:
        print("Tu equipo ya está lleno.")

#VentanaEleccion
def ventana_Pokemons():
    detener_musica()
    top_pokemons = Toplevel(ventana)
    top_pokemons.title("Selección de Entrenador y Equipo")
    top_pokemons.minsize(1470, 790)
    top_pokemons.resizable(width=NO, height=NO)
    top_pokemons.protocol("WM_DELETE_WINDOW", cierreTotaldeVentanas)
    ventana.withdraw()
    
    #-----------Fondo-----------
    C_Seleccion = Canvas(top_pokemons, width=1470, height=790, highlightthickness=0)
    C_Seleccion.place(x=0, y=0)
    C_Seleccion.fondo = cargar_img('Fondo2.png')
    C_Seleccion.create_image(0, 0, anchor=NW, image=C_Seleccion.fondo)
    #---------------------------

    #------------Frame(caja de seleccion)------------
    frame_interfaz = Frame(top_pokemons, bg="#67f824", padx=30, pady=30) 
    C_Seleccion.create_window(700, 410, window=frame_interfaz) 

    global lbl_nombre, panel_img, lbl_atribAtaque, lbl_atribDefensa, lbl_hp, lbl_img_avatar, ent_nombre

    # --- SECCIÓN IZQUIERDA: AVATAR (Columnas 0, 1, 2) ---
    Label(frame_interfaz, text="ENTRENADOR", font=("Pokemon Emerald", 20), fg="black", bg="#ffffff").grid(row=0, column=0, columnspan=3, pady=10)
    
    lbl_img_avatar = Label(frame_interfaz, bg="white")
    lbl_img_avatar.grid(row=1, column=1)
    
    Button(frame_interfaz, text="<", command=lambda: cambiar_avatar(-1), font=("Pokemon Emerald", 15)).grid(row=1, column=0, padx=10)
    Button(frame_interfaz, text=">", command=lambda: cambiar_avatar(1), font=("Pokemon Emerald", 15)).grid(row=1, column=2, padx=10)

    btn_elegir = Button(frame_interfaz, text="ELEGIR POKÉMON", font=("Pokemon Emerald", 15), 
                    command=elegir_para_equipo, bg="green", fg="white")
    btn_elegir.grid(row=6, column=4, columnspan=3, pady=10)

    Label(frame_interfaz, text="Nombre:", font=("Pokemon Emerald", 15), fg="black", bg="#ffffff").grid(row=2, column=0, pady=20,padx=40)
    ent_nombre = Entry(frame_interfaz, font=("Pokemon Emerald", 15))
    ent_nombre.grid(row=2, column=1, columnspan=2, pady=10)
    # --- ESPACIO CENTRAL (Columna 3 para separar) ---
    Label(frame_interfaz, text="   ",bg="#ffffff").grid(row=1, column=3, padx=40)

    # --- SECCIÓN DERECHA: POKÉMON (Columnas 4, 5, 6) ---
    Label(frame_interfaz, text="TU POKÉMON", font=("Pokemon Emerald", 20), fg="black", bg="#ffffff").grid(row=0, column=4, columnspan=3, pady=10)
    
    panel_img = Label(frame_interfaz, bg="#ffffff")
    panel_img.grid(row=1, column=5)
    
    Button(frame_interfaz, text="<", command=lambda: cambiar_pokemon(-1), font=("Pokemon Emerald", 15)).grid(row=1, column=4, padx=10)
    Button(frame_interfaz, text=">", command=lambda: cambiar_pokemon(1), font=("Pokemon Emerald", 15)).grid(row=1, column=6, padx=10)

    # --- ATRIBUTOS (Debajo del nombre del Pokemon) ---
    lbl_nombre = Label(frame_interfaz, text="", font=("Pokemon Emerald", 25, "bold"), fg="yellow", bg="#ffffff")
    lbl_nombre.grid(row=2, column=4, columnspan=3)

    lbl_atribAtaque = Label(frame_interfaz, text="", font=("Pokemon Emerald", 18), fg="black", bg="#ffffff")
    lbl_atribAtaque.grid(row=3, column=5)

    lbl_atribDefensa = Label(frame_interfaz, text="", font=("Pokemon Emerald", 18), fg="black", bg="#ffffff")
    lbl_atribDefensa.grid(row=4, column=5)

    lbl_hp = Label(frame_interfaz, text="", font=("Pokemon Emerald", 18), fg="#00ff00", bg="#ffffff")
    lbl_hp.grid(row=5, column=5)

    # --- BOTÓN FINAL (Abajo de todo) ---
    btn_listo = Button(frame_interfaz, text="¡ESTOY LISTO!", font=("Pokemon Emerald", 20), command=confirmar_seleccion)
    btn_listo.grid(row=6, column=0, columnspan=7, pady=20)

    # Inicializar Música y Datos
    global reproductor
    reproductor = vlc.MediaPlayer(cargarMP3("SeleccionPj.mp3"))
    reproductor.audio_set_volume(60) 
    reproductor.play()

    actualizar_avatar()
    actualizar_interfaz()

def preparar_batalla():
    if len(equipo_Jugador) < 3:
        messagebox.showerror("Error", "¡Te faltan pokémons en el equipo!")
        print("¡Te faltan pokémons en el equipo!")
        return
    
    generar_rival() 
    VentanaBatalla() 

def confirmar_seleccion():
    detener_musica()
    nombre = ent_nombre.get()
    if not nombre:
        messagebox.showerror("Error", "¡Debes ponerte un nombre!")
        return
    reproducir_effecto(cargarMP3("ListoSoundEffect.mp3"))
    generar_rival()
    VentanaBatalla()
C_principal = Canvas(ventana, width=1470, height=790, background="green" ,highlightthickness=0)
C_principal.place(x=0, y=0)

C_principal.fondo = cargar_img('FondoInicio.png')
Fondo1 = C_principal.create_image(0, 0, anchor=NW,image=C_principal.fondo)

logoPoketec=cargar_img('Logo.png')
C_principal.logoPoketec= logoPoketec


#Animacion del logo
desplazamiento = 0
direccion = 1 

def animar_logo(objeto_id):
    global desplazamiento, direccion
    
    limite = 15
    velocidad = 0.7 
    
    #Movimiento
    C_principal.move(objeto_id, 0, direccion * velocidad)
    desplazamiento += direccion * velocidad
    
    if abs(desplazamiento) >= limite:
        direccion *= -1
        
    #Cada cuanto se repite
    ventana.after(30, lambda: animar_logo(objeto_id))

Logo = C_principal.create_image(
    735, 395, 
    anchor=CENTER, 
    image=logoPoketec

)

#C_principal.create_image(300,300, anchor=CENTER, image=pokemonCharizard)

#Boton Iniciar
btn_iniciar = Button(ventana, text="JUGAR", command=ventana_Pokemons, width=20, height=1, font=("Pokemon Emerald", 20))
C_principal.create_window(735, 690, window=btn_iniciar) 


def cierreTotaldeVentanas():
    detener_musica()
    ventana.destroy()
    sys.exit()

ventana.protocol("WM_DELETE_WINDOW", cierreTotaldeVentanas)
reproducir_cancion(cargarMP3("Opening.mp3"))
animar_logo(Logo)
ventana.mainloop()