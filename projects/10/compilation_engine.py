import jack_tokenizer

class CompileError(Exception):
    pass

class CompilationEngine():
    def __init__(self, tokenizer: jack_tokenizer.JackTokenizer, xmlf):
        self.jt = tokenizer
        self.xmlf = xmlf
        try:
            self.advance()
            self.compile_class()
        except CompileError as e:
            print(e)

    def advance(self):
        """ tokenizerのhas_more_tokensとadvanceをセットにしたメソッド """

        if self.jt.has_more_tokens():
            self.jt.advance()
            return None
        else:
            pass

    def write_token_xml(self):
        """ xmlファイルにトークン情報を書き込む """

        if self.jt.token_type() == 'KEYWORD':
            self.xmlf.write('<keyword> ' + self.jt.keyword() + ' </keyword>\n')
        elif self.jt.token_type() == 'SYMBOL':
            s = self.jt.symbol()
            if s == '<': s = '&lt;'
            elif s == '>': s = '&gt;'
            elif s == '&': s = '&amp;'
            self.xmlf.write('<symbol> ' + s + ' </symbol>\n')
        elif self.jt.token_type() == 'IDENTIFIER':
            self.xmlf.write('<identifier> ' + self.jt.identifier() + ' </identifier>\n')
        elif self.jt.token_type() == 'INT_CONST':
            self.xmlf.write('<integerConstant> ' + self.jt.int_val() + ' </integerConstant>\n')
        elif self.jt.token_type() == 'STRING_CONST':
            self.xmlf.write('<stringConstant> ' + self.jt.string_val() + ' </stringConstant>\n')
        else:
            pass
        return None

    def print_token(self):
        """ デバッグ用 トークン表示メソッド """

        if self.jt.token_type() == 'KEYWORD': print('KEYWORD [' + self.jt.keyword() + ']')
        elif self.jt.token_type() == 'SYMBOL': print('SYMBOL [' + self.jt.symbol() + ']')
        elif self.jt.token_type() == 'IDENTIFIER': print('IDENTIFIER [' + self.jt.identifier() + ']')
        elif self.jt.token_type() == 'INT_CONST': print('INT_CONST [' + self.jt.int_val() + ']')
        elif self.jt.token_type() == 'STRING_CONST': print('STRING_CONST [' + self.jt.string_val() + ']')
        else: print('???')
        return None

    def check_symbol(self, symbol, err_msg):
        """ シンボルが含まれるかチェックする。

        シンボルが含まれる場合は、シンボルのxml出力をし、次のトークンを取得する。含まれない場合はエラー。

        Args:
            symbol: 確認するシンボル
            err_msg: エラーメッセージ
        """

        if self.jt.token_type() == 'SYMBOL' and self.jt.symbol() == symbol:
            self.write_token_xml()
        else:
            raise CompileError(err_msg)
        self.advance()
        return None

    def compile_class(self):
        # class: 'class' className '{' classVarDec* subroutineDec* '}'
        # className: identifier

        # class
        if self.jt.token_type() == 'KEYWORD' and self.jt.keyword() == 'class':
            self.xmlf.write('<class>\n')
            self.write_token_xml()
        else:
            raise CompileError('Class Error 1')
        self.advance()

        # className
        if self.jt.token_type() == 'IDENTIFIER':
            self.write_token_xml()
        else:
            raise CompileError('Class Error 2')
        self.advance()

        # '{'
        self.check_symbol('{', 'Class Error 3')

        # classVarDec*
        self.compile_class_var_dec()

        # subroutineDec*
        self.compile_subroutine()

        # '}'
        self.check_symbol('}', 'Class Error 4')

        self.xmlf.write('</class>\n')
        return None

    def compile_class_var_dec(self):
        # classVarDec: ('static' | 'field') type varName (',' varName)* ';'
        # type: 'int' | 'char' | 'boolean' | className
        # varName: identifier

        # ('static | 'field')
        if self.jt.token_type() == 'KEYWORD' and self.jt.keyword() in ('static', 'field'):
            self.xmlf.write('<classVarDec>\n')
            self.write_token_xml()
        else:
            return None
        self.advance()

        # type
        if self.jt.token_type() == 'KEYWORD' and self.jt.keyword() in ('int', 'char', 'boolean'):
            self.write_token_xml()
        elif self.jt.token_type() == 'IDENTIFIER':
            self.write_token_xml()
        else:
            raise CompileError('ClassVarDec Error 1')
        self.advance()

        # varName
        if self.jt.token_type() == 'IDENTIFIER':
            self.write_token_xml()
        else:
            raise CompileError('ClassVarDec Error 2')
        self.advance()

        # (',' varName)*
        while self.jt.token_type() == 'SYMBOL' and self.jt.symbol() == ',':
            # ','
            self.write_token_xml()
            self.advance()
            
            # varName
            if self.jt.token_type() == 'IDENTIFIER':
                self.write_token_xml()
            else:
                raise CompileError('ClassVarDec Error 3')
            self.advance()

        # ';'
        self.check_symbol(';', 'ClassVarDec Error 4')

        self.xmlf.write('</classVarDec>\n')

        # classVarDec* の*部分
        # もし次もclassVarDecの場合、本メソッドを再帰呼び出しをする。
        if self.jt.token_type() == 'KEYWORD' and self.jt.keyword() in ('static', 'field'):
            self.compile_class_var_dec()
        else:
            return None

    def compile_subroutine(self):
        # subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) subroutineName
        #   '(' parameterList ')' subroutineBody
        # subroutineName: identifier
        # subroutineBody: '{' varDec* statements '}'

        # ('constructor' | 'function' | 'method')
        if self.jt.token_type() == 'KEYWORD' and self.jt.keyword() in ('constructor', 'function', 'method'):
            self.xmlf.write('<subroutineDec>\n')
            self.write_token_xml()
        else:
            return None
        self.advance()

        # ('void' | type)
        if self.jt.token_type() == 'KEYWORD' and self.jt.keyword() in ('void', 'int', 'char', 'boolean'):
            # void | type(className除く)
            self.write_token_xml()
        elif self.jt.token_type() == 'IDENTIFIER':
            # className
            self.write_token_xml()
        else:
            raise CompileError('SubroutineDec Error 1')
        self.advance()

        # subroutineName
        if self.jt.token_type() == 'IDENTIFIER':
            self.write_token_xml()
        else:
            raise CompileError('SubroutineDec Error 2')
        self.advance()

        # '('
        self.check_symbol('(', 'SubroutineDec Error 3')

        # parameterList
        self.compile_parameter_list()

        # ')'
        self.check_symbol(')', 'SubroutineDec Error 4')

        # subroutineBody
        self.xmlf.write('<subroutineBody>\n')

        # '{'
        self.check_symbol('{', 'SubroutineDec Error 5')

        # varDec*
        self.compile_var_dec()

        # statements
        self.compile_statements()

        # '}'
        self.check_symbol('}', 'SubroutineDec Error 6')

        self.xmlf.write('</subroutineBody>\n')
        self.xmlf.write('</subroutineDec>\n')

        # subroutineDec* の*部分
        # もし次もsubroutineDecの場合、本メソッドを再帰呼び出しをする。
        if self.jt.token_type() == 'KEYWORD' and self.jt.keyword() in ('constructor', 'function', 'method'):
            self.compile_subroutine()
        else:
            return None

    def compile_parameter_list(self):
        # parameterList: ((type varName) (',' type varName)*)?

        self.xmlf.write('<parameterList>\n')

        # type
        if self.jt.token_type() == 'KEYWORD' and self.jt.keyword() in ('int', 'char', 'boolean'):
            self.write_token_xml()
        elif self.jt.token_type() == 'IDENTIFIER':
            self.write_token_xml()
        else:
            # (...)? parameterListの中身がない場合
            self.xmlf.write('</parameterList>\n')
            return None
        self.advance()

        # varName
        if self.jt.token_type() == 'IDENTIFIER':
            self.write_token_xml()
        else:
            raise CompileError('ParameterList Error 1')
        self.advance()

        # (',' type varName)*
        while self.jt.token_type() == 'SYMBOL' and self.jt.symbol() == ',':
            # ','
            self.write_token_xml()
            self.advance()
    
            # type
            if self.jt.token_type() == 'KEYWORD' and self.jt.keyword() in ('int', 'char', 'boolean'):
                self.write_token_xml()
            elif self.jt.token_type() == 'IDENTIFIER':
                self.write_token_xml()
            else:
                raise CompileError('ParameterList Error 2')
            self.advance()

            # varName
            if self.jt.token_type() == 'IDENTIFIER':
                self.write_token_xml()
            else:
                raise CompileError('ParameterList Error 3')
            self.advance()

        self.xmlf.write('</parameterList>\n')
        return None

    def compile_var_dec(self):
        #varDec: 'var' type varName(',' varName)* ';'

        # 'var'
        if self.jt.token_type() == 'KEYWORD' and self.jt.keyword() == 'var':
            self.xmlf.write('<varDec>\n')
            self.write_token_xml()
        else:
            # varDecがない場合
            return None
        self.advance()

        # type
        if self.jt.token_type() == 'KEYWORD' and self.jt.keyword() in ('int', 'char', 'boolean'):
            self.write_token_xml()
        elif self.jt.token_type() == 'IDENTIFIER':
            self.write_token_xml()
        else:
            raise CompileError('VarDec Error 1')      
        self.advance()

        # varName
        if self.jt.token_type() == 'IDENTIFIER':
            self.write_token_xml()
        else:
            raise CompileError('VarDec Error 2')
        self.advance()

        # (',' varName)*
        while self.jt.token_type() == 'SYMBOL' and self.jt.symbol() == ',':
            # ','
            self.write_token_xml()
            self.advance()
            
            # varName
            if self.jt.token_type() == 'IDENTIFIER':
                self.write_token_xml()
            else:
                raise CompileError('VarDec Error 3')
            self.advance()
    
        # ';'
        self.check_symbol(';', 'VarDec Error 4')

        self.xmlf.write('</varDec>\n')

        # varDec* の*部分
        # もし次もvarDecの場合、本メソッドを再帰呼び出しをする。
        if self.jt.token_type() == 'KEYWORD' and self.jt.keyword() == 'var':
            self.compile_var_dec()
        else:
            return None

    def compile_statements(self):
        # statements: statement*
        # statement: letStatement | ifStatement | whileStatement | doStatement | returnStatement

        self.xmlf.write('<statements>\n')

        while self.jt.token_type() == 'KEYWORD' \
            and self.jt.keyword() in ('let', 'if', 'while', 'do', 'return'):
            self.compile_let()
            self.compile_if()
            self.compile_while()
            self.compile_do()
            self.compile_return()

        self.xmlf.write('</statements>\n')
        return None

    def compile_do(self):
        # doStatement: 'do' subroutineCall ';'
        # subroutineCall: subroutineName '(' expressionList ')' 
        #   | (className | varName) '.' subroutineName '(' expressionList ')'

        # 'do'
        if self.jt.token_type() == 'KEYWORD' and self.jt.keyword() == 'do':
            self.xmlf.write('<doStatement>\n')
            self.write_token_xml()
        else:
            return None
        self.advance()
        
        # subroutineCall
        # subroutineName | className | varName
        if self.jt.token_type() == 'IDENTIFIER':
            self.write_token_xml()
        else:
            raise CompileError('DoStatement Error 1')
        self.advance()
        
        if self.jt.token_type() == 'SYMBOL' and self.jt.symbol() == '(':
            # 前のトークンがsubroutineNameの場合、'('となる

            self.write_token_xml()
            self.advance()

            # expressionList
            self.compile_expression_list()

            # ')'
            self.check_symbol(')', 'DoStatement Error 2')

        elif self.jt.token_type() == 'SYMBOL' and self.jt.symbol() == '.':
            # 前のトークンがclassNameまたはvarNameの場合、'.'となる
            self.write_token_xml()
            self.advance()

            # subroutineName
            if self.jt.token_type() == 'IDENTIFIER':
                self.write_token_xml()
            else:
                raise CompileError('DoStatement Error 3')
            self.advance()
            
            # '('
            self.check_symbol('(', 'DoStatement Error 4')

            # expressionList
            self.compile_expression_list()

            # ')'
            self.check_symbol(')', 'DoStatement Error 5')

        else:
            raise CompileError('DoStatement Error 6')

        # ';'
        self.check_symbol(';', 'DoStatement Error 7')

        self.xmlf.write('</doStatement>\n')
        return None

    def compile_let(self):
        # letStatement: 'let' varName ('[' expression ']')? '=' expression ';'

        # 'let'
        if self.jt.token_type() == 'KEYWORD' and self.jt.keyword() == 'let':
            self.xmlf.write('<letStatement>\n')
            self.write_token_xml()
        else:
            return None
        self.advance()

        # varName
        if self.jt.token_type() == 'IDENTIFIER':
            self.write_token_xml()
        else:
            raise CompileError('LetStatement Error 1')
        self.advance()

        # ('['expression']')?
        if self.jt.token_type() == 'SYMBOL' and self.jt.symbol() == '[':
            # '['
            self.write_token_xml()
            self.advance()

            # expression
            self.compile_expression()

            # ']'
            self.check_symbol(']', 'LetStatement Error 2')
        else:
            pass

        # '='
        self.check_symbol('=', 'LetStatement Error 3')

        # expression
        self.compile_expression()

        # ';'
        self.check_symbol(';', 'LetStatement Error 4')

        self.xmlf.write('</letStatement>\n')
        return None

    def compile_while(self):
        # whileStatement: 'while' '(' expression ')' '{' statements '}'

        # 'while'
        if self.jt.token_type() == 'KEYWORD' and self.jt.keyword() == 'while':
            self.xmlf.write('<whileStatement>\n')
            self.write_token_xml()
        else:
            return None
        self.advance()

        # '('
        self.check_symbol('(', 'WhileStatement Error 1')

        # expression
        self.compile_expression()

        # ')'
        self.check_symbol(')', 'WhileStatement Error 2')

        # '{'
        self.check_symbol('{', 'WhileStatement Error 3')

        # statements
        self.compile_statements()

        # '}'
        self.check_symbol('}', 'WhileStatement Error 4')

        self.xmlf.write('</whileStatement>\n')
        return None

    def compile_return(self):
        # returnStatement: 'return' expression? ';'

        # 'return'
        if self.jt.token_type() == 'KEYWORD' and self.jt.keyword() == 'return':
            self.xmlf.write('<returnStatement>\n')
            self.write_token_xml()
        else:
            return None
        self.advance()

        # ';' (expressionなしの場合)
        if self.jt.token_type() == 'SYMBOL' and self.jt.symbol() == ';':
            self.write_token_xml()
            self.advance()
            self.xmlf.write('</returnStatement>\n')
            return None
        else:
            # expression
            self.compile_expression()

            # ';'
            self.check_symbol(';', 'returnStatement Error 1')

            self.xmlf.write('</returnStatement>\n')
            return None

    def compile_if(self):
        # ifStatement: 'if' '(' expression ')' '{' statements '}'
        #   ('else' '{' statements '}')?

        # 'if'
        if self.jt.token_type() == 'KEYWORD' and self.jt.keyword() == 'if':
            self.xmlf.write('<ifStatement>\n')
            self.write_token_xml()
        else:
            return None
        self.advance()

        # '('
        self.check_symbol('(', 'IfStatement Error 1')

        # expression
        self.compile_expression()

        # ')'
        self.check_symbol(')', 'IfStatement Error 2')

        # '{'
        self.check_symbol('{', 'IfStatement Error 3')

        # statements
        self.compile_statements()

        # '}'
        self.check_symbol('}', 'IfStatement Error 4')

        # 'else'
        if self.jt.token_type() == 'KEYWORD' and self.jt.keyword() == 'else':
            self.write_token_xml()
            self.advance()

            # '{'
            self.check_symbol('{', 'IfStatement Error 5')

            # statements
            self.compile_statements()

            # '}'
            self.check_symbol('}', 'IfStatement Error 6')

        else:
            pass

        self.xmlf.write('</ifStatement>\n')
        return None

    def compile_expression(self):
        # expression: term (op term)*
        # op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='

        self.xmlf.write('<expression>\n')

        # term
        self.compile_term()

        # (op term)*
        while self.jt.token_type() == 'SYMBOL' and self.jt.symbol() in '+-*/&|<>=':
            self.write_token_xml()
            self.advance()
            self.compile_term()

        self.xmlf.write('</expression>\n')
        return None

    def compile_term(self):
        '''
        term: 
            integerConstant
            | stringConstant
            | keywordConstant
            | varName
            | varName '[' expression ']'
            | subroutineCall
            | '(' expression ')'
            | unaryOp term

        subroutineCall:
            subroutineName '(' expressionList ')'
            | (className | varName) '.' subroutineName '(' expressionList ')'
        expression: term (op term)*
        op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
        unaryOp: '-' | '~'
        keywordConstant: 'true'| 'false' | 'null' | 'this'
        '''

        if self.jt.token_type() == 'INT_CONST':
            # integerConstant
            self.xmlf.write('<term>\n')
            self.write_token_xml()
            self.advance()
            
        elif self.jt.token_type() == 'STRING_CONST':
            # stringConstant
            self.xmlf.write('<term>\n')
            self.write_token_xml()
            self.advance()

        elif self.jt.token_type() == 'KEYWORD' and self.jt.keyword() in ('true', 'false', 'null', 'this'):
            # keywordConstant
            self.xmlf.write('<term>\n')
            self.write_token_xml()
            self.advance()

        elif self.jt.token_type() == 'IDENTIFIER':
            # varName | subroutineCallのsubroutineName
            # | subroutineCallのclassName | subroutineCallのvarName

            self.xmlf.write('<term>\n')
            self.write_token_xml()
            self.advance()

            if self.jt.token_type() == 'SYMBOL' and self.jt.symbol() == '[':
                # 前のトークンがvarName(配列)の場合

                # '['
                self.write_token_xml()
                self.advance()

                # expression
                self.compile_expression()

                # ']'
                self.check_symbol(']', 'Term Error 1')

            elif self.jt.token_type() == 'SYMBOL' and self.jt.symbol() == '(':
                # 前のトークンがsubroutineCallのsubroutineNameの場合

                # '('
                self.write_token_xml()
                self.advance()

                # expressionList
                self.compile_expression_list()

                # ')'
                self.check_symbol(')', 'Term Error 2')

            elif self.jt.token_type() == 'SYMBOL' and self.jt.symbol() == '.':
                # 前のトークンがsubroutineCallの(className | varName)の場合

                # '.'
                self.write_token_xml()
                self.advance()

                # subroutineName
                if self.jt.token_type() == 'IDENTIFIER':
                    self.write_token_xml()
                    self.advance()
                else:
                    raise CompileError('Term Error 3')
                
                # '('
                self.check_symbol('(', 'Term Error 4')
                
                # expressionList
                self.compile_expression_list()

                # ')'
                self.check_symbol(')', 'Term Error 5')

            else:
                # 前のトークンがvarName(配列でない)の場合
                pass

        elif self.jt.token_type() == 'SYMBOL' and self.jt.symbol() == '(':
            # '(' expression ')'

            # '('
            self.xmlf.write('<term>\n')
            self.write_token_xml()
            self.advance()

            # expression
            self.compile_expression()

            # ')'
            self.check_symbol(')', 'Term Error 6')

        elif self.jt.token_type() == 'SYMBOL' and self.jt.symbol() in '-~':
            # unaryOp term

            # unaryOp
            self.xmlf.write('<term>\n')
            self.write_token_xml()
            self.advance()

            # term
            self.compile_term()

        else:
            raise CompileError('Term Error')

        self.xmlf.write('</term>\n')
        return None

    def compile_expression_list(self):
        # expressionList: (expression (',' expression)*)?

        self.xmlf.write('<expressionList>\n')

        # expressionListの中身がない場合
        if self.jt.token_type() == 'SYMBOL' and self.jt.symbol() == ')':
            self.xmlf.write('</expressionList>\n')
            return None

        # expression
        self.compile_expression()

        # (',' expression)*
        while self.jt.token_type() == 'SYMBOL' and self.jt.symbol() == ',':
            self.write_token_xml()
            self.advance()
            self.compile_expression()

        self.xmlf.write('</expressionList>\n')
        return None