import re
RESERVED_WORDS = {
        "cadeia": "A01", "caracter": "A02", "declaracoes": "A03", "enquanto": "A04", "false": "A05", 
        "fimDeclaracoes": "A06", "fimEnquanto": "A07", "fimFunc": "A08", "fimFuncoes": "A09", 
        "fimPrograma": "A10", "fimSe": "A11", "funcoes": "A12", "imprime": "A13", "inteiro": "A14", 
        "logico": "A15", "pausa": "A16", "programa": "A17", "real": "A18", "retorna": "A19", "se": "A20", 
        "senao": "A21", "tipofunc": "A22", "tipoParam": "A23", "tipoVar": "A24", "true": "A25", "vazio": "A26",
        "%": "B01", "(": "B02", ")": "B03", ",": "B04", ":": "B05", ":=": "B06", ";": "B07", "?": "B08", 
        "[": "B09", "]": "B10", "{": "B11", "}": "B12", "-": "B13", "*": "B14", "/": "B15","+": "B16", "!=": "B17", 
        "#": "B18", "<": "B19", "<=": "B20", "==": "B21", ">": "B22", ">=": "B23", "consCadeia": "C01", "consCaractere": "C02", 
        "consInteiro": "C03", "consReal": "C04", "nomFuncao": "C05", "nomPrograma": "C06", "variavel": "C07"
    }

def get_atom_code(lexeme):
    if lexeme.lower() in RESERVED_WORDS:
        return RESERVED_WORDS[lexeme.lower()]
    
    if lexeme.isdigit():
        return "C03"  # consInteiro
    
    try:
        float_value = float(lexeme)
        if float_value.is_integer():
            return "C03"  # consInteiro
        else:
            return "C04"  # consReal
    except ValueError:
        pass
    
    if lexeme.isidentifier() and lexeme.startswith("_"):
        return "C07"  # variavel
    
    return "UNKN"  # Desconhecido ou não especificado


# Tabela de Símbolos
class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.counter = 1


    def add_symbol(self, lexeme, symbol_type, line_number):
        if lexeme not in self.symbols:
            truncated_lexeme = lexeme[:30]
            atom_code = get_atom_code(lexeme)
            
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
        token_type = 'UNKN'  # Inicializa token_type como 'UNKN'

        if self.current_char is None:
            return token, token_type
        
        if self.current_char.isdigit():
            while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
                token += self.readChar()
            token_type = 'NUMBER'
        elif self.current_char == '_':
            token += self.readChar()
            while self.current_char is not None and self.current_char.isalnum():
                token += self.readChar()
            token_type = 'VARIABLE'
        elif self.current_char.isalpha():
            while self.current_char is not None and self.is_valid_char(self.current_char):
                token += self.readChar()
            if token.lower() in RESERVED_WORDS:
                token_type = RESERVED_WORDS[token.lower()]
            else:
                token_type = 'IDENTIFIER'
        else:
            token += self.readChar()

        if token:
            self.lexemes.append((token, start_position, self.position, self.line_number))
            self.symbol_table.add_symbol(token, token_type, self.line_number)
        return token, token_type

    def tokenize(self):
        tokens = []
        first_valid_name_found = False
        while self.current_char is not None:
            token_value, token_type = self.formToken()
            if token_value:  # Certifica-se de que um token foi formado
                # Se encontrar a palavra-chave "PROGRAMA", o próximo nome válido será o nome do programa
                if token_type == RESERVED_WORDS.get("programa", ""):
                    first_valid_name_found = True
                elif first_valid_name_found and token_type == 'IDENTIFIER':
                    token_type = 'PROGRAM_NAME'
                    first_valid_name_found = False

                tokens.append(Token(token_type, token_value))
            else:
                self.advance()  # Avança para evitar loops infinitos
        return tokens

    def generate_report(self, report_file_name, input_file_name):
        with open(report_file_name, 'w') as file:
            file.write("Codigo da Equipe: 06\n")
            file.write("Componentes:\n")
            file.write("Joao Marcelo Costa Miranda; joao.miranda@aln.senaicimatec.edu.br; (71)99286-9762\n")
            file.write("Gabriel de Brito Leal dos Santos; gabriel2@aln.senaicimatec.edu.br; (71)99244-7371\n")
            file.write("Henrique Malisano; henrique.malisano@aln.senaicimatec.edu.br; (71)99693-2526\n")
            file.write("Eric Lisboa Queiroz; eric.queiroz@aln.senaicimatec.edu.br; (71)99600-1889\n\n")
            file.write(f"RELATORIO DA ANALISE LEXICA. Texto fonte analisado: {input_file_name}\n")
            
            for lexeme_info in self.lexemes:
                lexeme, start_position, end_position, line_number = lexeme_info
                symbol_info = self.symbol_table.symbols.get(lexeme, {})
                atom_code = symbol_info.get('atom_code', 'UNKNOWN')
                file.write(f"Lexeme: {lexeme}, Codigo: {atom_code}, IndiceTabSimb: {symbol_info.get('index', 'UNKNOWN')}, Linha: {', '.join(map(str, symbol_info.get('lines', [])))}\n")

    def generate_symbol_table_report(self, report_file_name, input_file_name):
        with open(report_file_name, 'w') as file:
            file.write("Codigo da Equipe: 06\n")
            file.write("Componentes:\n")
            file.write("Joao Marcelo Costa Miranda; joao.miranda@aln.senaicimatec.edu.br; (71)99286-9762\n")
            file.write("Gabriel de Brito Leal dos Santos; gabriel2@aln.senaicimatec.edu.br; (71)99244-7371\n")
            file.write("Henrique Malisano; henrique.malisano@aln.senaicimatec.edu.br; (71)99693-2526\n")
            file.write("Eric Lisboa Queiroz; eric.queiroz@aln.senaicimatec.edu.br; (71)99600-1889\n\n")
            file.write(f"RELATORIO DA TABELA DE SIMBOLOS. Texto fonte analisado: {input_file_name}\n")

            for lexeme, symbol_info in self.symbol_table.symbols.items():
                atom_code = symbol_info.get('atom_code', 'UNKN')
                original_length = symbol_info.get('original_length', 'UNKN')
                truncated_length = symbol_info.get('truncated_length', 'UNKN')
                symbol_type = symbol_info.get('symbol_type', 'UNKN')
                lines = symbol_info.get('lines', [])
                
                # Ajuste para considerar o tipo de símbolo corretamente
                if atom_code != "UNKN":
                    symbol_type = "Identificador"  # Se não for desconhecido, assume como Identificador
                
                file.write(f"Entrada: {symbol_info['index']}, Codigo: {atom_code}, Lexeme: {lexeme}, QtdCharAntesTrunc: {original_length}, QtdCharDepoisTrunc: {truncated_length}, TipoSimb: {symbol_type}, Linhas: {{{', '.join(map(str, lines))}}}\n")