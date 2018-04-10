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

    def decode(self):
        string_flag = None
        string_context = ''
        context_stack = [0]

        for line in self.input_lines:
            self.column_index = 0
            cleaned_line = line.replace('\n', '').replace('\r', '')
            cleaned_line = cleaned_line.replace(' ', '').replace('\t', '')

            if not string_flag and not cleaned_line:
                # blank line, just ignore it
                self.line_index += 1
                continue

            if not string_flag:
                context_lexogram = ''
                while re.match(r'( |\t)', line[self.column_index]):
                    context_lexogram += line[self.column_index]
                    self.column_index += 1

                context_lexogram = context_lexogram.replace('\t', ' ' * 8)
