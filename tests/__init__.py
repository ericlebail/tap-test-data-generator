from tap_test_data_generator import load_definitions, load_schema_json, discover, load_schemas


def test_load_schemas():
    # given
    config = {
        "schema_dir": "tap_test_data_generator/schemas",
    }
    # when
    schemas = load_schemas(config)
    # then
    assert schemas is not None
    assert "sample" in schemas
    assert schemas["sample"] is not None
    schema_dict = schemas["sample"].to_dict()
    assert "properties" in schema_dict
    assert "checked" in schema_dict["properties"]
    assert "type" in schema_dict["properties"]["checked"]
    assert "boolean" == schema_dict["properties"]["checked"]["type"]


def test_load_schemas_invalid_dir():
    # given
    config = {
        "schema_dir": "tap_test_data_generator/dirdoesntexist",
    }
    # when
    schemas = load_schemas(config)
    # then
    assert schemas is not None
    assert 0 == len(schemas)


def test_load_schemas_wrong_file():
    # given
    config = {
        "schema_dir": "tap_test_data_generator/wrong_schemas",
    }
    # when
    schemas = load_schemas(config)
    # then
    assert schemas is not None
    assert 0 == len(schemas)


def test_load_definitions():
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
    catalog = discover(config)
    stream = catalog.get_stream("sample")
    schema_json = load_schema_json(config, stream)
    # when
    definitions = load_definitions(schema_json, config)
    # then
    assert definitions is not None
    assert "http://example.com/example.json/#" in definitions
    assert "$id" in definitions["http://example.com/example.json/#"]
    assert "http://example.com/example.json/#" == definitions["http://example.com/example.json/#"]["$id"]
    assert "type" in definitions["http://example.com/example.json/#"]
    assert "object" == definitions["http://example.com/example.json/#"]["type"]
    assert "required" in definitions["http://example.com/example.json/#"]
    assert ['checked', 'dimensions', 'id', 'name', 'color', 'price', 'tags', 'hour'] == \
           definitions["http://example.com/example.json/#"]["required"]


def test_load_definitions_empty_schema():
    # given
    config = {
        "schema_dir": "tap_test_data_generator/dirdoesntexist",
        "metadata_dir": "tap_test_data_generator/metadatas",
        "object_repository_dir": "tap_test_data_generator/object-repositories",
        "static_input_dir": "",
        "record_number": 100,
        "apply_record_number_on_pairwise": True,
        "data_locale_list": ["en_US", "fr_FR"]
    }
    catalog = discover(config)
    stream = catalog.get_stream("sample")
    schema_json = load_schema_json(config, stream)
    # when
    definitions = load_definitions(schema_json, config)
    # then
    assert definitions is not None


def test_load_definitions_not_JSON():
    # given
    config = {
        "schema_dir": "tap_test_data_generator/wrong_schemas",
        "metadata_dir": "tap_test_data_generator/metadatas",
        "object_repository_dir": "tap_test_data_generator/object-repositories",
        "static_input_dir": "",
        "record_number": 100,
        "apply_record_number_on_pairwise": True,
        "data_locale_list": ["en_US", "fr_FR"]
    }
    catalog = discover(config)
    stream = catalog.get_stream("sample")
    schema_json = load_schema_json(config, stream)
    # when
    definitions = load_definitions(schema_json, config)
    # then
    assert definitions is not None