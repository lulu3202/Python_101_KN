from flask import Flask, jsonify, request

app = Flask(__name__)

## Initial Data in my to-do list
items = [
    {"id": 1, "name": "Item 1", "description": "This is item 1"},
    {"id": 2, "name": "Item 2", "description": "This is item 2"}
]

# @app.route('/') is a Flask route decorator that maps the root URL ('/') to the home() function
@app.route('/')
def home():
    return "Welcome To The Sample To-Do List App"

# @app.route('/items', methods=['GET']) maps the '/items' URL to the get_items() function
# This allows retrieving all items when a GET request is made
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

# @app.route('/items/<int:item_id>', methods=['GET']) maps a dynamic URL with an integer parameter (item_id)
# This retrieves a specific item by ID when a GET request is made
@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if item is None:
        return jsonify({"error": "Item not found"})
    return jsonify(item)

# @app.route('/items', methods=['POST']) maps the '/items' URL to create_item() function
# This allows creating a new item when a POST request is made
@app.route('/items', methods=['POST'])
def create_item():
    if not request.json or 'name' not in request.json:
        return jsonify({"error": "Invalid request"})
    new_item = {
        "id": items[-1]["id"] + 1 if items else 1,
        "name": request.json['name'],
        "description": request.json.get("description", "")
    }
    items.append(new_item)
    return jsonify(new_item)

# @app.route('/items/<int:item_id>', methods=['PUT']) maps a URL with an integer ID
# This updates an existing item when a PUT request is made
@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if item is None:
        return jsonify({"error": "Item not found"})
    item['name'] = request.json.get('name', item['name'])
    item['description'] = request.json.get('description', item['description'])
    return jsonify(item)

# @app.route('/items/<int:item_id>', methods=['DELETE']) maps a URL with an integer ID
# This deletes an item when a DELETE request is made
@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global items
    items = [item for item in items if item["id"] != item_id]
    return jsonify({"result": "Item deleted"})

# Ensures the app runs only if executed directly
if __name__ == '__main__':
    app.run(debug=True)
