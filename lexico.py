class Lexer:

    def __init__ (self, input_data):
        self.input_data = input_data
        self.position = 0
        self.buffer = []
        self.current_char = None
        self.advance()

    #Avança a posição no texto de entrada e define o próximo caractere como o caractere atual.
    def advance(self):
        if self.position < len(self.input_data):
            self.current_char = self.input_data[self.position]
            self.position += 1
        else:
            self.current_char = None
    #Lê o caractere atual e avança para o próximo.
    def readChar(self):
        char = self.current_char
        self.advance()
        return char
    
    #Retorna o próximo caractere sem avançar a posição.
    def peekChar(self):
        if self.position < len(self.input_data):
            return self.input_data[self.position]
        else:
            return None
        
    def skipWhitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
    
    def skipComment(self):
        if self.current_char == '/' and self.peekChar() == '/':
            while self.current_char is not None and self.current_char != '\n':
                self.advance()
        elif self.current_char == '/' and self.peekChar() == '*':
            self.advance()
            self.advance()
            while self.current_char is not None:
                if self.current_char == '*' and self.peekChar() == '/':
                    self.advance()
                    self.advance()
                    break
                self.advance()

    def is_valid_char(self, char):
        return char.isalnum() or char in "_$\"'/*"
    
    def filterInvalidChars(self):
        self.input_data = ''.join(filter(self.is_valid_char, self.input_data))

    def formToken(self):
        self.skipWhitespace()
        self.skipComment()
        token = ''
        while self.current_char is not None and self.is_valid_char(self.current_char):
            token += self.readChar()
            if len(token) >= 30:
                break
        return token if token else None
    
    def bufferInput(self):
        self.buffer = list(self.input_data)

    def tokenize(self):
        tokens = []
        while self.current_char is not None:
            token_value = self.formToken()
            if token_value:
                if token_value.isdigit():
                    token_type = 'NUMBER'
                elif token_value.isidentifier():
                    token_type = 'IDENTIFIER'
                else:
                    token_type = 'UNKNOWN'
                
                tokens.append(Token(token_type, token_value))
        return tokens
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def __str__(self):
        return f"Token({self.type}, {self.value})"
    
    def __repr__(self):
        return self.__str__()