#interfca com o user
import sys 
import os 

sys.path.insert(0, os.path.dirname(__file__))

from models import Category,Product,Customer,Order
from analyzer import SalesAnalyzer


def clear_screen(): #limpa o terminal
    os.system("clear" if os.name == "posix" else "cls")
    
def print_header(title: str):
    print("\n" + "=" * 50)
    print(f" {title}")
    print("=" * 50)
    

def print_separator():
    print("-" * 50)


def press_enter():
    """Pausa até o usuário apertar Enter."""
    input("\n[ Pressione Enter para voltar... ]")


# ─────────────────────────────────────────────────────
# MENU DE PRODUTOS
# ─────────────────────────────────────────────────────

def menu_products():
    """Submenu de produtos."""
    while True:
        print_header("PRODUTOS")
        print("  [1] Listar todos os produtos")
        print("  [2] Buscar produto por ID")
        print("  [3] Filtrar por categoria")
        print("  [0] Voltar")
        print_separator()

        option = input("  Escolha: ").strip()

        if option == "1":
            show_all_products()
        elif option == "2":
            show_product_by_id()
        elif option == "3":
            show_products_by_category()
        elif option == "0":
            break
        else:
            print("\nOpção inválida!")
            press_enter()


def show_all_products():
    """Lista todos os produtos."""
    print_header("TODOS OS PRODUTOS")

    products = Product.get_all()

    if not products:
        print("  Nenhum produto encontrado.")
        press_enter()
        return

    for product in products:
        print(f"  {product}")

    press_enter()


def show_product_by_id():
    """Busca e exibe um produto pelo ID."""
    print_header("BUSCAR PRODUTO POR ID")

    try:
        product_id = int(input("  Digite o ID do produto: ").strip())
    except ValueError:
        print("\nID inválido! Digite apenas números.")
        press_enter()
        return

    product = Product.get_by_id(product_id)

    if not product:
        print(f"\nProduto com ID {product_id} não encontrado.")
        press_enter()
        return

    print(f"\n  {product}")
    press_enter()


def show_products_by_category():
    """Lista produtos filtrando por categoria."""
    print_header("FILTRAR POR CATEGORIA")

    # Mostra as categorias disponíveis
    categories = Category.get_all()
    for cat in categories:
        print(f"  {cat}")

    print_separator()

    try:
        category_id = int(input("  Digite o ID da categoria: ").strip())
    except ValueError:
        print("\n ID inválido! Digite apenas números.")
        press_enter()
        return

    # Verifica se a categoria existe
    category = Category.get_by_id(category_id)
    if not category:
        print(f"\nCategoria {category_id} não encontrada.")
        press_enter()
        return

    products = Product.get_by_category(category_id)

    print_header(f"PRODUTOS — {category.name.upper()}")

    if not products:
        print("  Nenhum produto nessa categoria.")
        press_enter()
        return

    for product in products:
        print(f"  {product}")

    press_enter()


# ─────────────────────────────────────────────────────
# MENU DE CLIENTES
# ─────────────────────────────────────────────────────

def menu_customers():
    """Submenu de clientes."""
    while True:
        print_header("CLIENTES")
        print("  [1] Listar todos os clientes")
        print("  [2] Ver pedidos de um cliente")
        print("  [0] Voltar")
        print_separator()

        option = input("  Escolha: ").strip()

        if option == "1":
            show_all_customers()
        elif option == "2":
            show_customer_orders()
        elif option == "0":
            break
        else:
            print("\nOpção inválida!")
            press_enter()


def show_all_customers():
    """Lista todos os clientes."""
    print_header("TODOS OS CLIENTES")

    customers = Customer.get_all()

    if not customers:
        print("  Nenhum cliente encontrado.")
        press_enter()
        return

    for customer in customers:
        print(f"  {customer}")

    press_enter()


def show_customer_orders():
    """Exibe os pedidos de um cliente específico."""
    print_header("PEDIDOS DO CLIENTE")

    # Mostra os clientes disponíveis
    customers = Customer.get_all()
    for customer in customers:
        print(f"  {customer}")

    print_separator()

    try:
        customer_id = int(input("  Digite o ID do cliente: ").strip())
    except ValueError:
        print("\n ID inválido! Digite apenas números.")
        press_enter()
        return

    customer = Customer.get_by_id(customer_id)
    if not customer:
        print(f"\nCliente {customer_id} não encontrado.")
        press_enter()
        return

    orders = Order.get_by_customer(customer_id)

    print_header(f"PEDIDOS — {customer.name.upper()}")

    if not orders:
        print("  Esse cliente ainda não fez pedidos.")
        press_enter()
        return

    for order in orders:
        print(f"\n  {order}")
        for item in order.items:
            print(item)
        print_separator()

    press_enter()


