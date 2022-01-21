import json
import random
import string
import sys

UNKNOWN = 0
NOTUSED = 1
WRONG_PLACE = 2
MATCHED = 3

letters = {}
for l in string.ascii_lowercase:
    letters[l] = UNKNOWN

def get_letter_status():
    return letters

def get_letter_status_str():
    result = []
    for l in string.ascii_lowercase:
        if letters[l] == UNKNOWN:
            result.append(l)
        elif letters[l] == WRONG_PLACE:
            result.append(l.upper())
        elif letters[l] == MATCHED:
            result.append("[" + l.upper() + "]")
    return "".join(result)
    
f = open('file_letters.json', 'r')
words = json.load(f)

def check_word(word, solution):
    global letters
    assert(len(word) == 5)
    result = []
    tmp_solution = list(solution)
    for index, letter in enumerate(word):
        #print("index: %d letter: %s word: %s tmp_solution: %s" % (index,letter,word,tmp_solution))
        if letter == tmp_solution[index]:
            result.append(letter.upper())
            tmp_solution[index] = '_'
            letters[letter] = MATCHED
        elif letter in tmp_solution:
            if letters[letter] != MATCHED:
                letters[letter] = WRONG_PLACE
            if tmp_solution.count(letter) > word[index+1:].count(letter):
                result.append(letter.lower())
            else:
                result.append("_")
        else:
            if letters[letter] == UNKNOWN:
                letters[letter] = NOTUSED
            result.append("_")
    return(result)
    

# For human 
if __name__ == "__main__":
    MAXTRY = 6
    attempt = 1
    if len(sys.argv) > 1:
        if sys.argv[1] not in words:
            print("%s is not in dictionary" % sys.argv[1])
            sys.exit(1)
        solution = sys.argv[1]
    else:
        solution = random.choice(words)
    while attempt <= MAXTRY:
        print(get_letter_status_str())
        answer = input()
        answer = answer.lower()
        if len(answer) != 5:
            print("answer must be 5 letters")
            continue
        if answer not in words:
            print("the word doesn't exist")
            continue
        if answer == solution:
            print("success! %d/%d" % (attempt, MAXTRY))
            exit()
        print("".join(check_word(answer, solution)))
        attempt += 1
    print("failed. answer: %s" % solution)
