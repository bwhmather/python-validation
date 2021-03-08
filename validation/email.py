# -*- coding: utf-8 -*-

import re
import unicodedata
import idna
import six

from .core import _validate_bool
from .common import make_optional_argument_default

_undefined = make_optional_argument_default()

# Based on RFC 2822 section 3.2.4 / RFC 5322 section 3.2.3, these
# characters are permitted in email addresses (not taking into
# account internationalization):
_ATEXT = r"a-zA-Z0-9_!#\$%&\'\*\+\-/=\?\^`\{\|\}~"

# A "dot atom text", per RFC 2822 3.2.4:
_DOT_ATOM_TEXT = "[" + _ATEXT + "]+(?:\\.[" + _ATEXT + "]+)*"

# RFC 6531 section 3.3 extends the allowed characters in internationalized
# addresses to also include three specific ranges of UTF8 defined in
# RFC3629 section 4, which appear to be the Unicode code points from
# U+0080 to U+10FFFF.
_ATEXT_UTF8 = _ATEXT + u"\u0080-\U0010FFFF"
_DOT_ATOM_TEXT_UTF8 = "[" + _ATEXT_UTF8 + "]+(?:\\.[" + _ATEXT_UTF8 + "]+)*"

# The domain part of the email address, after IDNA (ASCII) encoding,
# must also satisfy the requirements of RFC 952/RFC 1123 which restrict
# the allowed characters of hostnames further. The hyphen cannot be at
# the beginning or end of a *dot-atom component* of a hostname either.
_ATEXT_HOSTNAME = r"(?:(?:[a-zA-Z0-9][a-zA-Z0-9\-]*)?[a-zA-Z0-9])"

# A "dot atom text", per RFC 2822 3.2.4, but using the restricted
# characters allowed in a hostname (see ATEXT_HOSTNAME above).
_DOT_ATOM_TEXT_HOSTNAME = _ATEXT_HOSTNAME + r"(?:\." + _ATEXT_HOSTNAME + r")*"

# Length constants
# RFC 3696 + errata 1003 + errata 1690
# (https://www.rfc-editor.org/errata_search.php?rfc=3696&eid=1690)
# explains the maximum length of an email address is 254 octets.
_EMAIL_MAX_LENGTH = 254
_LOCAL_PART_MAX_LENGTH = 64
_DOMAIN_MAX_LENGTH = 255


