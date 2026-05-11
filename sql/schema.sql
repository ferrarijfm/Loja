DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS customers;

-- Categoria dos produtos
CREATE TABLE categories (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Produtos
CREATE TABLE products (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(200) NOT NULL,
    price       NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    stock       INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
    category_id INTEGER NOT NULL,

    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Clientes
CREATE TABLE customers (
    id     SERIAL PRIMARY KEY,
    name   VARCHAR(200) NOT NULL,
    email  VARCHAR(200) NOT NULL UNIQUE
);

--Pedidos
CREATE TABLE orders (
    id           SERIAL PRIMARY KEY,
    customers_id INTEGER NOT NULL,
    created_at   TIMESTAMP DEFAULT NOW()
);

-- Itens do pedido (tabela pivô entre orders e products)
CREATE TABLE order_items (
    id         SERIAL PRIMARY KEY, 
    order_id   INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity   INTEGER NOT NULL CHECK (quantity > 0),
    unit_price NUMERIC(10, 2) NOT NULL,

    FOREIGN KEY (order_id)   REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);