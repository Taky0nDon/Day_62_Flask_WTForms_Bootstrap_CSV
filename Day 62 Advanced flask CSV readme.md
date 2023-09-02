#flask

for details on how to use flask-sqlalchemy see: [[day63readme]]

## Coffee & Wifi

### The `<select>` element

* You don't need to add form tags if you use the render_form() method from bootstrap-flask
* instead of returning my cafe() function, which doesn't actually change the URL, i could have used the redirect() function
from Flask: `return redirect(url_for('cafes'))`

now this should appear in obsidian