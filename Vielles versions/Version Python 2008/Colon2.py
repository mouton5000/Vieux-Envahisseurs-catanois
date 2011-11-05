# Colon de catan V2.0 MSP Dimitri WATEL

#-----------------------------------------------------------------------------------------------------------------------#

# Plan de l'exécution du programme :
#  Introduction : nombre de joueur, mode de jeu
#  Création du terrain selon le mode de jeu
#  Lancement des dès pour savoir qui commence
#  Placement des colonies initiales
#  Placement des colonies finales => Ressources
#  Commencement du jeu => lancé de dès, ressource ou voleur, marchandage, constructions, décompte des points de victoires
#  Les règles peuvent être rappelée à tout instant

# Enfin TOUT METTRE EN OEUVRE POUR QUE LE PROGRAMME NE S'ARRETE PAS EN CAS DE MAUVAISE RENTREE DE DONNEES

#------------------------------------------------------------------------------------------------------------------------#

# Plan du programme

  # Ouverture de bibliothèques
   # Tkinter
   # Random
  
  # Fonctions
    #=> Choixclik, choixcons, Introduction, Evaluer et Evaluernom
    #=> Regles
    #=> listmelange
    #=> hexagone, cercle, cercleport
    #=> index
    #=> distance, recherche, rechercheindex, pointcons
    #=> lancerde
    #=> finirtour
    #=> fenetreprincipale
  
  # Exectution du programme

#------------------------------------------------------------------------------------------------------------------------#


# Variables globales !!!!!!

# Choixclik; entr; entrn; cnbrj; nom; nbrj; joueur; choixcons



#------------------------------------------------------------------------------------------------------------------------#


# Rappel des quantité sur le plateau



# Caractéristiques du plateau NORMAL

# - 4 fiches coût de construction
# - 2 fiches (routes, armée)
# - 5 colonies, 4 villes, 15 routes par couleur (*4)
# - 1 pion voleur
# - 18 jetons numérotés (2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12)
# - 25 cartes développement
# - 18 tuiles terrains (forêt, colline, Champs Pré, Montagne)
#- 95 cartes ressources (Bois, argile, blé, mouton, caillou)
# - 18 tuiles maritime (9 sans port, 4 port ?, 1 port de chaque élément)
# - 1 tuile désert
# - 2 dès

# De haut en bas, nombre de tuile par ligne, avec les maritimes :
# 4(maritimes),5,6,7,6,5,4(maritimes)

# - 12 Chevalier
# - Progrès
#    3 Construction de route
#    3 Invention
#    3 Monopole
# - 4 Construction spréciale



# Caractéristique du plateau extension

# - 11 tuiles terrain
# - 4 tuiles maritime
# - 2 couleurs de plus (avec le même nombre que plus haut
# - 25 cartes ressources en plus (dont un désert)
# - 9 dévellopements
# - 28 jetons nimérotés

# (en tout)
# De haut en bas, nombre de tuile par ligne, avec les maritimes :
# 4(maritimes),5,6,7,8,7,6,5,4(maritimes)

# (en tout)
# - 20 Chevalier
# - Progrès
#     3 Construction de route (constuit 2 routes à un endroit autorisé)
#     3 Invention (prends 2 ressources e son choix à la banque)
#     3 Monopole (volent toutes les ressources d'un type à tous les joueurs)
# - 5 Construction spréciale (1 point de victoire)


#------------------------------------------------------------------------------------------------------------------------#

#------------------------------------------------------------------------------------------------------------------------#
# Ouverture de bibliothèques
#------------------------------------------------------------------------------------------------------------------------#

from Tkinter import *
from random import randrange
from math import *

#------------------------------------------------------------------------------------------------------------------------#

#------------------------------------------------------------------------------------------------------------------------#
# Fonctions
#------------------------------------------------------------------------------------------------------------------------#

# Fonction d'introduction = nombre de joueur, noms des joueurs et mode de jeu

#Fonction qui permet de déplacer le voleur en lui attribuant la valeur x, ou une autre valeur si nécessaire
def depvoleur(x):
  global voleur
  voleur = x

#Fonction qui détermine si le clik est véritable ou non
def choisirclik(x):
  global choixclik
  choixclik = x


  
  
#Fonction qui détermine quelle construction est en cour
def choisircons(x):
  global choixcons
  choixcons = x



# Dans la fenetre cnbrj, evalue le nombre entré par l'utilisateur
def evaluer(event):
   global nbrj 
   nbr = eval(entr.get())
   if (nbr>=1) and (nbr<=4):
    nbrj = nbr
    cnbrj.destroy()


# Dans la fenetre nom, evalue les noms rentrés par l'utilisateur   
def evaluernom(event):
   joueur.append(eval(entrn.get()))
   nom.destroy()

#Pour choisir la couleur du joueur i
def choisircoul(coul,i):
 global jcouleur
 jcouleur[i] = coul



#Fonction qui introduit ^^
def introduction():
  global  entr,entrn, cnbrj,nom,jcouleur
  
 
  
  #Fenêtre de bienvenue
  bienv=Tk()
  can = Canvas(bienv, width=295, height=205, bg="red")
  photo = PhotoImage(file = "C:\Users\Dimitri\Documents\Programmation\Python\Colon de Catane\colon.gif")
  item = can.create_image(150,100, image=photo)
  can.pack()
  txt = Label(bienv, text='BIENVENUE AU COLON DE CATAN MSP Python')
  txt2 = Label(bienv, text='Amusez vous bien')
  txt.pack()
  txt2.pack()
  sortie=Button(bienv, text='Ok', command=bienv.destroy)
  sortie.pack(side=RIGHT)
  bienv.mainloop()





  #Fenêtre pour compter le nombre de joueur
  cnbrj=Tk()
  can = Canvas(cnbrj, width=100, height=10)  
  txt1=Label(cnbrj, text='Combien y a-t-il de joueur?')
  entr=Entry(cnbrj)
  entr.bind("<Return>",evaluer)
  txt1.pack()
  can.pack()
  entr.pack(side=LEFT)
  cnbrj.mainloop()


  #Fenêtre pour déterminer les noms de joueurs et leur couleur
  for i in range(nbrj):
  
    jcouleur.append("blue")
    nom=Tk()
    txt=Label(nom, text='Donnez le nom du joueur '+str(i+1)  + 'et choisissez sa couleur', font=('Arial',13))
    entrn=Entry(nom)
    entrn.bind("<Return>",evaluernom)
    var = IntVar()
    Radiobutton(nom,text="Bleu",  variable = var, value=0, command= lambda coul="blue",  x=i:choisircoul(coul,x)).pack()
    Radiobutton(nom,text="Vert",  variable = var, value=1, command= lambda coul="green", x=i:choisircoul(coul,x)).pack()
    Radiobutton(nom,text="Rouge", variable = var, value=2, command= lambda coul="red",   x=i:choisircoul(coul,x)).pack()
    Radiobutton(nom,text="Marron",variable = var, value=3, command= lambda coul="brown", x=i:choisircoul(coul,x)).pack()
    Radiobutton(nom,text="Blanc", variable = var, value=4, command= lambda coul="white", x=i:choisircoul(coul,x)).pack()
    Radiobutton(nom,text="Orange",variable = var, value=5, command= lambda coul="orange",x=i:choisircoul(coul,x)).pack()
    Radiobutton(nom,text="Jaune", variable = var, value=6, command= lambda coul="yellow",x=i:choisircoul(coul,x)).pack()
    Radiobutton(nom,text="Violet",variable = var, value=7, command= lambda coul="violet",x=i:choisircoul(coul,x)).pack()
    txt.pack()
    entrn.pack()
    nom.mainloop()

# Fin de l'introduction
#------------------------------------------------------------------------------------------------------------------------#

# Procedure d'affichage des règles

