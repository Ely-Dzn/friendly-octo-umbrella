import re

# Tabela de Palavras e Símbolos Reservados
RESERVED_WORDS = {
    "cadeia": "A01", "caracter": "A02", "declaracoes": "A03", "enquanto": "A04", "false": "A05", 
    "fimDeclaracoes": "A06", "fimEnquanto": "A07", "fimFunc": "A08", "fimFuncoes": "A09", 
    "fimPrograma": "A10", "fimSe": "A11", "funcoes": "A12", "imprime": "A13", "inteiro": "A14", 
    "logico": "A15", "pausa": "A16", "programa": "A17", "real": "A18", "retorna": "A19", "se": "A20", 
    "senao": "A21", "tipofunc": "A22", "tipoParam": "A23", "tipoVar": "A24", "true": "A25", "vazio": "A26",
    "%": "B01", "(": "B02", ")": "B03", ",": "B04", ":": "B05", ":=": "B06", ";": "B07", "?": "B08", 
    "[": "B09", "]": "B10", "{": "B11", "}": "B12", "-": "B13", "*": "B14", "/": "B15","+": "B16", "!=": "B17", 
    "#": "B18", "<": "B19", "<=": "B20", "==": "B21", ">": "B22", ">=": "B23", "consCadeia": "C01", "consCaractere": "C02", 
    "ConsInteiro": "C03", "ConsReal": "C04", "nomFuncao": "C05", "nomPrograma": "C06", "variavel": "C07"
}

# Tabela de Símbolos
class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.counter = 1

    def add_symbol(self, lexeme, symbol_type, line_number):
        if lexeme not in self.symbols:
            truncated_lexeme = lexeme[:30]
            atom_code = RESERVED_WORDS.get(lexeme.lower(), "UNKN")
            self.symbols[lexeme] = {
                'index': self.counter,
                'atom_code': atom_code,
                'lexeme': truncated_lexeme,
                'original_length': len(lexeme),
                'truncated_length': len(truncated_lexeme),
                'symbol_type': symbol_type,
                'lines': [line_number]
            }
            self.counter += 1
        else:
            if line_number not in self.symbols[lexeme]['lines']:
                self.symbols[lexeme]['lines'].append(line_number)
                if len(self.symbols[lexeme]['lines']) > 5:
                    self.symbols[lexeme]['lines'].pop(0)

class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

class Lexer:
    def __init__(self, input_data):
        self.input_data = input_data
        self.position = 0
        self.current_char = None
        self.symbol_table = SymbolTable()
        self.lexemes = []  # Armazenar informações dos lexemas
        self.line_number = 1  # Controle de linha
        self.advance()

    def advance(self):
        if self.position < len(self.input_data):
            self.current_char = self.input_data[self.position]
            self.position += 1
        else:
            self.current_char = None

    def readChar(self):
        char = self.current_char
        self.advance()
        if char == '\n':
            self.line_number += 1
        return char

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

    def formToken(self):
        self.skipWhitespace()
        self.skipComment()
        token = ''
        start_position = self.position
        while self.current_char is not None and self.is_valid_char(self.current_char):
            token += self.readChar()
            if len(token) >= 30:
                break
        if token:
            token_type = 'UNKN'
            if token.lower() in RESERVED_WORDS:
                token_type = RESERVED_WORDS[token.lower()]
            elif token.isidentifier():
                token_type = 'IDENTIFIER'
            self.lexemes.append((token, start_position, self.position, self.line_number))
            self.symbol_table.add_symbol(token, token_type, self.line_number)
        return token, token_type

    def tokenize(self):
        tokens = []
        while self.current_char is not None:
            token_value, token_type = self.formToken()
            if token_value:
                tokens.append(Token(token_type, token_value))
        return tokens

    def generate_report(self, report_file_name, input_file_name):
        with open(report_file_name, 'w') as file:
            file.write("Código da Equipe: 06\n")
            file.write("Componentes:\n")
            file.write("João Marcelo Costa Miranda; joao.miranda@aln.senaicimatec.edu.br; (71)99286-9762\n")
            file.write("Gabriel de Brito Leal dos Santos; gabriel2@aln.senaicimatec.edu.br; (71)99244-7371\n")
            file.write("Henrique Malisano; henrique.malisano@aln.senaicimatec.edu.br; (71)99693-2526\n")
            file.write("Eric Lisboa Queiroz; eric.queiroz@aln.senaicimatec.edu.br; (71)99600-1889\n\n")
            file.write(f"RELATÓRIO DA ANÁLISE LÉXICA. Texto fonte analisado: {input_file_name}\n")
            
            for lexeme_info in self.lexemes:
                lexeme, start_position, end_position, line_number = lexeme_info
                symbol_info = self.symbol_table.symbols.get(lexeme, {})
                atom_code = symbol_info.get('atom_code', 'UNKNOWN')
                file.write(f"Lexeme: {lexeme}, Código: {atom_code}, ÍndiceTabSimb: {symbol_info.get('index', 'UNKNOWN')}, Linha: {', '.join(map(str, symbol_info.get('lines', [])))}\n")
    
    def generate_symbol_table_report(self, report_file_name, input_file_name):
        with open(report_file_name, 'w') as file:
            file.write("Código da Equipe: 06\n")
            file.write("Componentes:\n")
            file.write("João Marcelo Costa Miranda; joao.miranda@aln.senaicimatec.edu.br; (71)99286-9762\n")
            file.write("Gabriel de Brito Leal dos Santos; gabriel2@aln.senaicimatec.edu.br; (71)99244-7371\n")
            file.write("Henrique Malisano; henrique.malisano@aln.senaicimatec.edu.br; (71)99693-2526\n")
            file.write("Eric Lisboa Queiroz; eric.queiroz@aln.senaicimatec.edu.br; (71)99600-1889\n\n")
            file.write(f"RELATÓRIO DA TABELA DE SÍMBOLOS. Texto fonte analisado: {input_file_name}\n")
        
            for lexeme, symbol_info in self.symbol_table.symbols.items():
                atom_code = symbol_info.get('atom_code', 'UNKNOWN')
                original_length = symbol_info.get('original_length', 'UNKNOWN')
                truncated_length = symbol_info.get('truncated_length', 'UNKNOWN')
                symbol_type = symbol_info.get('symbol_type', 'UNKNOWN')
                lines = symbol_info.get('lines', [])
                file.write(f"Entrada: {symbol_info['index']}, Codigo: {atom_code}, Lexeme: {lexeme}, QtdCharAntesTrunc: {original_length}, QtdCharDepoisTrunc: {truncated_length}, TipoSimb: {symbol_type}, Linhas: {{{', '.join(map(str, lines))}}}\n")
