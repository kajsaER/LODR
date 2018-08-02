class UndefinedLaser(UndefinedLaserBaseClass, UndefinedLaserWidget):
    def __init__(self, main, parent=None):
        super(UndefinedLaser, self).__init__(parent)
        self.setupUi(self)
        self.main = main
        self.main.laserConf.add_section('Custom')
        if 'Custom' not in self.main.laser_type_list:
            self.main.laserType.addItem('Custom')
            self.main.laser_type_list.append('Custom')
        LT = {'Power':'1000', 'Power min':'1E+00', 'Power max':'5E+06',
              'Energy':'1E-09', 'Energy min':'1E-09', 'Energy max':'1E+00',
              'Lambda':'1E-09', 'Lambda min':'1E-09', 'Lambda max':'1E+00', 
              'M2':'1', 'M2 min':'1', 'M2 max':'1E+02',
              'Cb':'1', 'Cb min':'1', 'Cb max':'1E+01',
              'Repetition rate':'1E+11', 'Pulse duration':'1e-09'}
        for name in list(LT.keys()):
            self.main.laserConf.set('Custom', name, LT[name])


        self.freqDub.toggled.connect(self.double_freq)
        
        self.slide_P.actionTriggered.connect(lambda act: self.slide_trigged(act, 'P'))
        self.slide_W.actionTriggered.connect(lambda act: self.slide_trigged(act, 'W'))
        self.slide_lambda.actionTriggered.connect(lambda act: self.slide_trigged(act, 'lambda'))
        self.slide_M2.actionTriggered.connect(lambda act: self.slide_trigged(act, 'M2'))
        self.slide_Cb.actionTriggered.connect(lambda act: self.slide_trigged(act, 'Cb'))
        self.slide_frep.actionTriggered.connect(lambda act: self.slide_trigged(act, 'frep'))
        self.slide_tau.actionTriggered.connect(lambda act: self.slide_trigged(act, 'tau'))
        self.slide_T.actionTriggered.connect(lambda act: self.slide_trigged(act, 'T'))
        
        self.slide_P.sliderMoved.connect(lambda value: self.slide_moved(value, 'P'))
        self.slide_W.sliderMoved.connect(lambda value: self.slide_moved(value, 'W'))
        self.slide_lambda.sliderMoved.connect(lambda value: self.slide_moved(value, 'lambda'))
        self.slide_M2.sliderMoved.connect(lambda value: self.slide_moved(value, 'M2'))
        self.slide_Cb.sliderMoved.connect(lambda value: self.slide_moved(value, 'Cb'))
        self.slide_frep.sliderMoved.connect(lambda value: self.slide_moved(value, 'frep'))
        self.slide_tau.sliderMoved.connect(lambda value: self.slide_moved(value, 'tau'))
        self.slide_T.sliderMoved.connect(lambda value: self.slide_moved(value, 'T'))

        self.slide_P.valueChanged.connect(lambda value: self.slide_changed(value, 'P'))
        self.slide_W.valueChanged.connect(lambda value: self.slide_changed(value, 'W'))
        self.slide_lambda.valueChanged.connect(lambda value: self.slide_changed(value, 'lambda'))
        self.slide_M2.valueChanged.connect(lambda value: self.slide_changed(value, 'M2'))
        self.slide_Cb.valueChanged.connect(lambda value: self.slide_changed(value, 'Cb'))
        self.slide_frep.valueChanged.connect(lambda value: self.slide_changed(value, 'frep'))
        self.slide_tau.valueChanged.connect(lambda value: self.slide_changed(value, 'tau'))
        self.slide_T.valueChanged.connect(lambda value: self.slide_changed(value, 'T'))

        self.unit_P.activated[str].connect(lambda choice: self.unit_change(choice, 'P'))
        self.unit_W.activated[str].connect(lambda choice: self.unit_change(choice, 'W'))
        self.unit_lambda.activated[str].connect(lambda choice: self.unit_change(choice, 'lambda'))
        self.unit_frep.activated[str].connect(lambda choice: self.unit_change(choice, 'frep'))
        self.unit_tau.activated[str].connect(lambda choice: self.unit_change(choice, 'tau'))
        self.unit_T.activated[str].connect(lambda choice: self.unit_change(choice, 'T'))

    def build_unit_box(self, measure):
        listed = []
        keylist = []
        mini = eval('self.min_' + measure)
        maxi = eval('self.max_' + measure)
        for key in list(extmath.allPot.keys()):
            pot = float(key)
            if pot > mini/1000 and pot < maxi and key not in [1e-02, 1e-01, 1e+01, 1e+02]:
                pref = extmath.allPot.get(key)
                keylist.append(float(key))
        keylist.sort()
        for key in keylist:
            listed.append(str(extmath.allPot.get(key) + units.get(measure)))
        exec('self.unit_'+measure+'.addItems(listed)')

    def setDefaultLaserParam(self, LaserType):
        self.freqDub.setChecked(False)
        self.LaserType = LaserType

        self.set_default_value('power', 'P')
        self.set_default_value('energy', 'W')
        self.set_default_value('lambda', 'lambda')
        self.set_default_value('m2', 'M2')
        self.set_default_value('cb', 'Cb')

        self.set_default_value('repetition rate', 'frep')
        self.set_default_value('pulse duration', 'tau')
        self.set_default_value('fire duration', 'T')

    def set_default_value(self, LONG, SHORT):
        temp = extmath.prefixedValue(self.LaserType.get(LONG))
        print(SHORT + ': ' + str(temp))
        exec('self.num_' + SHORT + '.display(temp[1])')
        if SHORT == 'frep':
            print(temp[1])
