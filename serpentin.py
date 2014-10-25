import random


#Configuration
nbr_eleves = 33
nbr_5dem = 2

start_dayN = 0 #Numero du jour: 0 = Lundi, etc.
start_day = 2 #numero du jour de depart, -1
start_month = 2 #numero du mois de depart

#Taille classe
colonnes = 8 #id: 0 a 8
colonnes_passage = 1

Days = ['LUNDI','MARDI','MERCREDI','JEUDI','VENDREDI','SAMEDI','DIMANCHE']
JoursParMois = [31,28,31,30,31,30,31,31,30,31,30,31]

Liste_serpentins = [] #liste de tableaux 2D (X,Y)


#   (0,0)   (1,0)  
#   (1,0)   (1,1)


def SerpentinToday(jour,mois):
    #Pas de travail le DIMANCHE
    if jour==6 or jour==3 or jour==4:
        return False
    return True
    #ajouter vacances + jours feries

def RenderCalendar(nbr):
    nbr_modulo = nbr_eleves-nbr_5dem
    i=0
    N=0 #la variable pour le +/- quotidien
    WeekNbr = 10
    while i <= nbr:
        Mois_blc = start_month #Mois dans la boucle, a la ieme iteration. Commence a 0
        total_jours = JoursParMois[Mois_blc]
        while i+start_day>=total_jours:
            Mois_blc+=1
            total_jours+=JoursParMois[Mois_blc]
        Jour_blc = (start_day+i-total_jours)%JoursParMois[start_month+Mois_blc] #Notre jour dans la boucle, a la ieme iteration. Commence a 0
 
            
        if SerpentinToday(start_dayN+i%7,Mois_blc):
            if start_dayN+i%7==0:
                print "Semaine",WeekNbr+(start_day+i)//7
            print '+%i/-%i %s %i/%i' %(N%nbr_modulo,(nbr_modulo-N)%nbr_modulo,Days[start_dayN+i%7],Jour_blc+1,Mois_blc+1)
            N+=1
        i+=1

def isPlace5dem(x,y):
    if (x==2 and y==0) or (x==3 and y==0):
        return True
    return False

def RenderPlan(): #Fonction qui va attribuer au hasard les numeros du serpentin
    to_distrib = [i for i in range(1,nbr_eleves-nbr_5dem)] #La 31e place est mise manuellement, a la fin
    Plan = []*colonnes #-1 = 5dem
    for y in range(4):
        Ligne_X=[]
        for x in range(colonnes):
            if(isPlace5dem(x,y)):
                Ligne_X.append(-1)
            else:
                Ligne_X.append(to_distrib.pop(random.randrange(len(to_distrib))))
        Plan.append(Ligne_X)

    #Enfin, on ajoute le 31 manuellement:
    Plan.append([0,0,0,31,0,0,0,0])
    return Plan
    

def PrintPlan(plan):
    for l in plan:
        print ""
        for m in l:
            print m,'\t',
    print ''

def savePlan(plan,score):
    fic = open("bestPlan.txt", "w") # Ouvre le fichier
    
    for l in plan:
        fic.write("\n")
        ligne=""
        for m in l:
            ligne+=str(m)
            ligne+='\t'
        fic.write(ligne)
    fic.write("\n")
    fic.write(str(score))
    fic.close()


def GenerateItin(plan):
    #pour un plan donne, retourne les X,Y du 1,2,3,4,5,6 etc.
    itineraire = []
    for i in range(nbr_eleves-nbr_5dem):
        for id_y in range(len(plan)):
            for id_x in range(len(plan[id_y])):
                if plan[id_y][id_x]==i+1:
                    itineraire.append([id_x,id_y])
                    break
                    break
    return itineraire

def valeurRangee(rangee):
    if rangee==0:
        return 20
    elif rangee==1:
        return 15
    elif rangee==2:
        return 10
    elif rangee==3:
        return 5
    else:
        return 0

def valeurColonne(rangee):
    if rangee==0:
        return 35
    elif rangee==1:
        return 30
    elif rangee==2:
        return 25
    elif rangee==3:
        return 20
    elif rangee==4:
        return 15
    elif rangee==5:
        return 10
    elif rangee==6:
        return 5
    else:
        return 0

def CalculAvtArriere(itineraire):
    #Retourne le score d'un plan quant à sa capacite à alterner entre avant et
    #arriere

    #Ici, on considere uniquement les Y
    #Rangee 1: 20
    #Rangee 2: 15
    #Rangee 3: 10
    #Rangee 4: 5
    #Rangee 5: 0

    #donc si on fait: abs(Rangee(N-1)-Rangee(N)) on a un nombre élevé si alterne bien
    score=0
    for i in range(1,31):
        score+=abs(valeurRangee(itineraire[i-1][1])-valeurRangee(itineraire[i][1]))
    return score

def CalculDroiteGauche(itineraire):
    #idem que la fonction pcdte
    score=0
    for i in range(1,31):
        score+=abs(valeurColonne(itineraire[i-1][0])-valeurColonne(itineraire[i][0]))
    return score


#Maintenant, place a la generation du serpentin

def ComputeScore(itineraire):
    return .8*CalculAvtArriere(itineraire)+.2*CalculDroiteGauche(itineraire)


lastscore=0
i=0
while 1<3:
    i+=1
    plan=RenderPlan()
    init=GenerateItin(plan)
    score=ComputeScore(init)
    if score>lastscore:
        print "BEST: Essai - Score:",i,score
        lastscore=score
        savePlan(plan,score)



RenderCalendar(40)



#On va generer X serpentins et garder celui qui a le plus gros score


#Calcul de score:
#Alterner AVANT, ARRIERE -> coef .70
#Alterner DROITE GAUCHE -> coef .30
#Maximiser les rencontres -> coef 0 -> J'ignore.

#Si on resonne en terme de moyenne, sur une rotation de 31, tout est ok, car on va faire toutes les places, donc "juste".
#Il faut donc eviter les "successions": Tp svt devant; puis tp svt derriere, etc.
#Il faut donc calculer une distance !

#Parcourir de 1 a 31 l'écart pour chaque increment, le serpentin ayant le maxi increment win.

