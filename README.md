# tap-test-data-generator

This is a [Singer](https://singer.io) tap that produces JSON-formatted test data
following the [Singer spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap generates test data complying with the JSON Schema passed as input.
Useful for Data Driven Testing (DDT)

This tap:

- Read the provided JSON schema
- Create one stream per provided schema
- Outputs the schema for each stream
- Incrementally generate data based on the schema and send the generated Singer records to the data streams.

This tap uses [JSON Schema Draft 7](https://json-schema.org/)

![Build status](https://travis-ci.com/ericlebail/tap-test-data-generator.svg?branch=master)
[![codecov](https://codecov.io/gh/ericlebail/tap-test-data-generator/branch/master/graph/badge.svg?token=C37SIU1IUG)](https://codecov.io/gh/ericlebail/tap-test-data-generator)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Python 3.10.2](https://img.shields.io/badge/python-3.10.2-blue.svg)](https://www.python.org/downloads/release/python-3102/)

[Sources on Github](https://github.com/ericlebail/tap-test-data-generator)

[![Package on PyPI](https://img.shields.io/pypi/v/tap-test-data-generator.svg)](https://pypi.org/project/tap-test-data-generator/)

## Standard JSON schema has been extended to add required parameters for data generation

- for "string" properties:
    
    - generate constant string
        
            "type": "string",
            "const": "constant Value"
        
    - generate empty string
    
            "$generator": "#/string-type/empty"
    
    - generate UUID4 using [Faker UUID4](https://faker.readthedocs.io/en/master/providers/faker.providers.misc.html#faker.providers.misc.Provider.uuid4) 
          
            "$generator": "#/string-type/uuid" 
    
    - generate a text with specified length  ( "maxLength" is optional default value is 100) using [Faker text](https://faker.readthedocs.io/en/master/locales/en_US.html#faker.providers.lorem.en_US.Provider.text)
          
            "$generator": "#/string-type/text", "maxLength": 30
            
    - generate a title "Mr.","Miss", ... using [Faker prefix](https://faker.readthedocs.io/en/master/providers/faker.providers.person.html#faker.providers.person.Provider.prefix)
          
            "$generator": "#/string-type/title"
            
    - generate a person first name using [Faker first_name](https://faker.readthedocs.io/en/master/providers/faker.providers.person.html#faker.providers.person.Provider.first_name)
          
            "$generator": "#/string-type/firstName"
            
    - generate a person last name using [Faker last_name](https://faker.readthedocs.io/en/master/providers/faker.providers.person.html#faker.providers.person.Provider.last_name)
        
            "$generator": "#/string-type/lastName"
            
    - generate a phone number using [Faker phone_number](https://faker.readthedocs.io/en/master/providers/faker.providers.phone_number.html#faker.providers.phone_number.Provider.phone_number)
            
            "$generator": "#/string-type/phone"
            
    - generate an Email address using [Faker email](https://faker.readthedocs.io/en/master/providers/faker.providers.internet.html#faker.providers.internet.Provider.email)
        
            "$generator": "#/string-type/email"
            
    - generate a city name using [Faker city](https://faker.readthedocs.io/en/master/providers/faker.providers.address.html#faker.providers.address.Provider.city)
        
            "$generator": "#/string-type/city"
            
    - generate a country name using [Faker country](https://faker.readthedocs.io/en/master/providers/faker.providers.address.html#faker.providers.address.Provider.country)
        
            "$generator": "#/string-type/country"
            
    - generate an ISO country code using [Faker country_code](https://faker.readthedocs.io/en/master/providers/faker.providers.address.html#faker.providers.address.Provider.country_code)
        
            "$generator": "#/string-type/countryCode"
            
    - generate an I18n language code using [Faker language_code](https://faker.readthedocs.io/en/master/providers/baseprovider.html#faker.providers.BaseProvider.language_code)
        
            "$generator": "#/string-type/languageCode"
            
    - generate a date using [Faker date_between_dates](https://faker.readthedocs.io/en/master/providers/faker.providers.date_time.html#faker.providers.date_time.Provider.date_between_dates) date format is YYYY-mm-dd
    
    minimum : the number of days from today for minimum date (default value is -30 years in days) MUST BE INTEGER (positive or negative)
    
    maximum : the number of days from today for maximum date (default is 0) MUST BE INTEGER (positive or negative)
              
            "type": "string",
            "format": "date",
            "minimum": -5,
            "maximum": 10
      
- for "object" properties:
    - get one JSON object from the file "object-name.json" in the configured object_repository_dir directory

            "$generator": "#/object-repository/object-name"
            
    - generate empty object
    
            "$generator": "#/object-type/empty"
            
- for "number" properties:
    - generate constant number
              
            "type": "number",
            "const": 25.00
      
    - generate null/None number
    
            "type": ["number", "null"],
            "const": null
          
    - generate number between
        
            "type": "number",
            "maximum": 1000.00,
            "minimum": 0.00

    - generate a random number or null/None (By default 5% of null are generated, this frequency can be configured)

            "type": ["number", "null"]
        
- for "integer" properties:
    - generate constant integer
              
            "type": "integer",
            "const": 25
      
    - generate null/None integer
    
            "type": ["integer", "null"],
            "const": null
          
    - generate integer between
        
            "type": "integer",
            "maximum": 1000,
            "minimum": 0
      
    - generate a random integer or null/None (By default 5% of null are generated, this frequency can be configured)

            "type": ["integer", "null"]
          

- Pair combination generation is available:
    to activate it you need to add on the property. 
    
        "$pairwise": true
        
    this mode is available for:
    
    - boolean propeties
    - String properties with "Enum" or "pattern" (Warning pairwise generation on pattern can be very slow depending on your pattern complexity)
    - Object with "$generator": "#/object-repository/object-name"

## Config file description:
    
Here is a sample config file:
    
        {
          "schema_dir": "schemas",
          "metadata_dir": "metadatas",
          "static_input_dir": "",
          "object_repository_dir": "object-repositories",
          "record_number": 1,
          "apply_record_number_on_pairwise": true,
          "generate_pairwise_hash": false,
          "data_locale_list": ["en_US","fr_FR"],
          "null_percent": 5,
          "stream_configs": {
            "sample": {
              "record_number": 100,
              "apply_record_number_on_pairwise": true,
              "generate_pairwise_hash": true,
              "data_locale_list": ["en_US","fr_FR"],
              "pair_generation_mode": "pairwise"
            }
          }
        }
    
### First part is "global configuration":

- "schema_dir" path to directory that contains JSON schema file(s).    
- "metadata_dir" path to directory that contains Singer Metadata file(s).
- "static_input_dir" âth to directory that contains JSON static inputs file.

In those 3 directories we expect 1 file per stream, filename = <stream-id>.json

- "object_repository_dir" path to the directory that contains repositories JSON files.

### Second part is default configuration for all streams:

- "record_number" : the default number of generated records (if not override)
- "apply_record_number_on_pairwise" : boolean, if true the previous record number is generated ignoring the number of 
possible permutation number computed by pairwise algorithm
- "generate_pairwise_hash" : boolean, if true a "pairwise_hash" property is added to the generated data to identify the 
Pair used by each record.
- "data_locale_list" : list of locale for generated data [Faker Documentation](https://faker.readthedocs.io/en/stable/locales.html)
- "pair_generation_mode": Optional Possible values are "pairwise" (Default mode) "all_combinations" and "every_value_at_least_once"

This parameter defines the type of combination generated with the possible values of all properties marked with "$pairwise": true
    
    - every_value_at_least_once : is the smallest combination, every value will be used at least once.
    - pairwise : generates more combination compliant with [Pairwise Testing](http://pairwise.org/)
    - all_combinations : is the biggest, is will generate all possible combinations of the provided values (cartesian product)

- "null_percent": Optional frequency in percent of Null values generated.

### Third part is stream specific configuration:

expected structure is:

        "stream_configs": {
            <stream-id1> : {},
            <stream-id2> : {}
        }

All values from second part (Default values) can be overridden for each stream.
    
## Dependencies:

- [jsonschema](https://pypi.org/project/jsonschema/)
- [Faker](https://pypi.org/project/Faker/)
- [exrex](https://pypi.org/project/exrex/)
- [ijson](https://pypi.org/project/ijson/)
- [allpairspy](https://pypi.org/project/allpairspy/)

## Example:

In order to generate the following JSON:

    {
        "checked": false,
        "dimensions": {
            "width": 5,
            "height": 10
        },
        "id": 1,
        "name": "A green door",
        "color": "green",
        "price": 12.5,
        "tags": [
            "home",
            "green"
        ],
        "hour": "09:31:40 AM"
    }
    
We first generate the JSON schema:

    {
      "$schema": "http://json-schema.org/draft-07/schema",
      "$id": "http://example.com/example.json",
      "type": "object",
      "required": [
        "checked",
        "dimensions",
        "id",
        "name",
        "color",
        "price",
        "tags",
        "hour"
      ],
      "properties": {
        "checked": {
          "$id": "#/properties/checked",
          "type": "boolean"
        },
        "dimensions": {
          "$id": "#/properties/dimensions",
          "type": "object",
          "required": [
            "width",
            "height"
          ],
          "properties": {
            "width": {
              "$id": "#/properties/dimensions/properties/width",
              "type": "integer"
            },
            "height": {
              "$id": "#/properties/dimensions/properties/height",
              "type": "integer"
            }
          },
          "additionalProperties": true
        },
        "id": {
          "$id": "#/properties/id",
          "type": "integer"
        },
        "name": {
          "$id": "#/properties/name",
          "type": "string"
        },
        "color": {
          "$id": "#/properties/color",
          "type": "string",
          "enum": ["green", "yellow", "red"]
        },
        "price": {
          "$id": "#/properties/price",
          "type": "number"
        },
        "tags": {
          "$id": "#/properties/tags",
          "type": "array",
          "additionalItems": true,
          "items": {
            "$id": "#/properties/tags/items",
            "type": "string"
          }
        },
        "hour": {
          "$id": "#/properties/hour",
          "type": "string",
          "pattern": "(1[0-2]|0[1-9])(:[0-5]\\d){2} (A|P)M"
        }
      },
      "additionalProperties": true
    }
    
Then we add the data generation details

    {
      "$schema": "http://json-schema.org/draft-07/schema",
      "$id": "http://example.com/example.json",
      "type": "object",
      "required": [
        "checked",
        "dimensions",
        "id",
        "name",
        "color",
        "price",
        "tags",
        "hour"
      ],
      "properties": {
        "checked": {
          "$id": "#/properties/checked",
          "type": "boolean",
          "$pairwise": true
        },
        "dimensions": {
          "$id": "#/properties/dimensions",
          "type": "object",
          "required": [
            "width",
            "height"
          ],
          "properties": {
            "width": {
              "$id": "#/properties/dimensions/properties/width",
              "type": "integer"
            },
            "height": {
              "$id": "#/properties/dimensions/properties/height",
              "type": "integer"
            }
          },
          "additionalProperties": true,
          "$generator": "#/object-repository/dim-sample",
          "$pairwise": true
        },
        "id": {
          "$id": "#/properties/id",
          "type": "integer"
        },
        "name": {
          "$id": "#/properties/name",
          "type": "string",
          "$generator": "#/string-type/lastName"
        },
        "color": {
          "$id": "#/properties/color",
          "type": "string",
          "enum": ["green", "yellow", "red"],
          "$pairwise": true
        },
        "price": {
          "$id": "#/properties/price",
          "type": "number"
        },
        "tags": {
          "$id": "#/properties/tags",
          "type": "array",
          "additionalItems": true,
          "items": {
            "$id": "#/properties/tags/items",
            "type": "string"
          }
        },
        "hour": {
          "$id": "#/properties/hour",
          "type": "string",
          "pattern": "(1[0-2]|0[1-9])(:[0-5]\\d){2} (A|P)M"
        }
      },
      "additionalProperties": true
    }

Then we setup the config file (we have 1 stream, no stream specific configuration):

    {
      "schema_dir": "Path to schemas directory",
      "metadata_dir": "Path to metadatas directory",
      "object_repository_dir": "Path to object-repositories directory",
      "static_input_dir": "Path to static-input directory",
      "record_number": 100,
      "apply_record_number_on_pairwise": true,
      "generate_pairwise_hash": false,
      "data_locale_list": ["en_US","fr_FR"]
    }

For local list see [Faker Documentation](https://faker.readthedocs.io/en/stable/locales.html)

---

Copyright &copy; 2020 Elebail
