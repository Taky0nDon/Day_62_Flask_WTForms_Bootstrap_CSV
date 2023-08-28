from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

'''
Red underline? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt
On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)


def add_line_to_csv(path_to_csv: str, new_line: list[str]) -> None:
    with open(path_to_csv, "a", encoding="utf-8") as file:
        new_line_stringified = ",".join(new_line)
        file.write("\n" + new_line_stringified)


class CafeForm(FlaskForm):
    cafe_name1 = StringField('Cafe name', validators=[DataRequired()])
    location_url_2 = StringField("Location", validators=[DataRequired(), URL(message="You must enter a valid URL.")])
    open_3 = StringField("Open", validators=[DataRequired()])
    close_4 = StringField("close", validators=[DataRequired()])
    coffee_5 = SelectField("coffee", validators=[DataRequired()], choices=["☕️"*i if i > 0 else "✘" for i in range(0,6)])
    wifi_6 = SelectField("wifi", validators=[DataRequired()], choices=["💪"*i if i > 0 else "✘" for i in range(0,6)])
 

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
      power_7 = SelectField("power", validators=[DataRequired()], choices=["🔌"*i if i > 0 else "✘" for i in range(0,6)])
    submit = SubmitField('Submit')
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️️️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below

def home):
    return render_template("index.html")



@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit(): added_cafe = [form.cafe_name1.data,
                      form.location_url_2.data,
                      form.open_3.data,
                      form.close_4.data,
                      form.coffee_5.data,
                      form.wifi_6.data,
                      form.power_7.data]
        add_line_to_csv("cafe-data.csv", added_cafe)
        return redirect(url_for('cafes'))
    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    else:
        return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = [row for row in csv_data]
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
