from src.database import execute_query

results = execute_query("SELECT * FROM products")

for product in results:
    print(product)