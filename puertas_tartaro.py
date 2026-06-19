###
# Nota del Autor
# Videojuego: Las Puertas del Tártaro
# 
# Autor: Manuel Migoya Herber (MMH-158)
# 
# Este videojuego ha sido creado para la competición GIGATHON 2026 ESPAÑA y no se usará para otros fines a menos que así lo diga el autor propio(yo)
# 
# Muchas gracias y a disfrutar
# ###
# DEFinicioN DE CLASES

class S: 
    def __init__(self, nm, hp, stam, fuerza, magia, hab, vel, turnos, ang):
        self.nm = nm
        self.nm_b = nm
        self.hp = hp
        self.stam = stam
        self.fuerza = fuerza
        self.magia = magia
        self.hab = hab
        self.vel = vel
        self.turnos = turnos
        self.angulo = ang
        self.llave = False
        self.granada = False
        self.estigio = False
        self.ira = 0
        self.curar = 0

class E:
    def __init__(self, nm, hp, fuerza, frase):
        self.nm = nm
        self.hp = hp
        self.fuerza = fuerza
        self.frase = frase
        
# DEFinicioN DE SEMIDIOSES Y ENEMIGOS

ares = S(
    'Ares',150, 90, 25,  0, ["Espada estigia: 50 de daño en 2 ataques en toda la partida"], 1, 30, None
)
ares.ira = 2

hermes = S(
    'Hermes', 90,  140, 20, 0, ["Zapatillas Divinas: puedes avanzar 1 o 2 casillas en un turno"], 2, 30, None
)

hecate = S(
    'Hécate', 100, 90 , 15,5, ["Absorción de almas: recuperas 30 puntos de salud, 2 usos en toda la partida"],1, 30, None
)
hecate.curar = 2

esq = E (
    "Esqueleto", 40,10, "Te encuentras con los esqueletos del ejército de Cronos, que intentan impedir tu misión"
)

esp = E (
    "Espíritu", 30, 12, "Notas un frío inusual, y ves un espíritu aparecer delante tuya"
)

lob = E (
    "Lobos malvados", 35, 15 , "Escuchas el aullido de unos lobos, no son tan grandes como Cerbero pero si te pueden hacer mucho daño si no acabas con ellos rápido"
)

cicl = E (
    "Ciclope Ritualista", 150, 20, "El ritual está en plena fase, los cíclopes no van a permitir que les arruines la fiesta"
)

had = E (
    "Hades", 100, 15, "Has enfadado al dios más poderoso de estos mundos, Hades; prepárate para sufrir su ira"
)

cron = E (
    "Cronos", 200, 25, "Cronos ha logrado escapar del Tártaro, es tu última oportunidad de salvar todo lo que conoces de las manos del Titán"
)

dificultades = {
    1: (0.8, 0.8),
    2: (1.0, 1.0),
    3: (1.3, 1.3),
}

import turtle
import random
from random import random
import copy
from copy import deepcopy

# DEFINICION DE FUNCIONES

def stats(S):
    print("-----")
    print(S.nm)
    print(f"HP: {S.hp}")
    print(f"Stamina: {S.stam}")
    print(f"Fuerza: {S.fuerza}")
    print(f"Magia: {S.magia}")
    print(f"Velocidad: {S.vel}")
    print(f"Habilidad: {S.hab}")
    print(f"Turnos: {S.turnos}")

def mapear(x,y,tipo):
    mapa[ALTO - 1 - y][x]=tipo # Esto para tener (0,0) en la esquina izq
def inv(jug):
    print("\n===== inv =====")
    print(f"Llave: {jug.llave}")
    print(f"Lágrima del Estigio: {jug.estigio}")
    print(f"Granada: {jug.granada}")
def ver_map():
    print("\n===== ZONAS DEL MAPA =====")
    for nm, coords in zonas.items():
        print(f"{nm}: {coords}")
