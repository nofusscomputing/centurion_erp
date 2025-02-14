from django import template
from django.template.defaultfilters import stringfilter

from core.lib.markdown import Markdown

register = template.Library()


@register.filter()
@stringfilter
def markdown(value):

    if not value:
        value = None

    markdown = Markdown()

    return markdown.render_markdown(value)


@register.filter()
@stringfilter
def lower(value):
    return str(value).lower()

@register.filter()
@stringfilter
def ticket_status(value):

    return str(value).lower().replace('(', '').replace(')', '').replace(' ', '_')


@register.filter()
@stringfilter
def date_time_seconds(value):

    return str(value).split('.')[0]


@register.filter()
@stringfilter
def to_duration(value):
    """Convert seconds to duration value

    Args:
        value (str): Time in seconds

    Returns:
        str: Duration value in format 00h 00m 00s
    """

    hour = int(3600)
    minute = int(60)

    if '-' in value:
        hour = int(-3600)
        minute = int(-60)

    hours = int(int(value)//hour)

    minutes = int((int(value)%hour)//minute)

    seconds = int((int(value)%hour)%minute)

    return str("{:02d}h {:02d}m {:02d}s".format(hours, minutes, seconds))

@register.simple_tag
def concat_strings(*args):
    """concatenate all args"""
    return ''.join(map(str, args))