from string import ascii_lowercase

MIN_WORD_LEN = 2

class WordleSolver(object):

    def __init__(self, dict_file_path, word_len):
        if word_len < MIN_WORD_LEN:
            raise ValueError(f'minimum word_len == {MIN_WORD_LEN}')
        else:
            self.word_len = word_len

        self.dict_file_path = dict_file_path
        
        # overall word set
        self.word_list = list()

        self._load_dict()
        self._init_analysis()
        self._dict_analysis_stats()
        self._word_scores()

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


    # initialise all the analysis data structures
    def _init_analysis(self):

        # in how many words does digram dg appear at position i?
        self.digram_pos_freq_ld = [dict()] * self.word_len
        for i in range(self.word_len - 1):
            self.digram_pos_freq_ld[i] = dict()
            for c1 in ascii_lowercase:
                for c2 in ascii_lowercase:
                    dg = f'{c1}{c2}'
                    self.digram_pos_freq_ld[i][dg] = 0
        

    #NOTE - what should determine highest scoring word?
    # we either want to guess the exact word, or make a guess
    # that elicits the most useful feedback.
    # if we guess a word that has the most likely letters and digrams
    # at each position, we are more likely to get useful feedback

    # freq analyse letters at each position, maybe digrams too?
    # freq analyse counts of letters in word, eg: letter 'e' appears
    # x times in y words, same with digrams
    def _dict_analysis_stats(self):
        for word in self.word_list:
            for (i, c,) in enumerate(word):

                # digram frequency at position
                if i < (len(word) - 1):
                    dg = word[i:i+2]
                    self.digram_pos_freq_ld[i][dg] += 1


    def _word_scores(self):
        # use sorted frequency stats to score each word and then sort the
        # list by score
        sorted_digram_pos_freq = [ [None] * (26 ** 2) ] * (self.word_len - 1)
        for i in range(self.word_len - 1):
            sorted_digram_pos_freq[i] = sorted(self.digram_pos_freq_ld[i].items(), key=lambda i: i[1], reverse=True)

        word_score_tup_l = list()
        for word in self.word_list:
            score = 0
            for i in range(len(word) - 1):
                dg = word[i:i+2]
                # lowest index is top score
                found_dg = False
                for (cur_dg, cur_dg_freq,) in sorted_digram_pos_freq[i]:
                    if cur_dg == dg:
                        found_dg = True
                        break
                if not found_dg:
                    raise ValueError(f'unable to find digram {dg} in sorted frequency list at position {i}')
                score += cur_dg_freq
            word_score_tup_l.append((word, score,))

        # created a set of words sorted by score, descending
        self.word_score_tup_l = sorted(word_score_tup_l, key=lambda i: i[1], reverse=True)


    def reset_game(self):
        self.game_word_score_tup_l = list(self.word_score_tup_l)
        self.green_letter_set = set()


    # c must be present at position i, prune any words
    # that have any other letter there
    def add_green(self, i, c):
        new_game_word_score_tup_l = list()
        # keep a set of these letters so we know what to do
        # if we get a grey on it later
        self.green_letter_set.add(c)
        for (word, score,) in self.game_word_score_tup_l:
            if word[i] == c:
                new_game_word_score_tup_l.append((word, score,))
        self.game_word_score_tup_l = new_game_word_score_tup_l

    
    # c must be present, but NOT at position i, prune
    # any words that have c at position i, and any words
    # that do not have c at all
    def add_yellow(self, i, c):
        new_game_word_score_tup_l = list()
        for (word, score,) in self.game_word_score_tup_l:
            if c in word and word[i] != c:
                new_game_word_score_tup_l.append((word, score,))
        self.game_word_score_tup_l = new_game_word_score_tup_l


    # c is either not present at all, prune any words that contain c - OR -
    # c is already green somewhere, and not also present at i
    def add_grey(self, i, c):
        new_game_word_score_tup_l = list()
        for (word, score,) in self.game_word_score_tup_l:
            if c not in word:
                new_game_word_score_tup_l.append((word, score,))
            elif c in self.green_letter_set and word[i] != c:
                new_game_word_score_tup_l.append((word, score,))
        self.game_word_score_tup_l = new_game_word_score_tup_l


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



    # return the top scoring available word, score tuple
    def guess(self):
        return self.game_word_score_tup_l[0]