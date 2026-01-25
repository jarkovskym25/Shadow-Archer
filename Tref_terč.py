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
#Informace pro střelu
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
# Šíp
obrazek_sipu = pygame.image.load("./sip_strela.png").convert_alpha()
sip = pygame.transform.scale_by(obrazek_sipu, 0.1)
sip_rect = sip.get_rect()
# Srdíčko
obrazek_srdicka = pygame.image.load("./srdicko.png").convert_alpha()
srdicko = pygame.transform.scale_by(obrazek_srdicka, 0.1)
srdicko_rect = srdicko.get_rect(center=(rozliseni_okna[0] // 2, 50))
# Prazdné srdíčko
obrazek_prazdneho_srdicka = pygame.image.load("./prazdne_srdicko.png").convert_alpha()
prazdne_srdicko = pygame.transform.scale_by(obrazek_prazdneho_srdicka, 0.1)
prazdne_srdicko_rect = prazdne_srdicko.get_rect(center=(rozliseni_okna[0] // 2, 50))
# Počet srdíček
pocet_srdicek = 1
# Komandy které stále běží
while True:
    for udalost in pygame.event.get():
        if udalost.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if not konec_hry and udalost.type == pygame.KEYDOWN:
            if udalost.key == pygame.K_RIGHT and not strela_leti:
                strela_leti = True
                sip_rect.center = (ctverecek_x + velikost_ctverecku, ctverecek_y + velikost_ctverecku // 2)
                
     # Pohyb s ctvereckem pomocí šipek
    stisknute_klavesy = pygame.key.get_pressed()
    if not konec_hry:
        if stisknute_klavesy[pygame.K_UP]:
            ctverecek_y -= posun_ctverecku
        if stisknute_klavesy[pygame.K_DOWN]:
            ctverecek_y += posun_ctverecku
  
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
        sip_rect.x += rychlost_strely
        if sip_rect.left > rozliseni_okna[0]:
            strela_leti = False
            pocet_srdicek -= 1
            
            if pocet_srdicek <= 0:
                pocet_srdicek = 0
                konec_hry = True

    # Čas terče
    aktualni_cas = pygame.time.get_ticks()
    uplynulo = aktualni_cas - terc_spawn_cas

    faktor = 1.0
    if uplynulo > terc_ceka:
        faktor = 1 - (uplynulo - terc_ceka) / terc_vyparovani
        faktor = max(faktor, 0)
        if faktor == 0:
            terc_x, terc_y = nahodna_pozice_terce()
    
    # Kolize
    terc_rect = pygame.Rect(terc_x, terc_y, sirka_terce, sirka_terce)
    if strela_leti and faktor > 0 and sip_rect.colliderect(terc_rect):
        penize += 10
        strela_leti = False
        terc_x, terc_y = nahodna_pozice_terce()
        
    # Vyplněné plochy barvou
    okno.fill(barva_pozadi)
    # Mínus srdíčko
    if pocet_srdicek > 0:
        okno.blit(srdicko, srdicko_rect)
    else:
        okno.blit(prazdne_srdicko, prazdne_srdicko_rect)
    
    # Vytvoření čtverečku 
    pygame.draw.rect(okno, (50, 50, 50), (ctverecek_x, ctverecek_y, velikost_ctverecku, velikost_ctverecku))
    # Vykreslení kruhů
    if faktor > 0:
        v1 = int(sirka_terce * faktor)
        v2 = int(sirka_terce_2 * faktor)
        v3 = int(sirka_terce_3 * faktor)

        o1 = (sirka_terce - v1) // 2
        o2 = (sirka_terce - v2) // 2
        o3 = (sirka_terce - v3) // 2
    pygame.draw.ellipse(okno, (200, 0, 0), (terc_x + o1, terc_y + o1, v1, v1))
    pygame.draw.ellipse(okno, (255, 255, 255), (terc_x + o2, terc_y + o2, v2, v2))
    pygame.draw.ellipse(okno, (200, 0, 0), (terc_x + o3, terc_y + o3, v3, v3))
    # Vykreslení šipu
    if strela_leti:
        okno.blit(sip, sip_rect)
    # Skore
    text = font.render(f"Peníze: {penize}", True, (0, 0, 0))
    text_rect = text.get_rect(midtop=(rozliseni_okna[0] // 2, 10))
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