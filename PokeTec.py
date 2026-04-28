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
        "vida_max":100,
        "ataque": 65,
        "defensa": 40,
        "img_front": "pikachuFront.png",
        "img_back": "pikachuBack.png",
        "img_mini": "pikachuMini.png",
        

    },
    {
        "nombre": "Charmander", 
        "vida": 100, 
        "vida_max":100,
        "ataque": 52, 
        "defensa": 43, 
        "img_front": "charmanderFront.png",
        "img_back": "charmanderBack.png",
        "img_mini": "charmanderMini.png"
    },
    {
        "nombre": "Squirtle", 
        "vida": 100, 
        "vida_max":100,
        "ataque": 52, 
        "defensa": 43, 
        "img_front": "squirtleFront.png",
        "img_back": "squirtleBack.png",
        "img_mini": "squirtleMini.png"
    },
    {
        "nombre": "Psyduck", 
        "vida": 100, 
        "vida_max":100,
        "ataque": 52, 
        "defensa": 43, 
        "img_front": "psyduckFront.png",
        "img_back": "psyduckBack.png",
        "img_mini": "psyduckMini.png"
    },
    {
        "nombre": "Snorlax", 
        "vida": 100, 
        "vida_max":100,
        "ataque": 52, 
        "defensa": 43, 
        "img_front": "snorlaxFront.png",
        "img_back": "snorlaxBack.png",
        "img_mini": "snorlaxMini.png"
    },
    {
        "nombre": "Charizard", 
        "vida": 100, 
        "vida_max":100,
        "ataque": 52, 
        "defensa": 43, 
        "img_front": "charizardFront.png",
        "img_back": "charizardBack.png",
        "img_mini": "charizardMini.png"
    },
    {
        "nombre": "Jigglypuff", 
        "vida": 100, 
        "vida_max":100,
        "ataque": 52, 
        "defensa": 43, 
        "img_front": "jigglypuffFront.png",
        "img_back": "jigglypuffBack.png",
        "img_mini": "jigglypuffMini.png"
    },
    {
        "nombre": "Cubone", 
        "vida": 100, 
        "vida_max":100,
        "ataque": 52, 
        "defensa": 43, 
        "img_front": "cuboneFront.png",
        "img_back": "cuboneBack.png",
        "img_mini": "cuboneMini.png"
    },
    {
        "nombre": "Mewtwo", 
        "vida": 100, 
        "vida_max":100,
        "ataque": 52, 
        "defensa": 43, 
        "img_front": "mewtwoFront.png"
        ,"img_back": "mewtwoBack.png",
        "img_mini": "mewtwoMini.png"
    },
    {
        "nombre": "VaporeonFront", 
        "vida": 100, 
        "vida_max":100,
        "ataque": 52, 
        "defensa": 43, 
        "img_front": "vaporeonFront.png",
        "img_back": "vaporeonBack.png",
        "img_mini": "vaporeonMini.png"
    },
    
]

avatar=[
    "Personaje1.png","Personaje2.png","Personaje3.png","Personaje4.png","Personaje5.png"
]
equipo_Jugador=[]
pokemons_ya_elegidos=[]
equipo_bot=[]
nombreBot=""
avatarBot=""
#Variables Globales
indice_actual = 0
indice_avatars=0
capturas_jugador = 0
capturas_bot = 0
turno_jugador = True
tiempo_restante = 60
timer_id = None

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
    reproductor.audio_set_volume(60)
    reproductor.play()

def reproducir_effecto(mp3):
    vlc.MediaPlayer(mp3).play()

def detener_musica():
    global reproductor
    if isinstance(reproductor, vlc.MediaPlayer):
        reproductor.stop()

#=====================================================Ventanas===========================================================================
def iniciar_timer():
    global tiempo_restante, timer_id,lbl_timer
    if tiempo_restante > 0:
        tiempo_restante -= 1
        lbl_timer.config(text=f"TIEMPO: {tiempo_restante}s")
        timer_id = VentanadeBatalla.after(1000, iniciar_timer)
    else:
        finalizar_por_tiempo()

