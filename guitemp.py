    # Debris functions #
    def load_debris(self, filename=False, scp=False):
        if scp == False:
            if filename == False:
                filename = self.get_filename(formats=["Debris Files (*.dcfg)"])
            debrisConfTemp = SCP(allow_no_value=True)
            debrisConfTemp.optionxform = str
            debrisConfTemp.read(str(filename))
        else:
            debrisConfTemp = scp
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
            print orbname
            orb = orbit()
            orb.make(float(o.get("rp")), float(o.get("epsilon")), float(o.get("omega")))
            print orb.rp
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
