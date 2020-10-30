from tap_test_data_generator import load_repositories, discover, load_schema_json


def test_load_repositories():
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
    # when
    object_repositories = load_repositories(config)
    # then
    assert object_repositories is not None
    assert "dim-sample" in object_repositories
    assert "width" in object_repositories["dim-sample"][0]
    assert 5 == object_repositories["dim-sample"][0]["width"]


def test_load_schema_json():
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
    # when
    schema_json = load_schema_json(config, stream)
    # then
    assert schema_json is not None
    assert "$schema" in schema_json
    assert "http://json-schema.org/draft-07/schema" == schema_json["$schema"]
    assert "type" in schema_json
    assert "object" == schema_json["type"]
    assert "properties" in schema_json
    assert "checked" in schema_json["properties"]
    assert "type" in schema_json["properties"]["checked"]
    assert "boolean" == schema_json["properties"]["checked"]["type"]
