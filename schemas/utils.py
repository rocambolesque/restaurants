from marshmallow import Schema, fields


class CsvList(fields.List):
    def _deserialize(self, value, attr, data):
        value = value.split(',')

        result = []
        errors = []
        for item in value:
            try:
                result.append(self.container.deserialize(item))
            except ValidationError as e:
                errors.append((item, e.messages))

        if errors:
            raise ValidationError(
                message={
                    'description': 'Error parsing data',
                    'code': 'csv_list_deserialization_validation_error',
                    'meta': {
                        'items': [error[0] for error in errors],
                        'errors': {error[0]: error[1] for error in errors},
                    }
                },
                data=result
            )

        return result
