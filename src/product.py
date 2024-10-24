from flask import Blueprint, redirect, request, render_template, current_app
from .fake_data import generate_random_id

product_bp = Blueprint("product", __name__)


@product_bp.route("/add", methods=["GET", "POST"])
def add_product():
    db_instance = current_app.config["DB_INSTANCE"]
    if request.method == "POST":
        # Fetch data from form
        product_name = request.form.get("name")
        manufacturer = request.form.get("manufacturer")
        product_id = generate_random_id()

        # Add product to the database
        db_instance.createProduct(product_id, product_name, manufacturer)
        return redirect("/product/list")

    return render_template("add.jinja")


@product_bp.route("/edit/<product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    db_instance = current_app.config["DB_INSTANCE"]
    product = db_instance.readProduct(product_id)
    ingredients = db_instance.fetchIngredientsForProduct(product_id)
    suppliers = db_instance.fetchAllSuppliers()

    if request.method == "POST":
        # Save changes to product
        if "save" in request.form:
            product_name = request.form["name"]
            manufacturer = request.form["manufacturer"]
            db_instance.updateProduct(product_id, product_name, manufacturer)

        # Add new ingredient
        if "add_ingredient" in request.form:
            ingredient_name = request.form["ingredient_name"]
            supplier_id = request.form["supplier_id"]
            if ingredient_name and supplier_id:
                db_instance.createIngredient(ingredient_name, product_id, supplier_id)

        # Delete an ingredient
        if "delete_ingredient" in request.form:
            ingredient_id = request.form["delete_ingredient"]
            db_instance.deleteIngredient(ingredient_id)

        # Delete the product and all its ingredients
        if "delete_product" in request.form:
            # First, delete all ingredients linked to the product
            db_instance.deleteIngredientsByProduct(product_id)
            # Then, delete the product itself
            db_instance.deleteProduct(product_id)
            return redirect("/products")

    return render_template(
        "edit.jinja",
        product=product,
        ingredients=ingredients,
        suppliers=suppliers
    )

@product_bp.route("/list")
def product_list():
    db_instance = current_app.config["DB_INSTANCE"]
    products = db_instance.fetchProducts()
    return render_template("list.jinja", products=products)
