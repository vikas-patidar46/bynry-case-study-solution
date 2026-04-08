from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime
from app import db


class Company(db.Model):
    __tablename__ = "company"
    id = Column(Integer, primary_key=True)
    name = Column(String)


class Warehouse(db.Model):
    __tablename__ = "warehouse"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    company_id = Column(Integer, ForeignKey("company.id"))


class Product(db.Model):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    sku = Column(String)
    category_id = Column(Integer, ForeignKey("category.id"))
    supplier_id = Column(Integer, ForeignKey("supplier.id"))


class Supplier(db.Model):
    __tablename__ = "supplier"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)


class Inventory(db.Model):
    __tablename__ = "inventory"
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    warehouse_id = Column(Integer, ForeignKey("warehouse.id"))
    current_stock = Column(Integer)
    threshold = Column(Integer)


class Orders(db.Model):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    order_date = Column(DateTime)


class OrderItems(db.Model):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("product.id"))
    quantity = Column(Integer)
    price = Column(DECIMAL)
    