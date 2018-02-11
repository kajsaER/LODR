from configparser import SafeConfigParser as SCP

def dict2scp(dictionary):
    scp = SCP(allow_no_value=True)
    scp.oprionxform = str
    for sec in list(dictionary.keys()):
        scp.add_section(sec)
        s = dictionary.get(sec)
        list1 = eval(s)
        print(list1)
        vals = dict(list1)
        for key in vals:
            scp.set(sec, key, str(vals.get(key)))
    return scp


if __name__ == "__main__":
    d = {'LEO': "[('rp', '7000000'), ('epsilon', '0.7'), ('omega', '2.34')]",
         'GEO': "[('rp', '42164000'), ('epsilon', '0'), ('omega', '1.23')]"}
    scp = dict2scp(d)
