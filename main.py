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
            report = lexer.generate_report()
            print(report)
        else:
            print(f"Não foi possível ler o arquivo {self.file_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Erro. O uso deve ser feito assim: python main.py <nome_do_arquivo_sem_extensao>")
    else:
        file_name = sys.argv[1]
        main = Main(file_name)
        main.run()
