from pydantic import BaseModel

# what does pydantic do?
# 1. Data validation: Pydantic validates the data types and constraints defined in the model. If the input data does not conform to the specified types or constraints, Pydantic raises a validation error.
# 2. Data parsing: Pydantic can parse data from various formats (e.g., JSON, dict) and convert it into Python objects based on the defined model.
# 3. Data serialization: Pydantic can serialize Python objects back into formats like JSON, making it easy to send data over the network or store it in a database.
#how can it serialize data?
## Pydantic models can be serialized to JSON using the .json() method, which converts the model instance into a JSON string. Additionally, you can use the .dict() method to convert the model instance into a Python dictionary, which can then be easily serialized to JSON using the json module from the standard library.
# Example:
# from pydantic import BaseModel
# class User(BaseModel):
#     name: str
# user = User(name="Alice")
# Serialize to JSON string

class RequestDTO(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int