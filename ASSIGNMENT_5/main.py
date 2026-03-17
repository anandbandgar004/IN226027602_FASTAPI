from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import math

app = FastAPI()


# Sample Products


products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics"},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery"},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics"},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery"}
]

orders = []
order_counter = 1



# ORDER MODEL


class Order(BaseModel):
    customer_name: str
    product_id: int
    quantity: int



# CREATE ORDER (for testing Q4 & Bonus)


@app.post("/orders")
def create_order(order: Order):

    global order_counter

    product = next((p for p in products if p["id"] == order.product_id), None)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    new_order = {
        "order_id": order_counter,
        "customer_name": order.customer_name,
        "product": product["name"],
        "quantity": order.quantity
    }

    orders.append(new_order)
    order_counter += 1

    return new_order



# Q1 — SEARCH PRODUCTS


@app.get("/products/search")
def search_products(keyword: str):

    results = [
        p for p in products
        if keyword.lower() in p["name"].lower()
    ]

    if not results:
        return {"message": f"No products found for: {keyword}"}

    return {
        "keyword": keyword,
        "total_found": len(results),
        "products": results
    }



# Q2 — SORT PRODUCTS


@app.get("/products/sort")
def sort_products(sort_by: str = "price", order: str = "asc"):

    if sort_by not in ["price", "name"]:
        raise HTTPException(status_code=400,
                            detail="sort_by must be 'price' or 'name'")

    reverse = True if order == "desc" else False

    sorted_products = sorted(products, key=lambda x: x[sort_by], reverse=reverse)

    return {
        "sort_by": sort_by,
        "order": order,
        "products": sorted_products
    }



# Q3 — PAGINATION


@app.get("/products/page")
def paginate_products(page: int = 1, limit: int = 2):

    total = len(products)
    total_pages = math.ceil(total / limit)

    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "products": products[start:end]
    }



# Q4 — SEARCH ORDERS


@app.get("/orders/search")
def search_orders(customer_name: str):

    results = [
        o for o in orders
        if customer_name.lower() in o["customer_name"].lower()
    ]

    if not results:
        return {"message": f"No orders found for: {customer_name}"}

    return {
        "customer_name": customer_name,
        "total_found": len(results),
        "orders": results
    }



# Q5 — SORT BY CATEGORY THEN PRICE


@app.get("/products/sort-by-category")
def sort_by_category():

    sorted_products = sorted(products, key=lambda x: (x["category"], x["price"]))

    return {
        "products": sorted_products
    }



# Q6 — SEARCH + SORT + PAGINATION


@app.get("/products/browse")
def browse_products(
        keyword: str = None,
        sort_by: str = "price",
        order: str = "asc",
        page: int = 1,
        limit: int = 4):

    result = products

    # Search
    if keyword:
        result = [
            p for p in result
            if keyword.lower() in p["name"].lower()
        ]

    # Sort
    reverse = True if order == "desc" else False
    result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)

    # Pagination
    total_found = len(result)
    total_pages = math.ceil(total_found / limit)

    start = (page - 1) * limit
    end = start + limit

    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit,
        "total_found": total_found,
        "total_pages": total_pages,
        "products": result[start:end]
    }



# ⭐ BONUS — PAGINATE ORDERS


@app.get("/orders/page")
def paginate_orders(page: int = 1, limit: int = 3):

    total = len(orders)
    total_pages = math.ceil(total / limit)

    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "orders": orders[start:end]
    }



# GET PRODUCT BY ID (must stay last)


@app.get("/products/{product_id}")
def get_product(product_id: int):

    for p in products:
        if p["id"] == product_id:
            return p

    raise HTTPException(status_code=404, detail="Product not found")