import copy
from Queue import (
    LifoQueue,Queue
    )
import math
import random


class Arrangement:

    def __init__(self, Seq, Row_next, P, L, Map):
        self.Seq = Seq
        self.Row_next = Row_next
        self.P = P
        self.L = L
        self.Map = Map


class Arangement_Initial:
    def __init__(self, N, L, Map):
        self.N = N
        self.L = L
        self.Map = Map
        self.lizards = [[0 for col in range(3)] for row in range(L)]
        arr = []
        for i in range(0,N):
            for j in range(0,N):
                if self.Map[i][j] == 0:
                    arr.append(i*N+j)
        even = len(arr)/L
        for i in range(0,L):
            even1 = random.randint(0,even-1)
            even2 = even1 + i * even
            even3 = arr[even2]
            row = even3/N
            column = even3%N
            self.Map[row][column] = 1
            self.lizards[i][0] = row
            self.lizards[i][1] = column 

class Arangement_SA:
    def __init__(self, N, L, Map,lizards):
        self.N = N
        self.L = L
        self.Map = Map
        self.lizards = lizards
        self.Error_total = 0
        error_total = 0
        for i in self.lizards:
            error = 0
            index = i[1]
            Row_next = i[0]
            column = index + 1
            row = Row_next
            while column - N < 0:
                temp = (self.Map[row][column] == 2)
                if temp:
                    break
                temp = (self.Map[row][column] == 1)
                if temp:
                    error = error +1
                column = column + 1

            column = index - 1
            row = Row_next
            while column + 1 > 0:
                temp = (self.Map[row][column] == 2)
                if temp:
                    break
                temp = (self.Map[row][column] == 1)
                if temp:
                    error = error +1
                column = column - 1

            row = Row_next + 1
            column = index
            while row - N < 0:
                temp = (self.Map[row][column] == 2)
                if temp:
                    break
                temp = (self.Map[row][column] == 1)
                if temp:
                    error = error +1
                row = row + 1

            row = Row_next - 1
            column = index
            while row + 1 > 0:
                temp = (self.Map[row][column] == 2)
                if temp:
                    break
                temp = (self.Map[row][column] == 1)
                if temp:
                    error = error +1
                row = row - 1

            column = index + 1
            row = Row_next + 1
            while row - N < 0 and column - N < 0:
                temp = (self.Map[row][column] == 2)
                if temp:
                    break
                temp = (self.Map[row][column] == 1)
                if temp:
                    error = error +1
                column =column + 1
                row = row + 1

            column = index + 1
            row = Row_next - 1
            while row + 1 > 0 and column - N < 0:
                temp = (self.Map[row][column] == 2)
                if temp:
                    break
                temp = (self.Map[row][column] == 1)
                if temp:
                    error = error +1
                column =column + 1
                row = row - 1

            column = index - 1
            row = Row_next + 1
            while row - N < 0 and column + 1 > 0:
                temp = (self.Map[row][column] == 2)
                if temp:
                    break
                temp = (self.Map[row][column] == 1)
                if temp:
                    error = error +1
                column =column - 1
                row = row + 1


            column = index - 1
            row = Row_next - 1
            while row + 1 > 0 and column + 1 > 0:
                temp = (self.Map[row][column] == 2)
                if temp:
                    break
                temp = (self.Map[row][column] == 1)
                if temp:
                    error = error +1
                column =column - 1
                row = row - 1
            i[2] = error
            error_total = error_total + error
        self.Error_total = error_total/2

def sucess_print(Map):
    output = open("output.txt", 'w')
    output.write("OK")
    for i in Map:
        output.write("\n")
        for j in i:
            if j + 1 == 0:
                j = 0
            output.write(str(j)) 


def fail_print():
    output = open("output.txt", 'w')
    output.write("FAIL")

def SA(root,T):
    now = root
    Min = 0.001
    rate = 0.999
    Temperature = root.Error_total
    conflict = root.Error_total
    while Temperature - Min > 0 and conflict != 0:
        next = Next_one(now,T)
        conflict_next = next.Error_total
        difference = conflict - conflict_next
        if difference >= 0:
            now = next
            conflict = conflict_next
        else:
            probability = math.exp(difference / Temperature)
            if probability - random.random() > 0:
                now = next
                conflict = conflict_next
        Temperature = Temperature * rate
    if conflict == 0:
        return now.Map
    return 0

def Next_one(now,T):
    new_now = copy.deepcopy(now)
    temp = 0
    while True:
        temp = random.randint(0, new_now.L - 1)
        if new_now.lizards[temp][2] != 0:
            break
    row = new_now.lizards[temp][0]
    column = new_now.lizards[temp][1]
    while True:
        upper = new_now.N - 1
        i = random.randint(0, upper)
        j = random.randint(0, upper)
        if not T:
            i = row
        if new_now.Map[i][j] == 0:
            new_now.Map[i][j] = 1
            new_now.Map[row][column] = 0
            new_now.lizards[temp][0] = i
            new_now.lizards[temp][1] = j
            break
    return Arangement_SA(new_now.N,new_now.L,new_now.Map,new_now.lizards)



