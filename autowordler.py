import json
import random
import string
import sys
import copy

MAXTRY = 6

UNKNOWN = 0
NOTUSED = 1
WRONG_PLACE = 2
MATCHED = 3

FAIL = -1

f = open('five_letters.json', 'r')
words = json.load(f)

def count_letters():
    letter_dict = {}
    for l in string.ascii_lowercase:
        letter_dict[l] = 0
    for w in words:
        for l in w:
            letter_dict[l] += 1
    return letter_dict

def evaluate_words():
    word_dict = {}
    letter_dict = count_letters()
    for w in words:
        v = 0
        # only count same letter once
        for l in set(w):
            v += letter_dict[l]
        word_dict[w] = v
    return {k:v for k,v in sorted(word_dict.items(), key=lambda item: item[1],
        reverse=True)}

def get_word_rank(word):
    sorted_words = list(evaluate_words().keys())
    return sorted_words.index(word) + 1

class Wordle(object):
    def __init__(self, solution=None):
        if solution is not None:
            self.solution = solution
        else:
            self.solution = random.choice(words)

        self.letters = {}
        for l in string.ascii_lowercase:
            self.letters[l] = UNKNOWN

    def get_letter_status(self):
        return self.letters

    def get_letter_status_str(self):
        result = []
        for l in string.ascii_lowercase:
            if self.letters[l] == UNKNOWN:
                result.append(l)
            elif self.letters[l] == WRONG_PLACE:
                result.append(l.upper())
            elif self.letters[l] == MATCHED:
                result.append("[" + l.upper() + "]")
        return "".join(result)
    
    def check_word(self, word):
        assert(len(word) == 5)
        result = []
        tmp_solution = list(self.solution)
        for index, letter in enumerate(word):
            #print("index: %d letter: %s word: %s tmp_solution: %s" % (index,letter,word,tmp_solution))
            if letter == tmp_solution[index]:
                result.append((letter, MATCHED))
                tmp_solution[index] = '_'
                self.letters[letter] = MATCHED
            elif letter in tmp_solution:
                if self.letters[letter] != MATCHED:
                    self.letters[letter] = WRONG_PLACE
                if tmp_solution.count(letter) > word[index+1:].count(letter):
                    result.append((letter, WRONG_PLACE))
                else:
                    result.append((letter, NOTUSED))
            else:
                if self.letters[letter] == UNKNOWN:
                    self.letters[letter] = NOTUSED
                result.append((letter, NOTUSED))
        return(result)

    def check_word_str(self, word):
        new_result = []
        result = self.check_word(word)
        for l, state in result:
            if state == NOTUSED:
                new_result.append("_")
            elif state == WRONG_PLACE:
                new_result.append(l.lower())
            elif state == MATCHED:
                new_result.append(l.upper())
            else:
                assert(False)
        return "".join(new_result)

def check_result(result):
    return all([status == MATCHED for (l, status) in result])

def get_most_bored(candidates):
    return candidates[0]

def get_most_rare(candidates):
    for w in reversed(candidates):
        if len(set(w)) == 5:
            return w
    # didn't find 5 letter rare words
    return candidates[0]

def update_candidates(result, candidates):
    new_candidates = []
    for word in candidates:
        removed = False
        removing_letters = set()
        keeping_letters = set()
        for index, (l, status) in enumerate(result):
            if status == NOTUSED:
                removing_letters.add(l)
            elif status == MATCHED:
                if word[index] != l:
                    removed = True
                else:
                    keeping_letters.add(l)
            elif status == WRONG_PLACE:
                if l not in word:
                    removed = True
                elif word[index] == l:
                    removed = True
                else:
                    keeping_letters.add(l)
        for letter in removing_letters:
            if letter not in keeping_letters and letter in word:
                removed = True
        if not removed:
            new_candidates.append(word)
    return new_candidates

def sort_candidates(candidates):
    ret = []
    sorted_words = evaluate_words()
    for k in sorted_words.keys():
        if k not in candidates:
            continue
        ret.append(k)
    return ret

AVG_STEP = 0
SUCCESS_RATE = 1    
RANDOM = 2
PREFIX = 3

def solve(solution, first_word=None, candidates=None, mode=AVG_STEP):
    game = Wordle(solution)
    attempt = 1
    can_prefix = True
    if not candidates:
        candidates = copy.copy(words)
    while attempt <= MAXTRY:
        letter_status = game.get_letter_status()
        #print(letter_status)
        if mode == PREFIX:
            if attempt == 1:
                word = 'whose'
            elif attempt == 2:
                if can_prefix and 'vital' in candidates:
                    word = 'vital'
                else:
                    can_prefix = False
                    word = get_most_bored(candidates)
            elif attempt == 3:
                if can_prefix and 'bumpy' in candidates:
                    word = 'bumpy'
                else:
                    can_prefix = False
                    word = get_most_bored(candidates)
            else:
                word = get_most_bored(candidates)
        elif attempt == 1 and first_word:
            word = first_word
        else:
            if mode == RANDOM:
                word = random.choice(candidates)
            elif mode == SUCCESS_RATE:
                if len(candidates) > 100 and attempt <= 3:
                    word = get_most_rare(candidates)
                else:
                    word = get_most_bored(candidates)
            elif mode == AVG_STEP:
                word = get_most_bored(candidates)
        print("%d: trying %s with %d candidates" % (attempt, word, len(candidates)))
        result = game.check_word(word)
        #print(result)
        if check_result(result):
            return attempt
        candidates.remove(word)
        candidates = update_candidates(result, candidates)
        if not candidates:
            print("no candidate for %s. %s" % (game.solution, game.get_letter_status_str()))
            return FAIL
        attempt += 1
    #print(candidates)
    return FAIL

def test(num, first_word=None, fixed_solution=None, mode=AVG_STEP):
    random.seed(0)
    success = []
    failure = []
    sum = 0
    sorted_candidates = copy.copy(words)
    sorted_candidates = sort_candidates(sorted_candidates)
    for i in range(num):
        candidates = copy.copy(sorted_candidates)
        if fixed_solution:
            w = fixed_solution
        else:
            w = random.choice(words)
        n = solve(w, first_word, candidates=candidates, mode=mode)
        if n == FAIL:
            failure.append(w)
        else:
            sum += n
            success.append((w, n))
    print("Success rate: %f Average step: %f" % (len(success)/num, sum/len(success)))
    return success, failure

# For human 
if __name__ == "__main__":
    attempt = 1
    if len(sys.argv) > 1:
        solution = sys.argv[1]
        if solution not in words:
            print("%s is not in dictionary" % solution)
            sys.exit(1)
        game = Wordle(solution)
    else:
        game = Wordle()
    while attempt <= MAXTRY:
        print(game.get_letter_status_str())
        answer = input()
        answer = answer.lower()
        if len(answer) != 5:
            print("answer must be 5 letters")
            continue
        if answer not in words:
            print("the word doesn't exist")
            continue
        if answer == game.solution:
            print("success! %d/%d" % (attempt, MAXTRY))
            exit()
        print(game.check_word_str(answer))
        attempt += 1
    print("failed. answer: %s" % solution)
