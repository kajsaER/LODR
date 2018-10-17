    # Debris functions #
    def load_debris(self, filename=False, scp=False):
        if scp != False:
            debrisConfTemp = scp
        else:
            if filename == False:
                filename = self.get_filename(formats=["Debris Files (*.dcfg)"])
            if filename == None:
                debrisConfTemp = None
            else:
                debrisConfTemp = SCP(allow_no_value=True, delimiters=('='))
                debrisConfTemp.optionxform = str
                debrisConfTemp.read(str(filename))
        if debrisConfTemp != None:
            orbitdict = dict(debrisConfTemp.items("ORBITS"))
            orbitscp = self.dict2scp(orbitdict)
            self.load_orbit(scp=orbitscp)
            debrisConfTemp.remove_section("ORBITS")
            Debris = debrisConfTemp.sections()
            for deb in Debris:
                d = dict(debrisConfTemp.items(deb))
                orbname = d.get("orbit")
                o = set(orbitscp.items(orbname))
                O = set(self.orbitConf.items(orbname))
                if len(o & O) < 3:
                    for orbname in self.orbitConf.sections():
                        O = set(self.orbitConf.items(orbname))
                        if len(o & O) == 3:
                            break
                o = dict(O)
                orb = orbit()
                orb.make(float(o.get("rp")), float(o.get("epsilon")), float(o.get("omega")))
                debname = (str(hex(int(float(d.get("mass")) + float(d.get("size")) + 
                           float(d.get("Cm"))*float(d.get("etac")) +
                           360/math.pi*float(d.get("nu"))))) + orbname)
                extra = 0
                n0 = debname
                while self.debrisConf.has_section(debname):
                    debname = n0 + str(extra)
                    extra += 1
                Deb = debris(str(debname), float(d.get("etac")), float(d.get("Cm")),
                             float(d.get("size")), float(d.get("mass")), orb, float(d.get("nu")))
                self.debrisConf.add_section(debname)
                for key in d:
                    self.debrisConf.set(debname, key, d.get(key))
                self.debrisConf.set(debname, "orbit", orbname)
                self.debrisConf.set("ORBITS", orbname, str(self.orbitConf.items(orbname)))
    
                self.debris_list.append(Deb)
            self.objectNbr.setMaximum(len(self.debris_list))

    def add_debris(self):
        new_deb = NewDebris(self)
        new_deb.exec_()
        self.objectNbr.setMaximum(len(self.debris_list))

    def remove_debris(self):
        rem_deb = RemoveDebris(self)
        rem_deb.exec_()
        self.objectNbr.setMaximum(len(self.debris_list))

    def save_debris(self, filename):
        if filename == False:
            filename = self.set_filename('dcfg', formats=['Debris Files (*.dcfg)'])
            if filename == None:
                return 
        with open(filename, 'w') as writefile:
            self.debrisConf.write(writefile)

    def change_debris(self, i):
        if i == 0:
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
        else:
            self.debris = self.debris_list[i-1]
            self.num_m.display(self.debris._mass)
            self.num_d.display(self.debris._size)
            self.num_Cm.display(self.debris._Cm)
            self.num_etac.display(self.debris._etac)
            self.update_position()
            self.update_orbit()

    def debris_step(self):
        self.lock.acquire()
        self.plot_orbit()
        self.lock.release()
        beta_achieved = False
        zeta_achieved = False
        self.kill_reason = None
        fired = False
        while self.running:
            t1 = time.time()
            for i in range(self.time_step):
                self.lock.acquire()
                self.debris.step()
                self.lock.release()
            self.lock.acquire()
            self.plot_debris()
            meas = self.debris.measure()
            beta = math.atan2(meas['sbeta'], meas['cbeta'])
            if (math.radians(float(self.beta_min.value())) < beta 
                    < math.radians(float(self.beta_max.value()))):
                beta_achieved = True 
                zeta = math.atan2(meas['szeta'], meas['czeta'])
                if (math.radians(self.zeta_min.value()) < zeta 
                        < math.radians(self.zeta_max.value())):
                    zeta_achieved = True
                    if not fired:
                        self.fire()
                        fired = True
                        self.plot_orbit()
            elif beta_achieved:
                if not zeta_achieved:
                    self.running = False
                    self.kill_reason = zetaNotInRange
                zeta_achieved = False
                beta_achieved = False
                fired = False
#            self.update_position()
            td = time.time() - t1
#            print(td)
            ts = .1 - td
            self.lock.release()
            time.sleep(ts if ts > 0 else 0)
        print("While ended") 
        if self.kill_reason == zetaNotInRange:
            print("emit killed")
            self.killed.emit()

    def on_killed(self):
        QtWidgets.QMessageBox.information(None, "Error",
                              ("No \u03b6 in the specified range was "
                               "found within the specified \u03b2 range"), 
                               QtWidgets.QMessageBox.Ok)

    def plot_debris(self):
#        print("Plot Debris")
        data = self.debris.plot_data()
        try:
            del self.graph.lines[self.graph.lines.index(self.deb_dot)]
        except (AttributeError, ValueError):
            pass
        self.deb_dot = self.graph.plot(data[0], data[1], 'ro')[0]
        self.canvas.draw()

    def update_position(self):
#        print("Update Position")
        v = round(self.debris._v)
        r = round(self.debris._r/1000)
        nu = round(math.degrees(self.debris._nu))
        self.num_r.display(r)
        self.num_nu.display(nu)
        self.num_v.display(v)

    def update_orbit(self):
#        print("Update orbit")
        orb = self.debris._orbit
        self.num_rp.display(orb.rp)
        self.num_ra.display(orb.ra)
        self.num_omega.display(orb.omega)
        self.num_epsilon.display(orb.ep)

    def reset_debris(self):
        debname = self.debris.ID
        

