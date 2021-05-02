class HandlerBase:
    @staticmethod
    def validate_register(register, group, prefix="Handler Registrar name"):
        if not group:
            return True  # pragma: no cover
        if register not in group:
            raise TypeError(f'{prefix} should be one of {group}')
        return True

    @staticmethod
    def validate_component_class(cls, parent_cls, cls_ref="class"):
        if not issubclass(cls, parent_cls):
            raise TypeError("fetcher_cls should be a subclass of Writer")
        return True

    @staticmethod
    def validate_component_target(target, component_cls, cls_ref="Component"):
        if not target == component_cls.is_for():
            raise TypeError(f"Provided {cls_ref} is not a match for {target}")
