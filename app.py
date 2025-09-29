from flask import Flask, render_template, request
import json
from main import main 

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])

def index():
    if request.method == 'POST':
        try:
            num_emails = int(request.form.get('value', 10))

        except ValueError:
            num_emails = 10
        
        
        main(max_emails=num_emails)


        with open('emails.json', encoding='utf-8') as f:
            emails = json.load(f)

        return render_template('emails.html', data=emails)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
