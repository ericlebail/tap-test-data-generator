from datetime import datetime

from allpairspy import AllPairs
from faker import Faker

from tap_test_data_generator import data_generator, load_repositories, discover, load_schema_json, load_definitions


def test_extract_value_lists():
    # given
    config = {
        "schema_dir": "tap_test_data_generator/schemas",
        "metadata_dir": "tap_test_data_generator/metadatas",
        "object_repository_dir": "tap_test_data_generator/object-repositories",
        "static_input_dir": "",
        "record_number": 100,
        "apply_record_number_on_pairwise": True,
        "data_locale_list": ["en_US", "fr_FR"]
    }
    object_repositories = load_repositories(config)
    catalog = discover(config)
    stream = catalog.get_stream("sample")
    schema_json = load_schema_json(config, stream)
    definitions = load_definitions(schema_json, config)
    # when
    value_lists = data_generator.extract_value_lists(None, schema_json, object_repositories, definitions)
    # then
    assert value_lists is not None
    assert "checked" in value_lists
    assert [True, False] == value_lists["checked"]
    assert "dimensions" in value_lists
    assert [{'width': 5, 'height': 10}, {'width': 10, 'height': 20}, {'width': 20, 'height': 40}, None] == value_lists[
        "dimensions"]
    assert "color" in value_lists
    assert ['green', 'yellow', 'red'] == value_lists["color"]


def test_generate_dictionary():
    # given
    config = {
        "schema_dir": "tap_test_data_generator/schemas",
        "metadata_dir": "tap_test_data_generator/metadatas",
        "object_repository_dir": "tap_test_data_generator/object-repositories",
        "static_input_dir": "",
        "record_number": 100,
        "apply_record_number_on_pairwise": True,
        "data_locale_list": ["en_US", "fr_FR"]
    }
    object_repositories = load_repositories(config)
    catalog = discover(config)
    stream = catalog.get_stream("sample")
    schema_json = load_schema_json(config, stream)
    definitions = load_definitions(schema_json, config)
    value_lists = data_generator.extract_value_lists(None, schema_json, object_repositories, definitions)
    pairwise_values = AllPairs(value_lists)
    pairs = pairwise_values.next()
    faker_factory = Faker()
    # when
    generated_dict = data_generator.generate_dictionary(None, schema_json, {}, faker_factory, object_repositories,
                                                        pairs, definitions, 5)
    # then
    assert generated_dict is not None
    assert "checked" in generated_dict
    assert "dimensions" in generated_dict
    assert "id" in generated_dict
    assert "color" in generated_dict
    assert "price" in generated_dict
    assert "tags" in generated_dict
    assert "hour" in generated_dict


def test_generate_dictionary_no_pairs():
    # given
    config = {
        "schema_dir": "tap_test_data_generator/schemas",
        "metadata_dir": "tap_test_data_generator/metadatas",
        "object_repository_dir": "tap_test_data_generator/object-repositories",
        "static_input_dir": "",
        "record_number": 100,
        "apply_record_number_on_pairwise": True,
        "data_locale_list": ["en_US", "fr_FR"]
    }
    object_repositories = load_repositories(config)
    catalog = discover(config)
    stream = catalog.get_stream("sample")
    schema_json = load_schema_json(config, stream)
    definitions = load_definitions(schema_json, config)
    faker_factory = Faker()
    # when
    generated_dict = data_generator.generate_dictionary(None, schema_json, {}, faker_factory, object_repositories,
                                                        None, definitions, 5)
    # then
    assert generated_dict is not None
    assert "checked" in generated_dict
    assert "dimensions" in generated_dict
    assert "id" in generated_dict
    assert "color" in generated_dict
    assert "price" in generated_dict
    assert "tags" in generated_dict
    assert "hour" in generated_dict


def test_extract_value_lists_from_string_enum():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "string",
        "enum": ["green", "yellow", "red"]
    }
    # when
    value_lists = data_generator.extract_value_lists_from_string(property_name, schema_json)
    # then
    assert value_lists is not None
    assert "test_property" in value_lists
    assert ['green', 'yellow', 'red'] == value_lists["test_property"]


def test_extract_value_lists_from_string_enum_withNull():
    # given
    property_name = "test_property"
    schema_json = {
        "type": ['string', 'null'],
        "enum": ["green", "yellow", "red"]
    }
    # when
    value_lists = data_generator.extract_value_lists_from_string(property_name, schema_json)
    # then
    assert value_lists is not None
    assert "test_property" in value_lists
    assert ['green', 'yellow', 'red', None] == value_lists["test_property"]