def finalizar_por_tiempo():
    # Si se acaba el tiempo, rotamos los pokémons al final de la lista
    global equipo_Jugador, equipo_bot
    messagebox.showinfo("TIEMPO AGOTADO", "Los Pokémon están cansados. ¡Siguiente ronda!")
    # Lógica para mover el actual al final y pedir el siguiente
    VentanadeBatalla.after(1000, preparar_interfaz_pelea)
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
    C_Seleccion.create_window(1100, 600, window=btn_atacar,tags="botones_pelea")

    btn_defender = Button(VentanadeBatalla, text="DEFENDER", font=("Pokemon Emerald", 25),
                          command=lambda: ejecutar_accion("defender"), width=12,height=1)
    C_Seleccion.create_window(1300, 600, window=btn_defender,tags="botones_pelea") 
    

def ejecutar_accion(accion_jugador):
    global pokemon_actual_jugador, pokemon_actual_bot, p_aliado,p_rival,lbl_prueba,capturas_jugador, capturas_bot
    
    herida_al_bot = pokemon_actual_jugador["ataque"] - pokemon_actual_bot["defensa"]
    
    pokemon_actual_bot["vida"] -= herida_al_bot

    lbl_prueba.config(text=f"{pokemon_actual_jugador['nombre']} usó {accion_jugador.upper()}!")
    
    actualizar_barras_vida()

    if pokemon_actual_jugador["vida"] <= 0:
        # Verificamos si te quedan más Pokémon con vida
        vivos = [p for p in equipo_Jugador if p["vida"] > 0]
        
        if len(vivos) == 0:
            # Si no quedan más, el bot gana definitivamente
            terminar_juego("DERROTA")
        else:
            # Si quedan, pedir relevo (lo que ya teníamos)
            pedir_nuevo_pokemon()

    # 2. VERIFICAR SI MURIÓ EL BOT
    if pokemon_actual_bot["vida"] <= 0:
        pokemon_actual_bot["vida"]=pokemon_actual_bot["vida_max"]
        capturas_jugador += 1
        actualizar_contadores()
        if capturas_jugador == 3:
            terminar_juego("VICTORIA")
        else:
            messagebox.showinfo("¡DEBILITADO!", f"¡{pokemon_actual_bot['nombre']} ha caído!")
            proxima_ronda_bot()
        return
    

    # 3. ATAQUE BOT (Turno automático)
    herida_al_jugador = pokemon_actual_bot["ataque"] - pokemon_actual_jugador["defensa"]
    pokemon_actual_jugador["vida"] -= herida_al_jugador
    actualizar_barras_vida()

    # 4. VERIFICAR SI MURIÓ EL JUGADOR
    if pokemon_actual_jugador["vida"] <= 0:
        capturas_bot += 1
        actualizar_contadores()
        messagebox.showwarning("¡TU POKÉMON CAYÓ!", "Selecciona a tu siguiente guerrero.")
        pedir_nuevo_pokemon() # Aquí vuelves a habilitar los botones de selección
def verificar_final():
    global capturas_jugador, capturas_bot
    
    if capturas_jugador == 3:
        messagebox.showinfo("VICTORIA", "¡Has capturado los 3 Pokémon del rival! Eres el maestro.")
        # Volver al menú o cerrar
    elif capturas_bot == 3:
        messagebox.showerror("DERROTA", "El bot te ha ganado y se llevó a tus Pokémon...")
    accion_bot = random.choice(["atacar", "defender"])
    if accion_bot == "atacar":
        golpe_bot = max(5, p_rival["ataque"] - p_aliado["defensa"])
        p_aliado["vida"] -= golpe_bot
    
