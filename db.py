from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import datetime

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import DateTime, Float

from settings import Settings


class Base(DeclarativeBase):
    pass


class Db:
    engine: AsyncEngine
    sessionmaker: async_sessionmaker[AsyncSession]

    def __init__(self) -> None:
        self.engine = create_async_engine(Settings().POSTGRES_URL)
        self.sessionmaker = async_sessionmaker(bind=self.engine)

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        async with self.sessionmaker() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise


class Customer(Base):
    __tablename__ = "customers"
    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))
    phone: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    
class Order(Base):
    __tablename__ = "orders"
    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    customer_id: Mapped[str] = mapped_column(String(50), ForeignKey("customers.id"))
    date: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[str] = mapped_column(String(50))
    total: Mapped[float] = mapped_column(Float)
    items: Mapped[list[str]] = mapped_column(JSONB)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    
class Product(Base):
    __tablename__ = "products"
    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    price: Mapped[float] = mapped_column(Float)
    stock: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    
CUSTOMERS_TABLE = {
    "CUST123": {
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "phone": "555-1234",
    },
    "CUST456": {
        "name": "Bob Smith",
        "email": "bob@example.com",
        "phone": "555-5678",
    },
}

ORDERS_TABLE = {
    "ORD1001": {
        "customer_id": "CUST123",
        "date": "2024-04-01",
        "status": "Shipped",
        "total": 89.99,
        "items": ["SKU100", "SKU200"],
    },
    "ORD1015": {
        "customer_id": "CUST123",
        "date": "2024-05-17",
        "status": "Processing",
        "total": 45.50,
        "items": ["SKU300"],
    },
    "ORD1022": {
        "customer_id": "CUST456",
        "date": "2024-06-04",
        "status": "Delivered",
        "total": 120.00,
        "items": ["SKU100", "SKU100"],
    },
}

PRODUCTS_TABLE = {
    "SKU100": {"name": "Wireless Mouse", "price": 29.99, "stock": 42},
    "SKU200": {"name": "Keyboard", "price": 59.99, "stock": 18},
    "SKU300": {"name": "USB-C Cable", "price": 15.50, "stock": 77},
}

async def seed_database(db: Db):
    async with db.get_session() as session:
        for customer_id, customer_data in CUSTOMERS_TABLE.items():
            customer = Customer(
                id=customer_id,
                name=customer_data["name"],
                email=customer_data["email"],
                phone=customer_data["phone"],
            )
            session.add(customer)
        await session.commit()
        for order_id, order_data in ORDERS_TABLE.items():
            order = Order(
                id=order_id,
                customer_id=order_data["customer_id"],
                date=datetime.fromisoformat(order_data["date"]),
                status=order_data["status"],
                total=order_data["total"],
                items=order_data["items"],
            )
            session.add(order)
        await session.commit()
        for product_id, product_data in PRODUCTS_TABLE.items():
            product = Product(
                id=product_id,
                name=product_data["name"],
                price=product_data["price"],
                stock=product_data["stock"],
            )
            session.add(product)
        await session.commit()

