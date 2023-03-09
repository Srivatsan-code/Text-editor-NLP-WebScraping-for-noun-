from distutils import text_file
import flask
from flask import Flask, request, render_template
import json
import main
from predict import predict
import webscrap
app = Flask(__name__)
import nltk
import spelling
import language_tool_python
tool = language_tool_python.LanguageTool('en-US')
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_end_predictions', methods=['post'])
def get_prediction_eos():
    input_lis = (request.json['input_text'].split()) #[how,are,you]
    n_word=input_lis[-1]
    st=""
    nxt=""
    if len(input_lis)>=3:
        res_lis = input_lis[-3:]
        for w in res_lis:
            st+=w+" "
    lines = n_word
    # function to test if something is a noun
    is_noun = lambda pos: pos[:2] == 'NN'
    # do the nlp stuff
    tokenized = nltk.word_tokenize(lines)
    nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)] 
    if len(nouns)==0:
        try:
            input_text = ' '.join(request.json['input_text'].split()) #[how,are,you]
            input_text += ' <mask>'
            top_k = request.json['top_k']
            if len(input_lis)>=3:
                st=st[:-1]
                nxt=predict(st)
                print(nxt+" THIS IS FROM LSTM....")
            res = main.get_all_predictions(input_text, top_clean=int(top_k))
            if nxt!="":
               res[0]=nxt
            spell=spelling.spellcheck(n_word)
            if(spell!=""):
                res["st"]=spell
            print(res)
            return app.response_class(response=json.dumps(res), status=200, mimetype='application/json')
        except Exception as error:
            err = str(error)
            print(err)
            return app.response_class(response=json.dumps(err), status=500, mimetype='application/json')
    else:
        input_text = ' '.join(request.json['input_text'].split()) #[how,are,you]
        input_text += ' <mask>'
        top_k = request.json['top_k']
        web=webscrap.web_scraping(n_word)
        res = main.get_all_predictions(input_text, top_clean=int(top_k))
        spell=spelling.spellcheck(n_word)
        if(spell!=""):
            res["st"]=spell
        if(web!=""):
            res["k"]=web
        print(res)
        return app.response_class(response=json.dumps(res), status=200, mimetype='application/json')      
@app.route("/chat-reply", methods=["post"])
def reply():
    input_text = request.json["input_text"]
    type(input_text)
    text = input_text
    res = tool.correct(text)

    res = {"reply": res}
    print(res)
    return app.response_class(
        response=json.dumps(res),
        status=200,
        mimetype="application/json",
    )
@app.route('/get_mask_predictions', methods=['post'])
def get_prediction_mask():
    try:
        input_text = ' '.join(request.json['input_text'].split())
        top_k = request.json['top_k']
        res = main.get_all_predictions(input_text, top_clean=int(top_k))
        return app.response_class(response=json.dumps(res), status=200, mimetype='application/json')
    except Exception as error:
        err = str(error)
        print(err)
        return app.response_class(response=json.dumps(err), status=500, mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000, use_reloader=False)
