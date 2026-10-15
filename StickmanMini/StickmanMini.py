# ==========================================
#   STICKMAN MINI - un juego para Thumby
#   8 mundos y 2 jefes!
#   Controles:
#     Izquierda / Derecha = caminar
#     A (o Arriba)        = saltar (en el agua: nadar)
#     B                   = punetazo
#     B mientras corres   = panzazo!
#   Termina cada nivel antes de que se acabe el tiempo!
#   Junta gemas, vence a los enemigos
#   y llega a la bandera!
# ==========================================

import thumby

thumby.display.setFPS(30)

# Para practicar un mundo, cambia este numero (1 a 8)
MUNDO_INICIAL = 1

# Segundos que tienes para terminar cada nivel
TIEMPO = 60

ANCHO = 72   # ancho de la pantalla
ALTO = 40    # alto de la pantalla
W = 5        # ancho del stickman
H = 9        # alto del stickman

# ------------------------------------------
#  LOS NIVELES
#  suelo y plataformas: (x, y, ancho)
#  nubes: (x, y, ancho)  -> desaparecen al pisarlas
#  palmeras: x           -> tiran cocos
#  gemas: (x, y)
#  enemigos: (x, y, limite_izq, limite_der)
#  Cambia estos numeros para crear tus propios niveles!
# ------------------------------------------
NIVELES = [
    {   # MUNDO 1
        "nombre": "JUNGLA",
        "suelo": [(0, 36, 60), (75, 36, 50), (140, 36, 80), (235, 36, 85)],
        "plataformas": [(40, 27, 15), (90, 24, 15), (120, 18, 12),
                        (160, 26, 20), (200, 20, 15), (255, 26, 15)],
        "gemas": [(45, 22), (95, 19), (124, 13), (170, 21),
                  (205, 15), (260, 21), (290, 30)],
        "enemigos": [(150, 36, 140, 215), (250, 36, 235, 310)],
        "meta": 305,
        "vel_enemigo": 0.5,
    },
    {   # MUNDO 2
        "nombre": "NIEVE",
        "suelo": [(0, 36, 50), (68, 36, 40), (125, 36, 30),
                  (172, 36, 60), (250, 36, 70)],
        "plataformas": [(30, 28, 14), (85, 26, 14), (108, 20, 12),
                        (150, 24, 14), (195, 26, 16), (230, 20, 14)],
        "gemas": [(35, 23), (90, 21), (112, 15), (155, 19),
                  (200, 21), (234, 15), (280, 30)],
        "enemigos": [(75, 36, 68, 106), (180, 36, 172, 230), (260, 36, 250, 318)],
        "meta": 310,
        "resbala": True,    # en la nieve te resbalas!
        "vel_enemigo": 0.6,
    },
    {   # MUNDO 3
        "nombre": "VOLCAN",
        "suelo": [(0, 36, 45), (62, 36, 30), (110, 36, 25), (150, 36, 40),
                  (210, 36, 30), (258, 36, 62)],
        "plataformas": [(25, 26, 12), (92, 26, 14), (135, 22, 12),
                        (190, 26, 16), (240, 22, 14)],
        "gemas": [(28, 21), (70, 30), (96, 21), (139, 17),
                  (195, 21), (244, 17), (290, 30)],
        "enemigos": [(65, 36, 62, 90), (155, 36, 150, 188), (262, 36, 258, 318)],
        "meta": 310,
        "lava": True,       # hay lava en los huecos!
        "vel_enemigo": 0.8,
    },
    {   # MUNDO 4
        "nombre": "CIUDAD|ACUATICA",
        "suelo": [(0, 36, 80), (100, 36, 60), (180, 36, 140)],
        "plataformas": [(60, 26, 12), (130, 22, 14), (200, 18, 12), (250, 26, 14)],
        "gemas": [(30, 14), (66, 21), (90, 30), (136, 17), (170, 12),
                  (205, 13), (230, 30), (256, 21), (290, 12)],
        "enemigos": [(70, 20, 50, 120), (150, 14, 130, 200),
                     (230, 28, 190, 300), (280, 18, 250, 318)],
        "meta": 310,
        "agua": True,       # aprieta A muchas veces para nadar!
        "enemigo": "pez",
        "vel_enemigo": 0.6,
        "jefe": "tiburon",
    },
    {   # MUNDO 5
        "nombre": "NUBELANDIA",
        "suelo": [(0, 36, 30), (290, 36, 30)],
        "plataformas": [],
        "nubes": [(34, 30, 14), (56, 26, 14), (80, 30, 12), (102, 24, 14),
                  (124, 28, 12), (146, 22, 14), (170, 26, 14), (192, 30, 12),
                  (214, 24, 14), (238, 28, 14), (262, 32, 14)],
        "gemas": [(41, 25), (63, 21), (86, 25), (109, 19), (130, 23),
                  (153, 17), (177, 21), (198, 25), (221, 19), (245, 23), (269, 27)],
        "enemigos": [(295, 36, 290, 318)],
        "meta": 310,
        "vel_enemigo": 0.5,
    },
    {   # MUNDO 6
        "nombre": "PLAYA|MARAVILLA",
        "suelo": [(0, 36, 70), (85, 36, 55), (155, 36, 60), (230, 36, 90)],
        "plataformas": [(60, 26, 14), (125, 24, 14), (200, 24, 14), (270, 26, 14)],
        "palmeras": [40, 110, 175, 250],
        "gemas": [(67, 21), (100, 30), (132, 19), (190, 30),
                  (207, 19), (277, 21), (300, 30)],
        "enemigos": [(95, 36, 85, 138), (165, 36, 155, 213), (240, 36, 230, 318)],
        "meta": 310,
        "enemigo": "cangrejo",
        "vel_enemigo": 0.6,
    },
    {   # MUNDO 7
        "nombre": "ESPACIO|EXTERIOR",
        "suelo": [(0, 36, 40), (75, 36, 30), (140, 36, 30),
                  (205, 36, 30), (270, 36, 50)],
        "plataformas": [(50, 20, 12), (115, 16, 12), (180, 20, 12), (245, 16, 12)],
        "gemas": [(56, 15), (90, 25), (121, 11), (155, 25), (186, 15),
                  (220, 25), (251, 11), (300, 30)],
        "enemigos": [(80, 36, 75, 105), (145, 36, 140, 170),
                     (210, 36, 205, 235), (280, 36, 270, 318)],
        "meta": 310,
        "gravedad": 0.15,   # poca gravedad: saltas altisimo!
        "salto": -2.6,
        "estrellas": True,
        "vel_enemigo": 0.6,
    },
    {   # MUNDO 8
        "nombre": "CASTILLO DE|BLACKY",
        "suelo": [(0, 36, 40), (58, 36, 35), (112, 36, 30), (160, 36, 40),
                  (218, 36, 30), (266, 36, 54)],
        "plataformas": [(25, 26, 12), (97, 24, 12), (145, 22, 12),
                        (205, 26, 12), (250, 22, 12)],
        "gemas": [(30, 21), (75, 30), (102, 19), (150, 17), (180, 30),
                  (210, 21), (255, 17), (300, 30)],
        "enemigos": [(60, 36, 58, 93), (115, 36, 112, 142),
                     (170, 36, 160, 200), (270, 36, 266, 318)],
        "meta": 310,
        "lava": True,
        "castillo": True,
        "vel_enemigo": 0.9,
        "jefe": "blacky",
    },
]

