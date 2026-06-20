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

import turtle
import random
import copy


class S: 
    def __init__(self, nm, hp, stam, fza, magia, hab, vel, turnos, ang):
        self.nm = nm
        self.nm_b = nm
        self.hp = hp
        self.stam = stam
        self.fza = fza
        self.magia = magia
        self.hab = hab
        self.vel = vel
        self.turnos = turnos
        self.ang = ang
        self.llave = False
        self.gran = False
        self.est = False
        self.ira = 0
        self.cur = 0

class E:
    def __init__(self, nm, hp, fza, frase):
        self.nm = nm
        self.hp = hp
        self.fza = fza
        self.frase = frase


ares = S('Ares',150, 90, 25,0, ["Espada estigia: 50 de daño en 2 ataques en toda la partida"], 1, 30, None)
ares.ira = 2

hermes = S('Hermes', 90,140, 20,0, ["Zapatillas Divinas: puedes avanzar 1 o 2 casillas en un turno"], 2, 30, None)

hecate = S('Hécate', 100, 90,15,5, ["Absorción de almas: recuperas 30 puntos de salud, 2 usos en toda la partida"],1,30,None)
hecate.cur = 2

esq = E("Esqueleto",40,10,'Te encuentras con los esqueletos del ejército de Cronos, que intentan impedir tu misión')
esp = E("Espíritu",30,12,'Notas un frío inusual, y ves un espíritu aparecer delante tuya')
lob = E("Lobos malvados",35,15,'Escuchas el aullido de unos lobos, no son tan grandes como Cerbero pero si te pueden hacer mucho daño si no acabas con ellos rápido')
cicl = E("Ciclope Ritualista",150,20,"El ritual está en plena fase, los cíclopes no van a permitir que les arruines la fiesta")
had = E("Hades",100,15,"Has enfadado al dios más poderoso de estos mundos, Hades; prepárate para sufrir su ira")
cron = E("Cronos",200,25,"Cronos ha logrado escapar del Tártaro, es tu última oportunidad de salvar todo lo que conoces de las manos del Titán")

difs = {1: (0.8, 0.8), 2: (1.0, 1.0), 3: (1.3, 1.3)}

def stats(s):
    print("-----")
    print(s.nm)
    print("HP: %d" % s.hp)
    print("Stamina: %d" % s.stam)
    print("Fuerza: %d" % s.fza)
    print(f'Magia: {s.magia}')
    print(f"Velocidad: {s.vel}")
    print(f'Hab: {s.hab}')
    print(f"Turnos: {s.turnos}")

def mapear(x,y,tipo):
    mapa[ALTO-1-y][x]=tipo # (0,0) esquina izq
def inv(j):
    print('\n===== INVENTARIO =====')
    print("Llave: %s" % j.llave)
    print(f"Estigio: {j.est}")
    print(f'Granada: {j.gran}')
def ver_map():
    print('\n==== ZONAS ====')
    for nm, xy in zonas.items():
        print("%s: %s" % (nm, xy))
def mov(j, jx, jy, ang, spd):
    nx=jx
    ny=jy
    ps=1
    if spd==2: # hermes
        while True:
            try:
                ps=int(input('¿Avanzar 1 o 2 casillas? '))
                if ps in[1,2]: break
                else: print('Solo puedes elegir 1 o 2')
            except ValueError:
                print('Dato inválido')
    cst=ps*5
    if j.stam<=cst: # agotado
        print('Te has agotado... pierdes el turno para no morirte del cansancio')
        return jx,jy
    j.stam-=cst
    print("Pierdes %d de stamina" % cst)
    print("Stamina: %d" % j.stam)
    if ang==0: nx+=ps
    elif ang==90: ny+=ps
    elif ang==180: nx-=ps
    elif ang==270: ny-=ps
    if not(0<=nx<ANCHO and 0<=ny<ALTO): # fuera mapa
        print('Intentas salir de los confines del inframundo, pero Hades es más poderoso y pierdes el turno')
        return jx,jy
    print("Nueva posición: (%d, %d)" % (nx, ny))
    return nx,ny

