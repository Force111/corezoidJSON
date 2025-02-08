import random
import string
import json

def rand_string(): 
    return ''.join(random.choices(string.ascii_letters, k=8))
def rand_integer(min=0, max=1000):
    return random.randint(min, max)
def rand_boolean(): 
    return random.choice([True, False])
def rand_enum(choices): 
    return random.choice(choices)
def fill_randomdata(schema, definitions=None):
    if definitions is None:
        definitions = schema.get("definitions", {})
    if "$ref" in schema:
        ref_key = schema["$ref"].lstrip("#")
        return fill_randomdata(definitions.get(ref_key, {}), definitions)
    if "anyOf" in schema:
        return fill_randomdata(random.choice(schema["anyOf"]), definitions)
    schema_type = schema.get("type")
    if schema_type == "string":
        return rand_string()
    if schema_type == "integer":
        return rand_integer(schema.get("minimum", 0), schema.get("maximum", 1000))
    if schema_type == "boolean":
        return rand_boolean()
    if schema_type == "null":
        return None
    if schema_type == "array":
        item_schema = schema.get("items", {})
        return [fill_randomdata(item_schema, definitions) for _ in range(random.randint(1, 5))]
    if schema_type == "object":
        obj = {}
        properties = schema.get("properties", {})
        required_fields = schema.get("required", properties.keys())
        for field in required_fields:
            if field in properties:
                field_schema = properties[field]
                if "enum" in field_schema:
                    obj[field] = rand_enum(field_schema["enum"])
                else:
                    obj[field] = fill_randomdata(field_schema, definitions)
        return obj
    return None
schema = {
    "definitions": {
        "attendees": {
            "type": "object",
            "$id": "#attendees",
            "properties": {
                "userId": {"type": "integer"},
                "access": {"enum": ["view", "modify","execute"]},
                "formAccess": {"enum": ["view", "execute", "execute_view"]}
            },
            "required": ["userId", "access"]
        }
    },
    "type": "object",
    "properties": {
        "id": {"anyOf": [{"type": "integer"}]},
        "title": {"type": "string"},
        "description": {"type": "string"},
        "startDate": {"type": "integer"},
        "endDate": {"type": "integer"},
        "attendees": {
            "type": "array",
            "items": {"$ref": "#attendees"}
        }
    },
    "required": ["id", "title", "description", "startDate", "endDate", "attendees"]
}

example_json = fill_randomdata(schema)
print(json.dumps(example_json, indent = 2))