def crear_barras_vida():
    global C_Seleccion, barra_jugador, barra_bot,txt_vida_jugador, txt_vida_bot
    
    C_Seleccion.create_rectangle(945, 490, 1245, 510, fill="#4d4d4d", outline="black", tags="interfaz_vida")
    barra_jugador = C_Seleccion.create_rectangle(945, 490, 1245, 510, fill="#2ecc71", outline="", tags="interfaz_vida")
    txt_vida_jugador = C_Seleccion.create_text(1250, 515, text="100/100", font=("Pokemon Emerald", 20,"bold"), fill="black", tags="interfaz_vida")

    C_Seleccion.create_rectangle(520, 170, 820, 190, fill="#4d4d4d", outline="black", tags="interfaz_vida")
    barra_bot = C_Seleccion.create_rectangle(520, 170, 820, 190, fill="#2ecc71", outline="", tags="interfaz_vida")
    txt_vida_bot = C_Seleccion.create_text(670, 205, text="100/100", font=("Pokemon Emerald", 25), fill="black", tags="interfaz_vida")

    C_Seleccion.tag_raise("interfaz_vida")
def actualizar_barras_vida():
    global C_Seleccion, pokemon_actual_jugador, pokemon_actual_bot, barra_jugador, barra_bot,txt_vida_jugador, txt_vida_bot
    
    ancho_maximo = 300
    
    ancho_jugador = (pokemon_actual_jugador['vida'] / pokemon_actual_jugador['vida_max']) * ancho_maximo
    ancho_bot = (pokemon_actual_bot['vida'] / pokemon_actual_bot['vida_max']) * ancho_maximo

    C_Seleccion.coords(barra_jugador, 1020, 480, 1020 + ancho_jugador, 500)
    C_Seleccion.itemconfig(txt_vida_jugador, 
                          text=f"{int(pokemon_actual_jugador['vida'])}/{pokemon_actual_jugador['vida_max']}")
    
    # Barra Bot
    C_Seleccion.coords(barra_bot, 520, 170, 520 + ancho_bot, 190)
    C_Seleccion.itemconfig(txt_vida_bot, 
                          text=f"{int(pokemon_actual_bot['vida'])}/{pokemon_actual_bot['vida_max']}")
    C_Seleccion.tag_raise("interfaz_vida")
    # 3. Opcional: Cambiar a rojo si tiene poca vida
    if pokemon_actual_jugador['vida'] < (pokemon_actual_jugador['vida_max'] * 0.3):
        C_Seleccion.itemconfig(barra_jugador, fill="#e74c3c")
    else:
        C_Seleccion.itemconfig(barra_jugador, fill="#2ecc71")
    C_Seleccion.tag_raise("interfaz_vida")

def elegir_inicial(indice_equipo): 
    global pokemon_actual_jugador, pokemon_actual_bot, equipo_Jugador, equipo_bot, C_Seleccion, lbl_prueba, nombreBot,lbl_nombrePokemonBot,lbl_nombrePokemon,lbl_prueba1
    
    pokemon_actual_jugador = equipo_Jugador[indice_equipo]
    pokemon_actual_bot = equipo_bot[0] 
    if equipo_Jugador[indice_equipo]["vida"] <= 0:
        messagebox.showwarning("Invalido", "Este Pokémon está debilitado.")
        return
    C_Seleccion.imgPokeAliado = cargar_img(pokemon_actual_jugador['img_back'])
    C_Seleccion.create_image(460, 445, anchor=CENTER, image=C_Seleccion.imgPokeAliado)
    
    # El Pokémon del Rival de frente
    C_Seleccion.imgPokeRival = cargar_img(pokemon_actual_bot['img_front'])
    C_Seleccion.create_image(980, 175, anchor=N, image=C_Seleccion.imgPokeRival)

    #Actualizar burbujas de textooo
    texto_batalla = f"{nombreBot} envió a {pokemon_actual_bot['nombre']}!"
    lbl_prueba.config(text=texto_batalla)

    txt_blanco=""
    lbl_prueba1.config(text=txt_blanco)

    texto_pokemonAliado=pokemon_actual_jugador['nombre']
    lbl_nombrePokemon.config(text=texto_pokemonAliado)

    texto_pokemonBot=pokemon_actual_bot['nombre']
    lbl_nombrePokemonBot.config(text=texto_pokemonBot)

    preparar_interfaz_pelea()


