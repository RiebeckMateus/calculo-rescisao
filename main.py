import streamlit as st
from app import CalculoRescisao

class StreamlitApp:
    def run(self):
        
        salario_bruto = st.number_input('Salario bruto', step=.10)
        
        data_inicio = st.date_input('Data de inicio', format='DD/MM/YYYY').strftime('%d/%m/%Y')

        data_encerramento = st.date_input('Data de encerramento', format='DD/MM/YYYY').strftime('%d/%m/%Y')
        
        dias_ferias_vencidas = st.number_input('Dias de férias vencidas', step=1)
        
        calcular = st.button('Calcular')
        
        calculo = CalculoRescisao(salario_bruto, data_inicio, data_encerramento, dias_ferias_vencidas)
        
        if calcular:
            if salario_bruto:
                st.text(calculo)
            else:
                st.warning('Não preencheu o campo de salário bruto')

app = StreamlitApp()
app.run()