def _validate_email_address(
    value,
    allow_unnormalized,
    allow_smtputf8,
    required,
):
    if value is None:
        if required:
            raise TypeError("required value is None")
        return

    if not isinstance(value, six.text_type):
        raise TypeError(
            ("expected unicode string, but value is of type {cls!r}").format(
                cls=value.__class__.__name__
            )
        )

    parts = value.split("@")
    if len(parts) < 2:
        raise ValueError("email address is missing an '@' sign")
    if len(parts) > 2:
        raise ValueError("email address contains multiple '@' signs")

    local_part, domain = parts

    # === Validate and normalize the email address' local part ===

    if not local_part:
        raise ValueError("expected local part before '@', but found nothing")

    # RFC 5321 4.5.3.1.1
    # We're checking the number of characters here. If the local part
    # is ASCII-only, then that's the same as bytes (octets). If it's
    # internationalized, then the UTF-8 encoding may be longer, but
    # that may not be relevant. We will check the total address length
    # instead.
    if len(local_part) > _LOCAL_PART_MAX_LENGTH:
        raise ValueError(
            "expected at most 64 characters, "
            "but local part contains {chars}".format(chars=len(local_part))
        )

    if re.match(_DOT_ATOM_TEXT + "\\Z", local_part):
        # The local part is valid ascii.
        normalized_local_part = local_part
        ascii_local_part = local_part

    else:
        if not re.match(_DOT_ATOM_TEXT_UTF8 + "\\Z", local_part):
            # It's not a valid internationalized address either. Report which
            # characters were not valid.
            bad_chars = ", ".join(
                sorted(
                    set(
                        c
                        for c in local_part
                        if not re.match(
                            u"["
                            + (_ATEXT if not allow_smtputf8 else _ATEXT_UTF8)
                            + u"]",
                            c,
                        )
                    )
                )
            )
            raise ValueError(
                "local part contains invalid characters: {bad_chars!r}".format(
                    bad_chars=bad_chars
                )
            )

        if not allow_smtputf8:
            raise ValueError("invalid non-ascii characters in local part")

        # RFC 6532 section 3.1 also says that Unicode NFC normalization should
        # be applied.
        normalized_local_part = unicodedata.normalize("NFC", local_part)
        ascii_local_part = None

    # === Validate and normalize the email address' domain ===

    if len(domain) == 0:
        raise ValueError("expected domain name after '@', but found nothing")

    # Perform UTS-46 normalization, which includes casefolding, NFC
    # normalization, and converting all label separators (the period/full
    # stop, fullwidth full stop, ideographic full stop, and halfwidth
    # ideographic full stop) to basic periods.
    # It will also raise an exception if there is an invalid character in the
    # input, such as "⒈" which is invalid because it would expand to include
    # a period.
    try:
        domain = idna.uts46_remap(domain, std3_rules=False, transitional=False)
    except idna.IDNAError as e:
        raise ValueError(
            "domain name contains invalid characters: {error}".format(error=e)
        )

    # Now we can perform basic checks on the use of periods (since equivalent
    # symbols have been mapped to periods). These checks are needed because the
    # IDNA library doesn't handle well domains that have empty labels (i.e.
    # initial dot, trailing dot, or two dots in a row).
    if domain.endswith("."):
        raise ValueError("unexpected period at end of domain name")
    if domain.startswith("."):
        raise ValueError("unexpected period at start of domain name")
    if ".." in domain:
        raise ValueError("unexpected consecutive periods in domain name")

    # Regardless of whether international characters are actually used,
    # first convert to IDNA ASCII. For ASCII-only domains, the transformation
    # does nothing. If internationalized characters are present, the MTA
    # must either support SMTPUTF8 or the mail client must convert the
    # domain name to IDNA before submission.
    #
    # Unfortunately this step incorrectly 'fixes' domain names with leading
    # periods by removing them, so we have to check for this above. It also
    # gives a funky error message ("No input") when there are two periods in a
    # row, also checked separately above.
    try:
        ascii_domain = idna.encode(domain, uts46=False).decode("ascii")
    except idna.IDNAError as e:
        if "Domain too long" in str(e):
            # We can't really be more specific because UTS-46 normalization
            # means the length check is applied to a string that is different
            # from the one the user supplied. Also I'm not sure if the length
            # check applies to the internationalized form, the IDNA ASCII
            # form, or even both!
            raise ValueError("domain name is too long")
        raise ValueError(
            "domain name contains invalid characters: {error}".format(error=e)
        )

    # We may have been given an IDNA ASCII domain to begin with. Check that
    # the domain actually conforms to IDNA. It could look like IDNA but not be
    # actual IDNA. For ASCII-only domains, the conversion out of IDNA just
    # gives the same thing back.
    #
    # This gives us the canonical internationalized form of the domain, which
    # we should use in all error messages.
    try:
        normalized_domain = idna.decode(ascii_domain.encode("ascii"))
    except idna.IDNAError as e:
        raise ValueError(
            "domain name is not valid idna: {error}".format(error=e)
        )

    # RFC 5321 4.5.3.1.2
    # We're checking the number of bytes (octets) here, which can be much
    # higher than the number of characters in internationalized domains, on
    # the assumption that the domain may be transmitted without SMTPUTF8 as
    # IDNA ASCII. This is also checked by idna.encode, so this exception is
    # never reached.
    if len(ascii_domain) > _DOMAIN_MAX_LENGTH:
        raise ValueError(
            "expected no more than 255 characters after idna encoding, "
            "but domain expanded to {count}".format(count=len(ascii_domain))
        )

    # Check the regular expression. This is probably entirely redundant with
    # idna.decode, which also checks this format.
    m = re.match(_DOT_ATOM_TEXT_HOSTNAME + "\\Z", ascii_domain)
    if not m:
        raise ValueError("unexpected characters in address domain")

    # All publicly deliverable addresses have domain named with at least one
    # period. We also know that all TLDs end with a letter.
    if "." not in ascii_domain:
        raise ValueError(
            "expected a subdomain of a tld, but domain is missing a period"
        )
    if not re.search(r"[A-Za-z]\Z", ascii_domain):
        raise ValueError(
            "expected a subdomain of a tld, but tld does not match pattern"
        )

    # === Check bulk properties of the email address ===

    normalized_email = normalized_local_part + "@" + normalized_domain
    if ascii_local_part and ascii_domain:
        ascii_email = ascii_local_part + "@" + ascii_domain
    else:
        ascii_email = None

    # If the email address has an ASCII representation, then we assume it may
    # be transmitted in ASCII (we can't assume SMTPUTF8 will be used on all
    # hops to the destination) and the length limit applies to ASCII
    # characters (which is the same as octets). The number of characters in
    # may be many fewer (because IDNA ASCII is verbose) and could be less than
    # 254 Unicode characters, and of course the number of octets over the
    # limit may not be the number of characters over the limit, so if the
    # email address is internationalized, we can't give any simple information
    # about why the address is too long.
    #
    # In addition, check that the UTF-8 encoding (i.e. not IDNA ASCII and not
    # Unicode characters) is at most 254 octets. If the addres is transmitted
    # using SMTPUTF8, then the length limit probably applies to the UTF-8
    # encoded octets.  If the email address has an ASCII form that differs
    # from its internationalized form, I don't think the internationalized
    # form can be longer, and so the ASCII form length check would be
    # sufficient.  If there is no ASCII form, then we have to check the UTF-8
    # encoding. The UTF-8 encoding could be up to about four times longer than
    # the number of characters.
    if ascii_email and len(ascii_email) > _EMAIL_MAX_LENGTH:
        raise ValueError("email address is too long when isda encoded")
    else:
        if len(normalized_email) > _EMAIL_MAX_LENGTH:
            raise ValueError("email address is too long")

        if len(normalized_email.encode("utf8")) > _EMAIL_MAX_LENGTH:
            raise ValueError("email address is too long when utf-8 encoded")

    if not allow_unnormalized and value != normalized_email:
        raise ValueError("email address is not normalised")


