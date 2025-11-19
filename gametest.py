#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, pygame, random, math, operator

# --- FUNZIONE XML PARSER ---
def x2d(file):
    try:
        xmlf=open(file,"r")
        xml=xmlf.read()
        xmlf.close()
    except FileNotFoundError:
        print(f"Errore: File {file} non trovato.")
        return {}
        
    di={}
    xml=xml.replace("    ","").replace("    ","").replace("\n","").replace("\t","")
    xmlr=xml.split("<")
    da=["di"]
    for e in xmlr:
        if not e.startswith("?") and e!="":
            if not e.startswith("/"):
                # Logica complessa originale mantenuta
                try:
                    idx_list = [pos for pos,char in enumerate(e) if char==">"]
                    if not idx_list: continue
                    idx = idx_list[-1]
                    
                    n=e[:idx]
                    if len(e)>idx+1:
                        tmp=e[idx+1:len(e)]
                        w=da[0]
                        for d in da:
                            if d!=da[0]:
                                w=w+"['"+d+"']"
                        exec("%s[n]=tmp"%w)
                    else:
                        w=da[0]
                        for d in da:
                            if d!=da[0]:
                                w=w+"['"+d+"']"
                        tmp={}
                        exec("%s[n]=tmp"%w)
                        da.append(n)
                except Exception as err:
                    print(f"Errore parsing XML riga: {err}")
            else:
                idx_list = [pos for pos,char in enumerate(e) if char==">"]
                if idx_list:
                    tag_end = e[1:idx_list[-1]]
                    if tag_end in da:
                        da.remove(tag_end)
    return di

# Caricamento opzioni (gestito con try/except per evitare crash se mancano file)
try:
    options=x2d("options-test.xml")
    # Fallback se options è vuoto o manca la chiave lang
    lang_code = options.get("lang", "it") 
    langf="lang/"+lang_code+"-test.xml"
    langr=x2d(langf)
except Exception:
    print("Attenzione: File XML di configurazione mancanti o corrotti.")
    langr = {"vincentmangiolli": {"dialog": {"1": "Ciao!"}}, "nicolaiavmenise": {"dialog": {"1": "Ehi!"}}}


def ri(f):
    try:
        return f+random.choice(os.listdir(f))
    except:
        return "" # Ritorna vuoto se la cartella non esiste

def psd(objs,x,y,screen):
    for obj in objs:
        try:
            image=pygame.image.load(obj)
            screen.blit(image, (x,y))
        except:
            pass # Salta immagini mancanti

def txt(txt,px,x,y):
    if not "\n" in txt:
        return screen.blit((pygame.font.Font("font/kongtext.ttf",px)).render(txt,False,(0,0,0)),(x,y))
    else:
        lines=txt.split("\n")
        i=0
        for line in lines:
            screen.blit((pygame.font.Font("font/kongtext.ttf",px)).render(line,False,(0,0,0)),(x,y+px*i))
            i+=1

def txtw(txt,px,x,y):
    if not "\n" in txt:
        return screen.blit((pygame.font.Font("font/kongtext.ttf",px)).render(txt,False,(255,255,255)),(x,y))
    else:
        lines=txt.split("\n")
        i=0
        for line in lines:
            screen.blit((pygame.font.Font("font/kongtext.ttf",px)).render(line,False,(255,255,255)),(x,y+px*i))
            i+=1

def near(x,y):
    dx=40
    dy=40
    if playerx>=x:
        if playerx-x<=dx:
            if playery>=y:
                if playery-y<=dy:
                    return True
                else:
                    return False
            elif playery<y:
                if y-playery<=dy:
                    return True
                else:
                    return False
    elif playerx<x:
        if x-playerx<=dx:
            if playery>=y:
                if playery-y<=dy:
                    return True
                else:
                    return False
            elif playery<y:
                if y-playery<=dy:
                    return True
                else:
                    return False

def talk(who,t):
    b=pygame.Surface((ww,wh))
    b.set_alpha(50)
    b.fill((0,0,0))
    screen.blit(b,(0,0))
    pygame.display.flip()

    isqh=150     # image square height
    isqw=150     # image square width
    dsqh=100     # dialog square height
    dsqw=ww-isqw # dialog square width
    br=10        # border
    pd=10        # padding
    ts=15        # txt size
    st=dsqw-pd*2 # space for one line of text
    cl=int(st/ts)# char for line

    running=True
    while running:
        pygame.draw.rect(screen,(0,0,0),(0,wh-isqh-br,isqw+br,isqh+br))
        pygame.draw.rect(screen,(255,255,255),(0,wh-isqh,isqw,isqh))
        pygame.draw.rect(screen,(0,0,0),(isqw,wh-dsqh-br,dsqw+br,dsqh+br))
        pygame.draw.rect(screen,(255,255,255),(isqw+br,wh-dsqh,dsqw,dsqh))
        
        # FIX: Python 3 divisione float
        if len(t)>cl and not "\n" in t:
            for i in range(int(len(t)/cl)): 
                t=t[:cl*(i+1)]+"\n"+t[cl*(i+1):]
                
        txt(t,ts,isqw+br+pd,wh-dsqh+pd)
        try:
            whoimg=pygame.image.load(who)
            screen.blit(whoimg,(0,wh-isqh))
        except:
            pass
            
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    running=False
            if event.type==pygame.QUIT:
                running=False
        pygame.display.flip()