def desc(j): #descanso
    print('Te sientas en el suelo y te tumbas un rato a descansar')
    if random.random()>0.7: # 30% dormido
        print('Te quedaste dormido, rescuperaste fuerzas pero has perdido un turno')
        j.turnos-=1
        j.hp+=10
        j.stam+=30
        print("Salud: %d | Stam: %d" % (j.hp, j.stam))
    else:
        print('Te sientas a descansar un rato')
        j.hp+=10
        j.stam+=30
        print("Salud: %d | Stamina: %d" % (j.hp, j.stam))

def hab_a(j, en): # ares
    if j.ira<=0:
        print('No te quedan usos')
        return False
    en.hp-=50
    j.ira-=1
    print('Desatas la Ira de Ares!')
    print('Inflinges 50 de daño.')
    return True
def hab_h(j): #hecate
    if j.cur<=0:
        print('No te quedan usos')
        return False
    j.hp+=30
    j.cur-=1
    print('Absorbes las almas del inframundo')
    print('Recuperas 30 puntos de salud')
    return True

def combate(j, en, jx, jy):
    print("COMBATE CONTRA %s!" % en.nm.upper())
    while en.hp>0 and j.hp>0: # los dos vivos
        print("%s: HP %d" % (j.nm, j.hp))
        print("%s: Stamina %d" % (j.nm, j.stam))
        print("%s: Fuerza %d" % (j.nm, j.fza))
        print("%s: HP %d" % (en.nm, en.hp))
        print("%s: Fuerza %d" % (en.nm, en.fza))
        print('Es tu turno de acción:')
        print('1. Atacar')
        print('2. Habilidad')
        print('3. Huir')
        try: # no crashear
            ac=int(input('¿Qué vas a hacer? '))
            if ac not in[1,2,3]:
                print('Opción no válida')
                continue
        except ValueError:
            print('Dato inválido')
            continue
        if ac==1:
            if j.stam<10:
                print('No tienes suficiente stamina para atacar (mínimo 10)')
                print('Te escondes para recuperar stamina (+10)')
                j.stam += 10
                continue # turno enemigo
            else:
                en.hp-=j.fza
                print("Golpeas a %s y haces %d de daño." % (en.nm, j.fza))
                j.stam-=2
                print('Consumes 2 de stamina')
        elif ac==2:
            if j.nm_b=='Ares':
                if not hab_a(j,en): continue # pasar turno
            elif j.nm_b=='Hécate':
                if not hab_h(j): continue # pasar tambien
            else:
                print('Hermes no posee habilidad de combate')
                continue
        elif ac==3:
            if en.nm=='Cronos' or en.nm=='Ciclope Ritualista': # jefes
                print('No puedes huir de este combate')
            else:
                if random.random()<0.6: # 60% escape
                    print('Consigues escapar')
                    part['comb_hui']+=1
                    return 'Huida'
                else:
                    print('Intentas huir, pero el enemigo te bloquea')
        if en.hp<=0: # win
            e_derr.add((jx,jy))
            part['comb_gan']+=1
            print("¡Has derrrotado a %s!" % en.nm)
            if (jx,jy) in zonas['Enemigos']:
                zonas['Enemigos'].remove((jx,jy))
            return True
        dmg=en.fza
        j.hp-=dmg
        part['daño_t']+=dmg
        print("%s te golpea" % en.nm)
        print("Recibes %d puntos de daño" % dmg)
        if j.hp<=0: # death
            print('Has muerto en combate...')
            part['fin']='Muerte en combate'
            return False

