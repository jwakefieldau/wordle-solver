from wordle import WordleSolver

def do_example():
    ws = WordleSolver('/usr/share/dict/british-english', 5)
    print(ws.guess())
    # bares
    ws.add_yellow(0, 'b')
    ws.add_grey(1, 'a')
    ws.add_yellow(2, 'r')
    ws.add_grey(3, 'e')
    ws.add_grey(4, 's')
    print(ws.guess())
    # crumb
    ws.add_grey(0, 'c')
    ws.add_yellow(1, 'r')
    ws.add_grey(2, 'u')
    ws.add_grey(3, 'm')
    ws.add_yellow(4, 'b')
    print(ws.guess())
    # robin
    ws.add_green(0, 'r')
    ws.add_green(1, 'o')
    ws.add_green(2, 'b')
    ws.add_grey(3, 'i')
    ws.add_grey(4, 'n')
    print(ws.guess())
    # robot - correct


if __name__ == '__main__':
    do_example()