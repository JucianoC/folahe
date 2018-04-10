import re
from collections import namedtuple


Token = namedtuple("Token", ('id', 'lexogram'))


class Lexical(object):

    TABLE_TOKENS = {
        'ADD': Token(id=0, lexogram="+"),
        'SUB': Token(id=1, lexogram="-"),
        'MUL': Token(id=2, lexogram="*"),
        'POW': Token(id=3, lexogram="**"),
        'ANDBIN': Token(id=4, lexogram="&"),
        'ORBIN': Token(id=5, lexogram="|"),
        'EQUAL': Token(id=6, lexogram="=="),
        'DIFF': Token(id=6, lexogram="!="),
        'DIV': Token(id=8, lexogram="/"),
        'INTDIV': Token(id=9, lexogram="//"),
        'MOD': Token(id=10, lexogram="%"),
        'LEFTBIN': Token(id=11, lexogram="<<"),
        'RIGHTBIN': Token(id=12, lexogram=">>"),
        'LESS': Token(id=13, lexogram="<"),
        'GRETHER': Token(id=14, lexogram=">"),
        'LESSEQUAL': Token(id=15, lexogram="<="),
        'GRETHEREQUAL': Token(id=16, lexogram=">="),
        'AND': Token(id=17, lexogram="and"),
        'OR': Token(id=18, lexogram="or"),
        'NOT': Token(id=19, lexogram="not"),
        'XORBIN': Token(id=20, lexogram="^"),
        'NOTBIN': Token(id=21, lexogram="~"),
        'IF': Token(id=22, lexogram="if"),
        'ELIF': Token(id=23, lexogram="elif"),
        'ELSE': Token(id=24, lexogram="else"),
        'FOR': Token(id=25, lexogram="for"),
        'WHILE': Token(id=26, lexogram="while"),
        'COMMENT': Token(id=27, lexogram="#"),
        'NEWLINE': Token(id=28, lexogram="\n"),
        'CR': Token(id=29, lexogram="\r"),
        'ID': Token(id=30, lexogram=None),
        'COLON': Token(id=31, lexogram=":"),
        'CONSTHEX': Token(id=33, lexogram=None),
        'CONSTOCT': Token(id=34, lexogram=None),
        'CONSTBIN': Token(id=35, lexogram=None),
        'CONSTDEC': Token(id=36, lexogram=None),
        'ATTRIB': Token(id=37, lexogram="="),
        'FALSE': Token(id=38, lexogram="False"),
        'CLASS': Token(id=39, lexogram='class'),
        'FINALLY': Token(id=40, lexogram="finally"),
        'IS': Token(id=41, lexogram="is"),
        'RETURN': Token(id=42, lexogram="return"),
        'NONE': Token(id=43, lexogram="None"),
        'CONTINUE': Token(id=44, lexogram="continue"),
        'LAMBDA': Token(id=45, lexogram='lambda'),
        'TRY': Token(id=46, lexogram='try'),
        'TRUE': Token(id=47, lexogram="True"),
        'DEF': Token(id=48, lexogram='def'),
        'FROM': Token(id=49, lexogram='from'),
        'NONLOCAL': Token(id=50, lexogram='nonlocal'),
        'DEL': Token(id=51, lexogram='del'),
        'GLOBAL': Token(id=52, lexogram='global'),
        'WITH': Token(id=53, lexogram='with'),
        'AS': Token(id=54, lexogram='as'),
        'YIELD': Token(id=55, lexogram='yield'),
        'ASSERT': Token(id=56, lexogram='assert'),
        'IMPORT': Token(id=57, lexogram='import'),
        'PASS': Token(id=58, lexogram='pass'),
        'BREAK': Token(id=59, lexogram='break'),
        'EXCEPT': Token(id=60, lexogram='except'),
        'IN': Token(id=61, lexogram='in'),
        'RAISE': Token(id=62, lexogram='raise'),
        'BACKSLASH': Token(id=63, lexogram='\\'),
        'COMMA': Token(id=64, lexogram=','),
        'SEMICOLON': Token(id=65, lexogram=';'),
        'LEFTPARENTHESIS': Token(id=66, lexogram='('),
        'RIGHTPARENTHESIS': Token(id=67, lexogram=')'),
        'LEFTBRACKET': Token(id=68, lexogram='['),
        'RIGHTBRACKET': Token(id=69, lexogram=']'),
        'LEFTBRACE': Token(id=70, lexogram='{'),
        'RIGHTBRACE': Token(id=71, lexogram='}'),
        'AT': Token(id=72, lexogram="@"),
        'ARROW': Token(id=73, lexogram='->'),
        'ATTRIBSUM': Token(id=73, lexogram='+='),
        'ATTRIBSUB': Token(id=74, lexogram='-='),
        'ATTRIBMUL': Token(id=75, lexogram='*='),
        'ATTRIBDIV': Token(id=76, lexogram='/='),
        'ATTRIBDIVINT': Token(id=77, lexogram='//='),
        'ATTRIBMOD': Token(id=78, lexogram='%='),
        'ATTRIBMTXMUL': Token(id=79, lexogram='@='),
        'ATTRIBANDBIN': Token(id=80, lexogram='&='),
        'ATTRIBORBIN': Token(id=81, lexogram='|='),
        'ATTRIBXORBIN': Token(id=82, lexogram='^='),
        'ATTRIBRIGHTBIN': Token(id=84, lexogram='>>='),
        'ATTRIBLEFTBIN': Token(id=85, lexogram='<<='),
        'ATTRIBPOW': Token(id=86, lexogram='**='),
        'QUOTE': Token(id=87, lexogram='\''),
        'DQUOTE': Token(id=88, lexogram='\"'),
        'TRIPLEQUOTE': Token(id=89, lexogram='\'\'\''),
        'TRIPLEDQUOTE': Token(id=90, lexogram='\"\"\"'),
        'CONSTFLOAT': Token(id=91, lexogram=None),
        'STRING': Token(id=92, lexogram=None),
        'INDENT': Token(id=93, lexogram=None),
        'DEDENT': Token(id=94, lexogram=None),
        'ENDMARKER': Token(id=95, lexogram=None),
        'DIFF2': Token(id=96, lexogram="<>"),
        'AWAIT': Token(id=97, lexogram="await"),
        'DOT': Token(id=98, lexogram="."),
        'ENDPRODUCTION': Token(id=99, lexogram='$'),
    }

    def __init__(self, input_file):
        if not hasattr(input_file, 'read'):
            raise TypeError("input_file must be a file-like object")
        self.input_lines = input_file.readlines()
        self.tokens = []
        self.column_index = 0
        self.line_index = 0
        self.string_flag = False
        self.string_context = ''

        # this var store the current identation level (in number of chars)
        self.context_stack = [0]

    def add_token(self, token, column):
        if not self.tokens and token.id == Lexical.TABLE_TOKENS['INDENT'].id:
            raise IndentationError

        if token.lexogram == '\n' and self.tokens[-1].id not in (31, 93, 94):
            # at the end of each statement are autmatic added a token ';',
            # this facilitate the grammar construction
            self.tokens.append({
                'token': next(filter(
                                     lambda val: val.lexogram == ';',
                                     Lexical.TABLE_TOKENS.values())).id,
                'lexogram': ';',
                'line': self.line_index,
                'column': self.column_index,
            })

        self.tokens.append({
            'token': token.id,
            'lexogram': token.lexogram,
            'line': self.line_index,
            'column': self.column_index
        })

    def manage_context(self, line):
        # here the identation is recognized
        context_lexogram = ''
        while re.match(r'( |\t)', line[self.column_index]):
            context_lexogram += line[self.column_index]
            self.column_index += 1

        # by default tabs are considered eight spaces
        context_lexogram = context_lexogram.replace('\t', ' ' * 8)

        number_characters = len(context_lexogram)
        if number_characters == self.context_stack[-1]:
            # same identation level just pass
            pass
        elif number_characters > self.context_stack[-1]:
            # identation level increase
            self.context_stack.append(number_characters)
            self.add_token(Lexical.TABLE_TOKENS['INDENT'], column=0)
        elif number_characters < self.context_stack[-1]:
            # identation level decreased
            if number_characters not in self.context_stack:
                # if the current number of chars isn't on stack,
                # this means that a wrong identation are found
                raise IndentationError

            while number_characters != self.context_stack[-1]:
                # while an identation level equal to the current
                # number of charactres are found, dedent tokens are
                # added.
                context_stack.pop()
                self.add_token(
                    Lexical.TABLE_TOKENS['DEDENT'], column=0)

    def is_blank_line(self, line):
        cleaned_line = line.replace('\n', '').replace('\r', '')
        cleaned_line = cleaned_line.replace(' ', '').replace('\t', '')

        if not self.string_flag and not cleaned_line:
            self.line_index += 1
            return True
        return False

    def possible_tokens_for_char(self, char):
        """
            Return a list of tokens with starts with this char
        """
        return [
            token for token in Lexical.TABLE_TOKENS.values()
            if token.lexogram is not None and token.lexogram.startswith(char)
        ]

    def discover_const_or_identifier(self, char, line):
        """
            This method discover if the string analyzed is an constant or an
            indentifier and return the correct token object
        """
        if char == '0':
            # if this token starts with zero, means that it's a const zero
            # or a number in hex/oct/bin notation, or an zero in scientific
            # notation (eg: 0e123)
            if self.column_index + 1 >= len(line):
                return self.const_zero()
            elif re.match(r'(x|o|b|X|O|B)', line[self.column_index + 1]):
                return self.const_hex_oct_bin(line)
            elif re.match(r'(e|E|\.)', line[self.column_index + 1]):
                return self.const_float(line)
            else:
                return self.const_zero()
        elif char == '.':
            return self.const_float(line)
        elif re.match(r'[0-9]', char):
            return self.const_decimal(line)
        elif re.match(r'(_|[A-Z]|[a-z])', char):
            return self.identifier(line)

    def const_decimal(self, line):
        lexogram = ''
        column = self.column_index

        while column < len(line) and re.match(r'([0-9]|_)', line[column]):
            lexogram += line[column]
            column += 1
        if column < len(line) and re.match(r'(\.|e|E)', line[column]):
            return self.const_float(line)

        self.column_index = column
        const_dec = Lexical.TABLE_TOKENS['CONSTDEC']
        return Token(id=const_dec.id, lexogram=lexogram)

    def identifier(self, line):
        column = self.column_index
        lexogram = ''

        while (
               column < len(line) and
               re.match(r'([0-9]|_|[A-Z]|[a-z])', line[column])):
            lexogram += line[column]
            column += 1

        self.column_index = column
        token_id = Lexical.TABLE_TOKENS['ID']
        return Token(id=token_id.id, lexogram=lexogram)

    def const_hex_oct_bin(self, line):
        self.column_index += 1
        mods = {
            'x': {
                'token': Lexical.TABLE_TOKENS['CONSTHEX'],
                'pattern': r'([0-9]|[a-f]|[A-F])'},
            'o': {
                'token': Lexical.TABLE_TOKENS['CONSTOCT'],
                'pattern': r'[0-7]'},
            'b': {
                'token': Lexical.TABLE_TOKENS['CONSTBIN'],
                'pattern': r'[0-1]'},
        }

        char = line[self.column_index]
        token_type = mods[char.lower()]
        lexogram = '0{}'.format(char)
        column = self.column_index + 1

        while (
               column < len(line) and
               re.match(token_type['pattern'], line[column])):
            lexogram += line[column]
            column += 1

        self.column_index = column
        token = Token(id=token_type['token'].id, lexogram=lexogram)
        return token

    def const_float(self, line):
        column = self.column_index
        lexogram = ''

        if re.match(r'[0-9]', line[column]):
            while column < len(line) and re.match(r'[0-9]', line[column]):
                lexogram += line[column]
                column += 1

        elif line[column] == '.':
            pass
        else:
            raise SyntaxError("Token {} ({}:{})".format(
                line[column], self.line_index, self.column_index))

        if column < len(line) and '.' == line[column]:
            lexogram += '.'
            column += 1
            while column < len(line) and re.match(r'[0-9]', line[column]):
                lexogram += line[column]
                column += 1
        elif column < len(line) and re.match(r'(e|E)', line[column]):
            pass
        else:
            raise SyntaxError("Token {} ({}:{})".format(
                line[column], self.line_index, self.column_index))

        if column < len(line) and re.match(r'(e|E)', line[column]):
            lexogram += line[column]
            column += 1
            if column < len(line) and re.match(r'(\+|\-)', line[column]):
                lexogram += line[column]
                column += 1
            while column < len(line) and re.match(r'[0-9]', line[column]):
                lexogram += line[column]
                column += 1

        self.column_index = column
        const_float = Lexical.TABLE_TOKENS['CONSTFLOAT']
        return Token(id=const_float.id, lexogram=lexogram)

    def const_zero(self):
        self.column_index += 1
        const_dec = Lexical.TABLE_TOKENS['CONSTDEC']
        token = Token(id=const_dec.id, lexogram='0')
        return token

    def process_line(self, line):
        while self.column_index < len(line):
            start_column = self.column_index
            char = line[self.column_index]

            if char in (' ', '\t'):
                if self.string_flag:
                    self.string_context += char
                self.column_index += 1
                continue

            possible_tokens = self.possible_tokens_for_char(char)

            try:
                dot_token = next(filter(
                    lambda token: token.lexogram == '.', possible_tokens))

                if re.match(r'\d', line[self.column_index + 1]):
                    # if the next element is an number this means that this dot
                    # is part of an float number
                    possible_tokens.remove(dot_token)
            except StopIteration:
                pass

            chosed_token = None
            if not possible_tokens:
                # if has no possible_token this means that the token is an
                # constant of an identifier
                chosed_token = self.discover_const_or_identifier(char, line)

            if chosed_token:
                self.add_token(chosed_token, column=start_column)

            # TODO develop other rules

    def decode(self):
        for line in self.input_lines:
            self.column_index = 0

            if self.is_blank_line(line):
                # blank line, just ignore it
                continue

            if not self.string_flag:
                self.manage_context(line)

            self.process_line(line)