def test_extract_value_lists_from_string_pattern():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "string",
        "pattern": "(A|P)M"
    }
    # when
    value_lists = data_generator.extract_value_lists_from_string(property_name, schema_json)
    # then
    assert value_lists is not None
    assert "test_property" in value_lists
    assert ['AM', 'PM'] == value_lists["test_property"]


def test_extract_value_lists_from_string_pattern_withNull():
    # given
    property_name = "test_property"
    schema_json = {
        "type": ['string', 'null'],
        "pattern": "(A|P)M"
    }
    # when
    value_lists = data_generator.extract_value_lists_from_string(property_name, schema_json)
    # then
    assert value_lists is not None
    assert "test_property" in value_lists
    assert ['AM', 'PM', None] == value_lists["test_property"]


def test_extract_value_lists_from_object_repository():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "object",
        "$generator": "#/object-repository/dim-sample",
        "$pairwise": True
    }
    config = {
        "object_repository_dir": "tap_test_data_generator/object-repositories"
    }
    object_repositories = load_repositories(config)
    # when
    value_lists = data_generator.extract_value_lists_from_object(property_name, schema_json, object_repositories, {})
    # then
    assert value_lists is not None
    assert "test_property" in value_lists
    assert [{'width': 5, 'height': 10}, {'width': 10, 'height': 20}, {'width': 20, 'height': 40}] == value_lists[
        "test_property"]


def test_extract_value_lists_from_object_repository_withNull():
    # given
    property_name = "test_property"
    schema_json = {
        "type": ['object', 'null'],
        "$generator": "#/object-repository/dim-sample",
        "$pairwise": True
    }
    config = {
        "object_repository_dir": "tap_test_data_generator/object-repositories"
    }
    object_repositories = load_repositories(config)
    # when
    value_lists = data_generator.extract_value_lists_from_object(property_name, schema_json, object_repositories, {})
    # then
    assert value_lists is not None
    assert "test_property" in value_lists
    assert [{'width': 5, 'height': 10}, {'width': 10, 'height': 20}, {'width': 20, 'height': 40}, None] == value_lists[
        "test_property"]


def test_extract_value_lists_from_object_no_repository():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "object",
        "required": [
            "one",
            "two"
        ],
        "properties": {
            "one": {
                "type": "integer"
            },
            "two": {
                "type": "string",
                "enum": ["green", "yellow", "red"],
                "$pairwise": True
            }
        },
        "additionalProperties": True
    }
    # when
    value_lists = data_generator.extract_value_lists_from_object(property_name, schema_json, None, {})
    # then
    assert value_lists is not None
    assert "two" in value_lists
    assert ['green', 'yellow', 'red'] == value_lists["two"]


def test_extract_value_lists_from_object_no_repository_withNull():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "object",
        "required": [
            "one",
            "two"
        ],
        "properties": {
            "one": {
                "type": "integer"
            },
            "two": {
                "type": ['string', 'null'],
                "enum": ["green", "yellow", "red"],
                "$pairwise": True
            }
        },
        "additionalProperties": True
    }
    # when
    value_lists = data_generator.extract_value_lists_from_object(property_name, schema_json, None, {})
    # then
    assert value_lists is not None
    assert "two" in value_lists
    assert ['green', 'yellow', 'red', None] == value_lists["two"]


def test_extract_value_lists_from_object_no_repository_parentNull():
    # given
    property_name = "test_property"
    schema_json = {
        "type": ['object', 'null'],
        "required": [
            "one",
            "two"
        ],
        "properties": {
            "one": {
                "type": "integer"
            },
            "two": {
                "type": "string",
                "enum": ["green", "yellow", "red"],
                "$pairwise": True
            }
        },
        "additionalProperties": True
    }
    # when
    value_lists = data_generator.extract_value_lists_from_object(property_name, schema_json, None, {})
    # then
    assert value_lists is not None
    assert "two" in value_lists
    assert ['green', 'yellow', 'red'] == value_lists["two"]


def test_generate_array_string_default():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "array",
        "additionalItems": True,
        "items": {
            "type": "string"
        }
    }
    faker_factory = Faker()
    # when
    value_lists = data_generator.generate_array({}, property_name, schema_json, faker_factory, None, None, {}, 5)
    # then
    assert value_lists is not None
    assert "test_property" in value_lists
    assert value_lists["test_property"] is not None
    assert 1 <= len(value_lists["test_property"])
    assert 10 >= len(value_lists["test_property"])


