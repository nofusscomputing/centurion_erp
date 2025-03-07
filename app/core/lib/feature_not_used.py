

class FeatureNotUsed:
    """Type used to denote that a feature is not enabled"""

    def __bool__(self):

        return False


    def __list__(self):

        return False