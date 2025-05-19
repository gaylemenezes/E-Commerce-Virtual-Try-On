from flask import Flask, render_template,jsonify, request, session,redirect
from models.database import get_db_connection  
import bcrypt


app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "your_super_secret_key"

@app.route("/")
def home():
    return render_template("home page.html")

@app.route("/women")
def women():
    return render_template("Nextpage.html")

@app.route("/tops")
def tops():
    return render_template("Tops&Sweatshirts.html")

@app.route("/skirts")
def skirts():
    return render_template("Skirts.html")
@app.route("/trousers")
def trousers():
    return render_template("Women-Trousers.html")
@app.route("/dresses")
def dresses():
    return render_template("Dresses.html")

@app.route("/men")
def men():
    return render_template("men.html")

@app.route("/sweatshirts")
def sweatshirts():
    return render_template("Tshirts&Sweatshirts.html")

@app.route("/jackets")
def jackets():
    return render_template("Jackets.html")

@app.route("/pants")
def pants():
    return render_template("Trousers.html")
@app.route("/hoodies")
def hoodies():
    return render_template("Hoodies.html")

@app.route("/product")
def product():
    return render_template("product1.html")

@app.route("/virtualtryon")
def virtualtryon():
    return render_template("virtualtryon.html")

@app.route("/cart")
def cart():
    return render_template("cart.html")


@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    data = request.json
    print(" Received JSON Data:", data)

    sku = data.get("sku").strip()  
    product_name = data.get("product_name")
    price = data.get("price")
    image_url = data.get("image_url")

    if not all([sku, product_name, price, image_url]):
        print(" Missing product details")
        return jsonify({"error": "Missing product details"}), 400

    user_session = session.get("user_id", request.remote_addr)
    print(" User Session:", user_session)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM products WHERE sku = %s", (sku,))
    product_exists = cursor.fetchone()
    print(" SKU Check Result:", product_exists)

    if not product_exists:
        print(f" SKU '{sku}' not found in products table")
        return jsonify({"error": "Invalid product SKU"}), 400


    cursor.execute("SELECT quantity FROM cart WHERE sku = %s AND user_session = %s", (sku, user_session))
    existing_item = cursor.fetchone()

    if existing_item:
        cursor.execute("UPDATE cart SET quantity = quantity + 1 WHERE sku = %s AND user_session = %s", (sku, user_session))
        print(" Updated quantity in cart")
    else:
        cursor.execute("INSERT INTO cart (sku, product_name, price, image_url, quantity, user_session) VALUES (%s, %s, %s, %s, %s, %s)",
                       (sku, product_name, price, image_url, 1, user_session))
        print(" Inserted new item in cart")

    conn.commit()
    conn.close()
    print("Product added successfully")

    return jsonify({"message": "Product added to cart successfully"})

@app.route("/cart_count")
def cart_count():
    user_session = session.get("user_id", request.remote_addr)  

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT SUM(quantity) FROM cart WHERE user_session = %s", (user_session,))
    count = cursor.fetchone()[0] or 0  

    conn.close()

    return jsonify({"count": count})

@app.route("/get_cart")
def get_cart():
    user_session = session.get("user_id", request.remote_addr)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT sku, product_name, price, image_url, quantity FROM cart WHERE user_session = %s", (user_session,))
    cart_items = cursor.fetchall()
    conn.close()

    return jsonify({"cart": cart_items})

@app.route("/update_cart", methods=["POST"])
def update_cart():
    data = request.json
    sku = data.get("sku")
    change = int(data.get("change"))
    user_session = session.get("user_id", request.remote_addr)

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE cart SET quantity = GREATEST(quantity + %s, 1) WHERE sku = %s AND user_session = %s",
                   (change, sku, user_session))
    
    conn.commit()
    conn.close()

    return jsonify({"message": "Quantity updated"})

@app.route("/remove_from_cart", methods=["POST"])
def remove_from_cart():
    data = request.json
    sku = data.get("sku")
    user_session = session.get("user_id", request.remote_addr)

    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM cart WHERE sku = %s AND user_session = %s", (sku, user_session))
    
    conn.commit()
    conn.close()

    return jsonify({"message": "Item removed"})

@app.route('/check_login')
def check_login():
    return jsonify({"logged_in": 'user_id' in session})



@app.route("/checkout")
def checkout():
    if 'user_id' not in session:
        return redirect('/login')  
    return render_template('checkout.html')  



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        db = get_db_connection()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        db.close()

        if user:
            print("🔹 User Found:", user)  
            stored_hash = user['password_hash']
            print("🔹 Stored Hash:", stored_hash)  
            print("🔹 Entered Password:", password)  

            if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):  
                session['user_id'] = user['id']
                session['username'] = user['username']
                return jsonify({"success": True})  
            else:
                print(" Password does not match!")  
                return jsonify({"success": False})  
        else:
            print(" No user found!")  
            return jsonify({"success": False})  

    return render_template('login.html')





if __name__ == "__main__":
    app.run(debug=True)

