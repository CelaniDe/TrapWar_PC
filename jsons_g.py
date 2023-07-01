class Product(object):
    def __init__(self,id) -> None:
        self.id = id

    def get_id(self):
        return self.id

    def set_name(self,name):
        self.name = name

    def get_name(self):
        return self.name

    def set_price(self,price):
        self.price = price

    def get_price(self):
        return self.price

    def set_amount(self,amount):
        self.amount = amount

    def get_amount(self):
        return self.amount
    
    def attribute_setter(self,json_desc : dict):
        for attribute , value in json_desc.items():
            if attribute == "name":
                self.name = value
            elif attribute == "price":
                self.price = value
            elif attribute == "amount":
                self.amount = value

    def __str__(self) -> str:
        return f"(name : {self.name}) | (price : {self.price}) | (amount : {self.amount})"
    
    def __repr__(self):
       return self.__str__()
    



json1 = {
    "id" : 0,
    "name" : "Product 0",
    "price" : 10
}

json2 = {
    "id" : 1,
    "name" : "Product 1",
}

json3 = {
    "id" : 0,
    "amount" : 100
}

json4 = {
    "id" : 1,
    "price" : 50,
    "amount" : 0
}

lista_of_products_json = [json1,json2,json3,json4]
products : list = list()
for current_json in lista_of_products_json: #current_json fetched from API
    current_product = [x for x in products if x.id == current_json["id"]][0] if [x for x in products if x.get_id() == current_json["id"]] else []
    if current_product:
        current_product.attribute_setter(current_json)
    else:
        new_product = Product(current_json["id"])
        new_product.attribute_setter(current_json)
        products.append(new_product)

print(
    products
)