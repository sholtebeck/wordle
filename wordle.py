#wordle functions
import random, datetime
#from wordb import insert_word
wordlines=open('./wordle5.txt').readlines()
commonwords=wordlines[0].strip()
uncommonwords=wordlines[1].strip()
allwords=commonwords+uncommonwords
wordloglines=[w.strip().split() for w in open('wordlog.txt').readlines()][-10:]
#wordlist=[w for w in wordlines if len(w)==5]
wordlist=[commonwords[x:x+5] for x in range(0,len(commonwords),5) if len(set(commonwords[x:x+5]))==5]
letters=[''.join(w[i] for w in wordlist) for i in range(5)]
percent= {letter:[len([word for word in wordlist if word[k]==letter]) for k in range(5)] for letter in set(commonwords)}

def wordscore(word):
    return sum([percent[word[k]][k] for k in range(5)])
    
def wordsort(word):
    return ''.join(sorted(w for w in word))    

def lastnwords(n=10):
    wordloglines=[w.strip().split() for w in open('./wordlog.txt').readlines()][-n:]
    wordloglines.sort(reverse=True)
    return [{"date":w[0],"word":w[2],"score":w[1][-3]} for w in wordloglines]

def matching_words(word):
    sortword=wordsort(word)
    outword=""
    for inline in open('./wordlist.txt').readlines():
        outword+=" ".join([inword for inword in inline.strip().split() if wordsort(inword)==sortword])
    return outword

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
    wordlist.sort(key=wordscore)
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
    todate=datetime.date.today().strftime("%Y-%m-%d")
    word=guesses[-1][0]
    line=todate+" #"+str(len(lines))+"("+str(len(guesses))+"): "+word+"\n"
    o=open('wordlog.txt','a')
    p=o.write(line)
    o.close() 
    #dbwords=insert_word(word,len(guesses),todate)
    dbwords=lastnwords(5)
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
    return dbwords

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

if __name__ == '__main__':
    print("Let's Play WORDLE")
    play_wordle()

