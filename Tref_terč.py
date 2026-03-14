import sys
import pygame
import random
import math
import json
import os
pygame.init()
# Plocha
rozliseni_okna = (800, 600)
barva_pozadi = (255, 255, 255)
okno = pygame.display.set_mode(rozliseni_okna)
# FPS hry
vsync = pygame.time.Clock()
FPS = 60
# Font
font = pygame.font.SysFont(None, 48)
font_tlacitka = pygame.font.SysFont(None, 32)
font_nazev = pygame.font.SysFont(None, 110)
font_vybrat_slot = pygame.font.SysFont(None, 25)
font_zpet = pygame.font.SysFont(None, 48)
# Informace pro čtvereček
velikost_ctverecku = 50
ctverecek_x = (rozliseni_okna[0] - velikost_ctverecku) - 700
ctverecek_y = (rozliseni_okna[1] - velikost_ctverecku) // 2
posun_ctverecku = 8
# Informace pro terč
sirka_terce = vyska_terce = 75
terc_x = (rozliseni_okna[0] - sirka_terce) - 50
terc_y = (rozliseni_okna[1] - vyska_terce) // 2
# Terč druhý
sirka_terce_2 = vyska_terce_2 = 50
# Terč třetí
sirka_terce_3 = vyska_terce_3 = 25
# Počet peněz
penize = 0
# Stav mapy
aktualni_mapa = 0
# Inventář
inventare = []
# Questy
class Quest:
    def __init__(self, nazev, popis, cil, odmena):
        self.nazev = nazev
        self.popis = popis
        self.cil = cil
        self.postup = 0
        self.odmena = odmena
        self.splneno = False

    def pridej_postup(self, kolik=1):
        if not self.splneno:
            self.postup += kolik
            if self.postup >= self.cil:
                self.splneno = True
                return True
        return False