def terminar_juego(resultado):
    global nombre, capturas_jugador, timer_id,capturas_bot,nombreBot, VentanadeBatalla
    
    if timer_id:
        VentanadeBatalla.after_cancel(timer_id)
    
    if resultado == "VICTORIA":
        puntos = capturas_jugador
        messagebox.showinfo("¡MAESTRO POKÉMON!", f"¡Felicidades {nombre}!Has capturado .\n: {puntos} Pokemons!")
        guardar_puntaje(nombre, puntos,"entrenador_jugador.png")
    else:
        puntos_bot = capturas_bot
        messagebox.showerror("DERROTA", f"El bot te ha vencido,\n ha capturado: {puntos_bot} Pokemons!")
        guardar_puntaje(nombre, puntos,"entrenador_bot.png")
        
    VentanadeBatalla.destroy()
    cierreTotaldeVentanas()
    ventana_ranking() 
def pedir_nuevo_pokemon():
    global C_Seleccion, lbl_prueba, lbl_prueba1
    
    # 1. Borramos los botones de ataque para que no pueda seguir pegando
    C_Seleccion.delete("botones_pelea") 
    
    # 2. Mostramos los mensajes de instrucción
    lbl_prueba.config(text="¡Tu Pokémon no puede continuar!")
    lbl_prueba1.config(text="¡Elige a tu siguiente Pokémon!")
    
    # 3. Volvemos a mostrar los botones de los Pokémon del equipo
    # Usamos la misma lógica que ya tienes en VentanaBatalla
    coords_botones = [(1100, 605), (1100, 680), (1300, 605)]
    for i in range(len(equipo_Jugador)):
        # Solo mostramos el botón si el Pokémon aún tiene vida
        if equipo_Jugador[i]["vida"] > 0:
            posX, posY = coords_botones[i]
            btn_relevo = Button(VentanadeBatalla, text=equipo_Jugador[i]["nombre"], 
                                 command=lambda idx=i: elegir_inicial(idx), 
                                 font=("Pokemon Emerald", 30), height=1, width=7)
            
            C_Seleccion.create_window(posX, posY, window=btn_relevo, tags="botones_seleccion")
def guardar_puntaje(nombre_usuario, capturas,avatar_path):
    with open("puntajes.txt", "a") as archivo:
        archivo.write(f"{nombre_usuario}|{capturas}|{avatar_path}\n")

def resetear_timer():
    global tiempo_restante, timer_id
    if timer_id:
        VentanadeBatalla.after_cancel(timer_id)
    tiempo_restante = 60
    iniciar_timer()

def proxima_ronda_bot():
    global equipo_bot, pokemon_actual_bot, C_Seleccion, lbl_nombrePokemonBot, lbl_prueba
    # 1. Verificar si la ventana existe antes de hacer nada
    if not VentanadeBatalla.winfo_exists():
        return

    if len(equipo_bot) > 0:
        # Quitamos al que acaba de morir
        equipo_bot.pop(0)
        
        # 2. Verificar si después de quitarlo aún quedan pokemons
        if len(equipo_bot) > 0:
            pokemon_actual_bot = equipo_bot[0]
            
            # Actualizamos la imagen
            C_Seleccion.imgPokeRival = cargar_img(pokemon_actual_bot['img_front'])
            C_Seleccion.create_image(980, 175, anchor=N, image=C_Seleccion.imgPokeRival)
            
            lbl_nombrePokemonBot.config(text=pokemon_actual_bot['nombre'])
            actualizar_barras_vida()
            resetear_timer()
        else:
            # Si ya no quedan, terminamos el juego y NO dibujamos nada más
            terminar_juego("VICTORIA")

def actualizar_contadores():
    global capturas_jugador, capturas_bot, lbl_contadores
    # Actualiza el Label que creamos en la VentanaBatalla
    lbl_contadores.config(text=f"Capturas: {capturas_jugador} - Rival: {capturas_bot}")

