from django.contrib.auth import logout
from django.http import HttpResponseForbidden

from social_core import backends

from centurion.logging import CenturionLogger



def required_claim(backend, response, strategy, **kwargs) -> None | HttpResponseForbidden:

    logger: CenturionLogger = strategy.setting('CENTURION_LOG').getChild( suffix = 'auth')

    try:

        if not isinstance(backend, backends.oauth.OAuthAuth):
            return

        claim_name = strategy.setting(f'SOCIAL_AUTH_{backend.name}_REQUIRED_CLAIM_NAME'.upper())
        claim_value = strategy.setting(f'SOCIAL_AUTH_{backend.name}_REQUIRED_CLAIM_VALUE'.upper())

        logger.info( msg = 'Checking required claim is present for user '
            f"{getattr(kwargs['user'], kwargs['user'].USERNAME_FIELD)}." )

        if(
            not claim_name or not claim_value
            and (
                claim_name or claim_value
            )
        ):

            raise ValueError( 'Required claim name and/or value has not been '
                f'configured for backend {backend.name}.' )


        if claim_name not in response:

            raise ValueError(
                f'{backend.name} '
                f'NOT AUTHORIZED. Required claim {claim_name} '
                f'does not exist for user '
                f"{getattr(kwargs['user'], kwargs['user'].USERNAME_FIELD)}."
            )


        if isinstance(response[claim_name], list):

            if claim_value not in response[claim_name]:

                raise ValueError(
                    f'{backend.name} '
                    f'NOT AUTHORIZED. Required claim {claim_name} '
                    f'with a value of {claim_value} was not found for user '
                    f"{getattr(kwargs['user'], kwargs['user'].USERNAME_FIELD)}."
                )

        else:

            if claim_value != response[claim_name]:

                raise ValueError(
                    f'{backend.name} '
                    f'NOT AUTHORIZED. Required claim {claim_name} does '
                    f'not equal {claim_value}, actual {response[claim_name]} for user '
                    f"{getattr(kwargs['user'], kwargs['user'].USERNAME_FIELD)}."
                )

        logger.info( msg =  f'{backend.name} Required claim found for user '
                        f"{getattr(kwargs['user'], kwargs['user'].USERNAME_FIELD)}." )

        return None


    except ValueError as e:
        logger.info( msg = e )


    logout(strategy.request)
    return HttpResponseForbidden("denied")
