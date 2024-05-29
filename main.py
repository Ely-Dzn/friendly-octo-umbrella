class Main:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_file(self):
        try:
            with open(self.file_path, 'r') as file:
                return file.read().upper()  # Converte o texto para maiusculas
        except FileNotFoundError:
            print(f"arquivo {self.file_path} não encontrado.")
            return ""
        except IOError:
            print(f"erro ao ler o arquivo {self.file_path}")
            return ""
  

if __name__ == "__main__":
    file_path = "exemplo.241"
    main = Main(file_path)
    main.run()
