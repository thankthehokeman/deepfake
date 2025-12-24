from flask import Flask, render_template, request, redirect, url_for, session
import random
import os

app = Flask(__name__)
app.secret_key='V,="z($ct8eRVe$iOqa!MzN.0`v*9Y'

@app.route('/')
def index():
    return redirect(get_front_page_url())

@app.route('/hello')
def hello():
    session["front_page"] = "good"
    return render_template('hello.html')

@app.route('/hi')
def hi():
    session["front_page"] = "bad"
    return render_template('hi.html')

@app.route('/greetings')
def greetings():
    session["front_page"] = "neutral"
    return render_template('greetings.html')

def get_front_page_url():
    front_page = session.get("front_page")

    if front_page == "good":
        return url_for("hello")
    elif front_page == "bad":
        return url_for("hi")
    elif front_page == "neutral":
        return url_for("greetings")

DEEPFAKE_BASENAMES = ["image_2", "image_4", "image_5", "image_8"]

def is_deepfake(filename):
    basename = os.path.basename(filename)
    name, _ext = os.path.splitext(basename)
    return name.lower() in DEEPFAKE_BASENAMES

@app.route('/uploads', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return "There is no image so please upload one", 400
        
    file = request.files['image']

    if file.filename == '':
        return "Please upload something"
        
    filename = file.filename
    deepfake = is_deepfake(filename)
    loading_time = random.randint(2, 5)

    session["allow_loading"] = True
    session["last_deepfake"] = deepfake
    session["last_filename"] = filename
    session["allow_results"] = True
    session["wait_seconds"] = loading_time
        
    return redirect(url_for("loading"))

@app.route('/loading')
def loading():
    if not session.get("allow_loading"):
        return redirect(get_front_page_url())
    
    session["allow_loading"] = False

    if "last_filename" not in session:
        return redirect(get_front_page_url())

    filename = session["last_filename"]
    wait_seconds = session.get("wait_seconds")

    return render_template('loading.html', filename = filename, front_page_url = get_front_page_url(), wait_seconds = wait_seconds)

@app.route('/results')
def results():
    if not session.get("allow_results"):
        return redirect(get_front_page_url())
    
    session["allow_results"] = False

    if "last_filename" not in session:
        return redirect(get_front_page_url())  
    
    filename = session["last_filename"]
    deepfake = session["last_deepfake"]

    if deepfake:
        verdict = "This is a deepfake."
    else:
         verdict = "This is not a deepfake."

    status_text = verdict

    return render_template('results.html', filename = filename, front_page_url = get_front_page_url(), status_text = status_text)

if __name__ == "__main__":
    app.run(port=8000, debug=True)