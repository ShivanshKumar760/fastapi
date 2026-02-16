from database import SessionLocal, Blog

db = SessionLocal()  # Create a new database session
blogs = db.query(Blog).all()  # Query all blog posts from the database
print(blogs)

# read by id

give_id=int(input("Enter the id of the blog post you want to read: "))
blog = db.query(Blog).filter(Blog.id == give_id).first()  # Query the blog post with the specified id
print(blog)

# read with multiple filtering 

blog_specific = db.query(Blog).filter(
    Blog.title == "My second Blog",
    Blog.id > 1
).all()

print(blog_specific)