from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, after_this_request
from PIL import Image
import random
import time
import os
from werkzeug.utils import secure_filename

GALLERY_FOLDER = "static/gallery"
UPLOAD_FOLDER = "static/uploads"

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", 'secret_key')
app.config["GALLERY_FOLDER"] = GALLERY_FOLDER
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route('/')
def home():
    return redirect(get_front_page_url())

@app.route('/hello')
def hello():
    session["front_page"] = "good"
    return render_template(
        'home.html', 
        front_page_url = get_front_page_url(), 
        page_css = "css/good.css", 
        pico_css = "css/pico.slate.min.css",
        gallery_images=GALLERY_IMAGES
    )

@app.route('/hi')
def hi():
    session["front_page"] = "bad"
    return render_template(
        'home.html', 
        front_page_url = get_front_page_url(), 
        page_css = "css/bad.css", 
        pico_css = "css/pico.grey.min.css",
        gallery_images=GALLERY_IMAGES
    )

@app.route('/greetings')
def greetings():
    session["front_page"] = "neutral"
    return render_template(
        'home.html', 
        front_page_url = get_front_page_url(), 
        page_css = "css/neutral.css", 
        pico_css = "css/pico.grey.min.css",
        gallery_images=GALLERY_IMAGES
    )

def get_front_page_url():
    front_page = session.get("front_page")

    if front_page == "good":
        return url_for("hello")
    elif front_page == "bad":
        return url_for("hi")
    elif front_page == "neutral":
        return url_for("greetings")

DEEPFAKE_BASENAMES = ["image_2", "image_5", "image_7", "image_8", "image_10", "image_11", "image_16", "image_19"]
GALLERY_IMAGES = ['image_1.png', 'image_2.png', 'image_3.png', 'image_4.png', 
                  'image_5.png', 'image_6.png', 'image_7.png', 'image_8.png', 
                  'image_9.png', 'image_10.png', 'image_11.png', 'image_12.png', 
                  'image_13.png', 'image_14.png', 'image_15.png', 'image_16.png', 
                  'image_17.png', 'image_18.png', 'image_19.png', 'image_20.png'
                 ]

def is_deepfake(filename):
    basename = os.path.basename(filename)
    name, _ext = os.path.splitext(basename)
    return name.lower() in DEEPFAKE_BASENAMES

def score_results(deepfake: bool):
    if deepfake:
        overall_prc = random.randint(86, 97)
    else:
        overall_prc = random.randint(10, 35)

    deepcheck = overall_prc + random.randint(-3, 3)
    sightlook = overall_prc + random.randint(-5, 5)
    frameguard = overall_prc + random.randint(-4, 4)
    forgescan = overall_prc + random.randint(-2, 2)

    return overall_prc, deepcheck, sightlook, frameguard, forgescan

