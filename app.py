from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html') 

@app.route('/htmx-test')
def htmx_text():
    return render_template('htmx/test-template.html') 

if __name__ == '__main__':
    app.run(debug=True)
