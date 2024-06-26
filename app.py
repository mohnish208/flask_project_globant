from flask import redirect, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from init import app,db
from models import User

class UpdateForm(FlaskForm):
    name = StringField("Name:")
    email = StringField("Email:")
    submit = SubmitField('Sumbit')

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    data = User.query.all()
    return render_template('index.html',data=data)

@app.route('/add', methods = ['POST'])
def add():
    name = request.form['name']
    email = request.form['email']
    newuser = User(name=name,email=email)
    db.session.add(newuser)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods = ['GET','POST'] )
def update(id):
    form = UpdateForm()
    data = User.query.get_or_404(id)
    if form.validate_on_submit():
        user = User.query.get(id)
        user.name = form.name.data
        user.email = form.email.data
        db.session.commit()
        return redirect(url_for('index'))
    form.name.data = data.name
    form.email.data = data.email
    return render_template('update.html', form=form)

@app.route('/delete/<int:id>', methods = ['POST'])
def delete(id):
    user = User.query.get(id)
    db.session.delete(user)   
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)