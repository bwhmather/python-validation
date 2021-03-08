# -*- coding: utf-8 -*-

import unittest

from validation import validate_email_address


class ValidateIntTestCase(unittest.TestCase):
    def test_valid_simple(self):
        validate_email_address(u"Abc@example.com")

    def test_valid_dot_in_local_part(self):
        validate_email_address(u"Abc.123@example.com")

    def test_valid_sensible_symbols_in_local_part(self):
        validate_email_address(u"user+mailbox/department=shipping@example.com")

    def test_valid_mad_symbols_in_local_part(self):
        validate_email_address(u"!#$%&'*+-/=?^_`.{|}~@example.com")

    def test_valid_chinese(self):
        validate_email_address(u"伊昭傑@郵件.商務")

    def test_valid_devanagari(self):
        validate_email_address(u"राम@मोहन.ईन्फो")

    def test_valid_cyrilic(self):
        validate_email_address(u"юзер@екзампл.ком")

    def test_valid_greek(self):
        validate_email_address(u"θσερ@εχαμπλε.ψομ")

    def test_invalid_taiwanese_not_normalized(self):
        with self.assertRaises(
            ValueError, msg="email address is not normalized"
        ):
            validate_email_address(u"葉士豪@臺網中心.tw")

    def test_valid_mixed_ascii_taiwanese(self):
        validate_email_address(u"jeff@臺網中心.tw")

    def test_invalid_all_taiwanese_not_normalized(self):
        with self.assertRaises(
            ValueError, msg="email address is not normalized"
        ):
            validate_email_address(u"葉士豪@臺網中心.台灣")

    def test_invalid_mixed_local_part_not_normalized(self):
        with self.assertRaises(
            ValueError, msg="email address is not normalized"
        ):
            validate_email_address(u"jeff葉@臺網中心.tw")

    def test_valid_accents(self):
        validate_email_address(u"ñoñó@example.com")

    def test_valid_chinese_local_part(self):
        validate_email_address(u"我買@example.com")

    def test_valid_chinese_local_part_long(self):
        validate_email_address(u"甲斐黒川日本@example.com")

    def test_valid_cyrilic_long(self):
        validate_email_address(u"чебурашкаящик-с-апельсинами.рф@example.com")

    def test_valid_devangari_local_part_long(self):
        validate_email_address(u"उदाहरण.परीक्ष@domain.with.idn.tld")

    def test_valid_greek_mixed(self):
        validate_email_address(u"ιωάννης@εεττ.gr")

    def test_invalid_leading_dot(self):
        with self.assertRaises(
            ValueError,
            msg="An email address cannot have a period immediately after the "
            " @-sign.",
        ):
            validate_email_address(u"my@.leadingdot.com")

    def test_invalid_leading_fwdot(self):
        with self.assertRaises(
            ValueError,
            msg="An email address cannot have a period immediately after the "
            "@-sign.",
        ):
            validate_email_address(u"my@．．leadingfwdot.com")

    def test_invalid_leading_dots(self):
        with self.assertRaises(
            ValueError,
            msg="An email address cannot have a period immediately after the "
            "@-sign.",
        ):
            validate_email_address(u"my@..twodots.com")

    def test_invalid_consecutive_dots(self):
        with self.assertRaises(
            ValueError,
            msg="An email address cannot have two periods in a row.",
        ):
            validate_email_address(u"my@twodots..com")

    def test_invalid_dash_component(self):
        with self.assertRaises(
            ValueError,
            msg="The domain name baddash.-.com contains invalid characters "
            "(Label must not start or end with a hyphen).",
        ):
            validate_email_address(u"my@baddash.-.com")

    def test_invalid_leading_dash_component(self):
        with self.assertRaises(
            ValueError,
            msg="The domain name baddash.-a.com contains invalid characters "
            "(Label must not start or end with a hyphen).",
        ):
            validate_email_address(u"my@baddash.-a.com")

    def test_invalid_trailing_dash_component(self):
        with self.assertRaises(
            ValueError,
            msg="The domain name baddash.b-.com contains invalid characters "
            "(Label must not start or end with a hyphen).",
        ):
            validate_email_address(u"my@baddash.b-.com")

    def test_invalid_newline_following_domain(self):
        with self.assertRaises(
            ValueError,
            msg="The domain name example.com\n contains invalid characters "
            "(Codepoint U+000A at position 4 of 'com\\n' not allowed).",
        ):
            validate_email_address(u"my@example.com\n")

    def test_invalid_newline_in_domain(self):
        with self.assertRaises(
            ValueError,
            msg="The domain name example\n.com contains invalid characters "
            "(Codepoint U+000A at position 8 of 'example\\n' not allowed).",
        ):
            validate_email_address(u"my@example\n.com")

    def test_invalid_leading_dot_in_local_part(self):
        with self.assertRaises(
            ValueError,
            msg="The email address contains invalid characters before the "
            "@-sign: ..",
        ):
            validate_email_address(u".leadingdot@domain.com")

    def test_invalid_two_leading_dots_in_local_part(self):
        with self.assertRaises(
            ValueError,
            msg="The email address contains invalid characters before the "
            "@-sign: ..",
        ):
            validate_email_address(u"..twodots@domain.com")

    def test_invalid_consecutive_dots_in_local_part(self):
        with self.assertRaises(
            ValueError,
            msg="The email address contains invalid characters before the "
            "@-sign: ..",
        ):
            validate_email_address(u"twodots..here@domain.com")

    def test_invalid_invalid_character_in_domain(self):
        with self.assertRaises(
            ValueError,
            msg="The domain name ⒈wouldbeinvalid.com contains invalid "
            "characters (Codepoint U+2488 not allowed "
            "at position 1 in '⒈wouldbeinvalid.com').",
        ):
            validate_email_address(u"me@⒈wouldbeinvalid.com")

    def test_invalid_missing_local_part(self):
        with self.assertRaises(
            ValueError, msg="There must be something before the @-sign."
        ):
            validate_email_address(u"@example.com")

    def test_invalid_leading_newline_in_local_part(self):
        with self.assertRaises(
            ValueError,
            msg="The email address contains invalid characters before the "
            "@-sign: \n.",
        ):
            validate_email_address(u"\nmy@example.com")

    def test_invalid_newline_in_local_part(self):
        with self.assertRaises(
            ValueError,
            msg="The email address contains invalid characters before the "
            "@-sign: \n.",
        ):
            validate_email_address(u"m\ny@example.com")

    def test_invalid_newline_after_local_part(self):
        with self.assertRaises(
            ValueError,
            msg="The email address contains invalid characters before the "
            "@-sign: \n.",
        ):
            validate_email_address(u"my\n@example.com")

    def test_invalid_local_part_just_too_long(self):
        with self.assertRaises(
            ValueError,
            msg="The email address is too long before the @-sign "
            "(1 character too many).",
        ):
            validate_email_address(
                u"111111111122222222223333333333"
                u"44444444445555555555666666666677777"
                u"@example.com"
            )

    def test_invalid_local_part_too_long(self):
        with self.assertRaises(
            ValueError,
            msg="The email address is too long before the @-sign "
            "(2 characters too many).",
        ):
            validate_email_address(
                u"111111111122222222223333333333"
                u"444444444455555555556666666666777777"
                u"@example.com"
            )

    def test_invalid_domain_too_long(self):
        with self.assertRaises(
            ValueError, msg="The email address is too long after the @-sign."
        ):
            validate_email_address(
                u"me"
                u"@1111111111222222222233333333334444444444555555555"
                u".6666666666777777777788888888889999999999000000000"
                u".1111111111222222222233333333334444444444555555555"
                u".6666666666777777777788888888889999999999000000000"
                u".111111111122222222223333333333444444444455555555556"
                u".com"
            )

    def test_invalid_too_long(self):
        with self.assertRaises(
            ValueError,
            msg="The email address is too long (2 characters too many).",
        ):
            validate_email_address(
                u"my.long.address"
                u"@1111111111222222222233333333334444444444555555555"
                u".6666666666777777777788888888889999999999000000000"
                u".1111111111222222222233333333334444444444555555555"
                u".6666666666777777777788888888889999999999000000000"
                u".11111111112222222222333333333344444"
                u".info"
            )

    def test_invalid_too_long_after_domain_conversion(self):
        with self.assertRaises(
            ValueError,
            msg="The email address is too long "
            "(when converted to IDNA ASCII).",
        ):
            validate_email_address(
                u"my.long.address"
                u"@λ111111111222222222233333333334444444444555555555"
                u".6666666666777777777788888888889999999999000000000"
                u".1111111111222222222233333333334444444444555555555"
                u".6666666666777777777788888888889999999999000000000"
                u".11111111112222222222333333"
                u".info"
            )

    def test_invalid_too_long_before_domain_conversion(self):
        with self.assertRaises(
            ValueError,
            msg="The email address is too long "
            "(at least 1 character too many).",
        ):
            validate_email_address(
                u"my.long.address"
                u"@λ111111111222222222233333333334444444444555555555"
                u".6666666666777777777788888888889999999999000000000"
                u".1111111111222222222233333333334444444444555555555"
                u".6666666666777777777788888888889999999999000000000"
                u".1111111111222222222233333333334444"
                u".info"
            )

    def test_invalid_too_long_after_local_part_conversion(self):
        with self.assertRaises(
            ValueError,
            msg="The email address is too long (when encoded in bytes).",
        ):
            validate_email_address(
                u"my.λong.address"
                u"@1111111111222222222233333333334444444444555555555"
                u".6666666666777777777788888888889999999999000000000"
                u".1111111111222222222233333333334444444444555555555"
                u".6666666666777777777788888888889999999999000000000"
                u".111111111122222222223333333333444"
                u".info"
            )

    def test_invalid_too_long_before_local_part_conversion(self):
        with self.assertRaises(
            ValueError,
            msg="The email address is too long "
            "(at least 1 character too many).",
        ):
            validate_email_address(
                u"my.λong.address"
                u"@1111111111222222222233333333334444444444555555555"
                u".6666666666777777777788888888889999999999000000000"
                u".1111111111222222222233333333334444444444555555555"
                u".6666666666777777777788888888889999999999000000000"
                u".1111111111222222222233333333334444"
                u".info"
            )
