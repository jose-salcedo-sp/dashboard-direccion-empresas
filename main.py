from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

DATA_PATH = Path(__file__).parent / "data.csv"

st.set_page_config(
    page_title="Dashboard Financiero — Pepe Salcedo",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

THEME = {
    "ventas": "#38bdf8",
    "gastos": "#f87171",
    "costos": "#fbbf24",
    "utilidad": "#34d399",
    "accent": "#818cf8",
    "bg": "#090b10",
    "surface": "#12151c",
    "surface_2": "#181c26",
    "border": "#252a36",
    "border_light": "#2f3544",
    "text": "#f1f5f9",
    "muted": "#94a3b8",
    "dim": "#64748b",
}

MES_ORDER = [
    "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre",
]

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@600;700;800&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}}

[data-testid="stAppViewContainer"] {{
    background: {THEME["bg"]};
    background-image:
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(56, 189, 248, 0.07), transparent),
        radial-gradient(ellipse 60% 40% at 100% 0%, rgba(129, 140, 248, 0.05), transparent);
}}

[data-testid="stHeader"] {{ background: transparent; }}
.block-container {{
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}}

[data-testid="stSidebar"] {{
    background: {THEME["surface"]};
    border-right: 1px solid {THEME["border"]};
}}
[data-testid="stSidebar"] .stMarkdown h3 {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: {THEME["dim"]};
}}

h1, h2, h3 {{
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    letter-spacing: -0.02em;
}}

/* Hide default streamlit chrome */
#MainMenu, footer, header[data-testid="stHeader"] {{
    visibility: hidden;
}}

/* ── Header ── */
.page-header {{
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    padding: 0 0 28px 0;
    border-bottom: 1px solid {THEME["border"]};
    margin-bottom: 28px;
}}
.page-header-left {{ flex: 1; }}
.page-eyebrow {{
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: {THEME["accent"]};
    margin-bottom: 6px;
}}
.page-title {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.85rem;
    font-weight: 800;
    color: {THEME["text"]};
    margin: 0 0 6px 0;
    line-height: 1.2;
}}
.page-subtitle {{
    font-size: 0.9rem;
    color: {THEME["muted"]};
    margin: 0;
    font-weight: 400;
}}
.page-badge {{
    background: {THEME["surface_2"]};
    border: 1px solid {THEME["border"]};
    border-radius: 8px;
    padding: 8px 14px;
    font-size: 0.78rem;
    color: {THEME["muted"]};
    white-space: nowrap;
    margin-top: 4px;
}}
.page-badge strong {{
    color: {THEME["text"]};
    font-weight: 600;
}}

/* ── KPI cards ── */
.kpi-section {{
    margin-top: 22px;
    margin-bottom: 6px;
}}
.kpi-section-label {{
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: {THEME["dim"]};
    margin-bottom: 10px;
}}
.kpi-grid {{ margin-bottom: 4px; }}
.kpi-card-sm .kpi-value {{
    font-size: 1.35rem;
}}
.kpi-card-sm .kpi-icon {{
    width: 28px;
    height: 28px;
    font-size: 12px;
}}
.kpi-card {{
    background: {THEME["surface"]};
    border: 1px solid {THEME["border"]};
    border-radius: 12px;
    padding: 20px 20px 18px 20px;
    position: relative;
    overflow: hidden;
    height: 100%;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}}
.kpi-card:hover {{
    border-color: {THEME["border_light"]};
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
}}
.kpi-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent);
}}
.kpi-top {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
}}
.kpi-label {{
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: {THEME["dim"]};
}}
.kpi-icon {{
    width: 32px;
    height: 32px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    background: var(--icon-bg);
    color: var(--accent);
}}
.kpi-value {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.65rem;
    font-weight: 800;
    color: {THEME["text"]};
    letter-spacing: -0.03em;
    line-height: 1.1;
    margin-bottom: 6px;
}}
.kpi-sub {{
    font-size: 0.78rem;
    color: {THEME["muted"]};
    line-height: 1.4;
}}

/* ── Section panels ── */
.section-block {{ margin-top: 32px; }}
.section-header {{
    display: flex;
    align-items: baseline;
    gap: 12px;
    margin-bottom: 16px;
}}
.section-title {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: {THEME["text"]};
    margin: 0;
}}
.section-desc {{
    font-size: 0.82rem;
    color: {THEME["dim"]};
    margin: 0;
}}
.chart-panel {{
    background: {THEME["surface"]};
    border: 1px solid {THEME["border"]};
    border-radius: 12px;
    padding: 20px 16px 8px 16px;
    margin-bottom: 4px;
}}
.chart-panel-sm {{
    background: {THEME["surface"]};
    border: 1px solid {THEME["border"]};
    border-radius: 12px;
    padding: 16px 12px 4px 12px;
}}

