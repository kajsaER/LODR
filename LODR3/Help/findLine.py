import matplotlib.pyplot as plt

f, ax = plt.subplots()
ax.axis('equal')
dot = ax.plot(8, 8, 'o')
print(dot[0])
try:
    print(ax.lines.index(dot[0]))
except ValueError:
    print(repr(dot) + " not found in " + repr(ax.lines))
