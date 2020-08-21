

def expand(stoch,add_underscores=True):
    if add_underscores:
        newstoch = ''
        for c in stoch:
            if c.isdigit() and not newstoch[-1:].isdigit():
                newstoch+='_'+c
            else:
                newstoch+=c
        stoch=newstoch
        while '__' in stoch: stoch = stoch.replace('__','_') ## Remove double underscores
        
    f = ''
    for c in stoch:
        if c.isupper() or c == "(":
            f+=' '+c
        else:
            f+=c
    while '_' in f:
        i = f.rfind("_")
        if f[i-1]==")":
            l = 1
            start = i-2
            while l > 0:
                if f[start]=="(":
                    l-=1
                elif f[start]==")":
                    l+=1
                start-=1
            subform = f[start+2:i-1]
            subform = expand(subform)
            k = i+1
            while k<len(f):
                k+=1
                if not f[i+1:k].isdigit():break
            
            num = f[i+1:k]
            f = f[:start+1]+(subform+' ')*int(num)+f[k:]
            
        else:
            nc = 1
            subform = f[i-nc]
            while subform.islower():
                nc+=1
                subform = f[i-nc:i]

            k = i+1
            while k<len(f):
                k+=1
                if not f[i+1:k].isdigit():break
            
            num = f[i+1:k]
            f = f[:i-nc]+(subform+' ')*int(num)+f[k:]
    while '  ' in f: f = f.replace('  ',' ')  
    return f

def parse_form(strform, verbose=False):

    left, right = strform.split('->')
    educts = left.split("+")
    products = right.split("+")
    
    formula = {'Educts':[],'Products':[]}
    for e in educts:
        atoms = expand(e,True).split(' ')
        while '' in atoms: atoms.remove('')
        formula['Educts'].append({'Formula':e.strip(),'Atoms':sorted(atoms)})
    for p in products:
        atoms = expand(p,True).split(' ')
        while '' in atoms: atoms.remove('')
        formula['Products'].append({'Formula':p.strip(),'Atoms':sorted(atoms)})

    if verbose:
        for k,v in formula.items():
            print(k)
            for e in v:
                for k2,v2 in e.items():
                    print('  - '+k2+': '+str(v2))
                print('')
    return(formula)

def count(formula,seq):
    atoms = {}
    for m in formula['Educts']+formula['Products']:
        for a in m['Atoms']:
            atoms[a] = [0,0]

    for i in range(len(seq[0])):
        m,n = formula['Educts'][i],seq[0][i]
        for a in m['Atoms']:
            atoms[a][0]+=n
            
    for i in range(len(seq[1])):
        m,n = formula['Products'][i],seq[1][i]
        for a in m['Atoms']:
            atoms[a][1]+=n
    return atoms

def score(atoms):
    score = []
    for a,b in atoms.values():
        if a < b:
            a,b=b,a
        score.append((a-b)/a)
    score = sum(score)/len(score)

    return 1-score


def balance(formula,maxint=50):
    eq = [[1]*len(formula['Educts']),[1]*len(formula['Products'])]
    cscore = score(count(formula,eq)) ## Compute initial score
    counter = 0

    while cscore < 1:
        for side in [0,1]:
            for coef in range(len(eq[side])):
                eq[side][coef]+=1
                nscore = score(count(formula,eq))
                if nscore>cscore:
                    cscore = nscore
                else:
                    eq[side][coef]-=1
        counter +=1
        if counter > maxint:
            break
    return eq

def niceprint(formula,eq,summary=True):
    outform = [[],[]]
    n = count(formula,eq)

    for i in range(len(eq[0])):
        outform[0].append(str(eq[0][i])+'*'+formula['Educts'][i]['Formula'])

    for i in range(len(eq[1])):
        outform[1].append(str(eq[1][i])+'*'+formula['Products'][i]['Formula'])

    outstring = ' -> '.join([' + '.join(s) for s in outform])

    if summary:
        sn = []
        for atom in sorted(list(n.keys())):
            sn.append(str(n[atom][0])+'*'+atom)
        outstring+= " / Atoms on both sides: "+'; '.join(sn)    

    return outstring
    
            
for equation in ["Ca(OH)2 + HNO3 -> Ca(NO3)2 + H2O",
                 "C6H12O6 + O2 -> CO2 + H2O",
                 "Pb(OH)4 + H2SO4 -> Pb(SO4)2 + H2O"]:
    print("Solving equation: "+equation)
    f = parse_form(equation)
    print(' -> '+niceprint(f,balance(f))+'\n')
    
    
    