/* ── Sidebar branding ── */
.sidebar-brand {{
    padding: 4px 0 20px 0;
    border-bottom: 1px solid {THEME["border"]};
    margin-bottom: 20px;
}}
.sidebar-brand-name {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.05rem;
    font-weight: 800;
    color: {THEME["text"]};
    margin: 0 0 2px 0;
}}
.sidebar-brand-sub {{
    font-size: 0.78rem;
    color: {THEME["dim"]};
    margin: 0;
}}
.sidebar-stat {{
    background: {THEME["surface_2"]};
    border: 1px solid {THEME["border"]};
    border-radius: 8px;
    padding: 12px 14px;
    margin: 8px 0 16px 0;
}}
.sidebar-stat-label {{
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: {THEME["dim"]};
    margin-bottom: 4px;
}}
.sidebar-stat-value {{
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: {THEME["text"]};
}}

/* Streamlit widget overrides */
[data-testid="stMultiSelect"] > label,
[data-testid="stDownloadButton"] > button {{
    font-size: 0.85rem;
}}
div[data-testid="stMetric"] {{
    background: {THEME["surface_2"]};
    border: 1px solid {THEME["border"]};
    border-radius: 8px;
    padding: 12px;
}}

.stTabs [data-baseweb="tab-list"] {{
    gap: 4px;
    background: {THEME["surface"]};
    border: 1px solid {THEME["border"]};
    border-radius: 10px;
    padding: 4px;
}}
.stTabs [data-baseweb="tab"] {{
    border-radius: 7px;
    font-size: 0.82rem;
    font-weight: 600;
    color: {THEME["muted"]};
    padding: 8px 16px;
}}
.stTabs [aria-selected="true"] {{
    background: {THEME["surface_2"]} !important;
    color: {THEME["text"]} !important;
}}

[data-testid="stDataFrame"] {{
    border: 1px solid {THEME["border"]};
    border-radius: 10px;
    overflow: hidden;
}}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_raw():
    return pd.read_csv(DATA_PATH)


@st.cache_data
def load_summary():
    raw = load_raw()
    ventas = (
        raw[raw["Tipo"] == "venta"]
        .groupby(["Mes", "Mes_Num"], as_index=False)["Monto"]
        .sum()
        .rename(columns={"Monto": "Ventas"})
    )
    costos = (
        raw[raw["Tipo"] == "costo"]
        .groupby(["Mes", "Mes_Num"], as_index=False)["Monto"]
        .sum()
        .rename(columns={"Monto": "Costos"})
    )
    gastos = (
        raw[raw["Tipo"] == "gasto"]
        .groupby(["Mes", "Mes_Num"], as_index=False)["Monto"]
        .sum()
        .rename(columns={"Monto": "Gastos"})
    )
    df = ventas.merge(costos, on=["Mes", "Mes_Num"]).merge(gastos, on=["Mes", "Mes_Num"])
    df["Utilidad"] = df["Ventas"] - df["Gastos"] - df["Costos"]
    df["Margen_Pct"] = (df["Utilidad"] / df["Ventas"] * 100).round(2)
    df["Mes"] = pd.Categorical(df["Mes"], categories=MES_ORDER, ordered=True)
    return df.sort_values("Mes_Num").reset_index(drop=True)


def fmt(v):
    return f"${v:,.0f}"


def pct(v):
    return f"{v:.1f}%"


def base_layout(fig, height=360, legend=True):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=THEME["text"], family="Inter, sans-serif", size=12),
        margin=dict(l=8, r=8, t=36 if legend else 16, b=8),
        height=height,
        hoverlabel=dict(
            bgcolor=THEME["surface_2"],
            bordercolor=THEME["border"],
            font=dict(color=THEME["text"], family="Inter"),
        ),
    )
    fig.update_xaxes(
        showgrid=False,
        tickfont=dict(size=11, color=THEME["muted"]),
        linecolor=THEME["border"],
        linewidth=1,
    )
    fig.update_yaxes(
        gridcolor=THEME["border"],
        gridwidth=1,
        zerolinecolor=THEME["border"],
        tickfont=dict(size=11, color=THEME["muted"]),
        tickprefix="$",
        tickformat=",.0f",
    )
    if legend:
        fig.update_layout(
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="left",
                x=0,
                bgcolor="rgba(0,0,0,0)",
                font=dict(size=11, color=THEME["muted"]),
            )
        )
    return fig