def test_generate_array_string_item_number():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "array",
        "additionalItems": True,
        "items": {
            "type": "string"
        },
        "minItems": 3,
        "maxItems": 15
    }
    faker_factory = Faker()
    # when
    value_lists = data_generator.generate_array({}, property_name, schema_json, faker_factory, None, None, {}, 5)
    # then
    assert value_lists is not None
    assert "test_property" in value_lists
    assert value_lists["test_property"] is not None
    assert 3 <= len(value_lists["test_property"])
    assert 15 >= len(value_lists["test_property"])


def test_generate_object_repository():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "object",
        "$generator": "#/object-repository/dim-sample",
        "$pairwise": True
    }
    config = {
        "object_repository_dir": "tap_test_data_generator/object-repositories"
    }
    object_repositories = load_repositories(config)
    faker_factory = Faker()
    value_lists = data_generator.extract_value_lists("test_property", schema_json, object_repositories, {})
    # adding a second property into value_lists because at least 2 properties are required in order to AllPairs works
    value_lists["boolean"] = [True, False]
    pairwise_values = AllPairs(value_lists)
    pairs = pairwise_values.next()
    # when
    dictionary = data_generator.generate_object({}, property_name, schema_json, faker_factory, object_repositories,
                                                pairs, {}, 5)
    # then
    assert dictionary is not None
    assert "test_property" in dictionary
    assert "width" in dictionary["test_property"]
    assert "height" in dictionary["test_property"]


def test_generate_object_no_repository():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "object",
        "required": [
            "width",
            "height"
        ],
        "properties": {
            "width": {
                "type": "integer"
            },
            "height": {
                "type": "string",
                "enum": ["green", "yellow", "red"]
            }
        },
        "additionalProperties": True
    }
    faker_factory = Faker()
    # when
    dictionary = data_generator.generate_object({}, property_name, schema_json, faker_factory, None, None, {}, 5)
    # then
    assert dictionary is not None
    assert "test_property" in dictionary
    assert "width" in dictionary["test_property"]
    assert "height" in dictionary["test_property"]


def test_generate_object_type_empty():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "object",
        "required": [
        ],
        "properties": {
            "width": {
                "type": "integer"
            },
            "height": {
                "type": "string",
                "enum": ["green", "yellow", "red"]
            }
        },
        "additionalProperties": True,
        "$generator": "#/object-type/empty"
    }
    faker_factory = Faker()
    # when
    dictionary = data_generator.generate_object({}, property_name, schema_json, faker_factory, None, None, {}, 5)
    # then
    assert dictionary is not None
    assert "test_property" in dictionary
    assert dictionary["test_property"] is not None
    assert len(dictionary["test_property"].keys()) == 0


def test_generate_string_pair_enum():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "string",
        "enum": ["green", "yellow", "red"],
        "$pairwise": True
    }
    faker_factory = Faker()
    value_lists = data_generator.extract_value_lists_from_string(property_name, schema_json)
    # adding a second property into value_lists because at least 2 properties are required in order to AllPairs works
    value_lists["boolean"] = [True, False]
    pairwise_values = AllPairs(value_lists)
    pairs = pairwise_values.next()
    # when
    generated_string = data_generator.generate_string(property_name, schema_json, faker_factory, pairs, 0)
    # then
    assert generated_string is not None
    assert "" != generated_string
    assert getattr(pairs, property_name) == generated_string


def test_generate_string_nopair_enum():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "string",
        "enum": ["green", "yellow", "red"],
        "$pairwise": True
    }
    faker_factory = Faker()
    # when
    generated_string = data_generator.generate_string(property_name, schema_json, faker_factory, None, 0)
    # then
    assert generated_string is not None
    assert "" != generated_string
    assert "green" == generated_string or "yellow" == generated_string or "red" == generated_string


def test_generate_string_enum():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "string",
        "enum": ["green", "yellow", "red"]
    }
    faker_factory = Faker()
    # when
    generated_string = data_generator.generate_string(property_name, schema_json, faker_factory, None, 0)
    # then
    assert generated_string is not None
    assert "" != generated_string
    assert "green" == generated_string or "yellow" == generated_string or "red" == generated_string


