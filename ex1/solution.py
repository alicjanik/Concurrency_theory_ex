'''case 1:
(a) x := x + 1
(b) y := y + 2z
(c) x := 3x + z
(d) w := w + v
(e) z := y - z
(f) v := x + v
A = {a, b, c, d, e, f}
w = acdcfbbe
'''
PATH="case0.txt"
ALPHABET = "abcdefghijklmnopqrstuwvxyz"

productions={}
D=[]
I=[]
dependents={}

#{"a": (x, [x]), "b": (y, [y, z]), ...} <- "production": (changed, [used])
#ZAŁOŻENIA: produkcje w formacie (a) x := x + 1 <- nazwa busi być 2. znakiem, zmieniana zmienna musi być 4. znakiem
#nazwy produkcj i zmienne muszą być pojedyńczymi literami

with open(PATH) as f:
    for x in f:
        if x[0]=='(':
            name=x[1]
            changed=x[4]
            used=[letter for letter in x[8::] if letter in ALPHABET]
            productions[name] = (changed, used)
        elif x[0]=='A':
            A=[prod for prod in x[2::] if prod in ALPHABET]
        elif x[0]=='w':
            w=x[4::]
        else:
            raise SyntaxError(f"{x[0]} is not a valid starting character")

if productions.keys() != set(A):
    raise ValueError("A does not match with declared productions")

for prod in A:
    dependents[prod] = []

for i, first in enumerate(A):
    for second in A[i::]:
        if productions[first][0] in productions[second][1] or productions[second][0] in productions[first][1]:
            D.append((first, second))
            if first != second:
                D.append((second, first))
                dependents[second].append(first)
                dependents[first].append(second)
        else:
            I.append((first, second))
            if first != second:
                I.append((second, first))

print(f"D: {D}")
print(f"I: {I}")

stacks = {}

for prod in A:
    stacks[prod] = []

fnf=[]

#FNF
count=0
for letter in w[::-1]:
    stacks[letter].append(1)
    count+=1
    for dep in dependents[letter]:
        stacks[dep].append(0)
        count+=1

while count>0:
    group=[]
    for s in A:
        if bool(stacks[s]) and stacks[s][-1]==1:
            group.append(s)
            stacks[s].pop()
            count-=1
    for s in group:
        for d in dependents[s]:
            stacks[d].pop()
            count-=1
    fnf.append(group)

print(f"FNF: {fnf}")    

