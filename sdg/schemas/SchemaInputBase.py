# -*- coding: utf-8 -*-

import os
import json
import jsonschema

class SchemaInputBase:
    """A base class for importing a schema, querying it, and validating with it.

    This class assumes imported schema (self.schema) are valid JSON Schema."""


    def __init__(self, schema_path=''):
        """Create a new SchemaBase object

        Parameters
        ----------
        schema_path : string
            A path to the schema file to input
        """

        self.schema_path = schema_path
        self.load_schema()
        self.load_validator()


    def load_schema(self):
        """Load the schema. This should be overridden by a subclass."""
        raise NotImplementedError


    def load_validator(self):
        """Load the validator for this schema."""
        try:
            validator_class = jsonschema.validators.validator_for(self.schema)
            validator_class.check_schema(self.schema)
            self.validator = validator_class(self.schema)
        except Exception as e:
            print(e)


    def validate(self, indicator):
        """Validate the data and/or metadata for an Indicator object.

        Parameters
        ----------
        indicator : Indicator
            The instance of Indicator to validate

        Returns
        -------
        boolean
            True if validation passes, False otherwise
        """

        status = True
        if indicator.has_meta():
            try:
                self.validator.validate(indicator.meta)
            except:
                status = False
                print('Validation errors for indicator ' + indicator.inid)
                for error in self.validator.iter_errors(indicator.meta):
                    print(error.message)

        return status


    def get(self, field, default=None, must_exist=False):
        """Fetch a field from the schema by key.

        Parameters
        ----------
        field : string
            The name of a field to get
        default : string or None
            A default value if the field is not present
        must_exist : boolean
            If True, an exception will be raised if the field is not present

        Return
        ------
        mixed or None
            The value of the field if present, otherwise None
        """
        f = self.schema['properties'].get(field, default)
        if must_exist and f is None:
            raise ValueError(field + " doesn't exist in schema")
        return f


    def get_values(self, field):
        """Get the allowed values for a select or multiselect field.

        Parameters
        ----------
        field : string
            The name of a field to get allowed values for

        Returns
        -------
        list
            List of allowed values
        """
        options = self.get_allowed_options(field)

        return [x['enum'][0] for x in options]


    def get_allowed_options(self, field):
        """Return a list of allowed options for a field from the schema.

        Parameters
        ----------
        field : string
            The name of a field to get allowed options for

        Returns
        -------
        list
            List of allowed options (dicts)
        """

        field = self.get(field)

        # In JSON Schema the options are in "anyOf", which can be in 2 places.
        if 'anyOf' in field:
            return field['anyOf']
        elif 'items' in field and 'anyOf' in field['items']:
            return field['items']['anyOf']

        return []


    def get_value_translation(self, field):
        """Get a map of values to 'translation_key' for schema field options.

        Parameters
        ----------
        field : string
            The name of a field to get a value translation map for

        Returns
        -------
        Dict
            Dict of allowed values to translation keys for a particular field
        """

        options = self.get_allowed_options(field)

        if len(options) == 0:
            raise ValueError(field + " field does not have options element")

        return {x['enum'][0]: x['translation_key'] for x in options}