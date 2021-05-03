class HandlerBase:

    def __init__(self, friendly="", description="", *args, **kwargs):

        self.friendly_name = friendly
        self.description = description

    @classmethod
    def get_from_object(cls, obj):
        """ Returns an instance of the subclass with all the properties retrieved
        from the provided object. Since all subclasses take *args, **kwargs
        we can pass everything we want to it and doesn't even care of the
        extra arguments."""

        return cls(
            source=getattr(obj, 'source', ""),
            type_=getattr(obj, 'output_type', ""),
            fetcher_cls=getattr(obj, 'Fetcher', None),
            parser_cls=getattr(obj, 'Parser', None),
            writer_cls=getattr(obj, 'Writer', None),
            filename_appendix=getattr(obj, 'filename_appendix', ""),
            description=getattr(obj, 'description', ""),
            friendly_name=getattr(obj, 'friendly_name', ""),
        )


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
