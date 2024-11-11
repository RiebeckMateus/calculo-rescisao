from datetime import datetime
import calendar

class CalculoRescisao:
    
    def __init__(self, salario_bruto, data_inicio, data_encerramento, dias_ferias_vencidas = 0) -> None:
        self.salario_bruto = salario_bruto
        self.data_inicio = data_inicio
        self.data_encerramento = data_encerramento
        self.dias_ferias_vencidas = dias_ferias_vencidas

    ## métodos
    
    def __desconto_inss(self, valor):
        if 0 < valor <= 1412:
            resultado = valor * 0.075
        elif 1412 < valor <= 2666.68:
            resultado = (valor * 0.9) - 21.18
        elif 2666.68 < valor <= 4000.03:
            resultado = (valor * 0.12) - 101.18
        elif 4000.03 < valor <= 7786.02:
            resultado = (valor * 0.14) - 181.18
        
        return round(resultado, 2)

    def __desconto_irrf(self, valor, inss):
        salario_menos_inss = valor - inss
        if 0 < salario_menos_inss <= 2259.20:
            resultado =  0
        elif 2259.20 < salario_menos_inss <= 2826.65:
            resultado = (salario_menos_inss * 0.075) - 168.44
        elif 2826.65 < salario_menos_inss <= 3751.05:
            resultado = (salario_menos_inss * 0.15) - 381.44
        elif 3751.05 < salario_menos_inss <= 4664.68:
            resultado = (salario_menos_inss * 0.225) - 662.77
        elif 4664.68 < salario_menos_inss:
            resultado = (salario_menos_inss * 0.275) - 896
        
        return round(resultado, 2)

    ## propriedades

    @property
    def ano_inicio(self):
        inicio_data = datetime.strptime(self.data_inicio, '%d/%m/%Y')
        return inicio_data.year
    
    @property
    def dia_encerramento(self):
        encerramento_data = datetime.strptime(self.data_encerramento, '%d/%m/%Y')
        return encerramento_data.day
    
    @property
    def mes_encerramento(self):
        encerramento_data = datetime.strptime(self.data_encerramento, '%d/%m/%Y')
        return encerramento_data.month
    
    @property
    def ano_encerramento(self):
        encerramento_data = datetime.strptime(self.data_encerramento, '%d/%m/%Y')
        return encerramento_data.year

    @property
    def dias_trabalhados(self):
        _, dias_totais = calendar.monthrange(self.ano_encerramento, self.mes_encerramento)
        return dias_totais - (dias_totais - self.dia_encerramento)

    @property
    def diaria(self):
        _, dias_totais = calendar.monthrange(self.ano_encerramento, self.mes_encerramento)
        diaria = round(self.salario_bruto / dias_totais, 2)
        return diaria

    @property
    def desconto_inss_salario_bruto(self):
        return round(self.__desconto_inss(self.salario_bruto), 2)

    @property
    def desconto_irrf_salario_bruto(self):
        return round(self.__desconto_irrf(self.salario_bruto, self.desconto_inss_salario_bruto), 2)

    @property
    def desconto_vale_transporte(self):
        desconto = min(self.salario_bruto * 0.06, 180)
        return desconto
    
    @property
    def salario_liquido(self):
        valor_proporcional = round(self.diaria * self.dias_trabalhados, 2)
        valor_final = valor_proporcional - (self.desconto_vale_transporte + self.desconto_inss_salario_bruto + self.desconto_irrf_salario_bruto)
        return valor_final

    @property
    def decimo_terceiro_proporcional(self):
        '''Parcela única'''
        meses_trabalhados = self.mes_encerramento
        proporcional = (self.salario_bruto/12) * meses_trabalhados
        
        return round(proporcional, 2)
    
    @property
    def desconto_inss_decimo_terceiro_proporcional(self):
        return self.__desconto_inss(self.decimo_terceiro_proporcional)
    
    @property
    def desconto_irrf_decimo_terceiro_proporcional(self):
        return self.__desconto_irrf(self.decimo_terceiro_proporcional, self.desconto_inss_decimo_terceiro_proporcional)

    @property
    def decimo_terceiro_liquido(self):
        return self.decimo_terceiro_proporcional - (self.desconto_inss_decimo_terceiro_proporcional + self.desconto_irrf_decimo_terceiro_proporcional)

    @property
    def ferias_vencidas(self):
        proporcinal = self.dias_ferias_vencidas * self.diaria
        um_terco = proporcinal / 3
        total = round(proporcinal + um_terco, 2)
        return total

    @property
    def desconto_inss_ferias_vencidas(self):
        return round(self.__desconto_inss(self.ferias_vencidas), 2)

    @property
    def ferias_vencidas_liquido(self):
        return self.ferias_vencidas - self.desconto_inss_ferias_vencidas

    @property
    def total(self):
        return self.salario_liquido + self.decimo_terceiro_liquido + self.ferias_vencidas_liquido

    def __str__(self) -> str:
        descricao_geral = f'''Salário bruto: R$ {self.salario_bruto:.2f}
Valor dia: {self.diaria}
Dias trabalhados: {self.dias_trabalhados}
Desconto INSS sobre salário bruto: R$ {self.desconto_inss_salario_bruto:.2f}
Desconto IRFF sobre salário bruto: R$ {self.desconto_irrf_salario_bruto:.2f}
Desconto vale transporte R$ {self.desconto_vale_transporte:.2f}
Salário líquido: R$ {self.salario_liquido}

Décimo terceiro proporcional: R$ {self.decimo_terceiro_proporcional}
Desconto INSS sobre décimo terceiro: R$ {self.desconto_inss_decimo_terceiro_proporcional}
Desconto IRRF sobre décimo terceiro: R$ {self.desconto_irrf_decimo_terceiro_proporcional}
Décimo terceiro líquido: R$ {self.decimo_terceiro_liquido}

Férias vencidas proporcional: R$ {self.ferias_vencidas}
Desconto INSS sobre férias vencidas: R$ {self.desconto_inss_ferias_vencidas}
Férias vencidas líquido: R$ {self.ferias_vencidas_liquido}

Total: R$ {self.total}'''

        return descricao_geral