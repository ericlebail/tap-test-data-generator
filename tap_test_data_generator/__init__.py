#!/usr/bin/env python3
import os
import json
import ijson
import singer
import jsonschema
from faker import Faker
from jsonschema import validate
from singer import utils
from singer.catalog import Catalog, CatalogEntry
from singer.schema import Schema

from tap_test_data_generator.value_pairs_combinator import compute_value_pairs
from . import data_generator

REQUIRED_CONFIG_KEYS = ["schema_dir", "metadata_dir", "object_repository_dir", "record_number",
                        "apply_record_number_on_pairwise", "generate_pairwise_hash"]
LOGGER = singer.get_logger()


def get_abs_path(path):
    path_os = path.replace("/", os.path.sep)
    pathname = os.path.join(os.getcwd(), path_os)
    return pathname


def load_config_for_stream(config, key, stream_id):
    value = None
    if key in config:
        value = config[key]
    if "stream_configs" in config and stream_id in config["stream_configs"] \
            and key in config["stream_configs"][stream_id]:
        value = config["stream_configs"][stream_id][key]
    return value


def load_schemas(config):
    """ Load schemas from schemas folder """
    schemas = {}
    schema_dir_path = get_abs_path(config['schema_dir'])
    if os.path.isdir(schema_dir_path):
        for filename in os.listdir(schema_dir_path):
            path = get_abs_path(config['schema_dir']) + '/' + filename
            file_raw = filename.replace('.json', '')
            if os.path.isfile(path):
                with open(path) as file:
                    try:
                        schemas[file_raw] = Schema.from_dict(json.load(file))
                    except json.decoder.JSONDecodeError as err:
                        LOGGER.warning("Schema file : " + file_raw + " is invalid or not JSON : " + err.msg)
    else:
        LOGGER.warning(schema_dir_path + " : Is not a valid directory")
    return schemas


def discover(config):
    raw_schemas = load_schemas(config)
    streams = []
    for stream_id, schema in raw_schemas.items():
        """ Load metadata from metadata folder """
        path = get_abs_path(config['metadata_dir']) + '/' + stream_id + '.json'
        if os.path.isfile(path):
            with open(path) as file:
                stream_metadata = json.load(file)
                key_properties = []
        else:
            # no metadata file adding default empty metadata
            stream_metadata = [
                {"metadata": {"selected": False, "inclusion": "available"}, "breadcrumb": []}
            ]
            key_properties = []
        streams.append(
            CatalogEntry(
                tap_stream_id=stream_id,
                stream=stream_id,
                schema=schema,
                key_properties=key_properties,
                metadata=stream_metadata,
                replication_key=None,
                is_view=None,
                database=None,
                table=None,
                row_count=None,
                stream_alias=None,
                replication_method=None,
            )
        )
    return Catalog(streams)


def load_definitions(schema_json, config):
    LOGGER.info("Loading definitions")
    definitions = {}
    # loading definitions internally set in schema
    if "definitions" in schema_json:
        definitions_values = schema_json['definitions']
        for key in definitions_values.keys():
            definitions['#/definitions/' + key] = definitions_values[key]
    # load external definitions
    if 'schema_dir' in config:
        definitions_dir_path = get_abs_path(config['schema_dir'] + '/definitions')
        if os.path.isdir(definitions_dir_path):
            for filename in os.listdir(definitions_dir_path):
                path = definitions_dir_path + '/' + filename
                if os.path.isfile(path):
                    with open(path) as file:
                        try:
                            file_content = json.load(file)
                            if "$id" in file_content:
                                id_value = file_content['$id']
                                definitions[id_value] = file_content
                        except json.decoder.JSONDecodeError as err:
                            LOGGER.warning("Definition file is invalid or not JSON : " + err.msg)
    return definitions


def sync(config, state, catalog):
    """ Sync data from tap source """
    # Loop over selected streams in catalog
    for stream in catalog.get_selected_streams(state):
        LOGGER.info("Syncing stream:" + stream.tap_stream_id)

        singer.write_schema(
            stream.tap_stream_id,
            stream.schema.to_dict(),
            stream.key_properties
        )
        apply_record_number_on_pairwise = load_config_for_stream(config, 'apply_record_number_on_pairwise',
                                                                 stream.tap_stream_id)
        pair_generation_mode = load_config_for_stream(config, 'pair_generation_mode', stream.tap_stream_id)
        generate_pairwise_hash = load_config_for_stream(config, 'generate_pairwise_hash',
                                                        stream.tap_stream_id)
        locale_list = load_config_for_stream(config, 'data_locale_list', stream.tap_stream_id)
        # initialize faker Factory
        faker_factory = Faker()
        if locale_list is not None:
            faker_factory = Faker(config['data_locale_list'])
        # load object-repositories
        object_repositories = load_repositories(config)

        schema_json = load_schema_json(config, stream)

        record_index = 0
        record_number = load_config_for_stream(config, 'record_number', stream.tap_stream_id)
        null_percent = load_config_for_stream(config, 'null_percent', stream.tap_stream_id)
        if null_percent is None:
            # default of 5 percent of generated values are null when applicable
            null_percent = 5

        definitions = load_definitions(schema_json, config)

        LOGGER.info("Extracting pairwise lists")
        # generate the list of values
        value_lists = data_generator.extract_value_lists(None, schema_json, object_repositories, definitions)

        # load the static data if provided:
        if "static_input_dir" in config:
            data_dir_name = config['static_input_dir']
            if data_dir_name:
                for filename in os.listdir(get_abs_path(data_dir_name)):
                    split_filename = os.path.splitext(filename)
                    if split_filename[0] == stream.tap_stream_id:
                        LOGGER.info("Static data file found for the stream")
                        path = get_abs_path(data_dir_name) + '/' + filename
                        load_json(path, stream.tap_stream_id, stream.schema)

        LOGGER.info("Generating records")
        record_index = generate_and_write_record_pairwise_list(faker_factory, object_repositories, record_index,
                                                               record_number, schema_json, stream, value_lists,
                                                               apply_record_number_on_pairwise, generate_pairwise_hash,
                                                               definitions, pair_generation_mode, null_percent)
        # generate again in loop to have the specified record number even if pairwise is active.
        if apply_record_number_on_pairwise:
            while record_index < record_number:
                record_index = generate_and_write_record_pairwise_list(faker_factory, object_repositories, record_index,
                                                                       record_number, schema_json, stream, value_lists,
                                                                       apply_record_number_on_pairwise,
                                                                       generate_pairwise_hash, definitions,
                                                                       pair_generation_mode, null_percent)
    return


