from django.test import TestCase

import pytest
import requests
import unittest

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from access.models.organization import Organization
from access.models.team import Team


