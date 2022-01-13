from string import ascii_lowercase

class WordleSolver(object):

    def __init__(self, dict_file_path, word_len):
        if word_len < 2:
            raise ValueError('minimum word_len == 2')
        else:
            self.word_len = word_len

        # in how many words does letter l occur n times?
        self.letter_freq_dl = dict()
        for c in ascii_lowercase:
            self.letter_freq_dl[c] = [0] * self.word_len

        # in how many words does digram dg occur n times?
        self.digram_freq_dl = dict()
        for i in range(self.word_len - 1):
            for c1 in ascii_lowercase:
                for c2 in ascii_lowercase:
                    dg = f'{c1}{c2}'
                    self.digram_freq_dl[dg] = [0] * self.word_len
 
        # in how many words does letter l appear at position i?
        self.letter_pos_freq_ld = [dict()] * self.word_len
        for i in range(self.word_len):
            self.letter_pos_freq_ld[i] = dict()
            for c in ascii_lowercase:
                self.letter_pos_freq_ld[i][c] = 0

        # in how many words does digram dg appear at position i?
        self.digram_pos_freq_ld = list()
        for i in range(self.word_len - 1):
            self.digram_pos_freq_ld[i] = dict()
            for c1 in ascii_lowercase:
                for c2 in ascii_lowercase:
                    dg = f'{c1}{c2}'
                    self.digram_pos_freq_ld[i][dg] = 0

        # overall word set
        self.word_set = set()

        # set of words with letter l at position p
        self.word_set_per_letter_per_pos = list()
        for i in range(self.word_len):
            self.word_set_per_letter_per_pos[i] = dict()
            for c in ascii_lowercase:
                self.word_set_per_letter_per_pos[i][c] = set()
        
        self.dict_file_path = dict_file_path

    # load dictionary, filter for length
    # relevant packages for ubuntu:
    # wamerican, wbritish, wcanadian
    # *-large | *-huge | *-insane | *-small if defaults don't work

    # currently just using wamerican - /usr/share/dict/words

    def _load_dict(self):
        with open(self.dict_file_path, 'rt') as f:
            for word in self.dict_file_path:
                if len(word) == self.word_len:
                    self.word_set.add(word)

    # freq analyse letters at each position, maybe digrams too?
    # freq analyse counts of letters in word, eg: letter 'e' appears
    # x times in y words, same with digrams
    #TODO - if this analysis is expensive enough, write something to save it to disk
    def _analyse_dict(self):
        for word in self.word_set:
            for (i, c,) in enumerate(word):

                # letter frequency at position
                self.letter_pos_freq_ld[i][c] += 1

                # digram frequency at position
                if i < (len(word) - 1):
                    dg = word[i:i+2]
                    self.digram_pos_freq_ld[i][dg] += 1

            # build sets of words by letter at position
            self.word_set_per_letter_per_pos[i][c].add(word)
                    
        # letter frequency in word
        for c in ascii_lowercase:
            c_count = word.count(c)
            self.letter_freq_dl[c][c_count] += 1

        # digram frequency in word
        for c1 in ascii_lowercase:
            for c2 in ascii_lowercase:
                dg = f'{c1}{c2}'
                cur_dg_count = 0
                for (i, _) in enumerate(word):
                    if i < (len(word) - 1):
                        cur_word_dg = word[i:i+2]
                        if cur_word_dg == dg:
                            cur_dg_count += 1
                self.digram_freq_dl[dg][cur_dg_count] += 1


    def reset_game(self):
        #TODO - reset game state


    # answer contains c at index i
    def add_green(self, i, c):
        #TODO - change game state


    # answer contains c, but NOT at index i
    def add_yellow(self, i, c):
        #TODO - change game state


    # answer does NOT contain c
    def add_grey(self, c):
        #TODO - change game state