def mov(jug, jug_x, jug_y, angulo, speed):
    nuevo_x=jug_x
    nuevo_y=jug_y

    pasos=1
    
    if speed==2: # en caso de que sea hermes
        while True:
            try:
                pasos=int (input("¿Avanzar 1 o 2 casillas? "))
                if pasos in[1, 2]:
                    break
                else: print("Solo puedes elegir 1 o 2")
            except ValueError:
                print("Dato inválido")
    coste=pasos * 5
    
    if jug.stam<=coste: # si intentas avanzar dos no avanzará ni uno
        print("Te has agotado... pierdes el turno para no morirte del cansancio")
        return jug_x,jug_y


    jug.stam-=coste
    print(f"Pierdes {coste} de stamina por moverte")
    print(f"Stamina actual: {jug.stam}")
    if angulo==0: # movimiento hacia adelante
        nuevo_x+=pasos
    elif angulo==90:
        nuevo_y+=pasos
    elif angulo==180:
        nuevo_x-=pasos
    elif angulo==270:
        nuevo_y-=pasos

    

    if not(0 <= nuevo_x < ANCHO and 0 <= nuevo_y < ALTO):
        print("Intentas salir de los confines del inframundo, pero Hades es más poderoso y pierdes el turno")
        return jug_x, jug_y 

    print(f"Nueva posición: ({nuevo_x}, {nuevo_y})") # si estas dentro del mapa
    return nuevo_x, nuevo_y

def desc(jug):
    print("Te sientas en el suelo y te tumbas un rato a descansar")
    if random.random() > 0.7: # 30% dormido
        print("Te quedaste dormido, rescuperaste fuerzas pero has perdido un turno")
        jug.turnos -= 1
        jug.hp += 10
        jug.stam += 30
        print(f"Salud: {jug.hp} | Stam: {jug.stam}")
    else: 
        print("Te sientas a descansar un rato")
        jug.hp += 10
        jug.stam += 30
        print(f"Salud: {jug.hp} | Stamina: {jug.stam}")

def hab_a(jug, e): # ares
    if jug.ira <= 0:
        print("No te quedan usos")
        return False
    e.hp -= 50
    jug.ira -= 1
    print("¡Desatas la Ira de Ares!")
    print("Inflinges 50 de daño.")
    return True
  
def hab_h(jug): #hecate
    if jug.curar <= 0:
        print("No te quedan usos")
        return False
    jug.hp += 30
    jug.curar -= 1
    print("Absorbes las almas del inframundo")
    print("Recuperas 30 puntos de salud")
    return True

def combate(jug, e, jug_x, jug_y):
    print(f"COMBATE CONTRA {e.nm.upper()}!")

    while e.hp >0 and jug.hp >0: # Los Dos Estan Vivos
        print(f"{jug.nm}: HP {jug.hp}")
        print(f"{jug.nm}: Stamina {jug.stam}")
        print(f"{jug.nm}: Fuerza {jug.fuerza}")
        print(f"{e.nm}: HP {e.hp}")
        print(f"{e.nm}: Fuerza {e.fuerza}")

        print(f"Es tu turno de acción:")
        print("1. Atacar")
        print("2. Habilidad")
        print("3. Huir")

        try:
            accion =int(input("¿Qué vas a hacer? "))
            if accion not in [1,2,3]:
                print("Opción no válida")
                continue
        except ValueError:
            print("Dato inválido")
            continue

        if accion ==1: 
            if jug.stam <10:
                print("No tienes suficiente stamina para atacar (mínimo 10)")
                continue # pasar a turno e
            else:
                e.hp -=jug.fuerza
                print(f"Golpeas a {e.nm} y haces {jug.fuerza} de daño.")
                jug.stam -=2
                print("Consumes 2 de stamina")
        elif accion ==2:
            if jug.nm_b =="Ares":
                if not hab_a(jug, e): continue # pasar turno
            elif jug.nm_b =="Hécate":
                if not hab_h(jug): continue # pasar tambien
            else:
                print("Hermes no posee habilidad de combate")
                continue
        elif accion ==3:
            if e.nm =="Cronos" or e.nm =="Ciclope Ritualista": # combate final
                print("No puedes huir de este combate") 
            else:
                if random.random() <0.6: # 60%
                    print("Consigues escapar")
                    part["comb_hui"] +=1
                    return "Huida"
                else: 
                    print("Intentas huir, pero el enemigo te bloquea")
        if e.hp <=0: # win
            e_derr.add((jug_x, jug_y))
            part["comb_gan"] +=1
            print(f"¡Has derrrotado a {e.nm}!")
            if (jug_x, jug_y) in zonas["Enemigos"]:
                zonas ["Enemigos"].remove((jug_x, jug_y))
            return True
        daño =e.fuerza
        jug.hp -=daño
        part["daño_t"] +=daño
        print(f"{e.nm} te golpea")
        print(f"Recibes {daño} puntos de daño")

        if jug.hp <=0: # death
            print("Has muerto en combate...")
            part["fin"] ="Muerte en combate"
            return False