def Regle():
  global photoregle
  regle=Tk()
  can=Canvas(regle, width=430, height=430, bg="white")
  photoregle = PhotoImage(file = "C:\Users\Dimitri\Documents\Programmation\Python\Colon de Catane\plateaucatane2.gif")
  item = can.create_image(215,215, image=photoregle)
  
  
  txt=Label(regle, text='Voici les règles du Colon de Catane')
  
  plateau=Label(regle,text='I) À gauche, vous pouvez observer le plateau de jeu.\
  Celui-ci est composé\n de différents hexagones, Des bleus, des colorés, ...\
  Le principe est simple,\n un hexagone bleu représente une tuile ou parcelle maritime.\
  Un hexagone coloré\n représente une tuile forêt, colline, Champs Pré ou  Montagne.\
  Un dernier type de\n tuile est le Desert, stérile surlequel rien ne pousse.\
  Les tuiles terrestres rapportent\n des ressources que les joueurs peuvent utiliser\
  pour se développer. Certaines\n tuiles maritimes comportent des ports pour faire des\
  echanges. Le but du jeu est\n de se développer sur ce terrain plus vite que les autres.')
  
  ressource=Label(regle,text='II) Chaque Hexagone terrestre sauf le désert donne accès à des ressources\
  différentes :\n La forêt donne accès au bois, les collines à la pierre, les champs au blé,\
  les prairies\n à la laine de mouton, et la montagne à l\'argile. Les ressources servent à construire\
  \nles routes, les colonies, les villes ou à avoir des cartes développement. Bref, sans ressources \nvous\
  n\'avez rien. Comment obtenir des ressources? C\'est expliqué plus loin.')
  
  
  colonie=Label(regle,text='III) Au début de la partie, vous obtenez 2 colonies que vous\
  pouvez placer à n\'importe\n quelle intersection de 3 hexagones (terrestre ou maritime).\
  Elle vous donne accès aux\n ressources liés aux hexagones et uniquement à celles là.\
  Choisissez bien votre emplacement.\n Après avoir récolté des ressources, et avoir marchandé\
  vous pouvez construire ou acheter\n des cartes développement. Vous pouvez construire une\
  route en payant un bois et un argile.\n Elles doivent être placés soit à côté d\'une de vos\
  colonie soit à côté d\'une autre de vos routes.\n Vous pouvez construire une colonie, il\
  vous faut un bois, un mouton, un blé et un argile.\n Vous devez placer votre colonie à l\'extrémité\
  d\'une route si l\'emplacement choisi est au moins\n éloigné de 2 voies avec une\
  colonie quelconque. Vous pouvez améliorer vos colonies en Ville avec\n 2 blés et 3 caillous. Les villes\
  rapportent 2 fois plus de ressources. Enfin vous pouvez acheter\n des cartes de développement.\
  Elles rapportent un bonus au hasard parmi 5. Elles coûtent un blé, un mouton,\n un caillou\
  et ne peuvent être utilisé que le tour suivant l\'achat. (1 par tour)')
  
  obtres=Label(regle,text='IV) Comment se déroule le jeu? Les tuiles sont placées au\
  hasard\n sur le continent. Après celà, on dépose, toujours au hasard,\n un numéro sur chaque tuile.\
  On choisit un ordre au dé.\n On place dans cet ordre une colonie sur le plateau,\n puis une autre, dans\
  l\'ordre inverse. On place également\n avec chaque colonie une route accolée. Lorsque l\'on place la 2e\
  \ncolonie, on obtient automatiquement une carte pour chaque ressource\n touchée par cette colonie. Commence ensuite le jeu\
  A chaque Tour,\n le joueur lance le dé. Si une des colonies touche une tuile avec ce numéro,\n il obtient\
  une ressource liée à cette tuile (ou 2 si c\'est une ville).\n Le joueur actif peut ensuite marchander\
  (voir plus loin).\n Enfin il peut construire comme indiqué dans la section adéquate.')
  
  echange=Label(regle,text='V) Les échanges ne sont pas bien compliqués. Une fois que les ressources\
  sont récoltées,\n le joueur actif peut marchander des ressources avec d\'autres joueurs ou marchander\
  des ressources\n avec la banque. Le taux général est de 4 mêmes ressources de votre choix contre une\
  ressource de\n votre choix. Si vous contrôlez un port, c\'est-à-dire si une de vos colonies est construite\
  sur la case\n port, Vous pouvez échanger selon le taux indiqué. Le ? signifie 3 mêmes ressources contre ce que\
  vous\n voulez, sinon le dessin indique que vous pouvez donner 2 ressources indiquée contre ce que vous voulez.')
  
  voleur=Label(regle,text='VI) Le voleur apparaît lorsqu\'un joueur fait un 7 au dé. Aucune ressource n\'est\
  distribuée.\n Le joueur actif déplace le voleur sur une tuile terrestre autre que le désert. Elle peut ou non\
  toucher\n une colonie. Il peut alors choisir une de ces colonies et voler au hasard une carte ressource de\n la\
  main du joueur concerné. Le voleur bloque la tuile tant qu\'il est dessus : elle ne produit plus\n de ressource.\
  Si un joueur le souhaite, il peut soudoyez le joueur actif (lui donner une carte de\n ressource de son plein gré)\
  et placer le voleur sur une autre tuile touchée par une colonie du\n soudoyeur. Enfin, si quelqu\'un possède\
  huit cartes ou plus dans sa main quand un joueur fait 7,\n il doit se défausser de la moitié de ses cartes, et\
  ce jusqu\' à ce qu\'il en ait moins de 7')
  
  victoire=Label(regle, text='La victoire est accordée par des points. On gagne 1 point par colonie en jeu\
  \n2 points par ville en jeu, 2 points pour l\'armée et/ou la route la plus grande et\n 4 cartes développement decernent un\
  point de victoire chacune. Vous gagnez\n si vous accumulez 10 points de victoire. Contrairement aux autres cartes\
  \ndéveloppement, celle donnant des points peuvent-être  abbatues ensemble le tour\n où elles sont achetées si elle fournissent\
  un nombre depoints nécessaire pour gagner.')
  
  
  sortie=Button(regle, text="Ok", width=10, height = 1, command=regle.destroy)
  
  can.grid(         row =1 , column =1, rowspan=3 )
  txt.grid(         row =4 , column =1 )
  plateau.grid(     row =1 , column =2 )
  ressource.grid(   row =2 , column =2 )
  colonie.grid(     row =3 , column =2, padx=5 )
  obtres.grid(      row =5 , column =1 )
  echange.grid(     row =4 , column =2 )
  voleur.grid(      row =5 , column =2 )
  victoire.grid(    row =6 , column =1, pady=5 )
  sortie.grid(      row =6 , column =2, pady=5 )
  regle.mainloop()

#Fin des règles
#------------------------------------------------------------------------------------------------------------------------#


#Procedure de mélange de liste
def listmelange(l):
   lprime = []
   tup=(l[1],)
   L=len(l)
   print "Melange en cours de " + str(L) + " elements"   
   for i in range(L):
    a=randrange(L)
    while (a in lprime):
      a=randrange(L)
    lprime.append(a)

   for i in range(L):
    if i==0 : 
      tup = (l[lprime[0]],)
    else :
      tup = ( tup + (l[lprime[i]],))
   print "Fin du melange"
   return tup
   
   
#------------------------------------------------------------------------------------------------------------------------#
   
#Procedure de creation d'un hexagone dans un Canevas, d'un cercle de rayon R/3 dans lequel Numero est centré, et d'un cercle port de rayon R/3
def hexagone(can,x,y,r, coul1="white", coul2="black"):
    can.create_polygon((x-r*sqrt(3./4.),y+r/2, x-r*sqrt(3./4.),y-r/2, x,y-r  , x+r*sqrt(3./4.),y-r/2 , x+r*sqrt(3./4.),y+r/2 , x,y+r), fill=coul1, width=2, outline=coul2)


def cercle(can,x,y,r,numero,coul="black"):
   if (numero==6) or (numero==8) :
    couleur = "red"
   else :
    couleur = "black"

   if (numero==2) or (numero==12):
    police  = ("Arial",12)
   else:
    police  = ("Arial", 20)

   if numero<>0: 
    can.create_oval(x-r/3.,y-r/3.,x+r/3.,y+r/3.,outline=coul,fill="#FFB56B")
    can.create_text(x,y,text=str(numero),fill=couleur, font=police)


