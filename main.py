from flask import Flask, request, render_template
from wordle import commonwords, new_wordlist, save_guesses, wordscore

app = Flask(__name__)
guesses=[]

def convert(guesses):
    if type(guesses)== type([]):
        return ','.join('.'.join(g) for g in guesses)
    elif guesses == '':
        return []
    elif type(guesses)==type(''):
        return [tuple(g.split('.')) for g in guesses.split(',')]

@app.route('/', methods=['GET'])
def hello_world():
    return("hello world")


@app.route('/wordle', methods=['GET','POST'])
def hello_wordle():
    found=False
    foundword=""
    hints=[]
    guesses=[]
    wordlist=new_wordlist(commonwords)
    if request.method =="POST":
        word=request.form.get('word')
        result=request.form.get('result')
        guesses=convert(request.form.get('guesses'))
        guesses.append((word.lower(),result.upper()))
        found=result.upper()=='GGGGG'
        if not found:
            wordlist=new_wordlist(commonwords,guesses)
            wordlist.sort(key=wordscore)
        else:
            save_guesses(guesses)
            foundword=word

    name = request.args.get("name", "Wordle")
    possible=len(wordlist)
    if len(wordlist)<500:
        hints=wordlist[-8:]
    return render_template('wordle.html',found=found, foundword=foundword, guesses=guesses, cguesses=convert(guesses),guessno=len(guesses)+1,hints=hints,possible=possible,name=name)

if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=5000)