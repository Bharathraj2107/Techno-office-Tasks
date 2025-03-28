import person_pb2

# Create a Person object
person = person_pb2.Person()#The .Person() is a constructor for the Person class
person.name = "Alice"
person.age = 30
person.email = "alice@example.com"

# Serialize the Person object to binary
binary_data = person.SerializeToString()
print("Serialized binary data:", binary_data)

# Deserialize the binary data back into a Person object
new_person = person_pb2.Person()
new_person.ParseFromString(binary_data)

# Print the deserialized data
print("Deserialized Person:")
print("Name:", new_person.name)
print("Age:", new_person.age)
print("Email:", new_person.email)

# Save binary data to a file
with open("person_data.bin", "wb") as f:
    f.write(binary_data)

# Load binary data from a file
with open("person_data.bin", "rb") as f:
    loaded_data = f.read()

# Deserialize the loaded data
loaded_person = person_pb2.Person()
loaded_person.ParseFromString(loaded_data)

print("\nLoaded Person from file:")
print("Name:", loaded_person.name)
print("Age:", loaded_person.age)
print("Email:", loaded_person.email)