def test_generate_string_pair_pattern():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "string",
        "pattern": "(A|P)M",
        "$pairwise": True
    }
    faker_factory = Faker()
    value_lists = data_generator.extract_value_lists_from_string(property_name, schema_json)
    # adding a second property into value_lists because at least 2 properties are required in order to AllPairs works
    value_lists["boolean"] = [True, False]
    pairwise_values = AllPairs(value_lists)
    pairs = pairwise_values.next()
    # when
    generated_string = data_generator.generate_string(property_name, schema_json, faker_factory, pairs, 0)
    # then
    assert generated_string is not None
    assert "" != generated_string
    assert getattr(pairs, property_name) == generated_string


def test_generate_string_nopair_pattern():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "string",
        "pattern": "(A|P)M",
        "$pairwise": True
    }
    faker_factory = Faker()
    # when
    generated_string = data_generator.generate_string(property_name, schema_json, faker_factory, None, 0)
    # then
    assert generated_string is not None
    assert "" != generated_string
    assert "AM" == generated_string or "PM" == generated_string


def test_generate_string_pattern():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "string",
        "pattern": "(A|P)M"
    }
    faker_factory = Faker()
    # when
    generated_string = data_generator.generate_string(property_name, schema_json, faker_factory, None, 0)
    # then
    assert generated_string is not None
    assert "" != generated_string
    assert "AM" == generated_string or "PM" == generated_string


def test_generate_string_const():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "string",
        "const": "my value"
    }
    faker_factory = Faker()
    # when
    generated_string = data_generator.generate_string(property_name, schema_json, faker_factory, None, 0)
    # then
    assert generated_string is not None
    assert "" != generated_string
    assert "my value" == generated_string


def test_generate_string_basic():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "string"
    }
    faker_factory = Faker()
    # when
    generated_string = data_generator.generate_string(property_name, schema_json, faker_factory, None, 0)
    # then
    assert generated_string is not None
    assert "" != generated_string
    

def test_generate_boolean_pair():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "boolean",
        "$pairwise": True
    }
    faker_factory = Faker()
    value_lists = data_generator.extract_value_lists(property_name, schema_json, None, {})
    # adding a second property into value_lists because at least 2 properties are required in order to AllPairs works
    value_lists["test2"] = ["A", "B"]
    pairwise_values = AllPairs(value_lists)
    pairs = pairwise_values.next()
    # when
    generated_boolean = data_generator.generate_boolean(property_name, schema_json, faker_factory, pairs, 0)
    # then
    assert generated_boolean is not None
    assert isinstance(generated_boolean, bool)
    assert getattr(pairs, property_name) == generated_boolean


def test_generate_boolean_const():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "boolean",
        "const": True
    }
    faker_factory = Faker()
    # when
    generated_boolean = data_generator.generate_boolean(property_name, schema_json, faker_factory, None, 0)
    # then
    assert generated_boolean is not None
    assert isinstance(generated_boolean, bool)


def test_generate_boolean_nopair():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "boolean",
        "$pairwise": True
    }
    faker_factory = Faker()
    # when
    generated_boolean = data_generator.generate_boolean(property_name, schema_json, faker_factory, None, 0)
    # then
    assert generated_boolean is not None
    assert isinstance(generated_boolean, bool)


def test_generate_boolean():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "boolean"
    }
    faker_factory = Faker()
    # when
    generated_boolean = data_generator.generate_boolean(property_name, schema_json, faker_factory, None, 0)
    # then
    assert generated_boolean is not None
    assert isinstance(generated_boolean, bool)


def test_generate_boolean_null0():
    # given
    property_name = "test_property"
    schema_json = {
        "type": ['boolean', 'null']
    }
    faker_factory = Faker()
    # when
    generated_boolean = data_generator.generate_boolean(property_name, schema_json, faker_factory, None, 0)
    # then
    assert generated_boolean is not None
    assert isinstance(generated_boolean, bool)


def test_generate_boolean_null100():
    # given
    property_name = "test_property"
    schema_json = {
        "type": ['boolean', 'null']
    }
    faker_factory = Faker()
    # when
    generated_boolean = data_generator.generate_boolean(property_name, schema_json, faker_factory, None, 100)
    # then
    assert generated_boolean is None


def test_generate_integer():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "integer"
    }
    faker_factory = Faker()
    # when
    generated_integer = data_generator.generate_integer(schema_json, faker_factory, 0)
    # then
    assert generated_integer is not None
    assert isinstance(generated_integer, int)
    assert len(str(generated_integer)) <= 10


