from sqlalchemy import select
from mcp.server.fastmcp import FastMCP

from db import Customer, Db, Order, Product

mcp = FastMCP()

db = Db()


@mcp.tool()
async def get_customer_info(customer_id: str) -> str:
    """Search for a customer using their unique identifier"""

    async with db.get_session() as session:
        customer = await session.get(Customer, customer_id)

        if customer is None:
            return "Customer not found"

        return str(customer)


@mcp.tool()
async def get_order_details(order_id: str) -> str:
    """Get the details of an order using its unique identifier"""

    async with db.get_session() as session:
        order: Order | None = await session.get(Order, order_id)
        
        if not order:
            return "Order not found"

        items = (
            (await session.execute(select(Product).where(Product.id.in_(order.items))))
            .scalars()
            .all()
        )

        return (
            f"Order ID: {order_id}\n"
            f"Customer ID: {order.customer_id}\n"
            f"Date: {order.date}\n"
            f"Status: {order.status}\n"
            f"Total: ${order.total:.2f}\n"
            f"Items: {', '.join(product.name for product in items)}"
        )


@mcp.tool()
async def check_inventory(product_name: str) -> str:
    """Search inventory for a product by product name."""

    async with db.get_session() as session:
        products = (
            await session.execute(
                select(Product).where(Product.name.ilike(f"%{product_name}%"))
            )
        ).scalars().all()

        if not products:
            return "No matching products found"

        return (
            f"Products found: {', '.join(product.name for product in products)}\n"
            f"Stock: {', '.join(str(product.stock) for product in products)}"
        )


@mcp.tool()
async def get_customer_ids_by_name(name: str) -> str:
    """Get the customer IDs by name."""

    async with db.get_session() as session:
        customers = (
           await session.execute(select(Customer.id).where(Customer.name.ilike(f"%{name}%")))
        )
        

        if not customers:
            return "No matching customers found"

        return f"Customer IDs: {', '.join([str(customer) for customer in customers.scalars().all()])}\n"

@mcp.tool()
async def get_order_ids_by_customer_id(customer_id: str) -> str:
    """Get the order IDs by customer ID."""
    async with db.get_session() as session:
        orders = await session.execute(select(Order.id).where(Order.customer_id == customer_id))
        
        if not orders:
            return "No matching orders found"

        return f"Order IDs: {', '.join([str(order) for order in orders.scalars().all()])}\n"