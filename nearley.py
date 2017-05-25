from re import compile as c
regex = type(c(""))

noop = lambda d, l, fail: d

class Value(object):
    __slots__ = "value"

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return repr(self.value)

class Type(object):
    __slots__ = "type"

    def __init__(self, type):
        self.type = type

    def __str__(self):
        return self.type

    def __repr__(self):
        return repr(self.type)

class Rule(object):
    __slots__ = ("expression", "grammar", "symbols", "process")

    def __init__(self, expression, grammar, symbols, process=noop):
        self.expression = expression
        self.grammar = grammar
        self.symbols = list(map(
            lambda symbol: (
                c(symbol.pattern)
                if isinstance(symbol, regex) else
                symbol
            ),
            symbols
        ))
        self.process = process

    def __str__(self):
        return self.to_string()

    def to_string(self, dot=None):

        def stringify_symbol(symbol):
            symbol_type = type(symbol)
            return (
                repr(symbol)
                if symbol_type == str else
                self.grammar.names[symbol]
                if symbol_type == int else
                symbol.type
                if symbol_type == Type else
                str(symbol)
            )

        return self.grammar.names[self.expression] + " → " + (
            " ".join(map(stringify_symbol, self.symbols))
            if dot is None else
            (
                " ".join(map(stringify_symbol, self.symbols[0:dot])) +
                " ● " +
                " ".join(map(stringify_symbol, self.symbols[dot:]))
            )
        )

class State(object):
    __slots__ = (
        "rule", "dot", "reference", "data", "token", "is_token",
        "left", "right", "wanted_by", "complete"
    )

    def __init__(
        self, rule=None, dot=0, reference=0, wanted_by=[], data=None,
        token=None, is_token=False
    ):
        self.rule, self.dot, self.reference = rule, dot, reference or 0
        self.data, self.wanted_by = data or [], wanted_by
        self.complete = rule and dot == len(rule.symbols)
        self.left = self.right = None
        self.token, self.is_token = token, is_token

    def __str__(self):
        return "{%s}, from: %i" % (
            self.rule.to_string(self.dot), self.reference
        )

    def next(self, child):
        state = State(self.rule, self.dot + 1, self.reference, self.wanted_by)
        state.left = self
        state.right = child
        if state.complete:
            state.data = state.build()
        return state

    def build(self):
        children, node = [], self
        children += [self.right.data]
        node = node.left
        while node.left:
            children += [node.right.data]
            node = node.left
        return children[::-1]

    def finish(self):
        self.data = self.rule.process(self.data, self.reference, Parser.fail)

class Column:
    def __init__(self, grammar, index):
        self.grammar, self.index = grammar, index
        self.states, self.scannable, self.wants, self.completed = [], [], {}, {}

    def process(self):
        states, wants, completed = self.states, self.wants, self.completed
        expression, i = None, -1
        while i < len(states) - 1: # because we push during iteration
            i += 1
            state = states[i]
            if state.complete:
                state.finish()
                if state.data != Parser.fail:
                    for item in state.wanted_by[::-1]:
                        self.complete(item, state)
                    # special-case nullables
                    if state.reference == self.index:
                        expression = state.rule.expression
                        if not expression in completed:
                            completed[expression] = []
                        completed[expression] += [state]
            else:
                expression = state.rule.symbols[state.dot]
                if not isinstance(expression, int):
                    self.scannable += [state]
                    continue
                if expression in wants:
                    wants[expression] += [state]
                    if expression in completed:
                        for complete in completed[expression]:
                            self.complete(state, complete)
                else:
                    wants[expression] = [state]
                    self.predict(expression)

    def predict(self, expression):
        rules = self.grammar.rules[expression] or []
        self.states += [
            State(rule, 0, self.index, self.wants[expression]) for rule in rules
        ]

    def complete(self, left, right):
        if left.rule.symbols[left.dot] == right.rule.expression:
            self.states += [left.next(right)]

class LexerState(object):
    __slots__ = ("line", "column")

    def __init__(self, line, column):
        self.line = line
        self.column = column