def test_generate_integer_withNull0():
    # given
    property_name = "test_property"
    schema_json = {
        "type": ['integer', 'null']
    }
    faker_factory = Faker()
    # when
    generated_integer = data_generator.generate_integer(schema_json, faker_factory, 0)
    # then
    assert generated_integer is not None
    assert isinstance(generated_integer, int)
    assert len(str(generated_integer)) <= 10


def test_generate_integer_withNull100():
    # given
    property_name = "test_property"
    schema_json = {
        "type": ['integer', 'null']
    }
    faker_factory = Faker()
    # when
    generated_integer = data_generator.generate_integer(schema_json, faker_factory, 100)
    # then
    assert generated_integer is None


def test_generate_integer_minimum_maximum():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "integer",
        "maximum": 1000,
        "minimum": 0
    }
    faker_factory = Faker()
    # when
    generated_integer = data_generator.generate_integer(schema_json, faker_factory, 0)
    # then
    assert generated_integer is not None
    assert isinstance(generated_integer, int)
    assert 1000 >= generated_integer
    assert 0 <= generated_integer


def test_generate_integer_const_value():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "integer",
        "const": 30
    }
    faker_factory = Faker()
    # when
    generated_integer = data_generator.generate_integer(schema_json, faker_factory, 0)
    # then
    assert generated_integer is not None
    assert isinstance(generated_integer, int)
    assert 30 == generated_integer


def test_generate_integer_const_null():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "number",
        "const": None
    }
    faker_factory = Faker()
    # when
    generated_integer = data_generator.generate_integer(schema_json, faker_factory, 0)
    # then
    assert generated_integer is None


def test_generate_integer_maxLength():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "integer",
        "maxLength": 15
    }
    faker_factory = Faker()
    # when
    generated_integer = data_generator.generate_integer(schema_json, faker_factory, 0)
    # then
    assert generated_integer is not None
    assert isinstance(generated_integer, int)
    assert len(str(generated_integer)) <= 15


def test_generate_number():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "number"
    }
    faker_factory = Faker()
    # when
    generated_number = data_generator.generate_number(schema_json, faker_factory, 0)
    # then
    assert generated_number is not None
    assert isinstance(generated_number, float)
    assert len(str(generated_number)) <= 11  # 1 character can be added for - sign


def test_generate_number_withNull0():
    # given
    property_name = "test_property"
    schema_json = {
        "type": ['number', 'null']
    }
    faker_factory = Faker()
    # when
    generated_number = data_generator.generate_number(schema_json, faker_factory, 0)
    # then
    assert generated_number is not None
    assert isinstance(generated_number, float)
    assert len(str(generated_number)) <= 11  # 1 character can be added for - sign


def test_generate_number_withNull100():
    # given
    property_name = "test_property"
    schema_json = {
        "type": ['number', 'null']
    }
    faker_factory = Faker()
    # when
    generated_number = data_generator.generate_number(schema_json, faker_factory, 100)
    # then
    assert generated_number is None


def test_generate_number_minimum_maximum():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "number",
        "maximum": 1000.00,
        "minimum": 0.00
    }
    faker_factory = Faker()
    # when
    generated_number = data_generator.generate_number(schema_json, faker_factory, 0)
    # then
    assert generated_number is not None
    assert isinstance(generated_number, float)
    assert 1000.00 >= generated_number
    assert 0.00 <= generated_number


def test_generate_number_const_value():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "number",
        "const": 30.00
    }
    faker_factory = Faker()
    # when
    generated_number = data_generator.generate_number(schema_json, faker_factory, 0)
    # then
    assert generated_number is not None
    assert isinstance(generated_number, float)
    assert 30.00 == generated_number


def test_generate_number_const_null():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "number",
        "const": None
    }
    faker_factory = Faker()
    # when
    generated_number = data_generator.generate_number(schema_json, faker_factory, 0)
    # then
    assert generated_number is None


def test_generate_number_max_length():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "number",
        "maxLength": 15
    }
    faker_factory = Faker()
    # when
    generated_number = data_generator.generate_number(schema_json, faker_factory, 0)
    # then
    assert generated_number is not None
    assert isinstance(generated_number, float)
    assert len(str(generated_number)) <= 16  # 1 character can be added for - sign


