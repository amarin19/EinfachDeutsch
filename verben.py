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
    print("Per l'estabilitat del diccionari, s'han d'escriure els nous verbs\n"+
        "tal i com s'indica a continuació:\n\tSignificat, Infinitiu en majúscules, ich, du, er, wir, ihr, sie, "+
        "Lliçó\nHa d'anar tot entre comes. Prem 'intro' a l'acabar un input.\n\n")
    counter = 0
    n = int(input('Quants en vols afegir? [0,n] '))
    if n != 0:
        while counter < n:
            Worter = input('Endavant:\t')
            while len(Worter.split(',')) != 9:
                print('Format incorrecte, havia de ser: Significat, Infinitiu en majúscules, ich, du, er, wir, ihr, sie, Lliçó ')
                Worter = input()
            wpd.loc[wpd.shape[0]+counter+1] = Worter.replace(', ',',').split(',')
            print('Verb registrat! '+['','Següent:\t'][counter+1==n])
            counter += 1
        wpd = wpd.sort_values(by='Infinitiv').reset_index(drop=True)            
        wpd.to_csv(path, index = False)
    pass


def Matrix(wpd, games, n, antwort, *Punktestand):
    '''This function defines a round and returns the points obtained. Guessing is penalized
    by -1 points.'''
    #Fancy matrix print:
    if Punktestand:
        print("="*16*(1+n))
        print(' {:^13} '.format(''), end = '')
        for i in Punktestand[0]:
            print('| {:^13} '.format(str(i)), end = '')
        print()
    else:
        print(' {:^13} '.format('Bedeutung'),end='')
        for i in games.T[0]:
            print('| {:^13} '.format(i),end='')
        print('\n {:^13} '.format('Verben'),end='')
        for i in games.T[1]:
            print('| {:^13} '.format(i),end='')
        print()
        print("="*16*(1+n))
        aux = 0
        for i in wpd.columns.values[2:-1]:
            print(' {:^13} '.format(i), end ='')
            for col in range(antwort.shape[0]):
                if antwort[col][aux] != 0:
                    print('| {:^13} '.format(antwort[col][aux]), end = '')
                else:
                    print('| {:13} '.format(''), end = '')
            print()
            aux += 1


def Spiel(wpd, n = 0):
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
    if n == 0:
        while True:
            try:
                n = int(input('N Spiels (1<=n<=5): '.format(len(wpd))))
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
    score = []
    games = wpd.iloc[np.random.choice(range(len(wpd)), n, replace = False)].values
    konjugation = np.zeros((n, 6),dtype=np.object)
    Matrix(wpd, games, n, konjugation)

    for i in range(n):
        #Main information of the round.
        print()
        antwort = input('Verben: {}. Konjugation:\n\t'.format(games.T[1][i])).replace(', ',',').split(',')
        konjugation[i] = antwort
        os.system('clear')
        Matrix(wpd, games, n, konjugation)
        points = 0
        for person in range(6):
            if games[i][2+person] == antwort[person]:
                points += 1
        score.append(round(points/.6,2))

    #Print the obtained points:
    Matrix(wpd, games, n, konjugation, score)
    print()
    Matrix(wpd, games, n, games.T[2:].T)
    print()
    pass

def Worterbuch(wpd, aktion):
    '''This function displays the dictionary built so far.'''

    #If we are searching for a word, it takes the input and try to find the word in german first.
    #IF the word is not found, it must have been written in Catalan. If that also fails, the word
    #is not in the dictionary. If we want the whole dictionary, it goes printing and 10 words at
    #a time until it is finished (by pressing space) or until the user writes "exit" or "e" in any
    #possible variant.

    '''PENDENT DE REESCRIURE.
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
    print()'''
    pass


def HauptFunktion():
    '''This is the principal function that manages the menu options and the game
    in general. It needs to import the dictionary properly first.'''
    #Check if the dictionary could be imported and ask the path until it succeeds.
    path = 'verben.csv'
    while True:
        try:
            wpd = pd.read_csv(path)
            break
        except:
            path = input('Schreiben Sie die absolut Adresse von "verben.csv" bitte: \t')
    
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
                Spiel(wpd)
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
