from flask import Flask,render_template,url_for,request,jsonify
from search import search, search_bio

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html',res = None, len=None, message = None)

@app.route('/predictTokens',methods=['POST'])
def predictTokens():
    if request.method == 'POST':
        message = request.form['message']
        if request.form.get('biography'):
            res = search_bio(message)
            if (len(res) == 0):
                res = ["ප්‍රතිඵල කිසිවක් හමු නොවීය.."]
                length = 0
            elif isinstance(res[0],list):
                length = len(res[0])
        else:
            res = search(message)
            if (len(res) == 0):
                res = ["ප්‍රතිඵල කිසිවක් හමු නොවීය.."]
                length = 0
            elif isinstance(res[0],list):
                length = len(res[0])
            else:
                length = 1
        # tokens = []
    return render_template('home.html', res = res, len = length, message = message)


if __name__ == '__main__':
    # serve(app, host='0.0.0.0', port=8000)
    app.run(debug=True)