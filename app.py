from flask import Flask , render_template , request , redirect , url_for , jsonify
from flask_cors import CORS
import os
from utils.recommend import recommend_products

app = Flask(__name__, static_folder="static")
@app.route("/" , methods=['GET'])
def home():
    return render_template("fron.html")
@app.route('/login' , methods=["GET"])
def login():
    return render_template('login.html')
@app.route('/signup' , methods=['GET'])
def signup():
    return render_template('signup.html')
@app.route('/seller' , methods=['get'])
def seller():
    return render_template('seller_dashboard.html')
@app.route('/user' , methods=['get'])
def user():
    return render_template('user_dashboard.html')

CORS(app)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

products = []
cart = []
orders = []


# ---------------- ADD PRODUCT ---------------- #

@app.route("/add-product", methods=["POST"])
def add_product():
    try:
        name = request.form["name"]
        price = int(request.form["price"])
        image = request.files["image"]

        # Save image
        path = os.path.join("static/uploads", image.filename)
        image.save(path)

        # Fix path
        path = path.replace("\\", "/")

        print("Saved image:", path)

        # Run AI safely
        ai = predict_trust(path)

        print("AI output:", ai)

        # FORCE SAFE TYPES
        trust = float(ai.get("confidence", 0))
        label = str(ai.get("label", "Unknown"))

        product = {
            "id": int(len(products)),
            "name": str(name),
            "price": int(price),
            "image": str(path),
            "trust_score": trust,
            "ai_label": label
        }

        products.append(product)

        print("Product added:", product)

        return jsonify(product)

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


# ---------------- GET PRODUCTS ---------------- #

@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)


# ---------------- RECOMMEND ---------------- #

@app.route("/recommend", methods=["POST"])
def recommend():

    user_history = request.json.get("history", [])

    recs = recommend_products(products, user_history)

    return jsonify(recs)


# ---------------- CART ---------------- #

@app.route("/add-cart", methods=["POST"])
def add_cart():
    item = request.json
    cart.append(item)
    return jsonify({"msg": "Added to cart"})


@app.route("/cart", methods=["GET"])
def get_cart():
    return jsonify(cart)


# ---------------- ORDERS ---------------- #

@app.route("/place-order", methods=["POST"])
def place_order():
    global cart
    orders.extend(cart)
    cart = []
    return jsonify({"msg": "Order placed"})


@app.route("/orders", methods=["GET"])
def get_orders():
    return jsonify(orders)

@app.route("/analyze-product", methods=["POST"])
def analyze_product():

    data = request.json
    image_path = data.get("image")
    price = data.get("price", 0)

    # Fix path (important for Mac/Windows)
    image_path = image_path.replace("/", os.sep)

    print("Analyzing:", image_path)

    ai = predict_trust(image_path)

    # Recommendations (simple logic)
    recs = []
    for p in products:
        if abs(p["price"] - price) < 5000:
            recs.append(p)

    return jsonify({
        "trust": ai["confidence"],
        "label": ai["label"],
        "recommendations": recs[:4]
    })

def predict_trust(image_path):
    try:
        # your model code...

        return {
            "confidence": float(confidence),  # MUST
            "label": str(label)               # MUST
        }

    except Exception as e:
        print("AI ERROR:", e)
        return {
            "confidence": 50.0,
            "label": "Unknown"
        }



if __name__ == "__main__":
    app.run(debug=True)
    