def cercleport(can,x,y,r,coul,direction):

   rrac=sqrt(3./4.)*r
   trait=10
   ite=trait*2+1
   
   if direction==1:
    x0=x
    y0=y+r
    x1=x+rrac
    y1=y+r/2.
   
   elif direction==2:
    x0=x+rrac
    y0=y+r/2.
    x1=x+rrac
    y1=y-r/2.
   elif direction==3:
    x0=x+rrac
    y0=y-r/2.
    x1=x
    y1=y-r
   elif direction==4:
    x0=x
    y0=y-r
    x1=x-rrac
    y1=y-r/2.
   elif direction==5:
    x0=x-rrac
    y0=y-r/2.
    x1=x-rrac
    y1=y+r/2.
   elif direction==6 or direction==0:
    x0=x-rrac
    y0=y+r/2.
    x1=x
    y1=y+r

   for i in range(trait):
    can.create_line(x*(2*i)/ite+x0*(ite-2*i)/ite,y*(2*i)/ite+y0*(ite-2*i)/ite,x*(2*i+1)/ite+x0*(ite-2*i-1)/ite,y*(2*i+1)/ite+y0*(ite-2*i-1)/ite)
    can.create_line(x*(2*i)/ite+x1*(ite-2*i)/ite,y*(2*i)/ite+y1*(ite-2*i)/ite,x*(2*i+1)/ite+x1*(ite-2*i-1)/ite,y*(2*i+1)/ite+y1*(ite-2*i-1)/ite)



   
   can.create_oval(x-r/3.,y-r/3.,x+r/3.,y+r/3.,outline="black",fill=coul)
   can.create_oval(x0-r/10.,y0-r/10.,x0+r/10.,y0+r/10.,outline="black")
   can.create_oval(x1-r/10.,y1-r/10.,x1+r/10.,y1+r/10.,outline="black")
   
   if coul=="white":
    can.create_text(x,y,text="?",font=("Arial",20))
   
#------------------------------------------------------------------------------------------------------------------------#

#Trouve le premier index de l'élément i dans une liste l
def index(i,l):
   k=0
   while (k<> len(l)-1) and l[k]<>i:
    k=k+1
   return (k)
   
#------------------------------------------------------------------------------------------------------------------------# 
  
  
#calcule la distance de (x1,y1) à (x2,y2)  
def distance(x1,y1,x2,y2):
  return sqrt((x1-x2)*(x1-x2)+(y1-y2)*(y1-y2))


#Recherche le point d'une liste de points de R² le plus proche de (x,y), retourne ce point et son index
def recherche(list,x,y):
  n = len(list)
  k=n-1
  d=distance(x,y,list[n-1][0],list[n-1][1])
  for i in range(n):
    dp = distance(x,y,list[i][0],list[i][1])
    if dp<d:
      k=i
      d=dp
  return (list[k][0],list[k][1],k)

# recherche l'indice de x dans la list1 et renvoie l'élément correspondant de la list2 (utile pour déterminer les indices des 
# routes verticales, horiz haut et horiz bas (voir plus loin))
def rechercheindex(x,list1,list2):
  k = index(x,list1)
  return list2[k]


