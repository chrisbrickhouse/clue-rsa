import random
import matplotlib.pyplot as plt

class Player():
    def __init__(self):
        self.holding = set([])
        self.shown = set([])
        self.unknown = set([
                       'Y', 'P', 'G', 'B', 'R', 'W',
                       'k', 'c', 'v', 'r', 'l', 'w',
                       'Hl', 'Ln', 'Dn', 'Kt', 'Ba', 'Cn', 'Bi', 'Lb', 'St'
                       ])
        
    def _receive_card(self,card):
        self.holding.add(card)
        self.unknown.discard(card)
    
    def see_card(self,card):
        self.shown.add(card)
        self.unknown.discard(card)
        
    def guess(self):
        p = [x for x in self.unknown if x.isupper()]
        w = [x for x in self.unknown if x.islower()]
        r = [x for x in self.unknown if not x.isupper() and not x.islower()]
        a = random.sample(p,1)[0]
        b = random.sample(w,1)[0]
        c = random.sample(r,1)[0]
        g = [a,b,c]
        print(g)
        return(set(g))

def set_up(p,w,r,players=[[],[],[]]):
    p,w,r,c=choose(p,w,r)
    to_dist = p+w+r
    print(to_dist,c)
    random.shuffle(to_dist)
    distribute(to_dist,players)
    return(c)

def choose(p,w,r):
    random.shuffle(p)
    random.shuffle(w)
    random.shuffle(r)
    a = p.pop()
    b = w.pop()
    c = r.pop()
    conf = set([a,b,c])
    return(p,w,r,conf)
    
def distribute(cards,players):
    n = len(players)
    i = 0
    for card in cards:
        if i >= n:
            i = 0
        players[i]._receive_card(card)
        i+=1

def main(n=3):
    people = ['Y','P','G','B','R','W']
    weapons = ['k','c','v','r','l','w']
    rooms = ['Hl','Ln','Dn','Kt','Ba','Cn','Bi','Lb','St']
    players = []
    for _ in range(n):
        players.append(Player())
        
    confidential = set_up(people,weapons,rooms,players)

    solved = False
    round_ = 1

    while solved != True:
        print('Round %s' % str(round_))
        i=0
        for i in range(n):
            print('Player %s' % str(i))
            print(len(players[i].unknown))
            guess = players[i].guess()
            j = i
            shown = False
            for _ in range(n):
                j += 1
                if j >= n:
                    j = 0
                test = guess.intersection(players[j].holding)
                if bool(test):
                    players[i].see_card(random.sample(test,1)[0])
                    shown = True
                    break
            if shown == False:
                if guess == confidential:
                    solved = True
                    break
                else:
                    print('Player accused wrong')
        round_ +=1
    print('Solved!')
    print(confidential)
    print(guess)
    return(round_,i)
    
rounds = []
winner = []
for _ in range(10000):
    dat = main(5)
    rounds.append(dat[0])
    winner.append(dat[1])
plt.hist(rounds)
plt.show()
plt.hist(winner)
plt.show()
