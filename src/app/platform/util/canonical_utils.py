def canonical_identifier(identifier: str | None) -> str | None:
    if identifier is None:
        return None
    return identifier.strip().lower() if "@" not in identifier else canonical_email(identifier)


def canonical_email(email: str | None) -> str | None:
    if email is None:
        return None
    return email.strip().lower()
