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
# Tlačítko
tlacitko = pygame.Rect(620, 40, 120, 50)
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
# Hra stále běží
konec_hry = False


# Vytvoření Hráče 
archer = pygame.Rect(ctverecek_x, ctverecek_y, velikost_ctverecku, velikost_ctverecku)
# Šíp
obrazek_sipu = pygame.image.load("./sip_strela.png").convert_alpha()
sip = pygame.transform.scale_by(obrazek_sipu, 0.15)
sip_rect = sip.get_rect()
# Srdíčko
obrazek_srdicka = pygame.image.load("./srdicko.png").convert_alpha()
srdicko = pygame.transform.scale_by(obrazek_srdicka, 0.1)
srdicko_rect = srdicko.get_rect(center=(rozliseni_okna[0] // 1.58, 55))
# Prazdné srdíčko
obrazek_prazdneho_srdicka = pygame.image.load("./prazdne_srdicko.png").convert_alpha()
prazdne_srdicko = pygame.transform.scale_by(obrazek_prazdneho_srdicka, 0.1)
prazdne_srdicko_rect = prazdne_srdicko.get_rect(center=(rozliseni_okna[0] // 1.58, 55))
# Pozadí 2. Mapy
obrazek_horiciho_mesta = pygame.image.load("./Horici_mesto.png").convert_alpha()
horici_mesto = pygame.transform.scale(obrazek_horiciho_mesta, rozliseni_okna)
horici_mesto_rect = horici_mesto.get_rect(topleft=(0, 0))
# Komandy které stále běží
while True:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if udalost.type == pygame.KEYDOWN:
            if udalost.key == pygame.K_e and not strela_leti:
                strela_leti = True
                sip_rect.midleft = archer.midright
                sip_smer_x = 1
                sip_smer_y = 0

        if udalost.type == pygame.MOUSEBUTTONDOWN:
            if tlacitko.collidepoint(udalost.pos):
                aktualni_mapa = 2 if aktualni_mapa == 1 else 1
                archer.topleft = (50, 535)
                print("Mapa:", aktualni_mapa)
         
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

    if aktualni_mapa == 1:
        terc_rect = pygame.Rect(terc_x, terc_y, sirka_terce, sirka_terce)
        if strela_leti and faktor > 0 and sip_rect.colliderect(terc_rect):
            penize += 10
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

    # Vykreslení
    if aktualni_mapa == 1:
        okno.fill((barva_pozadi))
    else:
        okno.blit(horici_mesto, horici_mesto_rect)
    # Srdíčko
    okno.blit(srdicko, srdicko_rect)
    # Vykreslení kruhů
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
    # Vykreslení Hráče
    pygame.draw.rect(okno, (50, 50, 50), archer)
    # Vykreslení šipu
    if strela_leti:
        okno.blit(sip, sip_rect)
    # Vykreslení tlačítka
    pygame.draw.rect(okno, (0, 0, 0), tlacitko)
    text = font.render("Městečko", True, (200, 0, 0))
    okno.blit(text, text.get_rect(center=tlacitko.center))
    # Skore
    text = font.render(f"Peníze: {penize}", True, (0, 0, 0))
    text_rect = text.get_rect(midtop=(rozliseni_okna[0] // 2, 10))
    okno.blit(text, text_rect)
    # Životy
    text = font.render(f"Životy: {pocet_zivotu}", True, (0, 0,0))
    text_rect = text.get_rect(center=(rozliseni_okna[0] // 2, 55))
    okno.blit(text, text_rect)
    # Konec hry
    if konec_hry:
        strela_leti = False
        text = font.render("Konec hry", True, (200, 0, 0))
        okno.blit(text, (300, 250))
    # Promítnutí změn na displeji
    pygame.display.update()
    # Omezení fps ve hře
    vsync.tick(FPS)