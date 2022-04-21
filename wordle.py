import random, datetime
wordlines=open('wordle5.txt').readlines()
commonwords=wordlines[0].strip() 
uncommonwords=wordlines[1].strip()      
allwords=commonwords+uncommonwords
wordlist=[commonwords[x:x+5] for x in range(0,len(commonwords),5) if len(set(commonwords[x:x+5]))==5]
letters=[''.join(w[i] for w in wordlist) for i in range(5)]
percent={w:round(commonwords.count(w)/len(commonwords),3) for w in set(commonwords)}
counts={w:[letters[i].count(w) for i in range(5)] for w in percent.keys()}

def wordscore(word):
    return sum(percent[w] for w in set(word))

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
            elif guess[x]=='R' and word.count(word[x])<2:
                wordlist=[w for w in wordlist if word[x] not in w]
            elif guess[x]=='-':
                wordlist=[w for w in wordlist if len(w)==len(set(w))]
    if len(wordlist)>0 or words==uncommonwords:
        return wordlist
    else:
        return new_wordlist(uncommonwords,guesses)

# save the latest guesses 
def save_guesses(guesses):
    lines=open('wordlog.txt').readlines()
    todate=datetime.date.today().strftime("%m/%d")     
    word=guesses[-1][0]
    line=todate+" - #"+str(len(lines))+"("+str(len(guesses))+"): "+word+"\n"
    o=open('wordlog.txt','a')
    p=o.write(line)
    o.close()
    cwords=new_wordlist(commonwords)
    uwords=new_wordlist(uncommonwords)
    if word in cwords:
        cwords.remove(word)
        uwords.append(word)
        uwords.sort()
        o=open("wordle5.txt","w")
        p=o.write(''.join(cwords)+"\n")
        q=o.write(''.join(uwords))
        o.close()      

def play_wordle(words=commonwords):
    wordlist,guesses,found=new_wordlist(words),[],False
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
        wordlist=new_wordlist(words,guesses)
        wordlist.sort(key=wordscore)
    if found:
        print("found",guesses[-1][0],"in",len(guesses),'guesses')
        save_guesses(guesses)        
            
print("Let's Play WORDLE") 
play_wordle()
		
      