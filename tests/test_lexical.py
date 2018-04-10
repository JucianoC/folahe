from io import StringIO
import pytest

from lexical import Lexical, Token


def test_instantiate():
    file_like = StringIO("Hello World!")
    instance = Lexical(file_like)

    assert instance.input_lines == ["Hello World!"]
    assert instance.tokens == []
    assert instance.context_stack == [0]
    assert instance.column_index == 0
    assert instance.line_index == 0
    assert not instance.string_flag

    for token in instance.TABLE_TOKENS.values():
        assert isinstance(token, Token)


def test_file_starting_with_indentation():
    wrong_file_like = StringIO('    variable = 2.0')
    instance = Lexical(wrong_file_like)
    with pytest.raises(IndentationError) as error:
        instance.decode()


def test_possible_tokens_for_char():
    instance = Lexical(StringIO())

    lexograms_for_plus = tuple([
        token.lexogram for token in instance.possible_tokens_for_char('+')])

    assert lexograms_for_plus == ('+', '+=')

    lexograms_for_o = tuple([
        token.lexogram for token in instance.possible_tokens_for_char('o')])

    assert lexograms_for_o == ('or', )


def test_recognize_const_zero():
    instance = Lexical(StringIO("0"))
    instance.decode()

    tokens = instance.tokens
    const_dec = Lexical.TABLE_TOKENS['CONSTDEC']

    assert len(tokens) == 1
    assert tokens[0]['token'] == const_dec.id
    assert tokens[0]['lexogram'] == '0'


def test_recognize_const_decimal():
    instance = Lexical(StringIO("123456"))
    instance.decode()

    tokens = instance.tokens
    const_dec = Lexical.TABLE_TOKENS['CONSTDEC']

    assert len(tokens) == 1
    assert tokens[0]['token'] == const_dec.id
    assert tokens[0]['lexogram'] == '123456'


def test_recognize_const_float():
    instance = Lexical(StringIO("123.456"))
    instance.decode()

    tokens = instance.tokens
    const_dec = Lexical.TABLE_TOKENS['CONSTFLOAT']

    assert len(tokens) == 1
    assert tokens[0]['token'] == const_dec.id
    assert tokens[0]['lexogram'] == '123.456'


def test_recognize_const_float_starting_with_dot():
    instance = Lexical(StringIO(".123456"))
    instance.decode()

    tokens = instance.tokens
    const_dec = Lexical.TABLE_TOKENS['CONSTFLOAT']

    assert len(tokens) == 1
    assert tokens[0]['token'] == const_dec.id
    assert tokens[0]['lexogram'] == '.123456'


def test_recognize_const_float_starting_with_zero():
    instance = Lexical(StringIO("0.123456"))
    instance.decode()

    tokens = instance.tokens
    const_dec = Lexical.TABLE_TOKENS['CONSTFLOAT']

    assert len(tokens) == 1
    assert tokens[0]['token'] == const_dec.id
    assert tokens[0]['lexogram'] == '0.123456'


def test_recognize_const_float_with_scientifc_notation():
    instance = Lexical(StringIO("10e123456"))
    instance.decode()

    tokens = instance.tokens
    const_dec = Lexical.TABLE_TOKENS['CONSTFLOAT']

    assert len(tokens) == 1
    assert tokens[0]['token'] == const_dec.id
    assert tokens[0]['lexogram'] == '10e123456'
