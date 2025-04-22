


class DoesNotExist:
    """Object does not exist

    Use this class as the expected value for a test cases expected value when
    the object does not exist.
    """

    @property
    def __name__(self):

        return str('does_not_exist')