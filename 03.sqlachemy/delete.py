from database import SessionLocal, Blog
db = SessionLocal()  # Create a new database session
# Delete a blog post with id 1
blog_to_delete = db.query(Blog).filter(Blog.id == 1).first()  # Query the blog post with the specified id

if blog_to_delete:
    db.delete(blog_to_delete)  # Mark the blog post for deletion
    db.commit()  # Commit the transaction to delete the blog post from the database
    print("Blog post deleted successfully.")
else:
    print("Blog post not found.")