# ------------------------------------------
#  Variables del juego
# ------------------------------------------
estado = "titulo"
espera = 0          # contador para los mensajes
cuadro = 0          # cuenta los cuadros (para animar)
nivel = 0
vidas = 3
gemas_total = 0
gemas_nivel = 0

mapa = NIVELES[0]   # el lugar donde estamos jugando ahora
en_jefe = False     # estamos peleando con un jefe?

px = 0.0
py = 0.0
vx = 0.0
vy = 0.0
en_suelo = False
mirando = 1         # 1 = derecha, -1 = izquierda
ataque = 0          # cuadros que dura el punetazo
panzazo = 0         # cuadros que dura el panzazo
camara = 0
gemas = []
enemigos = []
nubes = []
palmas = []         # [x, espera]
cocos = []          # [x, y, vy, tiempo para caer]
fuegos = []         # bolas de fuego de Blacky [x, y, vx]
jefe = None
tiempo = 0          # cuadros que le quedan al reloj
motivo = ""         # por que perdiste la vida


def texto_centrado(t, y):
    x = (ANCHO - len(t) * 6) // 2
    thumby.display.drawText(t, x, y, 1)


def choca(ax, ay, aw, ah, bx, by, bw, bh):
    return ax + aw > bx and ax < bx + bw and ay + ah > by and ay < by + bh