def cas (jug_x, jug_y): # ver en que casilla está
    part["recorr"].add((jug_x, jug_y))
    if (jug_x, jug_y) in e_bueno:
        EvBueno (jug)
        e_bueno.remove((jug_x, jug_y))
    elif (jug_x, jug_y) in e_malo:
        casilla = (jug_x, jug_y)
        resultado = EvMal (jug, jug_x, jug_y)
        if resultado == "Derrota":
            return  "Derrota"
        else:
            jug_x, jug_y = resultado
            e_malo.remove(casilla)
    elif (jug_x, jug_y) in zonas["Llave"] and not jug.llave:
        print("Encuentras la llave de Bronce Celestial")
        jug.llave =  True
    elif (jug_x, jug_y) in zonas["Rio_estigio"] and not jug.estigio:
        print("Encuentras la Lágrima del Estigio")
        jug.estigio = True
    elif (jug_x, jug_y) in zonas["Jardines"] and not jug.granada:
        print("Entras en los jardines y consigues la granada")
        jug.granada = True 
    elif (jug_x, jug_y) in zonas["Tartaro"]: # enemigos tartaro
        print("Estás ante las puertas del Tártaro")
        e = gen_enem(jug_x, jug_y, jug)

        print(e.frase)
        print(f"Aparece: {e.nm}")
        print(f"HP enemigo: {e.hp} | Fuerza: {e.fuerza}")

        batalla = combate (jug, e, jug_x, jug_y)

        if batalla ==  False:
            print("Has sido derrotado...")
            return "Derrota"

        elif batalla == "Huida":
            print("Escapas del combate")
            return jug_x, jug_y

        elif batalla == True:
            if e.nm == "Cronos":
                print ("¡Has derrotado a Cronos y salvado el mundo!")
                part["fin"] = "Has derrotado a Cronos"
            else:
                print("¡El ritual ha sido detenido y las puertas del Tártaro quedan selladas!")
                part["fin"] = "Cierre de las puertas del Tártaro"
            print("HAS GANADO")
            return True
    elif (jug_x, jug_y) in zonas["Praderas"]:
        print("Entras en las praderas llameantes")
        print("Las praderas son muy difíciles de atravesar, pierdes 10 stamina")
        jug.stam -= 10
    elif  ((jug_x, jug_y) in zonas["Enemigos"] or (jug_x, jug_y) in zonas ["Jardines"]): # enemigos gen
        e = gen_enem(jug_x, jug_y, jug) 

        if e:
            print(f"{e.frase}") 
            print(f"Aparece: {e.nm}")
            print(f"HP enemigo: {e.hp} | Fuerza: {e.fuerza}")

            batalla = combate(jug, e, jug_x, jug_y)
            if batalla == False:
                print("Has sido derrotado...")
                return  True
            elif batalla == "Huida":
                print("Escapas del combate")
                return jug_x,jug_y
            elif batalla == True:
                print("Enemigo derrotado")
                return jug_x,jug_y
        else:
            print("La zona está en calma...")

    if jug.llave and jug.estigio and jug.granada:
        print("Ya posees los tres artefactos")
        print("Dirígete al Tártaro para detener el ritual.")

    return jug_x,jug_y

def enem_mult(e_base, mult_hp, mult_dmg): # dificultad
    return E(
        e_base.nm,
        int(e_base.hp * mult_hp),
        int(e_base.fuerza * mult_dmg),
        e_base.frase
    )

def gen_enem(x, y, jug):
    if (x, y) in zonas["Jardines"]:
        if random.random() < 0.7:
            return hades
        else: 
            return copy.deepcopy(random.choice(e_gen)) # guardar hp default
    
    if (x, y) in zonas["Tartaro"]:
        if jug.llave and jug.estigio and jug.granada:
            return ciclope
        else: 
            return cronos
        
    if (x, y) in zonas["Enemigos"] and (x, y) not in e_derr:
        return random.choice(e_gen)
    else:
        return None

