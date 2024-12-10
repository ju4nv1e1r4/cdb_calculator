import streamlit as st
import pandas as pd

def calcular_rendimento_liquido(dias_vencimento, taxa_bruta, cdi, montante_investido):
    # Tabela de imposto de renda para CDB
    if dias_vencimento <= 180:
        aliquota_ir = 22.5 / 100
    elif dias_vencimento <= 360:
        aliquota_ir = 20.0 / 100
    elif dias_vencimento <= 720:
        aliquota_ir = 17.5 / 100
    else:
        aliquota_ir = 15.0 / 100

    # Cálculo do CDI diário (usando 252 dias úteis por ano)
    cdi_diario = (1 + cdi / 100) ** (1 / 252) - 1

    # Taxa bruta diária do título
    taxa_bruta_diaria = cdi_diario * (taxa_bruta / 100)

    # Montante bruto ao final do período
    montante_bruto = montante_investido * (1 + taxa_bruta_diaria) ** dias_vencimento

    # Rendimento bruto
    rendimento_bruto = montante_bruto - montante_investido

    # Imposto de renda sobre o rendimento bruto
    imposto_renda = rendimento_bruto * aliquota_ir

    # Montante líquido ao final do período
    montante_liquido = montante_bruto - imposto_renda

    # Rendimento líquido
    rendimento_liquido = montante_liquido - montante_investido

    # Rendimento líquido em percentual do investimento inicial
    rendimento_percentual_liquido = (rendimento_liquido / montante_investido) * 100

    # Rendimento em percentual do CDI
    rendimento_percentual_cdi = (1 + rendimento_liquido / montante_investido) ** (252 / dias_vencimento) - 1
    rendimento_percentual_cdi *= 100

    return {
        "Rendimento Percentual Bruto": f"{rendimento_percentual_liquido:.2f}%",
        "Valor Absoluto a ser Resgatado": f"R${montante_liquido:,.2f}",
        "Rendimento Absoluto": f"R${rendimento_liquido:,.2f}",
        "Rendimento em Percentual Líquido": f"{rendimento_percentual_cdi:.2f}%"
    }

# Interface Streamlit
st.title("Calculadora de Rendimento Líquido de Títulos")

st.sidebar.header("Parâmetros de Entrada")
dias_vencimento = st.sidebar.number_input("Dias para vencimento", min_value=1, max_value=2000, value=360, step=1)
taxa_bruta = st.sidebar.number_input("Taxa Bruta (% do CDI)", min_value=50.0, max_value=200.0, value=110.0, step=0.1)
cdi = st.sidebar.number_input("CDI do período (%)", min_value=0.0, max_value=20.0, value=9.45, step=0.01)
montante_investido = st.sidebar.number_input("Montante a ser investido (R$)", min_value=100.0, value=1000.0, step=50.0)

if st.sidebar.button("Calcular"):
    resultado = calcular_rendimento_liquido(dias_vencimento, taxa_bruta, cdi, montante_investido)
    
    st.header("Resultados")
    st.write(f"**Rendimento Percentual Líquido:** {resultado['Rendimento Percentual Líquido']}")
    st.write(f"**Valor Absoluto a ser Resgatado:** {resultado['Valor Absoluto a ser Resgatado']}")
    st.write(f"**Rendimento Absoluto:** {resultado['Rendimento Absoluto']}")
    st.write(f"**Rendimento em Percentual do CDI:** {resultado['Rendimento em Percentual do CDI']}")

    st.subheader("Detalhes")
    st.write(f"- **Dias para vencimento:** {dias_vencimento}")
    st.write(f"- **Taxa Bruta:** {taxa_bruta}% do CDI")
    st.write(f"- **CDI do período:** {cdi}%")
    st.write(f"- **Montante investido:** R${montante_investido:,.2f}")
