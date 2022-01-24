# autowordler

## What is Wordle? 

It's a word guessing game. https://www.powerlanguage.co.uk/wordle/

## What is data set?

I don't know. I'm using a 5 letter words list generated from

 https://github.com/benjamincrom/scrabble/blob/master/scrabble/dictionary.json

I don't include it because I'm not sure about licensing of scrabble words.

It has 8636 words. Considering official Wordle site accepts porin or xylyl, I think it's very close to official one.

## What strategy does this simulator use?

There are 4 mode. Currently this simulator is following hard mode rule, which must use already known letters.

### Best average steps
This uses most boring words. The definition is, count all letters in all words, and add the value for each word, but one letter is counted once for one word.
For example, If A's score is 100, B is 70, C is 50, "AA" is 100 and "BC" is 120. That makes 5 letter words more valuable.

### Best success rate
It chooses least boring words but with 5 different letters. It only use it for first 3 attempts AND there is more than 100 candidates.
Because of hard mode rule, it can give better coverage by missing minor letters first.

### Random
Pick up a word randomly from valid candidates.

### Prefix
It checks bumpy -> vital -> whose if applicable. That's combination I used to use.

## Test result with all words
With all scrabble words, test showed:

AVG_STEP
Success rate: 0.884090 Average step: 4.275835

SUCCESS_RATE
Success rate: 0.919407 Average step: 4.728967

RANDOM
Success rate: 0.856068 Average step: 4.544163

PREFIX (bumpy->vital->whose)
Success rate: 0.925544 Average step: 4.434755

It showed using boring words gives best step count. Using Prefix mode is actually better than Success rate mode.

## Test result with 2022 Wordle answers
Using Wordle answers as of Jan 23, 

AVG_STEP
success rate: 1.000000 Average step: 3.956522

SUCCESS_RATE
success rate: 1.000000 Average step: 4.521739

RANDOM
success rate: 0.939130 Average step: 4.486150

PREFIX
success rate: 1.000000 Average step: 4.130435

# Possible improvement
Considering words are picked up by Wordle author, some optimization can be done.

1. Words that are too minor are not chosen. 
2. We can exclude all words that were already used.
3. pural words are less likely chosen. (I've not checked if it's ever. 2695 of 8636 ends with S. So, I can ignore those words until there is no candidate left.


