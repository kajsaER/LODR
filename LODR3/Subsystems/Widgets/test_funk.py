import math as m
import sys, termios, tty, os, time

prefixes =   {-18:'a', -15:'f', -12:'p', -9:'n',    # Prefixes for displaying the value
            -6:'\u03bc', -3:'m', #-2:'c', -1:'d',
            +0:'', #+1:'da', +2:'h', 
            +3:'k', +6:'M', +9:'G', +12:'T', +15:'P', +18:'E'}

Prefixes =   {1e-18:'a', 1e-15:'f', 1e-12:'p', 1e-9:'n',    # Prefixes for displaying the value
            1e-6:'\u03bc', 1e-3:'m', #1e-2:'c', 1e-1:'d',
            1e+0:'', #1e+1:'da', 1e+2:'h', 
            1e+3:'k', 1e+6:'M', 1e+9:'G', 1e+12:'T', 1e+15:'P', 1e+18:'E'}

def getch():                    # Get character from keyboard without waiting for enter
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def calcy():                        # Convert from x integer to y value for display
    print("x: " + repr(x))
    exp2 = 3*((x/resolution) // 1e+3) + exp0    # integer division
    yp2 = round((x/resolution)%(1e+3), digits)  # remainder
    y2 = round(yp2 * m.pow(10, exp2), int(digits-exp2))
    print("y: " + repr(y2) + "   equal to " + repr(yp2) + str(prefixes[exp2]) + "J\n")

    if x < (1e+3 * resolution - 1):
        print("below")
        r = 0
        exp2 = exp0
        z = round((x+1)/resolution, digits)
    else:
        print("above")
        n = round((1e+3 - 1) * resolution)
        x2 = round(x - (1e+3 * resolution - 1))
        r = x2 // n + 1
        z = round((x2 % n)/resolution + 1, digits)
        exp2 = exp0 + r * 3
    print("r: " + repr(r) + "   z: " + repr(z))
    print("z*: " + repr(z) + str(prefixes[exp2]) + "J\n")

button_delay = 0.1

y = float(input("Give starting value:"))    # Choose a value to start from

exp0 = -9                                     # Exponent of minimum range [nJ]
digits = 1                                  # Number of decimals to be used
resolution = m.pow(10, 1)                   # The number of points for a change of size 1

exp = exp0                                     # Exponent of y
yp = y                                      # Short number of y
print("yp: " + repr(yp) + "   exp: " + repr(exp) + "   y*: " + repr(yp*10**(-exp)))
while (yp*10**(-exp)) < 1/resolution:                    # While the number is not in the prefixed unit
    yp = yp*1e+03                           # Multiply yp by 1000 (10³)
    exp += 3                                # Exponent increases by 3
    print("yp: " + repr(yp) + "   exp: " + repr(exp))

yp = round(y * m.pow(10, -exp), digits)     # The display value 
#x = int((yp + (exp - exp0)/3 * 1e+3) * resolution)   # Integer value representing the silder value

if exp == exp0:
    x90 = yp*resolution - 1
else:
    zp = (yp - 1)*resolution
    r = (exp - exp0)/3
    z = (r-1)*((1000-1)*resolution) + zp
    x90 = z + (1000*resolution - 1)
x = x90
print("x90: " + repr(x90))

calcy()                                     # Calculate y from x integer

while True:
    char = getch()

    if char == 'q':
        exit(0)
    elif char == '+':
        x += 1
        calcy()
        time.sleep(button_delay)
    elif char == '-':
        x -= 1
        calcy()
        time.sleep(button_delay)
    elif char == 'x':
        x = int(input("Give new x: "))
        calcy()
    else:
        print(char)
        time.sleep(button_delay)
