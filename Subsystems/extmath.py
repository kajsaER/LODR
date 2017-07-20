#!/usr/bin/python

def sinminus(sa, ca, sb, cb): # sin(a-b)
    return cb*sa - ca*sb

def sinplus(sa, ca, sb, cb): # sin(a+b)
    return sa*cb + ca*sb

def cosminus(sa, ca, sb, cb): # cos(a-b)
    return cb*ca + sb*sa

def cosplus(sa, ca, sb, cb): # cos(a+b)
    return ca*cb - sa*sb

