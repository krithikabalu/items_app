from http import HTTPStatus

from flask import Flask, render_template, request, url_for, render_template_string, jsonify
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

app = Flask(__name__)

items = [
    {"name": "item1", "price": 100, "quantity": 2000},
    {"name": "item2", "price": 200, "quantity": 2010}
]


@app.route("/")
def hello_world():
    return "hello world"


@app.route("/store_info")
def get_store_info():
    return """
    <html> 
    <h1> ABC Stores </h1>
    <p> <i> since 2000 </i></p>
    </html>
    """


@app.route("/item-list-static")
def get_item_list_static():
    return """
        <html> 
        <h1> ABC Stores </h1>
        <p> <i> since 2000 </i></p>
        <ul>
            <li>item 1</li>
            <li>item 2</li>
            <li>item 3</li>
            <li>item 4</li>
            <li>item 5</li>
            <li>item 6</li>
        </ul>
        </html>
        """


@app.route("/item-list-dynamic")
def get_item_list_dynamic():
    item_list = ['item1', 'item2', 'item3', 'item4', 'item5', 'item6', 'item7', 'item8', 'item9']
    items_html = "<ul>"
    items_html += "\n".join(["<li>{item}</li>".format(item=item) for item in item_list])
    items_html += "</ul>"
    html = """
        <html> 
        <h1> ABC Stores </h1>
        <p> <i> since 2000 </i></p>
        <ul>
            {items_html}
        </ul>
        </html>
        """
    return html.format(items_html=items_html)


@app.route("/item-list-jinja")
def get_item_list_jinja():
    item_list = ['item1', 'item2', 'item3', 'item4', 'item5', 'item6', 'item7', 'item8', 'item9', 'item10']
    html = """
        <html> 
        <h1> ABC Stores </h1>
        <p> <i> since 2000 </i></p>
        <ul>
            {% for item in item_list %}
                <li>{{item}}</li>
            {% endfor %}
        </ul>
        </html>
        """
    return render_template_string(html, item_list=item_list)


@app.route("/item/<string:item_name>")
def get_item_details(item_name):
    for item in items:
        if item['name'] == item_name:
            return jsonify({"item": item})
        else:
            abort(HTTPStatus.NOT_FOUND)


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
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_for('get_items'))


@app.route("/items/<name>/delete", methods=["POST"])
def delete_item(name):
    item_found = False
    for item in items:
        if item['name'] == name:
            item_found = True
            items.remove(item)
    if not item_found:
        abort(HTTPStatus.NOT_FOUND)
    return redirect(url_for('get_items'))


@app.errorhandler(HTTPStatus.NOT_FOUND)
def not_found(error):
    return "<html><p><i>Sorry, The product you are looking for does not exist</i></p></html>"


app.run(port=5000)
