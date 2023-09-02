from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, URL, number_range
from html import escape
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafe-db.db"
db = SQLAlchemy()
db.init_app(app)


class CafeForm(FlaskForm):
    cafe_name1 = StringField('Cafe name', validators=[DataRequired()])
    location_url_2 = StringField("Location", validators=[DataRequired(), URL(message="You must enter a valid URL.")])
    open_3 = StringField("Open", validators=[DataRequired()])
    close_4 = StringField("close", validators=[DataRequired()])
    coffee_5 = SelectField("coffee", validators=[DataRequired()], choices=["☕️"*i if i > 0 else "✘" for i in range(0,6)])
    wifi_6 = SelectField("wifi", validators=[DataRequired()], choices=["💪"*i if i > 0 else "✘" for i in range(0,6)])
    power_7 = SelectField("power", validators=[DataRequired()], choices=["🔌"*i if i > 0 else "✘" for i in range(0,6)])
    submit = SubmitField('Submit')
class Cafes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cafe_name = db.Column(db.String())
    location_url = db.Column(db.String())
    open = db.Column(db.String())
    close = db.Column(db.String())
    coffee = db.Column(db.String())
    choices = db.Column(db.String())
    wifi = db.Column(db.String())
    power = db.Column(db.String())


def stringify_data(data: list[str]) -> str:
    stringified = ",".join(data)
    return stringified


def add_line_to_csv(path_to_csv: str, new_line: str) -> None:
    with open(path_to_csv, "a", encoding="utf-8") as file:
        file.write(f'"\n"{new_line}')




# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields

# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️️️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")



@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        added_cafe = [fr"{form.cafe_name1.data}",
                      fr"{form.location_url_2.data}",
                      fr"{form.open_3.data}",
                      fr"{form.close_4.data}",
                      fr"{form.coffee_5.data}",
                      fr"{form.wifi_6.data}",
                      fr"{form.power_7.data}"]
        [print(e) for e in added_cafe]
        new_line = stringify_data([escape(e) for e in added_cafe])
        print(new_line)
        add_line_to_csv("cafe-data.csv", new_line)
        return redirect(url_for('cafes'))
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    else:
        return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    print(DelForm.get_csv_length("cafe-data.csv"))
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = [row for row in csv_data]
    for row in list_of_rows:
        print(row, f"{len(row)=}")
    return render_template('cafes.html', cafes=list_of_rows)


@app.route("/del/", methods=["GET", "POST"])
def show_delete_form():
    delete_form = DelForm()
    print(delete_form.max)
    if delete_form.validate_on_submit():
        print(type(delete_form.row_to_delete.data))
        print(delete_form.row_to_delete.data)
        return redirect(url_for('delete_row', line_to_delete=delete_form.row_to_delete.data))
    return render_template("delete-row.html", form=delete_form)
@app.route("/del/<int:line_to_delete>", methods=["GET", "POST"])
def delete_row(line_to_delete: int) -> str:
    if line_to_delete < 1:
        return "You cannot delete the title row!"
    with open("cafe-data.csv", encoding="utf-8") as csv_file:
        lines = csv_file.readlines()
        new_data = "".join([line for i, line in enumerate(lines) if i != line_to_delete])
        print(f"{new_data=}")
    keep_going = input("Continue with delete operation?")
    if keep_going == "y":
        with open("cafe-data.csv", "w", encoding="utf-8") as csv_file:
            csv_file.write(new_data)
            return f"{line_to_delete} deleted."
    else:
        return "Turning back was a wise choice."


if __name__ == '__main__':
    app.run(debug=True)
