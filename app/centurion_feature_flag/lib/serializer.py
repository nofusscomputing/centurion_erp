from datetime import datetime


class FeatureFlag:
    """Centurion ERP Feature Flag

    Contains a Centurion ERP feature flag.

    Args:
        key (str):

    Attributes:
        __bool__ (bool): Enabled value
        __str__ (str): Name of the feature flag
        key (str): Feature Flag key
        name (str): Feature Flag name
        description (str): Feature Flag Description
        enabled (bool): Enabled value of the feature flag
        created (datetime): Creation date of the feature flag
        modified (datetime): Date when feature flag was last modified
    """

    _key: str = None

    _name: str = None

    _description: str = None

    _enabled: bool = None

    _created: datetime = None

    _modified: datetime = None


    def __init__(self, key, flag: dict):

        self._key = key

        self._name = flag['name']

        self._description = flag['description']

        self._enabled = flag['enabled']

        self._created = flag['created']

        self._modified = flag['modified']


    def __bool__(self) -> bool:
        """Feature Flag Enabled

        Returns:
            bool: Feature flag enabled value.
        """

        return self._enabled


    def __str__(self) -> str:
        """Fetch name of Feature Flag

        Returns:
            str: Name of the Feature Flag
        """

        return self._name


    @property
    def key(self) -> str:

        return self._key


    @property
    def name(self) -> str:

        return self._name


    @property
    def description(self) -> str:

        return self._description


    @property
    def enabled(self) -> bool:

        return self._enabled


    @property
    def created(self) -> datetime:

        return self._created


    @property
    def modified(self) -> datetime:

        return self._modified


    def dump(self) -> dict:

        return {
            self.key: {
                'name': self.name,
                'description': self.description,
                'enabled': self.enabled,
                'created': self.created,
                'modified': self.modified
            }
        }
