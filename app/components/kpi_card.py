import streamlit as st

_CARD_CSS = """
<style>
.kpi-row { display: flex; gap: 14px; flex-wrap: wrap; margin-bottom: 32px; }
.kpi-card {
    flex: 1 1 150px;
    background: #ffffff;
    border-radius: 10px;
    padding: 20px 22px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.07), 0 1px 2px rgba(0,0,0,0.04);
    min-width: 130px;
    border-top: 3px solid var(--kpi-color, #4338CA);
}
.kpi-icon {
    font-size: 1rem;
    color: var(--kpi-color, #4338CA);
    margin-bottom: 12px;
    opacity: 0.80;
}
.kpi-value {
    font-size: 2rem;
    font-weight: 700;
    color: #0F172A;
    line-height: 1;
    letter-spacing: -0.04em;
}
.kpi-label {
    font-size: 0.68rem;
    color: #94A3B8;
    margin-top: 6px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
}
</style>
"""


def kpi_row(cards: list[dict]) -> None:
    st.markdown(_CARD_CSS, unsafe_allow_html=True)
    cols = st.columns(len(cards))
    for col, card in zip(cols, cards):
        color = card.get("color", "#4338CA")
        icon  = card.get("icon", "circle")
        with col:
            st.markdown(
                f"""
                <div class="kpi-card" style="--kpi-color:{color}">
                  <div class="kpi-icon"><i class="bi bi-{icon}"></i></div>
                  <div class="kpi-value">{card['value']}</div>
                  <div class="kpi-label">{card['label']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
