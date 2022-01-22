from wordle import WordleSolver

def do_example():
    ws = WordleSolver('./wordle-words', 5)
    print(ws.guess())
    # mares
    ws.feedback('0,m,Ye|1,a,Gy|2,r,Ye|3,e,Gy|4,s,Gy')
    print(ws.guess())
    # roomy
    ws.feedback('0,r,Ye|1,o,Gy|2,o,Gy|3,m,Gn|4,y,Gy')
    print(ws.guess())
    # crimp - correct


if __name__ == '__main__':
    do_example()