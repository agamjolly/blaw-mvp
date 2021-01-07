from flask import *
from collections import defaultdict
import json
import os

app = Flask(__name__)

# fetching the db assuming we get a JSON in response from Devin's law school API 

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "static/data", "db.json")
db = json.load(open(json_url)) 


def is_teacher(entry):
    """Returns if the entry is a teacher."""
    if entry["role"] == "teacher":
        return True
    return False

def is_student(entry):
    """Returns if the entry is a student."""
    if entry["role"] == "student":
        return True
    return False

def is_admin(entry):
    """Returns if the entry is an admin."""
    if entry["role"] == "admin":
        return True
    return False

def generate_students():
    students = []
    for entry in db:
        if entry["role"] == "student":
            students.append(entry)
    return students

def generate_admins():
    admins = []
    for entry in db:
        if entry["role"] == "admin":
            admins.append(entry)
    return admins

def generate_instructors():
    instructors = []
    for entry in db:
        if is_teacher(entry):
            curr = defaultdict() # making an empty dict
            curr["name"] = entry["name"]
            curr["role"] = entry["role"]
            curr["classes"] = defaultdict()
            # for every class the prof teaches
            for i in entry["classes"]:
                curr["classes"][i] = []
                for student in students:
                    # if a student takes that particular class
                    if i in student["classes"]:
                        curr["classes"][i].append({ 
                            "name": student["name"],
                            "username": student["username"],
                            "role": student["role"] # will always be `student` tho
                        })
                # curr["classes"][i].append(temp)

            instructors.append(dict(curr))
    return instructors

students = generate_students()
admins = generate_admins()
instructors = generate_instructors()


accepted_keys = set(["PRIVATE_KEYS_GO_HERE"])

# better auth needed
def auth(user_key): 
    if user_key == "users":
        return jsonify(db)
    elif user_key == "admins":
        return jsonify(admins)
    elif user_key == "students":
        return jsonify(students)
    elif user_key == "instructors":
        return jsonify(instructors)
    elif user_key in accepted_keys:
        return jsonify(db)
    else:
        return jsonify(error="Invalid key"), 406

@app.route('/api/v1/', methods=["POST", "GET"])
def api():
    if request.method == "POST":
        try:
            user_key = request.json["key"]
            if user_key == "users":
                return jsonify(db)
            elif user_key == "admins":
                return jsonify(admins)
            elif user_key == "students":
                return jsonify(students)
            elif user_key == "instructors":
                return jsonify(instructors)
            elif user_key in accepted_keys:
                return
        except:
            return jsonify(error="Invalid key"), 406

    else: 
        return jsonify(db)

"""Home route."""
@app.route("/")
def index():
    info = { 
        "title": "Welcome"
    }
    return render_template("index.html", title = info.get("title"))

username, password = None, None # initialized to `None`.
logged = False # changes to `True` when the user is logged in.

"""Just a temporary route."""
@app.route("/temp")
def temp():
    return render_template("temp.html", username = username, password = password)

def validate(username, password):
    """Validates username and password from the database. Returns a boolean and the entry if found."""
    for entry in db:
        if entry["username"] == username and entry["password"] == password:
            return True, entry
    return False, None

@app.route("/logout", methods = ['GET', 'POST'])
def logout():
    return redirect(url_for("signin"), code = 302)

@app.route("/signin", methods = ['GET', 'POST'])
def signin():
    info = { 
        "title": "Sign In"
    }

    if request.method == "POST":
        credentials = request.form
        username = credentials["username"]
        password = credentials["password"]
        
        # better authentication needed - this one might be too slow
        logged, data = validate(username, password)
        if logged:
            if data["role"] == "student":
                return render_template("student.html", data = data)
            elif data["role"] == "admin":
                return render_template("admin.html", data = data, db = db)
            else:
                return render_template("teacher.html", data = data)
        else:
            return render_template("signin.html", title = info.get("title"), invalid = True)      
    
    
    return render_template("signin.html", title = info.get("title"), invalid = False)

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 80, debug = True)