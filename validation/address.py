def uri_to_iri(uri, errors='replace'):
    r"""Converts a URI in a given charset to a IRI.

    Examples for URI versus IRI:

    >>> uri_to_iri(b'http://xn--n3h.net/')
    u'http://\u2603.net/'
    >>> uri_to_iri(b'http://%C3%BCser:p%C3%A4ssword@xn--n3h.net/p%C3%A5th')
    u'http://\xfcser:p\xe4ssword@\u2603.net/p\xe5th'

    Query strings are left unchanged:

    >>> uri_to_iri('/?foo=24&x=%26%2f')
    u'/?foo=24&x=%26%2f'

    :param uri:
        The URI to convert.
    :param charset:
        The charset of the URI.
    :param errors:
        The error handling on decode.
    """
    assert isinstance(uri, str)
    uri = urlsplit(uri)

    host = decode_idna(uri.hostname) if uri.hostname else ''
    if ':' in host:
        host = '[%s]' % host

    netloc = host

    if uri.port:
        if not 0 <= int(uri.port) <= 65535:
            raise ValueError('Invalid port')
        netloc = '%s:%s' % (netloc, uri.port)

    if uri.username or uri.password:
        if uri.username:
            username = _safe_urlunquote(
                uri.username, errors='strict', unsafe='/:%'
            )
        else:
            username = ''

        if uri.password:
            password = _safe_urlunquote(
                uri.password, errors='strict', unsafe='/:%'
            )
            auth = '%s:%s' % (username, password)
        else:
            auth = username

        netloc = '%s@%s' % (auth, netloc)

    path = _safe_urlunquote(
        uri.path, errors=errors, unsafe='%/;?'
    )
    query = _safe_urlunquote(
        uri.query, errors=errors, unsafe='%;/?:@&=+,$#'
    )
    fragment = _safe_urlunquote(
        uri.fragment, errors=errors, unsafe='%;/?:@&=+,$#'
    )
    return urlunsplit(
        (uri.scheme, netloc, path, query, fragment)
    )


def _encode_netloc(components):
    host = ''
    if components.hostname:
        host = encode_idna(components.hostname).decode('ascii')
    if ':' in host:
        host = '[%s]' % host

    netloc = host

    if components.port:
        if not 0 <= int(components.port) <= 65535:
            raise ValueError('Invalid port')
        netloc = '%s:%s' % (netloc, components.port)

    if components.username or components.password:
        if components.username:
            username = urlquote(
                components.username, safe='/:%'
            )
        else:
            username = ''

        if components.password:
            password = urlquote(
                components.password, safe='/:%'
            )
            auth = '%s:%s' % (username, password)
        else:
            auth = username

        netloc = '%s@%s' % (auth, netloc)
    return netloc


def iri_to_uri(iri):
    r"""Converts any unicode based IRI to an acceptable ASCII URI. Verktyg
    always uses utf-8 URLs internally because this is what browsers and HTTP do
    as well. In some places where it accepts an URL it also accepts a unicode
    IRI and converts it into a URI.

    Examples for IRI versus URI:

    >>> iri_to_uri(u'http://☃.net/')
    'http://xn--n3h.net/'
    >>> iri_to_uri(u'http://üser:pässword@☃.net/påth')
    'http://%C3%BCser:p%C3%A4ssword@xn--n3h.net/p%C3%A5th'

    :param iri:
        The IRI to convert.

    :returns:
        The equivalent URI as an ascii only string object.
    """
    assert isinstance(iri, str)

    iri = urlsplit(iri)

    netloc = _encode_netloc(iri)

    path = urlquote(
        iri.path, safe='/:~+%'
    )
    query = urlquote(
        iri.query, safe='%&[]:;$*()+,!?*/='
    )
    fragment = urlquote(
        iri.fragment, safe='=%&[]:;$()+,!?*/'
    )

    return urlunsplit(
        (iri.scheme, netloc, path, query, fragment)
    )


def _validate_uri(value, required=True):
    if value is None:
        if required:
            raise TypeError("required value is None")
        return

    if not isinstance(value, six.binary_type):
        raise TypeError((
            "uris must be encoded as a byte string, "
            "but value is of type {cls!r}"
        ).format(cls=value.__class__.__name__))


class _uri_validator(object):
    def __init__(self, required):
        _validate_bool(required)
        self.__required = required

    def __call__(self, value):
        _validate_uri(value, required=self.__required)

    def __repr__(self):
        raise NotImplementedError()


def validate_uri(value):
    """

    """


def _validate_iri(value):
    if value is None:
        if required:
            raise TypeError("required value is None")
        return

    if not isinstance(value, six.text_type):
        raise TypeError((
            "iris must be encoded as a unicode string, "
            "but value is of type {cls!r}"
        ).format(cls=value.__class__.__name__))

    # Perform basic sanity checks.

    # Convert to canonical URI form and check that it matches.


class _iri_validator(object):
    def __init__(self, allow_unnormalized, required):
        _validate_bool(allow_unnormalized)
        self.__allow_unnormalized = allow_unnormalized

        _validate_bool(required)
        self.__required = required

    def __call__(self, value):
        _validate_iri(
            value,
            allow_unnormalized=self.__allow_unnormalized,
            required=self.__required,
        )

    def __repr__(self):
        raise NotImplementedError()


def validate_iri(value, allow_unnormalized=False, required=True):
    pass
