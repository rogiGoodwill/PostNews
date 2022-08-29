from django import template
from ..uncensor_words import UNCENSOR_WORDS

register = template.Library()


@register.filter(name='censor_filter')
def censor_filter(text: str):
    words = text.split()
    for word in words:
        value = word.strip('.,?!').lower()
        if value in UNCENSOR_WORDS:
            words[words.index(word)] = '***'

    return ' '.join(words)