def EvBueno(jug): # posibilidad ampliación
    evento = random.randint(1,4)
    part["e_bueno"] += 1
    if evento == 1:
        jug.stam += 15
        print("Encuentras una botella, pruebas un sorbo y es néctar, +15 stamina") # ++
        print(f"Stamina actual: {jug.stam}")
    elif evento == 2:
        jug.turnos += 3
        print("Una heroína perdida se cruza contigo, parece que necesita ayuda. Rápidamente ofreces tus servicios y ayudas a la heroína. Cuando se despide de ti decide darte su favor, el de la legendaria Helena de Troya: Consigues 3 turnos.") # referencia
        print(f"Turnos actuales: {jug.turnos}")
    elif evento == 3: # OP
        if jug.estigio == False:
            print("Divisas un comerciante a lo lejos, vende objetos de gran valor. Entre los cuales ves justo el objeto mágico que te falta, una lágrima del estigio!!")
            jug.estigio = True
        elif jug.granada == False:
            print("Divisas un comerciante a lo lejos, vende objetos de gran valor. Entre los cuales ves justo el objeto mágico que te falta, una granada del jardín de Hades!!")
            jug.granada = True
        else: # mala suerte
            jug.hp += 5
            print("Divisas un comerciante a lo lejos, entre los objetos que vende ves una manzana tan apetecibe que te la zampas si saber sus efectos, por suerte era una manzana del Olimpo y recuperas 5 puntos de salud")
            print(f"Salud actual: {jug.hp}")
    elif evento == 4: # +++
        jug.fuerza += 5
        print("Te cruzas con un descendiente del legendario Cratos, que te da consejos para tus futuras batallas; ganas 5 puntos de fuerza")
        print(f"Fuerza actual: {jug.fuerza}")


def EvMal(jug, jug_x, jug_y): # más eventos
    evento = random.randint(1,4)
    part["e_malo"] += 1
    if evento == 1:
        jug.stam -= 15
        print("CUIDADO, una tormenta de espíritus se acerca; corres por tu vida a la cueva más cercana pero gastas 15 de energía en ponerte a salvo") # fastidiar
        print(f"Stamina actual: {jug.stam}")
    elif evento == 2:
        print("Caminabas tranquilamente cuando de repente el suelo sucumbe bajo tus pies y te arrastran hacia lo más profundo del inframundo, las puertas del Tártaro") # muerte
        jug_x = 0
        jug_y = 5
    elif evento == 3:
        jug.turnos -= 3
        print("Sientes un escalofrío por la espalda que te deja paralizado y pierdes 3 turnos") # liar
        print(f"Turnos actuales: {jug.turnos}")
    elif evento == 4: # detener
        e = random.choice(e_gen)

        print(f"{e.frase}")
        print(f"Aparece: {e.nm}")
        print(f"HP enemigo: {e.hp} | Fuerza: {e.fuerza}")

        batalla = combate(jug, e, jug_x, jug_y)
        if batalla == False:
            print("Has sido derrotado...")
            return "Derrota"
        elif batalla == "Huida":
            print("Escapas del combate")
        elif batalla == True:
            print("Enemigo derrotado")

    return jug_x, jug_y
def turno(jug, jug_x, jug_y): # main def
    global t_act

    print("\n" + "="*40)
    print(f"TURNO {t_act}")
    print(f"Turnos restantes {jug.turnos}")
    print(f"Posición: ({jug_x}, {jug_y})")
    print(f"Ángulo: {jug.angulo}")
    print(f"Stamina: {jug.stam}")
    print(f"Salud: {jug.hp}")

    print("\n ESCOGE UNA ACCIÓN")
    print("1. Moverte")
    print("2. Cambiar angulo")
    print("3. Descansar")
    print("4. Ver inventario (gratis)")
    print("5. Ver zonas del mapa (gratis)")

    while True:
        try:
            accion= int(input("Elige una opción: "))
            if accion in [1,2,3,4,5]:
                break
            else:
                print("Opción inválida")
        except ValueError:
            print("Dato inválido")
    
    if accion == 1: 
        print("Acción elegida: Moverse")
        old_x, old_y = jug_x, jug_y

        jug_x, jug_y = mov(jug,jug_x,jug_y,jug.angulo,jug.vel)
        act_jug(old_x, old_y, jug_x, jug_y)
    elif accion == 2:
        print("Acción elegida: Cambiar angulo")
        elec_ang = input("Que angulo quieres 0/90/180/270: ")
        if elec_ang.isdigit() and int(elec_ang) in [0,90,180,270]:
            if int(elec_ang) != jug.angulo: # ayuda -> no cambiar a mismo angulo
                jug.angulo = int(elec_ang)
                camb_ang(jug.angulo)
            else:
                print("Ya apuntas ahí")
        else:
            print("Angulo no válido")
    elif accion == 3:
        print("Acción elegida: Descansar")
        desc(jug)
    elif accion == 4:
        print("Acción gratuita: Mostrar inventario")
        inv(jug)
        return jug_x, jug_y
    elif accion == 5:
        print("Acción gratuita: Mostrar zonas")
        ver_map()
        return jug_x, jug_y

    result = cas(jug_x, jug_y) # ver casilla posicion
    if result is True:
        return "Victoria", jug_x, jug_y
    if result == "Derrota":
        return "Derrota", jug_x, jug_y
    # si no gana o pierde sigue
    jug_x, jug_y = result
    print("=== FINAL DE TURNO ===")
    print(f"Posición: ({jug_x}, {jug_y})")
    print(f"Ángulo: {jug.angulo}")
    print(f"Stamina: {jug.stam}")
    print(f"Salud: {jug.hp}")

    jug.turnos -= 1
    t_act += 1
    return jug_x, jug_y