def intro():
    screen.fill((0,0,0))
    pygame.display.flip()

    alpha=0
    alphat=True
    alpha2=0
    alpha2t=True
    alpha3=0
    alpha3t=True

    fs=.5 # fade speed

    running=True
    while running:
        screen.fill((0,0,0))
        try:
            image=pygame.image.load("glc.png")
            image.set_alpha(alpha)
            screen.blit(image,(ww/2-150/2,wh/2-150/2))
        except: pass # Salta se manca immagine
        
        prs=(pygame.font.Font("font/kongtext.ttf",30)).render("Presenta:",False,(255,255,255))
        prs.set_alpha(alpha2)
        screen.blit(prs,(ww/2-(30*len("Presenta:"))/2,wh/2-30/2))
        
        try:
            image=pygame.image.load("logo.png")
            image.set_alpha(alpha3)
            screen.blit(image,(ww/2-300/2,wh/2-300/2))
        except: pass
        
        if alpha<255 and alphat:
            alpha+=fs
        else:
            alphat=False
            if alpha>0:
                alpha-=fs
            else:
                if alpha2<255 and alpha2t:
                    alpha2+=fs
                else:
                    alpha2t=False
                    if alpha2>0:
                        alpha2-=fs
                    else:
                        if alpha3<255 and alpha3t:
                            alpha3+=fs
                        else:
                            alpha3t=False
                            if alpha3>0:
                                alpha3-=fs
                            else:
                                running=False
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    running=False
            if event.type==pygame.QUIT:
                global runningall;runningall=False
                running=False
        pygame.display.flip()

def menu():
    screen.fill((255,255,255))
    txt("MENU'",30,ww/2-15,0)
    txt("Nuova partita",20,ww/2-15,35)
    txt("Carica partita",20,ww/2-15,60)
    txt("Esci",20,ww/2-15,85)
    pygame.display.flip()

    o=1

    running=True
    while running:
        if o>3:
            o=1
        elif o<1:
            o=3
        screen.fill((255,255,255))
        pygame.draw.rect(screen,(255,255,145),(ww/2-15,o*25+10,300,20))
        txt("MENU'",30,ww/2-15,0)
        txt("Nuova partita",20,ww/2-15,35)
        txt("Carica partita",20,ww/2-15,60)
        txt("Esci",20,ww/2-15,85)
        pygame.display.flip()
        pressed=pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_w or event.key==pygame.K_a or event.key==pygame.K_UP or event.key==pygame.K_LEFT:
                    o-=1
                if event.key==pygame.K_s or event.key==pygame.K_d or event.key==pygame.K_DOWN or event.key==pygame.K_RIGHT:
                    o+=1
                if event.key==pygame.K_RETURN:
                    if o==1:
                        txt("Nuova partita...",30,0,0)
                        pygame.display.flip()
                        running=False
                        game()
                    if o==2:
                        txt("Carica partita...",30,0,0)
                        pygame.display.flip()
                        pygame.time.wait(1000)
                    if o==3:
                        running=False
                        global runningall; runningall=False
            if event.type==pygame.QUIT:
                running=False
                runningall=False
        pygame.display.flip()

