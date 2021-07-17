from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

# FLASK WTF FROM
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap

import os

app = Flask(__name__)

# ------------------- DATABASE ------------------- #
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///cafes.db")
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    seats = db.Column(db.String(250))
    coffee_price = db.Column(db.String(250))

# db.create_all()


# ------------------ FLASK FORM ------------------ #
app.secret_key = "cafetourmanagement"
bootstrap = Bootstrap(app)


class CafeForm(FlaskForm):
    name = StringField('Cafe Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    seats = StringField('Seats', validators=[DataRequired()])
    coffee_price = StringField('Coffee Price', validators=[DataRequired()])
    map_url = StringField('Map Url', validators=[DataRequired()])
    img_url = StringField('Image Url', validators=[DataRequired()])
    has_wifi = BooleanField('Wifi')
    can_take_calls = BooleanField('Phone Call')
    has_sockets = BooleanField('Socket')
    has_toilet = BooleanField('Toilet')
    submit = SubmitField(label='Add Cafe')
# ------------------------------------------------ #


@app.route('/')
def home():
    all_cafes = db.session.query(Cafe).all()
    return render_template("index.html", cafes=all_cafes)


@app.route('/cafe/<int:cafe_id>')
def cafe_detail(cafe_id):
    return render_template("cafe_detail.html", cafe=db.session.query(Cafe).get(cafe_id))


@app.route('/add_cafe', methods=('GET', 'POST'))
def add_cafe():
    add_cafe_form = CafeForm()
    if add_cafe_form.validate_on_submit():
        new_cafe = Cafe(
            name=add_cafe_form.name.data,
            map_url=add_cafe_form.map_url.data,
            img_url=add_cafe_form.img_url.data,
            location=add_cafe_form.location.data,
            has_sockets=add_cafe_form.has_sockets.data,
            has_toilet=add_cafe_form.has_toilet.data,
            has_wifi=add_cafe_form.has_wifi.data,
            can_take_calls=add_cafe_form.can_take_calls.data,
            seats=add_cafe_form.seats.data,
            coffee_price=add_cafe_form.coffee_price.data
        )
        db.session.add(new_cafe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("cafe_editor.html", form=add_cafe_form)


@app.route('/edit/<int:cafe_id>', methods=('GET', 'POST'))
def edit_cafe(cafe_id):
    cafe_to_update = Cafe.query.get(cafe_id)
    edit_form = CafeForm(obj=cafe_to_update)
    edit_form.submit.label.text = "Edit Cafe"
    if edit_form.validate_on_submit():
        cafe_to_update.name = edit_form.name.data
        cafe_to_update.map_url = edit_form.map_url.data
        cafe_to_update.img_url = edit_form.img_url.data
        cafe_to_update.location = edit_form.location.data
        cafe_to_update.has_sockets = edit_form.has_sockets.data
        cafe_to_update.has_toilet = edit_form.has_toilet.data
        cafe_to_update.has_wifi = edit_form.has_wifi.data
        cafe_to_update.can_take_calls = edit_form.can_take_calls.data
        cafe_to_update.seats = edit_form.seats.data
        cafe_to_update.coffee_price = edit_form.coffee_price.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("cafe_editor.html", form=edit_form)


@app.route("/delete")
def delete():
    cafe_id = request.args.get('id')
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)