def ex(jug, part):
    score = 0
    if jug.llave: score += 20; print("Tienes la llave, +20 puntos")
    if jug.estigio: score += 20; print("Tienes la lágrima del estigio, +20 puntos")
    if jug.granada: score += 20; print("Tienes la granada, +20 puntos")

    if jug.hp > 100: score += 20; print("Tienes más de 100 puntos de salud, +20 puntos")
    elif jug.hp > 50: score += 10; print("Tienes más de 50 puntos de salud, +10 puntos")
    else: score += 0

    if jug.turnos > 15: score += 20; print("Tienes más de 15 turnos restantes, +20 puntos")
    elif jug.turnos > 5: score += 10; print("Tienes más de 5 turnos restantes, +10 puntos")
    else: score += 0

    score_gan = part["comb_gan"] * 5
    score_huir = part["comb_hui"] * 3
    score += score_gan - score_huir
    print(f"Has ganado {part['comb_gan']} combates, +{score_gan} puntos")
    print(f"Has huido de {part['comb_hui']} combates, -{score_huir} puntos")

    score_b = part["e_bueno"] * 5
    score_m = part["e_malo"] * 3
    score += score_b - score_m
    print(f"Has encontrado {part['e_bueno']} eventos buenos aleatorios, +{score_b} puntos")
    print(f"Has encontrado {part['e_malo']} eventos malos aleatorios, -{score_m} puntos")
    if score < 0: score = 0

    score_d = round(part["daño_t"] // 30)
    score -= score_d
    print(f"Has recibido {part['daño_t']} puntos de daño, -{score_d} puntos")
    return score


def fin(jug, razon, jug_x, jug_y):
    print("\n===== RESUMEN FINAL =====")
    print(f"Expedición: La Puerta del Tártaro")
    print(f"Nombre del héroe: {jug.nm}")
    print(f"HP final: {jug.hp}")
    print(f"Stamina final: {jug.stam}")
    print(f"Turnos restantes: {jug.turnos}")
    print(f"Posición final: ({jug_x}, {jug_y})")
    print(f"Zonas visitadas: {len(part['recorr'])}")
    print(f"Causa de finalización: {razon}") 
    print(f"Éxito de la misión: {ex(jug, part)}/140")

play = 1
while play == 1:
    global t_act, e_derr

    t_act = 1 # contar turnos
    e_derr = set() # enemigs derrot
    # TURTLE
    pant = turtle.Screen()
    pant.tracer(0) # dibujar de seguido


    jug_t = turtle.Turtle() # Jugador
    jug_t.shape("triangle")
    jug_t.color("black")
    jug_t.penup()
    jug_t.speed(0)

    r = turtle.Turtle()  # Rastro
    r.speed(0)
    r.color("black")
    r.pensize(3)
    r.penup()
    r.hideturtle()

    def camb_ang(ang):
        if ang== 0:
            jug_t.setheading(0)
        elif ang== 90:
            jug_t.setheading(90)
        elif ang== 180:
            jug_t.setheading(180)
        elif ang== 270:
            jug_t.setheading(270)

    def dibj_mapa():
        pant.title("La Puerta del Tártaro")
        pant.setup(width=700, height=700)

        l= turtle.Turtle() # Lapiz
        l.speed(0)
        l.hideturtle()

        tam= 60
        inicio= -210

        col= {
            "Caronte": "lightblue",
            "Llave": "gold",
            "Rio_estigio": "blue",
            "Jardines": "green",
            "Tartaro": "darkred",
            "Praderas": "orange",
            "Enemigos": "gray"
        }
        map_z= {}
        for zona, coords in zonas.items():
            for c in coords:
                map_z[c] = zona

        for y in range(ALTO):
            for x in range(ANCHO):
                px= inicio + x*tam
                py= inicio + y*tam

                l.penup()
                l.goto(px, py)
                l.pendown()

                zona= map_z.get((x,y), None)
                if zona:
                    color= col[zona]
                else:
                    color= "white"
                l.fillcolor(color)
                l.begin_fill()

                for _ in range(4):
                    l.forward(tam)
                    l.left(90)
                l.end_fill()

                l.penup() 
                l.goto(px+5, py+5)
                l.write(f"({x},{y})", font=("Arial", 8, "normal")) # coords
        pant.update() # dibujar de seguido
        jug_t.penup()
        jug_t.goto(jug_t.position())
        r.pendown()

        leyenda= turtle.Turtle()
        leyenda.hideturtle()
        leyenda.penup()
        leyenda.speed(0)

        x_leyenda= 260
        y_leyenda= 200
        leyenda.goto(x_leyenda, y_leyenda)
        leyenda.write("LEYENDA", font=("Arial", 14, "bold")) # leyenda

        info= [
            ("Caronte", "lightblue"),
            ("Llave", "gold"),
            ("Rio_estigio", "blue"),
            ("Jardines", "green"),
            ("Tartaro", "darkred"),
            ("Praderas", "orange"),
            ("Enemigos", "gray")
        ]

        y_leyenda-= 30
        for nm, color in info:
            leyenda.goto(x_leyenda, y_leyenda)
            leyenda.color(color)
            leyenda.write(f"| {nm}", font=("Arial", 11, "normal")) # info leyenda
            y_leyenda-= 25

    def pixelar(x, y):
        tam = 60
        inicio = -210
        px = inicio + x*tam + tam/2
        py = inicio + y*tam + tam/2
        return px, py

    def act_jug(x, y, nuevo_x, nuevo_y):
        x2, y2 = pixelar(nuevo_x, nuevo_y)

        r.goto(x2, y2)
        jug_t.goto(x2, y2)

        pant.update()

    # MAPA

    ANCHO = ALTO = 7

    mapa = [["."] * ANCHO for _ in range(ALTO)]
    casillas = [(x,y) for x in range(ANCHO) for y in range(ALTO)]

    zonas = {
        "Caronte": [(3,3)],
        "Llave": [(0,0)],
        "Rio_estigio": [(3,6),(4,6),(5,6),(6,6),(6,5)],
        "Jardines": [(4,0),(5,0),(6,0),(4,1),(5,1),(6,1)],
        "Tartaro": [(0,5),(0,6),(1,6)],
        "Praderas": [(0,2),(1,2),(2,2),(0,3),(1,3),(2,3)],
        "Enemigos": [(2,1), (2,4), (5,4)]
    }


    for tipo, coords in zonas.items():
        for x,y in coords:
            mapear(x,y,tipo)

    ocupadas = set(sum(zonas.values(), []))
    ocupadas_spawn = ocupadas - set(zonas["Caronte"])
    libres = [c for c in casillas if c not in ocupadas]

    e_bueno = random.sample(libres,3)
    resto = [c for c in libres if c not in e_bueno]
    e_malo = random.sample(resto, 3)

    direcciones = {
        0: (1, 0),    # derecha
        90: (0, 1),   # arriba
        180: (-1, 0), # izquierda
        270: (0, -1)  # abajo
    }

    dibj_mapa()

    # inicio DE VIDEOJUEGO

    part = {
        "nm": "",
        "turnos_i": 0,
        "hp_i": 0,
        "stam_i": 0,
        "pos_f": None,
        "turnos_f": 0,
        "recorr": set(),
        "fin": "",
        "resultado": "",
        "e_bueno": 0,
        "e_malo": 0,
        "comb_gan": 0,
        "comb_hui": 0,
        "daño_t": 0,
    }

    print("LAS PUERTAS DEL TÁRTARO - MMH-158")
    print(
    "Las puertas del Tártaro, donde están encerrados los titanes más peligrosos, se están abriendo lentamente debido a un ritual mágico que están haciendo unos cíclopes.\n\n"
    "Los dioses no pueden adentrarse en el reino de Hades para impedir que los cíclopes completen el ritual de apertura.\n"
    "Si lo consiguen, liberarán el mal al mundo.\n\n"
    "Por eso te envían a ti, joven semidiós.\n"
    "Deberás encontrar tres artefactos del inframundo:\n"
    "- La Llave de Bronce Celestial (0,0)\n"
    "- La Granada del Jardín de Hades de (4,1) a (6,0)\n"
    "- Las Lágrimas del Río Estigio de (3,6) a (6,6) y (6,5) \n\n"
    "Deberás adentrarte en el corazón del inframundo y enfrentarte a peligros que nadie jamás a visto en años para encontrar los objetos y parar el ritual. Y date prisa porque si no regresas a tiempo, quedarás encerrado para siempre en los Campos de Asfódelos, vagando como un alma en pena."
    "En tu misión no solo se valorará el éxito del cierre de las puertas, sino que cada evento, acción y jugada se tendrán en cuenta a la hora de calificar tu misión\n\n"
    "Buena suerte"
    )
    print("Configura tu expedición antes de comenzar\n")
    input("Pulsa ENTER para continuar")
    print("Escoge tu linaje divino")
    stats(ares)
    stats(hermes)
    stats(hecate)


    jug = None

    while jug is None: # repetir hasta nombre escogido
        eleccion = input("Elige semidiós: ").lower()
        if eleccion == "ares":
            jug = copy.deepcopy(ares)
        elif eleccion == "hermes":
            jug = copy.deepcopy(hermes)
        elif eleccion == "hecate":
            jug = copy.deepcopy(hecate)
        else:
            print("Nombre incorrecto, comprueba que hayas escrito el nombre bien y sin puntuación")


    print(f"Has elegido a: {jug.nm}")
    part["nm"] = jug.nm
    part["turnos_i"] = jug.turnos
    part["hp_i"] = jug.hp
    part["stam_i"] = jug.stam
    nm_jug = input("¿Cómo quieres llamarte, semidiós? ")
    jug.nm = nm_jug
    print("Ahora, vamos a escoger donde vas a empezar tu aventura")
    print("\nZONAS DEL MAPA (No puedes aarecer directamente en una zona):")

    for nm, coords in zonas.items(): # print zonas
        t = ", ".join([f"({x},{y})" for x, y in coords])
        print(f"{nm}: {t}")
    print("-------------------- \n")
    print("Lugares recomendados (no es obligatorio)\n"
        "Barca de Caronte  (ayuda inicial): (3,3)\n" 
        "Cerca de la LLave: (1,1)\n"
        "Cerca del jardín de Hades: (5,2)\n"
        "Cerca del río Estigio: (4,4)")
    input("Pulsa ENTER para continuar")

    while True:
        try:
            x = int(input("Posicion X: "))
            y = int(input("Posicion Y: "))

            if not (0 <= x < ANCHO and 0 <= y < ALTO):
                print("Fuera del mapa")
                continue
            
            if (x,y) in ocupadas_spawn:
                print("Esa casilla pertenece a una zona del mundo, elige otra")
                continue
            
            jug_x, jug_y = x,y
            r.penup() # para no pintar en el tp
            act_jug(x, y, x, y)
            jug_t.goto(*pixelar(jug_x, jug_y))
            r.goto(*pixelar(jug_x, jug_y))
            r.pendown()
            break
        except ValueError: 
            print("Dato inválido, escoge otra vez")
    pos = jug_x, jug_y
    print(f"Apareces en: {pos}")
    if pos == (3,3):
        print("Recibes la ayuda de Caronte")
        jug.hp += 20
        jug.turnos += 5
        jug.stam += 20
        print("Incremento de recursos\n"
            f"Salud: {jug.hp}\n"
            f"Turnos: {jug.turnos}\n"
            f"Stamina: {jug.stam}\n")
        

    while True:
        try:
            angulo = int(input("Elige ángulo incial (ten en cuenta que solo vas a poder moverte en la direccion en la que apunte tu personaje y gastarás turnos si quieres cambiar de angulo) 0/90/180/270: "))
            if angulo == 0 or angulo == 90 or angulo == 180 or angulo == 270:
                jug.angulo = angulo
                camb_ang(jug.angulo)
                pant.update()
                break
            else: 
                print("Numero no válido, escoge 0/90/180/270")
                continue

        except ValueError:
            print("Dato invalido, escoge otra vez")
    jug.angulo = angulo

    print("\n ELige tu provisión inicial: "
        "\n 1. Néctar del olimpo (+stamina)"
        "\n 2. Bendición de Afrodita (+hp)"
        "\n 3. Favor de Atenea (+turnos)")
    while True:
        try:
            opcion = None
            while opcion not in [1,2,3]:
                opcion = int(input("Elige 1, 2 o 3: "))

            if opcion == 1:
                jug.stam += 20
                print("Has recibido néctar divino (+20 stamina)")
                print(f"Stamina: {jug.stam}")
                break
            elif opcion == 2:
                jug.hp += 10
                print("Afrodita te bendice con vida (+10 hp)")
                print(f"Salud: {jug.hp}")
                break
            elif opcion == 3:
                jug.turnos += 5
                print("Atenea te concede tiempo extra (+5 turnos)")
                print(f"Turnos: {jug.turnos}")
                break
        except ValueError:
            print("Dato invalido, escoge otra vez")

    print("Escoge la dificultad de la misión"
        "\n Dificultad: Fácil(x0.8), Normal(x1.0), Difícil(x1.3)")
    while True:
        try:
            dificultad = None
            while dificultad not in [1,2,3]:
                dificultad = int(input("Elige 1, 2 o 3: "))

            mult_hp, mult_dmg = dificultades[dificultad]
            print(f"Dificultad modo {dificultades[dificultad]}")
            esqueleto = enem_mult(esq, mult_hp, mult_dmg)
            espiritu = enem_mult(esp, mult_hp, mult_dmg)
            lobos = enem_mult(lob, mult_hp, mult_dmg)
            ciclope = enem_mult(cicl, mult_hp, mult_dmg)
            hades = enem_mult(had, mult_hp, mult_dmg)
            cronos = enem_mult(cron, mult_hp, mult_dmg)

            e_gen = [esqueleto, espiritu, lobos]
            e_inv = [ciclope]
            e_had = [hades]
            e_cron = [cronos]       
            break

        except ValueError:
            print("Dato inválido, escoge otro")

    print("\nConfiguración de inicio finalicada, comienza la aventura")

    print("En tu turno vas a poder hacer 1 acción: " 
    "\n1. Moverte / Descansar / Cambiar de ángulo")

    while jug.turnos > 0:
        resultado = turno(jug, jug_x, jug_y)

        if isinstance(resultado, tuple) and resultado[0] == "Victoria":
            part["pos_f"] = (jug_x, jug_y)
            part["turnos_f"] = part["turnos_i"] - jug.turnos
            part["resultado"] = "Victoria"
            fin(jug, part["fin"], jug_x, jug_y)
            break

        if isinstance(resultado, tuple) and resultado[0] == "Derrota":
            part["pos_f"] = (jug_x, jug_y)
            part["turnos_f"] = part["turnos_i"] - jug.turnos
            part["resultado"] = "Derrota"
            part["fin"] = "Muerte"
            fin(jug, part["fin"], jug_x, jug_y)
            break

        else: 
            jug_x, jug_y = resultado

    if jug.turnos <= 0:    
        print("Te has quedado sin turnos, no has podido salvar el mundo y te quedarás hasta la enternidad encerrado en el inframundo.")
        part["pos_f"] = (jug_x, jug_y)
        part["turnos_f"] = part["turnos_i"] - jug.turnos
        part["resultado"] = "Derrota"
        part["fin"] = "Sin turnos"
        fin(jug, part["fin"], jug_x, jug_y)
    
    while True:
        reset = input("¿Quieres jugar otra partida? (s/n): ").lower()

        if reset == "n":
            print("Saliendo del juego...")
            play = 0   
        elif reset == "s":
            print("Iniciando nueva partida...\n")
            pant.clearscreen()
            pant = turtle.Screen()
            pant.tracer(0)
            jug_t = turtle.Turtle()
            jug_t.shape("triangle")
            jug_t.color("black")
            jug_t.penup()
            jug_t.speed(0)
            r = turtle.Turtle()
            r.speed(0)
            r.color("black")
            r.pensize(3)
            r.penup()
            r.hideturtle()
            dibj_mapa()
            break   
        else:
            print("Dato inválido, escribe 's' o 'n'")
        