class _email_address_validator(object):
    def __init__(self, allow_unnormalized, allow_smtputf8, required):
        _validate_bool(allow_unnormalized)
        self.__allow_unnormalized = allow_unnormalized

        _validate_bool(allow_smtputf8)
        self.__allow_smtputf8 = allow_smtputf8

        _validate_bool(required)
        self.__required = required

    def __call__(self, value):
        _validate_email_address(
            value,
            allow_unnormalized=self.__allow_unnormalized,
            allow_smtputf8=self.__allow_smtputf8,
            required=self.__required,
        )

    def __repr__(self):
        args = []
        if self.__allow_unnormalized:
            args.append("allow_unnormalized=True")

        if not self.__allow_smtputf8:
            args.append("allow_smtputf8=False")

        if not self.__required:
            args.append(
                "required={required!r}".format(
                    required=self.__required,
                )
            )

        return "validate_email_address({args})".format(args=", ".join(args))


def validate_email_address(
    value=_undefined,
    allow_unnormalized=False,
    allow_smtputf8=True,
    required=True,
):
    """
    Checks that a string represents a valid email address.

    By default, only email addresses in fully normalized unicode form are
    accepted.

    Validation logic is based on the well written and thoroughly researched
    [email-validator](https://pypi.org/project/email-validator/) library.
    By default, `validate_email_address` will only accept email addresses in
    the normalized unicode form returned by `email_validator.validate_email`.
    Despite the conflict with this library's naming convention, we recommend
    that you use `email-validator` for validation and sanitisation of untrusted
    input.

    :param str value:
        The value to be validated.
    :param bool allow_unnormalized:
        Whether or not to accept addresses that are not completely normalized.
        Defaults to False, as in most cases you will want equivalent email
        addresses to compare equal.
    :param bool allow_smtputf8:
        Whether or not to accept email addresses with local parts that can't be
        encoded as plain ascii.  Defaults to True, as such email addresses are
        now common and very few current email servers do not support them.
    :param bool required:
        Whether the value can be `None`.  Defaults to `True`.

    :raises TypeError:
        If the value is not a unicode string.
    :raises ValueError:
        If the value is not an email address, or is not normalized.
    """
    validate = _email_address_validator(
        allow_unnormalized=allow_unnormalized,
        allow_smtputf8=allow_smtputf8,
        required=required,
    )

    if value is not _undefined:
        validate(value)
    else:
        return validate
