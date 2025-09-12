from flask import Flask, render_template, request
import json
from main import main 

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            num_emails = int(request.form.get('count', 10))
        except ValueError:
            num_emails = 10
        
        # Call your main function to fetch emails & create JSON file
        main(max_emails=num_emails)

        # Now load the generated JSON file
        with open('emails.json', encoding='utf-8') as f:
            emails = json.load(f)

        return render_template('emails.html', emails=emails)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
