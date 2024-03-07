import json

file_path = input("Enter the JSON file path: ")

with open(file_path) as file:
    data = json.load(file)

with open("output2.txt", "w") as file:
    schemas = data['components']['schemas']

    for schema_name, schema in schemas.items():
        file.write(f"Schema: {schema_name}\n")
        file.write(f"{json.dumps(schema, indent=4)}\n\n")