#VentanaBatalla
def VentanaBatalla():
    global ent_nombre,equipo_Jugador,nombre,equipo_bot,avatarBot,nombreBot,avatar,indice_avatars,C_Seleccion,VentanadeBatalla,lbl_prueba,lbl_prueba1,lbl_nombrePokemon,lbl_nombrePokemonBot,lbl_timer,lbl_contadores
    detener_musica()
    VentanadeBatalla=Toplevel(ventana)
    VentanadeBatalla.title("Seleccion de personaje")
    VentanadeBatalla.minsize(1470,790)
    VentanadeBatalla.resizable(width=NO, height=NO)
    VentanadeBatalla.protocol("WM_DELETE_WINDOW", cierreTotaldeVentanas)
    top_pokemons.withdraw()
    
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
    lbl_nombrePokemon=Label(VentanadeBatalla, text=f"{nombre}", font=("Pokemon Emerald", 35), fg="#2b2b2b", bg="#f5f5f5")
    C_Seleccion.create_window(1000, 460, window=lbl_nombrePokemon)

    C_Seleccion.textoPeque2 = cargar_img('TextoPeque2.png')
    C_Seleccion.create_image(600, 100, anchor=N, image=C_Seleccion.textoPeque2)
    lbl_nombrePokemonBot=Label(VentanadeBatalla, text=f"{nombreBot}", font=("Pokemon Emerald", 35), fg="#2b2b2b", bg="#f5f5f5")
    C_Seleccion.create_window(520, 170, window=lbl_nombrePokemonBot)
    
    
    lbl_prueba=Label(VentanadeBatalla, text=f"Has sido retado por el entrenador {nombreBot}!", font=("Pokemon Emerald", 35), fg="#2b2b2b", bg="#f5f5f5",border=1)
    C_Seleccion.create_window(500, 620, window=lbl_prueba)
    lbl_prueba1=Label(VentanadeBatalla, text=f"Elige que pokemon usar!", font=("Pokemon Emerald", 35), fg="#2b2b2b", bg="#f5f5f5",border=1)
    C_Seleccion.create_window(500, 660, window=lbl_prueba1)
    #------------BURBUJAS DE TEXTO------------
    crear_barras_vida()
    # Contador de capturas (Punto 4)
    lbl_contadores = Label(VentanadeBatalla, text=f"Capturas: {capturas_jugador}  Rival: {capturas_bot}", 
                           font=("Pokemon Emerald", 25),fg="black", bg="white")
    C_Seleccion.create_window(235, 50, window=lbl_contadores)

    # Timer (Punto 6)
    lbl_timer = Label(VentanadeBatalla, text="TIEMPO: 60s", font=("Pokemon Emerald", 25), fg="black", bg="white")
    C_Seleccion.create_window(1275, 50, window=lbl_timer)
    iniciar_timer()
    #------------BOTONES----------------------
    coords_botones=[(1100,605),(1100,680),(1300,605)]
    for i in range(3):
        posX,posY=coords_botones[i]
        btn1 = Button(VentanadeBatalla, text=equipo_Jugador[i]["nombre"], 
                     command=lambda idx=i: elegir_inicial(idx), font=("Pokemon Emerald", 30), height=1 ,width=10)
        
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

def elegir_pokemons():
    global indice_actual, equipo_Jugador, C_Seleccion,pokemons_ya_elegidos
    pokemon_seleccionado=pokemons[indice_actual]
    nombre_pokemon=pokemon_seleccionado["nombre"]
    
    if nombre_pokemon in pokemons_ya_elegidos:
        messagebox.showwarning("Ups!","Ese pokemon ya lo elegiste!")
        return
    if len(equipo_Jugador) < 3:
        equipo_Jugador.append(pokemon_seleccionado)
        pokemons_ya_elegidos.append(nombre_pokemon)

        #Minis de los Pokemons elegidos
        mini_img = cargar_img(pokemon_seleccionado['img_mini'])
        n = len(equipo_Jugador)
        posX = 550 + (n * 100) 
        
        setattr(C_Seleccion, f'mini_p{n}', mini_img) 
        C_Seleccion.create_image(posX, 490, image=getattr(C_Seleccion, f'mini_p{n}'))
            
    else:
        messagebox.showwarning("Ups, equipo lleno", "Ya tienes 3 Pokémon!")

