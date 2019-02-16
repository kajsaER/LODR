import numpy as np
from Subsystems import *

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from configparser import SafeConfigParser as SCP
import sys, os
import time, threading
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.patches import Circle as Circle
from matplotlib.figure import Figure


qtCreatorMain = "Subsystems/ui_Files/GUI.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorMain)

# Define standard states
skipThis = 00           # Skip only current item
renameThis = 0o1        # Rename only current item
replaceThis = 0o2       # Replace only current item
skipAll = 10            # Skip all items
renameAll = 11          # Rename all items
replaceAll = 12         # Replace all items


class OperatorGUI(QtWidgets.QMainWindow, Ui_MainWindow):    # Main GUI
    killed = QtCore.pyqtSignal()    # Initiate a signal called killed

    def __init__(self, parent=None):
        super(OperatorGUI, self).__init__(parent)
        self.setupUi(self)
        self.filefolder = os.getcwd()   # Get current working directory
        self.formats = list()           # Make an empty list and fill it with custom file formats
        for string in ['LODR Files (*.lodr)','Debris Files (*.dcfg)',
                       'Laser Files (*.lcfg)','Orbit Files (*.ocfg)',
                       'All Files (*)']:
            self.formats.append(string) 
        
        # Setup open and save dialog windows
        self.openDiag = QtWidgets.QFileDialog(self.central_widget)
        self.openDiag.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        self.openDiag.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        
        self.saveDiag = QtWidgets.QFileDialog(self.central_widget)
        self.saveDiag.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
        self.saveDiag.filterSelected.connect(self.updateSuffix)

        # Make a dictionry for default values and ranges of lasers
        dl = dict.fromkeys(['Power', 'Energy', 'Lambda', 'M2', 'Cd',
                            'Repetition rate', 'Pulse duration'])
        dl.update({'Energy min':'1E-09', 'Energy max':'1E+03', 'M2 min':'1', 'M2 max':'1E+02',
            'Cd min':'1', 'Cd max':'1E+01',
            'Repetition rate min':'1E+00', 'Repetition rate max':'1E+11',
            'Pulse duration min':'1E-15', 'Pulse duration max':'1E+00',
            'Fire duration':'1E+00', 'Fire duration min':'1E-06', 'Fire duration max':'1E+01'})
        # Make a SafeConfigParser for lasers, using the default values from dl
        self.laserConf = SCP(dl, allow_no_value=True, delimiters=('='))
        
        # Make a SafeConfigParser for debris, and add a section called ORBITS
        self.debrisConf = SCP(allow_no_value=False, delimiters=('='))
        self.debrisConf.add_section("ORBITS")
        self.debrisConf.optionxform = str   # Making the SCP case sensitive

        #Make a SafeConfigParser for orbits
        self.orbitConf = SCP(allow_no_value=True, delimiters=('='))
        # Using only '=' as a delimiter allows for storing dictionaries and specific laser names

        self.atmosphere = atmosphere()  # Initiate atmosphere object

        # File Menu
        self.actionOpen_file.triggered.connect(self.open_file)
        self.actionSave_file.triggered.connect(self.save_file)
        self.actionClose.triggered.connect(self.close_application)

        # Edit Menu
        self.actionLoad_Debris.triggered.connect(self.load_debris)
        self.actionAdd_Debris.triggered.connect(self.add_debris)
        self.actionRemove_Debris.triggered.connect(self.remove_debris)
        self.actionSave_Debris.triggered.connect(self.save_debris)
        
        self.actionLoad_Lasers.triggered.connect(self.load_laser)
        self.actionAdd_Laser.triggered.connect(self.add_laser)
        self.actionRemove_Laser.triggered.connect(self.remove_laser)
        self.actionSave_Laser.triggered.connect(self.save_laser)

        self.actionLoad_Orbits.triggered.connect(self.load_orbit)
        self.actionAdd_Orbits.triggered.connect(self.add_orbit)
        self.actionRemove_Orbits.triggered.connect(self.remove_orbit)
        self.actionSave_Orbits.triggered.connect(self.save_orbit)

        # Run Menu, disabled but can be enabled when more functionallity is added
        # A simple button is used for now
        self.menuRun.menuAction().setVisible(False)
        self.running = False
        self.kill_reason = None     # Message to show when run thread is killed from within
        self.time_step = 240        # Time resolution, nbr of steps to move the debris between measurements
        self.lock = threading.Lock()   
        self.killed.connect(self.on_killed, QtCore.Qt.QueuedConnection) # Connecting custom killed signal to action

        # Laser Widget
        self.laserType.activated[str].connect(self.laser_choice)    # Connect laser choice box to function
        self.laser_type_list = ['Choose']   # Make a list of laser types, make first element an instruction to choose
        
        self.lasersystem = laser()      # Initiate laser object
        self.laserwidget.setLayout(QtWidgets.QVBoxLayout()) # Set layout for laser widget
        self.laserstack = QtWidgets.QStackedWidget()        # So I can stack the different types
        self.laserwidget.layout().addWidget(self.laserstack)
        self.laserEmpty = Laser_Widget(self)                # Empty type
        self.laserDef = DefinedLaser(self)                  # Predefined type
        self.laserUndef = UndefinedLaser(self)              # Undefined type
        self.laserstack.addWidget(self.laserEmpty)          # Add them to the stack
        self.laserstack.addWidget(self.laserDef)
        self.laserstack.addWidget(self.laserUndef)

        # Antenna
        self.antenna = antenna(0,0)     # Initiate antenna object with Diameter and usage ratio both 0
        self.antennaD.setValidator(QtGui.QDoubleValidator())    # Requiere double values
        self.antennaD.editingFinished.connect(lambda: self.antenna.set_D(self.antennaD.text())) # Connect to function
        self.antennaEff.valueChanged.connect(lambda value: self.antenna.set_ratio(
            float(self.antennaEff.value()/100)))

        # Debris
        self.debris = None          # No debris chosen
        self.debris_list = []       # Initiate empty debris list, stores debris objects
        self.objectNbr.valueChanged.connect(self.change_debris)
        
        # Position

        # Orbit
        self.orbit_list = []        # Empty list for storing orbit objects
        
        # Buttons
        # Connect buttons to functions and short keys