def cas(jx,jy): # comprobar casilla
    part['recorr'].add((jx,jy))
    if (jx,jy) in e_bueno:
        EvB(jug)
        e_bueno.remove((jx,jy))
    elif (jx,jy) in e_malo:
        pos_act=(jx,jy)
        rm=EvM(jug,jx,jy)
        if rm=='Derrota': return 'Derrota'
        elif rm==True: return True
        else:
            jx,jy=rm
            e_malo.remove(pos_act)
    elif (jx,jy) in zonas['Llave'] and not jug.llave:
        print('Encuentras la llave de Bronce Celestial')
        jug.llave=True
    elif (jx,jy) in zonas['Rio_estigio'] and not jug.est:
        print('Encuentras la Lágrima del Estigio')
        jug.est=True
    elif (jx,jy) in zonas['Jardines'] and not jug.gran:
        print('Entras en los jardines y consigues la granada')
        jug.gran=True
    elif (jx,jy) in zonas['Tartaro']: # jefes
        print('Estás ante las puertas del Tártaro')
        en=genem(jx,jy,jug)
        print(en.frase)
        print("Aparece: %s" % en.nm)
        print("HP: %d | Fuerza: %d" % (en.hp, en.fza))
        bat=combate(jug,en,jx,jy)
        if bat==False:
            print('Has sido derrotado...')
            return 'Derrota'
        elif bat=='Huida':
            print('Escapas del combate')
            return jx,jy
        elif bat==True:
            if en.nm=='Cronos':
                print('¡Has derrotado a Cronos y salvado el mundo!')
                part['fin']='Has derrotado a Cronos'
            else:
                print('¡El ritual ha sido detenido y las puertas del Tártaro quedan selladas!')
                part['fin']='Cierre de las puertas del Tártaro'
            print('HAS GANADO')
            return True
    elif (jx,jy) in zonas['Praderas']:
        print('Entras en las praderas llameantes')
        print('Las praderas son muy difíciles de atravesar, pierdes 10 stamina')
        jug.stam-=10
        if jug.stam < 0: jug.stam = 0
    elif (jx,jy) in zonas['Enemigos'] or (jx,jy) in zonas['Jardines']: # enemigos gen
        en=genem(jx,jy,jug)
        if en:
            print(en.frase)
            print("Aparece: %s" % en.nm)
            print("HP: %d | Fuerza: %d" % (en.hp, en.fza))
            bat2=combate(jug,en,jx,jy)
            if bat2==False:
                print('Has sido derrotado...')
                return True
            elif bat2=='Huida':
                print('Escapas del combate')
                return jx,jy
            elif bat2==True:
                print('Enemigo derrotado')
                return jx,jy
        else:
            print('La zona está en calma...')
    if jug.llave and jug.est and jug.gran:
        print('Ya posees los tres artefactos')
        print('Dirígete al Tártaro para detener el ritual.')
    return jx,jy

def emult(eb, mhp, md): # escalar dificultad
    return E(eb.nm, int(eb.hp*mhp), int(eb.fza*md), eb.frase)

def genem(x,y,j):
    if (x,y) in zonas['Jardines']:
        ch=random.random()
        if ch<0.7: return hades
        else: return copy.deepcopy(random.choice(e_gen)) # copia para no modificar base
    if (x,y) in zonas['Tartaro']:
        if j.llave and j.est and j.gran: return ciclope
        else: return cronos
    if (x,y) in zonas['Enemigos'] and (x,y) not in e_derr:
        return random.choice(e_gen)
    return None

def EvB(j): # evento bueno -- posibilidad ampliación futura
    ev=random.randint(1,4)
    part['e_bueno']+=1
    if ev==1:
        j.stam+=15
        print('Encuentras una botella, pruebas un sorbo y es néctar, +15 stamina') # suerte
        print("Stamina: %d" % j.stam)
    elif ev==2:
        j.turnos+=3
        print('Una heroína perdida se cruza contigo, parece que necesita ayuda. Rápidamente ofreces tus servicios y ayudas a la heroína. Cuando se despide de ti decide darte su favor, el de la legendaria Helena de Troya: Consigues 3 turnos.') # referencia mitologia
        print("Turnos: %d" % j.turnos)
    elif ev==3: # OP si no tienes objetos
        if j.est==False:
            print('Divisas un comerciante a lo lejos, vende objetos de gran valor. Entre los cuales ves justo el objeto mágico que te falta, una lágrima del estigio!!')
            j.est=True
        elif j.gran==False:
            print('Divisas un comerciante a lo lejos, vende objetos de gran valor. Entre los cuales ves justo el objeto mágico que te falta, una granada del jardín de Hades!!')
            j.gran=True
        else: # mala suerte ya tienes todo
            j.hp+=5
            print('Divisas un comerciante a lo lejos, entre los objetos que vende ves una manzana tan apetecibe que te la zampas si saber sus efectos, por suerte era una manzana del Olimpo y recuperas 5 puntos de salud')
            print("Salud: %d" % j.hp)
    elif ev==4: # fuerza++
        j.fza+=5
        print('Te cruzas con un descendiente del legendario Cratos, que te da consejos para tus futuras batallas; ganas 5 puntos de fuerza')
        print("Fuerza: %d" % j.fza)