def poner_jugador():
    global px, py, vx, vy, en_suelo, ataque, panzazo, camara, mirando
    px = 5.0
    py = 36.0 - H
    vx = 0.0
    vy = 0.0
    en_suelo = False
    ataque = 0
    panzazo = 0
    camara = 0
    mirando = 1


def cargar_nivel(n):
    global mapa, en_jefe, gemas, enemigos, nubes, palmas, cocos, fuegos, gemas_nivel
    global tiempo
    mapa = NIVELES[n]
    tiempo = TIEMPO * 30             # 30 cuadros = 1 segundo
    en_jefe = False
    poner_jugador()
    gemas_nivel = 0
    gemas = [list(g) for g in mapa["gemas"]]
    # cada enemigo: [x, y, izq, der, direccion]
    enemigos = [[float(e[0]), e[1], e[2], e[3], 1] for e in mapa["enemigos"]]
    # cada nube: [x, y, ancho, tiempo desde que la pisaste]
    nubes = [[n2[0], n2[1], n2[2], 0] for n2 in mapa.get("nubes", [])]
    palmas = [[x, 0] for x in mapa.get("palmeras", [])]
    cocos = []
    fuegos = []


def preparar_jefe():
    # la arena del jefe: una sola pantalla
    global mapa, en_jefe, jefe, enemigos, gemas, nubes, palmas, cocos, fuegos
    datos = NIVELES[nivel]
    mapa = {
        "suelo": [(0, 36, 72)],
        "plataformas": [(6, 24, 14), (52, 24, 14)],
        "meta": 9999,
        "agua": datos.get("agua", False),
        "castillo": datos.get("castillo", False),
    }
    en_jefe = True
    enemigos = []
    gemas = []
    nubes = []
    palmas = []
    cocos = []
    fuegos = []
    if datos["jefe"] == "tiburon":
        jefe = {"tipo": "tiburon", "nombre": "REY TIBURON", "x": 55.0, "y": 18.0,
                "w": 12, "h": 7, "vx": -0.8, "vy": 0.0, "vida": 3, "max": 3,
                "inv": 30, "t": 0}
    else:
        jefe = {"tipo": "blacky", "nombre": "BLACKY", "x": 58.0, "y": 24.0,
                "w": 8, "h": 12, "vx": -0.6, "vy": 0.0, "vida": 5, "max": 5,
                "inv": 30, "t": 0}
    poner_jugador()


def volver_a_arena():
    global fuegos
    poner_jugador()
    fuegos = []
    jefe["x"] = 72.0 - jefe["w"] - 4
    jefe["inv"] = 30


def perder_vida(por=""):
    global vidas, estado, espera, motivo
    vidas -= 1
    motivo = por
    thumby.audio.play(150, 300)
    if vidas <= 0:
        estado = "continuar"
        espera = 10 * 30             # 10 segundos para decidir
    else:
        estado = "ouch"
        espera = 45


def alguno_presionado():
    # revisa todos los botones (todos, para que no se salte ninguno)
    apretados = [b.justPressed() for b in (thumby.buttonA, thumby.buttonB,
                 thumby.buttonU, thumby.buttonD, thumby.buttonL, thumby.buttonR)]
    return True in apretados


def volver_al_menu():
    # regresa al menu de juegos de la Thumby
    thumby.reset()


def golpe():
    # el lugar donde pega el punetazo o el panzazo
    if panzazo > 0:
        return (px - 2, py + 4, W + 4, 5)
    if ataque > 0:
        if mirando == 1:
            return (px + W, py + 2, 5, 5)
        return (px - 5, py + 2, 5, 5)
    return None


