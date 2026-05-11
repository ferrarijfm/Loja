INSERT INTO categories (name) VALUES
    ('Eletrônicos'),
    ('Roupas'),
    ('Alimentos');


INSERT INTO products (name, price, stock, category_id) VALUES
    ('Notebook',        3500.00, 10, 1),
    ('Mouse',             80.00, 50, 1),
    ('Teclado',          150.00, 30, 1),
    ('Camiseta',          49.90, 100, 2),
    ('Calça Jeans',      120.00, 60, 2),
    ('Arroz 5kg',         25.00, 200, 3),
    ('Café 500g',         18.00, 150, 3);

INSERT INTO customers (name, email) VALUES
    ('Ana Silva',       'ana@email.com'),
    ('Bruno Costa',     'bruno@email.com'),
    ('Carla Souza',     'carla@email.com');

INSERT INTO orders (customers_id) VALUES
    (1),
    (1),
    (2);

INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
    (1, 1, 1, 3500.00),
    (1, 2, 2,   80.00),
    (2, 4, 3,   49.90),
    (3, 3, 1,  150.00),
    (3, 6, 2,   25.00);