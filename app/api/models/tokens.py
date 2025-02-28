import hashlib
import random
import string

from django.conf import settings
from django.db import models
from django.forms import ValidationError

from rest_framework.reverse import reverse

from access.fields import (
    AutoCreatedField,
    AutoLastModifiedField
)



class AuthToken(models.Model):


    class Meta:

        ordering = [
            'expires'
        ]

        verbose_name = 'Auth Token'

        verbose_name_plural = 'Auth Tokens'



    def validate_note_no_token(self, note, token, raise_exception = True) -> bool:
        """ Ensure plaintext token cant be saved to notes field.

        called from app.settings.views.user_settings.TokenAdd.form_valid()

        Args:
            note (Field): _Note field_
            token (Field): _Token field_

        Raises:
            ValidationError: _Validation failed_
        """

        validation: bool = True


        if str(note) == str(token):

            validation = False


        if str(token)[:9] in str(note):    # Allow user to use up to 8 chars so they can reference it.

            validation = False

        if not validation and raise_exception:

            raise ValidationError('Token can not be placed in the notes field.')

        return validation



    id = models.AutoField(
        blank=False,
        help_text = 'ID of this token',
        primary_key=True,
        unique=True,
        verbose_name = 'ID'
    )

    note = models.CharField(
        blank = True,
        default = None,
        help_text = 'A note about this token',
        max_length = 50,
        null= True,
        verbose_name = 'Note'
    )

    token = models.CharField(
        blank = False,
        db_index=True,
        help_text = 'The authorization token',
        max_length = 64,
        null = False,
        unique = True,
        verbose_name = 'Auth Token',
    )


    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        help_text = 'User this token belongs to',
        on_delete=models.CASCADE,
        verbose_name = 'Owner'
    )

    expires = models.DateTimeField(
        blank = False,
        help_text = 'When this token expires',
        null = False,
        verbose_name = 'Expiry Date',
    )


    created = AutoCreatedField()

    modified = AutoLastModifiedField()


    @property
    def generate(self) -> str:

        return str(hashlib.sha256(str(self.randomword()).encode('utf-8')).hexdigest())


    def token_hash(self, token:str) -> str:

        salt = settings.SECRET_KEY

        return str(hashlib.sha256(str(token + salt).encode('utf-8')).hexdigest())


    def randomword(self) -> str:
    
        return ''.join(random.choice(string.ascii_letters) for i in range(120))


    def __str__(self):

        return self.token


    table_fields: list = [
        'note',
        'created',
        'expires',
        '-action_delete-',
    ]


    def get_url( self, request = None ) -> str:

        if request:

            return reverse(f"v2:_api_v2_user_settings_token-detail", request=request, kwargs = self.get_url_kwargs() )

        return reverse(f"v2:_api_v2_user_settings_token-detail", kwargs = self.get_url_kwargs() )


    def get_url_kwargs(self) -> dict:
        """Fetch the URL kwargs

        Returns:
            dict: kwargs required for generating the URL with `reverse`
        """

        return {
            'model_id': self.user.id,
            'pk': self.id
        }
