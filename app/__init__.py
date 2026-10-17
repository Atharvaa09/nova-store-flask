
import json
import os
import sqlite3
from pathlib import Path

from flask import (
    Flask,
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE = BASE_DIR / "data" / "nova_store.db"
PRODUCTS_FILE = BASE_DIR / "data" / "products.json"


def get_db():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    DATABASE.parent.mkdir(parents=True, exist_ok=True)
    with get_db() as db:
        db.execute(
            "CREATE TABLE IF NOT EXISTS orders ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "customer_name TEXT NOT NULL, "
            "email TEXT NOT NULL, total REAL NOT NULL, "
            "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
        )
        db.execute(
            "CREATE TABLE IF NOT EXISTS order_items ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "order_id INTEGER NOT NULL, "
            "product_id INTEGER NOT NULL, "
            "product_name TEXT NOT NULL, "
            "quantity INTEGER NOT NULL, "
            "unit_price REAL NOT NULL, "
            "FOREIGN KEY(order_id) REFERENCES orders(id))"
        )


def load_products():
    with PRODUCTS_FILE.open(encoding="utf-8") as file:
        return json.load(file)


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.environ.get(
            "SECRET_KEY",
            "dev-key-change-for-real-deployment",
        ),
        TESTING=False,
    )
    if test_config:
        app.config.update(test_config)
    init_db()

    @app.get("/")
    def index():
        products = load_products()
        query = request.args.get("q", "").strip().lower()
        category = request.args.get("category", "All")
        categories = sorted(
            {product["category"] for product in products}
        )
        filtered = [
            product for product in products
            if query in (
                product["name"] + " " + product["description"]
            ).lower()
            and (
                category == "All"
                or product["category"] == category
            )
        ]
        return render_template(
            "index.html",
            products=filtered,
            categories=categories,
            selected_category=category,
            query=request.args.get("q", ""),
            cart_count=sum(session.get("cart", {}).values()),
        )

    @app.post("/cart/add/<int:product_id>")
    def add_to_cart(product_id):
        product = next(
            (p for p in load_products() if p["id"] == product_id),
            None,
        )
        if product is None:
            abort(404)
        cart = session.get("cart", {})
        key = str(product_id)
        cart[key] = min(int(cart.get(key, 0)) + 1, 10)
        session["cart"] = cart
        flash(f'{product["name"]} added to your bag.')
        return redirect(request.referrer or url_for("index"))

    @app.get("/cart")
    def cart():
        products_by_id = {
            str(p["id"]): p for p in load_products()
        }
        items = [
            {
                **products_by_id[product_id],
                "quantity": quantity,
                "line_total": (
                    products_by_id[product_id]["price"] * quantity
                ),
            }
            for product_id, quantity in session.get(
                "cart", {}
            ).items()
            if product_id in products_by_id
        ]
        total = sum(item["line_total"] for item in items)
        return render_template(
            "cart.html",
            items=items,
            total=total,
            cart_count=sum(session.get("cart", {}).values()),
        )

    @app.post("/cart/update/<int:product_id>")
    def update_cart(product_id):
        cart_data = session.get("cart", {})
        quantity = request.form.get("quantity", type=int)
        key = str(product_id)
        if quantity is None or quantity < 1:
            cart_data.pop(key, None)
        else:
            cart_data[key] = min(quantity, 10)
        session["cart"] = cart_data
        return redirect(url_for("cart"))

    @app.post("/cart/remove/<int:product_id>")
    def remove_from_cart(product_id):
        cart_data = session.get("cart", {})
        cart_data.pop(str(product_id), None)
        session["cart"] = cart_data
        return redirect(url_for("cart"))

    @app.route("/checkout", methods=["GET", "POST"])
    def checkout():
        products_by_id = {
            str(p["id"]): p for p in load_products()
        }
        items = [
            {
                **products_by_id[product_id],
                "quantity": quantity,
                "line_total": (
                    products_by_id[product_id]["price"] * quantity
                ),
            }
            for product_id, quantity in session.get(
                "cart", {}
            ).items()
            if product_id in products_by_id
        ]
        total = sum(item["line_total"] for item in items)

        if not items:
            flash("Your bag is empty. Add a product before checkout.")
            return redirect(url_for("index"))

        if request.method == "POST":
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip()

            if (
                len(name) < 2
                or "@" not in email
                or "." not in email.split("@")[-1]
            ):
                return render_template(
                    "checkout.html",
                    items=items,
                    total=total,
                    cart_count=sum(
                        session.get("cart", {}).values()
                    ),
                    error="Enter a valid name and email.",
                )

            with get_db() as db:
                cursor = db.execute(
                    "INSERT INTO orders "
                    "(customer_name, email, total) "
                    "VALUES (?, ?, ?)",
                    (name, email, total),
                )
                order_id = cursor.lastrowid

                for item in items:
                    db.execute(
                        "INSERT INTO order_items "
                        "(order_id, product_id, product_name, "
                        "quantity, unit_price) "
                        "VALUES (?, ?, ?, ?, ?)",
                        (
                            order_id,
                            item["id"],
                            item["name"],
                            item["quantity"],
                            item["price"],
                        ),
                    )

            session["cart"] = {}
            return redirect(
                url_for("order_confirmation", order_id=order_id)
            )

        return render_template(
            "checkout.html",
            items=items,
            total=total,
            cart_count=sum(session.get("cart", {}).values()),
            error=None,
        )

    @app.get("/orders/<int:order_id>")
    def order_confirmation(order_id):
        with get_db() as db:
            order = db.execute(
                "SELECT * FROM orders WHERE id = ?",
                (order_id,),
            ).fetchone()
            items = db.execute(
                "SELECT * FROM order_items WHERE order_id = ?",
                (order_id,),
            ).fetchall()

        if order is None:
            abort(404)

        return render_template(
            "confirmation.html",
            order=order,
            items=items,
            cart_count=sum(session.get("cart", {}).values()),
        )

    @app.get("/health")
    def health():
        return {"status": "ok", "app": "NOVA Store"}

    return app
