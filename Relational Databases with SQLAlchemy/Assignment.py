from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, func
from sqlalchemy.orm import DeclarativeBase, sessionmaker, relationship

print("=== SQLAlchemy Relational Database Assignment ===")
print("\n=== Part 1: Setup ===")
print("Importing SQLAlchemy modules...")
print("Creating database engine for 'sqlite:///shop.db'...")

# Part 1: Setup
engine = create_engine('sqlite:///shop.db')

class Base(DeclarativeBase):
    pass

Session = sessionmaker(bind=engine)
session = Session()
print("Database session created successfully!")

print("\n=== Part 2: Define Tables ===")
print("Defining User, Product, and Order tables with relationships...")

# Part 2: Define Tables
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    orders = relationship('Order', back_populates='user', cascade='all, delete-orphan')

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    orders = relationship('Order', back_populates='product')

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    status = Column(Boolean, default=False) # Bonus: shipped or not
    user = relationship('User', back_populates='orders')
    product = relationship('Product', back_populates='orders')

print("Tables defined successfully!")
print("- User table: id, name, email (unique)")
print("- Product table: id, name, price")
print("- Order table: id, user_id (FK), product_id (FK), quantity, status")
print("- Relationships: User ↔ Orders (one-to-many), Product ↔ Orders (one-to-many)")

print("\n=== Part 3: Create Tables ===")
print("Creating tables in the database...")

# Part 3: Create Tables
Base.metadata.create_all(engine)

print("Database tables created successfully!")

# Part 4: Insert Data and Queries
def main():
    print("\n=== Part 4: Insert Data ===")
    # Create the session
    with Session() as session:
        
        # Clear existing data to avoid unique constraint violations
        session.query(Order).delete()
        session.query(User).delete()
        session.query(Product).delete()
        session.commit()
        
        # Add users (at least 2 users)
        print("Adding users...")
        user1 = User(name="Bryce Lawrence", email="bryce@example.com")
        user2 = User(name="Greg Sayer", email="greg@example.com")
        
        # Add products (at least 3 products)
        print("Adding products...")
        product1 = Product(name="Laptop", price=1200)
        product2 = Product(name="Phone", price=800)
        product3 = Product(name="Headphones", price=180)
        
        # Add orders (at least 4 orders)
        print("Adding orders...")
        order1 = Order(user=user1, product=product1, quantity=1, status=False)  # Not shipped
        order2 = Order(user=user1, product=product2, quantity=2, status=True)   # Shipped
        order3 = Order(user=user2, product=product3, quantity=1, status=False)  # Not shipped
        order4 = Order(user=user2, product=product1, quantity=1, status=True)   # Shipped
        
        # Save all data
        session.add_all([user1, user2, product1, product2, product3, order1, order2, order3, order4])
        session.commit()
        print("Data inserted successfully!\n")
        
        # Part 5: Queries
        print("=== Part 5: Query Operations ===")
        
        # 1. Retrieve all users and print their information
        print("\n1. All Users:")
        print("-" * 40)
        users = session.query(User).all()
        for user in users:
            print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")
        
        # 2. Retrieve all products and print their name and price
        print("\n2. All Products:")
        print("-" * 40)
        products = session.query(Product).all()
        for product in products:
            print(f"ID: {product.id}, Name: {product.name}, Price: ${product.price}")
        
        # 3. Retrieve all orders, showing the user's name, product name, and quantity
        print("\n3. All Orders:")
        print("-" * 50)
        orders = session.query(Order).all()
        for order in orders:
            status_text = "Shipped" if order.status else "Not Shipped"
            print(f"Order ID: {order.id}, User: {order.user.name}, Product: {order.product.name}, Quantity: {order.quantity}, Status: {status_text}")
        
        # 4. Update a product's price
        print("\n4. Updating Product Price:")
        print("-" * 40)
        product_to_update = session.query(Product).filter_by(name="Phone").first()
        if product_to_update:
            old_price = product_to_update.price
            product_to_update.price = 550
            session.commit()
            print(f"Updated {product_to_update.name} price from ${old_price} to ${product_to_update.price}")
        
        # Show updated products
        print("\nUpdated Products:")
        products = session.query(Product).all()
        for product in products:
            print(f"ID: {product.id}, Name: {product.name}, Price: ${product.price}")
        
        # 5. Delete a user by ID
        print("\n5. Deleting User:")
        print("-" * 40)
        user_to_delete = session.query(User).filter_by(name="Bryce Lawrence").first()
        if user_to_delete:
            user_id = user_to_delete.id
            user_name = user_to_delete.name
            print(f"Deleting user: ID {user_id}, Name: {user_name}")
            session.delete(user_to_delete)
            session.commit()
            print("User deleted successfully!")
        
        print("\nRemaining Users:")
        remaining_users = session.query(User).all()
        for user in remaining_users:
            print(f"ID: {user.id}, Name: {user.name}, Email: {user.email}")
        
        print("\nRemaining Orders (after cascade delete):")
        remaining_orders = session.query(Order).all()
        for order in remaining_orders:
            status_text = "Shipped" if order.status else "Not Shipped"
            print(f"Order ID: {order.id}, User: {order.user.name}, Product: {order.product.name}, Quantity: {order.quantity}, Status: {status_text}")
        
        # Part 6: Bonus Features
        print("\n=== Part 6: Bonus Features ===")
        
        # Query all orders that are not shipped
        print("\n1. Orders Not Shipped:")
        print("-" * 40)
        not_shipped_orders = session.query(Order).filter_by(status=False).all()
        if not_shipped_orders:
            for order in not_shipped_orders:
                print(f"Order ID: {order.id}, User: {order.user.name}, Product: {order.product.name}, Quantity: {order.quantity}")
        else:
            print("No unshipped orders found.")
        
        # Count the total number of orders per user
        print("\n2. Total Orders Per User:")
        print("-" * 40)
        order_counts = session.query(
            User.name,
            func.count(Order.id).label('order_count')
        ).join(Order).group_by(User.id, User.name).all()
        
        for user_name, count in order_counts:
            print(f"User: {user_name}, Total Orders: {count}")
        
        print("\n=== Assignment Complete! ===")


if __name__ == "__main__":
    # Run the main program
    main()