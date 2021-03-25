from tap_test_data_generator import discover


def test_discover():
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
    assert catalog is not None
    catalog_dict = catalog.to_dict()
    assert "streams" in catalog_dict
    assert "tap_stream_id" in catalog_dict["streams"][0]
    assert "schema" in catalog_dict["streams"][0]
    assert "properties" in catalog_dict["streams"][0]["schema"]
    assert "checked" in catalog_dict["streams"][0]["schema"]["properties"]
    assert "type" in catalog_dict["streams"][0]["schema"]["properties"]["checked"]
    assert "boolean" == catalog_dict["streams"][0]["schema"]["properties"]["checked"]["type"]

