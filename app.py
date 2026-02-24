import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# ─────────────────────────────────────────────
# Configuração da página
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Orçamento de Vidros e Espelhos",
    page_icon="🪟",
    layout="wide",
)

# ─────────────────────────────────────────────
# CSS customizado
# ─────────────────────────────────────────────
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a6fa8;
        text-align: center;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1rem;
        color: #555;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .section-header {
        font-size: 1.15rem;
        font-weight: 600;
        color: #1a6fa8;
        border-bottom: 2px solid #1a6fa8;
        padding-bottom: 4px;
        margin-bottom: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Função utilitária: formatar moeda BRL
# ─────────────────────────────────────────────
def fmt_brl(valor: float) -> str:
    """Formata um float como moeda brasileira: R$ 1.234,56"""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ─────────────────────────────────────────────
# Função para gerar PDF
# ─────────────────────────────────────────────
def gerar_pdf(itens, cliente, observacoes, preco_vidro, preco_espelho,
              total_vidro, total_espelho, total_geral):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Título
    pdf.set_font("Helvetica", "B", 18)
    pdf.set_text_color(26, 111, 168)
    pdf.cell(0, 12, "ORCAMENTO DE VIDROS E ESPELHOS", align="C",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Data
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 6, f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}", align="R",
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)

    # Dados do cliente
    if cliente:
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 7, f"Cliente: {cliente}",
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Preços de referência
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(
        0, 6,
        f"Preco referencia - Vidro: R$ {preco_vidro:.2f}/m2   |   Espelho: R$ {preco_espelho:.2f}/m2",
        new_x=XPos.LMARGIN, new_y=YPos.NEXT
    )
    pdf.ln(4)

    # Cabeçalho da tabela
    headers = ["Descricao", "Tipo", "Esp.", "Acab.", "L(m)", "A(m)", "Qtd", "Area Tot.", "Adic.%", "Vl. Total"]
    col_widths = [42, 16, 12, 18, 13, 13, 10, 18, 14, 24]

    pdf.set_fill_color(26, 111, 168)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 8)

    for h, w in zip(headers, col_widths):
        pdf.cell(w, 8, h, border=1, fill=True, align="C")
    pdf.ln()

    # Linhas da tabela
    pdf.set_font("Helvetica", "", 8)
    fill = False
    for item in itens:
        pdf.set_text_color(0, 0, 0)
        if fill:
            pdf.set_fill_color(235, 245, 255)
        else:
            pdf.set_fill_color(255, 255, 255)

        row = [
            item["Descricao"][:28],
            item["Tipo"],
            item["Espessura"],
            item["Acabamento"][:10],
            f"{item['Largura (m)']:.2f}",
            f"{item['Altura (m)']:.2f}",
            str(item["Qtd"]),
            f"{item['Area Total (m2)']:.3f}",
            f"{item['Adicional (%)']:.1f}%",
            f"R$ {item['Valor Total (R$)']:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        ]
        for val, w in zip(row, col_widths):
            pdf.cell(w, 7, val, border=1, fill=True, align="C")
        pdf.ln()
        fill = not fill

    pdf.ln(4)

    # Totais
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(0, 0, 0)

    pdf.cell(100, 8, "Total Vidros:", align="R")
    pdf.cell(0, 8, fmt_brl(total_vidro),
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.cell(100, 8, "Total Espelhos:", align="R")
    pdf.cell(0, 8, fmt_brl(total_espelho),
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font("Helvetica", "B", 12)
    pdf.set_fill_color(26, 111, 168)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(100, 10, "TOTAL GERAL:", align="R", fill=True)
    pdf.cell(0, 10, fmt_brl(total_geral), fill=True,
             new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # Observações
    if observacoes:
        pdf.ln(4)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 7, "Observacoes:",
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Helvetica", "", 9)
        pdf.multi_cell(0, 6, observacoes)

    return bytes(pdf.output())


# ─────────────────────────────────────────────
# Inicialização do estado da sessão
# ─────────────────────────────────────────────
if "itens" not in st.session_state:
    st.session_state.itens = []

if "preco_vidro" not in st.session_state:
    st.session_state.preco_vidro = 150.0

if "preco_espelho" not in st.session_state:
    st.session_state.preco_espelho = 200.0

if "cliente" not in st.session_state:
    st.session_state.cliente = ""

if "observacoes" not in st.session_state:
    st.session_state.observacoes = ""

# ─────────────────────────────────────────────
# Cabeçalho
# ─────────────────────────────────────────────
st.markdown('<div class="main-title">🪟 Orçamento de Vidros e Espelhos</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Calcule orçamentos de forma rápida e profissional</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Sidebar — Configurações de preço e cliente
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configurações")

    st.markdown("### 👤 Dados do Cliente")
    st.session_state.cliente = st.text_input(
        "Nome do cliente",
        value=st.session_state.cliente,
        placeholder="Ex.: João Silva"
    )
    st.session_state.observacoes = st.text_area(
        "Observações",
        value=st.session_state.observacoes,
        placeholder="Prazo de entrega, condições de pagamento...",
        height=80
    )

    st.divider()
    st.markdown("### 💰 Preço por m²")

    st.session_state.preco_vidro = st.number_input(
        "Vidro (R$/m²)",
        min_value=0.0,
        value=st.session_state.preco_vidro,
        step=5.0,
        format="%.2f"
    )

    st.session_state.preco_espelho = st.number_input(
        "Espelho (R$/m²)",
        min_value=0.0,
        value=st.session_state.preco_espelho,
        step=5.0,
        format="%.2f"
    )

    st.divider()
    st.markdown("### 🗑️ Limpar Orçamento")
    if st.button("🗑️ Remover todos os itens", use_container_width=True):
        st.session_state.itens = []
        st.rerun()

# ─────────────────────────────────────────────
# Layout principal — duas colunas
# ─────────────────────────────────────────────
col_form, col_lista = st.columns([1, 2], gap="large")

# ─── Coluna esquerda: formulário de adição ───
with col_form:
    st.markdown('<div class="section-header">➕ Adicionar Item</div>', unsafe_allow_html=True)

    with st.form("form_item", clear_on_submit=True):
        descricao = st.text_input("Descrição do item", placeholder="Ex.: Janela sala, Box banheiro...")

        tipo = st.selectbox("Tipo de material", ["Vidro", "Espelho"])

        col_l, col_a = st.columns(2)
        with col_l:
            largura = st.number_input("Largura (m)", min_value=0.01, value=1.0, step=0.05, format="%.2f")
        with col_a:
            altura = st.number_input("Altura (m)", min_value=0.01, value=1.0, step=0.05, format="%.2f")

        quantidade = st.number_input("Quantidade (peças)", min_value=1, value=1, step=1)

        espessura = st.selectbox(
            "Espessura",
            ["3mm", "4mm", "5mm", "6mm", "8mm", "10mm", "12mm", "Outro"]
        )

        acabamento = st.selectbox(
            "Acabamento",
            ["Polido", "Bisotado", "Lapidado", "Jateado", "Temperado", "Laminado", "Nenhum"]
        )

        adicional_pct = st.number_input(
            "Adicional de acabamento (%)",
            min_value=0.0,
            value=0.0,
            step=5.0,
            format="%.1f",
            help="Percentual extra sobre o valor base para o tipo de acabamento selecionado."
        )

        submitted = st.form_submit_button("✅ Adicionar Item", use_container_width=True, type="primary")

        if submitted:
            if not descricao.strip():
                st.error("Informe a descrição do item.")
            else:
                preco_base = (
                    st.session_state.preco_vidro
                    if tipo == "Vidro"
                    else st.session_state.preco_espelho
                )
                area = largura * altura
                area_total = area * quantidade
                valor_unitario = area * preco_base * (1 + adicional_pct / 100)
                valor_total = valor_unitario * quantidade

                item = {
                    "Descricao": descricao.strip(),
                    "Tipo": tipo,
                    "Espessura": espessura,
                    "Acabamento": acabamento,
                    "Largura (m)": largura,
                    "Altura (m)": altura,
                    "Area (m2)": round(area, 4),
                    "Qtd": quantidade,
                    "Area Total (m2)": round(area_total, 4),
                    "Preco/m2 (R$)": preco_base,
                    "Adicional (%)": adicional_pct,
                    "Valor Unit. (R$)": round(valor_unitario, 2),
                    "Valor Total (R$)": round(valor_total, 2),
                }
                st.session_state.itens.append(item)
                st.success(f"Item **{descricao.strip()}** adicionado com sucesso!")
                st.rerun()

# ─── Coluna direita: tabela de itens ───
with col_lista:
    st.markdown('<div class="section-header">📋 Itens do Orçamento</div>', unsafe_allow_html=True)

    if not st.session_state.itens:
        st.info("Nenhum item adicionado ainda. Use o formulário ao lado para começar.")
    else:
        df = pd.DataFrame(st.session_state.itens)

        # Renomear colunas para exibição
        df_display = df.rename(columns={
            "Descricao": "Descrição",
            "Area (m2)": "Área (m²)",
            "Area Total (m2)": "Área Total (m²)",
            "Preco/m2 (R$)": "Preço/m² (R$)",
        })

        colunas_exibir = [
            "Descrição", "Tipo", "Espessura", "Acabamento",
            "Largura (m)", "Altura (m)", "Qtd",
            "Área Total (m²)", "Preço/m² (R$)", "Adicional (%)",
            "Valor Total (R$)"
        ]
        st.dataframe(
            df_display[colunas_exibir],
            use_container_width=True,
            hide_index=False,
        )

        # ─── Remover item individual ───
        st.markdown("**Remover item pelo índice:**")
        col_idx, col_btn = st.columns([2, 1])
        with col_idx:
            idx_remover = st.number_input(
                "Índice do item a remover",
                min_value=0,
                max_value=max(0, len(st.session_state.itens) - 1),
                step=1,
                label_visibility="collapsed"
            )
        with col_btn:
            if st.button("🗑️ Remover", use_container_width=True):
                removed = st.session_state.itens.pop(int(idx_remover))
                st.success(f"Item **{removed['Descricao']}** removido.")
                st.rerun()

        st.divider()

        # ─── Totais ───
        total_vidro = sum(
            i["Valor Total (R$)"] for i in st.session_state.itens if i["Tipo"] == "Vidro"
        )
        total_espelho = sum(
            i["Valor Total (R$)"] for i in st.session_state.itens if i["Tipo"] == "Espelho"
        )
        total_geral = total_vidro + total_espelho

        t1, t2, t3 = st.columns(3)
        t1.metric("🪟 Total Vidros", fmt_brl(total_vidro))
        t2.metric("🪞 Total Espelhos", fmt_brl(total_espelho))
        t3.metric("💰 Total Geral", fmt_brl(total_geral))

        # ─── Exportar PDF ───
        st.divider()
        st.markdown('<div class="section-header">📄 Exportar Orçamento</div>', unsafe_allow_html=True)

        if st.button("📥 Gerar PDF do Orçamento", use_container_width=True, type="primary"):
            pdf_bytes = gerar_pdf(
                st.session_state.itens,
                st.session_state.cliente,
                st.session_state.observacoes,
                st.session_state.preco_vidro,
                st.session_state.preco_espelho,
                total_vidro,
                total_espelho,
                total_geral,
            )
            st.download_button(
                label="⬇️ Baixar PDF",
                data=pdf_bytes,
                file_name=f"orcamento_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
