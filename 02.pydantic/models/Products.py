from typing import List, Optional
from dto.RequestDTO import RequestDTO
products: List[RequestDTO] = [
    # Pydantic has a built in mapper like in jave we have toEntity and toDTO methods
    # Exactly. While Spring uses Jackson to convert JSON to a POJO and then often requires MapStruct to map that POJO to a Domain Entity, Pydantic does it all in one shot using Reflection and Type Hints.

    RequestDTO(id=1, name="Product 1", description="Description of Product 1", price=10.99, quantity=100),
    RequestDTO(id=2, name="Product 2", description="Description of Product 2", price=19.99, quantity=50),

]