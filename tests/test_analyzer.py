import sys 
import os 
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__),"..", "src"))

from analyzer import SalesAnalyzer


@pytest.fixture
def top_products(): # Retorna o resultado de top_products para os testes
    return SalesAnalyzer.top_products()

@pytest.fixture
def top_customers(): # Retorna o resultado de top_customers para os testes
    return SalesAnalyzer.top_customers()

@pytest.fixture
def summary(): # Retorna receita por categoria para os testes
    return SalesAnalyzer.general_summary()
 
@pytest.fixture
def revenue(): # Retorna receita por categoria para os testes
    return SalesAnalyzer.revenue_by_category()


class TestTopProducts: # testes para o relatorio de produtos mais vendidos
    def test_returns_list(self, top_products):
        assert isinstance(top_products, list)
    
    def test_list_is_not_empty(self, top_products): # Deve retornar pelo menos um produto
        assert len(top_products) > 0

    def test_respects_limit(self): # deve respeitar o limite passado como argumento
        result = SalesAnalyzer.top_products(limit=2)
        assert len(result) <= 2

    def test_has_expected_keys(self, top_products): # Cada item deve ter as chaves name, total_sold e total_revenue
        first = top_products[0]
        assert "name"          in first
        assert "total_sold"    in first
        assert "total_revenue" in first

    def test_ordered_by_quantity(self, top_products):
        """
        O primeiro produto deve ter quantidade
        maior ou igual ao segundo.
        """
        if len(top_products) >= 2:
            first  = int(top_products[0]["total_sold"])
            second = int(top_products[1]["total_sold"])
            assert first >= second

    def test_total_sold_is_positive(self, top_products):
        """Quantidade vendida deve ser positiva."""
        for product in top_products:
            assert int(product["total_sold"]) > 0

    def test_total_revenue_is_positive(self, top_products):
        """Receita deve ser positiva."""
        for product in top_products:
            assert float(product["total_revenue"]) > 0


# ─────────────────────────────────────────────────────
# TESTES — TopCustomers
# ─────────────────────────────────────────────────────

class TestTopCustomers:
    """Testes para o relatório de clientes."""

    def test_returns_list(self, top_customers):
        """Deve retornar uma lista."""
        assert isinstance(top_customers, list)

    def test_list_is_not_empty(self, top_customers):
        """Deve retornar pelo menos um cliente."""
        assert len(top_customers) > 0

    def test_respects_limit(self):
        """Deve respeitar o limite passado."""
        result = SalesAnalyzer.top_customers(limit=1)
        assert len(result) <= 1

    def test_has_expected_keys(self, top_customers):
        """Cada item deve ter as chaves esperadas."""
        first = top_customers[0]
        assert "name"         in first
        assert "total_orders" in first
        assert "total_spent"  in first

    def test_ordered_by_total_spent(self, top_customers):
        """
        O primeiro cliente deve ter gasto
        maior ou igual ao segundo.
        """
        if len(top_customers) >= 2:
            first  = float(top_customers[0]["total_spent"])
            second = float(top_customers[1]["total_spent"])
            assert first >= second

    def test_total_orders_is_positive(self, top_customers):
        """Total de pedidos deve ser positivo."""
        for customer in top_customers:
            assert int(customer["total_orders"]) > 0

    def test_ana_is_top_customer(self, top_customers):
        """
        Ana Silva deve ser o top cliente
        pois tem o maior gasto no seed.
        """
        top = top_customers[0]
        assert top["name"] == "Ana Silva"


# ─────────────────────────────────────────────────────
# TESTES — RevenueByCategory
# ─────────────────────────────────────────────────────

class TestRevenueByCategory:
    """Testes para o relatório de receita por categoria."""

    def test_returns_list(self, revenue):
        """Deve retornar uma lista."""
        assert isinstance(revenue, list)

    def test_list_is_not_empty(self, revenue):
        """Deve retornar pelo menos uma categoria."""
        assert len(revenue) > 0

    def test_has_expected_keys(self, revenue):
        """Cada item deve ter as chaves esperadas."""
        first = revenue[0]
        assert "category"      in first
        assert "total_sold"    in first
        assert "total_revenue" in first

    def test_ordered_by_revenue(self, revenue):
        """
        A primeira categoria deve ter receita
        maior ou igual à segunda.
        """
        if len(revenue) >= 2:
            first  = float(revenue[0]["total_revenue"])
            second = float(revenue[1]["total_revenue"])
            assert first >= second

    def test_eletronicos_is_top(self, revenue):
        """
        Eletrônicos deve ser a categoria com
        maior receita no seed.
        """
        top = revenue[0]
        assert top["category"] == "Eletrônicos"


# ─────────────────────────────────────────────────────
# TESTES — GeneralSummary
# ─────────────────────────────────────────────────────

class TestGeneralSummary:
    """Testes para o resumo geral da loja."""

    def test_returns_dict(self, summary):
        """Deve retornar um dicionário."""
        assert isinstance(summary, dict)

    def test_has_expected_keys(self, summary):
        """Deve ter todas as chaves esperadas."""
        assert "total_customers" in summary
        assert "total_products"  in summary
        assert "total_orders"    in summary
        assert "total_revenue"   in summary

    def test_customers_count(self, summary):
        """Deve ter 3 clientes conforme o seed."""
        assert int(summary["total_customers"]) == 3

    def test_products_count(self, summary):
        """Deve ter 7 produtos conforme o seed."""
        assert int(summary["total_products"]) == 7

    def test_orders_count(self, summary):
        """Deve ter 3 pedidos conforme o seed."""
        assert int(summary["total_orders"]) == 3

    def test_revenue_is_positive(self, summary):
        """Receita total deve ser positiva."""
        assert float(summary["total_revenue"]) > 0

    def test_revenue_value(self, summary):
        """
        Receita total deve ser 3959.70
        conforme os dados do seed.
        """
        revenue = float(summary["total_revenue"])
        assert revenue > 0 
        assert isinstance(revenue, float)

# ─────────────────────────────────────────────────────
# TESTES — LowStock
# ─────────────────────────────────────────────────────

class TestLowStock:
    """Testes para o relatório de estoque baixo."""

    def test_returns_list(self):
        """Deve retornar uma lista."""
        result = SalesAnalyzer.low_stock()
        assert isinstance(result, list)

    def test_high_threshold_returns_products(self):
        """
        Com threshold alto (999),
        deve retornar todos os produtos.
        """
        result = SalesAnalyzer.low_stock(threshold=999)
        assert len(result) > 0

    def test_zero_threshold_returns_empty(self):
        """
        Com threshold 0,
        não deve retornar nenhum produto
        pois estoque nunca é negativo.
        """
        result = SalesAnalyzer.low_stock(threshold=0)
        assert len(result) == 0

    def test_stock_below_threshold(self):
        """
        Todos os produtos retornados devem ter
        estoque abaixo do threshold.
        """
        threshold = 50
        result    = SalesAnalyzer.low_stock(threshold=threshold)

        for product in result:
            assert int(product["stock"]) < threshold

    def test_has_expected_keys(self):
        """Cada item deve ter as chaves esperadas."""
        result = SalesAnalyzer.low_stock(threshold=999)

        if result:
            first = result[0]
            assert "name"     in first
            assert "stock"    in first
            assert "category" in first

    def test_ordered_by_stock_asc(self):
        """
        Produtos devem vir ordenados do
        menor estoque para o maior.
        """
        result = SalesAnalyzer.low_stock(threshold=999)

        if len(result) >= 2:
            first  = int(result[0]["stock"])
            second = int(result[1]["stock"])
            assert first <= second