# ─────────────────────────────────────────────────────
# MENU DE RELATÓRIOS
# ─────────────────────────────────────────────────────

def menu_reports():
    """Submenu de relatórios."""
    while True:
        print_header("RELATÓRIOS")
        print("  [1] Resumo geral da loja")
        print("  [2] Produtos mais vendidos")
        print("  [3] Clientes que mais gastaram")
        print("  [4] Receita por categoria")
        print("  [5] Produtos com estoque baixo")
        print("  [0] Voltar")
        print_separator()

        option = input("  Escolha: ").strip()

        if option == "1":
            show_general_summary()
        elif option == "2":
            show_top_products()
        elif option == "3":
            show_top_customers()
        elif option == "4":
            show_revenue_by_category()
        elif option == "5":
            show_low_stock()
        elif option == "0":
            break
        else:
            print("\n Opção inválida!")
            press_enter()


def show_general_summary():
    """Exibe o resumo geral da loja."""
    print_header("RESUMO GERAL DA LOJA")

    summary = SalesAnalyzer.general_summary()

    print(f"  Clientes:       {summary['total_customers']}")
    print(f"  Produtos:       {summary['total_products']}")
    print(f"  Pedidos:        {summary['total_orders']}")
    print(f"  Receita total:  R$ {float(summary['total_revenue']):.2f}")

    press_enter()


def show_top_products():
    """Exibe o ranking de produtos mais vendidos."""
    print_header("PRODUTOS MAIS VENDIDOS")

    try:
        limit = int(input("  Quantos produtos no ranking? [padrão 5]: ").strip() or 5)
    except ValueError:
        limit = 5

    products = SalesAnalyzer.top_products(limit)

    if not products:
        print("  Nenhuma venda registrada.")
        press_enter()
        return

    print()
    for i, product in enumerate(products, start=1):
        print(
            f"  {i}. {product['name']:<15} | "
            f"Vendidos: {product['total_sold']:>4} | "
            f"Receita: R$ {float(product['total_revenue']):>10.2f}"
        )

    press_enter()


def show_top_customers():
    """Exibe o ranking de clientes que mais gastaram."""
    print_header("CLIENTES QUE MAIS GASTARAM")

    try:
        limit = int(input("  Quantos clientes no ranking? [padrão 5]: ").strip() or 5)
    except ValueError:
        limit = 5

    customers = SalesAnalyzer.top_customers(limit)

    if not customers:
        print("  Nenhuma venda registrada.")
        press_enter()
        return

    print()
    for i, customer in enumerate(customers, start=1):
        print(
            f"  {i}. {customer['name']:<15} | "
            f"Pedidos: {customer['total_orders']:>3} | "
            f"Total gasto: R$ {float(customer['total_spent']):>10.2f}"
        )

    press_enter()


def show_revenue_by_category():
    """Exibe a receita por categoria."""
    print_header("RECEITA POR CATEGORIA")

    categories = SalesAnalyzer.revenue_by_category()

    if not categories:
        print("  Nenhuma venda registrada.")
        press_enter()
        return

    print()
    for cat in categories:
        print(
            f"  {cat['category']:<15} | "
            f"Vendidos: {cat['total_sold']:>4} | "
            f"Receita: R$ {float(cat['total_revenue']):>10.2f}"
        )

    press_enter()


def show_low_stock():
    """Exibe produtos com estoque baixo."""
    print_header("PRODUTOS COM ESTOQUE BAIXO")

    try:
        threshold = int(input("  Limite mínimo de estoque? [padrão 20]: ").strip() or 20)
    except ValueError:
        threshold = 20

    products = SalesAnalyzer.low_stock(threshold)

    if not products:
        print(f"\n Nenhum produto com estoque abaixo de {threshold}.")
        press_enter()
        return

    print()
    for product in products:
        print(
            f" {product['name']:<15} | "
            f"Estoque: {product['stock']:>4} | "
            f"Categoria: {product['category']}"
        )

    press_enter()


# ─────────────────────────────────────────────────────
# MENU PRINCIPAL
# ─────────────────────────────────────────────────────

def main():
    """Ponto de entrada do sistema."""
    while True:
        clear_screen()
        print_header("LOJA SIMPLES — SISTEMA DE GESTÃO")
        print("  [1] Produtos")
        print("  [2] Clientes")
        print("  [3] Relatórios")
        print("  [0] Sair")
        print_separator()

        option = input("  Escolha: ").strip()

        if option == "1":
            menu_products()
        elif option == "2":
            menu_customers()
        elif option == "3":
            menu_reports()
        elif option == "0":
            print("\n  Até logo! \n")
            sys.exit(0)
        else:
            print("\n  Opção inválida!")
            press_enter()


# ─────────────────────────────────────────────────────
# PONTO DE ENTRADA
# ─────────────────────────────────────────────────────

if __name__ == "__main__":
    main()
    