class Lexer(object):
    __slots__ = ("buffer", "index", "line", "last_newline")

    def __init__(self):
        self.reset("")

    def reset(self, data, state=None):
        self.buffer = data
        self.index = 0
        self.line = state.line if state else 1
        self.last_newline = -state.column if state else 0

    def next(self):
        if self.index < len(self.buffer):
            character = self.buffer[self.index]
            if character == "\n":
                self.line += 1
                self.last_newline = self.index
            self.index += 1
            return Value(character)

    def save(self):
        return LexerState(self.line, self.index - self.last_newline)

    def format_error(self, token, message):
        buffer = self.buffer
        if isinstance(buffer, str):
            next_newline = buffer.find("\n", self.index);
            if next_newline == -1:
                next_newline = len(buffer)
            return (
                "%s at line %i column %i:\n\n  %s\n  %s^" %
                (
                    message,
                    self.line,
                    self.index - self.last_newline,
                    buffer[self.last_newline:next_newline],
                    " " * (self.index - self.last_newline - 1)
                )
            )
        else:
            return message + " at index " + (self.index - 1)

class Grammar(object):
    __slots__ = ("rules", "names", "lexer")

    def __init__(self, rules=None, names=None, lexer=None):
        self.rules = rules
        self.names = names
        self.lexer = lexer

    def from_compiled(rules, names, lexer=Lexer):
        grammar = Grammar(None, names, lexer)
        grammar.rules = [
            [
                Rule(
                    i,
                    grammar,
                    rule[0],
                    (rule[1] if len(rule) > 1 else noop)
                )
                for rule in rule_set
            ]
            for i, rule_set in zip(range(len(rules)), rules)
        ]
        return grammar

class Parser(object):
    __slots__ = (
        "grammar", "start", "options", "lexer", "lexer_state", "table",
        "current", "tokens", "results"
    )

    fail = {}

    def __init__(self, rules, names=None, lexer=None, options=None):
        grammar = None
        if isinstance(rules, Grammar):
            grammar = self.grammar = rules
            options = names
        elif isinstance(rules, dict):
            grammar = self.grammar = Grammar.from_compiled(
                rules["ParserRules"], rules["Names"], rules["Lexer"]
            )
            options = names
        else:
            grammar = self.grammar = Grammar.from_compiled(rules, names, lexer)
        self.start = grammar.rules[0]
        self.options = {
            "keep_history": False,
            "lexer": grammar.lexer or Lexer()
        }
        if options:
            for key in options:
                self.options[key] = options[key]
        self.lexer, self.lexer_state = self.options["lexer"], None
        column = Column(grammar, 0)
        self.table, self.current, self.tokens = [column], 0, 0
        column.wants[0] = []
        column.predict(0)
        column.process()

    def feed(self, chunk):
        lexer, token, column = self.lexer, None, None
        lexer.reset(chunk, self.lexer_state)
        token = lexer.next()
        while token:
            self.tokens += 1
            column = self.table[self.current]
            if not self.options["keep_history"]:
                self.table[self.current - 1] = None
            n = self.current + 1
            next = Column(self.grammar, n)
            self.table += [next]
            literal = token.value if isinstance(token, Value) else None
            value = token.value if type(lexer) == Lexer else token
            scannable = column.scannable
            for state in scannable:
                expect = state.rule.symbols[state.dot]
                expect_type = type(expect)
                if (
                    expect_type == regex and expect.match(value) or
                    (
                        expect_type == Type and
                        isinstance(token, Type) and
                        expect.type == token.type
                    ) or
                    expect == literal
                ):
                    next_state = state.next(State(
                        data=value, token=token, is_token=True
                    ))
                    next.states += [next_state]
            next.process()
            if not len(next.states):
                print(
                    "%s\nUnexpected %s%s\n" % (
                        self.lexer.format_error(token, "invalid syntax"),
                        (
                            token.type + " token: "
                            if isinstance(token, Type) else
                            ""
                        ),
                        repr(token)
                    )
                )
                __import__("sys").exit()
            if self.options["keep_history"]:
                column.lexer_state = lexer.save()
            self.current += 1
            token = lexer.next()
        if column:
            self.lexer_state = lexer.save()
        self.results = self.finish()
        return self

    def save(self):
        column = self.table[self.current]
        column.lexer_state = self.lexer_state
        return column

    def restore(self, column):
        index = column.index
        self.current = index
        self.table[index] = column
        # self.table.splice(index + 1)
        self.lexer_state = column.lexer_state
        self.results = self.finish()

    def finish(self):
        return ([
            state.data
            for state in self.table[-1].states if
            state.rule in self.start and
            state.complete and
            not state.reference and
            state.data != Parser.fail
        ], self.tokens)
