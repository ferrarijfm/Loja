from database import execute_query


class SalesAnalyzer:
    """
    Responsabilidade: gerar relatórios e análises de vendas.

    Não busca dados simples (isso é dos models).
    Aqui vivem as queries complexas que cruzam
    múltiplas tabelas e geram inteligência.
    """

    # ─────────────────────────────────────────────
    # RELATÓRIO 1 — Produtos mais vendidos
    # ─────────────────────────────────────────────

    @staticmethod
    def top_products(limit: int = 5) -> list[dict]:
        """
        Retorna os produtos mais vendidos por quantidade.

        Args:
            limit: quantidade de produtos no ranking

        Returns:
            Lista de dicts com name, total_sold, total_revenue
        """
        return execute_query("""
            SELECT
                p.name                        AS name,
                SUM(oi.quantity)              AS total_sold,
                SUM(oi.quantity * oi.unit_price) AS total_revenue
            FROM     order_items oi
            JOIN     products    p  ON oi.product_id = p.id
            GROUP BY p.name
            ORDER BY total_sold DESC
            LIMIT    %s
        """, (limit,))

    # ─────────────────────────────────────────────
    # RELATÓRIO 2 — Clientes que mais gastaram
    # ─────────────────────────────────────────────

    @staticmethod
    def top_customers(limit: int = 5) -> list[dict]:
        """
        Retorna os clientes que mais gastaram no total.

        Args:
            limit: quantidade de clientes no ranking

        Returns:
            Lista de dicts com name, total_orders, total_spent
        """
        return execute_query("""
            SELECT
                c.name                           AS name,
                COUNT(DISTINCT o.id)             AS total_orders,
                SUM(oi.quantity * oi.unit_price) AS total_spent
            FROM     customers   c
            JOIN     orders      o  ON o.customers_id  = c.id
            JOIN     order_items oi ON oi.order_id = o.id
            GROUP BY c.name
            ORDER BY total_spent DESC
            LIMIT    %s
        """, (limit,))

    # ─────────────────────────────────────────────
    # RELATÓRIO 3 — Receita por categoria
    # ─────────────────────────────────────────────

    @staticmethod
    def revenue_by_category() -> list[dict]:
        """
        Retorna a receita total gerada por cada categoria.

        Returns:
            Lista de dicts com category, total_sold, total_revenue
        """
        return execute_query("""
            SELECT
                cat.name                         AS category,
                SUM(oi.quantity)                 AS total_sold,
                SUM(oi.quantity * oi.unit_price) AS total_revenue
            FROM     order_items oi
            JOIN     products    p   ON oi.product_id   = p.id
            JOIN     categories  cat ON p.category_id   = cat.id
            GROUP BY cat.name
            ORDER BY total_revenue DESC
        """)

    # ─────────────────────────────────────────────
    # RELATÓRIO 4 — Resumo geral da loja
    # ─────────────────────────────────────────────

    @staticmethod
    def general_summary() -> dict:
        """
        Retorna um resumo geral com os principais
        números da loja.

        Returns:
            Dict com total_customers, total_products,
            total_orders e total_revenue
        """
        rows = execute_query("""
            SELECT
                (SELECT COUNT(*) FROM customers)   AS total_customers,
                (SELECT COUNT(*) FROM products)    AS total_products,
                (SELECT COUNT(*) FROM orders)      AS total_orders,
                (
                    SELECT COALESCE(SUM(quantity * unit_price), 0)
                    FROM   order_items
                )                                  AS total_revenue
        """)
        return rows[0]

    # ─────────────────────────────────────────────
    # RELATÓRIO 5 — Produtos com estoque baixo
    # ─────────────────────────────────────────────

    @staticmethod
    def low_stock(threshold: int = 20) -> list[dict]:
        """
        Retorna produtos com estoque abaixo do limite.

        Args:
            threshold: limite mínimo de estoque

        Returns:
            Lista de dicts com name, stock, category
        """
        return execute_query("""
            SELECT
                p.name       AS name,
                p.stock      AS stock,
                c.name       AS category
            FROM  products   p
            JOIN  categories c ON p.category_id = c.id
            WHERE p.stock < %s
            ORDER BY p.stock ASC
        """, (threshold,))