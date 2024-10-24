from .fake_data import _add_fake_data
import sqlite3
from threading import Lock

CREATE_TABLES_QUERY = """
DROP TABLE IF EXISTS ingredient;
DROP TABLE IF EXISTS product;
DROP TABLE IF EXISTS supplier;

-- Create the product table
CREATE TABLE product (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    manufacturer TEXT NOT NULL,
    homepage_image TEXT,
    background_image TEXT
);

-- Create the supplier table
CREATE TABLE supplier (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT NOT NULL,
    rating TEXT NOT NULL
);

-- Create the ingredient table
CREATE TABLE ingredient (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    product_id TEXT,
    supplier_id TEXT,
    FOREIGN KEY (product_id) REFERENCES product(id),
    FOREIGN KEY (supplier_id) REFERENCES supplier(id)
);
"""

PRODUCTS_FETCH_QUERY = """
SELECT p.id AS product_id, p.name AS product_name, p.manufacturer, p.homepage_image, p.background_image,
       i.name AS ingredient_name, s.name AS supplier_name, 
       s.location AS supplier_location, s.rating AS supplier_rating
FROM product p
JOIN ingredient i ON p.id = i.product_id
JOIN supplier s ON i.supplier_id = s.id;
"""

ONLY_PRODUCTS_QUERY = """
SELECT p.id AS product_id, p.name AS product_name, p.manufacturer, p.homepage_image, p.background_image
FROM product p;
"""

# PRODUCTS CRUD
PRODUCTS_CREATE_QUERY = """
INSERT INTO product (id, name, manufacturer, homepage_image, background_image) VALUES (?, ?, ?, ?, ?);
"""

PRODUCTS_READ_QUERY = """
SELECT * FROM product WHERE id = ?;
"""

PRODUCTS_UPDATE_QUERY = """
UPDATE product SET name = ?, manufacturer = ?, homepage_image = ?, background_image = ? WHERE id = ?;
"""

PRODUCTS_DELETE_QUERY = """
DELETE FROM product WHERE id = ?;
"""

# SUPPLIERS CRUD
SUPPLIER_CREATE_QUERY = """
INSERT INTO supplier (id, name, location, rating) VALUES (?, ?, ?, ?);
"""

SUPPLIER_READ_QUERY = """
SELECT * FROM supplier WHERE id = ?;
"""

SUPPLIER_UPDATE_QUERY = """
UPDATE supplier SET name = ?, location = ?, rating = ? WHERE id = ?;
"""

SUPPLIER_DELETE_QUERY = """
DELETE FROM supplier WHERE id = ?;
"""

# INGREDIENTS CRUD
INGREDIENTS_FOR_PRODUCT_QUERY = """
SELECT i.id AS ingredient_id, i.name AS ingredient_name, 
       s.id AS supplier_id, s.name AS supplier_name, s.location AS supplier_location, s.rating AS supplier_rating
FROM ingredient i
JOIN supplier s ON i.supplier_id = s.id
WHERE i.product_id = ?;
"""

INGREDIENT_CREATE_QUERY = """
INSERT INTO ingredient (name, product_id, supplier_id) VALUES (?, ?, ?);
"""

INGREDIENT_READ_QUERY = """
SELECT * FROM ingredient WHERE id = ?;
"""

INGREDIENT_UPDATE_QUERY = """
UPDATE ingredient SET name = ?, product_id = ?, supplier_id = ? WHERE id = ?;
"""

INGREDIENT_DELETE_QUERY = """
DELETE FROM ingredient WHERE id = ?;
"""


