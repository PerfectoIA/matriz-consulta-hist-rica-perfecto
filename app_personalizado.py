
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Perfecto Cálculos – Histórico de Processos", layout="centered")

# === LOGO E TÍTULO ===
st.image("logo_perfecto.png", width=220)
st.markdown("<h1 style='text-align: center; color: #c40000;'>Buscador de Pasta Anterior</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>🔍 Consulte o histórico de solicitações anteriores de forma rápida e precisa.</p>", unsafe_allow_html=True)

# === Função de busca ===
def buscar_pasta_anterior(numero_processo: str, df: pd.DataFrame) -> pd.DataFrame:
    numero_processo = numero_processo.strip().lower()
    df['PROCESSO_NORMALIZADO'] = df['PROCESSO'].astype(str).str.strip().str.lower()

    resultados = df[df['PROCESSO_NORMALIZADO'].str.contains(numero_processo, na=False)]

    if not resultados.empty:
        colunas_desejadas = {
            'DT PASTA': '📅 Data da Pasta',
            'EMPRESA': '🏢 Empresa',
            'RECLAMADA': '⚖️ Reclamada',
            'RECLAMANTE': '👤 Reclamante',
            'TIPO CÁLCULO': '📌 Tipo de Prazo'
        }
        return resultados[list(colunas_desejadas.keys())].rename(columns=colunas_desejadas)
    else:
        return pd.DataFrame()

# === Carregamento dos dados ===
try:
    # Carrega a aba única da nova planilha
    df_total = pd.read_excel("base_processos.xlsx", sheet_name=0)
    st.success("✅ Base de dados carregada com sucesso!")

    st.markdown("<h3 style='color: #222;'>Digite o número do processo para consultar:</h3>", unsafe_allow_html=True)
    processo_input = st.text_input("Exemplo: 1001414-13.2019.5.02.0311")

    if processo_input:
        resultado = buscar_pasta_anterior(processo_input, df_total)

        if not resultado.empty:
            st.success(f"🔍 Foram encontrados {len(resultado)} registro(s):")
            st.dataframe(resultado, use_container_width=True)
        else:
            st.warning("⚠️ Nenhum processo encontrado com esse número.")

except FileNotFoundError:
    st.error("❌ Arquivo 'base_processos.xlsx' não encontrado. Verifique se ele está na mesma pasta que o app.")
except Exception as e:
    st.error(f"❌ Erro ao carregar os dados: {e}")
