#!/usr/bin/python
allPrefixes = {'a':'1E-18', 'f':'1E-15', 'p':'1E-12', 'n':'1E-09',
                u'\u03bc':'1E-06', 'm':'1E-03', 'c':'1E-02', 'd':'1E-01',
                'da':'1E+01', 'h':'1E+02', 'k':'1E+03', 'M':'1E+06',
                'G':'1E+09', 'T':'1E+12', 'P':'1E+15', 'E':'1E+18'}
allPot =   {'1E-18':'a', '1E-15':'f', '1E-12':'p', '1E-09':'n',
            '1E-06':u'\u03bc', '1E-03':'m', '1E-02':'c', '1E-01':'d',
            '1E+01':'da', '1E+02':'h', '1E+03':'k', '1E+06':'M',
            '1E+09':'G', '1E+12':'T', '1E+15':'P', '1E+18':'E'}
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
    elif number == 0.0:
        Prefix = ['']
        pot = 0
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
