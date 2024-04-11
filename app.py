import os
import shutil

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for, send_file
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from filters import enhance_filter, color_filter, contrast_filter, brightness_filter, blur_filter, details_filter, sharpen_filter, smooth_filter

from helpers import login_required, apology

# Configure where the uploaded photos will be stored
UPLOAD_FOLDER = os.getcwd() + '/static/uploads'

# Configurate allowed file types
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
FILENAME = ""

# Configure application
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "docs"))
app = Flask(__name__, template_folder=template_dir)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///project.db")

# Check the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.after_request
def after_request(response):
    # Make sure responses aren't cached
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    # Check user's token balance
    userdata = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    usertokens = int(userdata[0]["tokens"])

    # Show the homepage with the token balance
    return render_template("index.html", usertokens=usertokens)

@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():

    global FILENAME

    # Get the upload directory for the user based on the user id
    userdir = os.path.join(app.config['UPLOAD_FOLDER'], str(session["user_id"]))

    # Wipe the user's upload directory if it existst each time the user clicks on upload
    if os.path.exists(userdir):
        shutil.rmtree(userdir)

    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect("/upload")

        # Assign the file to a variable
        file = request.files['file']

        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect("/upload")

        # Check if the file is allowed based on the allowed extensions
        if not allowed_file(file.filename):
            flash('Please select a .png, .jpg, or .jpeg, file')
            return redirect("/upload")

        # If the file exists and file extension is supported
        if file and allowed_file(file.filename):

            # Get the user's current token balance
            userdata = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
            usertokens = int(userdata[0]["tokens"])

            # Update the user balance for each successful upload
            balance = usertokens - 1
            db.execute("UPDATE users SET tokens = ? WHERE id = ?", balance, session["user_id"])

            if balance < 1:
                return apology("Not enough credits")

            else:
                # Store the file with a secure filename
                FILENAME = secure_filename(file.filename)

                # Get the upload directory for the user based on the user id
                userdir = os.path.join(app.config['UPLOAD_FOLDER'], str(session["user_id"]))

                # Check if the directory exists save the file
                if os.path.exists(userdir):
                    file.save(os.path.join(userdir, FILENAME))
                    return redirect("/edit")
                # If the user's directory does not exist - create then save
                else:
                    os.mkdir(userdir)
                    file.save(os.path.join(userdir, FILENAME))
                    return redirect("/edit")
        else:
            return apology("Unsupported file")

    else:
        return render_template("upload.html")

@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():

    # Variable to save the path to the uploaded image
    imgpath = ""

    # If the path does not exist, show an alert
    if not os.path.join('uploads' + '/' + str(session["user_id"]) + '/' + FILENAME):
        flash("No image loaded")

    # If the path exists set it to the exmpty variable
    else:
        imgpath = os.path.join('uploads' + '/' + str(session["user_id"]) + '/' + FILENAME)

    # When the user clicks on one of the options
    if request.method == 'POST':
        if FILENAME:
            # Save the full path to the file in a variable
            fullpath = os.path.join(app.config['UPLOAD_FOLDER'] + '/' + str(session["user_id"]) + '/' + FILENAME)

            # Make a copy of the uploaded file to work with and have the original intact
            shutil.copyfile(fullpath, os.path.join(app.config['UPLOAD_FOLDER'] + '/' + str(session["user_id"]) + '/' + 'copy-' + FILENAME))

            # Save the full path to the copied file in a variable
            copypath = os.path.join(app.config['UPLOAD_FOLDER'] + '/' + str(session["user_id"]) + '/' + 'copy-' + FILENAME)
            editedpath = os.path.join('uploads' + '/' + str(session["user_id"]) + '/' + 'copy-' + FILENAME)

            # If the user clicks on original show the initial unedited image
            if request.form.get("original"):
                flash("Original")
                return render_template("edit.html", imgpath=imgpath)

            # If the user clicks on enhance call the enhance function from filters.py
            elif request.form.get("enhance"):
                enhance_filter(copypath)
                flash("Enhanced")

            # If the user clicks on color call the color function from filters.py
            elif request.form.get("color"):
                color_filter(copypath)
                flash("Colored")

            # If the user clicks on contrast call the contrast function from filters.py
            elif request.form.get("contrast"):
                contrast_filter(copypath)
                flash("Contrasted")

            # If the user clicks on brightness call the brightness function from filters.py
            elif request.form.get("brightness"):
                brightness_filter(copypath)
                flash("Brightened")

            # If the user clicks on blur call the blur function from filters.py
            elif request.form.get("blur"):
                blur_filter(copypath)
                flash("Blurred")

            # If the user clicks on details call the details function from filters.py
            elif request.form.get("details"):
                details_filter(copypath)
                flash("Detailed")

            # If the user clicks on sharpen call the sharpen function from filters.py
            elif request.form.get("sharpen"):
                sharpen_filter(copypath)
                flash("Sharpened")

            # If the user clicks on smooth call the smooth function from filters.py
            elif request.form.get("smooth"):
                smooth_filter(copypath)
                flash("Smoothened")

            # If the user clicks on download, download the edited image
            elif request.form.get("download"):
                return send_file(copypath, as_attachment=True)

            return render_template("edit.html", imgpath=editedpath)

    # If the user didn't click on anything or just opened the page for the first time, show original image
    else:
        return render_template("edit.html", imgpath=imgpath)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Get the user's upload directory based on user id
    userdir = os.path.join(app.config['UPLOAD_FOLDER'], str(session["user_id"]))

    # If the upload directory exists, wipe it when the user logs out
    if os.path.exists(userdir):
        shutil.rmtree(userdir)

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Ensure password confirmation was submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 400)

        # Check if username already exists
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username does not already exist
        if len(rows) != 0:
            return apology("user already exists", 400)

        # Ensure password matches confirmation
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords don't match", 400)

        # Add user's data to our db
        id = db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get(
            "username"), generate_password_hash(request.form.get("password")))

        # Remember which user has logged in
        session["user_id"] = id

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")

@app.route("/refill", methods=["GET", "POST"])
@login_required
def refill():

    # Get the user's current token balance
    userdata = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
    usertokens = int(userdata[0]["tokens"])

    # If the user clicked on submit
    if request.method == "POST":
        # Get on which token amount option the user clicked
        tokens = int(request.form.get("option"))

        # Get user's card information just for emulating
        cardnumber = request.form.get("inputcard")
        cardname = request.form.get("inputname")
        cardexp = str(request.form.get("expmonth")) + '/' + str(request.form.get("expyear"))
        cardcvv = request.form.get("inputcvv")

        # Calculate the user current token balance plus the selected tokens amount
        balance = usertokens + tokens

        # If the user provided information for all the required fields, update user's token balance
        if cardnumber and cardname and cardexp and cardcvv:
            db.execute("UPDATE users SET tokens = ? WHERE id = ?", balance, session["user_id"])

        # If card number is not provided show an apology
        elif not cardnumber:
            return apology("need a card number", 400)

        # If card name is not provided show an apology
        elif not cardname:
            return apology("need a name on card", 400)

        # If card expiration date is not provided show an apology
        elif not cardexp:
            return apology("need an expiration date", 400)

        # If card cvv is not provided show an apology
        elif not cardcvv:
            return apology("need a cvv", 400)

        return redirect("/")


    else:
        return render_template("refill.html", usertokens=usertokens)