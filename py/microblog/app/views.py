from app import app
import flask
from .forms import LoginForm

@app.route('/')
@app.route('/index')
def index ():
	user = {'nickname': 'Chrissy'}
	posts = [
		{'author': {'nickname': 'John'}, 'body': 'Beautiful Day in Portland!'},
		{'author': {'nickname': 'Susan'}, 'body': 'The Avengers movie was so cool!'},
		{'author': {'nickname': 'Chrissy'}, 'body': 'Nice video of Cheese!'},
		{'author': {'nickname': 'Eva'}, 'body': 'I picked Villanova!'},
		{'author': {'nickname': 'Jack'}, 'body': 'I am quite comfortable.'}
	]
	return flask.render_template('index.html', user=user, posts=posts)
	# return flask.render_template('index.html', title='Home', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login ():
	form = LoginForm()
	if form.validate_on_submit():
		flask.flash('Login requested for OpenID="{}", remember_me={}'.format(form.openid.data, str(form.remember_me.data)))
		return flask.redirect('/index')
	return flask.render_template('login.html', title='Sign In', form=form, providers=app.config['OPENID_PROVIDERS'])
