from datetime import date, datetime

import validation


def _print_message(snippet):
    context = {}
    context.update(validation.__dict__)
    context.update(dict(datetime=datetime, date=date))

    try:
        exec(snippet, context)
    except Exception as exc:
        print(exc)
    else:
        raise Exception()


print('')
_print_message('validate_int(None)')
_print_message('validate_int("string")')
_print_message('validate_int(-1, min_value=0)')
_print_message('validate_int(9001, max_value=9000)')

print('')
_print_message('validate_bool(None)')
_print_message('validate_bool("true")')

print('')
_print_message('validate_text(None)')
_print_message('validate_text(b"bytes")')
_print_message('validate_text(u"12", min_length=3)')
_print_message('validate_text(u"1234", max_length=3)')
_print_message('validate_text(u"string", pattern="STRING")')

print('')
_print_message('validate_bytes(None)')
_print_message('validate_bytes(u"unicode")')
_print_message('validate_bytes(b"12", min_length=3)')
_print_message('validate_bytes(b"1234", max_length=3)')

print('')
_print_message('validate_date(None)')
_print_message('validate_date(datetime.now())')
_print_message('validate_date("1970-01-01")')

print('')
_print_message('validate_datetime(None)')
_print_message('validate_datetime(date.today())')
_print_message('validate_datetime(datetime.now())')

print('')
_print_message('validate_list(None)')
_print_message('validate_list(set())')
_print_message('validate_list([], min_length=2)')
_print_message('validate_list([1, 2, 3], max_length=2)')
_print_message('validate_list([1, "2", 3], validator=validate_int())')

print('')
_print_message('validate_set(None)')
_print_message('validate_set([])')
_print_message('validate_set({1}, min_length=2)')
_print_message('validate_set({1, 2, 3}, max_length=2)')
_print_message('validate_set({1, "2", 3}, validator=validate_int())')

print('')
_print_message('validate_mapping(None)')
_print_message('validate_mapping([])')
_print_message('validate_mapping({"1": 1}, key_validator=validate_int())')
_print_message('validate_mapping({"2": "2"}, value_validator=validate_int())')

print('')
_print_message('validate_structure(None)')
_print_message('validate_structure([])')
_print_message('validate_structure({}, schema={"key": lambda v: None})')
_print_message('validate_structure({"extra": "value"}, schema={})')
_print_message(
    'validate_structure({"key": "1"}, schema={"key": validate_int()})',
)
