from schemadiff.changes import Change, ApiChange


class EnumValueAdded(Change):
    def __init__(self, enum, value):
        self.criticality = ApiChange.dangerous(
            "Adding an enum value may break existing clients that were not "
            "programming defensively against an added case when querying an enum."
        )
        self.enum = enum
        self.value = value

    @property
    def message(self):
        return f"Enum value `{self.value}` was added to `{self.enum.name}` enum"

    @property
    def path(self):
        return f"{self.enum.name}.{self.value}"


class EnumValueRemoved(Change):
    def __init__(self, enum, value):
        self.criticality = ApiChange.breaking(
            "Removing an enum value will break existing queries that use this enum value"
        )
        self.enum = enum
        self.value = value

    @property
    def message(self):
        return f"Enum value `{self.value}` was removed from `{self.enum.name}` enum"

    @property
    def path(self):
        return f"{self.enum.name}.{self.value}"


class EnumValueDescriptionChanged(Change):

    criticality = ApiChange.safe()

    def __init__(self, enum, name, old_value, new_value):
        self.enum = enum
        self.name = name
        self.old_value = old_value
        self.new_value = new_value

    @property
    def message(self):
        if not self.old_value.description:
            msg = f"Description for enum value `{self.name}` set to `{self.new_value.description}`"
        else:
            msg = (
                f"Description for enum value `{self.name}` changed"
                f" from `{self.old_value.description}` to `{self.new_value.description}`"
            )
        return msg

    @property
    def path(self):
        return f"{self.enum.name}.{self.name}"


class EnumValueDeprecationReasonChanged(Change):

    criticality = ApiChange.safe()

    def __init__(self, enum, name, old_value, new_value):
        self.enum = enum
        self.name = name
        self.old_value = old_value
        self.new_value = new_value

    @property
    def message(self):
        if not self.old_value.deprecation_reason:
            msg = (
                f"Enum value `{self.name}` was deprecated "
                f"with reason `{self.new_value.deprecation_reason}`"
            )
        else:
            msg = (
                f"Deprecation reason for enum value `{self.name}` changed "
                f"from `{self.old_value.deprecation_reason}` to `{self.new_value.deprecation_reason}`"
            )
        return msg

    @property
    def path(self):
        return f"{self.enum.name}.{self.name}"