def kpi_card(label, value, sub, accent, icon, icon_bg, small=False):
    cls = "kpi-card kpi-card-sm" if small else "kpi-card"
    return f"""
    <div class="{cls}" style="--accent:{accent};--icon-bg:{icon_bg}">
        <div class="kpi-top">
            <div class="kpi-label">{label}</div>
            <div class="kpi-icon">{icon}</div>
        </div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>"""


def render_kpi_section(title, cards, cols=4, small=False):
    st.markdown(f'<div class="kpi-section"><div class="kpi-section-label">{title}</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="kpi-grid">', unsafe_allow_html=True)
    columns = st.columns(cols)
    for col, (label, value, sub, accent, icon, icon_bg) in zip(columns, cards):
        with col:
            st.markdown(kpi_card(label, value, sub, accent, icon, icon_bg, small=small), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def compute_kpis(dff, raw, sel_nums):
    n = len(dff)
    empty = {
        "t_ventas": 0, "t_gastos": 0, "t_costos": 0, "t_egresos": 0, "t_utilidad": 0,
        "margen_bruto": 0, "margen_contrib": 0, "pct_mp": 0, "pct_gastos": 0, "pct_egresos": 0,
        "prom_ventas": 0, "prom_utilidad": 0, "best_mes": "—", "worst_mes": "—",
        "best_util": 0, "worst_util": 0, "meses_positivos": 0, "n_meses": 0,
        "top_rubro": "—", "top_rubro_pct": 0, "mom_ventas": None,
    }
    if n == 0:
        return empty

    t_ventas = dff["Ventas"].sum()
    t_gastos = dff["Gastos"].sum()
    t_costos = dff["Costos"].sum()
    t_egresos = t_gastos + t_costos
    t_utilidad = dff["Utilidad"].sum()

    best_row = dff.loc[dff["Utilidad"].idxmax()]
    worst_row = dff.loc[dff["Utilidad"].idxmin()]

    cat_gastos = (
        raw[(raw["Mes_Num"].isin(sel_nums)) & (raw["Tipo"] == "gasto")]
        .groupby("Categoria")["Monto"]
        .sum()
    )
    if len(cat_gastos) and t_gastos:
        top_rubro = cat_gastos.idxmax().replace("GASTOS DE ", "").title()
        top_rubro_pct = cat_gastos.max() / t_gastos * 100
    else:
        top_rubro = "—"
        top_rubro_pct = 0

    mom_ventas = None
    if n >= 2:
        first, last = dff["Ventas"].iloc[0], dff["Ventas"].iloc[-1]
        mom_ventas = (last / first - 1) * 100 if first else None

    return {
        "t_ventas": t_ventas,
        "t_gastos": t_gastos,
        "t_costos": t_costos,
        "t_egresos": t_egresos,
        "t_utilidad": t_utilidad,
        "margen_bruto": t_utilidad / t_ventas * 100 if t_ventas else 0,
        "margen_contrib": (t_ventas - t_costos) / t_ventas * 100 if t_ventas else 0,
        "pct_mp": t_costos / t_ventas * 100 if t_ventas else 0,
        "pct_gastos": t_gastos / t_ventas * 100 if t_ventas else 0,
        "pct_egresos": t_egresos / t_ventas * 100 if t_ventas else 0,
        "prom_ventas": dff["Ventas"].mean(),
        "prom_utilidad": dff["Utilidad"].mean(),
        "best_mes": str(best_row["Mes"]),
        "worst_mes": str(worst_row["Mes"]),
        "best_util": best_row["Utilidad"],
        "worst_util": worst_row["Utilidad"],
        "meses_positivos": int((dff["Utilidad"] > 0).sum()),
        "n_meses": n,
        "top_rubro": top_rubro,
        "top_rubro_pct": top_rubro_pct,
        "mom_ventas": mom_ventas,
    }


raw = load_raw()
df = load_summary()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <p class="sidebar-brand-name">Pepe Salcedo</p>
        <p class="sidebar-brand-sub">Panel de Control Financiero</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Período")
    meses_opts = df["Mes"].tolist()
    sel = st.multiselect(
        "Meses a incluir",
        meses_opts,
        default=meses_opts,
        label_visibility="collapsed",
    )

    dff = df[df["Mes"].isin(sel)] if sel else df

    st.markdown(f"""
    <div class="sidebar-stat">
        <div class="sidebar-stat-label">Período activo</div>
        <div class="sidebar-stat-value">{len(dff)} de 12 meses</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Exportar")
    csv = raw.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Descargar data.csv",
        csv,
        "data.csv",
        "text/csv",
        use_container_width=True,
    )
    st.caption(f"{len(raw):,} registros · {raw['Codigo'].nunique()} cuentas contables")

    st.markdown("---")
    st.caption("Datos calculados en tiempo real desde el CSV fuente.")

# ── Header ────────────────────────────────────────────────────────────────────
if len(dff) > 1:
    period_label = f"{dff['Mes'].iloc[0]} – {dff['Mes'].iloc[-1]}"
elif len(dff) == 1:
    period_label = str(dff["Mes"].iloc[0])
else:
    period_label = "Sin datos"

st.markdown(f"""
<div class="page-header">
    <div class="page-header-left">
        <div class="page-eyebrow">Reporte Ejecutivo · 2025</div>
        <h1 class="page-title">Dashboard Financiero</h1>
        <p class="page-subtitle">Análisis de ventas, costos operativos y utilidad bruta</p>
    </div>
    <div class="page-badge">Período: <strong>{period_label}</strong></div>
</div>
""", unsafe_allow_html=True)

# ── KPIs ──────────────────────────────────────────────────────────────────────
sel_nums = dff["Mes_Num"].tolist() if len(dff) else []
k = compute_kpis(dff, raw, sel_nums)

mom_sub = f"{k['mom_ventas']:+.1f}% vs. primer mes" if k["mom_ventas"] is not None else "Selecciona 2+ meses"

render_kpi_section("Resultados del período", [
    ("Ventas Totales", fmt(k["t_ventas"]), f"Promedio {fmt(k['prom_ventas'])}/mes", THEME["ventas"], "↗", "rgba(56,189,248,0.12)"),
    ("Total Egresos", fmt(k["t_egresos"]), "Gastos operativos + materia prima", THEME["gastos"], "Σ", "rgba(248,113,113,0.12)"),
    ("Utilidad Bruta", fmt(k["t_utilidad"]), "Ventas − egresos totales", THEME["utilidad"], "◉", "rgba(52,211,153,0.12)"),
    ("Margen Bruto", pct(k["margen_bruto"]), "Utilidad bruta / ventas", THEME["accent"], "%", "rgba(129,140,248,0.12)"),
])

render_kpi_section("Estructura de costos", [
    ("Materia Prima", fmt(k["t_costos"]), f"{k['pct_mp']:.1f}% de ventas", THEME["costos"], "◈", "rgba(251,191,36,0.12)"),
    ("Gastos Operativos", fmt(k["t_gastos"]), f"{k['pct_gastos']:.1f}% de ventas", THEME["gastos"], "◎", "rgba(248,113,113,0.12)"),
    ("Margen Contribución", pct(k["margen_contrib"]), "Ventas − materia prima", "#2dd4bf", "△", "rgba(45,212,191,0.12)"),
    ("Egresos / Ventas", pct(k["pct_egresos"]), "Costo total sobre ingresos", "#fb923c", "÷", "rgba(251,146,60,0.12)"),
], small=True)

render_kpi_section("Indicadores operativos", [
    ("Mejor Mes", k["best_mes"], f"Utilidad {fmt(k['best_util'])}", THEME["utilidad"], "▲", "rgba(52,211,153,0.12)"),
    ("Peor Mes", k["worst_mes"], f"Utilidad {fmt(k['worst_util'])}", THEME["gastos"], "▼", "rgba(248,113,113,0.12)"),
    ("Meses Rentables", f"{k['meses_positivos']}/{k['n_meses']}", "Meses con utilidad positiva", THEME["ventas"], "✓", "rgba(56,189,248,0.12)"),
    ("Mayor Rubro de Gasto", k["top_rubro"], f"{k['top_rubro_pct']:.1f}% del total operativo", THEME["accent"], "◆", "rgba(129,140,248,0.12)"),
], small=True)

if k["mom_ventas"] is not None:
    trend_color = THEME["utilidad"] if k["mom_ventas"] >= 0 else THEME["gastos"]
    render_kpi_section("Tendencia", [
        ("Variación de Ventas", pct(k["mom_ventas"]), mom_sub, trend_color, "↔", "rgba(129,140,248,0.12)"),
        ("Utilidad Promedio", fmt(k["prom_utilidad"]), "Por mes en el período", THEME["utilidad"], "≈", "rgba(52,211,153,0.12)"),
    ], cols=2, small=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab_resumen, tab_analisis, tab_detalle = st.tabs(["Resumen", "Análisis", "Detalle"])

with tab_resumen:
    st.markdown("""
    <div class="section-block">
        <div class="section-header">
            <p class="section-title">Comparativo Mensual</p>
            <p class="section-desc">Ventas vs. egresos por mes</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    fig1 = go.Figure()
    for col, name, color in [
        ("Ventas", "Ventas", THEME["ventas"]),
        ("Gastos", "Gastos Operativos", THEME["gastos"]),
        ("Costos", "Materia Prima", THEME["costos"]),
    ]:
        fig1.add_trace(go.Bar(
            x=dff["Mes"], y=dff[col], name=name,
            marker=dict(color=color, line=dict(width=0), cornerradius=4),
            hovertemplate=f"<b>{name}</b><br>%{{x}}<br>$%{{y:,.0f}}<extra></extra>",
        ))
    fig1.update_layout(barmode="group", bargap=0.22, bargroupgap=0.08)
    base_layout(fig1, height=380)
    st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
    st.plotly_chart(fig1, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="section-block">
        <div class="section-header">
            <p class="section-title">Composición de Egresos</p>
            <p class="section-desc">Gastos y costos apilados frente a la línea de ventas</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(
        x=dff["Mes"], y=dff["Ventas"], name="Ventas",
        mode="lines",
        line=dict(color=THEME["ventas"], width=2.5, dash="dot"),
        hovertemplate="Ventas: $%{y:,.0f}<extra></extra>",
    ))
    fig4.add_trace(go.Scatter(
        x=dff["Mes"], y=dff["Costos"], name="Materia Prima",
        stackgroup="one",
        fillcolor="rgba(251,191,36,0.35)",
        line=dict(color=THEME["costos"], width=0),
        hovertemplate="Materia Prima: $%{y:,.0f}<extra></extra>",
    ))
    fig4.add_trace(go.Scatter(
        x=dff["Mes"], y=dff["Gastos"], name="Gastos Operativos",
        stackgroup="one",
        fillcolor="rgba(248,113,113,0.35)",
        line=dict(color=THEME["gastos"], width=0),
        hovertemplate="Gastos: $%{y:,.0f}<extra></extra>",
    ))
    base_layout(fig4, height=340)
    fig4.update_layout(hovermode="x unified")
    st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
    st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with tab_analisis:
    c_left, c_right = st.columns(2)

    with c_left:
        st.markdown("""
        <div class="section-header">
            <p class="section-title">Utilidad Bruta</p>
            <p class="section-desc">Resultado mensual</p>
        </div>
        """, unsafe_allow_html=True)
        fig2 = go.Figure()
        colors = [THEME["utilidad"] if v >= 0 else THEME["gastos"] for v in dff["Utilidad"]]
        fig2.add_trace(go.Scatter(
            x=dff["Mes"], y=dff["Utilidad"],
            mode="lines+markers",
            line=dict(color=THEME["utilidad"], width=2.5, shape="spline"),
            marker=dict(size=7, color=colors, line=dict(width=2, color=THEME["surface"])),
            fill="tozeroy",
            fillcolor="rgba(52,211,153,0.08)",
            hovertemplate="<b>%{x}</b><br>Utilidad: $%{y:,.0f}<extra></extra>",
        ))
        fig2.add_hline(y=0, line_dash="dot", line_color=THEME["dim"], line_width=1)
        base_layout(fig2, height=300, legend=False)
        st.markdown('<div class="chart-panel-sm">', unsafe_allow_html=True)
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with c_right:
        st.markdown("""
        <div class="section-header">
            <p class="section-title">Margen de Utilidad</p>
            <p class="section-desc">Porcentaje sobre ventas</p>
        </div>
        """, unsafe_allow_html=True)
        bar_colors = [THEME["utilidad"] if v >= 0 else THEME["gastos"] for v in dff["Margen_Pct"]]
        fig3 = go.Figure(go.Bar(
            x=dff["Mes"], y=dff["Margen_Pct"],
            marker=dict(color=bar_colors, cornerradius=4),
            hovertemplate="<b>%{x}</b><br>Margen: %{y:.1f}%<extra></extra>",
        ))
        fig3.add_hline(y=0, line_dash="dot", line_color=THEME["dim"], line_width=1)
        base_layout(fig3, height=300, legend=False)
        fig3.update_yaxes(tickprefix="", ticksuffix="%", tickformat=".1f")
        st.markdown('<div class="chart-panel-sm">', unsafe_allow_html=True)
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    # Category breakdown
    st.markdown("""
    <div class="section-block">
        <div class="section-header">
            <p class="section-title">Distribución de Gastos por Categoría</p>
            <p class="section-desc">Participación del total de egresos operativos</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    cat_gastos = (
        raw[(raw["Mes_Num"].isin(sel_nums)) & (raw["Tipo"] == "gasto")]
        .groupby("Categoria")["Monto"]
        .sum()
        .reset_index()
        .sort_values("Monto", ascending=False)
    )

    palette = ["#38bdf8", "#f87171", "#fbbf24", "#34d399", "#818cf8", "#fb923c"]
    fig5 = go.Figure(go.Pie(
        labels=cat_gastos["Categoria"],
        values=cat_gastos["Monto"],
        hole=0.55,
        marker=dict(colors=palette[: len(cat_gastos)], line=dict(color=THEME["surface"], width=2)),
        textinfo="label+percent",
        textfont=dict(size=11, color=THEME["text"]),
        hovertemplate="<b>%{label}</b><br>$%{value:,.0f}<br>%{percent}<extra></extra>",
    ))
    fig5.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=THEME["text"], family="Inter"),
        margin=dict(l=0, r=0, t=16, b=0),
        height=380,
        showlegend=False,
    )
    st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
    st.plotly_chart(fig5, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with tab_detalle:
    st.markdown("""
    <div class="section-header">
        <p class="section-title">Resumen Mensual</p>
        <p class="section-desc">Cifras consolidadas por mes</p>
    </div>
    """, unsafe_allow_html=True)

    display = dff[["Mes", "Ventas", "Gastos", "Costos", "Utilidad", "Margen_Pct"]].copy()
    display["Total Egresos"] = display["Gastos"] + display["Costos"]
    display["Margen Contrib. %"] = ((display["Ventas"] - display["Costos"]) / display["Ventas"] * 100).round(2)
    display = display[["Mes", "Ventas", "Gastos", "Costos", "Total Egresos", "Utilidad", "Margen Contrib. %", "Margen_Pct"]]
    display.columns = [
        "Mes", "Ventas", "Gastos Operativos", "Materia Prima",
        "Total Egresos", "Utilidad Bruta", "Margen Contrib. %", "Margen Bruto %",
    ]
    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Mes": st.column_config.TextColumn("Mes", width="medium"),
            "Ventas": st.column_config.NumberColumn("Ventas", format="$%.2f"),
            "Gastos Operativos": st.column_config.NumberColumn("Gastos Operativos", format="$%.2f"),
            "Materia Prima": st.column_config.NumberColumn("Materia Prima", format="$%.2f"),
            "Total Egresos": st.column_config.NumberColumn("Total Egresos", format="$%.2f"),
            "Utilidad Bruta": st.column_config.NumberColumn("Utilidad Bruta", format="$%.2f"),
            "Margen Contrib. %": st.column_config.NumberColumn("Margen Contrib. %", format="%.2f%%"),
            "Margen Bruto %": st.column_config.NumberColumn("Margen Bruto %", format="%.2f%%"),
        },
    )

    st.markdown("""
    <div class="section-block">
        <div class="section-header">
            <p class="section-title">Desglose por Cuenta Contable</p>
            <p class="section-desc">Detalle acumulado del período seleccionado</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    detalle = raw[raw["Mes_Num"].isin(sel_nums)].copy()
    cat = (
        detalle.groupby(["Tipo", "Categoria", "Subcategoria", "Codigo", "Concepto"], dropna=False)["Monto"]
        .sum()
        .reset_index()
        .sort_values(["Tipo", "Categoria", "Subcategoria", "Codigo"])
    )
    cat = cat.rename(columns={
        "Tipo": "Tipo",
        "Categoria": "Categoría",
        "Subcategoria": "Subcategoría",
        "Codigo": "Código",
        "Concepto": "Concepto",
        "Monto": "Total",
    })
    st.dataframe(
        cat,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Total": st.column_config.NumberColumn("Total", format="$%.2f"),
            "Subcategoría": st.column_config.TextColumn("Subcategoría"),
        },
    )
