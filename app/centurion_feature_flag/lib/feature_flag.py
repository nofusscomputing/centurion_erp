import json
import requests

from datetime import datetime
from dateutil.parser import parse
from pathlib import Path

from centurion_feature_flag.lib.serializer import FeatureFlag


class CenturionFeatureFlagging:
    """Centurion ERP Feature Flags

    This class contains all required methods so as to use feature flags
    provided by a Centurion ERP deployment.

    Examples:

    Checking if feature flagging is usable can be done with:

    >>> ff = CenturionFeatureFlagging(
    >>>     'http://127.0.0.1:8002/api/v2/public/1/flags/2844',
    >>>     'Centurion ERP',
    >>>     './your-cache-dir'
    >>> )
    >>> if ff:
    >>>     print('ok')
    ok

    To use a feature flag, in this case `2025-00007` can be achived with:

    >>> if ff["2025-00007"]:
    >>>     print('ok')
    ok

    Note: This assumes that feature flag `2025-00007` is enabled. If it is not
    `false` will be returned as the boolean check returns the flags `enabled`
    value.

    Args:
        url (str): URL of the Centurion Instance to query
        user_agent (str): User Agent to report to Centurion Instance this
            should be the name of your application
        cache_dir (str): Directory where the feature flag cache file is saved.
        disable_downloading (bool): Prevent the downloaing of feature flags
        unique_id (str, optional): Unique ID of the application that is
            reporting to Centurion ERP
        version (str, optional): The version of your application

    Attributes:
        __len__ (int): Count of feature flags
        __bool__ (bool): Feature Flag fetch was successful
        CenturionFeatureFlagging[<feature flag>] (dict): Feature flag data
        get (None): Make a http request to the Centurion ERP
            instance.
    """

    _cache_date: datetime = None
    """Date the feature flag file was last saved"""

    _cache_dir: str = None
    """Directory name (with trailing slash `/`) where the feature flags will be saved/cached."""

    _disable_downloading: bool = False
    """Prevent check-in and subsequent downloading from remote Centurion instance"""

    _feature_flags: list = None

    _feature_flag_filename: str = 'feature_flags.json'
    """ File name for the cached feture flags"""

    _headers: dict = {
        "Accept": "application/json",
    }

    _last_modified: datetime = None
    """ Last modified date/time of the feature flags"""

    _over_rides: dict = None
    """Feature Flag Over rides."""

    _response: requests.Response = None
    """Cached response from fetched feature flags"""

    _ssl_verify: bool = True
    """Verify the SSL certificate of the remote Centurion ERP instance"""

    _url: str = None
    """ url of the centurion ERP instance"""



    def __init__(
        self,
        url: str,
        user_agent: str,
        cache_dir: str,
        disable_downloading: bool = False,
        unique_id: str = None,
        version: str = None,
        over_rides: dict = None,
    ):

        if not str(cache_dir).endswith('/'):

            raise AttributeError(f'cache directory {cache_dir} must end with trailing slash `/`')


        self._url = url

        self._cache_dir = cache_dir

        self._disable_downloading = disable_downloading

        if self._disable_downloading:

            self._feature_flags = {}

        _over_rides: dict = {}

        if over_rides:

            for entry in over_rides:

                [*key], [*flag] = zip(*entry.items())

                _over_rides.update({
                    key[0]: FeatureFlag(key[0], flag[0])
                })


        self._over_rides = _over_rides


        if version is None:

            self._headers.update({
                'User-Agent': f'{user_agent} 0.0'
            })

        else:

            self._headers.update({
                'User-Agent': f'{user_agent} {version}'
            })

        if unique_id is not None:

            self._headers.update({
                'client-id': unique_id
            })


    def __bool__(self) -> bool:

        if(
            (
                (
                    getattr(self._response, 'status_code', 0) == 200
                    or getattr(self._response, 'status_code', 0) == 304
                )
                and self._feature_flags is not None
            )
            or (    # Feature flags were loaded from file
               self._feature_flags is not None
               and self._last_modified is not None
            )
        ):

            return True

        return False



    def __getitem__(self, key: str, raise_exceptions: bool = False) -> dict:
        """ Fetch a Feature Flag

        Args:
            key (str): Feature Flag id to fetch.
            raise_exceptions (bool, optional): Raise an exception if the key is
                not found. Default `False`

        Raises:
            KeyError: The specified Feature Flag does not exist. Only if arg `raise_exceptions=True`

        Returns:
            dict: A complete Feature Flag.
        """
        if(
            self._feature_flags is None
            and self._over_rides.get(key, None) is None
        ):

            print('Feature Flagging has not been completly initialized.')
            print('    please ensure that the feature flags have been downloaded.')

            return False


        if(
            self._feature_flags.get(key, None) is None
            and self._over_rides.get(key, None) is None
            and raise_exceptions
        ):

            raise KeyError(f'Feature Flag "{key}" does not exist')

        elif(
            not raise_exceptions
            and self._feature_flags.get(key, None) is None
            and self._over_rides.get(key, None) is None
        ):

            return False

        elif(
            not raise_exceptions
            and self._over_rides.get(key, None) is not None
        ):

            return  self._over_rides[key]

        
        return self._feature_flags[key]



    def __len__(self) -> int:
        """Count the Feature Flags

        Returns:
            int: Total number of feature flags.
        """

        return len(self._feature_flags)



    def get( self ):
        """ Get the available Feature Flags

        Will first check the filesystem for file `feature_flags.json` and if
        the file is '< 4 hours' old, will load the feature flags from the file.
        If the file does not exist or the file is '> 4 hours' old, the feature
        flags will be fetched from Centurion ERP.
        """

        url = self._url

        fetched_flags: list = []

        feature_flag_path = self._cache_dir + self._feature_flag_filename

        feature_flag_file = Path(feature_flag_path)

        if feature_flag_file.is_file():

            if(
                feature_flag_file.lstat().st_mtime > datetime.now().timestamp() - (4 * 3580)    # -20 second buffer
                or self._disable_downloading
            ):
                # Only open file if less than 4 hours old

                with open(feature_flag_path, 'r') as saved_feature_flags:

                    fetched_flags = json.loads(saved_feature_flags.read())

                    self._cache_date = datetime.fromtimestamp(feature_flag_file.lstat().st_mtime)
                    
                    url = None


        response = None

        if self._disable_downloading:    # User has disabled downloading.

            url = None

        while(url is not None):

            try:

                resp = requests.get(
                    headers = self._headers,
                    timeout = 3,
                    url = url,
                    verify = self._ssl_verify,
                )

                if response is None:    # Only save first request

                    response = resp

                    self._response = response


                if resp.status_code == 304:    # Nothing has changed, exit the loop

                    url = None

                elif resp.ok:    # Fetch next page of results

                    fetched_flags += resp.json()['results']

                    url = resp.json()['next']

                else:

                    url = None

            except requests.exceptions.ConnectionError as err:

                print(f'Error Connecting to {url}')

                url = None

            except requests.exceptions.ReadTimeout as err:

                print(f'Connection Timed Out connecting to {url}')

                url = None


        if(
            getattr(response, 'status_code', 0) == 200
            or len(fetched_flags) > 0
        ):

            feature_flags: dict = {}

            for entry in fetched_flags:

                [*key], [*flag] = zip(*entry.items())

                feature_flags.update({
                    key[0]: FeatureFlag(key[0], flag[0])
                })

            self._feature_flags = feature_flags

            if response is not None:

                if response.headers.get('last-modified', None) is not None:

                    self._last_modified = datetime.strptime(response.headers['last-modified'], '%a, %d %b %Y %H:%M:%S %z')

            else:

                last_mod_date: datetime = datetime.fromtimestamp(0)

                for item in self._feature_flags:

                    parsed_date = parse(self._feature_flags[item].modified)

                    if parsed_date.timestamp() > last_mod_date.timestamp():

                        last_mod_date = parsed_date

                self._last_modified = last_mod_date



            if getattr(response, 'status_code', 0) == 200:

                with open(feature_flag_path, 'w') as feature_flag_file:

                    feature_flag_file.write(self.toJson())

                self._cache_date = datetime.now()



    def toJson(self):

        obj = []

        for entry in self._feature_flags:

            obj += [
                self._feature_flags[entry].dump()
            ]

        return json.dumps(obj)
