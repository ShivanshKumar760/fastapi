from database import SessionLocal, Blog 

# db = SessionLocal()  # Create a new database session
# new_blog = Blog(title="My First Blog", content="This is the content of my first blog post.")
# db.add(new_blog)  # Add the new blog post to the session
# db.commit()  # Commit the transaction to save the changes to the database
# db.refresh(new_blog)  # Refresh the instance to get the updated data from the database
# print("New blog post inserted successfully.")
# db.close()  # Close the database connection


# db = SessionLocal()  # Create a new database session
# new_blog = Blog(title="My second Blog", content="This is the content of my second post.")
# db.add(new_blog)  # Add the new blog post to the session
# db.commit()  # Commit the transaction to save the changes to the database
# db.refresh(new_blog)  # Refresh the instance to get the updated data from the database
# print("New blog post inserted successfully.")
# db.close()  # Close the database connection

db = SessionLocal()  # Create a new database session
new_blog = Blog(title="My third Blog", content="This is the content of my third post.")
db.add(new_blog)  # Add the new blog post to the session
db.commit()  # Commit the transaction to save the changes to the database
db.refresh(new_blog)  # Refresh the instance to get the updated data from the database
print("New blog post inserted successfully.")
db.close()  # Close the database connection