#VentanaEleccion
def ventana_Pokemons():
    global lbl_nombre, panel_img, lbl_atribAtaque, lbl_atribDefensa, lbl_hp, lbl_img_avatar, ent_nombre,C_Seleccion,top_pokemons
    
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

    
    #--------------------------Interfez Avatar------------------------------
    C_Seleccion.tarjeta_avatar = cargar_img('TarjetaPrueba.png')
    C_Seleccion.create_image(345, 100, anchor=N, image=C_Seleccion.tarjeta_avatar)

    lbl_tuAvatar=Label(C_Seleccion, text="ENTRENADOR", font=("Pokemon Emerald", 25,"bold"), fg="black", bg="#f5f5f5")
    C_Seleccion.create_window(345, 160, window=lbl_tuAvatar)

    #Img avatr
    lbl_img_avatar = Label(C_Seleccion, bg="#f5f5f5")
    C_Seleccion.create_window(345, 410, window=lbl_img_avatar)

    #Nombre avatar
    lbl_NombreAvatar=Label(C_Seleccion, text="Nombre:", font=("Pokemon Emerald", 30, "bold"), fg="black", bg="#f5f5f5")
    C_Seleccion.create_window(265, 620, window=lbl_NombreAvatar)

    ent_nombre = Entry(C_Seleccion, font=("Pokemon Emerald", 30),width=10)
    C_Seleccion.create_window(410, 620, window=ent_nombre)

    #Botones
    btn_Slider_D_Avatar=Button(C_Seleccion, text="<", command=lambda: cambiar_avatar(-1), font=("Pokemon Emerald", 15))
    C_Seleccion.create_window(145, 390, window=btn_Slider_D_Avatar)
    btn_Slider_I_Avatar=Button(C_Seleccion, text=">", command=lambda: cambiar_avatar(1), font=("Pokemon Emerald", 15))
    C_Seleccion.create_window(550, 390, window=btn_Slider_I_Avatar)

    #--------------------Interfaz elegir Pokemons------------------------------------
    C_Seleccion.create_image(1155, 100, anchor=N, image=C_Seleccion.tarjeta_avatar)

    lbl_tuPokemon=Label(C_Seleccion, text="TU POKÉMON", font=("Pokemon Emerald", 20), fg="black", bg="#f5f5f5")
    C_Seleccion.create_window(1155, 160, window=lbl_tuPokemon)

    #Img Pokemon
    panel_img = Label(C_Seleccion, bg="#f5f5f5")
    C_Seleccion.create_window(1155, 390, window=panel_img)
    
    #Sliders
    btn_Slider_D_Pokemons=Button(C_Seleccion, text="<", command=lambda: cambiar_pokemon(-1), font=("Pokemon Emerald", 15))
    C_Seleccion.create_window(950, 390, window=btn_Slider_D_Pokemons)
    btn_Slider_I_Pokemons=Button(C_Seleccion, text=">", command=lambda: cambiar_pokemon(1), font=("Pokemon Emerald", 15))
    C_Seleccion.create_window(1360, 390, window=btn_Slider_I_Pokemons)

    btn_elegir = Button(C_Seleccion, text="ELEGIR POKÉMON", font=("Pokemon Emerald", 20,"bold"), command=elegir_pokemons, bg="green", fg="white")
    C_Seleccion.create_window(1155, 625, window=btn_elegir)

    # --- ATRIBUTOS (Debajo del nombre del Pokemon) ---
    lbl_nombre = Label(C_Seleccion, text="", font=("Pokemon Emerald", 25, "bold"), fg="black", bg="#f5f5f5")
    C_Seleccion.create_window(1065, 550, window=lbl_nombre)

    lbl_atribAtaque = Label(C_Seleccion, text="", font=("Pokemon Emerald", 25), fg="black", bg="#f5f5f5")
    C_Seleccion.create_window(1075, 580, window=lbl_atribAtaque)

    lbl_atribDefensa = Label(C_Seleccion, text="", font=("Pokemon Emerald", 25), fg="black", bg="#f5f5f5")
    C_Seleccion.create_window(1245, 580, window=lbl_atribDefensa)

    lbl_hp = Label(C_Seleccion, text="", font=("Pokemon Emerald", 25), fg="#107e10", bg="#f5f5f5")
    C_Seleccion.create_window(1255, 550, window=lbl_hp)

    

    #Datos del medio
    C_Seleccion.cuadro_Medio = cargar_img('FondoPrueba2.png')
    C_Seleccion.create_image(750, 150, anchor=N, image=C_Seleccion.cuadro_Medio)
    lbl_intruccionesMedio=Label(C_Seleccion, text="Elige 3 pokemones!", font=("Pokemon Emerald", 35), fg="#2b2b2b", bg="#ffffff")
    C_Seleccion.create_window(750, 300, window=lbl_intruccionesMedio)

    #BotonLuchar
    btn_listo = Button(C_Seleccion, text="LUCHAR", font=("Pokemon Emerald", 25), command=confirmar_seleccion)
    C_Seleccion.create_window(755, 600, window=btn_listo)
    
    #Minis
    C_Seleccion.fondo_mini1 = cargar_img('EspacioMinis.png')
    C_Seleccion.create_image(650, 490, image=C_Seleccion.fondo_mini1)

    C_Seleccion.fondo_mini2 = cargar_img('EspacioMinis.png')
    C_Seleccion.create_image(750, 490, image=C_Seleccion.fondo_mini2)

    C_Seleccion.fondo_mini3 = cargar_img('EspacioMinis.png')
    C_Seleccion.create_image(850, 490, image=C_Seleccion.fondo_mini3)
    

    # Inicializar Música y Datos
    reproducir_cancion(cargarMP3("SeleccionPj.mp3"))
    actualizar_avatar()
    actualizar_interfaz()


