PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS OrderItems;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Stock;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Sizes;
DROP TABLE IF EXISTS Manufacturers;
DROP TABLE IF EXISTS Categories;
DROP TABLE IF EXISTS Users;

CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    last_name TEXT NOT NULL,
    first_name TEXT NOT NULL,
    middle_name TEXT,
    login TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL
        CHECK (role IN ('Администратор', 'Менеджер', 'Авторизованный пользователь'))
);

CREATE TABLE Categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE Manufacturers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE Sizes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    value TEXT NOT NULL UNIQUE
);

CREATE TABLE Products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL REFERENCES Categories (id),
    manufacturer_id INTEGER NOT NULL REFERENCES Manufacturers (id),
    name TEXT NOT NULL,
    subcategory TEXT,
    description TEXT,
    composition TEXT,
    price REAL NOT NULL CHECK (price >= 0),
    image TEXT,
    UNIQUE (name, manufacturer_id)
);

CREATE TABLE Stock (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL REFERENCES Products (id) ON DELETE CASCADE,
    size_id INTEGER NOT NULL REFERENCES Sizes (id),
    quantity INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    UNIQUE (product_id, size_id)
);

CREATE TABLE Orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_date TEXT NOT NULL,
    user_id INTEGER NOT NULL REFERENCES Users (id)
);

CREATE TABLE OrderItems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL REFERENCES Orders (id) ON DELETE CASCADE,
    stock_id INTEGER NOT NULL REFERENCES Stock (id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price REAL NOT NULL CHECK (unit_price >= 0)
);

CREATE INDEX idx_products_category ON Products (category_id);
CREATE INDEX idx_products_manufacturer ON Products (manufacturer_id);
CREATE INDEX idx_stock_product ON Stock (product_id);
CREATE INDEX idx_orders_user ON Orders (user_id);
CREATE INDEX idx_orders_date ON Orders (order_date);
CREATE INDEX idx_orderitems_order ON OrderItems (order_id);
CREATE INDEX idx_orderitems_stock ON OrderItems (stock_id);
