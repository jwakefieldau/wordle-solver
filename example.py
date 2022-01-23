from wordle import WordleSolver

def do_example():
    ws = WordleSolver('./wordle-words', 5)
    print(ws.guess())
    # mares
    ws.feedback('0,m,Ye|1,a,Gy|2,r,Ye|3,e,Gy|4,s,Gy')
    print(ws.guess())
    # grimy
    ws.feedback('0,g,Gy|1,r,Gn|2,i,Gn|3,m,Gn|4,y,Gy')
    print(ws.guess())
    # crimp - correct


if __name__ == '__main__':
    do_example()