def mover_jugador():
    global px, py, vx, vy, en_suelo, mirando, gemas_nivel, estado, espera
    global camara, ataque, panzazo, tiempo

    # --- el reloj (no cuenta en las peleas contra jefes) ---
    if not en_jefe:
        tiempo -= 1
        if tiempo <= 10 * 30 and tiempo % 30 == 0:
            thumby.audio.play(1000, 30)  # tic, tac!
        if tiempo <= 0:
            perder_vida("TIEMPO!")
            return
    agua = mapa.get("agua", False)
    resbala = mapa.get("resbala", False)
    gravedad = mapa.get("gravedad", 0.35)
    if agua:
        gravedad = 0.1

    # --- punetazo y panzazo (boton B) ---
    if ataque > 0:
        ataque -= 1
    if panzazo > 0:
        panzazo -= 1
    if thumby.buttonB.justPressed() and ataque == 0 and panzazo == 0:
        if thumby.buttonL.pressed() or thumby.buttonR.pressed():
            panzazo = 16                 # te lanzas de panza!
            vx = 2.4 * mirando
            if en_suelo:
                vy = -1.5
            thumby.audio.play(400, 120)
        else:
            ataque = 7                   # punetazo
            thumby.audio.play(800, 40)

    # --- caminar ---
    if panzazo > 0:
        vx *= 0.97
    else:
        empuje = 0.15 if resbala else 0.4
        if thumby.buttonL.pressed():
            vx -= empuje
            mirando = -1
        elif thumby.buttonR.pressed():
            vx += empuje
            mirando = 1
        else:
            vx *= 0.94 if resbala else 0.5
        vx = max(-1.3, min(1.3, vx))

    # --- saltar o nadar ---
    if thumby.buttonA.justPressed() or thumby.buttonU.justPressed():
        if agua:
            vy = -1.8                    # brazada!
            thumby.audio.play(300, 30)
        elif en_suelo:
            vy = mapa.get("salto", -3.6)
            thumby.audio.play(600, 60)

    # --- mover a los lados ---
    x_antes = px
    px += vx
    if px < 0:
        px = 0
    if en_jefe and px > ANCHO - W:
        px = ANCHO - W
    for (bx, by, bw) in mapa["suelo"]:
        if py + H > by + 1 and px + W > bx and px < bx + bw:
            px = x_antes
            vx = 0

    # --- caer (gravedad) ---
    vy += gravedad
    maximo = 1.2 if agua else (2 if gravedad < 0.3 else 4)
    if vy > maximo:
        vy = maximo
    abajo_antes = py + H
    py += vy
    if agua and py < 8:
        py = 8                           # la superficie del agua
        vy = 0
    cayendo = vy > 0
    en_suelo = False
    if vy >= 0:
        for (bx, by, bw) in mapa["suelo"] + mapa["plataformas"]:
            if px + W > bx and px < bx + bw and abajo_antes <= by and py + H >= by:
                py = by - H
                vy = 0
                en_suelo = True
        for nb in nubes:
            if nb[3] < 30 and px + W > nb[0] and px < nb[0] + nb[2] \
                    and abajo_antes <= nb[1] and py + H >= nb[1]:
                py = nb[1] - H
                vy = 0
                en_suelo = True
                if nb[3] == 0:
                    nb[3] = 1            # la nube empieza a desaparecer

    # --- las nubes desaparecen y despues vuelven ---
    for nb in nubes:
        if nb[3] > 0:
            nb[3] += 1
            if nb[3] > 130:
                nb[3] = 0

    # --- se cayo al hueco ---
    if py > ALTO:
        perder_vida()
        return

    # --- gemas ---
    for g in gemas:
        if abs(px + 2 - g[0]) < 4 and abs(py + 4 - g[1]) < 6:
            gemas.remove(g)
            gemas_nivel += 1
            thumby.audio.play(1200, 50)
            break

    # --- tus golpes ---
    gp = golpe()
    if gp:
        for e in enemigos:
            if choca(gp[0], gp[1], gp[2], gp[3], e[0], e[1] - 4, 5, 4):
                enemigos.remove(e)
                thumby.audio.play(1000, 60)
                break
        for c in cocos:
            if choca(gp[0], gp[1], gp[2], gp[3], c[0] - 1, c[1] - 1, 3, 3):
                cocos.remove(c)
                thumby.audio.play(700, 40)
                break

    # --- enemigos ---
    for e in enemigos:
        e[0] += e[4] * mapa["vel_enemigo"]
        if e[0] < e[2] or e[0] + 5 > e[3]:
            e[4] = -e[4]
        ex = e[0]
        ey = e[1] - 4
        if choca(px, py, W, H, ex, ey, 5, 4):
            if cayendo and abajo_antes <= ey + 2:
                enemigos.remove(e)       # le saltaste encima!
                vy = -2.5
                thumby.audio.play(900, 80)
            else:
                perder_vida()
            return

    # --- palmeras y cocos ---
    for p in palmas:
        if p[1] > 0:
            p[1] -= 1
        elif abs(px + 2 - p[0]) < 20:
            cocos.append([p[0], 17.0, 0.0, 12])   # un coco va a caer!
            p[1] = 60
            thumby.audio.play(250, 40)
    for c in cocos:
        if c[3] > 0:
            c[3] -= 1                    # el coco tiembla antes de caer
            continue
        c[2] += 0.25
        c[1] += c[2]
        if choca(px, py, W, H, c[0] - 1, c[1] - 1, 3, 3):
            perder_vida()
            return
        if c[1] > 35:
            cocos.remove(c)

    # --- el jefe ---
    if en_jefe:
        if mover_jefe(gp, cayendo, abajo_antes):
            return

    # --- llegaste a la bandera ---
    if px + W >= mapa["meta"]:
        if NIVELES[nivel].get("jefe"):
            estado = "jefe_intro"
            espera = 60
            thumby.audio.play(200, 400)
        else:
            estado = "nivel_ok"
            espera = 60
            thumby.audio.play(1500, 200)

    # --- la camara sigue al stickman ---
    largo = mapa["meta"] + 15
    camara = int(px) - 30
    camara = max(0, min(largo - ANCHO, camara))
    if en_jefe:
        camara = 0


