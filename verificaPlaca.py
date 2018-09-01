import re

class VerificaPlaca:
    def __init__(self):
        pass

    def verificar(self,placa):
        pattern = re.compile("[A-Z]{3}-?[0-9]{4}")
        placa = placa.replace(" ", "")
        placa = placa.upper()
        if pattern.match(placa):
            return placa
        else:
            return -1

