from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from contents import cont
app = Flask(__name__)

app.config['SECRET_KEY'] = '497f5e863942d4fd0a245f1226934286'

posts = [
    {
        'user' : 'arliardiandy',
        'title' : 'Comment Title 1',
        'comment' : 'First Comment',
        'date' : 'May 2020'
    },
    {
        'user' : 'nurseramika',
        'title' : 'Comment Title 2',
        'comment' : 'Second Comment',
        'date' : 'May 2020'
    }
]

atama = cont()

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=atama)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/map')
def map():
    return render_template('map.html', title='Map', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created { form.username.data }!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
    app.run(debug=True)





