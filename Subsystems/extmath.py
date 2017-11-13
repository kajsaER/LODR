#!/usr/bin/python

prefixLarge = ['', 'k', 'M', 'G', 'T', 'P', 'E']
prefixMedium = ['', 'd', 'c']
prefixSmall = ['', 'm', u'\u03bc', 'n', 'p', 'f', 'a']

def sinminus(sa, ca, sb, cb): # sin(a-b)
    return cb*sa - ca*sb

def sinplus(sa, ca, sb, cb): # sin(a+b)
    return sa*cb + ca*sb

def cosminus(sa, ca, sb, cb): # cos(a-b)
    return cb*ca + sb*sa

def cosplus(sa, ca, sb, cb): # cos(a+b)
    return ca*cb - sa*sb

def myfloat(item):
    if item == None:
        return item
    else:
        return float(item)

def prefixedValue(item, useDeci=False, useDeca=False, useHecto=False):
    number = myfloat(item)
    pref = 0
    pot = 0
    if number >=1000:
        Prefix = prefixLarge
        while number >= 1000 and pref < len(Prefix)-1:
            number = number/1000
            pref = pref+1
            pot = pot+3
    elif number >= 100 and useHecto:
        Prefix = ['h']
        number = number/100
        pot = 2
    elif number >= 10 and useDeca:
        Prefix = ['da']
        number = number/10
        pot = 1
    elif number >= 0.01 and useDeci:
        Prefix = prefixMedium
        while number < 1 and pref < len(Prefix)-1:
            number = number*10
            pref = pref+1
            pot = pot-1
    else:
        Prefix = prefixSmall
        while number < 1 and pref < len(Prefix)-1:
            number = number*1000
            pref = pref+1
            pot = pot-3
    return [Prefix[pref], number, pot]