def test_generate_string_with_type_city():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "string",
        "$generator": "#/string-type/city"
    }
    faker_factory = Faker()
    # when
    generated_string = data_generator.generate_string_with_type(faker_factory, schema_json, 0)
    # then
    assert generated_string is not None
    assert isinstance(generated_string, str)


def test_generate_string_with_type_firstName():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "string",
        "$generator": "#/string-type/firstName"
    }
    faker_factory = Faker()
    # when
    generated_string = data_generator.generate_string_with_type(faker_factory, schema_json, 0)
    # then
    assert generated_string is not None
    assert isinstance(generated_string, str)


def test_generate_string_with_type_lastName():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "string",
        "$generator": "#/string-type/lastName"
    }
    faker_factory = Faker()
    # when
    generated_string = data_generator.generate_string_with_type(faker_factory, schema_json, 0)
    # then
    assert generated_string is not None
    assert isinstance(generated_string, str)


def test_generate_string_with_type_title():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "string",
        "$generator": "#/string-type/title"
    }
    faker_factory = Faker()
    # when
    generated_string = data_generator.generate_string_with_type(faker_factory, schema_json, 0)
    # then
    assert generated_string is not None
    assert isinstance(generated_string, str)


def test_generate_string_with_type_phone():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "string",
        "$generator": "#/string-type/phone"
    }
    faker_factory = Faker()
    # when
    generated_string = data_generator.generate_string_with_type(faker_factory, schema_json, 0)
    # then
    assert generated_string is not None
    assert isinstance(generated_string, str)


def test_generate_string_with_type_email():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "string",
        "$generator": "#/string-type/email"
    }
    faker_factory = Faker()
    # when
    generated_string = data_generator.generate_string_with_type(faker_factory, schema_json, 0)
    # then
    assert generated_string is not None
    assert isinstance(generated_string, str)


def test_generate_string_with_type_languageCode():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "string",
        "$generator": "#/string-type/languageCode"
    }
    faker_factory = Faker()
    # when
    generated_string = data_generator.generate_string_with_type(faker_factory, schema_json, 0)
    # then
    assert generated_string is not None
    assert isinstance(generated_string, str)


def test_generate_string_with_type_countryCode():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "string",
        "$generator": "#/string-type/countryCode"
    }
    faker_factory = Faker()
    # when
    generated_string = data_generator.generate_string_with_type(faker_factory, schema_json, 0)
    # then
    assert generated_string is not None
    assert isinstance(generated_string, str)


def test_generate_string_with_type_country():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "string",
        "$generator": "#/string-type/country"
    }
    faker_factory = Faker()
    # when
    generated_string = data_generator.generate_string_with_type(faker_factory, schema_json, 0)
    # then
    assert generated_string is not None
    assert isinstance(generated_string, str)


def test_generate_string_with_type_uuid():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "string",
        "$generator": "#/string-type/uuid"
    }
    faker_factory = Faker()
    # when
    generated_string = data_generator.generate_string_with_type(faker_factory, schema_json, 0)
    # then
    assert generated_string is not None
    assert isinstance(generated_string, str)


def test_generate_string_with_type_timezone():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "string",
        "$generator": "#/string-type/timezone"
    }
    faker_factory = Faker()
    # when
    generated_string = data_generator.generate_string_with_type(faker_factory, schema_json, 0)
    # then
    assert generated_string is not None
    assert isinstance(generated_string, str)


def test_generate_string_with_type_empty():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "string",
        "$generator": "#/string-type/empty"
    }
    faker_factory = Faker()
    # when
    generated_string = data_generator.generate_string_with_type(faker_factory, schema_json, 0)
    # then
    assert generated_string is not None
    assert isinstance(generated_string, str)
    assert "" == generated_string


def test_generate_string_with_type_invalid():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "string",
        "$generator": "#/string-type/invalid_type"
    }
    faker_factory = Faker()
    # when
    generated_string = data_generator.generate_string_with_type(faker_factory, schema_json, 0)
    # then
    assert generated_string is not None
    assert isinstance(generated_string, str)
    assert "" == generated_string


def test_generate_string_with_type_text():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "string",
        "$generator": "#/string-type/text"
    }
    faker_factory = Faker()
    # when
    generated_string = data_generator.generate_string_with_type(faker_factory, schema_json, 0)
    # then
    assert generated_string is not None
    assert isinstance(generated_string, str)
    assert 100 >= len(generated_string)