questy = [
    Quest("Střelec", "Tref 10 terčů", 10, 50),
    Quest("Hasič", "Uhas všechny ohně!", 1, 100),
    Quest("Boháč", "Nasbírej 500 peněz", 500, 0),
    Quest("Boss", "Poraž Draka a vyhraj hru!", 1, 100)
]
aktualni_quest_index = 0
# Tlačítka
tlacitko_m = pygame.Rect(10, 60, 120, 50)
tlacitko_ob = pygame.Rect(10, 5, 120, 50)
tlacitko_i = pygame.Rect(136, 5, 120, 50)
tlacitko_b = pygame.Rect(136, 60, 120, 50)
tlacitko_s = pygame.Rect(0, 0, 120, 50)
tlacitko_s.center = (rozliseni_okna[0] // 2, rozliseni_okna[1] - 350)
tlacitko_u = pygame.Rect(0, 0, 120, 50)
tlacitko_u.center = (rozliseni_okna[0] // 2, rozliseni_okna[1] - 290)
tlacitko_od = pygame.Rect(0, 0, 120, 50)
tlacitko_od.center = (rozliseni_okna[0] // 2, rozliseni_okna[1] - 230)
tlacitko_1 = pygame.Rect(0, 0, 120, 50)
tlacitko_1.center = (rozliseni_okna[0] // 2, 260)
tlacitko_2 = pygame.Rect(0, 0, 120, 50)
tlacitko_2.center = (rozliseni_okna[0] // 2, 320)
tlacitko_3 = pygame.Rect(0, 0, 120, 50)
tlacitko_3.center = (rozliseni_okna[0] // 2, 380)
tlacitko_zpet = pygame.Rect(5, rozliseni_okna[1] - 40, 80, 35)
vybrany_slot = None
zobrazit_slot_menu = False
tlacitko_ulozit = pygame.Rect(0,0,150,50)
tlacitko_restart = pygame.Rect(0,0,150,50)
tlacitko_ulozit.center = (rozliseni_okna[0]//2 - 100, rozliseni_okna[1]//2 + 150)
tlacitko_restart.center = (rozliseni_okna[0]//2 + 100, rozliseni_okna[1]//2 + 150)
# Barva inventáře
barva_inventaree = (145, 96, 68)
# Počet srdíček
pocet_zivotu = 100
#Informace pro střelu (Šíp)
strela_leti = False 
rychlost_strely = 10
# Informace pro nahnutý luk
nahnuty_luk_x = 0.866
nahnuty_luk_y = -0.5

# Čas terče
terc_spawn_cas = pygame.time.get_ticks()
terc_ceka = 1500
terc_vyparovani = 2000
def nahodna_pozice_terce():
    global terc_spawn_cas
    x = rozliseni_okna[0] - sirka_terce - 50
    y = random.randint(0, rozliseni_okna[1] - vyska_terce)
    terc_spawn_cas = pygame.time.get_ticks()
    return x, y
# Ceny itemů
cena_luk = 50
cena_helma = 80
cena_brneni = 120
cena_heal_potion = 100
cena_fire_resistance_potion = 100
cena_coin_potion = 120
# False hry
konec_hry = False
vyhra = False
mesto_uhaseno = False
# Stav nákupu
koupeno_luk = False
koupeno_helma = False
koupeno_brneni = False
koupeno_heal_potion = False
koupeno_fire_resistance_potion = False
koupeno_coin_potion = False
#  ----------- Vykreslení -----------
# Vytvoření Hráče 
archer = pygame.Rect(ctverecek_x, ctverecek_y, velikost_ctverecku, velikost_ctverecku)
start_pozice_hrace = archer.topleft
# Vykreslení šípu
obrazek_sipu = pygame.image.load("./sip_strela.png").convert_alpha()
sip = pygame.transform.scale_by(obrazek_sipu, 0.15)
sip_rect = sip.get_rect()
# Vykreslení srdíčka
obrazek_srdicka = pygame.image.load("./srdicko.png").convert_alpha()
srdicko = pygame.transform.scale_by(obrazek_srdicka, 0.1)
srdicko_rect = srdicko.get_rect(center=(rozliseni_okna[0] // 1.58, 55))
# Prazdné srdíčko
obrazek_prazdneho_srdicka = pygame.image.load("./prazdne_srdicko.png").convert_alpha()
prazdne_srdicko = pygame.transform.scale_by(obrazek_prazdneho_srdicka, 0.1)
prazdne_srdicko_rect = prazdne_srdicko.get_rect(center=(rozliseni_okna[0] // 1.58, 55))
# Pozadí 2. Mapy
obrazek_horiciho_mesta = pygame.image.load("./horici_mesto.png").convert_alpha()
horici_mesto = pygame.transform.scale(obrazek_horiciho_mesta, rozliseni_okna)
horici_mesto_rect = horici_mesto.get_rect(topleft=(0, 0))
mesto_odemcene = False
# Pozadí 3. Mapy
obrazek_obchodu = pygame.image.load("./obchod_pozadí.png").convert_alpha()
obchod = pygame.transform.scale(obrazek_obchodu, rozliseni_okna)
obchod_rect = obchod.get_rect(topleft=(0, 0))
# Pozadí 5. Mapy
obrazek_jeskyne = pygame.image.load("./boss_pozadi.png").convert_alpha()
jeskyne = pygame.transform.scale(obrazek_jeskyne, rozliseni_okna)
jeskyne_rect = jeskyne.get_rect(topleft=(0, 0))
# Pozadí Menu
obrazek_menu = pygame.image.load("./menu_pozadi.png").convert_alpha()
menu = pygame.transform.scale(obrazek_menu, rozliseni_okna)
menu_rect = menu.get_rect(topleft=(0, 0))
# Pozadí Trénovací zony
obrazek_treninku = pygame.image.load("./trenovaci_zona_pozadi.png").convert_alpha()
trenink = pygame.transform.scale(obrazek_treninku, rozliseni_okna)
trenink_rect = trenink.get_rect(topleft=(0, 0))
# Pozadí Menu
obrazek_inventare = pygame.image.load("./inventory_pozadi.png").convert_alpha()
inventar = pygame.transform.scale(obrazek_inventare, rozliseni_okna)
inventar_rect = inventar.get_rect(topleft=(0, 0))
# Vykreslení Ohně
obrazek_ohne = pygame.image.load("./ohen.png").convert_alpha()
ohen = pygame.transform.scale_by(obrazek_ohne, 0.35)
ohen_rect = ohen.get_rect(center=(rozliseni_okna[0] // 2, 25))
# Vykreslení Vylitého kbeliku
obrazek_vyliteho_kbeliku = pygame.image.load("./kbelik_vylity.png").convert_alpha()
vylity_kbelik = pygame.transform.scale_by(obrazek_vyliteho_kbeliku, 0.4)
vylity_kbelik_rect = vylity_kbelik.get_rect(center=(rozliseni_okna[0] // 2, 25))
# Vykreslení Vody pro kbelik
obrazek_vody_kbeliku = pygame.image.load("./voda_kbeliku.png").convert_alpha()
voda_kbeliku = pygame.transform.scale_by(obrazek_vody_kbeliku, 0.4)
voda_kbeliku_rect = voda_kbeliku.get_rect(center=(rozliseni_okna[0] // 2, 25))
voda_aktivni = False
voda_rect = voda_kbeliku.get_rect()
cas_vody = 0
# Vykreslení Ohně draka
obrazek_ohne_draka = pygame.image.load("./ohen_draka.png").convert_alpha()
ohen_zmenseny = pygame.transform.scale_by(obrazek_ohne_draka, 0.4)
nova_sirka = int(ohen_zmenseny.get_width() * 4)
nova_vyska = ohen_zmenseny.get_height()
ohen_draka = pygame.transform.scale(ohen_zmenseny, (nova_sirka, nova_vyska))
ohen_draka_rect = ohen_draka.get_rect(center=(rozliseni_okna[0] // 2, 518))
# Vykreslení startovního luku
obrazek_startovniho_luku =pygame.image.load("./startovni_luk.png").convert_alpha()
startovni_luk = pygame.transform.scale_by(obrazek_startovniho_luku, 0.4)
startovni_luk_rect = startovni_luk.get_rect()
startovni_luk_up = pygame.transform.rotate(startovni_luk, 90)
aktualni_luk = startovni_luk
aktualni_luk_up = startovni_luk_up
sip_aktualni = sip
# Vykreslení draka
obrazek_draka = pygame.image.load("./cely_drak.png").convert_alpha()
drak = pygame.transform.scale_by(obrazek_draka, 0.7)
drak_rect = drak.get_rect(center=(rozliseni_okna[0] - 180 , 360))
# Útok draka
drak_start_pozice = drak_rect.topleft
interval_utoku = 2000 
posledni_utok = pygame.time.get_ticks()
drak_utoci = False
drak_smer = -1
drak_rychlost = 12
drak_max_vzdalenost = 250
drak_urazena_vzdalenost = 0
drak_dal_damage = False
drak_ohnovy_utok = False
drak_ohnovy_start = 0
drak_ohnovy_interval = 5000 
drak_ohnovy_posledni = pygame.time.get_ticks()
drak_ohnovy_posledni_zraneni = 0
zabity_drak = 0
boss_odemcen = False
pocet_zivotu_draka = 250
# Uložení
ulozeno = False
def uloz_hru(slot):
    data = {
        "penize": penize,
        "zivoty": pocet_zivotu,
        "inventare": inventare,
        "mesto_odemcene": mesto_odemcene,
        "boss_odemcen": boss_odemcen,
        "quest_index": aktualni_quest_index,

        "koupeno_luk": koupeno_luk,
        "koupeno_helma": koupeno_helma,
        "koupeno_brneni": koupeno_brneni,
        "koupeno_heal_potion": koupeno_heal_potion,
        "koupeno_fire_resistance_potion": koupeno_fire_resistance_potion,
        "koupeno_coin_potion": koupeno_coin_potion
    }
    with open(f"save_{slot}.json", "w") as soubor:
        json.dump(data, soubor)
# Reset hry
def reset_slot(slot):
    global penize, pocet_zivotu, inventare
    global mesto_odemcene, boss_odemcen, aktualni_quest_index
    global mesto_uhaseno, koupeno_luk, koupeno_helma, koupeno_brneni
    global koupeno_heal_potion, koupeno_fire_resistance_potion, koupeno_coin_potion
    global fire_resistance_active, coin_bonus, aktualni_luk, aktualni_luk_up, rychlost_strely
    
    # Výchozí stav hry
    default_data = {
        "penize": 0,
        "zivoty": 100,
        "inventare": [],
        "mesto_odemcene": False,
        "boss_odemcen": False,
        "quest_index": 0,
        "koupeno_luk": False,
        "koupeno_helma": False,
        "koupeno_brneni": False,
        "koupeno_heal_potion": False,
        "koupeno_fire_resistance_potion": False,
        "koupeno_coin_potion": False
    }
    with open(f"save_{slot}.json", "w") as soubor:
        json.dump(default_data, soubor)

    if vybrany_slot == slot:
        penize = 0
        pocet_zivotu = 100
        inventare = []
        mesto_odemcene = False
        boss_odemcen = False
        aktualni_quest_index = 0
        mesto_uhaseno = False
        koupeno_luk = False
        koupeno_helma = False
        koupeno_brneni = False
        koupeno_heal_potion = False
        koupeno_fire_resistance_potion = False
        koupeno_coin_potion = False
        fire_resistance_active = False
        coin_bonus = 0
        aktualni_luk = startovni_luk
        aktualni_luk_up = startovni_luk_up
        rychlost_strely = 10

        for o in ohne:
            o["faktor"] = 1.0

        for q in questy:
            q.postup = 0
            q.splneno = False

    print(f"Slot {slot} byl restartován na výchozí stav")
    
# Načtení hry
def nacti_hru(slot):
    global aktualni_luk, aktualni_luk_up, rychlost_strely
    global penize, pocet_zivotu, inventare
    global mesto_odemcene, boss_odemcen, aktualni_quest_index
    global koupeno_luk, koupeno_helma, koupeno_brneni
    global koupeno_heal_potion, koupeno_fire_resistance_potion, koupeno_coin_potion

    try:
        with open(f"save_{slot}.json", "r") as soubor:
            data = json.load(soubor)

        penize = data["penize"]
        pocet_zivotu = data["zivoty"]
        inventare = data["inventare"]
        mesto_odemcene = data["mesto_odemcene"]
        boss_odemcen = data["boss_odemcen"]
        aktualni_quest_index = data["quest_index"]
        
        koupeno_luk = data.get("koupeno_luk", False)
        koupeno_helma = data.get("koupeno_helma", False)
        koupeno_brneni = data.get("koupeno_brneni", False)
        koupeno_heal_potion = data.get("koupeno_heal_potion", False)
        koupeno_fire_resistance_potion = data.get("koupeno_fire_resistance_potion", False)
        koupeno_coin_potion = data.get("koupeno_coin_potion", False)
        
        # RESET QUESTŮ
        for q in questy:
            q.postup = 0
            q.splneno = False
            
        koupeno_coin_potion = data.get("koupeno_coin_potion", False)

        # nastavení vybavení po načtení
        if koupeno_luk:
            aktualni_luk = luk_hrac
            aktualni_luk_up = luk_hrac_up
            rychlost_strely = 18

    except FileNotFoundError:
        print("Save neexistuje")
# Restart po smrti
restart_pozice_x = ctverecek_x
restart_pozice_y = ctverecek_y
restart_mapa = 1
tlacitko_zkusit_znovu = pygame.Rect(0, 0, 180, 55)
tlacitko_zkusit_znovu.center = (rozliseni_okna[0] // 2, rozliseni_okna[1] // 2 + 80)
# --------------- Vykreslení věcí do obchodu ---------------
# Luk
obrazek_luk_obchod = pygame.image.load("./luk_obchod.png").convert_alpha()
luk_obchod = pygame.transform.scale_by(obrazek_luk_obchod, 0.3)
luk_obchod_rect = luk_obchod.get_rect()
luk_hrac = pygame.transform.scale_by(obrazek_luk_obchod, 0.3)
luk_hrac_up = pygame.transform.rotate(luk_hrac, 90)
# Armor
obrazek_helmy_obchod = pygame.image.load("./helma_obchod.png").convert_alpha()
helma_obchod = pygame.transform.scale_by(obrazek_helmy_obchod, 0.5)
helma_obchod_rect = helma_obchod.get_rect()

obrazek_brneni_obchod = pygame.image.load("./brneni_obchod.png").convert_alpha()
brneni_obchod = pygame.transform.scale_by(obrazek_brneni_obchod, 0.5)
brneni_obchod_rect = brneni_obchod.get_rect()
# Potions
obrazek_heal_potion = pygame.image.load("./health_potion.png").convert_alpha()
heal_potion = pygame.transform.scale_by(obrazek_heal_potion, 0.4)
heal_potion_rect = heal_potion.get_rect()

obrazek_fire_resistance_potion = pygame.image.load("./fire_resistance_potion.png").convert_alpha()
fire_resistance_potion = pygame.transform.scale_by(obrazek_fire_resistance_potion, 0.4)
fire_resistance_potion_rect = fire_resistance_potion.get_rect()

obrazek_coin_potion = pygame.image.load("./coin_potion.png").convert_alpha()
coin_potion = pygame.transform.scale_by(obrazek_coin_potion, 0.4)
coin_potion_rect = coin_potion.get_rect()
# Efekty potionů
fire_resistance_active = False
heal_amount = 25
coin_bonus = 0
# Prazdny slot
prazdny_slot = pygame.image.load("./nedostatek_penez.png").convert_alpha()
nedostatek_penez = pygame.transform.scale_by(prazdny_slot, 0.4)
nedostatek_penez_rect = nedostatek_penez.get_rect()
# Plný slot
plny_slot = pygame.image.load("./dostatek_penez.png").convert_alpha()
dostatek_penez = pygame.transform.scale_by(plny_slot, 0.4)
dostatek_penez_rect = dostatek_penez.get_rect()
# Sloty
sloty_obchod = []
sloty_inventory = []
sloty_save = []
# Pocty slotu pro obchod
pocty_slotu = 6
pocet_sloupcu = 3
pocet_radku = 2
mezera = 30
velikost_slotu = nedostatek_penez.get_width()
start_x = (rozliseni_okna[0] - (pocet_sloupcu * velikost_slotu + (pocet_sloupcu - 1) * mezera)) // 2
start_y = 100
sloty_save = [tlacitko_1.copy(), tlacitko_2.copy(), tlacitko_3.copy()]
for radek in range(pocet_radku):
    for sloupec in range(pocet_sloupcu):
        x = start_x + sloupec * (velikost_slotu + mezera)
        y = start_y + radek * (velikost_slotu + mezera)
        rect = nedostatek_penez.get_rect(topleft=(x, y))
        sloty_obchod.append(rect.copy())
        sloty_inventory.append(rect.copy())
# ----------- Vykreslení věcí pro městečko -----------
# Vykreslení Kbelíku
kbelik_s_vodou = pygame.image.load("./kbelik_s_vodou.png").convert_alpha()
kbelik = pygame.transform.scale_by(kbelik_s_vodou, 0.4)
kbelik_rect = kbelik.get_rect()
kbelik_pozice = [
    (rozliseni_okna[0] // 1.8, 110),
    (rozliseni_okna[0] // 6.5, 70),
    (rozliseni_okna[0] // 2.67, 240),
    (rozliseni_okna[0] // 1.35, 60),
    (rozliseni_okna[0] // 1.078, 180),
]
def presun_kbelik():
    pozice = random.choice(kbelik_pozice)
    kbelik_rect.center = pozice

kbelik_rect = kbelik.get_rect()
presun_kbelik()

# Seznam ohňů
pocty_ohnu = 10
ohne = []
for i in range(pocty_ohnu):
    x = random.randint(50, rozliseni_okna[0] - 50)
    y = random.randint(200, rozliseni_okna[1] - 50)
    rect = ohen.get_rect(center=(x, y))
    faktor = 1.0
    rust = random.uniform(0.0002, 0.0008) 
    cas_sireni = pygame.time.get_ticks() + random.randint(5000, 15000)  
    ohne.append({"rect": rect, "faktor": faktor, "rust": rust, "cas_sireni": cas_sireni})  
# -------------------- Komandy které stále běží --------------------
while True:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if konec_hry or vyhra:
            if udalost.type == pygame.KEYDOWN:
                if udalost.key == pygame.K_r:
                    pass 
            continue 
        if udalost.type == pygame.KEYDOWN:    
            if udalost.key == pygame.K_e and not strela_leti:
                strela_leti = True
                if aktualni_mapa == 1:
                    sip_rect = sip.get_rect()
                    sip_rect.midleft = archer.midright
                    sip_smer_x = 1
                    sip_smer_y = 0
                    sip_aktualni = sip 
                if aktualni_mapa == 2:
                    sip_aktualni = pygame.transform.rotate(sip, 90)  
                    sip_rect = sip_aktualni.get_rect()
                    sip_rect.midbottom = archer.midtop  
                    sip_smer_x = 0
                    sip_smer_y = -1
                if aktualni_mapa == 5:
                    uhel_stupne = 30
                    uhel = math.radians(uhel_stupne)
                    sip_aktualni = pygame.transform.rotate(sip, uhel_stupne)
                    sip_smer_x = math.cos(uhel)
                    sip_smer_y = -math.sin(uhel)
                    vzdalenost_od_hrace = 40
                    start_x = archer.centerx + math.cos(uhel) * vzdalenost_od_hrace
                    start_y = archer.centery - math.sin(uhel) * vzdalenost_od_hrace
                    sip_rect = sip_aktualni.get_rect(center=(start_x, start_y))
        # Tlačítka - shrnutí
        if udalost.type == pygame.MOUSEBUTTONDOWN:
            # Tlačítko zpět
            if tlacitko_zpet.collidepoint(udalost.pos):
                if aktualni_mapa in [2, 5]: 
                    aktualni_mapa = 1  
                    archer.topleft = (50, 535)
                elif aktualni_mapa in [3, 4]:
                    aktualni_mapa = 1
                    archer.topleft = start_pozice_hrace
                elif aktualni_mapa == 6:  
                    aktualni_mapa = 0
                elif aktualni_mapa == 1:
                    aktualni_mapa = 0
                    archer.topleft = start_pozice_hrace
            # Tlačítko pro hlavní menu
            elif aktualni_mapa == 0:
                if tlacitko_s.collidepoint(udalost.pos):
                    aktualni_mapa = 1

                elif tlacitko_u.collidepoint(udalost.pos):
                    aktualni_mapa = 6

                elif tlacitko_od.collidepoint(udalost.pos):
                    pygame.quit()
                    sys.exit()
            # Tlačítka pro sloty na uložení a restarovat
            elif aktualni_mapa == 6:
                for i, slot in enumerate(sloty_save):
                    if udalost.button == 3 and slot.collidepoint(udalost.pos):
                        vybrany_slot = i + 1
                        zobrazit_slot_menu = True
                    if udalost.button == 1 and slot.collidepoint(udalost.pos):
                        nacti_hru(i + 1)
                        aktualni_mapa = 0
                        
                if zobrazit_slot_menu:
                    if tlacitko_ulozit.collidepoint(udalost.pos):
                        uloz_hru(vybrany_slot)
                        zobrazit_slot_menu = False
                    if tlacitko_restart.collidepoint(udalost.pos):
                        reset_slot(vybrany_slot)
                        zobrazit_slot_menu = False
                        
            # --------- Tlačítka map hry ---------
            elif aktualni_mapa not in [0,6]:

                # Město
                if mesto_odemcene and tlacitko_m.collidepoint(udalost.pos):
                    if aktualni_mapa == 1:
                        aktualni_mapa = 2
                        archer.topleft = (50, 535)

                # Obchod
                elif tlacitko_ob.collidepoint(udalost.pos):
                    if aktualni_mapa == 1:
                        aktualni_mapa = 3

                # Inventář
                elif tlacitko_i.collidepoint(udalost.pos):
                    if aktualni_mapa == 1:
                        aktualni_mapa = 4

                # Boss
                elif tlacitko_b.collidepoint(udalost.pos) and boss_odemcen:
                    if aktualni_mapa == 1:
                        restart_pozice_x = archer.x 
                        restart_pozice_y = archer.y 
                        restart_mapa = 1 
                        aktualni_mapa = 5
                        archer.topleft = (50, 515)
                        posledni_utok = pygame.time.get_ticks()
                        drak_ohnovy_posledni = pygame.time.get_ticks()
                        drak_ohnovy_posledni_zraneni = pygame.time.get_ticks()
                    else:
                        aktualni_mapa = 1
                        archer.topleft = start_pozice_hrace
                    
            if aktualni_mapa == 3:
                # Luk
                if sloty_obchod[0].collidepoint(udalost.pos) and not koupeno_luk:
                    if penize >= cena_luk:
                        penize -= cena_luk
                        koupeno_luk = True
                        rychlost_strely = 18
                        
                        aktualni_luk = luk_hrac
                        aktualni_luk_up = luk_hrac_up
                        
                        inventare.append("luk")
                # Helma
                if sloty_obchod[1].collidepoint(udalost.pos) and not koupeno_helma:
                    if penize >= cena_helma:
                        penize -= cena_helma
                        koupeno_helma = True
                        pocet_zivotu += 25
                        
                        inventare.append("helma_obchod")
                # Brnění
                if sloty_obchod[2].collidepoint(udalost.pos) and not koupeno_brneni:
                    if penize >= cena_brneni:
                        penize -= cena_brneni
                        koupeno_brneni = True
                        pocet_zivotu += 50
                        
                        inventare.append("brneni_obchod")
                # Heal potion
                if sloty_obchod[3].collidepoint(udalost.pos) and not koupeno_heal_potion:
                    if penize >= cena_heal_potion:
                        penize -= cena_heal_potion
                        koupeno_heal_potion = True
                        pocet_zivotu += heal_amount
                        
                        inventare.append("heal_potion")

                # Fire resistance potion
                if sloty_obchod[4].collidepoint(udalost.pos) and not koupeno_fire_resistance_potion:
                    if penize >= cena_fire_resistance_potion:
                        penize -= cena_fire_resistance_potion
                        koupeno_fire_resistance_potion = True
                        fire_resistance_active = True
                        
                        inventare.append("fire_resistance_potion")

                # Coin potion
                if sloty_obchod[5].collidepoint(udalost.pos) and not koupeno_coin_potion:
                    if penize >= cena_coin_potion:
                        penize -= cena_coin_potion
                        koupeno_coin_potion = True
                        coin_bonus = 5
                        
                        inventare.append("coin_potion")
                        
    # Stisknuté klávesy
    klavesy = pygame.key.get_pressed()

    # Kontrola prekroceni spodniho okraje okna
    if ctverecek_y > rozliseni_okna[1] - velikost_ctverecku:
        ctverecek_y = rozliseni_okna[1] - velikost_ctverecku
        posun_ctverecku = -posun_ctverecku

    # Kontrola prekroceni horniho okraje okna
    if ctverecek_y < 0:
        ctverecek_y = 0
        posun_ctverecku = -posun_ctverecku
        
    # Omezení hráče na hranice obrazovky
    archer.x = max(0, min(archer.x, rozliseni_okna[0] - velikost_ctverecku))
    archer.y = max(0, min(archer.y, rozliseni_okna[1] - velikost_ctverecku))
    
    # Posun strely
    if strela_leti:
        sip_rect.x += sip_smer_x * rychlost_strely
        sip_rect.y += sip_smer_y * rychlost_strely
        if (sip_rect.left > rozliseni_okna[0] or sip_rect.right < 0 or sip_rect.top > rozliseni_okna[1] or sip_rect.bottom < 0):
            strela_leti = False
        if aktualni_mapa == 5:
            hitbox_draka_x = 60
            hitbox_draka_y = 100
            drak_hitbox = pygame.Rect(
                drak_rect.left + hitbox_draka_x,
                drak_rect.top + hitbox_draka_y,
                drak_rect.width - 2 * hitbox_draka_x,
                drak_rect.height - 2 * hitbox_draka_y
            )

            # Životy draka
            if aktualni_mapa == 5:
                if sip_rect.colliderect(drak_hitbox):
                    pocet_zivotu_draka -= 2
                    strela_leti = False
                    pocet_zivotu_draka = max(pocet_zivotu_draka, 0)

                    if pocet_zivotu_draka <= 0 and zabity_drak == 0:
                        zabity_drak = 1
                        questy[3].pridej_postup(1)
        # Vyliti vody
        if aktualni_mapa == 2 and strela_leti and sip_rect.colliderect(kbelik_rect):
            voda_aktivni = True
            vylity_kbelik_rect.center = kbelik_rect.center
            voda_rect.midtop = kbelik_rect.midtop
            voda_rect.y += 40
            cas_vody = pygame.time.get_ticks()
            strela_leti = False
            
        if aktualni_mapa == 3:
            strela_leti = False
        if aktualni_mapa == 4:
            strela_leti = False
    # ------ Questy ------
    if aktualni_mapa == 1:
        terc_rect = pygame.Rect(terc_x, terc_y, sirka_terce, sirka_terce)
        if strela_leti and sip_rect.colliderect(terc_rect):
            odmena_za_zasah = 10 + coin_bonus if koupeno_coin_potion else 10
            penize += odmena_za_zasah
            
            # Kontrola 1. Questu (Střelec)
            if aktualni_quest_index == 0:
                if questy[0].pridej_postup():
                    penize += questy[0].odmena
                    mesto_odemcene = True  
                    aktualni_quest_index += 1
            
            strela_leti = False
            terc_x, terc_y = nahodna_pozice_terce()
                
    # Kontrola 2. Questu (Hasič)
    if aktualni_quest_index == 1:  
        if all(o["faktor"] <= 0 for o in ohne) and not questy[1].splneno:
            if questy[1].pridej_postup():
                penize += questy[1].odmena
                aktualni_quest_index = 2
                mesto_uhaseno = True
                    
    # Kontrola 3. Questu (Boháč) 
    if aktualni_quest_index == 2:  
        questy[2].postup = penize  # aktualizuj postup
        if questy[2].postup >= questy[2].cil and not questy[2].splneno:
            questy[2].splneno = True
            boss_odemcen = True
            aktualni_quest_index = 3
            
    # Kontrola 4. Questu (Boss)
    if questy[3].postup >= questy[3].cil and not questy[3].splneno:
        questy[3].splneno = True
        vyhra = True 
        if aktualni_quest_index == 3:
            aktualni_quest_index = 4
            
    # Čas terče
    aktualni_cas = pygame.time.get_ticks()
    uplynulo = aktualni_cas - terc_spawn_cas

    faktor = 1.0
    if uplynulo > terc_ceka:
        faktor = 1 - (uplynulo - terc_ceka) / terc_vyparovani
        faktor = max(faktor, 0)
        if faktor == 0:
            terc_x, terc_y = nahodna_pozice_terce()
    # Pocet Zivotu
    if pocet_zivotu <= 0:
        pocet_zivotu = 0
        konec_hry = True
    # Posun v mapách
    # 1. Mapa
    if aktualni_mapa == 1:
        if klavesy[pygame.K_w]:
            archer.y -= posun_ctverecku
        if klavesy[pygame.K_s]:
            archer.y += posun_ctverecku
    # 2. Mapa 
    if aktualni_mapa == 2:
        if klavesy[pygame.K_a]:
            archer.x -= posun_ctverecku
        if klavesy[pygame.K_d]:
            archer.x += posun_ctverecku
    # 5. Mapa
    if aktualni_mapa == 5:
        if klavesy[pygame.K_a]:
            archer.x -= posun_ctverecku
        if klavesy[pygame.K_d]:
            archer.x += posun_ctverecku
    # Drakovi utoky       
        if aktualni_mapa == 5 and not konec_hry and pocet_zivotu_draka > 0:
            aktualni_cas = pygame.time.get_ticks()
            if not drak_utoci and not drak_ohnovy_utok:
                if aktualni_cas - posledni_utok > interval_utoku:
                    volba_utoku = random.randint(1, 2)
                    
                    # 1. Rush útok 
                    if volba_utoku == 1:
                        drak_utoci = True
                        drak_smer = -1
                        drak_urazena_vzdalenost = 0
                        drak_dal_damage = False
                        print("Drak startuje RUSH!")
                        
                    # 2. Ohnivý útok 
                    elif volba_utoku == 2: 
                        drak_ohnovy_utok = True
                        drak_ohnovy_start = aktualni_cas
                        drak_ohnovy_posledni_zraneni = aktualni_cas
                        print("Drak startuje OHEN!")

            # --- Pohyb při Rush útoku ---
            if drak_utoci:
                drak_rect.x += drak_smer * drak_rychlost
                drak_urazena_vzdalenost += drak_rychlost         
                if drak_rect.colliderect(archer) and drak_smer == -1 and not drak_dal_damage:
                    damage = 10
                    pocet_zivotu -= damage
                    drak_dal_damage = True
                    
                if drak_urazena_vzdalenost >= drak_max_vzdalenost:
                    if drak_smer == -1:
                        drak_smer = 1
                        drak_urazena_vzdalenost = 0
                    else:
                        drak_utoci = False
                        drak_rect.topleft = drak_start_pozice
                        posledni_utok = pygame.time.get_ticks()

            # --- Logika Ohnivého útoku ---
            if drak_ohnovy_utok:
                ohen_draka_rect.centerx = rozliseni_okna[0] // 2
                ohen_draka_rect.bottom = rozliseni_okna[1] - 20 
                if ohen_draka_rect.colliderect(archer):
                    if aktualni_cas - drak_ohnovy_posledni_zraneni >= 100:
                        damage_z_ohne = 1
                        if fire_resistance_active:
                            damage_z_ohne = 0  
                        pocet_zivotu -= damage_z_ohne
                        pocet_zivotu = max(pocet_zivotu, 0)
                        drak_ohnovy_posledni_zraneni = aktualni_cas

                if aktualni_cas - drak_ohnovy_start > 2000: 
                    drak_ohnovy_utok = False
                    posledni_utok = aktualni_cas
                    print("Drak dokončil OHEN!")
    # --------- Vykreslení v mapách ---------
    if not konec_hry:
        # 0. Mapa
        if aktualni_mapa == 0:
            okno.blit(menu, menu_rect)
            # Název hry
            nazev_text = font_nazev.render("SHADOW ARCHER", True, (0, 0, 0))
            nazev_rect = nazev_text.get_rect(center=(rozliseni_okna[0] // 2, 120))
            okno.blit(nazev_text, nazev_rect)
        # 1. Mapa
        if aktualni_mapa == 1:
            okno.blit(trenink, trenink_rect)
        # 2. Mapa
        if aktualni_mapa == 2:
            okno.blit(horici_mesto, horici_mesto_rect)
            # Vykreslení ohňů
            for o in ohne:
                if o["faktor"] > 0:
                    velikost = int(100 * o["faktor"])
                    if velikost > 0:
                        ohen_zmenseny = pygame.transform.scale(ohen, (velikost, velikost))
                        rect = ohen_zmenseny.get_rect(center=o["rect"].center)
                        okno.blit(ohen_zmenseny, rect)
                        # Rozšiřování ohně
                        if o["faktor"] < 2.5 and not mesto_uhaseno:
                            o["faktor"] += o["rust"]
            # Šíření ohně na nová místa
            if not mesto_uhaseno:
                aktualni_cas_ohne = pygame.time.get_ticks()
                nove_ohne = []
                for o in ohne:
                    if o["faktor"] > 0 and aktualni_cas_ohne >= o["cas_sireni"]:
                        o["cas_sireni"] = aktualni_cas_ohne + random.randint(8000, 20000)
                        offset_x = random.randint(-120, 120)
                        offset_y = random.randint(-120, 120)
                        nx = max(50, min(rozliseni_okna[0] - 50, o["rect"].centerx + offset_x))
                        ny = max(200, min(rozliseni_okna[1] - 50, o["rect"].centery + offset_y))
                        novy_rect = ohen.get_rect(center=(nx, ny))
                        nove_ohne.append({
                            "rect": novy_rect,
                            "faktor": 0.3,
                            "rust": random.uniform(0.0002, 0.0008),
                            "cas_sireni": aktualni_cas_ohne + random.randint(8000, 20000)
                        })
                ohne.extend(nove_ohne)
            # Kbelík Vylitý a plný
            if voda_aktivni:
                okno.blit(vylity_kbelik, vylity_kbelik_rect)
            else:
                okno.blit(kbelik, kbelik_rect)

            # Efekt vody
            if voda_aktivni:
                voda_rect2 = voda_rect.copy()
                voda_rect2.y += voda_kbeliku.get_height()
                voda_rect3 = voda_rect.copy()
                voda_rect3.y += voda_kbeliku.get_height() * 2

                # Hašení ohňů
                for o in ohne:
                    if (o["rect"].colliderect(voda_rect) or
                        o["rect"].colliderect(voda_rect2) or
                        o["rect"].colliderect(voda_rect3)):
                        o["faktor"] -= 0.05
                        o["faktor"] = max(o["faktor"], 0)

                # Vykreslení vody
                okno.blit(voda_kbeliku, voda_rect)
                okno.blit(voda_kbeliku, voda_rect2)
                okno.blit(voda_kbeliku, voda_rect3)
                okno.blit(vylity_kbelik, vylity_kbelik_rect)

                # Kontrola času vody
                if pygame.time.get_ticks() - cas_vody > 1000:
                    voda_aktivni = False
                    presun_kbelik()
        # 3. Mapa
        if aktualni_mapa == 3:
            okno.blit(obchod, obchod_rect)
            # Sloty
            for i, slot in enumerate(sloty_obchod):
                if i == 0 and koupeno_luk:
                    okno.blit(dostatek_penez, slot)
                elif i == 1 and koupeno_helma:
                    okno.blit(dostatek_penez, slot)
                elif i == 2 and koupeno_brneni:
                    okno.blit(dostatek_penez, slot)
                elif i == 3 and koupeno_heal_potion:
                    okno.blit(dostatek_penez, slot)
                elif i == 4 and koupeno_fire_resistance_potion:
                    okno.blit(dostatek_penez, slot)
                elif i == 5 and koupeno_coin_potion:
                    okno.blit(dostatek_penez, slot)
                else:
                    okno.blit(nedostatek_penez, slot)
            
            # ----- Itemy -----
            
            # Luk do prvního slotu
            luk_obchod_rect.center = sloty_obchod[0].center
            okno.blit(luk_obchod, luk_obchod_rect)
            # Helma do druhého slotu
            helma_obchod_rect.center = sloty_obchod[1].center
            okno.blit(helma_obchod, helma_obchod_rect)
            # Brnění do třetího slotu
            brneni_obchod_rect.center = sloty_obchod[2].center
            okno.blit(brneni_obchod, brneni_obchod_rect)
            # Heal potion
            heal_potion_rect.center = sloty_obchod[3].center
            okno.blit(heal_potion,heal_potion_rect)
            # Fire resistance potion
            fire_resistance_potion_rect.center = sloty_obchod[4].center
            okno.blit(fire_resistance_potion, fire_resistance_potion_rect)
            # Coin potion
            coin_potion_rect.center = sloty_obchod[5].center
            okno.blit(coin_potion, coin_potion_rect)
            # ----- CENY POD SLOTY -----
            ceny = [
                cena_luk,
                cena_helma,
                cena_brneni,
                cena_heal_potion,
                cena_fire_resistance_potion,
                cena_coin_potion
            ]

            for i, slot in enumerate(sloty_obchod):
                cena_text = font.render(str(ceny[i]) + "$", True, (0, 0, 0))
                cena_rect = cena_text.get_rect(midtop=(slot.centerx, slot.bottom + 5))
                okno.blit(cena_text, cena_rect)
        # 4. Mapa
        if aktualni_mapa == 4:
            okno.blit(inventar, inventar_rect)
            for i, item in enumerate(inventare):
                if i < len(sloty_inventory):
                    okno.blit(dostatek_penez, sloty_inventory[i])
                    
                    if item == "luk":
                        luk_obchod_rect.center = sloty_inventory[i].center
                        okno.blit(luk_obchod, luk_obchod_rect)

                    elif  item == "helma_obchod":
                        helma_obchod_rect.center = sloty_inventory[i].center
                        okno.blit(helma_obchod, helma_obchod_rect)   
     
                    elif item == "brneni_obchod":
                        brneni_obchod_rect.center = sloty_inventory[i].center
                        okno.blit(brneni_obchod, brneni_obchod_rect)

                    elif item == "heal_potion":
                        heal_potion_rect.center = sloty_inventory[i].center
                        okno.blit(heal_potion, heal_potion_rect)

                    elif item == "fire_resistance_potion":
                        fire_resistance_potion_rect.center = sloty_inventory[i].center
                        okno.blit(fire_resistance_potion, fire_resistance_potion_rect)

                    elif item == "coin_potion":
                        coin_potion_rect.center = sloty_inventory[i].center
                        okno.blit(coin_potion, coin_potion_rect)
        # 5. Mapa - Vykreslení
        if aktualni_mapa == 5:
            okno.blit(jeskyne, jeskyne_rect)
            if pocet_zivotu_draka > 0:
                okno.blit(drak, drak_rect)
                if drak_ohnovy_utok:
                    okno.blit(ohen_draka, ohen_draka_rect)
            else:
                vyhra_text = font.render("DRAK JE MRTVÝ!", True, (255, 215, 0))
                text_rect = vyhra_text.get_rect(center=(rozliseni_okna[0] // 2, rozliseni_okna[1] // 2))
                okno.blit(vyhra_text, text_rect)
        # 6. Mapa - Uložení hry
        if aktualni_mapa == 6:
            okno.blit(jeskyne, jeskyne_rect)
            # Instrukce nahoře 
            instrukce_text = font_vybrat_slot.render("Levým tlačítkem vybereš slot a Pravým tlačítkem uložíš / restartuješ hru", True, (0,0,0))
            instrukce_rect = instrukce_text.get_rect(center=(rozliseni_okna[0] // 2, 50))
            okno.blit(instrukce_text, instrukce_rect)

            pygame.draw.rect(okno, (200,200,200), tlacitko_1)
            pygame.draw.rect(okno, (200,200,200), tlacitko_2)
            pygame.draw.rect(okno, (200,200,200), tlacitko_3)

            text1 = font_tlacitka.render("Slot 1", True, (0,0,0))
            text2 = font_tlacitka.render("Slot 2", True, (0,0,0))
            text3 = font_tlacitka.render("Slot 3", True, (0,0,0))

            okno.blit(text1, text1.get_rect(center=tlacitko_1.center))
            okno.blit(text2, text2.get_rect(center=tlacitko_2.center))
            okno.blit(text3, text3.get_rect(center=tlacitko_3.center))
            
        if aktualni_mapa == 6 and zobrazit_slot_menu:

            pygame.draw.rect(okno,(200,200,200), tlacitko_ulozit)
            pygame.draw.rect(okno,(200,200,200), tlacitko_restart)

            text = font_tlacitka.render("Uložit", True,(0,0,0))
            okno.blit(text, text.get_rect(center=tlacitko_ulozit.center))

            text = font_tlacitka.render("Restart", True,(0,0,0))
            okno.blit(text, text.get_rect(center=tlacitko_restart.center))
        # Vykreslení kruhů pro terč
        if aktualni_mapa == 1 and faktor > 0:
            v1 = int(sirka_terce * faktor)
            v2 = int(sirka_terce_2 * faktor)
            v3 = int(sirka_terce_3 * faktor)

            o1 = (sirka_terce - v1) // 2
            o2 = (sirka_terce - v2) // 2
            o3 = (sirka_terce - v3) // 2
            pygame.draw.ellipse(okno, (200, 0, 0), (terc_x + o1, terc_y + o1, v1, v1))
            pygame.draw.ellipse(okno, (255, 255, 255), (terc_x + o2, terc_y + o2, v2, v2))
            pygame.draw.ellipse(okno, (200, 0, 0), (terc_x + o3, terc_y + o3, v3, v3))
            
        # Vykreslení věcí na Hráčovi
        if aktualni_mapa == 1 or aktualni_mapa == 2 or aktualni_mapa == 5:
            pygame.draw.rect(okno, (50, 50, 50), archer)
            
            if koupeno_brneni:
                brneni_rect = brneni_obchod.get_rect(center=archer.center)
                okno.blit(brneni_obchod, brneni_rect)
            
            if koupeno_helma:
                helma_rect = helma_obchod.get_rect(midbottom=archer.midtop)
                okno.blit(helma_obchod, helma_rect)
                
            if aktualni_mapa == 1:
                luk_rect = aktualni_luk.get_rect(midleft=archer.midright)
                okno.blit(aktualni_luk, luk_rect)

            elif aktualni_mapa == 5:
                luk_30 = pygame.transform.rotate(aktualni_luk, 30)
                luk_rect = luk_30.get_rect(center=archer.center)
                luk_rect.x += 50  
                luk_rect.y -= 15

                okno.blit(luk_30, luk_rect)
            else:
                luk_rect = aktualni_luk_up.get_rect(midbottom=archer.midtop)
                okno.blit(aktualni_luk_up, luk_rect)
        # Tlačítko Zpět
        if aktualni_mapa != 0:
            # Zpět pro mapu 1 a 6
            if aktualni_mapa in [1, 6]:
                tlacitko_zpet.topleft = (5, rozliseni_okna[1] - 40)
                tlacitko_zpet.size = (80, 35)
                pygame.draw.rect(okno, (0, 0, 0), tlacitko_zpet)
                text = font_tlacitka.render("Zpět", True, (255, 255, 255))
                okno.blit(text, text.get_rect(center=tlacitko_zpet.center))
            # Zpět pro ostatní mapy 
            else:
                tlacitko_zpet.topleft = (10, 10)
                tlacitko_zpet.size = (120, 50)
                pygame.draw.rect(okno, (0, 0, 0), tlacitko_zpet)
                text = font_zpet.render("Zpět", True, (255, 255, 255))
                okno.blit(text, text.get_rect(center=tlacitko_zpet.center))
                
         # ----------- Vykreslení v Mapách -----------
        if aktualni_mapa != 0 and aktualni_mapa != 6:        
            # Vykreslení šipu
            if strela_leti:
                okno.blit(sip_aktualni, sip_rect)
            # Srdíčko
            okno.blit(srdicko, srdicko_rect)
            # Penize
            text = font.render(f"Peníze: {penize}", True, (0, 0, 200))
            text_rect = text.get_rect(midtop=(rozliseni_okna[0] // 2, 10))
            okno.blit(text, text_rect)
            # Životy
            text = font.render(f"Životy: {pocet_zivotu}", True, (0, 0, 200))
            text_rect = text.get_rect(center=(rozliseni_okna[0] // 2, 55))
            okno.blit(text, text_rect)
            # Životy draka
            if aktualni_mapa == 5:
                text = font.render(f"Životy draka: {pocet_zivotu_draka}", True, (0, 0, 200))
                text_rect = text.get_rect(center=(drak_rect.centerx, drak_rect.top - 20))
                okno.blit(text, text_rect)
            # Uhašené město
            if aktualni_mapa == 2 and mesto_uhaseno:
                text = font.render("Uhasil jsi město!", True, (0, 0, 200))
                rect = text.get_rect(center=(rozliseni_okna[0] // 2, rozliseni_okna[1] - 40))
                okno.blit(text, rect)
            #Vykreslení Questů
            if aktualni_quest_index < len(questy):
                    q = questy[aktualni_quest_index]
                    y_offset = 10
                    barva = (0, 200, 0) if q.splneno else (0, 0, 0)

                    nazev_text = font.render(f"{q.nazev}: {q.postup}/{q.cil}", True, barva)
                    okno.blit(nazev_text, (550, y_offset))

                    popis_font = pygame.font.SysFont(None, 28)
                    popis_text = popis_font.render(q.popis, True, (0, 0, 255))
                    okno.blit(popis_text, (550, y_offset + 35))
            else:
                vsechny_questy_font = pygame.font.SysFont(None, 28)
                vse_hotovo_text = vsechny_questy_font.render("Všechny questy splněny!", True, (0, 200, 0))
                okno.blit(vse_hotovo_text, (550, 10))
        if aktualni_mapa == 1:   
            # Vykreslení tlačítka pro město
            if mesto_odemcene:
                pygame.draw.rect(okno, (0, 0, 0), tlacitko_m)
                text = font_tlacitka.render("Městečko", True, (200, 0, 0))
                okno.blit(text, text.get_rect(center=tlacitko_m.center))
            # Vykreslení tlačítka pro obchod
            pygame.draw.rect(okno, (0, 0, 0), tlacitko_ob)
            text = font_tlacitka.render("Obchod", True, (200, 0, 0))
            okno.blit(text, text.get_rect(center=tlacitko_ob.center))
            # Vykreslení tlačítka pro inventář
            pygame.draw.rect(okno, (0, 0, 0), tlacitko_i)
            text = font_tlacitka.render("Inventář", True, (200, 0, 0))
            okno.blit(text, text.get_rect(center=tlacitko_i.center))
            # Vykreslení tlačítka pro boss fight
            if boss_odemcen:
                pygame.draw.rect(okno, (0, 0, 0), tlacitko_b)
                text = font_tlacitka.render("Boss Fight!", True, (200, 0, 0))
                okno.blit(text, text.get_rect(center=tlacitko_b.center))
        if aktualni_mapa == 0:
            # Hlavní menu
            pygame.draw.rect(okno, (255,255,255), tlacitko_s)
            text = font_tlacitka.render("Start Hry", True, (200,0,0))
            okno.blit(text, text.get_rect(center=tlacitko_s.center))

            pygame.draw.rect(okno, (255,255,255), tlacitko_u)
            text = font_tlacitka.render("Uložení hry", True, (200,0,0))
            okno.blit(text, text.get_rect(center=tlacitko_u.center))
            
            pygame.draw.rect(okno, (255,255,255), tlacitko_od)
            text = font_tlacitka.render("Odejít", True, (200,0,0))
            okno.blit(text, text.get_rect(center=tlacitko_od.center))
    # Promítnutí změn na displeji
    pygame.display.update()
    # Konec a vyhra hry
    if konec_hry:
            okno.fill((0, 0, 0))
            text = font.render("KONEC HRY - ZEMŘEL JSI", True, (200, 0, 0))
            text_rect = text.get_rect(center=(rozliseni_okna[0] // 2, rozliseni_okna[1] // 2))
            okno.blit(text, text_rect)

            pygame.draw.rect(okno, (255, 255, 255), tlacitko_zkusit_znovu)
            text_btn = font_tlacitka.render("Zkusit znovu", True, (200, 0, 0))
            okno.blit(text_btn, text_btn.get_rect(center=tlacitko_zkusit_znovu.center))
            
            pygame.display.update()
            
            for udalost in pygame.event.get():
                if udalost.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if udalost.type == pygame.MOUSEBUTTONDOWN:
                    if tlacitko_zkusit_znovu.collidepoint(udalost.pos):
                        # Reset hry zpět před boss fight
                        konec_hry = False
                        pocet_zivotu = 100
                        pocet_zivotu_draka = 250
                        zabity_drak = 0
                        drak_utoci = False
                        drak_ohnovy_utok = False
                        drak_rect.topleft = drak_start_pozice
                        posledni_utok = pygame.time.get_ticks()
                        drak_ohnovy_posledni = pygame.time.get_ticks()
                        drak_ohnovy_posledni_zraneni = pygame.time.get_ticks()
                        strela_leti = False
                        aktualni_mapa = restart_mapa
                        archer.x = restart_pozice_x
                        archer.y = restart_pozice_y
                        
    # Omezení fps ve hře
    vsync.tick(FPS)