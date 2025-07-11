def validate_register(data):
    required_fields = ("username", "password")

    missing_fields = [field for field in required_fields if not data.get(field)]

    if missing_fields:
        raise ValueError(f"Missing required field(s): {', '.join(missing_fields)}")

    not_string = [
        field for field in required_fields if not isinstance(data[field], str)
    ]

    if not_string:
        raise ValueError(f"{', '.join(not_string)} field(s) must be string.")

    if len(data["password"]) < 8:
        raise ValueError("Password must be at least 8 characters long.")