#Fenetre de réaction au clik d'une construction ou de déplacement de voleur
def pointcons(event,can,r,rrac,list1,list2,list3,list4,list5,list6,X0,Y0,l1,l2,lbl,cancoul):
 global choixclik,choixcons,matcons,nrojoueur,couleur,debut,debcons,voleur,vol1,vol2
  
 #Quelques variables locale : rp pour les graphiques, couleur est la couleur du joueur en cours, fentest vérifie si la construction est autorisée ou pas.
 rp = r/3.
 fentest = 0
 couleur = jcouleur[nrojoueur]
 
 # Si un joueur a demandé à construire un batîment ou une route.
 if debut==2 and voleur==0: 

   if choixcons == 1:#(route)
    x0,y0,k=recherche(list2,event.x,event.y) # On recherche l'emplacement de route le plus proche du clik
    lc = rechercheindex(k,range(len(list2)),l2) # On recherche dans matcons la ligne et la colonne en relation avec cette route
    ligne,colon = lc[1],lc[0]
    
    # Si elle est horizontale haute
    if k+1 in list3 and (matcons[ligne][colon][0] in [-2,-1]) and (matcons[ligne][colon-1][1] == nrojoueur or matcons[ligne][colon+1][1] == nrojoueur or matcons[ligne-2][colon/2][1] == nrojoueur\
    or matcons[ligne+2][colon/2][1] == nrojoueur or matcons[ligne-1][colon/2][1] == nrojoueur or matcons[ligne+1][colon/2][1] == nrojoueur):
      fentest = 1
      matcons[ligne][colon][0] = can.create_polygon(x0-rrac/4.+.05*r,y0+r/8.+0.05*r,x0-rrac/4.-.04*r,y0+r/8.-.05*r,x0+rrac/4.-.05*r,y0-r/8.-.05*r,x0+rrac/4.+.04*r,y0-r/8.+0.05*r,fill=couleur,outline="black")
      matcons[ligne][colon][1] = nrojoueur
    
    # Si elle est horizontale basse
    elif k+1 in list4 and (matcons[ligne][colon][0] in [-2,-1]) and (matcons[ligne][colon-1][1] == nrojoueur or matcons[ligne][colon+1][1] == nrojoueur or matcons[ligne-2][(colon-1)/2][1] == nrojoueur\
    or matcons[ligne+2][(colon+1)/2][1] == nrojoueur or matcons[ligne-1][(colon-1)/2][1] == nrojoueur or matcons[ligne+1][(colon+1)/2][1] == nrojoueur):
      fentest = 1
      matcons[ligne][colon][0] = can.create_polygon(x0-rrac/4.+.04*r,y0-r/8.-0.05*r,x0-rrac/4.-.05*r,y0-r/8.+.05*r,x0+rrac/4.-.05*r,y0+r/8.+.05*r,x0+rrac/4.+.04*r,y0+r/8.-0.05*r,fill=couleur,outline="black")
      matcons[ligne][colon][1] = nrojoueur   
    
    #Si elle est verticale
    elif k+1 in list5 and (matcons[ligne][colon][0] in [-2,-1]) and (matcons[ligne-2][2*colon-1][1] == nrojoueur or matcons[ligne-2][2*colon][1] == nrojoueur or matcons[ligne+2][2*colon][1] == nrojoueur\
    or matcons[ligne+2][2*colon+1][1] == nrojoueur or matcons[ligne-1][colon][1] == nrojoueur or matcons[ligne+1][colon][1] == nrojoueur):
      fentest = 1
      matcons[ligne][colon][0] = can.create_polygon(x0-0.05*r,y0-r/4,x0-0.05*r,y0+r/4,x0+0.05*r,y0+r/4,x0+0.05*r,y0-r/4,fill=couleur,outline="black")
      matcons[ligne][colon][1] = nrojoueur     
    
   elif choixcons == 2:#(Colonie)
    x0,y0,k=recherche(list1,event.x,event.y) # On recherche l'emplacement de colonie le plus proche du clik
    lc = rechercheindex(k,range(len(list1)),l1) # On recherche dans matcons la ligne et la colonne en relation avec cette colonie
    ligne,colon = lc[1],lc[0]
    
 
    if (matcons[ligne][colon][0] in [-2,-1]) and (((matcons[ligne-2][colon-1][0] in [-2,-1] and matcons[ligne-2][colon][0] in [-2,-1] and matcons[ligne+2][colon][0] in [-2,-1] and (matcons[ligne+1][colon][1] == nrojoueur or matcons[ligne-1][colon*2-1][1] == nrojoueur or matcons[ligne-1][colon*2][1] == nrojoueur)) and (ligne/4==ligne/4.)) or\
    ((matcons[ligne-2][colon][0] in [-2,-1] and matcons[ligne+2][colon][0] in [-2,-1] and matcons[ligne+2][colon+1][0] in [-2,-1] and (matcons[ligne-1][colon][1] == nrojoueur or matcons[ligne+1][colon*2][1] == nrojoueur or matcons[ligne+1][colon*2+1][1] == nrojoueur)) and (ligne/4<>ligne/4.))) :
      fentest = 1
      matcons[ligne][colon][0] = can.create_polygon(x0-rp*2/sqrt(18), y0+rp/3,x0-rp*2/sqrt(18), y0-rp/3,x0-0.4*rp,y0-0.4*rp,x0-0.4*rp,y0-0.6*rp,x0-0.2*rp,y0-0.6*rp,\
      x0-0.2*rp,y0-1.4/3*rp,x0,y0-0.6*rp,x0+rp*2/sqrt(18),y0-rp/3,x0+rp*2/sqrt(18),y0+rp/3,fill=couleur,outline="black")
      matcons[ligne][colon][1] = nrojoueur

    
   elif choixcons == 3: #(Ville)
    x0,y0,k=recherche(list1,event.x,event.y) # On recherche l'emplacement de ville le plus proche du clik
    lc = rechercheindex(k,range(len(list1)),l1) # On recherche dans matcons la ligne et la colonne en relation avec cette ville
    ligne,colon = lc[1],lc[0]
    

    if matcons[ligne][colon][1] == nrojoueur:
      can.delete(matcons[ligne][colon][0])
      matcons[ligne][colon][0] = can.create_polygon(x0-0.6*rp,y0+rp*0.4,x0-0.6*rp,y0-rp*0.8/3,x0-rp*0.3,y0-2*rp/3,x0,y0-rp*0.8/3,x0+0.6*rp,y0-rp*0.8/3,x0+0.6*rp,y0+rp*0.4,fill=couleur,outline="black")
      fentest=2
  
   # Si on a construit quelque chose, on demande si on veut l'annuler ou pas
   if fentest in [1,2]:
      fen1=Tk()
      var =IntVar()
      Label(fen1,text="Voulez-vous vraiment cliquer à cet endroit?").pack()
      Radiobutton(fen1,text="Oui",variable = var, value=1, command= lambda x=1:choisirclik(x)).pack()
      Radiobutton(fen1,text="Non",variable = var, value=0,command= lambda x=0:choisirclik(x)).pack()
      Button(fen1,text="Ok",command=fen1.quit).pack()
 
      fen1.mainloop()
      fen1.destroy()
   
      #Si non, on efface tout on recommence
      if choixclik<>1 and fentest == 1:
        can.delete(matcons[ligne][colon][0])
        matcons[ligne][colon] = [-2,-2]
      elif choixclik<>1 and fentest == 2:
        can.delete(matcons[ligne][colon][0])
        matcons[ligne][colon][0] = can.create_polygon(x0-rp*2/sqrt(18), y0+rp/3,x0-rp*2/sqrt(18), y0-rp/3,x0-0.4*rp,y0-0.4*rp,x0-0.4*rp,y0-0.6*rp,x0-0.2*rp,y0-0.6*rp,\
        x0-0.2*rp,y0-1.4/3*rp,x0,y0-0.6*rp,x0+rp*2/sqrt(18),y0-rp/3,x0+rp*2/sqrt(18),y0+rp/3,fill=couleur,outline="black")
      else: #Si oui, on efface rien, on précise que la construction est finie
        choixcons = -1
  
  
     #Sinon la construction est interdite
   else:
      fen1=Tk()
      Label(fen1,text="Construction interdite").pack()
      Button(fen1,text="Ok",command=fen1.destroy).pack()
      fen1.mainloop() 


 





    # Si on est en période de début, on construit simultanément une colonie et une route accolée.
 elif debut in [0,1] and voleur ==0:
  
  


  x0,y0,k=recherche(list2,event.x,event.y) # On recherche l'emplacement de route le plus proche du clik
  lc = rechercheindex(k,range(len(list2)),l2) # On recherche dans matcons la ligne et la colonne en relation avec cette route
  ligne,colon = lc[1],lc[0]
  x0p,y0p,kp=recherche(list1,event.x,event.y) # On recherche l'emplacement de colonie le plus proche du clik
  lc = rechercheindex(kp,range(len(list1)),l1) # On recherche dans matcons la ligne et la colonne en relation avec cette colonie
  lignep,colonp = lc[1],lc[0]   
   
  if(matcons[ligne][colon][0] in [-2,-1]) and \
  matcons[lignep][colonp][0] in [-2,-1] and ((matcons[lignep-2][colonp-1][0] in [-2,-1] and matcons[lignep-2][colonp][0] in [-2,-1] and matcons[lignep+2][colonp][0] in [-2,-1] and (lignep/4==lignep/4.)) or\
  (matcons[lignep-2][colonp][0] in [-2,-1] and matcons[lignep+2][colonp][0] in [-2,-1] and matcons[lignep+2][colonp+1][0] in [-2,-1] and (lignep/4<>lignep/4.))):

  # Si la route est horizontale haute
   if k+1 in list3:
     fentest = 1
     matcons[ligne][colon][0] = can.create_polygon(x0-rrac/4.+.05*r,y0+r/8.+0.05*r,x0-rrac/4.-.04*r,y0+r/8.-.05*r,x0+rrac/4.-.05*r,y0-r/8.-.05*r,x0+rrac/4.+.04*r,y0-r/8.+0.05*r,fill=couleur,outline="black")
     matcons[ligne][colon][1] = nrojoueur
     matcons[lignep][colonp][0] = can.create_polygon(x0p-rp*2/sqrt(18), y0p+rp/3,x0p-rp*2/sqrt(18), y0p-rp/3,x0p-0.4*rp,y0p-0.4*rp,x0p-0.4*rp,y0p-0.6*rp,x0p-0.2*rp,y0p-0.6*rp,\
     x0p-0.2*rp,y0p-1.4/3*rp,x0p,y0p-0.6*rp,x0p+rp*2/sqrt(18),y0p-rp/3,x0p+rp*2/sqrt(18),y0p+rp/3,fill=couleur,outline="black")
     matcons[lignep][colonp][1] = nrojoueur
    
   # Si la route est horizontale basse    
   elif k+1 in list4:
     fentest = 1
     matcons[ligne][colon][0] = can.create_polygon(x0-rrac/4.+.04*r,y0-r/8.-0.05*r,x0-rrac/4.-.05*r,y0-r/8.+.05*r,x0+rrac/4.-.05*r,y0+r/8.+.05*r,x0+rrac/4.+.04*r,y0+r/8.-0.05*r,fill=couleur,outline="black")
     matcons[ligne][colon][1] = nrojoueur  
     matcons[lignep][colonp][0] = can.create_polygon(x0p-rp*2/sqrt(18), y0p+rp/3,x0p-rp*2/sqrt(18), y0p-rp/3,x0p-0.4*rp,y0p-0.4*rp,x0p-0.4*rp,y0p-0.6*rp,x0p-0.2*rp,y0p-0.6*rp,\
     x0p-0.2*rp,y0p-1.4/3*rp,x0p,y0p-0.6*rp,x0p+rp*2/sqrt(18),y0p-rp/3,x0p+rp*2/sqrt(18),y0p+rp/3,fill=couleur,outline="black")
     matcons[lignep][colonp][1] = nrojoueur   

   # Si la route est verticale
   elif k+1 in list5:
     fentest = 1
     matcons[ligne][colon][0] = can.create_polygon(x0-0.05*r,y0-r/4,x0-0.05*r,y0+r/4,x0+0.05*r,y0+r/4,x0+0.05*r,y0-r/4,fill=couleur,outline="black")
     matcons[ligne][colon][1] = nrojoueur      
     matcons[lignep][colonp][0] = can.create_polygon(x0p-rp*2/sqrt(18), y0p+rp/3,x0p-rp*2/sqrt(18), y0p-rp/3,x0p-0.4*rp,y0p-0.4*rp,x0p-0.4*rp,y0p-0.6*rp,x0p-0.2*rp,y0p-0.6*rp,\
     x0p-0.2*rp,y0p-1.4/3*rp,x0p,y0p-0.6*rp,x0p+rp*2/sqrt(18),y0p-rp/3,x0p+rp*2/sqrt(18),y0p+rp/3,fill=couleur,outline="black")
     matcons[lignep][colonp][1] = nrojoueur
   

    
  finirtourtest = 0 # Indicateur de finisseur de tour, si il est nul, on ne change pas de personnage, le clik est à refaire.
  if fentest in [1,2]: # On a construit un truc, et on vérifie si on veut vraiment le construire là
      fen1=Tk()
      var =IntVar()
      Label(fen1,text="Voulez-vous vraiment cliquer à cet endroit?").pack()
      Radiobutton(fen1,text="Oui",variable = var, value=1, command= lambda x=1:choisirclik(x)).pack()
      Radiobutton(fen1,text="Non",variable = var, value=0,command= lambda x=0:choisirclik(x)).pack()
      Button(fen1,text="Ok",command=fen1.quit).pack()
 
      fen1.mainloop()
      fen1.destroy()
   
      if choixclik<>1:
       can.delete(matcons[ligne][colon][0])
       can.delete(matcons[lignep][colonp][0])
       matcons[ligne][colon] = [-2,-2]
       matcons[lignep][colonp] = [-2,-2]
 

      else:
       choixcons = -1
       finirtourtest=1
  
  
  else: # Si on a construit sur un endroit illégal
      fen1=Tk()
      Label(fen1,text="Construction interdite").pack()
      Button(fen1,text="Ok",command=fen1.destroy).pack()
      fen1.mainloop() 







  if finirtourtest==1: # Si l'indicateur vaut 1, on avance le curseur de fin de tour de 1
     finirtour(lbl,cancoul)



 elif voleur ==1 : # Si on a fait 7, cliquer sur l'écran reviendra a déplacer le voleur
  x0,y0,k=recherche(list6,event.x,event.y) # On recherche l'emplacement de voleur le plus proche du clik
  can.delete(vol1)
  can.delete(vol2)
  vol1 = can.create_polygon(x0+0.1*r,y0+0.1*r,x0+0.3*r,y0+0.4*r,x0-0.3*r,y0+0.4*r,x0-0.1*r,y0+0.1*r,fill="black")
  vol2 = can.create_oval(x0+0.2*r,y0+0.25*r,x0-0.2*r,y0-0.45*r,fill="black")   
  # (on construit immédiatement ici car il n'y a aucun test à faire, constrairement aux constructions qui nécessite une matrice qui mémorise le plateau)
  # Cela sera nécessaire si on désire savoir à tout instant où est le voleur.
  
  # Détermine si on désire placer le voleur là, ou le placer ailleurs.
  fen1=Tk()
  var =IntVar()
  Label(fen1,text="Laissez-vous le voleur à cet endroit?").pack()
  Radiobutton(fen1,text="Oui",variable = var, value=1, command= lambda x=1:choisirclik(x)).pack()
  Radiobutton(fen1,text="Non",variable = var, value=0,command= lambda x=0:choisirclik(x)).pack()
  Button(fen1,text="Ok",command=fen1.quit).pack()
 
  fen1.mainloop()
  fen1.destroy()
   
  if choixclik<>1:
    can.delete(vol1)
    can.delete(vol2)

  else:
  # Une fois placé, le voleur ne peut plus être déplacé avant un 7.
    voleur = 0
  
 
 
 
 
 
 
