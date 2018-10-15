import random

def deel(spelers=4, dekken=1):
    kaarten = ['1','2','3','4','5','6','7','8','9','10','J','Q','K']*4*dekken
    random.shuffle(kaarten)
    handen = [[] for _ in range(spelers)]
    j = 0
    for i in kaarten:
        handen[j].append(i)
        j = (j+1)*((j+1)%spelers!=0)
    return handen

def sort(hand):
    values = {'1': 14, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
              '8': 8, '9': 9, '10': 10, 'J': 11, 'Q':12, 'K':13}
    hand.sort(key=lambda x: values[x])

    
def waarde(hand):
    values = {'1': 14, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
              '8': 8, '9': 9, '10': 10, 'J': 11, 'Q':12, 'K':13}

    hand.sort(key=lambda x:values[x])
    return values[hand[-1]]

def check(nieuwhand, oudhand):
    if len(nieuwhand) > len(oudhand):
        return True
    elif waarde(nieuwhand) > waarde(oudhand) and len(nieuwhand)==len(oudhand):
        return True
    else:
        return False

values = values = {'1': 14, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
                   '8': 8, '9': 9, '10': 10, 'J': 11, 'Q':12, 'K':13}
