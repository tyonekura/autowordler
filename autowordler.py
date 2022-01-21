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

f = open('file_letters.json', 'r')
words = json.load(f)

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

def guess(letter_status, history, candidates):
    return "teams"

def solve(solution):
    game = Wordle(solution)
    attempt = 1
    history = []
    candidates = copy.copy(words)
    while attempt <= MAXTRY:
        letter_status = game.get_letter_status()
        print(letter_status)
        word = guess(letter_status, history, candidates)
        result = game.check_word(word)
        print(result)
        if check_result(result):
            return attempt
        attempt += 1
    return 1000

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