def confirmar_seleccion():
    global nombre,equipo_Jugador
    
    nombre = ent_nombre.get()
    if not nombre:
        messagebox.showerror("Error", "¡Debes ponerte un nombre!")
        return
    if len(equipo_Jugador)<3:
        messagebox.showerror("Ups","Equipo incompleto.")
        return
    detener_musica()
    reproducir_effecto(cargarMP3("ListoSoundEffect.mp3"))
    generar_rival()
    VentanaBatalla()

def ventana_ranking():
    detener_musica()
    top_puntajes = Toplevel(ventana)
    top_puntajes.title("Ranking de Entrenadores")
    top_puntajes.minsize(400, 500)
    
    Label(top_puntajes, text="TABLA DE POSICIONES", font=("Pokemon Emerald", 25)).pack(pady=10)
    
    if path.exists("puntajes.txt"):
        with open("puntajes.txt", "r") as f:
            lineas = f.readlines()
            lineas.sort(key=lambda x: int(x.split('|')[1]), reverse=True)

            for linea in lineas:
                datos = linea.strip().split("|")
                if len(datos) == 3:
                    n, p, img_path = datos
                    
                    fila = Frame(top_puntajes)
                    fila.pack(pady=10, fill=X, padx=20)
                    
                    img = cargar_img(img_path) 
                    lbl_img = Label(fila, image=img)
                    lbl_img.image = img 
                    lbl_img.pack(side=LEFT)
                    
                    Label(fila, text=f" {n.upper()} ", font=("Pokemon Emerald", 18, "bold")).pack(side=LEFT)
                    Label(fila, text=f"- {p} Capturas", font=("Pokemon Emerald", 18)).pack(side=LEFT)
    else:
        Label(top_puntajes, text="¡Aún no hay records registrados!", font=("Pokemon Emerald", 15)).pack(pady=20)
    reproducir_cancion(cargarMP3("victorytheme.mp3"))
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