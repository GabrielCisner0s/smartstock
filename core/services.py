class BaseService:

    @staticmethod
    def validate_required_fields(data, fields):

        for field in fields:

            if field not in data:

                raise ValueError(
                    f"Falta el campo {field}"
                )