import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/data'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



## include db name in URI; _HOST entry overwrites all others
#app.config['MONGODB_HOST'] = 'mongodb://localhost:27017/sivji-sandbox'


# initalize app with database
#db.init_app(app)


@app.route("/")
def index():
    ## get the last date the webscraper was run
    

    return render_template(
        'hello.html'
        )

@app.route("/date")
def all_dates():
    ## get all the dates the scraper was run on
    dates = Post.objects().fields(date_str=1).distinct('date_str')

    return render_template(
        'all-dates.html',
        dates=reversed(list(dates)) # latest date on top
        )

@app.route("/date/<day_to_pull>")
def by_date(day_to_pull=None):
    return render_template(
        'index.html',
        Post=Post,
        day_to_pull=day_to_pull
        )

@app.route("/sub")
def all_subs():
    ## get all the dates the scraper was run on
    subs = Post.objects().fields(sub=1).distinct('sub')

    return render_template(
        'all-subreddits.html',
        subs=sorted(list(subs), key=str.lower) # sort list of subreddits
        )

@app.route("/sub/<sub_to_pull>")
def by_subreddit(sub_to_pull=None):
    return render_template(
        'by-subreddit.html',
        Post=Post,
        sub=sub_to_pull
        )

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


if __name__ == "__main__":
    app.run(debug=True)