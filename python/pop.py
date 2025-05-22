from flask import Flask,render_template

app = Flask(__name__)

JOBS=[
{
    'id': 1,
    'title': 'Software Developer',
    'description': 'Software Developer at Google',
    'location': 'Mountain View, CA',
},
{
    'id': 2,
    'title':'data scientist',
    'description':'data scientist at facebook',
    'location':'menlo park, CA',
},
{
    'id':3,
    'title':'data analyst',
    'description':'data analyst at apple',
    'location':'cupertino, CA',
},
{
    'id':4,
    'title':'data engineer',
    'description':'data engineer at amazon',
    'location':'bengaluru, india',
}    
]

@app.route("/")
def hello():
    return render_template('home.html',
                        jobs=JOBS)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)