import subprocess

from django.core.management.base import BaseCommand

from app import settings

from centurion_feature_flag.lib.feature_flag import CenturionFeatureFlagging



class Command(BaseCommand):
    help = 'Running this command will download the available feature flags form the Centurion Server if the cache has expired (>4hours) or the cache file does not exist.'


    def add_arguments(self, parser):
        parser.add_argument('-r', '--reload', action='store_true', help='Restart the Centurion Process')


    def handle(self, *args, **kwargs):

        if getattr(settings,'feature_flag', None):

            feature_flagging = CenturionFeatureFlagging(
                url = settings.feature_flag['url'],
                user_agent = settings.feature_flag['user_agent'],
                cache_dir =settings.feature_flag['cache_dir'],
                unique_id = settings.feature_flag.get('unique_id', None),
                version = settings.feature_flag.get('version', None),
            )

            self.stdout.write('Fetching Feature Flags.....')

            feature_flagging.get()

            if feature_flagging:

                self.stdout.write('Success.')

            else:

                self.stdout.stderr('Error. Something went wrong.')

            if kwargs['reload']:

                if settings.BUILD_SHA:

                    self.stdout.write('restarting Centurion')

                    restart = subprocess.run(["supervisorctl", "restart", "gunicorn"], capture_output = True)

                    status = subprocess.run(["supervisorctl", "status", "gunicorn"], capture_output = True)

                    if status.returncode == 0:

                        self.stdout.write('Centurion restarted successfully')



                    a = 'b'

                else:

                    self.stdout.write('using kwarg `--reload` whilst not within production does nothing.')

        else:

            self.stdout.write('Feature Flaggin is not enabled')





