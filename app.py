from flask import Flask, flash, request, redirect, url_for, render_template, make_response
import urllib.request
import os
from werkzeug.utils import secure_filename
import cohere
co = cohere.Client('dG9FO5NCPecnNjWtiSGAlXmQf3qbkVkBGX2krkBg')

fixed_str = ""

app = Flask(__name__)
 
UPLOAD_FOLDER = 'static/uploads/'
 
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    return render_template('index.html')
 
@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        resp = make_response(render_template('index.html', filename=filename))
        resp.set_cookie('photoname', filename)
        return resp
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
 
@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


def detect_document(path):
    words = []
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient.from_service_account_json("HackTheNorth-4bd17a719544.json")

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    words.append(word_text)
    return(" ".join(map(str, words)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

def fix_text(test_str):
    training_data = "This is a spell check generator that fixes samples of text.\n\nSample: a new type OF aurora , FounD on saturn resolves a planetary mystery.\nFixed: A new type of aurora, found on saturn resolves a planetary mystery.\n--\nSample: online Shopping , internet , and phones are ReSHaping Real-world Cities\nFixed: Online shopping, internet, and phones are reshaping real-world cities\n--\nSample: When you close 100 TAbs AFter Finding THE SoluTion To A BuG , you feel Relaxed .\nFixed: When you close 100 tabs after finding the solution to a bug, you feel relaxed.\n--\nSample: masteing DYNAmIC ProGrammING\nFixed: Mastering dynamic programming\n--\nSample: While THis wasnt something completely unheard of , it als wasn\'t normal .\nFixed: While this wasn\'t something completely unheard of, it also wasn\'t normal.\n--\nSample: after hunting for . several hours , we  finally saw a large seal sunning itself on a flat rock .\nFixed: After hunting for several hours, we finally saw a large seal sunning itself on a flat rock.\n--\nSample: "+test_str+"\nFixed:"
    response1 = co.generate(
    model='large',
    prompt=training_data,
    max_tokens=400,
    temperature=0.3,
    k=0,
    p=0.75,
    frequency_penalty=0,
    presence_penalty=0,
    stop_sequences=["--"],
    return_likelihoods='NONE')

    fixed_str = response1.generations[0].text
    return fixed_str
    #print('Fixed Text:', fixed_str)
def summarize(fixed_str):
    summary_training_data = "Passage: Is Wordle getting tougher to solve? Players seem to be convinced that the game has gotten harder in recent weeks ever since The New York Times bought it from developer Josh Wardle in late January. The Times has come forward and shared that this likely isn’t the case. That said, the NYT did mess with the back end code a bit, removing some offensive and sexual language, as well as some obscure words There is a viral thread claiming that a confirmation bias was at play. One Twitter user went so far as to claim the game has gone to “the dusty section of the dictionary” to find its latest words.\n\nTLDR: Wordle has not gotten more difficult to solve.\n--\nPassage: ArtificialIvan, a seven-year-old, London-based payment and expense management software company, has raised $190 million in Series C funding led by ARG Global, with participation from D9 Capital Group and Boulder Capital. Earlier backers also joined the round, including Hilton Group, Roxanne Capital, Paved Roads Ventures, Brook Partners, and Plato Capital.\n\nTLDR: ArtificialIvan has raised $190 million in Series C funding.\n--\nPassage: After hunting for several hours, we finally saw a large seal sunning itself on a flat rock. I took one of the wooden clubs while Larry took the longer one. We slowly snuck up behind the seal until we were close enough to club it over its head. The seal slumped over and died. This seal would help us survive. We could eat the meat and fat. The fat could be burned in a shell for light and the fur could be used to make a blanket. We declared our first day of hunting a great success.\n\nTLDR: We successfully hunted a seal, which gave us meat and fat\n--\nPassage: He watched as the young man tried to impress everyone in the room with his intelligence. There was no doubt that he was smart. The fact that he was more intelligent than anyone else in the room could have been easily deduced, but nobody was really paying any attention due to the fact that it was also obvious that the young man only cared about his intelligence.\n\nTLDR: The young man was smart, but only cared about his intelligence.\n--\nPassage: " + fixed_str +  "\n\nTLDR:"
    response2 = co.generate( 
    model='large', 
    prompt=summary_training_data, 
    max_tokens=75, 
    temperature=0.3, 
    k=0, 
    p=0.3, 
    frequency_penalty=0, 
    presence_penalty=0, 
    stop_sequences=["--"], 
    return_likelihoods='NONE') 
    return((response2.generations[0].text))

@app.route("/Process/", methods=['POST'])
def process():
    photoname =  request.cookies.get('photoname')
    test_str = detect_document("static/uploads/"+photoname)
    global fixed_str 
    fixed_str = fix_text(test_str)
    summary = summarize(fixed_str)
    return render_template('index.html', processed_text = fixed_str, summary_text = summary);

@app.route("/RegenSummary/", methods=['POST'])
def regenSummary():
    summary = summarize(fixed_str)
    return render_template('index.html', processed_text = fixed_str, summary_text = summary);

if __name__ == "__app__":
    app.run()