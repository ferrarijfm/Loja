#representar os dados 
from database import execute_query, execute_write

# Tabela Categories do banco
class Category:
    
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name 
        
    def __str__(self):
        return f"Category(id={self.id}, name={self.name})"
    
    def __repr__(self):
        return self.__str__()
    
    # Retorna todas as categorias do banco 
    @classmethod
    def get_all(cls) -> list["Category"]:
        
        rows = execute_query("SELECT id, name FROM categories")
        
        return [cls (row["id"], row["name"]) for row in rows]

    # Retorna uma categoria pelo ID ou None se não existir
    @classmethod
    def get_by_id(cls, category_id: int) -> "Category | None":
        
        rows = execute_query(
            "SELECT id, name FROM categories WHERE id = %s",
            (category_id,)
        )        
        
        if not rows:
            return None
        
        return cls(rows[0]["id"], rows[0]["name"])

# Representa a tabela products do banco
class Product:
    
    def __init__(
        self,
        id:            int,
        name:          str,
        price:         float,
        stock:         int,
        category_id:   int,
        category_name: str = None,
                 
    ):
        self.id               = id
        self.name             = name
        self._price           = price
        self.stock            = stock
        self.category_id      = category_id
        self.category_name    = category_name
        
    # Protege o preço de valores invalidos 
    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        if value < 0:
            raise ValueError(f"Preço não pode ser negativo: {value}")
        self._price = value
    
    #Retorna True se o produto tem estoque
    def is_available(self) -> bool:
        return self.stock > 0

    def __str__(self):
        category = self.category_name or f"ID {self.category_id}"
        status = "DISPONIVEL" if self.is_available() else "SEM ESTOQUE"
        return (
            f"[{self.id}] {self.name} | "
            f"R$ {self.price:.2f} | "
            f"Categoris: {category} {status}"
        )
        
    def __repr__(self):
        return self.__str__
    
    # Constroi um Product a partir de um dicionario retornado pelo banco 
    @classmethod
    def _from_row(cls, row: dict) -> "Product":
        return cls(
            id            = row["id"],
            name          = row["name"],
            price         = float(row["price"]),
            stock         = row["stock"],
            category_id   = row["category_id"],
            category_name = row.get("category_name"),
        )

    # Retorna todos os produtos com o nome da categoria
    @classmethod
    def get_all(cls) -> list["Product"]:
        rows = execute_query("""
            SELECT
                p.id,
                p.name,
                p.price,
                p.stock,
                p.category_id,
                c.name AS category_name
            FROM  products   p
            JOIN  categories c ON p.category_id = c.id
            ORDER BY p.name
        """)
        return [cls._from_row(row) for row in rows]

    # Retorna um produto pelo ID ou None.
    @classmethod
    def get_by_id(cls, product_id: int) -> "Product | None":
        rows = execute_query("""
            SELECT
                p.id,
                p.name,
                p.price,
                p.stock,
                p.category_id,
                c.name AS category_name
            FROM  products   p
            JOIN  categories c ON p.category_id = c.id
            WHERE p.id = %s
        """, (product_id,))

        if not rows:
            return None

        return cls._from_row(rows[0])

    #Retorna todos os produtos de uma categoria
    @classmethod
    def get_by_category(cls, category_id: int) -> list["Product"]:
        rows = execute_query("""
            SELECT
                p.id,
                p.name,
                p.price,
                p.stock,
                p.category_id,
                c.name AS category_name
            FROM  products   p
            JOIN  categories c ON p.category_id = c.id
            WHERE p.category_id = %s
            ORDER BY p.price
        """, (category_id,))

        return [cls._from_row(row) for row in rows]

    #Atualiza o estoque de um produto
    @classmethod
    def update_stock(cls, product_id: int, quantity: int) -> None:
        execute_write("""
            UPDATE products
            SET    stock = stock + %s
            WHERE  id    = %s
        """, (quantity, product_id))
        