def mover_jefe(gp, cayendo, abajo_antes):
    # regresa True si algo importante paso (te pegaron o ganaste)
    global vy, estado, espera
    j = jefe
    j["t"] += 1
    if j["inv"] > 0:
        j["inv"] -= 1

    if j["tipo"] == "tiburon":
        # nada de lado a lado y te persigue hacia arriba y abajo
        j["x"] += j["vx"]
        if j["x"] < 0 or j["x"] > ANCHO - j["w"]:
            j["vx"] = -j["vx"]
        if j["y"] < py:
            j["y"] += 0.25
        else:
            j["y"] -= 0.25
        j["y"] = max(9, min(29, j["y"]))
    else:
        # Blacky camina hacia ti, salta y lanza fuego
        rapido = 1.0 if j["vida"] <= 2 else 0.6
        j["vx"] = rapido if px > j["x"] else -rapido
        j["x"] += j["vx"]
        j["x"] = max(0, min(ANCHO - j["w"], j["x"]))
        j["vy"] += 0.35
        j["y"] += j["vy"]
        if j["y"] + j["h"] >= 36:
            j["y"] = 36 - j["h"]
            j["vy"] = 0
            if j["t"] % 70 == 0:
                j["vy"] = -3.5           # salto!
        if j["t"] % 80 == 40:
            lado = 1 if px > j["x"] else -1
            fx = j["x"] + (j["w"] if lado == 1 else 0)
            fuegos.append([fx, j["y"] + 6, 1.4 * lado])
            thumby.audio.play(180, 100)

    # bolas de fuego
    for f in fuegos:
        f[0] += f[2]
        if f[0] < -4 or f[0] > ANCHO + 4:
            fuegos.remove(f)
        elif choca(px, py, W, H, f[0] - 1, f[1] - 1, 3, 3):
            perder_vida()
            return True

    jx, jy, jw, jh = j["x"], j["y"], j["w"], j["h"]
    if j["inv"] == 0:
        pego = False
        if gp and choca(gp[0], gp[1], gp[2], gp[3], jx, jy, jw, jh):
            pego = True
        elif choca(px, py, W, H, jx, jy, jw, jh):
            if cayendo and abajo_antes <= jy + 3:
                pego = True
                vy = -3.0                # rebotas en su cabeza
            else:
                perder_vida()
                return True
        if pego:
            j["vida"] -= 1
            j["inv"] = 40
            thumby.audio.play(1300, 120)
            if j["tipo"] == "tiburon":
                j["vx"] = (abs(j["vx"]) + 0.25) * (1 if jx > px else -1)
            if j["vida"] <= 0:
                estado = "jefe_ok"
                espera = 90
                thumby.audio.play(2000, 500)
                return True
    return False


# ------------------------------------------
#  DIBUJOS
# ------------------------------------------
def linea(sx, sy, m, x1, y1, x2, y2):
    # dibuja una linea; si m = -1 la voltea (espejo)
    if m == -1:
        x1 = 4 - x1
        x2 = 4 - x2
    thumby.display.drawLine(sx + x1, sy + y1, sx + x2, sy + y2, 1)


