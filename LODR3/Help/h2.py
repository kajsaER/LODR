import ConfigParser as CP

laser_config = CP.SafeConfigParser(allow_no_value=True)

laser_config.read('lasers.cfg')

CO2 = dict(laser_config.items('CO2'))

print CO2.get('energy')

#for laser in laser_config.sections():

#    P =  laser_config.getfloat(str(laser), 'Power')
#    frep = laser_config.getfloat(str(laser), 'Repetition rate')

#    if not laser_config.has_section:
#        laser_config.add_section(str(laser))
    #laser_config.set('CO2', 'Power', '70.0')
#    laser_config.set(str(laser), 'Energy', str(P/frep))
    #laser_config.set('CO2', 'Lambda', '10.6e-6')
    #laser_config.set('CO2', 'M2', '')
    #laser_config.set('CO2', 'Cb', '')
    #laser_config.set('CO2', 'Repetition rate', '')
    #laser_config.set('CO2', 'Pulse duration', '')


with open('lasers.cfg', 'w') as f:
    laser_config.write(f)


#with open('workfile', 'a+') as f:

#    l = raw_input('add a line: \n')

#    f.write(l)
#    f.flush()

#    print 'your line was: ' + l 
    
#    print f.tell()

#    f.seek(0)

#    for line in f:
#        print line
#    f.seek(51)
#    print f.tell()
#    f.close()