def map_update(N, index, Row_next, Map):

    Map_new = copy.deepcopy(Map)
    row = Row_next
    column = index
    Map_new[row][column] = 1

    column = index + 1
    row = Row_next
    while column - N< 0:
        temp = (Map_new[row][column] == 2)
        if temp:
            break
        temp = (Map_new[row][column] == 0)
        if temp:
            Map_new[row][column] = -1
        column = column + 1

    column = index - 1
    row = Row_next
    while column + 1 > 0:
        temp = (Map_new[row][column] == 2)
        if temp:
            break
        temp = (Map_new[row][column] == 0)
        if temp:
            Map_new[row][column] = -1
        column = column - 1

    row = Row_next + 1
    column = index
    while row - N < 0:
        temp = (Map_new[row][column] == 2)
        if temp:
            break
        temp = (Map_new[row][column] == 0)
        if temp:
            Map_new[row][column] = -1
        row = row + 1

    row = Row_next - 1
    column = index
    while row + 1 > 0:
        temp = (Map_new[row][column] == 2)
        if temp:
            break
        temp = (Map_new[row][column] == 0)
        if temp:
            Map_new[row][column] = -1
        row = row - 1

    column = index + 1
    row = Row_next + 1
    while row - N < 0 and column - N < 0:
        temp = (Map_new[row][column] == 2)
        if temp:
            break
        temp = (Map_new[row][column] == 0)
        if temp:
            Map_new[row][column] = -1
        column =column + 1
        row = row + 1

    column = index + 1
    row = Row_next - 1
    while row + 1 > 0 and column - N < 0:
        temp = (Map_new[row][column] == 2)
        if temp:
            break
        temp = (Map_new[row][column] == 0)
        if temp:
            Map_new[row][column] = -1
        column =column + 1
        row = row - 1

    column = index - 1
    row = Row_next + 1
    while row - N < 0 and column + 1 > 0:
        temp = (Map_new[row][column] == 2)
        if temp:
            break
        temp = (Map_new[row][column] == 0)
        if temp:
            Map_new[row][column] = -1
        column =column - 1
        row = row + 1


    column = index - 1
    row = Row_next - 1
    while row + 1 > 0 and column + 1 > 0:
        temp = (Map_new[row][column] == 2)
        if temp:
            break
        temp = (Map_new[row][column] == 0)
        if temp:
            Map_new[row][column] = -1
        column =column - 1
        row = row - 1
    return Map_new

def checkRow(arrangement,N):
    for i in range(0,N):
        if arrangement.Map[arrangement.Row_next][i] == 0:
            return False
    return True

def search(N, arrangement, queue):
    Sequence = arrangement.Seq
    while arrangement.Row_next - N < 0 and checkRow(arrangement,N):
        arrangement.Row_next = arrangement.Row_next + 1
    row = arrangement.Row_next
    for index in range(0,N):
        if row - N < 0:
            if arrangement.Map[row][index] == 0:
                Sequence = Sequence + 1
                arrangement_new = Arrangement(Sequence,row,arrangement,arrangement.L+1,map_update(N,index,row,arrangement.Map))
                queue.put_nowait(arrangement_new)

def BFS(N, L, root):
    queue = Queue()
    queue.put_nowait(root)
    while queue.qsize() != 0:
        arrangement = queue.get_nowait()
        if arrangement.L == L:
            return arrangement.Map
        else:
            search(N, arrangement, queue)
    return 0

def DFS(N, L, root):
    queue = LifoQueue()
    queue.put_nowait(root)
    while queue.qsize() != 0:
        arrangement = queue.get_nowait()
        if arrangement.L == L:
            return arrangement.Map
        else:
            search(N, arrangement, queue)
    return 0

with open('input.txt','r') as f:
    lines=f.readlines()
    method = ''
    method = lines[0].strip()
    N = int(lines[1].strip())
    nursery = [[0 for i in range(N)] for j in range(N)]
    L = int(lines[2].strip())
    l_list = lines[3:]
    k = 0
    T = False
    for i in l_list:
        j = 0
        for num in i.strip():
            nursery[k][j] = int(num)
            j = j + 1
            if not T:
                T = (num == '2')
                if T:
                    T = True
        k = k + 1
F = not T and (L - N > 0)
if F:
    fail_print()
elif method == "BFS":
    root = Arrangement(1,0,None,0,nursery)

    result = BFS(N, L, root)
    if result == 0:
        fail_print()
    else:
        sucess_print(result)
elif method == "DFS":
    root = Arrangement(1,0,None,0,nursery)
    result = DFS(N, L, root)
    if result == 0:
        fail_print()
    else:
        sucess_print(result)    
elif method == "SA":
    t = Arangement_Initial(N,L,nursery)
    root = Arangement_SA(t.N,t.L,t.Map,t.lizards)
    result = SA(root,T)
    if result == 0:
        fail_print()
    else:
        sucess_print(result)
else:
    fail_print()