class Customer:
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email
    
    def __str__(self):
        return f"[{self.id}] {self.name} {self.email}"
    
    def __repr__(self):
        return self.__str__()
    
    # Retorna todos os clientes
    @classmethod
    def get_all(cls) -> list["Customer"]:
        rows = execute_query("""
            SELECT id, name, email
            FROM customers
            ORDER BY name                             
        """)
        return [cls(r["id"], r["name"], r["email"]) for r in rows]
    
    # Retorna um cliente pelo id ou None
    @classmethod
    def get_by_id(cls, customers_id: int) -> "Customer | None":
        rows = execute_query("""
            SELECT id, name, email
            FROM customers
            WHERE id = %s
            """, (customers_id) )
        
        if not rows:
            return None
        
        r = rows[0]
        return cls(r["id"], r["name"], r["email"])
    
# OrderItem representa um item dentro de um pedido. Tabela: order_items
class OrderItem:
    def __init__(
        self,
        id: int,
        order_id: int,
        product_id: int,
        quantity: int,
        unit_price: float,
        product_name: str = None,
    ):
        self.id = id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.product_name = product_name
        
    #Calcula o subtotal do item (preço x quantidade)
    @property
    def subtotal(self) -> float:
        return self.unit_price * self.quantity
    
    def __str__(self):
        name = self.product_name or f"Produto {self.product_id}"
        return (
            f" {name} | "
            f"Qtd : {self.quantity}"
            f"R$ {self.unit_price:.2f} = "
            f"R$ {self.subtotal:.2f}"
        )
    
# representa a tabela orders do banco de dados. Operações relacionadas a pedidos    
class Order :
    
    def __init__(
        self,
        id: int,
        customers_id:   int,
        created_at,
        customer_name: str  = None,
        items:         list = None,
    ):
        self.id            = id
        self.customers_id   = customers_id
        self.created_at    = created_at
        self.customer_name = customer_name
        self.items         = items or []

    #Soma o subtotal de todos os itens do pedido.
    @property
    def total(self) -> float:
        return sum(item.subtotal for item in self.items)

    def __str__(self):
        name = self.customer_name or f"Cliente {self.customers_id}"
        date = self.created_at.strftime("%d/%m/%Y %H:%M")
        return (
            f"Pedido #{self.id} | "
            f"Cliente: {name} | "
            f"Data: {date} | "
            f"Total: R$ {self.total:.2f}"
        )


    #Retorna todos os pedidos de um cliente com seus itens.
    # Busca os pedidos do cliente
    @classmethod
    def get_by_customer(cls, customers_id: int) -> list["Order"]:
        order_rows = execute_query("""
            SELECT
                o.id,
                o.customers_id,
                o.created_at,
                c.name AS customer_name
            FROM  orders    o
            JOIN  customers c ON o.customers_id = c.id
            WHERE o.customers_id = %s
            ORDER BY o.created_at DESC
        """, (customers_id,))

        orders = []

        # Para cada pedido, busca os itens
        for row in order_rows:
            item_rows = execute_query("""
                SELECT
                    oi.id,
                    oi.order_id,
                    oi.product_id,
                    oi.quantity,
                    oi.unit_price,
                    p.name AS product_name
                FROM  order_items oi
                JOIN  products    p  ON oi.product_id = p.id
                WHERE oi.order_id = %s
            """, (row["id"],))

        # Constrói os objetos OrderItem
            items = [
                OrderItem(
                    id           = i["id"],
                    order_id     = i["order_id"],
                    product_id   = i["product_id"],
                    quantity     = i["quantity"],
                    unit_price   = float(i["unit_price"]),
                    product_name = i["product_name"],
                )
                for i in item_rows
            ]

        # Constrói o objeto Order com os itens
            orders.append(cls(
                id            = row["id"],
                customers_id   = row["customers_id"],
                created_at    = row["created_at"],
                customer_name = row["customer_name"],
                items         = items,
            ))

        return orders