# Fonction qui lance les dés : choisi une nouvelle valeur pour les dés, et les affiche.
def lancerde(dec,delist,item1,item2):
  global photode1,photode2,nrojoueur,voleur
  i,j = randrange(6),randrange(6)
  dec.delete(item1)
  dec.delete(item2)
  photode1   = PhotoImage(file = delist[i])
  item1      = dec.create_image(28,30,image = photode1)
  photode2   = PhotoImage(file = delist[j])
  item2      = dec.create_image(3*28,30,image = photode2)
  
  # Lien avec le voleur si on fait 7
  if i+j == 5 and debut == 2:
    voleur = 1
    fen1 = Tk()
    Label(fen1, text = joueur[nrojoueur] + " a fait un 7, il peut déplacer le voleur").pack()
    Label(fen1, text = "Tout joueur possédant 8 cartes ou plus s'en défausse de la moitié").pack()
    Label(fen1, text = "Si après vous être défaussé, vous possédez encore 8 cartes ou plus, recommencez").pack()
    Label(fen1, text = "Une fois le voleur placé, un des joueurs sur l'hexagone du voleur se voit volé une carte au hasard").pack()
    Label(fen1, text = "Un de ses joueurs peut proposer une carte au voleur, et déplacer le pion sur l'hexagone de son choix").pack()
    Label(fen1, text = "Toutefois, cet hexagone doit être adjacent à une colonie de ce joueur").pack()
    Button(fen1, text = "Ok", command = fen1.destroy).pack()


    fen1.mainloop()

# Fonction qui finit le tour, ou effectue la rotation horaire=>trigo au début du tour
def finirtour(lbl,can):
  global nrojoueur,debut
  
  
  if debut==2: #Tour "normal"
  
   nrojoueur =nrojoueur+1
   if nrojoueur ==nbrj:
     nrojoueur = 0

  elif debut ==0: #Première rotation du début (sens horaire)
   nrojoueur =nrojoueur+1
   if nrojoueur ==nbrj:
     debut = 1
     nrojoueur = nbrj-1

  else: #Deuxième rotation du début (sens trigo)
   nrojoueur =nrojoueur-1
   if nrojoueur ==-1:
     debut = 2
     nrojoueur=0
  lbl.configure(text='Tour de ' + joueur[nrojoueur], font = ("Arial",20))
  can.configure(bg=jcouleur[nrojoueur]) 