class Database:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.db = sqlite3.connect("test.db", check_same_thread=False)
        self.createTables()
        self.createSampleProducts()

    def createTables(self):
        self.db.executescript(CREATE_TABLES_QUERY)
        self.db.commit()

    def createSampleProducts(self):
        _add_fake_data(self)

    def fetchProducts(self):
        cursor = self.db.execute(PRODUCTS_FETCH_QUERY)
        products = {}
        for row in cursor.fetchall():
            if row[0] not in products:
                products[row[0]] = {}

            products[row[0]].update(
                {
                    "product_id": row[0],
                    "product_name": row[1],
                    "manufacturer": row[2],
                    "homepage_image": row[3],
                    "background_image": row[4],
                }
            )
            if "ingredients" not in products[row[0]]:
                products[row[0]]["ingredients"] = []

            products[row[0]]["ingredients"].append(
                {
                    "ingredient_name": row[5],
                    "supplier_name": row[6],
                    "supplier_location": row[7],
                    "supplier_rating": row[8],
                }
            )

        cursor = self.db.execute(ONLY_PRODUCTS_QUERY)
        for row in cursor.fetchall():
            if row[0] not in products:
                products[row[0]] = {
                    "product_id": row[0],
                    "product_name": row[1],
                    "manufacturer": row[2],
                    "homepage_image": row[3],
                    "background_image": row[4],
                }

        f = []
        for i in products.values():
            f.append(i)

        return f

    def createProduct(self, id, name, manufacturer, homepage_image, background_image):
        self.db.execute(PRODUCTS_CREATE_QUERY, (id, name, manufacturer, homepage_image, background_image))
        self.db.commit()

    def readProduct(self, id):
        cursor = self.db.execute(PRODUCTS_READ_QUERY, (id,))
        row = cursor.fetchone()
        return {
            "id": row[0],
            "name": row[1],
            "manufacturer": row[2],
            "homepage_image": row[3],
            "background_image": row[4]
        } if row else None

    def getFullProduct(self, id):
        prod = self.readProduct(id)
        ing = self.fetchIngredientsForProduct(id)
        prod["ingredients"] = ing

        return prod

    def updateProduct(self, id, name, manufacturer, homepage_image, background_image):
        self.db.execute(PRODUCTS_UPDATE_QUERY, (name, manufacturer, homepage_image, background_image, id))
        self.db.commit()

    def deleteProduct(self, id):
        self.db.execute(PRODUCTS_DELETE_QUERY, (id,))
        self.db.commit()

    def fetchAllSuppliers(self):
        cursor = self.db.execute("SELECT * FROM supplier")
        suppliers = cursor.fetchall()
        return [
            {"id": row[0], "name": row[1], "location": row[2], "rating": row[3]}
            for row in suppliers
        ]

    def createSupplier(self, id, name, location, rating):
        self.db.execute(SUPPLIER_CREATE_QUERY, (id, name, location, rating))
        self.db.commit()

    def readSupplier(self, id):
        cursor = self.db.execute(SUPPLIER_READ_QUERY, (id,))
        row = cursor.fetchone()
        return (
            {"id": row[0], "name": row[1], "location": row[2], "rating": row[3]}
            if row
            else None
        )

    def updateSupplier(self, id, name, location, rating):
        self.db.execute(SUPPLIER_UPDATE_QUERY, (name, location, rating, id))
        self.db.commit()

    def deleteSupplier(self, id):
        self.db.execute(SUPPLIER_DELETE_QUERY, (id,))
        self.db.commit()

    def fetchIngredientsForProduct(self, product_id):
        cursor = self.db.execute(INGREDIENTS_FOR_PRODUCT_QUERY, (product_id,))
        ingredients = cursor.fetchall()
        return [
            {
                "id": row[0],
                "name": row[1],
                "supplier_id": row[2],
                "supplier_name": row[3],
                "supplier_location": row[4],
                "supplier_rating": row[5],
            }
            for row in ingredients
        ]

    def createIngredient(self, name, product_id, supplier_id):
        self.db.execute(INGREDIENT_CREATE_QUERY, (name, product_id, supplier_id))
        self.db.commit()

    def readIngredient(self, id):
        cursor = self.db.execute(INGREDIENT_READ_QUERY, (id,))
        row = cursor.fetchone()
        return (
            {"id": row[0], "name": row[1], "product_id": row[2], "supplier_id": row[3]}
            if row
            else None
        )

    def updateIngredient(self, id, name, product_id, supplier_id):
        self.db.execute(INGREDIENT_UPDATE_QUERY, (name, product_id, supplier_id, id))
        self.db.commit()

    def deleteIngredient(self, id):
        self.db.execute(INGREDIENT_DELETE_QUERY, (id,))
        self.db.commit()


db_instance = Database()
