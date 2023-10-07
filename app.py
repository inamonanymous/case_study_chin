from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route('/') 
def index():
    return f"hi"

if __name__ == "__main__":
    app.run(debug=True)