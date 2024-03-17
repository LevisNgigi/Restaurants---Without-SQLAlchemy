from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Restaurant, Customer, Review, Base

# Create an engine and connect to the database
engine = create_engine('sqlite:///restaurant_reviews.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Sample data creation for testing
restaurant1 = Restaurant(name="Restaurant A", price=3)
restaurant2 = Restaurant(name="Restaurant B", price=2)

customer1 = Customer(first_name="Levis", last_name="Ngigi")
customer2 = Customer(first_name="Alice", last_name="Wambui")

review1 = Review(restaurant=restaurant1, customer=customer1, star_rating=4, content="Great food!")
review2 = Review(restaurant=restaurant2, customer=customer2, star_rating=5, content="Excellent service!")

# Add instances to the session and commit changes to the database
session.add_all([restaurant1, restaurant2, customer1, customer2, review1, review2])
session.commit()

# Example usage of the methods
# You can call the methods defined in the models and print the results to verify functionality

# Close the session
session.close()
