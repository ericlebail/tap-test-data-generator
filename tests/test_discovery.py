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

    item_number = 0
    for stream in catalog_dict["streams"]:
        item_number += 1
        assert "tap_stream_id" in stream
        # test the "sample stream"
        if "sample" == stream["tap_stream_id"]:
            assert "schema" in stream
            assert "properties" in stream["schema"]
            assert "checked" in stream["schema"]["properties"]
            assert "type" in stream["schema"]["properties"]["checked"]
            assert "boolean" == stream["schema"]["properties"]["checked"]["type"]
    # test item number
    assert item_number == 3

