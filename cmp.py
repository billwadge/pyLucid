""" check and compile into atomic y-code """

import prs,prp,pio,pop,pre,ren, ari,map,ali,glb,exp,atz

if __name__ == "__main__":
    pg = prs.ParseFile("testprog.lu")
    print("check locals")
    pre.CheckLocals(pg)
    print("check dups")
    pre.CheckDups(pg)
    print("check embeddings")
    pre.ProgramEmbedded(pg)
    prp.Termln(pg)
    print('renaming')
    prp.Termln(pg)
    rpg = ren.Rename(pg,pop.EmptySet)
    prp.Termln(rpg)
    print('Checking Arities')
    m = ari.Aritytab(rpg,map.EmptyMap)
    pio.WriteItemln(m)
    ari.ArityCheck(rpg,m)
    print('globalizing')
    gpg = glb.Gprogram(rpg)
    print('Ali-anating')
    atab,ftab, ypg = ali.ActualTable(gpg,map.EmptyMap,map.EmptyMap)
    prp.Term(ypg);
    print()
    pio.WriteItemln(atab)
    pio.WriteItemln(ftab)
    adefs = ali.ActualDefs(atab,ftab)
    subj,body = exp.WhereD(ypg)
    body = pop.Append(body,adefs)
    pg = exp.WhereC(subj,body)
    print('extended program')
    prp.Termln(pg)
    pg = atz.Awhere(pg)
    print('atomized program')
    prp.Termln(pg)
    