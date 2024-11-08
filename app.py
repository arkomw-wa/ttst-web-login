from flask import Flask, render_template, redirect, url_for, session, flash
from forms import RegisterForm, Login
from models import db, User
from flask_bcrypt import Bcrypt

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ARK16112540'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost:5432/ttst-ldz-lab'

    bcrypt = Bcrypt()

    db.init_app(app)
    bcrypt.init_app(app)
    with app.app_context():
        
        db.create_all() 

    @app.route('/',methods=['GET','POST'])
    def login():
        form = Login()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password,form.password.data):
                session['usr_id'] = user.id
                session['username'] = user.username
                return redirect(url_for('dashboard'))
            else: flash("Login failed. Please check your email and password.", "danger")
        return render_template("login.html", form =form)
    
    @app.route('/register', methods = ['GET','POST'])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            hased_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=hased_password,
            )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))

        return render_template("register.html", form =form)
    
    @app.route('/dashboard')
    def dashboard():
        return render_template("dashboard.html")

    @app.route('/logout')
    def logout():
        session.pop('usr_id')
        session.pop('username')
        flash('You have been logged out')
        return redirect(url_for('login'))

    return app


if __name__ =='__main__':
    app = create_app()
    app.run(debug=True)