#            exec('self.num_' + SHORT + '.display(2)')
        exec('self.min_'+SHORT+' = extmath.myfloat(self.LaserType.get(str(LONG + \' min\')))')
        exec('self.max_'+SHORT+' = extmath.myfloat(self.LaserType.get(str(LONG + \' max\')))')
        pot = pow(10, temp[2])
        exec('self.scale_'+SHORT+' = self.max_' + SHORT + '-self.min_' + SHORT)
        if SHORT not in {'M2', 'Cb'}:
            exec('self.pot_' + SHORT + ' = pot')
            self.build_unit_box(SHORT)
            if pot != 1:
                self.set_unit(SHORT)
            exec('self.slide_'+SHORT+'.setValue(self.num_'+SHORT+'.value())')
        else:
            exec('self.slide_'+SHORT+'.setValue((self.num_'+SHORT+'.value()-self.min_'+SHORT+')*'
                'self.slide_'+SHORT+'.maximum()/self.scale_'+SHORT+')')

    def set_unit(self, var):
        p = eval('self.pot_' + var)
        power = '%.0E' % Decimal(p)
        prefixedunit = extmath.allPot.get(p) + units.get(var)
        unit = eval('self.unit_' + var)
        for ind in range(0, unit.count()):
            if unit.itemText(ind) == prefixedunit:
                unit.setCurrentIndex(ind)
                break

    def unit_change(self, choice, var):
        if var == 'frep':
            pref = str(choice[0:len(choice)-2])
        else:
            pref = str(choice[0:len(choice)-1])
        old_pot = eval('self.pot_' + var)
        new_pot = extmath.myfloat(extmath.allPrefixes.get(pref))
        exec('self.pot_' + var + ' = new_pot')
        val = eval('new_pot * self.num_'+var+'.value()')
        mini = eval('self.min_'+var)
        maxi = eval('self.max_'+var)
        if val < mini:
            exec('self.num_'+var+'.display(mini/new_pot)')
            exec('self.slide_'+var+'.setValue(mini/new_pot)')
            exec('self.main.lasersystem._' + var + '= mini')
        elif val > maxi:
            exec('self.num_'+var+'.display(maxi/new_pot)')
            exec('self.slide_'+var+'.setValue(maxi/new_pot)')
            exec('self.main.lasersystem._' + var + '= maxi')
        else:
            exec('self.main.lasersystem._' + var + '= val')

    def double_freq(self):
        if self.freqDub.isChecked():
            self.main.lasersystem.doubfreq()
        else:
            self.main.lasersystem.normfreq()

    def slide_trigged(self, action, var):
        if var not in {'M2', 'Cb'}:
            val = eval('self.slide_' + var + '.value()')
            pot = eval('self.pot_' + var)
        else:
            val = eval('self.slide_' + var + '.value()*self.scale_'+
                  var + '/self.slide_' + var + '.maximum() + self.min_' + var)
            pot = 1
        exec('self.num_' + var + '.display(val)')
        if var != 'T':
            exec('self.main.lasersystem._' + var + ' = val*pot')

    def slide_moved(self, value, var):
        if var not in {'M2', 'Cb'}:
            val = value
        else:
            val = eval('value*self.scale_' + var +
                '/self.slide_' + var + '.maximum() + self.min_' + var)
        exec('self.num_' + var + '.display(val)')

    def slide_changed(self, value, var):
        if var not in {'M2', 'Cb'}:
            val = value
            pot = eval('self.pot_' + var)
        else:
            val = eval('value*self.scale_' + var +
                '/self.slide_' + var + '.maximum() + self.min_' + var)
            pot = 1
        exec('self.num_' + var + '.display(val)')
        if var != 'T':
            exec('self.main.lasersystem._' + var + ' = val*pot')

    def get_duration(self):
        return self.num_T.value()*self.pot_T

