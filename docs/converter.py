import json

file_path = input("Enter the JSON file path: ")

def get_schema_by_ref(root, ref):
    parts = ref.split('/')
    schema = root
    for part in parts:
        if part and not part == "#":  # skip empty strings resulting from leading '/'
            schema = schema[part]

    return schema

with open(file_path) as file:
    data = json.load(file)

with open("output.txt", "w") as file:
    endpoints = data["paths"]

    for path, content in endpoints.items():
        for method, details in content.items():
            if "summary" in details:
                file.write(f"({method}) {details['summary']}\n")
                file.write(f"'{path}'\n")
            else:
                file.write(f"({method}) '{path}'\n")

            if "description" in details:
                file.write(f"Description: {details['description']}\n")

            file.write(f"Responses:\n")

            for status, response in details['responses'].items():
                file.write(f"{status}: {response['description']}\n")

                if "content" in response:
                    file.write("Response models:\n")

                    for content_type, schema in response['content'].items():

                        if "$ref" in schema['schema']:
                            file.write(f"({content_type})\n{json.dumps(get_schema_by_ref(data, schema['schema']['$ref']), indent=4)}\n")
                        else:
                            file.write(f"({content_type})\n{json.dumps(schema['schema'], indent=4)}\n")


            file.write("\n\n")