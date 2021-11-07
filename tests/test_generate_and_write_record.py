from allpairspy import AllPairs
from faker import Faker

from tap_test_data_generator import discover, load_repositories, load_schema_json, load_definitions, data_generator, \
    generate_and_write_record


def test_invalid_schema_wrong_type():
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
    # introduce schema error
    schema_json['properties']['dimensions']['type'] = 'invalid-type'

    # when
    record_index = generate_and_write_record(faker_factory, object_repositories, pairs, 0,
                                             schema_json, stream, False, definitions, 0)

    # then
    assert record_index is not None
    assert record_index == 0

