from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html", is_active=['true', 'false', 'false'])

@app.route('/courses')
def courses():
    return render_template("courses.html", is_active=['false', 'true', 'false'])

@app.route('/settings')
def settings():
    return render_template("settings.html", is_active=['false', 'false', 'true'])



if __name__ == '__main__':
    app.run(debug=True)