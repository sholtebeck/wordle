from flask import Flask, request, render_template
from wordle import commonwords, new_wordlist, save_guesses, wordscore, matching_words
from baseball import awards,teams,batstats,pitchstats,positions,get_players,get_description

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
    from datetime import datetime 
    return render_template('index.html',dotw=datetime.today().strftime("%A"))

@app.route('/grid', methods=['GET','POST'])
def grid():
    filters="  "
    players=description=None
    if request.method =="POST":
        form=request.form
        filters=sorted([form.get("filter1"),form.get("filter2")])
        description=get_description(filters)
        players=get_players(filters)
    return render_template('grid.html',description=description,filters=filters,players=players,awards=awards,batstats=batstats,pitchstats=pitchstats,positions=positions,teams=teams)

@app.route('/jumble', methods=['GET','POST'])
def jumble():
    inword=outword=None
    if request.method =="POST":
        inword=request.form.get('inword')
        outword=matching_words(inword)
    return render_template('jumble.html',inword=inword,outword=outword)

@app.route('/wordle', methods=['GET','POST'])
def wordle():
    dbwords=[]
    found=False
    foundword=""
    hints=""
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
            dbwords=save_guesses(guesses)
            foundword=word

    name = request.args.get("name", "Wordle")
    possible=len(wordlist)
    if len(wordlist)<500:
        hints=wordlist[-8:]
    return render_template('wordle.html',found=found, foundword=foundword, guesses=guesses, cguesses=convert(guesses),guessno=len(guesses)+1,hints=hints,possible=possible,name=name,dbwords=dbwords)

if __name__ == '__main__':
    app.run(threaded=True, host='0.0.0.0', port=5000)