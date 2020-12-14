
class StringGenerator:

    @staticmethod
    def generate_city(faker_factory, schema_json):
        return faker_factory.city()

    @staticmethod
    def generate_firstName(faker_factory, schema_json):
        return faker_factory.first_name()

    @staticmethod
    def generate_lastName(faker_factory, schema_json):
        return faker_factory.last_name()

    @staticmethod
    def generate_title(faker_factory, schema_json):
        return faker_factory.prefix()

    @staticmethod
    def generate_phone(faker_factory, schema_json):
        return faker_factory.phone_number()

    @staticmethod
    def generate_email(faker_factory, schema_json):
        return faker_factory.email()

    @staticmethod
    def generate_languageCode(faker_factory, schema_json):
        return faker_factory.language_code()

    @staticmethod
    def generate_countryCode(faker_factory, schema_json):
        return faker_factory.country_code()

    @staticmethod
    def generate_country(faker_factory, schema_json):
        return faker_factory.country()

    @staticmethod
    def generate_text(faker_factory, schema_json):
        # generate text
        max_char = 100
        if "maxLength" in schema_json:
            max_char = schema_json['maxLength']
        return faker_factory.text(max_nb_chars=max_char).replace('\n', '')

    @staticmethod
    def generate_uuid(faker_factory, schema_json):
        return faker_factory.uuid4()

    @staticmethod
    def generate_timezone(faker_factory, schema_json):
        return faker_factory.timezone()

    @staticmethod
    def generate_empty(faker_factory, schema_json):
        return ""
