#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 21:38:02 2017

@author: al
"""

#Import Packages:
import numpy as np
import os
import pandas as pd

#Funktions:
def Einfugen(wpd, path):
    '''Add a new value to the dictionary.'''
    print('INSTRUCCIONS:')
    print("Per l'estabilitat del diccionari, s'han d'escriure les noves paraules\n"+
        "tal i com s'indica a continuació:\n\tSingular, Plural, Article, Significat, Norma "+
        "per construir el plural, Lliçó\nHa d'anar tot entre comes i amb majúscula la prime"+
        "ra lletra de totes\nles paraules. Prem 'intro' a l'acabar una paraula.\n\n")
    counter = 0
    n = int(input('Quantes en vols afegir? [0,n] '))
    if n != 0:
        while counter < n:
            Worter = input('Endavant:\t')
            while len(Worter.split(',')) != 6:
                print('Format incorrecte, havia de ser: Singular, Plural, Article, Significat, Norma, Lliçó')
                Worter = input()
            wpd.loc[wpd.shape[0]+counter+1] = Worter.replace(', ',',').split(',')
            print('Paraula registrada! '+['','Següent:\t'][counter+1==n])
            counter += 1
        wpd = wpd.sort_values(by='Singular').reset_index(drop=True)
        wpd.to_csv(path, index = False)
    pass

def Runde(wort, losung, aktion, *artikel):
    '''This function defines a round and returns the points obtained. Guessing is penalized
    by -1 points.'''
    if aktion != 'Bedeutung':
        print('Was ist der {} von «{}»?'.format(aktion, wort), end = ' ')
    else:
        print('Was bedeutet «{} {}»?'.format(artikel[0], wort), end = ' ')
    a = 2
    points = 0
    while a != 0:
        auswahl = input().lower()
        print('\t\tDeine Auswahl ist ', end = '')
        if auswahl == losung.lower():
            print('Korrect! :D', end = '\n\n')
            points += 1
            break
        else:
            print('nicht Korrect. ', end = '')
            a -= 1
            points = -0.5
        if a != 0:
            print('Versuchen Sie noch einmal: ', end = '')
    if a == 0:
        print('Der korrect lösung ist: «{}»'.format(losung), end = '\n\n')
        points = -1
    return points
    
def Spiel(wpd, aktion):
    '''This is the function that defines a game. '''

    #Ask for a specific lection or all the lektions
    maximum = wpd['Lektion'].values.max()
    while True:
        lektion = input('Lektion Nummer? (1<=l<={}, oder "Alles"): '.format(maximum))
        try:
            lektion = int(lektion)
            if lektion > 0 and lektion < maximum+1:
                wpd = wpd[wpd['Lektion'] == lektion]
                break
        except:
            if lektion[0].lower() == 'a':
                break
            else:
                print('Falsch Eingabe, versuchen Sie noch einmal.\n')

    #Ask for the number of games:
    while True:
        try:
            n = int(input('N Spiels (1<=n<={}): '.format(len(wpd))))
            if n > 0 and n < len(wpd)+1:
                os.system('clear')
                break
            else:
                print('Das ist keine gültig Zahl (1<=n<={}).'.format(len(wpd)))
        except:
            print('Das ist keine Zahl, Apfelkopf!')
            continue

    #Main part: start with a score of 0 and draw the questions that will be asked.
    #Then, for each round, select the entry and pass it to the "RUNDE" function.
    score = 0
    games = wpd.iloc[np.random.choice(range(len(wpd)), n, replace = False)]
    for i in range(n):
        #Only to display how to write that a word has no plural.
        if i == 0 and aktion == 'p':
            print('Achtung: kein Plural = «-»')
        #Main information of the round.
        print('Spiel {}/{}.'.format(i+1,n), end = '\t')
        entry = games.iloc[i]
        if aktion == 'a':
            points = Runde(entry['Singular'], entry['Artikel'], 'Artikel')
        elif aktion == 'p':
            points = Runde(entry['Singular'], entry['Plural'], 'Plural')
        else:
            points = Runde(entry['Singular'], entry['Bedeutung'], 'Bedeutung',
                           entry['Artikel'])
        score += points

    #Print the obtained points:
    score = [0, score][score > 0]
    print('Punktestand: {}/{} ({}%)'.format(score,n,round(score/n*100,2)))
    if score == 0:
        print('Studier JETZT GLEICH, bitte <3', end = '\n\n')
    pass

def Worterbuch(wpd, aktion):
    '''This function displays the dictionary built so far.'''

    #If we are searching for a word, it takes the input and try to find the word in german first.
    #IF the word is not found, it must have been written in Catalan. If that also fails, the word
    #is not in the dictionary. If we want the whole dictionary, it goes printing and 10 words at
    #a time until it is finished (by pressing space) or until the user writes "exit" or "e" in any
    #possible variant.
    template = '{:^7} | {:^7} | {:^15} | {:^15}'
    if aktion == 's':
        Wort = input('Schreiben die Wort bitte [DE oder CAT]: ').capitalize()
        data = wpd.loc[wpd.Singular == Wort].values
        if data.size==0:
            try:
                data = wpd.loc[wpd.Bedeutung == Wort].values[0]
            except:
                print('\n[ ! ] Das Wort ist in die Worterbuch nicht. [ ! ]\n')
                return
        else:
            data = data[0]
        print()
        print(template.format('Artikel','Plural','Wort','Bedeutung'))
        print('='*54)
        print(template.format(data[2], data[-2], data[0], data[-3]))
    else:
        print(template.format('Artikel','Plural','Wort','Bedeutung'))
        print('='*54)
        for i in range(wpd.shape[0]):
            data = wpd.loc[i].values
            print(template.format(data[2], data[-2], data[0], data[-3]))
            if not (i+1)%10:
                more = input().lower()
                if 'e' in more:
                    break
    print()
    pass


def HauptFunktion():
    '''This is the principal function that manages the menu options and the game
    in general. It needs to import the dictionary properly first.'''
    #Check if the dictionary could be imported and ask the path until it succeeds.
    path = 'worter.csv'
    while True:
        try:
            wpd = pd.read_csv(path)
            break
        except:
            path = input('Schreiben Sie die absolut Adresse von "worter.csv" bitte: \t')
    
    #Main menu:
    while True:
        aktion = input('Schreiben Sie: S - Spielen |  W - Wörterbuch | E - Einfügen | V - Verlassen.\t'
			'Auswahl: ').lower()
        print()
        try:
            aktion = aktion[0]
        except:
            continue
        if aktion == 'v':
            break
        elif aktion in ['s', 'w', 'e']:
            #Spielen!
            if aktion == 's':
                while True:
                    aktion2 = input('Schreiben Sie: A - Artikel | P - Plural | '
                                    'B - Bedeutung | Z - Zurück\tAuswahl: ').lower()[0]
                    print()
                    if aktion2 in ['a', 'p', 'b']:
                        Spiel(wpd, aktion2)
                        break
                    elif aktion2 == 'z':
                        break
                    else:
                        print('Falsch Eingabe, versuchen Sie noch einmal.\n')
            #Worterbuch!
            elif aktion == 'w':
                while True:
                    aktion2 = input('Schreiben Sie: S - Suchen | A - Anzeigen | Z - Zurück\tAuswahl: ').lower()
                    try:
                        aktion2 = aktion2[0]
                    except:
                        continue
                    print()
                    if aktion2 in ['s', 'a']:
                        Worterbuch(wpd, aktion2)
                        break
                    elif aktion2 == 'z':
                        break
                    else:
                        print('Falsch Eingabe, versuchen Sie noch einmal.\n')
            else:
                Einfugen(wpd, path)
                wpd = pd.read_csv(path)
        else:
            print('Falsch Eingabe, versuchen Sie noch einmal.\n')

#Play!
if __name__ == "__main__":
    HauptFunktion()    
