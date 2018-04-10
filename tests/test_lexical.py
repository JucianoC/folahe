from io import StringIO
from lexical import Lexical, Token


def test_instantiate():
    file_like = StringIO("Hello World!")
    instance = Lexical(file_like)

    assert instance.input_lines == ["Hello World!"]
    assert instance.tokens == []
    assert instance.column_index == 0
    assert instance.line_index == 0

    for token in instance.TABLE_TOKENS.values():
        assert isinstance(token, Token)
