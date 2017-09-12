#! /usr/bin/python3

import os

def find_index(tab,x):
    """
    Dichotomic search to find the closest element to x in a given list
    
    Args:
        tab (list): probabilties of value increase for each currency
        x (float): number to search for 
    
    Returns:
        int: index of element closest to x in the list

    """
    #dichotomie
    if len(tab) == 0 :
        return 0
    if x <= tab[0][0]:
        return 0
    if x >= tab[-1][0]:
        return len(tab)
    a = 0
    c = 0
    b = len(tab) - 1
    while b-a > 1:
        c = int((a+b)/2)
        if x < tab[c][0]:
            b = c
        else:
            a = c
    return b
