import re
from django import template
from urllib.parse import urlparse, parse_qs

from accounts.models import Perfil

register = template.Library()


@register.filter(name='youtube_embed_url')
# converts youtube URL into embed HTML
# value is url
def youtube_embed_url(value):
    if urlparse(value).netloc == "youtu.be":
        match = re.search(r'^(http|https)\:\/\/youtu\.be\/(\w*)(\&(.*))?$', value)

        if match:
            embed_url = 'https://www.youtube.com/embed/%s' % (match.group(2))
            res = "<iframe id=\"ytVideo\" width=\"100%%\" height=\"720\" src=\"%s\"?version=3?enablejsapi=1&controls=0 frameborder=\"0\" allow=\"accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen></iframe>" % (
                embed_url)
            return res
    elif ("embed/") in (urlparse(value).path):
        if value:
            res = "<iframe id=\"ytVideo\" width=\"100%%\" height=\"720\" src=\"%s\"?version=3?enablejsapi=1&controls=0 frameborder=\"0\" allow=\"accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen></iframe>" % (value)
            return res
    elif urlparse(value).netloc == "www.youtube.com":
        match = re.search(r'^(http|https)\:\/\/www\.youtube\.com\/watch\?v\=(\w*)(\&(.*))?$', value)

        if match:
            embed_url = 'https://www.youtube.com/embed/%s' % (match.group(2))
            res = "<iframe id=\"ytVideo\" width=\"100%%\" height=\"720\" src=\"%s\"?version=3?enablejsapi=1&controls=0 frameborder=\"0\" allow=\"accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen></iframe>" % (embed_url)
            return res
        else:
            embed_url = 'https://www.youtube.com/embed/%s' % (value.rsplit('watch?v=', 1)[-1])
            res = "<iframe id=\"ytVideo\" width=\"100%%\" height=\"720\" src=\"%s\"?version=3?enablejsapi=1&controls=0 frameborder=\"0\" allow=\"accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture\" allowfullscreen></iframe>" % (embed_url)
            return res


youtube_embed_url.is_safe = True


@register.filter(name='mylist')
# value is pk
def mylist(value, user):
    try:
        return Perfil.objects.filter(pk=user, carrinho__pk=value).exists()
    except:
        return False


@register.filter(name='youtube_featured')
def youtube_featured(value):
    u_pars = urlparse(value)
    quer_v = parse_qs(u_pars.query).get('v')
    if quer_v:
        return quer_v[0]
    pth = u_pars.path.split('/')
    if pth:
        return pth[-1]


youtube_embed_url.is_safe = True
