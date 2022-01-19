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
        self.word_set = set()

        self._load_dict()
        self._init_analysis()
        self._dict_analysis_stats()
        self._score_words()

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
                        self.word_set.add(word)


    # initialise all the analysis data structures
    def _init_analysis(self):

        # in how many words does letter l occur n times?
        """
        self.letter_freq_dl = dict()
        for c in ascii_lowercase:
            self.letter_freq_dl[c] = [0] * self.word_len
        """

        # in how many words does digram dg occur n times?
        """
        self.digram_freq_dl = dict()
        for i in range(self.word_len - 1):
            for c1 in ascii_lowercase:
                for c2 in ascii_lowercase:
                    dg = f'{c1}{c2}'
                    self.digram_freq_dl[dg] = [0] * self.word_len
        """
 
        # in how many words does letter l appear at position i?
        """
        self.letter_pos_freq_ld = [dict()] * self.word_len
        for i in range(self.word_len):
            self.letter_pos_freq_ld[i] = dict()
            for c in ascii_lowercase:
                self.letter_pos_freq_ld[i][c] = 0
        """

        # in how many words does digram dg appear at position i?
        self.digram_pos_freq_ld = [dict()] * self.word_len
        for i in range(self.word_len - 1):
            self.digram_pos_freq_ld[i] = dict()
            for c1 in ascii_lowercase:
                for c2 in ascii_lowercase:
                    dg = f'{c1}{c2}'
                    self.digram_pos_freq_ld[i][dg] = 0


        # set of words with letter l at position p
        """
        self.word_set_per_letter_per_pos = [dict()] * self.word_len
        for i in range(self.word_len):
            self.word_set_per_letter_per_pos[i] = dict()
            for c in ascii_lowercase:
                self.word_set_per_letter_per_pos[i][c] = set()
        """
         

    #NOTE - what should determine highest scoring word?
    # we either want to guess the exact word, or make a guess
    # that elicits the most useful feedback.
    # if we guess a word that has the most likely letters and digrams
    # at each position, we are more likely to get useful feedback

    # freq analyse letters at each position, maybe digrams too?
    # freq analyse counts of letters in word, eg: letter 'e' appears
    # x times in y words, same with digrams
    #TODO - if this analysis is expensive enough, write something to save it to disk
    #TODO - sort frequency stats
    def _dict_analysis_stats(self):
        for word in self.word_set:
            for (i, c,) in enumerate(word):

                # letter frequency at position
                #self.letter_pos_freq_ld[i][c] += 1

                # digram frequency at position
                if i < (len(word) - 1):
                    dg = word[i:i+2]
                    self.digram_pos_freq_ld[i][dg] += 1


                # build sets of words by letter at position
                #self.word_set_per_letter_per_pos[i][c].add(word)
                    
                # letter frequency in word
                """
                for c in ascii_lowercase:
                    c_count = word.count(c)
                    self.letter_freq_dl[c][c_count] += 1
                """

                # digram frequency in word
                """
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
                """

    def _score_words(self):
        #TODO - use sorted frequency stats to score each word and then sort the
        # set by score
        sorted_digram_pos_freq_ll = [ [None] * (26 ** 2) ] * self.word_len
        for i in range(self.word_len - 1):
            sorted_digram_pos_freq_ll[i] = sorted(self.digram_pos_freq_ld[i].items(), key=lambda i: i[1], reverse=True)

        word_score_tup_l = list()
        for word in self.word_set:
            score = 0
            for i in range(len(word) - 1):
                dg = word[i:i+2]
                # lowest index is top score
                cur_score = (26 ** 2) - sorted_digram_pos_freq_ll[i].index(dg)
                score += cur_score
            word_score_tup_l.append((word, score,))

        # created a set of words sorted by score, descending
        self.word_set = set(sorted(word_score_tup_l, key=lambda i: i[1]), reverse=True)


    def reset_game(self):
        self.game_word_set = set(self.word_set)
        self.green_letter_set = set()


    # c must be present at position i, prune any words
    # that have any other letter there
    def add_green(self, i, c):
        # keep a set of these letters so we know what to do
        # if we get a grey on it later
        self.green_letter_set.add(c)
        prune_set = set()
        for word in self.game_word_set:
            if word[i] != c:
                prune_set.add(word)

        self.game_word_set -= prune_set     

    
    # c must be present, but NOT at position i, prune
    # any words that have c at position i, and any words
    # that do not have c at all
    def add_yellow(self, i, c):
        prune_set = set()
        for word in self.game_word_set:
            if word[i] == c:
                prune_set.add(word)
            elif c not in word:
                prune_set.add(word)

        self.game_word_set -= prune_set


    # c is either not present at all, prune any words that contain c - OR -
    # c is already green somewhere, and not also present at i
    def add_grey(self, c, i):
        prune_set = set()
        if c in self.green_letter_set:
            for word in self.game_word_set:
                if word[i] == c:
                    prune_set.add(word)
        else:
            for word in self.game_word_set:
                if c in word:
                    prune_set.add(word)

        self.game_word_set -= prune_set


