import abc

class ComponentBase(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def is_for():
        """Should return a string/identifier for what this component is meant to.
        In the case of a Writer for example this should be the output type it can
        handle. (i.e. constants.OUTPUT_TYPE)
        For Components that handle data (fetching, parsing...) the source
        that links them together. (i.e. constants.SOURCES)

        The identifier should be a unique way to identiy the istance of that type
        of componant against others of the same type, but can be shared against
        different types of components."""
        return NotImplemented
        # raise NotImplementedError
