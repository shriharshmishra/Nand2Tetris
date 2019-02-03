from JackTokenizer import JackTokenizer


class CompilationEngine:

    def __init__(self, path, filename):
        self._jt = JackTokenizer(path, filename)
        self._opfilename = filename
        self._tags = []
        self.compileClass()
        #print(*self._tags)


    def exportXML(self):
        with open(self._opfilename, 'w') as f:
            f.writelines(self._tags)

    def compileClass(self):
        self.start_non_terminal_tag('class', addToTags=True)
        self.move_to_next_token()
        self.eat_token('class', addToTags=True)
        self.move_to_next_token()
        self.eat_token_type('IDENTIFIER', addToTags=True)
        self.move_to_next_token()
        self.eat_token('{', addToTags=True)

        class_var_dec = self.compile_class_var_dec()
        while class_var_dec:
            self._tags += class_var_dec
            class_var_dec = self.compile_class_var_dec()
        else:
            subroutine_dec = self.compile_subroutine_dec()
            while subroutine_dec:
                self._tags += subroutine_dec
                subroutine_dec = self.compile_subroutine_dec()

        self.eat_token('}', addToTags=True)
        self.end_non_terminal_tag('class', addToTags=True)

    def compile_class_var_dec(self):
        tags = []
        tags.append(self.start_non_terminal_tag('classVarDec'))
        tags.append(self.eat_token('static') or self.eat_token('field'))
        if False in tags:
            return False
        tags.append(self.compile_type())
        tags.append(self.eat_token_type(self.get_token_type('varName')))
        collect = self.eat_token(',')
        while collect:
            tags.append(collect)
            self.move_to_next_token()
            tags.append(self.eat_token_type(self.get_token_type('varName')))
            self.move_to_next_token()
            collect = self.eat_token(',')
        else:
            tags.append(self.eat_token(';'))

        tags.append(self.end_non_terminal_tag('classVarDec'))

        return self.validate_tags(tags)


    def compile_type(self):
        return self.eat_token('int') or self.eat_token('char') or self.eat_token('boolean') or self.eat_token_type(
            self.get_token_type('className'))

    def compile_subroutine_dec(self):
        tags = []
        tags.append(self.start_non_terminal_tag('subroutineDec'))

        self.move_to_next_token()
        tags.append(self.eat_token('constructor') or self.eat_token('function') or self.eat_token('method'))

        if False in tags:
            return False

        self.move_to_next_token()
        tags.append(self.eat_token('void') or self.compile_type())

        self.move_to_next_token()
        tags.append(self.eat_token_type(self.get_token_type('subroutineName')))

        self.move_to_next_token()
        tags.append(self.eat_token('('))

        parameter_list_tags = self.compileParameterList()
        if parameter_list_tags:
            tags += parameter_list_tags

        self.move_to_next_token()
        tags.append(self.eat_token(')'))

        subroutine_body_tags = self.compile_subroutine_body()
        if subroutine_body_tags:
            tags += subroutine_body_tags

        tags.append(self.end_non_terminal_tag('subroutineDec'))

        return self.validate_tags(tags)

    def compileParameterList(self):

        self.move_to_next_token()
        type = self.compile_type()

        if not type:
            tags = [self.start_non_terminal_tag('parameterList'), self.end_non_terminal_tag('parameterList')]
            return self.validate_tags(tags)
        else:
            tags = [self.start_non_terminal_tag('parameterList'), type]

            self.move_to_next_token()
            tags.append(self.eat_token_type(self.get_token_type('varName')))

            self.move_to_next_token()
            is_comma = self.eat_token(',')

            while is_comma:
                tags.append(is_comma)

                self.move_to_next_token()
                tags.append(self.compile_type())

                self.move_to_next_token()
                tags.append(self.eat_token_type(self.get_token_type('varName')))

                self.move_to_next_token()
                is_comma = self.eat_token(',')

            tags.append(self.end_non_terminal_tag('parameterList'))
            return self.validate_tags(tags)

    def compile_subroutine_body(self):
        tags = [self.start_non_terminal_tag('subroutineBody')]

        self.move_to_next_token()
        tags.append(self.eat_token('{'))

        var_dec_tags = self.compile_var_dec()
        while var_dec_tags:
            tags += var_dec_tags
            var_dec_tags = self.compile_var_dec()

        statements_tags = self.compile_statements()
        if statements_tags:
            tags += statements_tags

        self.move_to_next_token()
        tags.append(self.eat_token('}'))

        tags.append(self.end_non_terminal_tag('subroutineBody'))
        return self.validate_tags(tags)

    def compile_var_dec(self):
        tags = [self.start_non_terminal_tag('varDec')]

        self.move_to_next_token()
        tags.append(self.eat_token('var'))

        self.move_to_next_token()
        tags.append(self.compile_type())

        self.move_to_next_token()
        tags.append(self.eat_token_type(self.get_token_type('varName')))

        self.move_to_next_token()
        is_comma = self.eat_token(',')
        while is_comma:
            tags.append(is_comma)

            self.move_to_next_token()
            tags.append(self.eat_token_type(self.get_token_type('varName')))

            self.move_to_next_token()
            is_comma = self.eat_token(',')
        else:
            tags.append(self.eat_token(';'))

        tags.append(self.end_non_terminal_tag('varDec'))
        return self.validate_tags(tags)

    def compile_statements(self):
        tags = [self.start_non_terminal_tag('statements')]

        statement = self.compile_statement()
        while statement:
            tags += statement
            statement = self.compile_statement()

        tags.append(self.end_non_terminal_tag('statements'))

        return self.validate_tags(tags)

    def compile_statement(self):
        return (self.compile_let_statement()
                or self.compile_if_statement()
                or self.compile_while_statement()
                or self.compile_do_statement()
                or self.compile_return_statement())

    def compile_let_statement(self):
        tags = [self.start_non_terminal_tag('letStatement')]
        self.move_to_next_token()
        tags.append(self.eat_token('let'))
        if False in tags:
            return False
        self.move_to_next_token()
        tags.append(self.eat_token_type(self.get_token_type('varName')))

        self.move_to_next_token()
        bracket = self.eat_token('[')
        if bracket:
            tags.append(bracket)
            tags += self.compile_expression()
            tags.append(self.eat_token(']'))

        self.move_to_next_token()
        tags.append(self.eat_token('='))

        tags += self.compile_expression()

        self.move_to_next_token()
        tags.append(self.eat_token(';'))

        tags.append(self.end_non_terminal_tag('letStatement'))
        return self.validate_tags(tags)

    def compile_if_statement(self):
        tags = [self.start_non_terminal_tag('ifStatement')]

        self.move_to_next_token()
        tags.append(self.eat_token('if'))
        if False in tags:
            return False

        self.move_to_next_token()
        tags.append(self.eat_token('('))
        tags += self.compile_expression()

        self.move_to_next_token()
        tags.append(self.eat_token(')'))

        self.move_to_next_token()
        tags.append(self.eat_token('{'))

        tags += self.compile_statements()

        self.move_to_next_token()
        tags.append(self.eat_token('}'))

        else_tag = self.eat_token('else')
        if else_tag:
            tags.append(else_tag)
            self.move_to_next_token()
            tags.append(self.eat_token('{'))
            tags += self.compile_statements()
            self.move_to_next_token()
            tags.append(self.eat_token('}'))

        tags.append(self.end_non_terminal_tag('ifStatement'))
        return self.validate_tags(tags)

    def compile_while_statement(self):
        tags = [self.eat_token('while'), self.eat_token('(')]
        if False in tags:
            return False
        tags += self.compile_expression()
        tags.append(self.eat_token(')'))
        tags.append(self.eat_token('{'))
        tags += self.compile_statements()
        tags.append(self.eat_token('}'))
        tags = self.add_non_terminal_tags('whileStatement', tags)
        return self.validate_tags(tags)

    def compile_do_statement(self):
        tags = [self.eat_token('do'), self.eat_token_type(self.get_token_type('subroutineName'))]
        if False in tags:
            return False
        paren_tag = self.eat_token('(')
        if paren_tag:
            tags.append(paren_tag)
            tags += self.compile_expression_list()
            tags.append(self.eat_token(')'))
        else:
            tags.append(self.eat_token('.'))
            tags.append(self.eat_token_type(self.get_token_type('subroutineName')))
            tags.append(self.eat_token('('))
            tags += self.compile_expression_list()
            tags.append(self.eat_token(')'))

        tags.append(self.eat_token(';'))
        tags = self.add_non_terminal_tags('doStatement', tags)
        return self.validate_tags(tags)

    def compile_return_statement(self):
        tags = [self.eat_token('return')]
        if False in tags:
            return False
        expression_tags = self.compile_expression()
        if expression_tags:
            tags += expression_tags
        tags.append(self.eat_token(';'))
        tags = self.add_non_terminal_tags('returnStatement', tags)
        return self.validate_tags(tags)

    def compile_expression(self):
        tags = [self.start_non_terminal_tag('expression')]

        term_tags = self.compile_term()
        if term_tags:
            tags += term_tags
        else:
            return False

        self.move_to_next_token()
        while self._jt.token in ('+', '-', '*', '/', '&amp;', '|', '&lt;' , '&gt;', '='):
            tags.append(self.eat_token_type('SYMBOL'))
            tags += self.compile_term()
            self.move_to_next_token()

        tags.append(self.end_non_terminal_tag('expression'))

        return self.validate_tags(tags)

    def compile_term(self):
        tags = []

        self.move_to_next_token()
        constant = (self.eat_token_type(self.get_token_type('integerConstant'))
                    or self.eat_token_type(self.get_token_type('stringConstant')))

        if not constant and self._jt.token in ('this', 'null', 'true', 'false'):
            constant = self.eat_token_type('KEYWORD')

        if not constant:
            identifier = self.eat_token_type('IDENTIFIER')
            if identifier:
                self.move_to_next_token() # checking the next token
                if self._jt.token == '[': # is it an array invocation?
                    tags.append(identifier)
                    tags.append(self.eat_token('['))
                    tags += self.compile_expression()
                    self.move_to_next_token()
                    tags.append(self.eat_token(']'))
                elif self._jt.token in ('.', '('): # is it a subroutine call?
                    tags.append(identifier)
                    if self._jt.token == '(': # its a subroutine call within the Jack class
                        tags.append(self.eat_token('('))
                        tags += self.compile_expression_list()
                        self.move_to_next_token()
                        self.eat_token(')')
                    else: #its a subroutine call outside this Jack class
                        tags.append(self.eat_token('.'))
                        self.move_to_next_token()
                        tags.append(self.eat_token_type(self.get_token_type('subroutineName')))
                        self.move_to_next_token()
                        tags.append(self.eat_token('('))
                        tags += self.compile_expression_list()
                        self.move_to_next_token()
                        tags.append(self.eat_token(')'))
                else:
                    tags.append(identifier) # just varName is given
            elif self._jt.tokenType == 'SYMBOL':
                if self._jt.token == '(':
                    tags.append(self.eat_token('('))
                    tags += self.compile_expression()
                    tags.append(self.eat_token(')'))
                elif self._jt.token in ('~', '-'):
                    tags.append(self.eat_token('~') or self.eat_token('-'))
                    tags += self.compile_term()
        else:
            tags.append(constant)

        if len(tags) > 0:
            tags = self.add_non_terminal_tags('term', tags)
            return self.validate_tags(tags)
        else:
            return False

    def compile_expression_list(self):
        tags = [self.start_non_terminal_tag('expressionList')]

        expression_tags = self.compile_expression()
        if expression_tags:
            tags += expression_tags

        self.move_to_next_token()
        is_comma = self.eat_token(',')
        while is_comma:
            tags.append(is_comma)
            self.move_to_next_token()
            expression = self.compile_expression()
            if expression:
                tags += expression
            is_comma = self.eat_token(',')

        tags.append(self.end_non_terminal_tag('expressionList'))
        return self.validate_tags(tags)


    GRAMMAR_KEYWORD = {
        ('varName', 'className', 'subroutineName'): 'IDENTIFIER',
        ('integerConstant'): 'INT_CONST',
        ('stringConstant') : 'STRING_CONST'
    }

    def get_token_type(self, token):
        for t in self.GRAMMAR_KEYWORD:
            if token in t:
                return self.GRAMMAR_KEYWORD[t]
        else:
            raise Exception(token + ' not found in grammar')

    def eat_token(self, token, addToTags=False):
        self.move_to_next_token()
        if self._jt.token == token:
            self._jt.tokenConsumed = True

            xmltag = self.xmltag()
            if addToTags:
                self._tags.append(xmltag)
            return xmltag
        else:
            return False

    def eat_token_type(self, tokenType, addToTags=False):
        self.move_to_next_token()
        if self._jt.tokenType == tokenType:
            self._jt.tokenConsumed = True
            xmltag = self.xmltag()
            if addToTags:
                self._tags.append(xmltag)
            return xmltag
        else:
            return False

    def move_to_next_token(self):
        if self._jt.hasMoreTokens():
            self._jt.advance();

    def xmltag(self):
        type_ = self._jt.tokenTypeXmlTags[self._jt.tokenType]
        return '<' + type_ +'> ' + self._jt.token +' </' + type_ + '>\n'

    def add_non_terminal_tags(self, name, tags):
        return [self.start_non_terminal_tag(name)] + tags + [self.end_non_terminal_tag(name)]

    def start_non_terminal_tag(self, tag, addToTags=False):
        tag_n_ = '<' + tag + '>\n'
        if addToTags:
            self._tags.append(tag_n_)
        return tag_n_

    def end_non_terminal_tag(self, tag, addToTags=False):
        tag_n_ = '</' + tag + '>\n'
        if addToTags:
            self._tags.append(tag_n_)
        return tag_n_

    def validate_tags(self, tags):
        if False not in tags:
            return tags
        else:
            return False


if __name__ == "__main__":
    # CompilationEngine('ExpressionLessSquare/Main.jack', 'CompileOutput.xml').exportXML()
    # CompilationEngine('ExpressionLessSquare/Square.jack', 'CompileOutput.xml').exportXML()
    # CompilationEngine('ExpressionLessSquare/SquareGame.jack', 'CompileOutput.xml').exportXML()
    # CompilationEngine('Square/Square.jack', 'CompileOutput.xml').exportXML()
    CompilationEngine('Square/SquareGame.jack', 'CompileOutput.xml').exportXML()
