class HandlerBase:

    def __init__(self, friendly="", description=""):

        self.friendly_name = friendly
        self.description = description

    @staticmethod
    def validate_component_class(target, cls, parent_cls, cls_ref="class"):
        if not issubclass(cls, parent_cls):
            raise TypeError(
                f"fetcher_cls should be a subclass of {cls_ref},"
                f" got {type(cls)} instead")

        if not target == cls.is_for():
            raise TypeError(
                f"{cls_ref} {cls.__name__} has the wrong target."
                " should be {target}")
        return True
