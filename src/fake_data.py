import random
import string

# from .db import Database


def generate_random_id(length=6):
    return "".join(random.choices(string.ascii_lowercase, k=length))


def _add_fake_data(db):
    # Suppliers
    supplier_1_id = generate_random_id()
    supplier_2_id = generate_random_id()
    supplier_3_id = generate_random_id()
    supplier_4_id = generate_random_id()
    supplier_5_id = generate_random_id()
    supplier_6_id = generate_random_id()
    supplier_7_id = generate_random_id()

    db.createSupplier(supplier_1_id, "Yashaswi Exports", "Bangalore", "8/10")
    db.createSupplier(supplier_2_id, "Shivaji Oil Mills Pvt. Ltd.", "Bangalore", "9/10")
    db.createSupplier(supplier_3_id, "Shiva Shakthi Associates", "Bangalore", "8/10")
    db.createSupplier(
        supplier_4_id, "KMF Ltd (Karnataka Milk Federation)", "Bangalore", "9/10"
    )
    db.createSupplier(supplier_5_id, "E.I.D. Parry (India) Ltd.", "Bagalkot", "8/10")
    db.createSupplier(supplier_6_id, "Manjari Sugars", "Belagavi", "7/10")
    db.createSupplier(supplier_7_id, "Chikmagalur", "Chikmagalur", "8/10")

    # Products
    product_1_id = "chips"
    product_2_id = "cold_coffee"
    product_3_id = "yoghurt"

    db.createProduct(
        product_1_id,
        "Lay's Classic Potato Chips",
        "Frito-Lay",
        "https://ganguram.com/cdn/shop/files/plain-potato-chips.png?v=1709113575&width=480",
        "https://img.freepik.com/premium-vector/chips-pattern-seamless-background-vector_631970-12.jpg",
    )
    db.createProduct(
        product_2_id,
        "Nescafe Cold Coffee",
        "Nestlé",
        "https://mytastycurry.com/wp-content/uploads/2020/04/Cafe-style-cold-coffee-with-icecream.jpg",
        "https://i.pinimg.com/564x/c8/0c/4a/c80c4ae0ba5657d5b3deecc6f4ca33a6.jpg",
    )
    db.createProduct(
        product_3_id,
        "Epigamia Greek Yogurt",
        "Drums Food International",
        "https://www.seriouseats.com/thmb/9jHEWvj_g5Gl46G3dO2RWwpxuRU=/750x0/filters:no_upscale():max_bytes(150000):strip_icc():format(webp)/__opt__aboutcom__coeus__resources__content_migration__serious_eats__seriouseats.com__2019__06__20190614-yogurt-vicky-wasik-8-1b8381eea1b44c17ac31879c11e6c624.jpg",
        "https://img.pikbest.com/wp/202344/homemade-yogurt-macro-close-up-of-creamy-strawberry-with-blueberries_9924373.jpg!bw700",
    )

    # Ingredients for Lay's Classic Potato Chips
    db.createIngredient("Potato", product_1_id, supplier_1_id)
    db.createIngredient("Vegetable Oil", product_1_id, supplier_2_id)
    db.createIngredient("Salt", product_1_id, supplier_3_id)

    # Ingredients for Nescafe Cold Coffee
    db.createIngredient(
        "Water", product_2_id, None
    )  # Assuming water is not tied to a supplier
    db.createIngredient("Milk solids", product_2_id, supplier_4_id)
    db.createIngredient("Sugar", product_2_id, supplier_5_id)
    db.createIngredient("Instant coffee powder", product_2_id, supplier_7_id)
    db.createIngredient("Sweeteners", product_2_id, supplier_6_id)

    # Ingredients for Epigamia Greek Yogurt
    db.createIngredient("Pasteurized double-toned milk", product_3_id, supplier_4_id)
    db.createIngredient("Milk solids", product_3_id, supplier_4_id)
    db.createIngredient(
        "Prebiotic (pectin)", product_3_id, None
    )  # No supplier for this
    db.createIngredient(
        "Permitted lactic acid cultures", product_3_id, None
    )  # No supplier for this