#        app.aboutToQuit.connect(self.close_application)
        self.closeBtn.clicked.connect(self.close_application)
        self.closeBtn.setShortcut(QtGui.QKeySequence.Quit)  # Doesn't work since system update
        self.closeBtn.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_W)) # Added this to solve
        self.runBtn.clicked.connect(self.run_pushed)
        self.runBtn.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_R))
        self.resetBtn.clicked.connect(self.reset_debris)
#        self.resetBtn.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_R)) Potential short key for resetting orbit
        self.WholePlotBtn.clicked.connect(self.show_whole_plot)
        self.EmptyPlotBtn.clicked.connect(self.empty_plot)

        # PlotView
        bgcolor =  np.asarray(self.palette().color(self.backgroundRole()).getRgb()[0:3])/255    # Get the bg color of the GUI
        self.figure = Figure(tight_layout=True, facecolor=bgcolor)  # Make a figure object with the same bg color
#        self.figure.suptitle('Title', fontsize=15, y=0.995)
        self.canvas = FigureCanvas(self.figure)                     # Make a canvas for the figure
        self.toolbar = NavigationToolbar(self.canvas, self)         # Make a toolbar
        self.plotLayout.addWidget(self.toolbar)                     # Add them to the layout
        self.plotLayout.addWidget(self.canvas)
        self.graph = self.figure.add_subplot(111)                   # Add a graph to plot in
        self.empty_plot()                                           # Run function to show start image
        
