class Envio:
    def __init__(self, codigo_postal, direccion, tipo_envio, forma_pago):
        self.codigo_postal = codigo_postal
        self.direccion = direccion
        self.tipo_envio = tipo_envio
        self.forma_pago = forma_pago

    def __repr__(self):
        return f"Código postal: {self.codigo_postal}, dirección: {self.direccion}, tipo de envío: {self.tipo_envio}, forma de pago: {self.forma_pago}"
    
    def __str__(self):
        return f"Código postal: {self.codigo_postal}, dirección: {self.direccion}, tipo de envío: {self.tipo_envio}, forma de pago: {self.forma_pago}"
    
    def obtener_pais_destino(self):
        n = len(self.codigo_postal)
        if n < 4 or n > 9:
            return 'Otro'

        # ¿es Argentina?
        if n == 8:
            if self.codigo_postal[0].isalpha() and self.codigo_postal[0] not in 'IO' and self.codigo_postal[1:5].isdigit() and self.codigo_postal[5:8].isalpha():
                return 'Argentina'
            else:
                return 'Otro'

        # ¿es Brasil?
        if n == 9:
            if self.codigo_postal[0:5].isdigit() and self.codigo_postal[5] == '-' and self.codigo_postal[6:9].isdigit():
                return 'Brasil'
            else:
                return 'Otro'

        if self.codigo_postal.isdigit():
            # ¿es Bolivia?
            if n == 4:
                return 'Bolivia'

            # ¿es Chile?
            if n == 7:
                return 'Chile'

            # ¿es Paraguay?
            if n == 6:
                return 'Paraguay'

            # ¿es Uruguay?
            if n == 5:
                return 'Uruguay'

        # ...si nada fue cierto, entonces sea lo que sea, es otro...
        return 'Otro'
    
    def obtener_importe_final(self):
        # determinación del importe inicial a pagar.
        importes = (1100, 1800, 2450, 8300, 10900, 14300, 17900)
        monto = importes[int(self.tipo_envio)]
    
        destino = self.obtener_pais_destino()
        if destino == 'Argentina':
            inicial = monto
        else:
            if destino == 'Bolivia' or destino == 'Paraguay' or (destino == 'Uruguay' and self.codigo_postal[0] == '1'):
                inicial = int(monto * 1.20)
            elif destino == 'Chile' or (destino == 'Uruguay' and self.codigo_postal[0] != '1'):
                inicial = int(monto * 1.25)
            elif destino == 'Brasil':
                if self.codigo_postal[0] == '8' or self.codigo_postal[0] == '9':
                    inicial = int(monto * 1.20)
                else:
                    if self.codigo_postal[0] == '0' or self.codigo_postal[0] == '1' or self.codigo_postal[0] == '2' or self.codigo_postal[0] == '3':
                        inicial = int(monto * 1.25)
                    else:
                        inicial = int(monto * 1.30)
            else:
                inicial = int(monto * 1.50)
            
        # determinación del valor final del ticket a pagar.
        # asumimos que es pago en tarjeta...
        final = inicial
    
        # ... y si no lo fuese, la siguiente será cierta y cambiará el valor...
        if self.forma_pago == 1:
            final = int(0.9 * inicial)
        
        return final
    
