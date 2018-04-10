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