#------------------------------------------------------------------------------------------------------------------------#
# Procedure principale : fenetre graphique du jeu, (avec résultats en temps réel, non programmé).
def fenetreprincipale():
  global matcons,detest,photode1,photode2,photoregle,couleur0,couleur1,couleur2,couleur3,debut,vol1,vol2
  # Variables des hexagones : rayon, centre de la carte sur le canevas; et ouverture de la fenêtre.
  r = 75
  x0 = 500
  y0 = 495
  rrac = sqrt(3./4.)*r
  princ=Tk()
  
  # Variables couleurs, différentes listes utiles
  
  
  ceau="blue"
  cbois="#006E36"
  cble="yellow"
  ccaillou="#606060"
  cargile="#FF7A00"
  cmouton="green"
  cdesert="white"
  cinterr="white"
  
  lcouleur = listmelange([cdesert,cbois,cbois,cbois,cbois,cble,cble,cble,cble,ccaillou,ccaillou,ccaillou,cargile,cargile,cargile,cmouton,cmouton,cmouton,cmouton])
  idesert  = index("white",lcouleur) #index du désert"
  lnumero  = listmelange([2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12])
  lnumero  = lnumero[:idesert]+(0,) + lnumero[idesert:] # On place un zéro à l'emplacement du désert, celà permet de ne pas placer de numéro dessus.
  lport    = listmelange([cinterr,cinterr,cinterr,cinterr,cbois,cble,cargile,cmouton,ccaillou])
  
  # Liste des centres des hexagones, pour placer les numéros
  lcentre  = [[x0-3*rrac,y0-4.5*r],[x0-rrac,y0-4.5*r]  ,[x0+rrac,y0-4.5*r],[x0+3*rrac,y0-4.5*r]\
  ,           [x0-4*rrac,y0-3*r]  ,[x0-2*rrac,y0-3*r]  ,[x0,y0-3*r]       ,[x0+2*rrac,y0-3*r]  ,[x0+4*rrac,y0-3*r]\
  ,           [x0-5*rrac,y0-1.5*r],[x0-3*rrac,y0-1.5*r],[x0-rrac,y0-1.5*r],[x0+rrac,y0-1.5*r]  ,[x0+3*rrac,y0-1.5*r],[x0+5*rrac,y0-1.5*r]\
  ,           [x0-6*rrac,y0]      ,[x0-4*rrac,y0]       ,[x0-2*rrac,y0]    ,[x0,y0]             ,[x0+2*rrac,y0]      ,[x0+4*rrac,y0],[x0+6*rrac,y0]\
  ,           [x0-5*rrac,y0+1.5*r],[x0-3*rrac,y0+1.5*r] ,[x0-rrac,y0+1.5*r],[x0+rrac,y0+1.5*r] ,[x0+3*rrac,y0+1.5*r],[x0+5*rrac,y0+1.5*r]\
  ,           [x0-4*rrac,y0+3*r]  ,[x0-2*rrac,y0+3*r]   ,[x0,y0+3*r]       ,[x0+2*rrac,y0+3*r] ,[x0+4*rrac,y0+3*r]\
  ,           [x0-3*rrac,y0+4.5*r],[x0-rrac,y0+4.5*r]   ,[x0+rrac,y0+4.5*r],[x0+3*rrac,y0+4.5*r]]
  
  #Liste des intersections triples des hexagones pour placer les colonies et les villes
  linters  = [[x0-2*rrac,y0-4*r],[x0,y0-4*r],[x0+2*rrac,y0-4*r]\
  ,           [x0-3*rrac,y0-3.5*r],[x0-rrac,y0-3.5*r],[x0+rrac,y0-3.5*r],[x0+3*rrac,y0-3.5*r]\
  ,           [x0-3*rrac,y0-2.5*r],[x0-rrac,y0-2.5*r],[x0+rrac,y0-2.5*r],[x0+3*rrac,y0-2.5*r]\
  ,           [x0-4*rrac,y0-2*r],[x0-2*rrac,y0-2*r],[x0,y0-2*r],[x0+2*rrac,y0-2*r],[x0+4*rrac,y0-2*r]\
  ,           [x0-4*rrac,y0-1*r],[x0-2*rrac,y0-1*r],[x0,y0-1*r],[x0+2*rrac,y0-1*r],[x0+4*rrac,y0-1*r]\
  ,           [x0-5*rrac,y0-.5*r],[x0-3*rrac,y0-.5*r],[x0-rrac,y0-.5*r],[x0+rrac,y0-.5*r],[x0+3*rrac,y0-.5*r],[x0+5*rrac,y0-.5*r]\
  ,           [x0-5*rrac,y0+.5*r],[x0-3*rrac,y0+.5*r],[x0-rrac,y0+.5*r],[x0+rrac,y0+.5*r],[x0+3*rrac,y0+.5*r],[x0+5*rrac,y0+.5*r]\
  ,           [x0-4*rrac,y0+1*r],[x0-2*rrac,y0+1*r],[x0,y0+1*r],[x0+2*rrac,y0+1*r],[x0+4*rrac,y0+1*r]\
  ,           [x0-4*rrac,y0+2*r],[x0-2*rrac,y0+2*r],[x0,y0+2*r],[x0+2*rrac,y0+2*r],[x0+4*rrac,y0+2*r]\
  ,           [x0-3*rrac,y0+2.5*r],[x0-rrac,y0+2.5*r],[x0+rrac,y0+2.5*r],[x0+3*rrac,y0+2.5*r]\
  ,           [x0-3*rrac,y0+3.5*r],[x0-rrac,y0+3.5*r],[x0+rrac,y0+3.5*r],[x0+3*rrac,y0+3.5*r]\
  ,           [x0-2*rrac,y0+4*r],[x0,y0+4*r],[x0+2*rrac,y0+4*r]]
  
  #Liste des intersections doubles des hexagones pour placer les routes
  lroute    = [[x0-5./2.*rrac,y0-15./4.*r],[x0-3./2.*rrac,y0-15./4.*r],[x0-1./2.*rrac,y0-15./4.*r],[x0+1./2.*rrac,y0-15./4.*r],[x0+3./2.*rrac,y0-15./4.*r],[x0+5./2.*rrac,y0-15./4.*r]\
  ,           [x0-3*rrac,y0-3*r],[x0-rrac,y0-3*r],[x0+rrac,y0-3*r],[x0+3*rrac,y0-3*r]\
  ,           [x0-7./2.*rrac,y0-9./4.*r],[x0-5./2.*rrac,y0-9./4.*r],[x0-3./2.*rrac,y0-9./4.*r],[x0-1./2.*rrac,y0-9./4.*r],[x0+1./2.*rrac,y0-9./4.*r],[x0+3./2.*rrac,y0-9./4.*r],[x0+5./2.*rrac,y0-9./4.*r],[x0+7./2.*rrac,y0-9./4.*r]\
  ,           [x0-4*rrac,y0-1.5*r],[x0-2*rrac,y0-1.5*r],[x0,y0-1.5*r],[x0+2*rrac,y0-1.5*r],[x0+4*rrac,y0-1.5*r]\
  ,           [x0-9./2.*rrac,y0-3./4.*r],[x0-7./2.*rrac,y0-3./4.*r],[x0-5./2.*rrac,y0-3./4.*r],[x0-3./2.*rrac,y0-3./4.*r],[x0-1./2.*rrac,y0-3./4.*r],\
  [x0+1./2.*rrac,y0-3./4.*r],[x0+3./2.*rrac,y0-3./4.*r],[x0+5./2.*rrac,y0-3./4.*r],[x0+7./2.*rrac,y0-3./4.*r],[x0+9./2.*rrac,y0-3./4.*r]\
  ,           [x0-5*rrac,y0],[x0-3*rrac,y0],[x0-rrac,y0],[x0+rrac,y0],[x0+3*rrac,y0],[x0+5*rrac,y0]\
  ,           [x0-9./2.*rrac,y0+3./4.*r],[x0-7./2.*rrac,y0+3./4.*r],[x0-5./2.*rrac,y0+3./4.*r],[x0-3./2.*rrac,y0+3./4.*r],[x0-1./2.*rrac,y0+3./4.*r],\
  [x0+1./2.*rrac,y0+3./4.*r],[x0+3./2.*rrac,y0+3./4.*r],[x0+5./2.*rrac,y0+3./4.*r],[x0+7./2.*rrac,y0+3./4.*r],[x0+9./2.*rrac,y0+3./4.*r]\
  ,           [x0-4*rrac,y0+1.5*r],[x0-2*rrac,y0+1.5*r],[x0,y0+1.5*r],[x0+2*rrac,y0+1.5*r],[x0+4*rrac,y0+1.5*r]\
  ,           [x0-7./2.*rrac,y0+9./4.*r],[x0-5./2.*rrac,y0+9./4.*r],[x0-3./2.*rrac,y0+9./4.*r],[x0-1./2.*rrac,y0+9./4.*r],[x0+1./2.*rrac,y0+9./4.*r],[x0+3./2.*rrac,y0+9./4.*r],[x0+5./2.*rrac,y0+9./4.*r],[x0+7./2.*rrac,y0+9./4.*r]\
  ,           [x0-3*rrac,y0+3*r],[x0-rrac,y0+3*r],[x0+rrac,y0+3*r],[x0+3*rrac,y0+3*r]\
  ,           [x0-5./2.*rrac,y0+15./4.*r],[x0-3./2.*rrac,y0+15./4.*r],[x0-1./2.*rrac,y0+15./4.*r],[x0+1./2.*rrac,y0+15./4.*r],[x0+3./2.*rrac,y0+15./4.*r],[x0+5./2.*rrac,y0+15./4.*r]]

  # Les 3 listes suivantes regroupes les indices (incrémentés de 1) des routes Haut-droit; Bas-Droit; et Verticales.
  lrouhh    = [1, 3, 5, 11, 13, 15, 17, 24, 26, 28, 30, 32, 41, 43, 45, 47, 49, 56, 58, 60, 62, 68, 70, 72]
  lrouhb    = [2, 4, 6, 12, 14, 16, 18, 25, 27, 29, 31, 33, 40, 42, 44, 46, 48, 55, 57, 59, 61, 67, 69, 71]
  lrouvv    = [7, 8, 9, 10, 19, 20, 21, 22, 23, 34, 35, 36, 37, 38, 39, 42, 50, 51, 52, 53, 63, 64, 65, 66]
  
  
  # Matrice des emplacements de constructions de la carte : -2 ==> rien de construit; -1 : impossible de construire (ce sont des sécurités, qui indiquent des 
  # tuiles maritimes ou tout simplement un élément qui sert à ne pas planter le programme si il recherche trop loin dans la liste.
  # La première case de chaque couple contiendra les dessins de constructions, la 2e case contiendras le numéro du joueur qui a construit à cet emplacement.
  matcons   = [[[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]]\
  ,           [[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]]\
  ,           [[-1,-1],[-2,-2],[-2,-2],[-2,-2],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]]\
  ,           [[-1,-1],[-1,-1],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]]\
  ,           [[-1,-1],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]]\
  ,           [[-1,-1],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]]\
  ,           [[-1,-1],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]]\
  ,           [[-1,-1],[-1,-1],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]]\
  ,           [[-1,-1],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]]\
  ,           [[-1,-1],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]]\
  ,           [[-1,-1],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]]\
  ,           [[-1,-1],[-1,-1],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]]\
  ,           [[-1,-1],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]]\
  ,           [[-1,-1],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]]\
  ,           [[-1,-1],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]]\
  ,           [[-1,-1],[-1,-1],[-1,-1],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]]\
  ,           [[-1,-1],[-1,-1],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]]\
  ,           [[-1,-1],[-1,-1],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]]\
  ,           [[-1,-1],[-1,-1],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]]\
  ,           [[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]]\
  ,           [[-1,-1],[-1,-1],[-1,-1],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]]\
  ,           [[-1,-1],[-1,-1],[-1,-1],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]]\
  ,           [[-1,-1],[-1,-1],[-1,-1],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]]\
  ,           [[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-2,-2],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]]\
  ,           [[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-2,-2],[-2,-2],[-2,-2],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]]\
  ,           [[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]]\
  ,           [[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1],[-1,-1]]]
  # routes entourant la route [n,m] verticale  : [n-2,2*m-1] [n-2,2*m] [n+2,2*m] [n+2,2*m+1]
  # routes entourant la route [n,m] horiz bas  : [n,m-1] [n,m+1] [n-2,m/2] [n+2,m/2]
  # routes entourant la route [n,m] horiz haut : [n,m-1] [n,m+1] [n-2,(m-1)/2] [n+2,(m+1)/2]  
  # routes entourant une colonie [n,m] haut    : [n-2,m-1] [n-2,m] [n+2,m]  
  # routes entourant une colonie [n,m] bas     : [n-2,m] [n+2,m] [n+2,m+1]
  
  # Regroupe les [lignes,colones] de la matrice Matcons qui correspondent à des instersections triples (colonie, ville)
  lintersmatcons = [[1,2],[2,2],[3,2]\
  ,     [1,4],[2,4],[3,4],[4,4]\
  ,     [1,6],[2,6],[3,6],[4,6]\
  ,     [1,8],[2,8],[3,8],[4,8],[5,8]\
  ,     [1,10],[2,10],[3,10],[4,10],[5,10]\
  ,     [1,12],[2,12],[3,12],[4,12],[5,12],[6,12]\
  ,     [1,14],[2,14],[3,14],[4,14],[5,14],[6,14]\
  ,     [2,16],[3,16],[4,16],[5,16],[6,16]\
  ,     [2,18],[3,18],[4,18],[5,18],[6,18]\
  ,     [3,20],[4,20],[5,20],[6,20]\
  ,     [3,22],[4,22],[5,22],[6,22]\
  ,     [4,24],[5,24],[6,24]]
  
  # Regroupe les [lignes,colones] de la matrice Matcons qui correspondent à des instersections doubles (route)
  lroutematcons = [[2,3],[3,3],[4,3],[5,3],[6,3],[7,3]\
  ,     [1,5],[2,5],[3,5],[4,5]\
  ,     [2,7],[3,7],[4,7],[5,7],[6,7],[7,7],[8,7],[9,7]\
  ,     [1,9],[2,9],[3,9],[4,9],[5,9]\
  ,     [2,11],[3,11],[4,11],[5,11],[6,11],[7,11],[8,11],[9,11],[10,11],[11,11]\
  ,     [1,13],[2,13],[3,13],[4,13],[5,13],[6,13]\
  ,     [3,15],[4,15],[5,15],[6,15],[7,15],[8,15],[9,15],[10,15],[11,15],[12,15]\
  ,     [2,17],[3,17],[4,17],[5,17],[6,17]\
  ,     [5,19],[6,19],[7,19],[8,19],[9,19],[10,19],[11,19],[12,19]\
  ,     [3,21],[4,21],[5,21],[6,21]\
  ,     [7,23],[8,23],[9,23],[10,23],[11,23],[12,23]]


  #Liste des images relatives aux dés
  delist=["C:\Users\Dimitri\Documents\Programmation\Python\Colon de Catane\de1.gif","C:\Users\Dimitri\Documents\Programmation\Python\Colon de Catane\de2.gif"\
  ,"C:\Users\Dimitri\Documents\Programmation\Python\Colon de Catane\de3.gif","C:\Users\Dimitri\Documents\Programmation\Python\Colon de Catane\de4.gif",\
  "C:\Users\Dimitri\Documents\Programmation\Python\Colon de Catane\de5.gif","C:\Users\Dimitri\Documents\Programmation\Python\Colon de Catane\de6.gif"]
  
  #Liste qui regroupe presque dans l'ordre les indices des tuiles terrestre dans lcentre (pour trouver le centre du désert et y placer le voleur)
  lliencoulcentre = [31,5,6,7,10,11,12,13,16,17,18,19,20,23,24,25,26,29,30]
  
  # Canevas principal : plateau de jeu
  plateau    = Canvas(princ,width=2*x0,height=2*y0, bg="cyan")
  
  # Lieu de lancement des dé

  dec = Canvas(princ,width=112,height=60)

  i,j = randrange(6),randrange(6)
  photode1   = PhotoImage(file = delist[i])
  item1      = dec.create_image(28,30,image = photode1)
  photode2   = PhotoImage(file = delist[j])
  item2      = dec.create_image(3*28,30,image = photode2)
  de         = Button(princ,text="Lancez les dés",font = ('Arial',11), command = lambda :lancerde(dec,delist,item1,item2))
  
  # Lieu titre affiche le nom et la couleur du joueur actif
  coulnomtour   = Canvas(princ, width=50, height=50,bg=jcouleur[nrojoueur])
  lblnomtour    = Label(princ, text='Tour de ' + joueur[nrojoueur], font = ("Arial",20))
  
  
  # Lieu d'organisation du tour, séries de bouttons et d'étiquettes en relation avec ce qui peut etre fait pendant le tour.
  fin           = Button(princ,text="Fin du tour", font = ('Arial',11), command = lambda : finirtour(lblnomtour,coulnomtour))
  lblordre      = Label(princ, text="Ordre", font = ('Arial',15),borderwidth=10,relief=GROOVE)
  lblressource  = Label(princ, text="1) Ressource", font = ('Arial',15))
  lblcommerce   = Label(princ, text="2) Commerce", font = ('Arial',15))
  lblconstruc   = Label(princ, text="3) Construction", font = ('Arial',15))
  regles        = Button(princ,text="Déplacer le voleur",font = ('Arial',11),command= lambda x=1: depvoleur(x))
  constrroute   = Button(princ,text="Construire une route",font = ('Arial',11), command= lambda x=1: choisircons(x))
  constrcolonie = Button(princ,text="Construire une colonie",font = ('Arial',11), command= lambda x=2:choisircons(x))
  constrville   = Button(princ,text="Construire une ville",font = ('Arial',11), command= lambda x=3:choisircons(x))
  
  
  # Lieu de rappel des coûts de construction
  carte = Canvas(princ,width=270,height=308)
  photo = PhotoImage(file = "C:\Users\Dimitri\Documents\Programmation\Python\Colon de Catane\colons_de_catane_cout.gif")
  item  = carte.create_image(135,154,image=photo)
  
  #Lieu de comptage de la route la plus longue (non programmé)
  lbl6    = Label(princ, text="Route la plus longue")
  j1route = Label(princ, text="2",borderwidth=5,relief=GROOVE,font = ('Arial',11))
  j2route = Label(princ, text="4",borderwidth=5,relief=GROOVE,font = ('Arial',11))
  j3route = Label(princ, text="5",borderwidth=5,relief=GROOVE,font = ('Arial',11))
  j4route = Label(princ, text="1",borderwidth=5,relief=GROOVE,font = ('Arial',11))
  
  #Lieu de comptage de l'armée la plus grande (non programmé)
  lbl7    = Label(princ, text="Armée la plus grande")
  j1armee = Label(princ, text="1",borderwidth=5,relief=GROOVE,font = ('Arial',11))
  j2armee = Label(princ, text="4",borderwidth=5,relief=GROOVE,font = ('Arial',11))
  j3armee = Label(princ, text="3",borderwidth=5,relief=GROOVE,font = ('Arial',11))
  j4armee = Label(princ, text="5",borderwidth=5,relief=GROOVE,font = ('Arial',11))
  
  #Lieu de comptage des points (non programmé)
  lbl8    = Label(princ, text="Totaux")
  j1point = Label(princ, text="1",borderwidth=5,relief=GROOVE,font = ('Arial',11))
  j2point = Label(princ, text="3",borderwidth=5,relief=GROOVE,font = ('Arial',11))
  j3point = Label(princ, text="4",borderwidth=5,relief=GROOVE,font = ('Arial',11))
  j4point = Label(princ, text="2",borderwidth=5,relief=GROOVE,font = ('Arial',11))
  
   
  # Ligne de séparation entre le canevas principal et les options de droite (paske sinon c'est pas joli)
  plateau.create_line(2*x0,0,2*x0,2*y0)


  # Dessin du plateau !!!
  #1e ligne

  hexagone(plateau,lcentre[0][0],lcentre[0][1],r,ceau)
  hexagone(plateau,lcentre[1][0],lcentre[1][1],r,ceau)  
  hexagone(plateau,lcentre[2][0],lcentre[2][1],r,ceau)
  hexagone(plateau,lcentre[3][0],lcentre[3][1],r,ceau)
  
  
  
  #2e ligne
  
  hexagone(plateau,lcentre[4][0],lcentre[4][1],r,ceau)
  hexagone(plateau,lcentre[5][0],lcentre[5][1],r,lcouleur[1])
  hexagone(plateau,lcentre[6][0],lcentre[6][1],r,lcouleur[2])  
  hexagone(plateau,lcentre[7][0],lcentre[7][1],r,lcouleur[3])
  hexagone(plateau,lcentre[8][0],lcentre[8][1],r,ceau)
  
  cercle(plateau,lcentre[5][0],lcentre[5][1],r,lnumero[1])
  cercle(plateau,lcentre[6][0],lcentre[6][1],r,lnumero[2])
  cercle(plateau,lcentre[7][0],lcentre[7][1],r,lnumero[3])
  
  
  
  #3e ligne
  
  hexagone(plateau,lcentre[9][0],lcentre[9][1],r,ceau)
  hexagone(plateau,lcentre[10][0],lcentre[10][1],r,lcouleur[4])
  hexagone(plateau,lcentre[11][0],lcentre[11][1],r,lcouleur[5])  
  hexagone(plateau,lcentre[12][0],lcentre[12][1],r,lcouleur[6])
  hexagone(plateau,lcentre[13][0],lcentre[13][1],r,lcouleur[7])
  hexagone(plateau,lcentre[14][0],lcentre[14][1],r,ceau)
  
  cercle(plateau,lcentre[10][0],lcentre[10][1],r,lnumero[4])
  cercle(plateau,lcentre[11][0],lcentre[11][1],r,lnumero[5])  
  cercle(plateau,lcentre[12][0],lcentre[12][1],r,lnumero[6])
  cercle(plateau,lcentre[13][0],lcentre[13][1],r,lnumero[7])
  
  
  
  
  #4e ligne 
  
  hexagone(plateau,lcentre[15][0],lcentre[15][1],r,ceau)
  hexagone(plateau,lcentre[16][0],lcentre[16][1],r,lcouleur[8])
  hexagone(plateau,lcentre[17][0],lcentre[17][1],r,lcouleur[9])  
  hexagone(plateau,lcentre[18][0],lcentre[18][1],r,lcouleur[10])
  hexagone(plateau,lcentre[19][0],lcentre[19][1],r,lcouleur[11])
  hexagone(plateau,lcentre[20][0],lcentre[20][1],r,lcouleur[12])
  hexagone(plateau,lcentre[21][0],lcentre[21][1],r,ceau)
  
  cercle(plateau,lcentre[16][0],lcentre[16][1],r,lnumero[8])
  cercle(plateau,lcentre[17][0],lcentre[17][1],r,lnumero[9])
  cercle(plateau,lcentre[18][0],lcentre[18][1],r,lnumero[10])
  cercle(plateau,lcentre[19][0],lcentre[19][1],r,lnumero[11])
  cercle(plateau,lcentre[20][0],lcentre[20][1],r,lnumero[12])
  
  
  
  #5e ligne
  
  hexagone(plateau,lcentre[22][0],lcentre[22][1],r,ceau)
  hexagone(plateau,lcentre[23][0],lcentre[23][1],r,lcouleur[13])
  hexagone(plateau,lcentre[24][0],lcentre[24][1],r,lcouleur[14])  
  hexagone(plateau,lcentre[25][0],lcentre[25][1],r,lcouleur[15])
  hexagone(plateau,lcentre[26][0],lcentre[26][1],r,lcouleur[16])
  hexagone(plateau,lcentre[27][0],lcentre[27][1],r,ceau)
  
  cercle(plateau,lcentre[23][0],lcentre[23][1],r,lnumero[13])
  cercle(plateau,lcentre[24][0],lcentre[24][1],r,lnumero[14])  
  cercle(plateau,lcentre[25][0],lcentre[25][1],r,lnumero[15])
  cercle(plateau,lcentre[26][0],lcentre[26][1],r,lnumero[16])
  
  
  
  
  #6e ligne
  
  hexagone(plateau,lcentre[28][0],lcentre[28][1],r,ceau)
  hexagone(plateau,lcentre[29][0],lcentre[29][1],r,lcouleur[17])
  hexagone(plateau,lcentre[30][0],lcentre[30][1],r,lcouleur[18])  
  hexagone(plateau,lcentre[31][0],lcentre[31][1],r,lcouleur[0])
  hexagone(plateau,lcentre[32][0],lcentre[32][1],r,ceau)
  
  cercle(plateau,lcentre[29][0],lcentre[29][1],r,lnumero[17])
  cercle(plateau,lcentre[30][0],lcentre[30][1],r,lnumero[18])
  cercle(plateau,lcentre[31][0],lcentre[31][1],r,lnumero[0])
  
  
  
  
  #7e ligne
  
  hexagone(plateau,lcentre[33][0],lcentre[33][1],r,ceau)
  hexagone(plateau,lcentre[34][0],lcentre[34][1],r,ceau)  
  hexagone(plateau,lcentre[35][0],lcentre[35][1],r,ceau)
  hexagone(plateau,lcentre[36][0],lcentre[36][1],r,ceau)
  
  
  
  # Placement des ports, avec orientation aléatoire
  cercleport(plateau,lcentre[0][0],lcentre[0][1],r,lport[0],1)
  cercleport(plateau,lcentre[2][0],lcentre[2][1],r,lport[1],randrange(2))
  cercleport(plateau,lcentre[9][0],lcentre[9][1],r,lport[8], randrange(2)+1)
  cercleport(plateau,lcentre[22][0],lcentre[22][1],r,lport[7],randrange(2)+2)
  cercleport(plateau,lcentre[33][0],lcentre[33][1],r,lport[6],3)
  cercleport(plateau,lcentre[35][0],lcentre[35][1],r,lport[5],randrange(2)+3)
  cercleport(plateau,lcentre[32][0],lcentre[32][1],r,lport[4],randrange(2)+4)
  cercleport(plateau,lcentre[21][0],lcentre[21][1],r,lport[3],5)
  cercleport(plateau,lcentre[8][0],lcentre[8][1],r,lport[2],randrange(2)+5)
  
  
  
  # Placement initial du voleur sur le désert : on trouve le centre du désert, et on y place le voleur.
  X0,Y0 = lcentre[lliencoulcentre[idesert]][0],lcentre[lliencoulcentre[idesert]][1]
  vol1 = plateau.create_polygon(X0+0.1*r,Y0+0.1*r,X0+0.3*r,Y0+0.4*r,X0-0.3*r,Y0+0.4*r,X0-0.1*r,Y0+0.1*r,fill="black")
  vol2 = plateau.create_oval(X0+0.2*r,Y0+0.25*r,X0-0.2*r,Y0-0.45*r,fill="black")   

  # Lancement de la procedure pointcons en cas de clik sur le plateau de jeu.
  plateau.bind("<Button-1>",lambda event:pointcons(event,plateau,r,rrac,linters,lroute,lrouhh,lrouhb,lrouvv,lcentre,x0,y0,lintersmatcons,lroutematcons,lblnomtour,coulnomtour))
  
  # Placement des objets dans la fenêtre
  plateau.grid(      row =1  ,column =1, rowspan=15)
  coulnomtour.grid(  row =1  ,column =2, padx=10 )
  lblnomtour.grid(   row =1  ,column =3, columnspan=3)
  lblordre.grid(     row =2  ,column =2, rowspan=3)
  lblressource.grid( row =2  ,column =3, columnspan=3)
  lblcommerce.grid(  row =3  ,column =3, columnspan=3)
  lblconstruc.grid(  row =4  ,column =3, columnspan=3)
  regles.grid(       row =5  ,column =2, padx=1, rowspan=3)
  constrroute.grid(  row =5  ,column =3, padx=1,columnspan=2)
  constrcolonie.grid(row =6  ,column =3, padx=1,columnspan=2)
  constrville.grid(  row =7  ,column =3, padx=1,columnspan=2)
  fin.grid(          row =5  ,column =5, padx=5, rowspan=3)
  dec.grid(          row =8  ,column =2, columnspan=3)
  de.grid(           row =8  ,column =5, padx=4)
  carte.grid(        row =9  ,column =2, columnspan=4)
  lbl6.grid(         row =10 ,column =2, columnspan=4)
  j1route.grid(      row =11 ,column =2)
  j2route.grid(      row =11 ,column =3)
  j3route.grid(      row =11 ,column =4)
  j4route.grid(      row =11 ,column =5)
  lbl7.grid(         row =12 ,column =2, columnspan=4)
  j1armee.grid(      row =13 ,column =2)
  j2armee.grid(      row =13 ,column =3)
  j3armee.grid(      row =13 ,column =4)
  j4armee.grid(      row =13 ,column =5)
  lbl8.grid(         row =14 ,column =2, columnspan=4)
  j1point.grid(      row =15 ,column =2)
  j2point.grid(      row =15 ,column =3)
  j3point.grid(      row =15 ,column =4)
  j4point.grid(      row =15 ,column =5)
  
  
  
  
  princ.mainloop()
  
  
  
  


#------------------------------------------------------------------------------------------------------------------------#

#------------------------------------------------------------------------------------------------------------------------#
# Exectution du programme
#------------------------------------------------------------------------------------------------------------------------#

joueur=[]
jcouleur=[]
nbrj = 4
choixclik=-1
choixcons=-1
detest=-1
nrojoueur = 0
debut = 0
consdeb = 0


voleur = 0
introduction()


print "Le nombre de joueur est ",nbrj
for i in range(nbrj):
  print "Le joueur ",i+1," est ",joueur[i]
raw_input()

Regle()
fenetreprincipale()

  
  
  

#------------------------------------------------------------------------------------------------------------------------#
# FIN
#------------------------------------------------------------------------------------------------------------------------#