def dibujar_stickman(sx, sy, caminando):
    d = thumby.display
    m = mirando
    if panzazo > 0:
        # acostado, volando de panza
        cabeza = 5 if m == 1 else -3
        d.drawRectangle(sx + cabeza, sy + 5, 3, 3, 1)
        linea(sx, sy, m, 0, 6, 5, 6)      # cuerpo
        linea(sx, sy, m, 8, 5, 9, 5)      # brazos al frente
        linea(sx, sy, m, 0, 6, -3, 5)     # piernas
        linea(sx, sy, m, 0, 6, -3, 7)
        return
    d.drawRectangle(sx + 1, sy, 3, 3, 1)             # cabeza
    d.drawLine(sx + 2, sy + 3, sx + 2, sy + 6, 1)    # cuerpo
    if ataque > 0:
        linea(sx, sy, m, 2, 4, 7, 4)                 # punetazo!
        puno = 7 if m == 1 else -4
        d.drawFilledRectangle(sx + puno, sy + 3, 2, 3, 1)
        linea(sx, sy, m, 2, 4, 0, 5)
    else:
        d.drawLine(sx, sy + 4, sx + 4, sy + 4, 1)    # brazos
    paso = (cuadro // 4) % 2 if caminando else 0
    if paso == 0:
        d.drawLine(sx + 2, sy + 6, sx, sy + 8, 1)
        d.drawLine(sx + 2, sy + 6, sx + 4, sy + 8, 1)
    else:
        d.drawLine(sx + 2, sy + 6, sx + 1, sy + 8, 1)
        d.drawLine(sx + 2, sy + 6, sx + 3, sy + 8, 1)


def dibujar_gema(x, y):
    d = thumby.display
    d.setPixel(x, y - 1, 1)
    d.setPixel(x - 1, y, 1)
    d.setPixel(x + 1, y, 1)
    d.setPixel(x, y + 1, 1)


def dibujar_enemigo(x, y, direccion):
    d = thumby.display
    tipo = mapa.get("enemigo", "")
    if tipo == "pez":
        d.drawFilledRectangle(x, y - 3, 4, 3, 1)
        cola = x + 4 if direccion == -1 else x - 1
        d.drawLine(cola, y - 4, cola, y, 1)
        d.setPixel(x + (1 if direccion == -1 else 2), y - 2, 0)
    elif tipo == "cangrejo":
        d.drawFilledRectangle(x, y - 3, 5, 3, 1)
        d.setPixel(x - 1, y - 4, 1)      # tenazas
        d.setPixel(x + 5, y - 4, 1)
        d.setPixel(x + 1, y - 2, 0)
        d.setPixel(x + 3, y - 2, 0)
    else:
        d.drawFilledRectangle(x, y - 4, 5, 4, 1)
        d.setPixel(x + 1, y - 3, 0)
        d.setPixel(x + 3, y - 3, 0)


def dibujar_palmera(x):
    d = thumby.display
    d.drawLine(x, 35, x + 1, 19, 1)
    d.drawLine(x + 1, 18, x - 4, 21, 1)
    d.drawLine(x + 1, 18, x + 6, 21, 1)
    d.drawLine(x + 1, 18, x - 3, 15, 1)
    d.drawLine(x + 1, 18, x + 5, 15, 1)


def dibujar_jefe():
    d = thumby.display
    j = jefe
    # barra de vida del jefe
    for i in range(j["vida"]):
        d.drawFilledRectangle(26 + i * 4, 1, 3, 2, 1)
    if j["inv"] > 0 and (j["inv"] // 3) % 2 == 1:
        return                           # parpadea cuando le pegas
    x = int(j["x"])
    y = int(j["y"])
    if j["tipo"] == "tiburon":
        izq = j["vx"] < 0                # hacia donde mira
        d.drawFilledRectangle(x + (0 if izq else 2), y + 2, 10, 4, 1)
        c = x + 10 if izq else x + 1     # cola
        d.drawLine(c, y + 3, c + (1 if izq else -1), y + 1, 1)
        d.drawLine(c, y + 4, c + (1 if izq else -1), y + 6, 1)
        d.drawLine(x + 4, y + 1, x + 7, y + 1, 1)   # aleta
        d.setPixel(x + 5, y, 1)
        ojo = x + 2 if izq else x + 9
        d.setPixel(ojo, y + 3, 0)
        for i in range(3):                           # dientes
            d.setPixel(ojo + (i * 2 if izq else -i * 2), y + 5, 0)
    else:
        # Blacky: todo negro con ojos brillantes y cuernos
        d.drawRectangle(x + 1, y, 6, 4, 1)          # cabeza
        d.setPixel(x + 1, y - 1, 1)                  # cuernos
        d.setPixel(x, y - 2, 1)
        d.setPixel(x + 6, y - 1, 1)
        d.setPixel(x + 7, y - 2, 1)
        d.setPixel(x + 2, y + 1, 1)                  # ojos
        d.setPixel(x + 5, y + 1, 1)
        d.drawRectangle(x + 1, y + 4, 6, 6, 1)      # cuerpo
        d.drawLine(x + 1, y + 4, x - 1, y + 10, 1)  # capa
        d.drawLine(x + 6, y + 4, x + 8, y + 10, 1)
        d.drawLine(x + 2, y + 10, x + 2, y + 11, 1)  # piernas
        d.drawLine(x + 5, y + 10, x + 5, y + 11, 1)


def visible(x, ancho):
    return x + ancho >= 0 and x < ANCHO


def dibujar_fondo():
    d = thumby.display
    cam = camara
    if mapa.get("estrellas"):
        for i in range(16):
            d.setPixel((i * 29 - cam // 3) % ANCHO, 9 + (i * 11) % 22, 1)
    if mapa.get("agua"):
        for x in range(0, ANCHO, 3):      # olas arriba
            d.setPixel(x, 7 + (x // 3 + cuadro // 6) % 2, 1)
        for i in range(5):                # burbujas
            d.setPixel((i * 17 + 5 - cam // 2) % ANCHO,
                       35 - ((cuadro + i * 23) // 2) % 26, 1)
    if mapa.get("castillo"):
        for i in range(3):                # columnas del castillo
            cx = (i * 40 - cam // 2) % 120 - 24
            for y in range(10, 34, 2):
                d.setPixel(cx, y, 1)
                d.setPixel(cx + 6, y, 1)
        for x in range(0, ANCHO, 6):      # almenas
            d.drawFilledRectangle(x, 8, 3, 2, 1)
    if mapa.get("lava"):
        for x in range(0, ANCHO, 2):
            d.setPixel(x, 38 + (x // 2 + cuadro // 4) % 2, 1)


def dibujar_nivel():
    d = thumby.display
    cam = camara
    dibujar_fondo()

    for (bx, by, bw) in mapa["suelo"]:
        if visible(bx - cam, bw):
            d.drawFilledRectangle(bx - cam, by, bw, ALTO - by, 1)
    for (bx, by, bw) in mapa["plataformas"]:
        if visible(bx - cam, bw):
            d.drawFilledRectangle(bx - cam, by, bw, 2, 1)
    for nb in nubes:
        if nb[3] < 30 and visible(nb[0] - cam, nb[2]):
            if nb[3] > 15 and cuadro % 4 < 2:
                continue                  # parpadea antes de desaparecer
            x = nb[0] - cam
            d.drawRectangle(x, nb[1], nb[2], 3, 1)
            d.drawLine(x + 2, nb[1] - 1, x + nb[2] - 3, nb[1] - 1, 1)

    for p in palmas:
        if visible(p[0] - cam - 5, 12):
            dibujar_palmera(p[0] - cam)
    for c in cocos:
        tiembla = (cuadro % 2) if c[3] > 0 else 0
        d.drawFilledRectangle(int(c[0]) - cam - 1 + tiembla, int(c[1]) - 1, 3, 3, 1)

    for g in gemas:
        if visible(g[0] - cam, 2):
            dibujar_gema(g[0] - cam, g[1])

    for e in enemigos:
        ex = int(e[0]) - cam
        if visible(ex, 5):
            dibujar_enemigo(ex, e[1], e[4])

    if en_jefe:
        dibujar_jefe()
        for f in fuegos:
            fx = int(f[0])
            fy = int(f[1])
            dibujar_gema(fx, fy)
            if cuadro % 2:
                d.setPixel(fx, fy, 1)
    else:
        fx = mapa["meta"] - cam           # bandera
        if visible(fx, 6):
            d.drawLine(fx, 35, fx, 22, 1)
            d.drawFilledRectangle(fx + 1, 22, 5, 3, 1)

    caminando = (abs(vx) > 0.3 and en_suelo) or (mapa.get("agua") and not en_suelo)
    dibujar_stickman(int(px) - cam, int(py), caminando)

    # marcador: el reloj (parpadea cuando quedan 10 segundos)
    if not en_jefe and (tiempo > 10 * 30 or (cuadro // 5) % 2 == 0):
        t = str((tiempo + 29) // 30)
        d.drawText(t, 36 - len(t) * 3, 0, 1)

    # marcador: gemas y vidas
    dibujar_gema(2, 3)
    d.drawText(str(gemas_total + gemas_nivel), 5, 0, 1)
    for i in range(vidas):
        hx = 68 - i * 5
        d.setPixel(hx, 1, 1)
        d.setPixel(hx + 2, 1, 1)
        d.drawLine(hx, 2, hx + 2, 2, 1)
        d.setPixel(hx + 1, 3, 1)


# ------------------------------------------
#  CICLO PRINCIPAL
# ------------------------------------------
while True:
    cuadro += 1
    d = thumby.display
    d.fill(0)

    if estado == "titulo":
        texto_centrado("STICKMAN", 3)
        texto_centrado("MINI", 12)
        dibujar_stickman((cuadro // 2) % 80 - 5, 29, True)
        if (cuadro // 15) % 2 == 0:
            texto_centrado("Pulsa A", 21)
        if thumby.buttonA.justPressed():
            nivel = MUNDO_INICIAL - 1
            vidas = 3
            gemas_total = 0
            estado = "intro"
            espera = 50

    elif estado == "intro":
        texto_centrado("MUNDO " + str(nivel + 1), 4)
        partes = NIVELES[nivel]["nombre"].split("|")
        for i in range(len(partes)):
            texto_centrado(partes[i], 18 + i * 10)
        espera -= 1
        if espera <= 0:
            cargar_nivel(nivel)
            estado = "jugar"

    elif estado == "jugar":
        mover_jugador()
        dibujar_nivel()

    elif estado == "jefe_intro":
        if (cuadro // 6) % 2 == 0:
            texto_centrado("CUIDADO!", 6)
        texto_centrado("JEFE:", 18)
        texto_centrado("BLACKY" if NIVELES[nivel]["jefe"] == "blacky"
                       else "REY TIBURON", 28)
        espera -= 1
        if espera <= 0:
            preparar_jefe()
            estado = "jugar"

    elif estado == "ouch":
        texto_centrado(motivo if motivo else "AY!", 8)
        texto_centrado("Vidas: " + str(vidas), 20)
        espera -= 1
        if espera <= 0:
            if en_jefe:
                volver_a_arena()
            else:
                cargar_nivel(nivel)
            estado = "jugar"

    elif estado == "jefe_ok":
        texto_centrado("VENCISTE A", 6)
        texto_centrado(jefe["nombre"], 18)
        dibujar_stickman(33, 28, False)
        espera -= 1
        if espera <= 0:
            estado = "nivel_ok"
            espera = 60

    elif estado == "nivel_ok":
        texto_centrado("BIEN!", 8)
        texto_centrado("Gemas: " + str(gemas_nivel), 20)
        espera -= 1
        if espera <= 0:
            gemas_total += gemas_nivel
            gemas_nivel = 0
            nivel += 1
            if nivel >= len(NIVELES):
                estado = "ganaste"
                thumby.audio.play(2000, 400)
            else:
                estado = "intro"
                espera = 50

    elif estado == "continuar":
        texto_centrado("CONTINUAR?", 3)
        texto_centrado(str((espera + 29) // 30), 16)
        if (cuadro // 10) % 2 == 0:
            texto_centrado("Pulsa algo", 30)
        apreto = alguno_presionado()
        if espera % 30 == 0:
            thumby.audio.play(500, 40)
        espera -= 1
        if apreto and espera < 10 * 30 - 15:
            vidas = 3              # vuelves al principio del mismo mundo
            gemas_nivel = 0
            estado = "intro"
            espera = 50
        elif espera <= 0:
            volver_al_menu()       # nadie apreto nada: al menu de la Thumby

    elif estado == "ganaste":
        texto_centrado("GANASTE!", 4)
        texto_centrado("Gemas: " + str(gemas_total), 16)
        texto_centrado("Pulsa A", 28)
        if thumby.buttonA.justPressed():
            estado = "titulo"

    d.update()
