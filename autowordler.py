import json
import random

f = open('file_letters.json', 'r')
words = json.load(f)
solution = random.choice(words)
#print(solution)

def check_word(word):
    assert(len(word) == 5)
    result = []
    tmp_solution = list(solution)
    for index, letter in enumerate(word):
        #print("index: %d letter: %s word: %s tmp_solution: %s" % (index,letter,word,tmp_solution))
        if letter == tmp_solution[index]:
            result.append(letter.upper())
            tmp_solution[index] = '_'
        elif letter in tmp_solution:
            if tmp_solution.count(letter) >= word[index+1:].count(letter):
                result.append(letter.lower())
        else:
            result.append("_")
    return(result)
    

# For human 
if __name__ == "__main__":
    MAXTRY = 6
    attempt = 1
    while attempt <= MAXTRY:
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
        print("".join(check_word(answer)))
        attempt += 1
    print("failed. answer: %s" % solution)
