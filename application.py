from flask import Flask, render_template, request, flash, url_for
from werkzeug.utils import redirect

app = Flask(__name__)
app.config.from_mapping(SECRET_KEY='dev')

items = [
    {"name": "item1", "price": 100, "quantity":2000},
    {"name": "item2", "price": 200, "quantity":2010}
        ]


@app.route("/")
def hello_world():
    return "hello world"


@app.route("/items", methods=["GET"])
def get_items():
    return render_template("items.html", items=items)


@app.route("/items", methods=["POST"])
def create_item():
    new_item = {"name": request.form['name'],
                "price": request.form['price'],
                "quantity": request.form['quantity']}
    items.append(new_item)
    return redirect(url_for('get_items'))


@app.route("/items/<name>/update", methods=["GET"])
def update_item_form(name):
    return render_template('update.html', item=next(filter(lambda item: item["name"] == name, items)))


@app.route("/items/<name>/update", methods=["POST"])
def update_item(name):
    item_found = False
    for item in items:
        if item['name'] == name:
            item_found = True
            item["name"]= request.form['name']
            item["price"]= request.form['price']
            item["quantity"]= request.form['quantity']
    if not item_found:
        flash("Item not found")
    return redirect(url_for('get_items'))


@app.route("/items/<name>/delete", methods=["POST"])
def delete_item(name):
    item_found = False
    for item in items:
        if item['name'] == name:
            item_found = True
            items.remove(item)
    if not item_found:
        flash("Item not found")
    return redirect(url_for('get_items'))


app.run(port=5000)