def test_generate_string_with_type_text_maxLength():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "string",
        "$generator": "#/string-type/text",
        "maxLength": 50
    }
    faker_factory = Faker()
    # when
    generated_string = data_generator.generate_string_with_type(faker_factory, schema_json, 0)
    # then
    assert generated_string is not None
    assert isinstance(generated_string, str)
    assert 50 >= len(generated_string)


def test_generate_string_with_type_random():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "string"
    }
    faker_factory = Faker()
    # when
    generated_string = data_generator.generate_string_with_type(faker_factory, schema_json, 0)
    # then
    assert generated_string is not None
    assert isinstance(generated_string, str)
    assert 1 <= len(generated_string)
    assert 100 >= len(generated_string)


def test_generate_string_with_type_random_minLength_maxLength():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "string",
        "minLength": 5,
        "maxLength": 50
    }
    faker_factory = Faker()
    # when
    generated_string = data_generator.generate_string_with_type(faker_factory, schema_json, 0)
    # then
    assert generated_string is not None
    assert isinstance(generated_string, str)
    assert 5 <= len(generated_string)
    assert 50 >= len(generated_string)


def test_generate_formatted_string_date():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "string",
        "format": "date"
    }
    faker_factory = Faker()
    # when
    generated_string = data_generator.generate_formatted_string(faker_factory, schema_json, 0)
    # then
    assert generated_string is not None
    assert isinstance(generated_string, str)
    assert datetime.strptime(generated_string, '%Y-%m-%d')


def test_generate_formatted_string_date_with_null100():
    # given
    property_name = "test_property"
    schema_json = {
        "type": ['string', 'null'],
        "format": "date"
    }
    faker_factory = Faker()
    # when
    generated_string = data_generator.generate_formatted_string(faker_factory, schema_json, 100)
    # then
    assert generated_string is None


def test_generate_formatted_string_date_with_null0():
    # given
    property_name = "test_property"
    schema_json = {
        "type": ['string', 'null'],
        "format": "date"
    }
    faker_factory = Faker()
    # when
    generated_string = data_generator.generate_formatted_string(faker_factory, schema_json, 0)
    # then
    assert generated_string is not None
    assert isinstance(generated_string, str)
    assert datetime.strptime(generated_string, '%Y-%m-%d')


def test_generate_formatted_string_date_min_max_future():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "string",
        "format": "date",
        "minimum": 0,
        "maximum": 10
    }
    faker_factory = Faker()
    # when
    generated_string = data_generator.generate_formatted_string(faker_factory, schema_json, 0)
    # then
    assert generated_string is not None
    assert isinstance(generated_string, str)
    assert datetime.strptime(generated_string, '%Y-%m-%d')


def test_generate_formatted_string_date_min_max_past():
    # given
    property_name = "test_property"
    schema_json = {
        "type": "string",
        "format": "date",
        "minimum": -10,
        "maximum": 0
    }
    faker_factory = Faker()
    # when
    generated_string = data_generator.generate_formatted_string(faker_factory, schema_json, 0)
    # then
    assert generated_string is not None
    assert isinstance(generated_string, str)
    assert datetime.strptime(generated_string, '%Y-%m-%d')


def test_generate_string_withNull0():
    # given
    property_name = "test_property"
    schema_json = {
        "type": ['string', 'null']
    }
    faker_factory = Faker()
    # when
    generated_string = data_generator.generate_string(property_name, schema_json, faker_factory, None, 0)
    # then
    assert generated_string is not None
    assert "" != generated_string


def test_generate_string_withNull100():
    # given
    property_name = "test_property"
    schema_json = {
        "type": ['string', 'null']
    }
    faker_factory = Faker()
    # when
    generated_string = data_generator.generate_string(property_name, schema_json, faker_factory, None, 100)
    # then
    assert generated_string is None


def test_generate_string_withNull0_inverted():
    # given
    property_name = "test_property"
    schema_json = {
        "type": ['null','string']
    }
    faker_factory = Faker()
    # when
    generated_string = data_generator.generate_string(property_name, schema_json, faker_factory, None, 0)
    # then
    assert generated_string is not None
    assert "" != generated_string


def test_generate_string_withNull0_inverted():
    # given
    property_name = "test_property"
    schema_json = {
        "type": ['null','string']
    }
    faker_factory = Faker()
    # when
    generated_string = data_generator.generate_string(property_name, schema_json, faker_factory, None, 100)
    # then
    assert generated_string is None
