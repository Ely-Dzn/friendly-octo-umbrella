import os
import sys
from lexico import Lexer

class Main:
    def __init__(self, file_name):
        self.file_path = self.validateFile(file_name)

    def validateFile(self, file_name):
        if not file_name.endswith(".241"):
            file_name += ".241"
        return os.path.abspath(file_name)

    def readInputFile(self):
        try:
            with open(self.file_path, 'r') as file:
                return file.read().upper()  # Lê o conteúdo do arquivo e converte para maiúsculas
        except FileNotFoundError:
            print(f"Arquivo {self.file_path} não encontrado.")
            return ""
        except IOError:
            print(f"Erro ao ler o arquivo {self.file_path}.")
            return ""

    def run(self):
        input_data = self.readInputFile()
        if input_data:
            lexer = Lexer(input_data)
            tokens = lexer.tokenize()
            report_file_name = os.path.splitext(self.file_path)[0] + ".lex"
            lexer.generate_report(report_file_name, os.path.basename(self.file_path))
            report_file_name = os.path.splitext(self.file_path)[0] + ".tab"
            lexer.generate_symbol_table_report(report_file_name, os.path.basename(self.file_path))
        else:
            print(f"Não foi possível ler o arquivo {self.file_path}")

if __name__ == "__main__":
    file_name = input("Digite o nome do arquivo fonte: ")
    main = Main(file_name)
    main.run()