@app.route('/uploads', methods=['GET', 'POST'])
def upload():

    start_ms = time.time()
    gallery_choice = request.form.get("gallery_choice")

    if gallery_choice:
        if gallery_choice not in GALLERY_IMAGES:
            return "Invalid gallery image selection", 400
        
        filename = gallery_choice
        image_path = os.path.join(app.config["GALLERY_FOLDER"], filename)

        if not os.path.exists(image_path):
                return "Gallery image not found.", 400
    
        image_size = os.path.getsize(image_path) // 1024
        deepfake = is_deepfake(filename)
        loading_time = random.randint(1, 3)
        overall_prc, deepcheck, sightlook, frameguard, forgescan = score_results(deepfake)
        

        try:
            with Image.open(image_path) as img:
                width, height = img.size
        except Exception:
            return "Please upload a valid image file", 400

        elapsed_ms = int((time.time() - start_ms) * 1000)

        session["source"] = "gallery"
        session["allow_loading"] = True
        session["last_deepfake"] = deepfake
        session["last_filename"] = filename
        session["allow_results"] = True
        session["wait_seconds"] = loading_time
        session["overall_percent"] = overall_prc
        session["deepcheck"] = deepcheck
        session["sightlook"] = sightlook
        session["frameguard"] = frameguard
        session["forgescan"] = forgescan
        session["img_mimetype"] = "image/png"
        session["img_size"] = int(image_size)
        session["img_width"] = int(width)
        session["img_height"] = int(height)
        session["img_ms"] = elapsed_ms
            
        return redirect(url_for("loading"))
    else:
        if 'image' not in request.files:
            return "There is no image so please upload one", 400
            
        file = request.files['image']

        if file.filename == '':
            return "Please upload something"
            
        filename = secure_filename(file.filename)
        
        image_path = (os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file.save(image_path)
        image_size = os.path.getsize(image_path) // 1024
        deepfake = is_deepfake(filename)
        loading_time = random.randint(1, 3)
        overall_prc, deepcheck, sightlook, frameguard, forgescan = score_results(deepfake)
        

        try:
            with Image.open(image_path) as img:
                width, height = img.size
        except Exception:
            return "Please upload a valid image file", 400

        elapsed_ms = int((time.time() - start_ms) * 1000)

        session["source"] = "upload"
        session["allow_loading"] = True
        session["last_deepfake"] = deepfake
        session["last_filename"] = filename
        session["allow_results"] = True
        session["wait_seconds"] = loading_time
        session["overall_percent"] = overall_prc
        session["deepcheck"] = deepcheck
        session["sightlook"] = sightlook
        session["frameguard"] = frameguard
        session["forgescan"] = forgescan
        session["img_mimetype"] = file.mimetype
        session["img_size"] = int(image_size)
        session["img_width"] = int(width)
        session["img_height"] = int(height)
        session["img_ms"] = elapsed_ms
            
        return redirect(url_for("loading"))

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    image_path = (os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    @after_this_request
    def remove_file(response):
        try:
            os.remove(image_path)
        except OSError:
            pass
        return response
    
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/gallery/<filename>")
def gallery_file(filename):    
    return send_from_directory(app.config["GALLERY_FOLDER"], filename)

@app.route('/loading')
def loading():

    if not session.get("allow_loading"):
        return redirect(get_front_page_url())
    
    session["allow_loading"] = False

    if "last_filename" not in session:
        return redirect(get_front_page_url())

    filename = session["last_filename"]
    wait_seconds = session.get("wait_seconds")

    return render_template(
        'loading.html',
        filename = filename, 
        front_page_url = get_front_page_url(), 
        wait_seconds = wait_seconds,
    )


@app.route('/results')
def results():
    if not session.get("allow_results"):
        return redirect(get_front_page_url())
    
    session["allow_results"] = False

    if "last_filename" not in session:
        return redirect(get_front_page_url())  
    
    filename = session["last_filename"]
    deepfake = session["last_deepfake"]
    overall_prc = session.get("overall_percent")
    deepcheck = session.get("deepcheck")
    sightlook = session.get("sightlook")
    frameguard = session.get("frameguard")
    forgescan = session.get("forgescan")
    source = session.get("source", "upload")
    if source == "gallery":
        img_url = url_for("gallery_file", filename=filename)
    else:
        img_url = url_for("uploaded_file", filename=filename)
    img_mimetype = session.get("img_mimetype")
    img_size = session.get("img_size") 
    img_width = session.get("img_width")
    img_height = session.get("img_height")
    elapsed_ms = session.get("img_ms")


    if deepfake:
        verdict = "fake"
    else:
         verdict = "real"

    return render_template(
        'results.html', 
        filename = filename, 
        front_page_url = get_front_page_url(),  
        page_css = "css/results.css", 
        pico_css = "css/pico.slate.min.css",
        verdict = verdict,
        overall_prc=overall_prc,
        deepcheck=deepcheck,
        sightlook=sightlook,
        frameguard=frameguard,
        forgescan=forgescan,
        img_url=img_url,
        img_mimetype=img_mimetype,
        img_size=img_size,
        img_width=img_width,
        img_height=img_height,
        elapsed_ms=elapsed_ms
    )

if __name__ == "__main__":
    app.run(port=8000, debug=True)