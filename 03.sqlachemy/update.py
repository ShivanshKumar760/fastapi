from database import SessionLocal, Blog

db = SessionLocal()  # Create a new database session
# Update a blog post with id 1
blog_to_update = db.query(Blog).filter(Blog.id == 1).first()  # Query the blog post with the specified id
if blog_to_update:
    blog_to_update.title = "Updated Blog Title"  # Update the title
    blog_to_update.content = "This is the updated content of the blog post."  # Update the content
    db.commit()  # Commit the transaction to save the changes to the database
    print("Blog post updated successfully.")