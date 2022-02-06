import math

from string import ascii_lowercase

MIN_WORD_LEN = 2

class WordleSolver(object):

    def __init__(self, dict_file_path, word_len=5):
        if word_len < MIN_WORD_LEN:
            raise ValueError(f'minimum word_len == {MIN_WORD_LEN}')
        else:
            self.word_len = word_len

        self.dict_file_path = dict_file_path
        
        # overall word set
        self.word_list = list()

        self._load_dict()
        self.reset_game()

    # load dictionary, filter for length
    # relevant packages for ubuntu:
    # wamerican, wbritish, wcanadian
    # *-large | *-huge | *-insane | *-small if defaults don't work

    # currently just using /usr/share/dict/british-english

    def _load_dict(self):
        with open(self.dict_file_path, 'rt') as f:
            for word in f:
                word = word.strip()
                skip_word = False
                if len(word) == self.word_len:
                    for c in word:
                        if c not in ascii_lowercase:
                            skip_word = True
                            break
                    if not skip_word:
                        self.word_list.append(word)


    def reset_game(self):
        self.game_word_list = list(self.word_list)
        self.green_letter_set = set()


    # c must be present at position i, prune any words
    # that have any other letter there
    def add_green(self, i, c):
        new_game_word_list = list()
        # keep a set of these letters so we know what to do
        # if we get a grey on it later
        self.green_letter_set.add(c)
        for word in self.game_word_list:
            if word[i] == c:
                new_game_word_list.append(word)
        self.game_word_list = new_game_word_list

    
    # c must be present, but NOT at position i, prune
    # any words that have c at position i, and any words
    # that do not have c at all
    def add_yellow(self, i, c):
        new_game_word_list = list()
        for word in self.game_word_list:
            if c in word and word[i] != c:
                new_game_word_list.append(word)
        self.game_word_list = new_game_word_list


    # c is either not present at all, prune any words that contain c - OR -
    # c is already green somewhere, and not also present at i
    def add_grey(self, i, c):
        new_game_word_list = list()
        for word in self.game_word_list:
            if c not in word:
                new_game_word_list.append(word)
            elif c in self.green_letter_set and word[i] != c:
                new_game_word_list.append(word)
        self.game_word_list = new_game_word_list


    # add constraints in the form of a string, a bit more convenient
    # than separate function calls for interaction
    def feedback(self, s):
        # 0,c,{Gy,Ye,Gn}|...n,c,{Gy,Ye,Gn}
        # Gy - grey
        # Ye - yellow
        # Gn - green

        # do greens first, then yellows, then grey
        # greens must be done before greys, because we 
        # can get a green and a grey on the same letter
        # (repeated), and the order matters
        green_ops = list()
        yellow_ops = list()
        grey_ops = list()
        op_list = s.split('|')
        for op_s in op_list:
            (i, c, colour,) = op_s.split(',')
            if colour == 'Gn':
                green_ops.append((int(i), c,))
            elif colour == 'Ye':
                yellow_ops.append((int(i), c,))
            elif colour == 'Gy':
                grey_ops.append((int(i), c,)) 

        for (i, c,) in green_ops:
            self.add_green(i, c)
        for (i, c,) in yellow_ops:
            self.add_yellow(i, c)
        for (i, c,) in grey_ops:
            self.add_grey(i, c)


    def guess(self):
        # for each word in the game word set, figure out how 
        # much smaller the game word set gets if the solution 
        # was each other word, then rank each word by the average
        # change in word set, and return the one with the highest
        # average
        word_score_d = dict()
        for cur_score_word in self.game_word_list:
            cur_score_sum = 0
            for cur_constr_word in self.game_word_list:
                green_char_set = set()
                green_ops = list()
                yellow_ops = list()
                grey_ops = list()
                # do greens first
                for (i, inner_c,) in enumerate(cur_constr_word):
                    if inner_c == cur_score_word[i]:
                        green_ops.append((i, inner_c,))
                        green_char_set.add(inner_c)
                # now yellow and grey
                for (i, inner_c,) in enumerate(cur_constr_word):
                    if inner_c not in cur_score_word or (inner_c in green_char_set and inner_c != cur_score_word[i]):
                        grey_ops.append((i, inner_c,))
                    elif inner_c in cur_score_word:
                        yellow_ops.append((i, inner_c,))
                # now, with our constraints, go through all the words and see how many
                # words match them, this tell us how many words the game list would 
                # shrink by for cur_score_word if cur_constr_word were the solution 
                cur_guess_reduc_list = list()
                for cur_guess_word in self.game_word_list:
                    match_guess = True
                    for (green_i, green_c,) in green_ops:
                        if cur_guess_word[green_i] != green_c:
                            match_guess = False
                    for (yellow_i, yellow_c,) in yellow_ops:
                        if yellow_c not in cur_guess_word:
                            match_guess = False
                    for (grey_i, grey_c,) in grey_ops:
                        if grey_c not in green_char_set and grey_c in cur_guess_word:
                            match_guess = False
                    if match_guess:
                        cur_guess_reduc_list.append(cur_guess_word)
                cur_score_sum += len(self.game_word_list) - len(cur_guess_reduc_list)
            word_score_d[cur_score_word] = float(cur_score_sum / len(self.game_word_list))
        sorted_word_score_items_tl = sorted(word_score_d.items(), key=lambda i: i[1], reverse=True)
        guess_tup = sorted_word_score_items_tl[0]

        return guess_tup
