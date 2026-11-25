PATH="case0.txt"
OUT="graph.dot"
ALPHABET = "abcdefghijklmnopqrstuwvxyz"

#productions have to be in the format: (a) x := x + 1
#production name has to be one char, and it has to be the second char in the line
#changed variable has to be onr char, and be the fourth char in the line
#variables have to be single chars, and start after 8th char in the line
#production names in A have to start after the second char
#productions in w have to start after 4th char

def dfs(graph, i, j):
    n = len(graph)
    if i>=n or j >=n:
        raise IndexError(f"{i} or {j} does not belong to the graph")
    if i == j:
        raise IndexError("i and j cannot be the same vertex")
    visited = [False]*n
    to_visit=[i]
    while(len(to_visit)):
        s = to_visit.pop()
        if(not visited[s]):
            visited[s]= True
            if s == j:
                return True
            for v in graph[s]:
                to_visit.append(v)
    return False


productions={} #name: (changed, [used])
D=[]
I=[]
dependents={} #name: [other dependent productions]

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
            w=x[4::].strip()
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

#GRAPH
graph = {}

for i in range(len(w)): #creating a full graph
    graph[i] = []
    for j in range(0, i):
        if (w[j], w[i]) in D:
            graph[j].append(i)

for i in range(len(w)):
    length = len(graph[i])
    for j in range(length-1, -1, -1):#len(graph) can change, so the connections have to be checked from the back
        s = graph[i][j] #j-th connection from i
        graph[i].pop(j)
        if not dfs(graph, i, s): #if s cannot be visited from i the connection has to be in the graph
            graph[i].insert(j, s)

with open(OUT, "w") as out: #writing the graph to a file in a .dot format
    out.write("digraph g{\n")
    for i in graph.items():
        for j in i[1]:
            out.write(f"{i[0]} -> {j}\n")
    for i in range(len(w)):
        out.write(f'{i}[label="{w[i]}"]\n')
    out.write("}")