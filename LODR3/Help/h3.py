
class classA:

    def __init__(self):
        self.thingy = 'A Thingy'
        self.b = classB(self)


class classB:

    def __init__(self, master):
        self.master = master

    def printMasterThingy(self):
        print self.master.thingy





if __name__ == '__main__':

    ca = classA()

    ca.b.printMasterThingy()
