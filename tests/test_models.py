import sys
sys.path.insert(0, "src")

from models import Category, Product, Customer, Order

print("=" * 50)
print("CATEGORIAS")
print("=" * 50)
for cat in Category.get_all():
    print(cat)

print("\n" + "=" * 50)
print("PRODUTOS")
print("=" * 50)
for prod in Product.get_all():
    print(prod)

print("\n" + "=" * 50)
print("PRODUTOS DA CATEGORIA 1")
print("=" * 50)
for prod in Product.get_by_category(1):
    print(prod)

print("\n" + "=" * 50)
print("PEDIDOS DA ANA (cliente 1)")
print("=" * 50)
orders = Order.get_by_customer(1)
for order in orders:
    print(order)
    for item in order.items:
        print(item)


print("\n" + "=" * 50)
print("Customers")
print("=" * 50)
customers = Customer.get_all()
for customer in customers:
    print(customer)