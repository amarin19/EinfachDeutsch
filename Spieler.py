#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 21:38:02 2017

@author: al
"""

#Import Packages:
import os

#Play!
if __name__ == "__main__":
    print('\n\n'+'#'*44+'\n#'+' '*42+'#')
    print('#  Wilkommen zu die Deutsche Lernen script #\n#     Albert Marin (c) Copyright 2018      #')
    print('#'+' '*42+'#\n'+'#'*44+'\n')

    while True:
        a = input('Sag mal. Ich möchte [W]örter - [V]erben - [A]djective üben (oder [E]xit): ')[0].lower()
        if a in ['w','v','a','e']:
            if a == 'w':
                os.system('./worter.py')
            elif a == 'v':
                os.system('./verben.py')
            elif a == 'a':
                os.system('./adj_adv.py')
            else:
                break
        else:
            print('Falsch Eingabe, versuchen Sie noch einmal.\n')
    print('Okay, bis später! :)\nAlbert Marin (c) Copyright 2018')
    