import json
import random
import string
import sys

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
                result.append(letter.upper())
                tmp_solution[index] = '_'
                self.letters[letter] = MATCHED
            elif letter in tmp_solution:
                if self.letters[letter] != MATCHED:
                    self.letters[letter] = WRONG_PLACE
                if tmp_solution.count(letter) > word[index+1:].count(letter):
                    result.append(letter.lower())
                else:
                    result.append("_")
            else:
                if self.letters[letter] == UNKNOWN:
                    self.letters[letter] = NOTUSED
                result.append("_")
        return(result)

# For human 
if __name__ == "__main__":
    MAXTRY = 6
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
        print("".join(game.check_word(answer)))
        attempt += 1
    print("failed. answer: %s" % solution)
