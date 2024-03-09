import json

file_path = input("Enter the JSON file path: ")

with open(file_path) as file:
    data = json.load(file)

with open("output2.txt", "w") as file:
    schemas = data['components']['schemas']

    for schema_name, schema in schemas.items():
        file.write(f"\n{schema_name}\n")
        for prop_name, prop in schema['properties'].items():
            file.write(f"{prop_name}: {prop['type']}\n")