def EvM(j,jx,jy): # evento malo -- más eventos en futuras versiones
    ev2=random.randint(1,4)
    part['e_malo']+=1
    if ev2==1:
        j.stam-=15
        if j.stam<0: j.stam=0
        print('CUIDADO, una tormenta de espíritus se acerca; corres por tu vida a la cueva más cercana pero gastas 15 de energía en ponerte a salvo') # mala suerte
        print("Stamina: %d" % j.stam)
    elif ev2==2:
        print('Caminabas tranquilamente cuando de repente el suelo sucumbe bajo tus pies y te arrastran hacia lo más profundo del inframundo, las puertas del Tártaro') # tp forzado
        jx=0
        jy=5
        r.penup() # no pintar tp
        act_jug(jx,jy,jx,jy)
        jug_t.goto(*pixelar(jx,jy))
        r.goto(*pixelar(jx,jy))
        r.pendown()
        en=cronos
        print(en.frase)
        print("Aparece: %s" % en.nm)
        print("HP: %d | Fuerza: %d" % (en.hp, en.fza))
        bat3=combate(j,en,jx,jy)
        if bat3==False:
            print('Has sido derrotado...')
            return 'Derrota'
        elif bat3==True:
            print('¡Has derrotado a Cronos!')
            part['fin']='Has derrotado a Cronos'
            return True
        return jx,jy
    elif ev2==3:
        j.turnos-=3
        if j.turnos<0: j.turnos=0
        print('Sientes un escalofrío por la espalda que te deja paralizado y pierdes 3 turnos') # liar
        print("Turnos: %d" % j.turnos)
    elif ev2==4: # combate random
        en=random.choice(e_gen)
        print(en.frase)
        print("Aparece: %s" % en.nm)
        print("HP: %d | Fuerza: %d" % (en.hp, en.fza))
        bat4=combate(j,en,jx,jy)
        if bat4==False:
            print('Has sido derrotado...')
            return 'Derrota'
        elif bat4=='Huida': print('Escapas del combate')
        elif bat4==True: print('Enemigo derrotado')
    return jx,jy

def turno(j,jx,jy): # main loop turno
    global t_act
    print('\n'+'='*40)
    print("TURNO %d" % t_act)
    print("Turnos restantes: %d" % j.turnos)
    print("Pos: (%d, %d)" % (jx, jy))
    print("Ang: %d" % j.ang)
    print("Stamina: %d" % j.stam)
    print("Salud: %d" % j.hp)
    print('\n ESCOGE UNA ACCIÓN')
    print('1. Moverte')
    print('2. Cambiar angulo')
    print('3. Descansar')
    print('4. Ver inventario (gratis)')
    print('5. Ver zonas del mapa (gratis)')
    while True:
        try:
            ac2=int(input('Elige una opción: '))
            if ac2 in[1,2,3,4,5]: break
            else: print('Opción inválida')
        except ValueError:
            print('Dato inválido')
    if ac2==1:
        print('Acción elegida: Moverse')
        ox,oy=jx,jy
        jx,jy=mov(j,jx,jy,j.ang,j.vel)
        act_jug(ox,oy,jx,jy)
    elif ac2==2:
        print('Acción elegida: Cambiar angulo')
        ea=input('Que angulo quieres 0/90/180/270: ')
        if ea.isdigit() and int(ea) in[0,90,180,270]:
            if int(ea)!=j.ang: # no mismo angulo
                j.ang=int(ea)
                camb_ang(j.ang)
            else: print('Ya apuntas ahí')
        else: print('Angulo no válido')
    elif ac2==3:
        print('Acción elegida: Descansar')
        desc(j)
    elif ac2==4:
        print('Acción gratuita: inventario')
        inv(j)
        return jx,jy
    elif ac2==5:
        print('Acción gratuita: zonas')
        ver_map()
        return jx,jy
    res=cas(jx,jy) # comprobar casilla actual
    if res is True: return 'Victoria',jx,jy
    if res=='Derrota': return 'Derrota',jx,jy
    jx,jy=res # actualizar pos
    print('=== FINAL DE TURNO ===')
    print("Pos: (%d, %d)" % (jx, jy))
    print("Ang: %d" % j.ang)
    print("Stamina: %d" % j.stam)
    print("Salud: %d" % j.hp)
    j.turnos-=1
    t_act+=1
    return jx,jy