################## End of main window init code #####################
     
    # Debris functions #
    def load_debris(self, filename=False, scp=False):   # Load debris data from a file
        if scp != False:                # If an SCP is provided, use it
            debrisConfTemp = scp
        else:                           # If no SCP is provided
            if filename == False:       # If no filename is provided
                filename = self.get_filename(formats=["Debris Files (*.dcfg)"]) # Open dialog to open debris file
            if filename == None:        # If no file was chosen
                debrisConfTemp = None   # Temporary SCP is None
            else:                       # If a file was chosen, make a new SCP and read the file into it
                debrisConfTemp = SCP(allow_no_value=True, delimiters=('='))
                debrisConfTemp.optionxform = str
                debrisConfTemp.read(str(filename))
        if debrisConfTemp != None:      # If the temporary SCP isn't None
            orbitdict = dict(debrisConfTemp.items("ORBITS"))    # Get the orbits from the file
            orbitscp = self.dict2scp(orbitdict)     # Make an SCP of the orbits
            self.load_orbit(scp=orbitscp)   # Load the orbits
            debrisConfTemp.remove_section("ORBITS") # Remove the orbit section from the SCP, leaving only the debris
            Debris = debrisConfTemp.sections()      # Get the id:s of all debris in the SCP
            for deb in Debris:          # For each peice of debris
                d = dict(debrisConfTemp.items(deb)) # Make an dictionary
                orbname = d.get("orbit")            # Get the name of the used orbit
                o = set(orbitscp.items(orbname))        # Make a set of the orbit from local SCP
                O = set(self.orbitConf.items(orbname))  # Make a set of the orbit from "global" SCP
                if len(o & O) < 3:      # Compare the 2 sets, if they differ
                    for orbname in self.orbitConf.sections():   # Check if any other orbit in the global SCP
                        O = set(self.orbitConf.items(orbname))  # is the same as the local one
                        if len(o & O) == 3:     # If match is found
                            break               # Stop looking
                if len(o & O) < 3:              # If no match was found
                    choice = NoMatch(d.get("orbit")).exec_()    # Ask user what to do
                    if choice == QtWidgets.QMessageBox.RejectRole:      # Use stored orbit parameters
                        pass                                    # O = O
                    elif choice == QtWidgets.QMessageBox.ActionRole:    # Rename the new orbit
                        orbname = d.get("orbit")
                        name = orbname
                        while orbname in self.orbit_list:   # While name is a duplicate, ask for a new one
                            orbname = str(QtWidgets.QInputDialog.getText(self.central_widget,
                                      "Rename Orbit", "Name")[0])
                        if len(orbname) < 1:   # No new name given => use stored orbit
                            orbname = name
                        else:
                            O = set(orbitscp.items(name))           # O = o
                            self.insert_orbit(orbname, dict(O))     # Put in Conf and list
                o = dict(O)
                orb = orbit()       # Make a new orbit object with chosen parameters
                orb.make(float(o.get("rp")), float(o.get("epsilon")), float(o.get("omega")))
                debname = (str(hex(int(float(d.get("mass")) + float(d.get("size")) + 
                           float(d.get("Cm"))*float(d.get("etac")) +
                           360/math.pi*float(d.get("nu"))))) + orbname) # Make ID for debris
                extra = 0
                n0 = debname
                while self.debrisConf.has_section(debname): # While the ID isn't unique add a number to the end
                    debname = n0 + str(extra)
                    extra += 1
                Deb = debris(str(debname), float(d.get("etac")), float(d.get("Cm")),    # Make new debris object
                             float(d.get("size")), float(d.get("mass")), float(d.get("nu")),
                             orbit=orb)
                self.debrisConf.add_section(debname)        # Make new section i debris Conf
                for key in d:               # Add all values to the Conf
                    self.debrisConf.set(debname, key, d.get(key))
                self.debrisConf.set(debname, "orbit", orbname)
                self.debrisConf.set("ORBITS", orbname, str(self.orbitConf.items(orbname)))  # Add orbit to orbit section
    
                self.debris_list.append(Deb)    # Add debris to the debris list
            self.objectNbr.setMaximum(len(self.debris_list))    # Adjust the size of the debris choice box

    def add_debris(self):       # Add new debris
        new_deb = NewDebris(self)   # Open new debris window
        new_deb.exec_()             # Wait for it to close
        self.objectNbr.setMaximum(len(self.debris_list))    # Adjust the size of the debris choice box

    def remove_debris(self):    # Remove debris
        rem_deb = RemoveDebris(self)# Open remove debris window
        rem_deb.exec_()             # Wait for it to close
        self.objectNbr.setMaximum(len(self.debris_list))    # Adjust the size of the debris choice box

    def save_debris(self, filename):# Save debris information to file
        if filename == False:   # If no filename was provided, open save file dialog
            filename = self.set_filename('dcfg', formats=['Debris Files (*.dcfg)'])
            if filename == None:# If no filename was chosen
                return          # Quit save action
        with open(filename, 'w') as writefile:  # Open file with filename and write info in Conf to it
            self.debrisConf.write(writefile)

    def change_debris(self, i):# When debris choice box index is changed
        if i == 0:      # If index is 0, no debris ⇒ display only 0's
            self.num_m.display(0)
            self.num_d.display(0)
            self.num_Cm.display(0)
            self.num_etac.display(0)
            self.num_r.display(0)
            self.num_nu.display(0)
            self.num_v.display(0)
            self.num_rp.display(0)
            self.num_ra.display(0)
            self.num_omega.display(0)
            self.num_epsilon.display(0)
        else:           # Debris is chosen
            self.debris = self.debris_list[i-1]     # Store debris object
            self.num_m.display(self.debris._mass)   # Display debris info
            self.num_d.display(self.debris._size)
            self.num_Cm.display(self.debris._Cm)
            self.num_etac.display(self.debris._etac)
            self.update_position()                  # Update displayed position info
            self.update_orbit()                     # Update displayed orbit info

    def debris_step(self):      # Function to run as tread when program is running
        self.lock.acquire()     # Lock processor power
        self.plot_orbit()       # Plot the orbit of the chosen debris
        self.lock.release()     # Release processor
        beta_achieved = False   # Set start values to False/None
        zeta_achieved = False
        self.kill_reason = None
        fired = False
        while self.running:     # While system should be running
            try:                # Look for Exceptions
                t1 = time.time()    # Get start time for loop
                for i in range(self.time_step): # Move the debris for given time
                    self.lock.acquire()
                    self.debris.step()      # Each step is 1s long
                    self.lock.release()
                self.lock.acquire()
                self.plot_debris()          # Plot debris position in graph
                meas = self.debris.measure()# Get measurements as from Gs
                beta = math.atan2(meas['sbeta'], meas['cbeta']) # Get elevation angle 
                beta_min = math.radians(float(self.beta_min.value()))   # Minimum
                beta_max = math.radians(float(self.beta_max.value()))   # Maximum
                if (beta_min < beta < beta_max):    # Check if β is in range
                    beta_achieved = True            # Remember that β was found
                    zeta = math.atan2(meas['szeta'], meas['czeta']) # Get ∠zv
                    zeta_min = math.radians(self.zeta_min.value())  # Minimum
                    zeta_max = math.radians(self.zeta_max.value())  # Maximum
                    if (zeta_min < zeta < zeta_max):    # Check if ζ is in range
                        zeta_achieved = True            # Remember that ζ was found
                        if not fired:       # If laser hasn't been fired during the passing
                            if self.expZeta.isChecked():    # If the expand ζ box was ticked
                                zeta_max = math.pi/2        # Set ζ = π/2
                            self.fire(beta_min, beta_max, zeta_min, zeta_max)   # Fire at given angles
                            fired = True    # Remember that the laser was fired
                            if self.pltTransfer.isChecked():
                                self.plot_transfer()    # Plot a line between the transfer points
                            if self.pltApprox.isChecked():
                                self.plot_approx_orbit()    # Plot approximation
                            self.plot_orbit()       # Plot the new orbit

                            if self.debris.inAtmosphere():
                                self.running = False
                                self.success = True
                                if self.lock.locked():
                                    self.lock.release()
                                self.killed.emit()

                elif beta_achieved:     # If β was in range but no longer is
                    if not zeta_achieved:   # If ζ wasn't found
                        self.running = False    # Stop the loop, nothing will change with set values
                        raise Exception("No \u03b6 in the specified range " # Raise an exception to 
                                        "was found within the specified "   # show a message box explaining
                                        "\u03b2 range")                     # why it was stopped
                    zeta_achieved = False   # Reset values to False before next iteration of the loop
                    beta_achieved = False
                    fired = False
    #            self.update_position()      # Updating the position in each iteration causes intermittent segmentation faults from PqQt package
                td = time.time() - t1   # Check how long the iteration took
                ts = .1 - td            # Compute sleep time
                if self.lock.locked():
                    self.lock.release()
                time.sleep(ts if ts > 0 else 0) # Only sleep if iteration was quick enough
            # While loop finished
            except Exception as e:      # If an exception was raised
                self.success = False
                self.running = False    # Stop loop
                if self.lock.locked():
                    self.lock.release()     # Make sure processor is released
                self.kill_reason = e    # Store message for exception
                self.killed.emit()      # Emit kill signal

    def on_killed(self):    # When kill signal is given, show message box with explination message
        if self.success:
            QtWidgets.QMessageBox.information(None, "De-orbit successful",
                      ("The orbit has entered the atmosphere.\n" +
                       "The debris will crash or burn up in the atmosphere."),
                        QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.information(None, "Error", str(self.kill_reason), QtWidgets.QMessageBox.Ok)

    def plot_debris(self):  # Plot debris position in the graph
        data = self.debris.plot_data()  # Get [x,y] coordinates 
        try:                            # Try to remove old debris dot
            del self.graph.lines[self.graph.lines.index(self.deb_dot)]
        except (AttributeError, ValueError):    # Catch and disgard if dot wasn't there
            pass
        self.deb_dot = self.graph.plot(data[0], data[1], 'ro')[0]   # Plot new dot
        self.canvas.draw()              # Redraw the canvas with new dot

    def plot_transfer(self):# Plot debris transfer between orbits
        data = self.debris.transfer_data()  # Get matrix of transfer points
        if len(data) > 0:   # If there are points in the matrix
            self.graph.plot(data[:, 0], data[:, 1], '--') # Plot the transfer with a dashed line
            self.canvas.draw()

    def update_position(self):  # Update the displayed position values
        v = round(self.debris._v)
        r = round(self.debris._r/1000)
        nu = round(math.degrees(self.debris._nu))
        self.num_r.display(r)
        self.num_nu.display(nu)
        self.num_v.display(v)

    def update_orbit(self):     # Update the displayed orbit values
        orb = self.debris._orbit
        self.num_rp.display(orb.rp)
        self.num_ra.display(orb.ra)
        self.num_omega.display(orb.omega)
        self.num_epsilon.display(orb.ep)

    def reset_debris(self):     # Reset the debris orbit and position to that stored in the Conf
        d = dict(self.debrisConf.items(self.debris.ID))
        o = dict(self.orbitConf.items(d.get("orbit")))
        self.debris.compute(float(d.get("etac")), float(d.get("Cm")), float(d.get("size")), 
                float(d.get("mass")), float(d.get("nu")), 
                rp=float(o.get("rp")), ep=float(o.get("epsilon")), omega=float(o.get("omega")))
        self.num_m.display(self.debris._mass)
        self.num_d.display(self.debris._size)
        self.num_Cm.display(self.debris._Cm)
        self.num_etac.display(self.debris._etac)
        self.update_position()
        self.update_orbit()
        

    # Orbit functions #
    def load_orbit(self, filename=False, scp=False):    # Load orbit data from file
        if scp == False:            # If no SCP was provided
            if filename == False:   # And no filename was provided, open dialog to open orbit file
                filename = self.get_filename(formats=['Orbit Files (*.ocfg)'])
            orbitConfTemp = SCP(allow_no_value=True, delimiters=('='))  # Make temporary SCP
            orbitConfTemp.read(str(filename))       # And read data from file into it
        else:                       # If SCP was provided
            orbitConfTemp = scp     # Use it
        orbits = orbitConfTemp.sections()
        forAll = None       # Initiate for all value as None
        for orb in orbits:  # For each orbit in the local conf
            if orb not in self.orbit_list:  # If not already in the list
                vals = dict(orbitConfTemp.items(orb))   # Get values as a dictionary
                self.insert_orbit(orb, vals)            # Add orbit to list
            elif len(set(orbitConfTemp.items(orb)) & set(self.orbitConf.items(orb))) == 3:  # In same as in list
                pass        # Do nothing
            else:           # If in list but not the same
                if forAll == None:  # If no forAll action has been set
                    action = DuplicateOrbit(orb).exec_()    # Show question window to get action
                    if action >= 10:            # If action is one of the for all ones
                        action = action % 10    # Action is the remainder when devided by 10
                        forAll = action         # Set this action to be used for all
                else:               # If forAll action has been set
                    action = forAll # The action is the same as forAll
                if action == 0: # Skip
                    pass
                elif action == 1: # Rename
                    name = orb
                    while name in self.orbit_list: # While name is a duplicate, ask for a new one
                        name = str(QtWidgets.QInputDialog.getText(self.central_widget,
                                "Rename Orbit", "Name")[0])
                    if len(name) < 1:   # No new name given => skip
                        pass
                    else:
                        vals = dict(orbitConfTemp.items(orb))   # Put in Conf and list
                        self.insert_orbit(name, vals)
                elif action == 2: # Replace
                    vals = dict(orbitConfTemp.items(orb))   # Change values for orbit in Conf
                    self.insert_orbit(orb, vals)
        self.orbit_list.sort()  # Sort the list in alphabetical order

    def insert_orbit(self, name, vals): # Insert an orbit into Conf and list
        if self.orbit_list.count(name) <= 0:
            self.orbit_list.append(name)
        if not self.orbitConf.has_section(name):
            self.orbitConf.add_section(name)
        self.orbitConf.set(name, "rp", vals.get("rp"))
        self.orbitConf.set(name, "epsilon", vals.get("epsilon"))
        self.orbitConf.set(name, "omega", vals.get("omega"))

    def add_orbit(self):    # Add new orbit
        self.new_orb = NewOrbit(self)   # Open new orbit window
        self.new_orb.exec_()            # Wait for it to close

    def remove_orbit(self): # Remove orbit
        rem_orb = RemoveOrbit(self)     # Open remove orbit window
        rem_orb.exec_()                 # Wait for it to close

    def save_orbit(self, filename): # Save orbits to file
        if filename == False:       # If no filename is provided, open save file dialog to get one
            filename = self.set_filename('ocfg', formats=['Orbit Files (*.ocfg)'])
            if filename == None:    # If no filename was given
                return              # Quit save function
        with open(filename, 'w') as writefile:  # Open file and write orbit conf to it
            self.orbitConf.write(writefile)

    def plot_approx_orbit(self):    # Plot the computation of the orbit from measurements
        data = self.debris._orbit.plot_approx_data()    # Get data from orbit class
        self.graph.plot(data[0], data[1], ':')          # Plot data as dotted line
        self.graph.axis('equal')                        # Set axis to equal
        self.canvas.draw()                              # Redraw canvas

    def plot_orbit(self):   # Plot orbit in graph
        data = self.debris._orbit.plot_data()   # Get [x,y] coordinates
        self.graph.plot(data[0], data[1])
        self.graph.axis('equal')
        self.canvas.draw()

    def show_whole_plot(self):
        self.graph.axis('equal')
        self.canvas.draw()


    # Laser functions #
    def load_laser(self, filename=False, scp=False):    # Load laser data from file
        if scp == False:    # If an SCP wasn't provieded
            if filename == False:   # And no filename was provided, open dialog to open laser file
                filename = self.get_filename(formats=['Laser Files (*.lcfg)'])
            laserConfTemp = SCP(allow_no_value=True, delimiters=('='))  # Make local SCP
            laserConfTemp.read(str(filename))       # Read data from file into local SCP
        else:               # If an SCP was provided, use it
            laserConfTemp = scp
        lasers = laserConfTemp.sections()   # Get all laser names
        forAll = None                       # Initiate forAll as None
        for laser in lasers:    # For each laser in the local Conf
            if laser not in self.laserConf.sections():  # If it's not already in the global Conf
                vals = dict(laserConfTemp.items(laser)) # Add it to the list and Conf
                self.insert_laser(laser, vals)
            elif len(set(laserConfTemp.items(laser)) & set(self.laserConf.items(laser))) == 7:  # If there and the same
                pass    # Do nothing
            else:   # If name already exists but values differ
                if forAll == None:  # If no forAll action has been set
                    action = DuplicateLaser(laser).exec_()  # Show quiestion window to get action
                    if action >= 10:    # If action is one of forAll type
                        action = action % 10    # Action is the remainder when devided by 10
                        forAll = action         # Set forAll to this action
                else:               # If a forAll action has been set
                    action = forAll # Action is the forAll
                if action == 0: # Skip
                    pass
                elif action == 1: # Rename
                    name = laser
                    while name in self.laserConf.sections():    # While the name isn't unique
                        name = str(QtWidgets.QInputDialog.getText(self.central_widget,
                                "Rename Laser", "Name")[0])     # Ask for a new one
                    if len(name) < 1:   # No new name given => skip
                        pass
                    else:
                        vals = dict(laserConfTemp.items(laser))     # And add it to the Conf and list
                        self.insert_laser(name, vals)
                elif action == 2: # Replace
                    vals = dict(laserConfTemp.items(laser))     # Change values in Conf
                    self.insert_laser(laser, vals)

    def insert_laser(self, name, vals): # Insert a laser into the Conf and list
        if self.laser_type_list.count(name) <= 0:
            if 'Custom' in self.laser_type_list:    # If list has Custom, put it second last
                pos = self.laserType.count()-1
            else:                                   # Else, put it last
                pos = self.laserType.count()
            self.laserType.insertItem(pos, name)
            self.laser_type_list.insert(pos, name)
        if not self.laserConf.has_section(name):
            self.laserConf.add_section(name)
        for key in vals:
            self.laserConf.set(name, key, vals.get(key))

    def add_laser(self):    # Add a new laser to the system
        new_laser = NewLaser(self)  # Open new laser window
        new_laser.exec_()           # Wait for it to close

    def remove_laser(self): # Remove a laser from the system
        rem_laser = RemoveLaser(self)
        rem_laser.exec_()

    def save_laser(self, filename): # Save all laser data to a file
        if filename == False:       # If no filename was provided, Open dialog to save file
            filename = self.set_filename('lcfg', formats=['Laser Files (*.lcfg)'])
            if filename == None:    # If no filename was chosen
                return              # Quit save function
        with open(filename, 'w') as writefile:  # Open file and write Conf data to it
            self.laserConf.write(writefile)

    def laser_choice(self, choice): # When laser choice box is edited
        if choice == "Choose":      # If the chosen value is Choose, show the empty widget
            self.laserstack.setCurrentWidget(self.laserEmpty)
            LT = self.laserConf.defaults()  # Set the laser system to the default values
            self.lasersystem.switch(LT)
        elif choice == "Custom":    # If the chosen value is Custom, show the undefined widget
            self.laserstack.setCurrentWidget(self.laserUndef)
            LT = dict(self.laserConf.items(str(choice)))    # Set default values to the ones
            self.laserUndef.setDefaultLaserParam(LT)        # for an undefined laser
            self.lasersystem.switch(LT)
        else:                       # If one of the defined lasers are chosen, show the defined widget
            self.laserstack.setCurrentWidget(self.laserDef)
            LT = dict(self.laserConf.items(str(choice)))    # Set default values of the 
            self.laserDef.setDefaultLaserParam(LT)          # chosen laser
            self.lasersystem.switch(LT)

    def fire(self, beta_min, beta_max, zeta_min, zeta_max): # When the laser is fired
        self.lasersystem.fire(self.antenna, self.debris,    # Run the fire function in the laser class
                float(self.laserstack.currentWidget().get_duration()),  # with the current values
                self.atmosphere, beta_min, beta_max, zeta_min, zeta_max)
        self.update_position()      # Update the debris position
        self.update_orbit()         # Update the orbit

    # Other functions #
    def open_file(self):    # When open file, in file menu is klicked
        filename = str(self.get_filename(pref='LODR Files (*.lodr)'))   # Get name of the file to be opened
        if filename != 'None':      # If a filename was provided
            if filename.endswith('lodr'):   # If the file format is .lodr
                confTemp = SCP(allow_no_value=True, delimiters=('='))   # Make a temporary SCP
                confTemp.optionxform = str              # Make it case sensitive
                confTemp.read(str(filename))            # Read the file into the SCP
                for section in confTemp.sections():     # For each section in the SCP
                    dictionary = dict(confTemp.items(section))  # Make a dictionare of all section data
                    scp = self.dict2scp(dictionary)     # Make an SCP of the dictionary
                    exec("self.load_" + str(section).lower() + "(scp=scp)") # Run load function for each section with scp as input
            elif filename.endswith('dcfg'): # Debris files
                self.load_debris(filename=filename)
            elif filename.endswith('lcfg'): # Laser files
                self.load_laser(filename=filename)
            elif filename.endswith('ocfg'): # Orbit files
                self.load_orbit(filename=filename)
            else:                   # If the file format isn't known, show message box 
                QtWidgets.QMessageBox.warning(self.central_widget, 'Unsupported format',
                        'The file you chose has an unsupported format. \n' +
                        'Please choose a different file', buttons=QtWidgets.QMessageBox.Ok,
                        defaultButton=QtWidgets.QMessageBox.NoButton)
    
    def save_file(self):    # When save file, in the file menu is klicked
        filename = str(self.set_filename('lodr', pref='LODR Files (*.lodr)'))   # Use set filename function to choose a file name
        if filename != 'None':  # If a filename was provided
            if filename.endswith('lodr'):   # If the file format is .lodr
                confTemp = SCP(allow_no_value=True, delimiters=('='))   # Make a temporary SCP
                confTemp.optionxform = str              # Make it case sensitive
                confTemp.add_section("LASER")           # Add laser section
                for name in self.laserConf.sections():  # For each laser in the laser conf
                    if name != "Custom":        # If it's not the custom one
                        confTemp.set("LASER", name, str(self.laserConf.items(name)))    # Make a sting of the values and add it to the temp SCP
                confTemp.add_section("ORBIT")           # Add an orbit section
                for name in self.orbitConf.sections():  # For each orbit in the orbit conf
                    confTemp.set("ORBIT", name, str(self.orbitConf.items(name)))    # Make a string of the values and add it to the temp SCP
                confTemp.add_section("DEBRIS")          # Add a debris section
                for name in self.debrisConf.sections(): # For each debris on the debris conf
                    confTemp.set("DEBRIS", name, str(self.debrisConf.items(name)))  # Make a string of the values and add it to the temp SCP
                with open(filename, 'w') as writefile:  # Open the file with filename and write the data in the conf to it
                    confTemp.write(writefile)
            elif filename.endswith('dcfg'): # Debris files
                self.save_debris(filename=filename)
            elif filename.endswith('lcfg'): # Laser files
                self.save_laser(filename=filename)
            elif filename.endswith('ocfg'): # Orbit files
                self.save_orbit(filename=filename)
            else:                           # If the file format is unknown, show message
                QtWidgets.QMessageBox.warning(self.central_widget, 'Unsupported format',
                        'The file you chose has an unsupported format. \n' +
                        'Please choose a different file', buttons=QtWidgets.QMessageBox.Ok,
                        defaultButton=QtWidgets.QMessageBox.NoButton)
    
    def get_filename(self, pref=None, formats=None):    # Get filename
        if formats == None:         # If no format list is provided
            formats = self.formats  # Use standard list
        if pref == None:            # If no preferred format is provided
            pref = formats[0]       # Use the first entry in the list
        self.openDiag.setNameFilters(formats)       # Set list to only files of listed formats
        self.openDiag.setDirectory(self.filefolder) # Set start folder to the last used one
        self.openDiag.selectNameFilter(pref)        # Show only preferred file format
        if (self.openDiag.exec_()): # When closed with button
            filename = self.openDiag.selectedFiles()[0] # Use filename from the dialog
            self.filefolder = os.path.dirname(os.path.realpath(str(filename)))  # Save filefolder for later use
            return filename         # Return the filename

    def set_filename(self, suffix, pref=None, formats=None):    # Set filename
        if formats == None:         # If no format list is provided
            formats = self.formats  # Use standard list
        if pref == None:            # If no preferred format is provided
            pref = formats[0]       # Use the first entry in the list
        self.saveDiag.setNameFilters(formats)       # Set list to only files of listed formats
        self.saveDiag.selectNameFilter(pref)        # Show only preferred file format
        self.saveDiag.setDefaultSuffix(suffix)      # Set suffix to given one
        if (self.saveDiag.exec_()): # When closed with button
            filename = self.saveDiag.selectedFiles()[0] # Use filename from dialog
            self.filefolder = os.path.dirname(os.path.realpath(str(filename)))  # Save filefolder for later use
            return filename         # Return the filename

    def updateSuffix(self, nameFilter):     # Update suffix 
        namefilter = str(nameFilter)        # String including suffix
        if namefilter.rfind('*.') > -1:     # If *. is found in the string
            part = namefilter.rpartition('*.')[2]   # Get whats after *.
            suffix = part[0:len(part)-1]    # Get file format
        else:                               # If no *.
            suffix = 'txt'                  # Use txt as format
        self.saveDiag.setDefaultSuffix(suffix)  # Set suffix to be used

    def empty_plot(self):   # Starting plot
        self.graph.clear()  # Clear the graph, plot the Earth in green and the atmosphere in blue
        self.graph.add_patch(Circle((0, 0), consts.Re+160e+03, color='b', alpha=0.2))
        self.graph.add_patch(Circle((0, 0), consts.Re, color='g', alpha=0.5))
        self.graph.margins(0.1, tight=False)    # Set margins and layout
        self.graph.axis('equal')                # Set equal axis
        self.canvas.draw()                      # Draw plots on canvas

    def dict2scp(self, dictionary): # Convert dictionary to SCP
        scp = SCP(allow_no_value=True, delimiters=('='))    # Make a new SCP
        scp.optionxform = str                   # Make it case sensitive
        for sec in list(dictionary.keys()):     # For each key in the dictionary
            scp.add_section(sec)                # Make a section in the SCP
            vals = dict(eval(dictionary.get(sec)))  # Make a dict from the string of the key
            for key in vals:                    # For each key in this dictionary 
                scp.set(sec, key, str(vals.get(key)))   # Store value in the SCP
        return scp                              # Return the SCP


    def run_pushed(self):       # When run button is pushed
        if self.debris != None:             # If a piece of debris is chosen
            self.running = not self.running # Toggel the value of running
            if self.running:                # If system should run, start a thread using debris_step function
                self.debris_thread = threading.Thread(target=self.debris_step).start()
        else:                               # If no debris is chosen, Show error message
            QtWidgets.QMessageBox.information(self.central_widget, "Error",
                                          "No debris chosen", QtWidgets.QMessageBox.Ok)
            self.running = False            # Set running to False

    def close_application(self):    # When close button is pushed
        choice = QtWidgets.QMessageBox.question(self.central_widget, "Close",   # Show a window asking:
                                            "Are you sure you want to close the application?",
                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if choice == QtWidgets.QMessageBox.Yes:     # If yes, exit the system
            sys.exit()
        else:                                       # If no, do nothing
            pass



if __name__ == "__main__":      # Main function

    sys.settrace                            # Enable tracing
    app = QtWidgets.QApplication(sys.argv)   
    window = OperatorGUI()                  # Make a new object of the GUI
    window.show()                           # Show the GUI and run program
    sys.exit(app.exec_())                   # When program is done, close application
