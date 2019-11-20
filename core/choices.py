import datetime

PLATAFORM_CHOICES = (
    ('steam', 'Steam'),
    ('gog', 'GOG Galaxy'),
    ('uplay', 'Uplay'),
)

OS_CHOICES = (
    ('windows', 'Windows'),
    ('linux', 'Linux'),
    ('macos', 'MacOS'),
)

YEARS_CHOICES = [(r, r) for r in range(1984, datetime.date.today().year + 1)]

MONTH_CHOICES = (
    ('1', u'Janeiro'),
    ('2', u'Fevereiro'),
    ('3', u'Março'),
    ('4', u'Abril'),
    ('5', u'Maio'),
    ('6', u'Junho'),
    ('7', u'Julho'),
    ('8', u'Agosto'),
    ('9', u'Setembro'),
    ('10', u'Outubro'),
    ('11', u'Novembro'),
    ('12', u'Dezembro'),
)
