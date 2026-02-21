import sys
import pygame
import random
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
# Informace pro čtvereček
velikost_ctverecku = 50
ctverecek_x = (rozliseni_okna[0] - velikost_ctverecku) - 700
ctverecek_y = (rozliseni_okna[1] - velikost_ctverecku) //2
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
aktualni_mapa = 1
# Inventář
inventar = []
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
    Quest("Boháč", "Nasbírej 500 peněz", 500, 0)
]
aktualni_quest_index = 0
# Tlačítka
tlacitko_m = pygame.Rect(10, 60, 120, 50)
tlacitko_o = pygame.Rect(10, 5, 120, 50)
tlacitko_i = pygame.Rect(136, 5, 120, 50)
# Barva inventáře
barva_inventare = (145, 96, 68)
# Počet srdíček
pocet_zivotu = 100
#Informace pro střelu (Šíp)
strela_leti = False 
rychlost_strely = 10
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
# False hry
konec_hry = False
mesto_uhaseno = False
# Ceny itemů
cena_luk = 50
cena_helma = 80
cena_brneni = 120
cena_heal_potion = 100
cena_fire_resistance_potion = 100
cena_coin_potion = 120
koupeno_x = True
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
#Pozadí 3. Mapy
obrazek_obchodu = pygame.image.load("./obchod_pozadí.png").convert_alpha()
obchod = pygame.transform.scale(obrazek_obchodu, rozliseni_okna)
obchod_rect = obchod.get_rect(topleft=(0, 0))
#Vykreslení Ohně
obrazek_ohne = pygame.image.load("./ohen.png").convert_alpha()
ohen = pygame.transform.scale_by(obrazek_ohne, 0.35)
ohen_rect = ohen.get_rect(center=(rozliseni_okna[0] // 2, 25))
#Vykreslení startovního luku
obrazek_startovniho_luku =pygame.image.load("./startovni_luk.png").convert_alpha()
startovni_luk = pygame.transform.scale_by(obrazek_startovniho_luku, 0.4)
startovni_luk_rect = startovni_luk.get_rect()
startovni_luk_up = pygame.transform.rotate(startovni_luk, 90)
aktualni_luk = startovni_luk
aktualni_luk_up = startovni_luk_up

# Vykreslení věcí do obchodu

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

# Prazdny slot
prazdny_slot = pygame.image.load("./nedostatek_penez.png").convert_alpha()
nedostatek_penez = pygame.transform.scale_by(prazdny_slot, 0.4)
nedostatek_penez_rect = nedostatek_penez.get_rect()
# Plný slot
plny_slot = pygame.image.load("./dostatek_penez.png").convert_alpha()
dostatek_penez = pygame.transform.scale_by(plny_slot, 0.4)
dostatek_penez_rect = dostatek_penez.get_rect()

pocty_slotu = 6
sloty = []
pocet_sloupcu = 3
pocet_radku = 2
mezera = 30

velikost_slotu = nedostatek_penez.get_width()
start_x = (rozliseni_okna[0] - (pocet_sloupcu * velikost_slotu + (pocet_sloupcu - 1) * mezera)) // 2
start_y = 100

for radek in range(pocet_radku):
    for sloupec in range(pocet_sloupcu):
        x = start_x + sloupec * (velikost_slotu + mezera)
        y = start_y + radek * (velikost_slotu + mezera)
        rect = nedostatek_penez.get_rect(topleft=(x, y))
        sloty.append(rect)

# Seznam ohňů
pocty_ohnu = 10
ohne = []
for i in range(pocty_ohnu):
    x = random.randint(50, rozliseni_okna[0] - 50)
    y = random.randint(50, rozliseni_okna[1] - 50)
    rect = ohen.get_rect(center=(x, y))
    faktor = 1.0
    ohne.append({"rect": rect, "faktor": faktor})
# -------------------- Komandy které stále běží --------------------
while True:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
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
        # Tlačítka - shrnutí
        if udalost.type == pygame.MOUSEBUTTONDOWN:
            if mesto_odemcene and tlacitko_m.collidepoint(udalost.pos):
                aktualni_mapa = 2 if aktualni_mapa == 1 else 1
                archer.topleft = (50, 535)
                print("Mapa:", aktualni_mapa)
            elif tlacitko_o.collidepoint(udalost.pos):
                aktualni_mapa = 3 if aktualni_mapa == 1 else 1
                print("Mapa:", aktualni_mapa)
            elif tlacitko_i.collidepoint(udalost.pos):
                aktualni_mapa = 4 if aktualni_mapa == 1 else 1
                print("Mapa:", aktualni_mapa)
                
            if aktualni_mapa == 3:
                # Luk
                if sloty[0].collidepoint(udalost.pos) and not koupeno_luk:
                    if penize >= cena_luk:
                        penize -= cena_luk
                        koupeno_luk = True
                        rychlost_strely = 18
                        
                        aktualni_luk = luk_hrac
                        aktualni_luk_up = luk_hrac_up
                        
                        inventar.append("luk")
                # Helma
                if sloty[1].collidepoint(udalost.pos) and not koupeno_helma:
                    if penize >= cena_helma:
                        penize -= cena_helma
                        koupeno_helma = True
                        pocet_zivotu += 25
                        
                        inventar.append("helma_obchod")
                # Brnění
                if sloty[2].collidepoint(udalost.pos) and not koupeno_brneni:
                    if penize >= cena_brneni:
                        penize -= cena_brneni
                        koupeno_brneni = True
                        pocet_zivotu += 50
                        
                        inventar.append("brneni_obchod")
                # Heal potion
                if sloty[3].collidepoint(udalost.pos) and not koupeno_heal_potion:
                    if penize >= cena_heal_potion:
                        penize -= cena_heal_potion
                        koupeno_heal_potion = True
                        pocet_zivotu += heal_amount
                        
                        inventar.append("heal_potion")

                # Fire resistance potion
                if sloty[4].collidepoint(udalost.pos) and not koupeno_fire_resistance_potion:
                    if penize >= cena_fire_resistance_potion:
                        penize -= cena_fire_resistance_potion
                        koupeno_fire_resistance_potion = True
                        fire_resistance_active = True
                        
                        inventar.append("fire_resistance_potion")

                # Coin potion
                if sloty[5].collidepoint(udalost.pos) and not koupeno_coin_potion:
                    if penize >= cena_coin_potion:
                        penize -= cena_coin_potion
                        koupeno_coin_potion = True
                        coin_bonus = 5
                        
                        inventar.append("coin_potion")
                        
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
        
    # Omezená hranice
    ctverecek_y = max(0, min(ctverecek_y, rozliseni_okna[1] - velikost_ctverecku))
    
    # Posun strely
    if strela_leti:
        sip_rect.x += sip_smer_x * rychlost_strely
        sip_rect.y += sip_smer_y * rychlost_strely
        if (sip_rect.left > rozliseni_okna[0] or sip_rect.right < 0 or sip_rect.top > rozliseni_okna[1] or sip_rect.bottom < 0):
            strela_leti = False
         
        if aktualni_mapa == 2 and sip_rect.colliderect(kbelik_rect):
            for o in ohne:
                o["faktor"] -= 0.05  
                o["faktor"] = max(o["faktor"], 0)  
            presun_kbelik()
            strela_leti = False
            
        if aktualni_mapa == 3:
            strela_leti = False
        if aktualni_mapa == 4:
            strela_leti = False
    # ------ Questy ------
    # Kontrola 2. Questu (Hasič) 
    if all(o["faktor"] <= 0 for o in ohne) and not questy[1].splneno:
        mesto_uhaseno = True  
        if not questy[1].splneno:
            if questy[1].pridej_postup():
                penize += questy[1].odmena
                if aktualni_quest_index == 1: 
                    aktualni_quest_index = 2

    # Kontrola 3. Questu (Boháč) 
    questy[2].postup = penize
    if questy[2].postup >= questy[2].cil and not questy[2].splneno:
        questy[2].splneno = True
        if aktualni_quest_index == 2:
            aktualni_quest_index = 3
            
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
    # 1. Mapa
    if aktualni_mapa == 2:
        if klavesy[pygame.K_a]:
            archer.x -= posun_ctverecku
        if klavesy[pygame.K_d]:
            archer.x += posun_ctverecku
    # 2. Mapa
    else:
        if klavesy[pygame.K_w]:
            archer.y -= posun_ctverecku
        if klavesy[pygame.K_s]:
            archer.y += posun_ctverecku

    # --------- Vykreslení v mapách --------- 
    # 1. Mapa
    if aktualni_mapa == 1:
        okno.fill((barva_pozadi))
    # 2. Mapa
    if aktualni_mapa == 2:
        okno.blit(horici_mesto, horici_mesto_rect)
        # Vykreslení kbeliku
        okno.blit(kbelik, kbelik_rect)
        for o in ohne:
            if o["faktor"] > 0:
                velikost = int(100 * o["faktor"])
                if velikost > 0: 
                    ohen_zmenseny = pygame.transform.scale(ohen, (velikost, velikost))
                    rect = ohen_zmenseny.get_rect(center=o["rect"].center)
                    okno.blit(ohen_zmenseny, rect)
    # 3. Mapa
    if aktualni_mapa == 3:
        okno.blit(obchod, obchod_rect)
        # Sloty
        for i, slot in enumerate(sloty):
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
        luk_obchod_rect.center = sloty[0].center
        okno.blit(luk_obchod, luk_obchod_rect)
        # Helma do druhého slotu
        helma_obchod_rect.center = sloty[1].center
        okno.blit(helma_obchod, helma_obchod_rect)
        # Brnění do třetího slotu
        brneni_obchod_rect.center = sloty[2].center
        okno.blit(brneni_obchod, brneni_obchod_rect)
        # Heal potion
        heal_potion_rect.center = sloty[3].center
        okno.blit(heal_potion,heal_potion_rect)
        # Fire resistance potion
        fire_resistance_potion_rect.center = sloty[4].center
        okno.blit(fire_resistance_potion, fire_resistance_potion_rect)
        # Coin potion
        coin_potion_rect.center = sloty[5].center
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

        for i, slot in enumerate(sloty):
            cena_text = font.render(str(ceny[i]) + "$", True, (0, 0, 0))
            cena_rect = cena_text.get_rect(midtop=(slot.centerx, slot.bottom + 5))
            okno.blit(cena_text, cena_rect)
    # 4. Mapa
    if aktualni_mapa == 4:
        okno.fill((barva_inventare))
        for i, item in enumerate(inventar):
            if i < len(sloty):
                okno.blit(dostatek_penez, sloty[i])
                
                if item == "luk":
                    luk_obchod_rect.center = sloty[i].center
                    okno.blit(luk_obchod, luk_obchod_rect)

                elif  item == "helma_obchod":
                    helma_obchod_rect.center = sloty[i].center
                    okno.blit(helma_obchod, helma_obchod_rect)   
 
                elif item == "brneni_obchod":
                    brneni_obchod_rect.center = sloty[i].center
                    okno.blit(brneni_obchod, brneni_obchod_rect)

                elif item == "heal_potion":
                    heal_potion_rect.center = sloty[i].center
                    okno.blit(heal_potion, heal_potion_rect)

                elif item == "fire_resistance_potion":
                    fire_resistance_potion_rect.center = sloty[i].center
                    okno.blit(fire_resistance_potion, fire_resistance_potion_rect)

                elif item == "coin_potion":
                    coin_potion_rect.center = sloty[i].center
                    okno.blit(coin_potion, coin_potion_rect)
    # Srdíčko
    okno.blit(srdicko, srdicko_rect)

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
    if aktualni_mapa == 1 or aktualni_mapa == 2:
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
        else:
            luk_rect = aktualni_luk_up.get_rect(midbottom=archer.midtop)
            okno.blit(aktualni_luk_up, luk_rect)
                
    # Vykreslení šipu
    if strela_leti:
        okno.blit(sip_aktualni, sip_rect)
        
    # Vykreslení tlačítka pro město
    if mesto_odemcene:
        pygame.draw.rect(okno, (0, 0, 0), tlacitko_m)
        text = font.render("Městečko", True, (200, 0, 0))
        okno.blit(text, text.get_rect(center=tlacitko_m.center))
    # Vykreslení tlačítka pro obchod
    pygame.draw.rect(okno, (0, 0, 0), tlacitko_o)
    text = font.render("Obchod", True, (200, 0, 0))
    okno.blit(text, text.get_rect(center=tlacitko_o.center))
    # Vykreslení tlačítka pro inventář
    pygame.draw.rect(okno, (0, 0, 0), tlacitko_i)
    text = font.render("Inventář", True, (200, 0, 0))
    okno.blit(text, text.get_rect(center=tlacitko_i.center))
    # Skore
    text = font.render(f"Peníze: {penize}", True, (0, 0, 200))
    text_rect = text.get_rect(midtop=(rozliseni_okna[0] // 2, 10))
    okno.blit(text, text_rect)
    # Životy
    text = font.render(f"Životy: {pocet_zivotu}", True, (0, 0, 200))
    text_rect = text.get_rect(center=(rozliseni_okna[0] // 2, 55))
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
            
            # Barva podle toho, jestli je splněno (pro jistotu)
            barva = (0, 200, 0) if q.splneno else (0, 0, 0)

            nazev_text = font.render(f"{q.nazev}: {q.postup}/{q.cil}", True, barva)
            okno.blit(nazev_text, (550, y_offset))

            popis_font = pygame.font.SysFont(None, 28)
            popis_text = popis_font.render(q.popis, True, (0, 0, 255))
            okno.blit(popis_text, (550, y_offset + 35))
    else:
        # Pokud jsou všechny questy hotové
        vse_hotovo_text = font.render("Všechny questy splněny!", True, (0, 200, 0))
        okno.blit(vse_hotovo_text, (450, 10))
    # Konec hry
    if konec_hry:
        strela_leti = False
        text = font.render("Konec hry", True, (200, 0, 0))
        okno.blit(text, (300, 250))
        
    # Promítnutí změn na displeji
    pygame.display.update()
    # Omezení fps ve hře
    vsync.tick(FPS)