def load_schema_json(config, stream):
    schema_json = {}
    if stream is not None:
        schema_path = get_abs_path(config['schema_dir']) + '/' + stream.tap_stream_id + '.json'
        if os.path.isfile(schema_path):
            with open(schema_path) as file:
                try:
                    schema_json = json.load(file)
                except json.decoder.JSONDecodeError as err:
                    LOGGER.warning("Schema is invalid : " + err.msg)
    else:
        LOGGER.warning("Cannot load schema JSON for empty stream")
    return schema_json


def load_repositories(config):
    object_repositories = {}
    for filename in os.listdir(get_abs_path(config['object_repository_dir'])):
        file_path = get_abs_path(config['object_repository_dir']) + '/' + filename
        file_raw = filename.replace('.json', '')
        with open(file_path, 'rb') as fd:
            object_list = []
            objects = ijson.items(fd, file_raw + '-list.item')
            for o in objects:
                object_list.append(o)
            object_repositories[file_raw] = object_list
    return object_repositories


def load_json(file_path, stream_id, stream_schema):
    with open(file_path, 'rb') as fd:
        objects = ijson.items(fd, stream_id + '.item')
        for o in objects:
            try:
                validate(o, stream_schema.to_dict())
                singer.write_record(stream_id, o)
            except jsonschema.exceptions.SchemaError as err:
                LOGGER.warning("Schema is invalid : " + err.message)
            except jsonschema.exceptions.ValidationError as err2:
                LOGGER.warning("Schema validation failed : " + err2.message)
    return


def generate_and_write_record_pairwise_list(faker_factory, object_repositories, record_index, record_number,
                                            schema_json, stream, value_lists, apply_record_number_on_pairwise,
                                            generate_pairwise_hash, definitions, pair_generation_mode, null_percent):
    # calculate the pairwise combinations
    pairwise_values = compute_value_pairs(value_lists, pair_generation_mode)
    for pairs in pairwise_values:
        record_index = generate_and_write_record(faker_factory, object_repositories, pairs, record_index,
                                                 schema_json, stream, generate_pairwise_hash, definitions, null_percent)
        # exit loop if number of record is reached
        if (record_index >= record_number) and apply_record_number_on_pairwise:
            break
    if record_index == 0:
        # specific case with no pairwise generation, switch to full random mode
        while record_index < record_number:
            record_index = generate_and_write_record(faker_factory, object_repositories, None, record_index,
                                                     schema_json, stream, generate_pairwise_hash, definitions, null_percent)
    return record_index


def generate_and_write_record(faker_factory, object_repositories, pairs, record_index, schema_json, stream,
                              generate_pairwise_hash, definitions, null_percent):
    # generate data matching schema for one record.
    try:
        # generate the required values
        generated_dict = data_generator.generate_dictionary(None, schema_json, {}, faker_factory, object_repositories,
                                                            pairs, definitions, null_percent)
        # add the pairwise hash if needed
        if generate_pairwise_hash:
            pairwise_hash = data_generator.generate_pairwise_hash(pairs)
            generated_dict["pairwise_hash"] = pairwise_hash
        resolver = jsonschema.RefResolver("", "", definitions)
        jsonschema.Draft4Validator(stream.schema.to_dict(), resolver=resolver).validate(generated_dict)
        # write one or more rows to the stream:
        singer.write_record(stream.tap_stream_id, generated_dict)
    except jsonschema.exceptions.SchemaError as err:
        LOGGER.warning("Schema is invalid : " + err.message)
    except jsonschema.exceptions.ValidationError as err2:
        LOGGER.warning("Schema validation failed : " + err2.message)
    record_index += 1
    return record_index


@utils.handle_top_exception(LOGGER)
def main():
    # Parse command line arguments
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)

    # If discover flag was passed, run discovery mode and dump output to stdout
    if args.discover:
        catalog = discover(args.config)
        catalog.dump()
    # Otherwise run in sync mode
    else:
        if args.catalog:
            catalog = args.catalog
        else:
            catalog = discover(args.config)
        sync(args.config, args.state, catalog)


if __name__ == "__main__":
    main()
