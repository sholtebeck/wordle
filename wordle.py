import random
wordlines=open('wordle5.txt').readlines()
commonwords=wordlines[0] 
allwords=wordlines[1]      
counts={w:commonwords.count(w) for w in set(commonwords)}
#wordlist=new_wordlist(allwords,[])

def wordscore(word):
    return sum(counts[w] for w in set(word))

def random_word(words=commonwords):
    wordlist=new_wordlist(words)  
    return wordlist[random.randrange(len(wordlist))]

def get_guess(secret,guess):
    res=''
    for x in range(len(secret)):
        if secret[x]==guess[x]:
            res+='G'
        elif guess[x] in secret:
            res+='Y'
        else:
            res+='R'
    return (guess,res)

def new_wordlist(words=commonwords,guesses=[]):
    wordlist=[words[x:x+5] for x in range(0,len(words),5)]
    for word,guess in guesses:
        for x in range(len(word)):
            if guess[x]=='G':
                wordlist=[w for w in wordlist if w[x]==word[x]]
            elif guess[x]=='Y':
                wordlist=[w for w in wordlist if word[x] in w and word[x]!=w[x]]
            elif guess[x]=='R':
                wordlist=[w for w in wordlist if word[x] not in w]
    if len(wordlist)>0 or words==allwords:
        return wordlist
    else:
        return new_wordlist(allwords,guesses)

def play_wordle():
    wordlist,guesses,found=new_wordlist(commonwords),[],False
    wordlist.sort(key=wordscore)
    while not found:
        print(len(wordlist),"possible words",wordlist[-5:])
        guessno="Guess#"+str(len(guesses)+1)+"["+wordlist[-1]+"]:"
        ressno="Result#"+str(len(guesses)+1)+":"
        word=input(guessno)
        if len(word)==0:
            word=wordlist[-1]
        result=input(ressno)
        if len(word)==len(result)==5:
            guesses.append((word,result.upper()))
            found=result.upper()=='GGGGG'
        else:
            print("invalid word length")    
        wordlist=new_wordlist(commonwords,guesses)
        wordlist.sort(key=wordscore)
    if found:
        print("found",guesses[-1][0],"in",len(guesses),'guesses')        
            
print("Let's Play WORDLE") 
play_wordle()
		
      