def game():
    screen.fill((255,255,140))
    try:
        wall=pygame.image.load("texture/wall/wall001.png")
        floor=pygame.image.load("texture/floor/floor001.png")
    except:
        # Fallback texture se mancano file
        wall = pygame.Surface((150,150)); wall.fill((100,100,100))
        floor = pygame.Surface((150,150)); floor.fill((200,200,200))

    # walls
    minw=-50
    maxw=ww-105
    minh=35
    maxh=wh-125

    thingsdata={}

    pcpu001l="texture/fig/people/vincentmangiolli/little.png";thingsdata["pcpu001l"]=pcpu001l
    pcpu001n="texture/fig/people/vincentmangiolli/normal.png";thingsdata["pcpu001n"]=pcpu001n
    
    # FIX: Casting a int per randint
    pcpu001x=random.randint(int(minw),int(maxw));thingsdata["pcpu001x"]=pcpu001x
    pcpu001y=random.randint(int(minh),int(maxh));thingsdata["pcpu001y"]=pcpu001y

    pcpu002l="texture/fig/people/nicolaiavmenise/little.png";thingsdata["pcpu002l"]=pcpu002l
    pcpu002n="texture/fig/people/nicolaiavmenise/normal.png";thingsdata["pcpu002n"]=pcpu002n
    
    # FIX: Casting a int per randint
    pcpu002x=random.randint(int(minw),int(maxw));thingsdata["pcpu002x"]=pcpu002x
    pcpu002y=random.randint(int(minh),int(maxh));thingsdata["pcpu002y"]=pcpu002y

    pbodyl=ri("texture/bodylittle/")
    pfacel=ri("texture/facelittle/")
    peyel=ri("texture/eyelittle/")
    phairl=ri("texture/hairlittle/")
    pmouthl=ri("texture/mouthlittle/")
    ppants=ri("texture/pants/")
    pshoe=ri("texture/shoe/")
    
    for y in range(int(math.ceil(ww/150))+1):
        screen.blit(wall,(y*150,0))
    for x in range(int(math.ceil(wh/150))+1):
        screen.blit(floor,(0,(x+1)*150))
        for y in range(int(math.ceil(ww/150))+1):
            screen.blit(floor,(y*150,(x+1)*150))
            
    global playerx;playerx=120
    global playery;playery=160
    l=0
    psd([pcpu001l],pcpu001x,pcpu001y,screen)
    psd([pbodyl,pfacel,peyel,phairl,pmouthl,ppants,pshoe],playerx,playery,screen)
    pygame.display.flip()

    thingsd={"player":playery,"pcpu001":pcpu001y,"pcpu002":pcpu002y}
    
    # FIX: aggiunto import operator sopra
    thingsd=dict(sorted(thingsd.items(),key=operator.itemgetter(1)))
    things=thingsd

    music=False#music=True
    try:
        pygame.mixer.music.load("music/shootingstarsmidi.mid")
        if music:
            pygame.mixer.music.play()
    except: pass

    running=True
    while running:
        #pygame.time.wait(1)
        for y in range(int(math.ceil(ww/150))+1):
            screen.blit(wall,(y*150,0))
        for x in range(int(math.ceil(wh/150))+1):
            screen.blit(floor,(0,(x+1)*150))
            for y in range(int(math.ceil(ww/150))+1):
                screen.blit(floor,(y*150,(x+1)*150))

        pressed=pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            if playery>=35:
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    playery-=.5
                else:
                    playery-=.3
        if pressed[pygame.K_a]:
            if playerx>=-50:
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    playerx-=.5
                else:
                    playerx-=.3
        if pressed[pygame.K_s]:
            if playery<=wh-125:
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    playery+=.5
                else:
                    playery+=.3
        if pressed[pygame.K_d]:
            if playerx<=ww-105:
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    playerx+=.5
                else:
                    playerx+=.3

        if pressed[pygame.K_r]:
            pbodyl=ri("texture/bodylittle/")
            pfacel=ri("texture/facelittle/")
            peyel=ri("texture/eyelittle/")
            phairl=ri("texture/hairlittle/")
            pmouthl=ri("texture/mouthlittle/")
            ppants=ri("texture/pants/")
            pshoe=ri("texture/shoe/")

        if pressed[pygame.K_n]:
            if music:
                pygame.mixer.music.stop()
                music=False
            else:
                try:
                    pygame.mixer.music.play()
                    music=True
                except: pass

        if near(pcpu001x,pcpu001y):
            txt("'E' to talk",30,0,0)
            if pressed[pygame.K_e]:
                try:
                    dialogs = list(langr["vincentmangiolli"]["dialog"].items())
                    talk(pcpu001n,random.choice(dialogs)[1])
                except: pass
                
        if near(pcpu002x,pcpu002y):
            txt("'E' to talk",30,0,0)
            if pressed[pygame.K_e]:
                try:
                    dialogs = list(langr["nicolaiavmenise"]["dialog"].items())
                    talk(pcpu002n,random.choice(dialogs)[1].replace("R","V").replace("r","v"))
                except: pass

        thingsd={"player":playery,"pcpu001":pcpu001y,"pcpu002":pcpu002y}
        thingsd=sorted(thingsd.items(),key=operator.itemgetter(1))
        things=list(thingsd)

        for objr in things:
            obj=objr[0]
            if obj=="player":
                psd([pbodyl,pfacel,peyel,phairl,pmouthl,ppants,pshoe],playerx,playery,screen)
            else:
                psd([thingsdata[str(obj)+"l"]],thingsdata[str(obj)+"x"],thingsdata[str(obj)+"y"],screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
def main():
    pygame.init()
    pygame.font.init()
    try:
        logo=pygame.image.load("logo.png")
        pygame.display.set_icon(logo)
    except: pass
    
    pygame.display.set_caption("VaporSchool")

    global info;info=pygame.display.Info()
    # FIX: Cast a int per evitare float creep in coordinate
    global ww;ww=int(info.current_w/3)
    global wh;wh=int(info.current_h/3)
    global screen;screen=pygame.display.set_mode((ww,wh))

    global runningall;runningall=True

    intro()
    if runningall:
        menu()

if __name__=="__main__":
    main()