def calc_ex(j,pt): # puntuacion final
    sc=0
    if j.llave: sc+=20; print('Tienes la llave, +20 puntos')
    if j.est: sc+=20; print('Tienes la lágrima del estigio, +20 puntos')
    if j.gran: sc+=20; print('Tienes la granada, +20 puntos')
    if j.hp>100: sc+=20; print('Tienes más de 100 puntos de salud, +20 puntos')
    elif j.hp>50: sc+=10; print('Tienes más de 50 puntos de salud, +10 puntos')
    else: sc+=0; print('Tienes menos de 50 puntos de salud, +0 puntos')
    if j.turnos>15: sc+=20; print('Tienes más de 15 turnos restantes, +20 puntos')
    elif j.turnos>5: sc+=10; print('Tienes más de 5 turnos restantes, +10 puntos')
    else: sc+=0; print('Tienes menos de 5 turnos restantes, +0 puntos')
    sg=pt['comb_gan']*5
    sh=pt['comb_hui']*3
    sc+=sg-sh
    print("Has ganado %d combates, +%d puntos" % (pt['comb_gan'], sg))
    print("Has huido de %d combates, -%d puntos" % (pt['comb_hui'], sh))
    sb=pt['e_bueno']*5
    sm=pt['e_malo']*3
    sc+=sb-sm
    print("Has encontrado %d eventos buenos, +%d puntos" % (pt['e_bueno'], sb))
    print("Has encontrado %d eventos malos, -%d puntos" % (pt['e_malo'], sm))
    if sc<0: sc=0
    sd=round(pt['daño_t']//30)
    sc-=sd
    print("Has recibido %d puntos de daño, -%d puntos" % (pt['daño_t'], sd))
    return sc

def res_fin(j,razon,jx,jy):
    print('\n===== RESUMEN FINAL =====')
    print('Expedición: La Puerta del Tártaro')
    print("Héroe: %s" % j.nm)
    print("HP final: %d" % j.hp)
    print("Stamina final: %d" % j.stam)
    print("Turnos restantes: %d" % j.turnos)
    print("Posición final: (%d, %d)" % (jx, jy))
    print("Zonas visitadas: %d" % len(part['recorr']))
    print(f"Causa: {razon}")
    print("Éxito de la misión: %d/130" % calc_ex(j,part)) # casi imposible 130

play=1
while play==1:
    global t_act,e_derr
    t_act=1 # contador turnos
    e_derr=set() # enemigos ya derrotados
    # turtle setup
    pant=turtle.Screen()
    pant.tracer(0) # dibuja todo de golpe

    jug_t=turtle.Turtle() # personaje jugador
    jug_t.shape('triangle')
    jug_t.color('black')
    jug_t.penup()
    jug_t.speed(0)

    r=turtle.Turtle() # rastro movimiento
    r.speed(0)
    r.color('black')
    r.pensize(3)
    r.penup()
    r.hideturtle()

    def camb_ang(ang):
        if ang==0: jug_t.setheading(0)
        elif ang==90: jug_t.setheading(90)
        elif ang==180: jug_t.setheading(180)
        elif ang==270: jug_t.setheading(270)

    def dibj_mapa():
        pant.title('La Puerta del Tártaro')
        pant.setup(width=700,height=700)
        l=turtle.Turtle() # lapiz dibujar
        l.speed(0)
        l.hideturtle()
        tam=60
        ini=-210
        col={'Caronte':'lightblue',
             'Llave':'gold',
             'Rio_estigio':'blue',
             'Jardines':'green',
             'Tartaro':'darkred',
             'Praderas':'orange',
             'Enemigos':'gray'}
        mz={}
        for zona,xy in zonas.items():
            for c in xy: mz[c]=zona
        for y in range(ALTO):
            for x in range(ANCHO):
                px=ini+x*tam
                py=ini+y*tam
                l.penup()
                l.goto(px,py)
                l.pendown()
                zn=mz.get((x,y),None)
                if zn: color=col[zn]
                else: color='white'
                l.fillcolor(color)
                l.begin_fill()
                for _ in range(4):
                    l.forward(tam)
                    l.left(90)
                l.end_fill()
                l.penup()
                l.goto(px+5,py+5)
                l.write(f"({x},{y})",font=("Arial",8,"normal")) # coords casilla
        pant.update()
        jug_t.penup()
        r.pendown()
        ley=turtle.Turtle()
        ley.hideturtle()
        ley.penup()
        ley.speed(0)
        xl=260
        yl=200
        ley.goto(xl,yl)
        ley.write('LEYENDA',font=("Arial",14,"bold"))
        inf=[('Caronte','lightblue'),
             ('Llave','gold'),
             ('Rio_estigio','blue'),
             ('Jardines','green'),
             ('Tartaro','darkred'),
             ('Praderas','orange'),
             ('Enemigos','gray')]
        yl-=30
        for nm,color in inf:
            ley.goto(xl,yl)
            ley.color(color)
            ley.write(f"| {nm}",font=("Arial",11,"normal"))
            yl-=25

    def pixelar(x,y):
        tam=60
        ini=-210
        px=ini+x*tam+tam/2
        py=ini+y*tam+tam/2
        return px,py

    def act_jug(x,y,nx,ny):
        x2,y2=pixelar(nx,ny)
        r.goto(x2,y2)
        jug_t.goto(x2,y2)
        pant.update()

    # mapa definicion
    ANCHO=ALTO=7
    mapa=[['.']* ANCHO for _ in range(ALTO)]
    casillas=[(x,y) for x in range(ANCHO) for y in range(ALTO)]
    zonas={
        'Caronte':[(3,3)],
        'Llave':[(0,0)],
        'Rio_estigio':[(3,6),(4,6),(5,6),(6,6),(6,5)],
        'Jardines':[(4,0),(5,0),(6,0),(4,1),(5,1),(6,1)],
        'Tartaro':[(0,5),(0,6),(1,6)],
        'Praderas':[(0,2),(1,2),(2,2),(0,3),(1,3),(2,3)],
        'Enemigos':[(2,1),(2,4),(5,4)]
    }
    for tipo,coords in zonas.items():
        for x,y in coords: mapear(x,y,tipo)
    ocup=set(sum(zonas.values(),[]))
    ocup_sp=ocup-set(zonas['Caronte'])
    libres=[c for c in casillas if c not in ocup]
    e_bueno=random.sample(libres,3)
    rest=[c for c in libres if c not in e_bueno]
    e_malo=random.sample(rest,3)
    dirs={0:(1,0),90:(0,1),180:(-1,0),270:(0,-1)} # direcciones posibles
    dibj_mapa()

    # datos partida
    part={
        'nm':'','turnos_i':0,'hp_i':0,'stam_i':0,
        'pos_f':None,'turnos_f':0,'recorr':set(),
        'fin':'','resultado':'','e_bueno':0,'e_malo':0,
        'comb_gan':0,'comb_hui':0,'daño_t':0,
    }

    print('LAS PUERTAS DEL TÁRTARO - MMH-158')
    print(
    'Las puertas del Tártaro, donde están encerrados los titanes más peligrosos, se están abriendo lentamente debido a un ritual mágico que están haciendo unos cíclopes.\n\n'
    'Los dioses no pueden adentrarse en el reino de Hades para impedir que los cíclopes completen el ritual de apertura.\n'
    'Si lo consiguen, liberarán el mal al mundo.\n\n'
    'Por eso te envían a ti, joven semidiós.\n'
    'Deberás encontrar tres artefactos del inframundo:\n'
    '- La Llave de Bronce Celestial (0,0)\n'
    '- La Granada del Jardín de Hades de (4,1) a (6,0)\n'
    '- Las Lágrimas del Río Estigio de (3,6) a (6,6) y (6,5)\n\n'
    'Deberás adentrarte en el corazón del inframundo y enfrentarte a peligros que nadie jamás a visto en años para encontrar los objetos y parar el ritual. Y date prisa porque si no regresas a tiempo, quedarás encerrado para siempre en los Campos de Asfódelos, vagando como un alma en pena.'
    'En tu misión no solo se valorará el éxito del cierre de las puertas, sino que cada evento, acción y jugada se tendrán en cuenta a la hora de calificar tu misión\n\n'
    'Buena suerte'
    )
    print('Configura tu expedición antes de comenzar\n')
    input('Pulsa ENTER para continuar')
    print('Escoge tu linaje divino')
    stats(ares)
    stats(hermes)
    stats(hecate)

    jug=None
    while jug is None: # hasta elegir personaje
        el=input('Elige semidiós: ').lower()
        if el=='ares': jug=copy.deepcopy(ares)
        elif el=='hermes': jug=copy.deepcopy(hermes)
        elif el=='hecate': jug=copy.deepcopy(hecate)
        else: print('Nombre incorrecto, comprueba que hayas escrito el nombre bien y sin puntuación')

    print("Has elegido a: %s" % jug.nm)
    part['nm']=jug.nm
    part['turnos_i']=jug.turnos
    part['hp_i']=jug.hp
    part['stam_i']=jug.stam
    nm_j=input('¿Cómo quieres llamarte, semidiós? ')
    jug.nm=nm_j
    print('Ahora, vamos a escoger donde vas a empezar tu aventura')
    print('\nZONAS DEL MAPA (No puedes aparecer directamente en una zona):')
    for nm,coords in zonas.items(): # imprimir zonas
        t=', '.join([f"({x},{y})" for x,y in coords])
        print("%s: %s" % (nm, t))
    print('-------------------- \n')
    print('Lugares recomendados (no es obligatorio)\n'
        'Barca de Caronte  (ayuda inicial): (3,3)\n'
        'Cerca de la LLave: (1,1)\n'
        'Cerca del jardín de Hades: (5,2)\n'
        'Cerca del río Estigio: (4,4)')
    input('Pulsa ENTER para continuar')

    while True:
        try:
            x=int(input('Posicion X: '))
            y=int(input('Posicion Y: '))
            if not(0<=x<ANCHO and 0<=y<ALTO):
                print('Fuera del mapa')
                continue
            if (x,y) in ocup_sp:
                print('Esa casilla pertenece a una zona del mundo, elige otra')
                continue
            jug_x,jug_y=x,y
            r.penup() # no pintar teleport
            act_jug(x,y,x,y)
            jug_t.goto(*pixelar(jug_x,jug_y))
            r.goto(*pixelar(jug_x,jug_y))
            r.pendown()
            break
        except ValueError:
            print('Dato inválido, escoge otra vez')

    ps=jug_x,jug_y
    print(f"Apareces en: {ps}")
    if ps==(3,3):
        print('Recibes la ayuda de Caronte')
        jug.hp+=20
        jug.turnos+=5
        jug.stam+=20
        print('Incremento de recursos\n'
            "Salud: %d\n" % jug.hp +
            "Turnos: %d\n" % jug.turnos +
            "Stamina: %d\n" % jug.stam)

    while True:
        try:
            angulo=int(input('Elige ángulo incial (ten en cuenta que solo vas a poder moverte en la direccion en la que apunte tu personaje y gastarás turnos si quieres cambiar de angulo) 0/90/180/270: '))
            if angulo==0 or angulo==90 or angulo==180 or angulo==270:
                jug.ang=angulo
                camb_ang(jug.ang)
                pant.update()
                break
            else:
                print('Numero no válido, escoge 0/90/180/270')
                continue
        except ValueError:
            print('Dato invalido, escoge otra vez')
    jug.ang=angulo

    print('\n ELige tu provisión inicial: '
        '\n 1. Néctar del olimpo (+stamina)'
        '\n 2. Bendición de Afrodita (+hp)'
        '\n 3. Favor de Atenea (+turnos)')
    while True:
        try:
            op=None
            while op not in[1,2,3]:
                op=int(input('Elige 1, 2 o 3: '))
            if op==1:
                jug.stam+=20
                print('Has recibido néctar divino (+20 stamina)')
                print("Stamina: %d" % jug.stam)
                break
            elif op==2:
                jug.hp+=10
                print('Afrodita te bendice con vida (+10 hp)')
                print("Salud: %d" % jug.hp)
                break
            elif op==3:
                jug.turnos+=5
                print('Atenea te concede tiempo extra (+5 turnos)')
                print("Turnos: %d" % jug.turnos)
                break
        except ValueError:
            print('Dato invalido, escoge otra vez')

    print('Escoge la dificultad de la misión'
        '\n Dificultad: Fácil(x0.8), Normal(x1.0), Difícil(x1.3)')
    while True:
        try:
            dif=None
            while dif not in[1,2,3]:
                dif=int(input('Elige 1, 2 o 3: '))
            mhp,md=difs[dif]
            print(f"Dificultad modo {difs[dif]}")
            esqueleto=emult(esq,mhp,md)
            espiritu=emult(esp,mhp,md)
            lobos=emult(lob,mhp,md)
            ciclope=emult(cicl,mhp,md)
            hades=emult(had,mhp,md)
            cronos=emult(cron,mhp,md)
            e_gen=[esqueleto,espiritu,lobos]
            e_inv=[ciclope]
            e_had=[hades]
            e_cron=[cronos]
            break
        except ValueError:
            print('Dato inválido, escoge otro')

    print('\nConfiguración de inicio finalicada, comienza la aventura')
    print('En tu turno vas a poder hacer 1 acción: \n1. Moverte / Descansar / Cambiar de ángulo')

    while jug.turnos>0:
        r2=turno(jug,jug_x,jug_y)
        if isinstance(r2,tuple) and r2[0]=='Victoria':
            part['pos_f']=(jug_x,jug_y)
            part['turnos_f']=part['turnos_i']-jug.turnos
            part['resultado']='Victoria'
            res_fin(jug,part['fin'],jug_x,jug_y)
            break
        if isinstance(r2,tuple) and r2[0]=='Derrota':
            part['pos_f']=(jug_x,jug_y)
            part['turnos_f']=part['turnos_i']-jug.turnos
            part['resultado']='Derrota'
            part['fin']='Muerte'
            res_fin(jug,part['fin'],jug_x,jug_y)
            break
        else:
            jug_x,jug_y=r2

    if jug.turnos<=0:
        print('Te has quedado sin turnos, no has podido salvar el mundo y te quedarás hasta la enternidad encerrado en el inframundo.')
        part['pos_f']=(jug_x,jug_y)
        part['turnos_f']=part['turnos_i']-jug.turnos
        part['resultado']='Derrota'
        part['fin']='Sin turnos'
        res_fin(jug,part['fin'],jug_x,jug_y)

    while True:
        reset=input("¿Quieres jugar otra partida? (s/n): ").lower()
        if reset=='n':
            print('Saliendo del juego...')
            play=0
        elif reset=='s':
            print('Iniciando nueva partida...\n')
            jug_t.clear()
            jug_t.penup()
            jug_t.goto(0,0)
            r.clear()
            r.penup()
            r.goto(0,0)

            pant.clearscreen()
            pant.tracer(0)
            dibj_mapa()
            break
        else:
            print("Dato inválido, escribe 's' o 'n'")
