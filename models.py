from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create an engine and connect to the database
engine = create_engine('sqlite:///restaurant_reviews.db', echo=True)
Base = declarative_base()

# Define the Review model
class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    customer_id = Column(Integer, ForeignKey('customer.id'))
    star_rating = Column(Integer)
    content = Column(String)

    # Define relationships
    restaurant = relationship("Restaurant", back_populates="reviews")
    customer = relationship("Customer", back_populates="reviews")

    def review_details(self):
        return f"Review for {self.restaurant.name} by {self.customer.full_name()}: {self.star_rating} stars."

# Define the Restaurant model
class Restaurant(Base):
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

    # One-to-many relationship with Review
    reviews = relationship("Review", back_populates="restaurant")

    # Many-to-many relationship with Customer
    customers = relationship("Customer", secondary="reviews", back_populates="restaurants")

    @classmethod
    def fanciest(cls):
        return session.query(cls).order_by(cls.price.desc()).first()

    def get_reviews(self):
        return [review.review_details() for review in self.reviews]

    def get_customers(self):
        return [customer.full_name() for customer in self.customers]

# Define the Customer model
class Customer(Base):
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    # One-to-many relationship with Review
    reviews = relationship("Review", back_populates="customer")

    # Many-to-many relationship with Restaurant
    restaurants = relationship("Restaurant", secondary="reviews", back_populates="customers")

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def favorite_restaurant(self):
        highest_rating = 0
        favorite_restaurant = None
        for review in self.reviews:
            if review.star_rating > highest_rating:
                highest_rating = review.star_rating
                favorite_restaurant = review.restaurant
        return favorite_restaurant

    def add_review(self, restaurant, rating, content):
        new_review = Review(restaurant=restaurant, customer=self, star_rating=rating, content=content)
        self.reviews.append(new_review)

    def delete_reviews(self, restaurant):
        for review in self.reviews:
            if review.restaurant == restaurant:
                self.reviews.remove(review)

    def get_reviews(self):
        return [review.review_details() for review in self.reviews]

# Create the tables in the database
Base.metadata.create_all(engine)

# Create a Session
Session = sessionmaker(bind=engine)
session = Session()

# Sample data creation for testing
restaurant1 = Restaurant(name="Restaurant A", price=3)
restaurant2 = Restaurant(name="Restaurant B", price=2)

customer1 = Customer(first_name="Levis", last_name="Ngigi")
customer2 = Customer(first_name="Alice", last_name="Wambui")

# Add instances to the session and commit changes to the database
session.add_all([restaurant1, restaurant2, customer1, customer2])
session.commit()

# Close the session
session.close()
