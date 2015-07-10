from flasked import app
from flask import render_template, request, flash,session,redirect,url_for
from flask.ext.mail import Message,Mail
from flasked.forms import ContactForm,SignupForm,SigninForm,ChangePasswordForm,DoneForm,UndoDoneForm
from flasked.models import db,User,Article,Finished
from werkzeug import generate_password_hash
mail=Mail()
 
@app.route('/')
def home():
  return render_template('home.html')
    
@app.route('/about')
def about():
  return render_template('about.html')  
  
@app.route('/contact', methods=['GET', 'POST'])
def contact():
  fields=['name','email','subject','message']
  form=ContactForm() 
  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form,fields=fields)
    else:
      msg = Message(form.subject.data, sender='contact@example.com', recipients=['utsavdey@outlook.com'])
      msg.body = """
      From: %s <%s>
      %s
      """ % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)
 
      return render_template('contact.html', success='true',fields=fields)
 
  elif request.method == 'GET':
    return render_template('contact.html', form=form,fields=fields)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()
		   
	if request.method == 'POST':
		if form.validate() == False:
			return render_template('signup.html', form=form)
		else:
			newuser=User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
			db.session.add(newuser)
			db.session.commit()
			session['email'] = newuser.email
			return redirect(url_for('profile'))
		   
	elif request.method == 'GET':
		return render_template('signup.html', form=form)

@app.route('/profile')
def profile():
 
  if 'email' not in session:
    return redirect(url_for('signin'))
 
  user = User.query.filter_by(email = session['email']).first()
  if user is None:
    return redirect(url_for('signin'))
  else:
    article_finished=Finished.query.filter_by(uid = user.uid,state=1)
    article_links=[]
    for cur_article in article_finished:
      article_links=article_links+[Article.query.filter_by(id = cur_article.aid).first().title]
    if article_finished is None:
      return render_template('profile.html',user=user)
    else :
      article_titles={}
      for s in article_links:
          i=0
          sn=s+" "
          ns=""
          while sn[i]!=" ":
                  if sn[i]=="_":
                          ns=ns+" "
                  else:
                          ns=ns+sn[i]
                  i=i+1
          article_titles[s]=ns
          
      return render_template('profile.html',user=user,article_links=article_links,article_titles=article_titles)
	
@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()
  if 'email' in session:
    return redirect(url_for('profile'))
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signin.html', form=form)
    else:
      session['email'] = form.email.data
      return redirect(url_for('profile'))
                 
  elif request.method == 'GET':
    return render_template('signin.html', form=form)

@app.route('/signout')
def signout():
 
  if 'email' not in session:
    return redirect(url_for('signin'))
     
  session.pop('email', None)
  return redirect(url_for('home'))

@app.route('/changepassword', methods=['GET', 'POST'])
def changepassword():
  form = ChangePasswordForm()
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('changepassword.html', form=form)
    else:
      session['email'] = form.email.data
      user = User.query.filter_by(email = session['email'] .lower()).first()
      user.pwdhash=generate_password_hash(form.newpassword.data)
      db.session.merge(user)
      db.session.commit()
      return redirect(url_for('profile'))
                 
  elif request.method == 'GET':
    return render_template('changepassword.html', form=form)

@app.route('/lorem', methods=['GET', 'POST'])
def lorem():
  return render_progress_tracking('lorem')

@app.route('/bengal', methods=['GET', 'POST'])
def bengal():
  return render_progress_tracking('bengal') 

def render_progress_tracking(page):
  if 'email' in session:
      state=0
      form = DoneForm()
      unform=UndoDoneForm()
      user = User.query.filter_by(email = session['email'] .lower()).first()
      article = Article.query.filter_by(title = page).first()
      a=user.uid
      b=article.id
      FinishState=Finished.query.filter_by(uid =a,aid=b).first()
      if FinishState is not None:
        state=FinishState.state
      if request.method=='GET':
        if state==0:
          return render_template(page+'.html', form=form,state=state)                    
        else:
          return render_template(page+'.html', form=unform,state=state)
      elif request.method=='POST':
        if state==0:
          state=1
          if FinishState is None:
            newstate=Finished(1,user.uid,article.id)
            db.session.add(newstate)
            db.session.commit()
          else:
            FinishState.state=1
            db.session.merge(FinishState)
            db.session.commit()
          return render_template(page+'.html', form=unform,state=state)
        else:
          state=0
          FinishState.state=0
          db.session.merge(FinishState)
          db.session.commit()
          return render_template(page+'.html', form=form,state=state)  
  return render_template(page+'.html')
  
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.errorhandler(405)
def method_not_found(e):
    return "405 encountered"  
