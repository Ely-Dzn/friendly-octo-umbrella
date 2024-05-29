import os
import sys

class Main:
    def __init__(self, file_name):
        self.file_path = self.get_full_path(file_name)

    def get_full_path(self, file_name):
        if not file_name.endswith(".241"):
            file_name += ".241"
        return os.path.abspath(file_name)

    def read_file(self):
        try:
            with open(self.file_path, 'r') as file:
                return file.read().upper() 
        except FileNotFoundError:
            print(f"Arquivo {self.file_path} não encontrado.")
            return ""
        except IOError:
            print(f"Erro ao ler o arquivo {self.file_path}.")
            return ""


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Erro. O uso deve ser feito assim: python main.py <nome_do_arquivo_sem_extensao>")
    else:
        file_name = sys.argv[1]
        main = Main(file_name)
        main.run()
