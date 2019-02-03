import re


class JackTokenizer:

    tokens = {'keyword' : lambda token: token in  ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char',
                           'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return'],
              'symbol' : lambda token: token in ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~'],
              'intConst' : lambda token: bool(re.match('\d', token)),
              'stringConst': lambda token:  bool(re.search('^"$', token)),
              'identifier': lambda  token: bool(re.search('^[_]|[a-zA-Z]{1}[_0-9a-zA-Z]*$', token)) }

    tokenTypeXmlTags = {'IDENTIFIER': 'identifier', 'KEYWORD' : 'keyword', 'STRING_CONST' : 'stringConstant',
                        "INT_CONST": "integerConstant", "SYMBOL" : "symbol"}

    symbol_escape_dict = {'<' : '&lt;', '>' : '&gt;', '&' : '&amp;'}

    def __init__(self, path, filename):
        self._path = path
        self._sourceLines  = self._readJackFile(path)
        self._source = "".join(self._sourceLines)
        self._loc = 0
        self._tokenstart = 0
        self._currentToken = ''
        self._outputFileName = filename + '.xml'
        self.tokenConsumed = True

    def _readJackFile(self, path):
        with open(path, 'r') as f:
            lines = [line.strip() for line in f]
            codelines = [line for line in lines
                            if not line.startswith("//")
                            if not line.startswith("/*")
                            if not line.startswith("*")
                            if line != ''
                            if not line.startswith("*/")]

            codelines = [self.remove_comment(line) for line in codelines]
            return codelines

    def remove_comment(self, line, startingAt=0, comment='//'):
        updated_line = line

        for comment in ('/*', '//'):
            try :
                idx_slashes = updated_line.index(comment, startingAt)
                linebeforeslashes = updated_line[:idx_slashes]
                quotecount = linebeforeslashes.count('"')
                if quotecount%2 == 0:
                    updated_line = linebeforeslashes
                else:
                    updated_line  = self.remove_comment(updated_line, idx_slashes)
            except ValueError:
                pass

        return updated_line



    def hasMoreTokens(self):
        return self._loc < len(self._source)

    def advance(self):
        """Advances tokenizer to next token"""

        if not self.tokenConsumed:
            return

        self._currentToken = ''
        self.tokenType = ''
        self.token = ''
        tokenFound = False


        # if current token is an int, continue until the new char is not int, finalize token and set loc appropriately
        # if current token is empty and current char is ", proceed until next " is found, return token as StringConst
        #   increment loc appropriately.
        # check if current char is symbol
        #   if yes, finalize current token if it is not empty. don't increment loc
        #   if yes, and current token is empty, return symbol and increment loc
        #   if no, add to current token string and proceed to next step, increment loc
        # check if current token is keyword, if yes proceed, inc loc and return token

        while not tokenFound  :
            currentChar = self._source[self._loc]

            if self._currentToken == '':

                intCheck = self.tokens['intConst']
                strCheck = self.tokens['stringConst']

                if intCheck(currentChar):
                    self.tokenType = "INT_CONST"
                    self._currentToken += currentChar
                    self._loc += 1

                    testIntRange = lambda i : int(i) in range(0, 32768)

                    while self._loc < len(self._source):
                        currentChar = self._source[self._loc]

                        if intCheck(currentChar) and testIntRange(self._currentToken  + currentChar) :
                            self._collectChar(currentChar)
                        else :
                            tokenFound = True
                            break


                elif strCheck(currentChar):
                    self.tokenType = "STRING_CONST"
                    self._loc += 1 # skip the startig " character
                    while self._loc < len(self._source):
                        currentChar = self._source[self._loc]
                        if not strCheck(currentChar) :
                            self._collectChar(currentChar, False)
                        else :
                            tokenFound = True
                            self._loc += 1 # skip the ending " character
                            break

                elif self.tokens['symbol'](currentChar):
                    tokenFound = True
                    self.tokenType = "SYMBOL"
                    if currentChar in self.symbol_escape_dict:
                        currentChar = self.symbol_escape_dict[currentChar]

                    self._collectChar(currentChar)

                else:
                    self._collectChar(currentChar)

            else :
                if self.tokens['keyword'](self._currentToken + currentChar):
                    tokenFound = True
                    self.tokenType = "KEYWORD"
                    self._collectChar(currentChar)
                elif self.tokens['symbol'](currentChar) | (currentChar == ' '):
                    tokenFound = True
                    self.tokenType = 'IDENTIFIER'
                else:
                    self._collectChar(currentChar)

        if tokenFound:
            self.token = self._currentToken
            self.tokenConsumed = False

    def printTokens(self):
        while(self.hasMoreTokens()):
            self.advance()
            #print(f'Token Type - {self.token} -> Token = {self.tokenType}')


    def exportXML(self):
        tags = ['<tokens>\n']
        while(self.hasMoreTokens()):
            self.advance()
            type_ = self.tokenTypeXmlTags[self.tokenType]
            #tags.append(f'<{type_}> {self.token} </{type_}>\n')
            self.tokenConsumed = True

        tags.append('</tokens>')
        print(*tags)
        with open(self._outputFileName, 'w') as f:
            f.writelines(tags)


    def _collectChar(self, currentChar, dontStrip=True):
        """Adds current character to token and increments loc. For String Constants white space is preserved by setting
        dontStrip parameter as False, default value is set to True for everything else"""
        if dontStrip:
            self._currentToken += currentChar.strip()
        else:
            self._currentToken += currentChar
        self._loc += 1


#def remove_comment(line, startingAt=0):
#    updated_line = line
#
#    for comment in ('/*', '//'):
#        try :
#            idx_slashes = updated_line.index(comment, startingAt)
#            linebeforeslashes = updated_line[:idx_slashes]
#            quotecount = linebeforeslashes.count('"')
#            if quotecount%2 == 0:
#                updated_line = linebeforeslashes
#            else:
#                updated_line  = remove_comment(updated_line, idx_slashes)
#        except ValueError:
#            pass
#
#    return updated_line
#JackTokenizer('ArrayTest/Main.jack', "Output").exportXML()
if __name__ == '__main__':
    # JackTokenizer('ExpressionLessSquare/Main.jack', "Output").exportXML()
    JackTokenizer('ExpressionLessSquare/Square.jack', "Output").exportXML()
