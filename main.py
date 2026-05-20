from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

DATA_PATH = Path(__file__).parent / "data.csv"

st.set_page_config(
    page_title="Transformadora de Hules y Plásticos - Dashboard Financiero",
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

CAT_MO = "GASTOS DE MANO DE OBRA"
CAT_FIN = "GASTOS FINANCIEROS"
SCENARIO_PRESETS = {
    "Conservador": {
        "target_sales": 24_000_000,
        "shifts_pct": 22,
        "regional_push_pct": 10,
        "marketing_pct": 1.8,
        "t90_energy_pct": 12,
        "t90_cycle_pct": 7,
    },
    "Base": {
        "target_sales": 30_000_000,
        "shifts_pct": 35,
        "regional_push_pct": 18,
        "marketing_pct": 2.5,
        "t90_energy_pct": 22,
        "t90_cycle_pct": 12,
    },
    "Agresivo": {
        "target_sales": 36_000_000,
        "shifts_pct": 50,
        "regional_push_pct": 28,
        "marketing_pct": 3.8,
        "t90_energy_pct": 30,
        "t90_cycle_pct": 18,
    },
}

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

.scenario-shell {{
    background: linear-gradient(160deg, rgba(24,28,38,0.9), rgba(18,21,28,0.92));
    border: 1px solid {THEME["border"]};
    border-radius: 14px;
    padding: 16px 18px;
    margin-bottom: 14px;
}}
.scenario-shell-title {{
    margin: 0 0 4px 0;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: {THEME["text"]};
}}
.scenario-shell-desc {{
    margin: 0;
    font-size: 0.82rem;
    color: {THEME["muted"]};
}}
.scenario-chip {{
    display: inline-block;
    margin: 8px 8px 0 0;
    padding: 6px 10px;
    border-radius: 999px;
    font-size: 0.74rem;
    font-weight: 600;
    color: {THEME["text"]};
    background: {THEME["surface_2"]};
    border: 1px solid {THEME["border"]};
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
    df = df.sort_values("Mes_Num").reset_index(drop=True)
    return enrich_monthly(df, raw)


def enrich_monthly(df, raw):
    mo = (
        raw[raw["Categoria"] == CAT_MO]
        .groupby(["Mes", "Mes_Num"], as_index=False)["Monto"]
        .sum()
        .rename(columns={"Monto": "ManoObra"})
    )
    fin = (
        raw[raw["Categoria"] == CAT_FIN]
        .groupby(["Mes", "Mes_Num"], as_index=False)["Monto"]
        .sum()
        .rename(columns={"Monto": "GastosFin"})
    )
    intereses = (
        raw[(raw["Categoria"] == CAT_FIN) & (raw["Concepto"] == "INTERESES")]
        .groupby(["Mes", "Mes_Num"], as_index=False)["Monto"]
        .sum()
        .rename(columns={"Monto": "Intereses"})
    )
    out = df.merge(mo, on=["Mes", "Mes_Num"], how="left")
    out = out.merge(fin, on=["Mes", "Mes_Num"], how="left")
    out = out.merge(intereses, on=["Mes", "Mes_Num"], how="left")
    for col in ("ManoObra", "GastosFin", "Intereses"):
        out[col] = out[col].fillna(0)

    out["Margen_Neto_Pct"] = (out["Utilidad"] / out["Ventas"] * 100).round(2)
    out["Margen_Bruto_Pct"] = ((out["Ventas"] - out["Costos"]) / out["Ventas"] * 100).round(2)
    out["Pct_MP"] = (out["Costos"] / out["Ventas"] * 100).round(2)
    out["Pct_MO"] = (out["ManoObra"] / out["Ventas"] * 100).round(2)
    out["Pct_Fin"] = (out["GastosFin"] / out["Ventas"] * 100).round(2)
    out["EBITDA"] = out["Utilidad"] + out["Intereses"]
    out["EBITDA_Pct"] = (out["EBITDA"] / out["Ventas"] * 100).round(2)
    out["ROI_Pct"] = (out["Utilidad"] / (out["Costos"] + out["Gastos"]) * 100).round(2)
    mc = (out["Ventas"] - out["Costos"]) / out["Ventas"]
    out["Break_Even"] = (out["Gastos"] / mc).where(mc > 0)
    out["MoM_Ventas"] = (out["Ventas"].pct_change() * 100).round(1)
    return out


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


def pct_layout(fig, height=360, legend=True):
    fig = base_layout(fig, height=height, legend=legend)
    fig.update_yaxes(tickprefix="", ticksuffix="%", tickformat=".1f")
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


def compute_kpis(dff, raw, sel_nums, full_df):
    n = len(dff)
    empty = {
        "t_ventas": 0, "t_gastos": 0, "t_costos": 0, "t_egresos": 0, "t_utilidad": 0,
        "margen_neto": 0, "margen_bruto": 0, "pct_mp": 0, "pct_mo": 0, "pct_fin": 0,
        "pct_gastos": 0, "pct_egresos": 0, "ebitda": 0, "ebitda_pct": 0, "roi": 0,
        "prom_ventas": 0, "prom_utilidad": 0, "prom_be": 0,
        "best_mes": "—", "worst_mes": "—", "best_util": 0, "worst_util": 0,
        "best_ventas_mes": "—", "worst_ventas_mes": "—", "best_ventas": 0, "worst_ventas": 0,
        "meses_positivos": 0, "n_meses": 0, "cobertura": 0,
        "mom_ventas": None, "mom_sub": "—",
    }
    if n == 0:
        return empty

    t_ventas = dff["Ventas"].sum()
    t_gastos = dff["Gastos"].sum()
    t_costos = dff["Costos"].sum()
    t_egresos = t_gastos + t_costos
    t_utilidad = dff["Utilidad"].sum()
    t_mo = dff["ManoObra"].sum()
    t_fin = dff["GastosFin"].sum()
    t_intereses = dff["Intereses"].sum()
    t_ebitda = t_utilidad + t_intereses

    best_row = dff.loc[dff["Utilidad"].idxmax()]
    worst_row = dff.loc[dff["Utilidad"].idxmin()]
    best_v_row = dff.loc[dff["Ventas"].idxmax()]
    worst_v_row = dff.loc[dff["Ventas"].idxmin()]

    prom_be = dff["Break_Even"].mean() if n else 0

    prom_gastos = dff["Gastos"].mean()
    prom_ventas = dff["Ventas"].mean()
    cobertura = prom_ventas / prom_gastos if prom_gastos else 0

    mom_ventas = None
    mom_sub = "—"
    if n >= 2:
        last_mom = dff["MoM_Ventas"].iloc[-1]
        if pd.notna(last_mom):
            mom_ventas = last_mom
            mom_sub = f"vs. {dff['Mes'].iloc[-2]} ({fmt(dff['Ventas'].iloc[-2])})"
    elif n == 1:
        pos = full_df.index[full_df["Mes"] == dff["Mes"].iloc[0]]
        if len(pos) and pos[0] > 0:
            prev = full_df.iloc[pos[0] - 1]
            cur = dff.iloc[0]
            if prev["Ventas"]:
                mom_ventas = (cur["Ventas"] / prev["Ventas"] - 1) * 100
                mom_sub = f"vs. {prev['Mes']} ({fmt(prev['Ventas'])})"

    return {
        "t_ventas": t_ventas,
        "t_gastos": t_gastos,
        "t_costos": t_costos,
        "t_egresos": t_egresos,
        "t_utilidad": t_utilidad,
        "margen_neto": t_utilidad / t_ventas * 100 if t_ventas else 0,
        "margen_bruto": (t_ventas - t_costos) / t_ventas * 100 if t_ventas else 0,
        "pct_mp": t_costos / t_ventas * 100 if t_ventas else 0,
        "pct_mo": t_mo / t_ventas * 100 if t_ventas else 0,
        "pct_fin": t_fin / t_ventas * 100 if t_ventas else 0,
        "pct_gastos": t_gastos / t_ventas * 100 if t_ventas else 0,
        "pct_egresos": t_egresos / t_ventas * 100 if t_ventas else 0,
        "ebitda": t_ebitda,
        "ebitda_pct": t_ebitda / t_ventas * 100 if t_ventas else 0,
        "roi": t_utilidad / t_egresos * 100 if t_egresos else 0,
        "prom_ventas": prom_ventas,
        "prom_utilidad": dff["Utilidad"].mean(),
        "prom_be": prom_be,
        "best_mes": str(best_row["Mes"]),
        "worst_mes": str(worst_row["Mes"]),
        "best_util": best_row["Utilidad"],
        "worst_util": worst_row["Utilidad"],
        "best_ventas_mes": str(best_v_row["Mes"]),
        "worst_ventas_mes": str(worst_v_row["Mes"]),
        "best_ventas": best_v_row["Ventas"],
        "worst_ventas": worst_v_row["Ventas"],
        "meses_positivos": int((dff["Utilidad"] > 0).sum()),
        "n_meses": n,
        "cobertura": cobertura,
        "mom_ventas": mom_ventas,
        "mom_sub": mom_sub,
    }


def allocate_total(total, base_series, fallback_weights):
    base_sum = base_series.sum()
    if base_sum > 0:
        weights = base_series / base_sum
    else:
        weights = fallback_weights
    return weights.reset_index(drop=True) * total


def build_30m_scenario(base_df, raw, target_sales, shifts_pct, regional_push_pct, t90_energy_pct, t90_cycle_pct, marketing_pct):
    annual = {
        "ventas": float(base_df["Ventas"].sum()),
        "costos": float(base_df["Costos"].sum()),
        "gastos": float(base_df["Gastos"].sum()),
    }
    growth_factor = target_sales / annual["ventas"] if annual["ventas"] else 1.0

    base_mo = raw[raw["Categoria"] == CAT_MO]["Monto"].sum()
    base_fin = raw[raw["Categoria"] == CAT_FIN]["Monto"].sum()
    base_intereses = raw[(raw["Categoria"] == CAT_FIN) & (raw["Concepto"] == "INTERESES")]["Monto"].sum()
    base_electricidad = raw[raw["Concepto"] == "ELECTRICIDAD"]["Monto"].sum()
    base_marketing = raw[raw["Concepto"] == "PUBLICIDAD"]["Monto"].sum()
    base_logistica = raw[raw["Concepto"].isin(["FLETES", "TRANSPORTE", "CARRETERAS", "COMBUST VEH"])]["Monto"].sum()

    base_otros = annual["gastos"] - (base_mo + base_fin + base_electricidad + base_marketing + base_logistica)
    base_otros = max(base_otros, 0)

    # Materia prima sube con volumen, pero T90 reduce mermas.
    mp_fijo = annual["costos"] * 0.15
    mp_variable = annual["costos"] * 0.85
    proj_costos = mp_fijo + mp_variable * growth_factor * (1 - (t90_cycle_pct * 0.6))

    # Mano de obra: más turnos + eficiencia de productividad.
    mo_fijo = base_mo * 0.40
    mo_variable = base_mo * 0.60
    proj_mo = (mo_fijo + mo_variable * growth_factor) * (1 + shifts_pct) * (1 - t90_cycle_pct)

    # Electricidad: más carga, mitigada por T90.
    elec_fijo = base_electricidad * 0.25
    elec_variable = base_electricidad * 0.75
    proj_electricidad = elec_fijo + elec_variable * growth_factor * (1 - t90_energy_pct)

    # Logística comercial por expansión geográfica.
    log_fijo = base_logistica * 0.20
    log_variable = base_logistica * 0.80
    proj_logistica = (log_fijo + log_variable * growth_factor) * (1 + regional_push_pct)

    # Otros gastos operativos semi variables.
    otros_fijo = base_otros * 0.60
    otros_variable = base_otros * 0.40
    proj_otros = otros_fijo + otros_variable * growth_factor
    proj_fin = base_fin * growth_factor
    proj_intereses = base_intereses * growth_factor

    # Presupuesto comercial mínimo como % de ventas proyectadas.
    proj_marketing = max(base_marketing * growth_factor, target_sales * marketing_pct)

    proj_gastos = proj_mo + proj_electricidad + proj_logistica + proj_otros + proj_marketing + proj_fin
    proj_utilidad = target_sales - proj_costos - proj_gastos

    month_weights = (base_df["Ventas"] / base_df["Ventas"].sum()).reset_index(drop=True)
    out = base_df[["Mes", "Mes_Num", "Ventas", "Costos", "Gastos", "Utilidad"]].copy()
    out = out.rename(columns={
        "Ventas": "Ventas_Base",
        "Costos": "Costos_Base",
        "Gastos": "Gastos_Base",
        "Utilidad": "Utilidad_Base",
    })
    out["Ventas_30M"] = allocate_total(target_sales, base_df["Ventas"], month_weights)
    out["Costos_30M"] = allocate_total(proj_costos, base_df["Costos"], month_weights)
    out["MO_30M"] = allocate_total(
        proj_mo,
        raw[raw["Categoria"] == CAT_MO].groupby("Mes_Num")["Monto"].sum().reindex(out["Mes_Num"]).fillna(0).reset_index(drop=True),
        month_weights,
    )
    out["Electricidad_30M"] = allocate_total(
        proj_electricidad,
        raw[raw["Concepto"] == "ELECTRICIDAD"].groupby("Mes_Num")["Monto"].sum().reindex(out["Mes_Num"]).fillna(0).reset_index(drop=True),
        month_weights,
    )
    out["Logistica_30M"] = allocate_total(
        proj_logistica,
        raw[raw["Concepto"].isin(["FLETES", "TRANSPORTE", "CARRETERAS", "COMBUST VEH"])].groupby("Mes_Num")["Monto"].sum().reindex(out["Mes_Num"]).fillna(0).reset_index(drop=True),
        month_weights,
    )
    out["Marketing_30M"] = allocate_total(
        proj_marketing,
        raw[raw["Concepto"] == "PUBLICIDAD"].groupby("Mes_Num")["Monto"].sum().reindex(out["Mes_Num"]).fillna(0).reset_index(drop=True),
        month_weights,
    )
    out["Fin_30M"] = allocate_total(
        proj_fin,
        raw[raw["Categoria"] == CAT_FIN].groupby("Mes_Num")["Monto"].sum().reindex(out["Mes_Num"]).fillna(0).reset_index(drop=True),
        month_weights,
    )
    out["Intereses_30M"] = allocate_total(
        proj_intereses,
        raw[(raw["Categoria"] == CAT_FIN) & (raw["Concepto"] == "INTERESES")].groupby("Mes_Num")["Monto"].sum().reindex(out["Mes_Num"]).fillna(0).reset_index(drop=True),
        month_weights,
    )
    out["Otros_30M"] = allocate_total(
        proj_otros,
        (
            raw[
                ~raw["Categoria"].isin([CAT_MO, CAT_FIN])
                & ~raw["Concepto"].isin(["ELECTRICIDAD", "PUBLICIDAD", "FLETES", "TRANSPORTE", "CARRETERAS", "COMBUST VEH"])
                & (raw["Tipo"] == "gasto")
            ]
            .groupby("Mes_Num")["Monto"]
            .sum()
            .reindex(out["Mes_Num"])
            .fillna(0)
            .reset_index(drop=True)
        ),
        month_weights,
    )
    out["Gastos_30M"] = out["MO_30M"] + out["Electricidad_30M"] + out["Logistica_30M"] + out["Marketing_30M"] + out["Fin_30M"] + out["Otros_30M"]
    out["Utilidad_30M"] = out["Ventas_30M"] - out["Costos_30M"] - out["Gastos_30M"]
    out["Margen_30M_Pct"] = (out["Utilidad_30M"] / out["Ventas_30M"] * 100).round(2)

    annual_out = {
        "ventas_base": annual["ventas"],
        "ventas_30m": target_sales,
        "costos_base": annual["costos"],
        "costos_30m": proj_costos,
        "gastos_base": annual["gastos"],
        "gastos_30m": proj_gastos,
        "fin_30m": proj_fin,
        "mo_30m": proj_mo,
        "marketing_30m": proj_marketing,
        "logistica_30m": proj_logistica,
        "utilidad_base": annual["ventas"] - annual["costos"] - annual["gastos"],
        "utilidad_30m": proj_utilidad,
        "margen_base": ((annual["ventas"] - annual["costos"] - annual["gastos"]) / annual["ventas"] * 100) if annual["ventas"] else 0,
        "margen_30m": (proj_utilidad / target_sales * 100) if target_sales else 0,
        "growth_pct": (target_sales / annual["ventas"] - 1) * 100 if annual["ventas"] else 0,
    }
    return out.sort_values("Mes_Num").reset_index(drop=True), annual_out


def build_scenario_dashboard_frame(scenario_df):
    scen = scenario_df[["Mes", "Mes_Num"]].copy()
    scen["Ventas"] = scenario_df["Ventas_30M"]
    scen["Costos"] = scenario_df["Costos_30M"]
    scen["Gastos"] = scenario_df["Gastos_30M"]
    scen["Utilidad"] = scenario_df["Utilidad_30M"]
    scen["Margen_Neto_Pct"] = (scen["Utilidad"] / scen["Ventas"] * 100).round(2)
    scen["Margen_Bruto_Pct"] = ((scen["Ventas"] - scen["Costos"]) / scen["Ventas"] * 100).round(2)
    scen["ManoObra"] = scenario_df["MO_30M"]
    scen["GastosFin"] = scenario_df["Fin_30M"]
    scen["Intereses"] = scenario_df["Intereses_30M"]
    scen["Pct_MP"] = (scen["Costos"] / scen["Ventas"] * 100).round(2)
    scen["Pct_MO"] = (scen["ManoObra"] / scen["Ventas"] * 100).round(2)
    scen["Pct_Fin"] = (scen["GastosFin"] / scen["Ventas"] * 100).round(2)
    mc = (scen["Ventas"] - scen["Costos"]) / scen["Ventas"]
    scen["Break_Even"] = (scen["Gastos"] / mc).where(mc > 0)
    scen["ROI_Pct"] = (scen["Utilidad"] / (scen["Costos"] + scen["Gastos"]) * 100).round(2)
    scen["MoM_Ventas"] = (scen["Ventas"].pct_change() * 100).round(1)
    return scen


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
        <h1 class="page-title">Transformadora de Hules y Plásticos - Dashboard Financiero</h1>
        <p class="page-subtitle">Análisis de ventas, costos operativos y utilidad bruta</p>
    </div>
    <div class="page-badge">Período: <strong>{period_label}</strong></div>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
base_dff = dff.copy()
selected_scenario = st.radio(
    "Escenario activo",
    options=["Actual", "Conservador", "Agresivo", "Personalizado"],
    horizontal=True,
    key="selected_scenario_global",
)

scenario_monthly = None
scenario_slug = selected_scenario.lower().replace(" ", "_")
if selected_scenario == "Actual":
    dff = base_dff
    st.markdown("""
    <div class="scenario-shell">
        <p class="scenario-shell-title">Escenario activo: Actual</p>
        <p class="scenario-shell-desc">Vista operativa basada en los datos reales del período seleccionado.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    scenario_presets = {
        "Conservador": SCENARIO_PRESETS["Conservador"],
        "Agresivo": SCENARIO_PRESETS["Agresivo"],
    }
    if selected_scenario == "Personalizado":
        custom_col_1, custom_col_2, custom_col_3 = st.columns(3)
        with custom_col_1:
            custom_target = st.number_input(
                "Meta de ventas anual (MXN)",
                min_value=1_000_000,
                max_value=80_000_000,
                step=500_000,
                format="%d",
                value=30_000_000,
                key="custom_target_sales_input_global",
            )
            custom_shifts = st.slider("Impacto turnos extra MO (%)", min_value=0, max_value=80, step=1, value=35, key="custom_shifts_input_global")
        with custom_col_2:
            custom_regional = st.slider("Sobrecosto logístico (%)", min_value=0, max_value=60, step=1, value=18, key="custom_regional_input_global")
            custom_marketing = st.slider("Marketing como % de ventas", min_value=0.0, max_value=10.0, step=0.1, value=2.5, key="custom_marketing_input_global")
        with custom_col_3:
            custom_energy = st.slider("Ahorro energía T90 (%)", min_value=0, max_value=40, step=1, value=22, key="custom_energy_input_global")
            custom_cycle = st.slider("Eficiencia ciclo T90 (%)", min_value=0, max_value=35, step=1, value=12, key="custom_cycle_input_global")
        cfg = {
            "target_sales": custom_target,
            "shifts_pct": custom_shifts / 100,
            "regional_push_pct": custom_regional / 100,
            "marketing_pct": custom_marketing / 100,
            "t90_energy_pct": custom_energy / 100,
            "t90_cycle_pct": custom_cycle / 100,
        }
    else:
        preset = scenario_presets[selected_scenario]
        cfg = {
            "target_sales": preset["target_sales"],
            "shifts_pct": preset["shifts_pct"] / 100,
            "regional_push_pct": preset["regional_push_pct"] / 100,
            "marketing_pct": preset["marketing_pct"] / 100,
            "t90_energy_pct": preset["t90_energy_pct"] / 100,
            "t90_cycle_pct": preset["t90_cycle_pct"] / 100,
        }

    scenario_monthly, scenario_kpi = build_30m_scenario(df, raw, **cfg)
    scenario_view = build_scenario_dashboard_frame(scenario_monthly)
    dff = scenario_view[scenario_view["Mes"].isin(sel)].copy() if sel else scenario_view
    st.markdown(f"""
    <div class="scenario-shell">
        <p class="scenario-shell-title">Escenario activo: {selected_scenario}</p>
        <p class="scenario-shell-desc">Todos los tabs se actualizan con este escenario.</p>
        <span class="scenario-chip">Meta ventas: {fmt(cfg["target_sales"])}</span>
        <span class="scenario-chip">Crecimiento: {scenario_kpi["growth_pct"]:.1f}%</span>
        <span class="scenario-chip">Margen: {scenario_kpi["margen_30m"]:.1f}%</span>
    </div>
    """, unsafe_allow_html=True)

kpi_reference_df = df if selected_scenario == "Actual" else scenario_view
sel_nums = dff["Mes_Num"].tolist() if len(dff) else []
tab_resumen, tab_analisis, tab_detalle = st.tabs(["Resumen", "Análisis", "Detalle"])

with tab_resumen:
    k = compute_kpis(dff, raw, sel_nums, kpi_reference_df)

    render_kpi_section("Resultados del período", [
        ("Ventas Totales", fmt(k["t_ventas"]), f"Promedio {fmt(k['prom_ventas'])}/mes", THEME["ventas"], "↗", "rgba(56,189,248,0.12)"),
        ("Utilidad Bruta", fmt(k["t_utilidad"]), "Ventas − egresos totales", THEME["utilidad"], "◉", "rgba(52,211,153,0.12)"),
        ("Margen Neto", pct(k["margen_neto"]), "Utilidad / ventas", THEME["accent"], "%", "rgba(129,140,248,0.12)"),
        ("Margen Bruto", pct(k["margen_bruto"]), "Ventas − materia prima", "#2dd4bf", "△", "rgba(45,212,191,0.12)"),
    ])

    render_kpi_section("Eficiencia operativa", [
        ("Materia Prima", pct(k["pct_mp"]), f"{fmt(k['t_costos'])} en el período", THEME["costos"], "◈", "rgba(251,191,36,0.12)"),
        ("Mano de Obra", pct(k["pct_mo"]), "% de ventas", THEME["gastos"], "◎", "rgba(248,113,113,0.12)"),
        ("Gasto Financiero", pct(k["pct_fin"]), "Créditos, intereses y comisiones", "#818cf8", "₿", "rgba(129,140,248,0.12)"),
        ("EBITDA Aprox.", pct(k["ebitda_pct"]), f"{fmt(k['ebitda'])} · utilidad + intereses", "#a78bfa", "◉", "rgba(167,139,250,0.12)"),
    ], small=True)

    render_kpi_section("Rentabilidad y liquidez", [
        ("ROI Período", pct(k["roi"]), "Utilidad / total invertido", THEME["utilidad"], "↗", "rgba(52,211,153,0.12)"),
        ("Punto de Equilibrio", fmt(k["prom_be"]), "Ventas mínimas mensuales promedio", "#fb923c", "⚖", "rgba(251,146,60,0.12)"),
        ("Cobertura Gastos", f"{k['cobertura']:.1f}x", "Ventas promedio / gastos operativos", THEME["ventas"], "🛡", "rgba(56,189,248,0.12)"),
        ("Gastos / Ventas", pct(k["pct_gastos"]), f"{fmt(k['t_gastos'])} operativos", THEME["gastos"], "÷", "rgba(248,113,113,0.12)"),
    ], small=True)

    render_kpi_section("Indicadores operativos", [
        ("Mejor Mes (Utilidad)", k["best_mes"], fmt(k["best_util"]), THEME["utilidad"], "▲", "rgba(52,211,153,0.12)"),
        ("Peor Mes (Utilidad)", k["worst_mes"], fmt(k["worst_util"]), THEME["gastos"], "▼", "rgba(248,113,113,0.12)"),
        ("Mejor Mes (Ventas)", k["best_ventas_mes"], fmt(k["best_ventas"]), THEME["ventas"], "★", "rgba(56,189,248,0.12)"),
        ("Peor Mes (Ventas)", k["worst_ventas_mes"], fmt(k["worst_ventas"]), "#fb923c", "◇", "rgba(251,146,60,0.12)"),
    ], small=True)

    if k["mom_ventas"] is not None:
        trend_color = THEME["utilidad"] if k["mom_ventas"] >= 0 else THEME["gastos"]
        render_kpi_section("Tendencia", [
            ("Crecimiento MoM", f"{k['mom_ventas']:+.1f}%", k["mom_sub"], trend_color, "↔", "rgba(129,140,248,0.12)"),
            ("Utilidad Promedio", fmt(k["prom_utilidad"]), "Por mes en el período", THEME["utilidad"], "≈", "rgba(52,211,153,0.12)"),
            ("Meses Rentables", f"{k['meses_positivos']}/{k['n_meses']}", "Meses con utilidad positiva", THEME["accent"], "✓", "rgba(129,140,248,0.12)"),
        ], cols=3, small=True)
    else:
        render_kpi_section("Tendencia", [
            ("Meses Rentables", f"{k['meses_positivos']}/{k['n_meses']}", "Meses con utilidad positiva", THEME["accent"], "✓", "rgba(129,140,248,0.12)"),
        ], cols=1, small=True)

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

    st.markdown("""
    <div class="section-block">
        <div class="section-header">
            <p class="section-title">Ratios Clave Mes a Mes</p>
            <p class="section-desc">Materia prima, mano de obra, gasto financiero y margen neto sobre ventas</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    fig_ratios = go.Figure()
    for col, name, color in [
        ("Pct_MP", "Materia Prima %", THEME["costos"]),
        ("Pct_MO", "Mano de Obra %", THEME["gastos"]),
        ("Pct_Fin", "Gasto Financiero %", THEME["accent"]),
        ("Margen_Neto_Pct", "Margen Neto %", THEME["utilidad"]),
    ]:
        fig_ratios.add_trace(go.Scatter(
            x=dff["Mes"], y=dff[col], name=name,
            mode="lines+markers",
            line=dict(color=color, width=2),
            marker=dict(size=6),
            hovertemplate=f"<b>{name}</b><br>%{{x}}<br>%{{y:.1f}}%<extra></extra>",
        ))
    pct_layout(fig_ratios, height=340)
    st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
    st.plotly_chart(fig_ratios, use_container_width=True, config={"displayModeBar": False})
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
            <p class="section-title">Margen Neto</p>
            <p class="section-desc">Utilidad / ventas por mes</p>
        </div>
        """, unsafe_allow_html=True)
        bar_colors = [THEME["utilidad"] if v >= 0 else THEME["gastos"] for v in dff["Margen_Neto_Pct"]]
        fig3 = go.Figure(go.Bar(
            x=dff["Mes"], y=dff["Margen_Neto_Pct"],
            marker=dict(color=bar_colors, cornerradius=4),
            hovertemplate="<b>%{x}</b><br>Margen neto: %{y:.1f}%<extra></extra>",
        ))
        fig3.add_hline(y=0, line_dash="dot", line_color=THEME["dim"], line_width=1)
        pct_layout(fig3, height=300, legend=False)
        st.markdown('<div class="chart-panel-sm">', unsafe_allow_html=True)
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    c_mom, c_be = st.columns(2)

    with c_mom:
        st.markdown("""
        <div class="section-header">
            <p class="section-title">Crecimiento MoM de Ventas</p>
            <p class="section-desc">Variación vs. mes anterior</p>
        </div>
        """, unsafe_allow_html=True)
        mom_data = dff[dff["MoM_Ventas"].notna()]
        mom_colors = [THEME["utilidad"] if v >= 0 else THEME["gastos"] for v in mom_data["MoM_Ventas"]]
        fig_mom = go.Figure(go.Bar(
            x=mom_data["Mes"], y=mom_data["MoM_Ventas"],
            marker=dict(color=mom_colors, cornerradius=4),
            hovertemplate="<b>%{x}</b><br>MoM: %{y:+.1f}%<extra></extra>",
        ))
        fig_mom.add_hline(y=0, line_dash="dot", line_color=THEME["dim"], line_width=1)
        pct_layout(fig_mom, height=300, legend=False)
        st.markdown('<div class="chart-panel-sm">', unsafe_allow_html=True)
        st.plotly_chart(fig_mom, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with c_be:
        st.markdown("""
        <div class="section-header">
            <p class="section-title">Punto de Equilibrio vs Ventas</p>
            <p class="section-desc">Ventas mínimas para cubrir gastos operativos</p>
        </div>
        """, unsafe_allow_html=True)
        fig_be = go.Figure()
        fig_be.add_trace(go.Scatter(
            x=dff["Mes"], y=dff["Ventas"], name="Ventas",
            mode="lines+markers",
            line=dict(color=THEME["ventas"], width=2.5),
            marker=dict(size=7),
            hovertemplate="Ventas: $%{y:,.0f}<extra></extra>",
        ))
        fig_be.add_trace(go.Scatter(
            x=dff["Mes"], y=dff["Break_Even"], name="Punto de equilibrio",
            mode="lines+markers",
            line=dict(color="#fb923c", width=2, dash="dash"),
            marker=dict(size=7),
            hovertemplate="Break-even: $%{y:,.0f}<extra></extra>",
        ))
        base_layout(fig_be, height=300)
        fig_be.update_layout(hovermode="x unified")
        st.markdown('<div class="chart-panel-sm">', unsafe_allow_html=True)
        st.plotly_chart(fig_be, use_container_width=True, config={"displayModeBar": False})
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

    if selected_scenario == "Actual":
        cat_gastos = (
            raw[(raw["Mes_Num"].isin(sel_nums)) & (raw["Tipo"] == "gasto")]
            .groupby("Categoria")["Monto"]
            .sum()
            .reset_index()
            .sort_values("Monto", ascending=False)
        )
    else:
        scenario_scope = scenario_monthly[scenario_monthly["Mes"].isin(sel)].copy() if sel else scenario_monthly.copy()
        cat_gastos = pd.DataFrame(
            {
                "Categoria": [
                    "Mano de Obra",
                    "Gastos Financieros",
                    "Electricidad",
                    "Logística",
                    "Marketing",
                    "Otros",
                ],
                "Monto": [
                    scenario_scope["MO_30M"].sum(),
                    scenario_scope["Fin_30M"].sum(),
                    scenario_scope["Electricidad_30M"].sum(),
                    scenario_scope["Logistica_30M"].sum(),
                    scenario_scope["Marketing_30M"].sum(),
                    scenario_scope["Otros_30M"].sum(),
                ],
            }
        ).sort_values("Monto", ascending=False)
        cat_gastos = cat_gastos[cat_gastos["Monto"] > 0]

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

    display = dff[[
        "Mes", "Ventas", "Gastos", "Costos", "Utilidad",
        "MoM_Ventas", "Pct_MP", "Pct_MO", "Pct_Fin", "Break_Even", "ROI_Pct",
        "Margen_Bruto_Pct", "Margen_Neto_Pct",
    ]].copy()
    display["Total Egresos"] = display["Gastos"] + display["Costos"]
    display = display[[
        "Mes", "Ventas", "MoM_Ventas", "Gastos", "Costos", "Total Egresos", "Utilidad",
        "Pct_MP", "Pct_MO", "Pct_Fin", "Break_Even", "ROI_Pct",
        "Margen_Bruto_Pct", "Margen_Neto_Pct",
    ]]
    display.columns = [
        "Mes", "Ventas", "MoM %", "Gastos Operativos", "Materia Prima", "Total Egresos",
        "Utilidad Bruta", "MP %", "MO %", "Fin %", "Punto Equilibrio", "ROI %",
        "Margen Bruto %", "Margen Neto %",
    ]
    st.dataframe(
        display,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Mes": st.column_config.TextColumn("Mes", width="medium"),
            "Ventas": st.column_config.NumberColumn("Ventas", format="$%.2f"),
            "MoM %": st.column_config.NumberColumn("MoM %", format="%+.1f%%"),
            "Gastos Operativos": st.column_config.NumberColumn("Gastos Operativos", format="$%.2f"),
            "Materia Prima": st.column_config.NumberColumn("Materia Prima", format="$%.2f"),
            "Total Egresos": st.column_config.NumberColumn("Total Egresos", format="$%.2f"),
            "Utilidad Bruta": st.column_config.NumberColumn("Utilidad Bruta", format="$%.2f"),
            "MP %": st.column_config.NumberColumn("MP %", format="%.2f%%"),
            "MO %": st.column_config.NumberColumn("MO %", format="%.2f%%"),
            "Fin %": st.column_config.NumberColumn("Fin %", format="%.2f%%"),
            "Punto Equilibrio": st.column_config.NumberColumn("Punto Equilibrio", format="$%.2f"),
            "ROI %": st.column_config.NumberColumn("ROI %", format="%.2f%%"),
            "Margen Bruto %": st.column_config.NumberColumn("Margen Bruto %", format="%.2f%%"),
            "Margen Neto %": st.column_config.NumberColumn("Margen Neto %", format="%.2f%%"),
        },
    )

    if selected_scenario == "Actual":
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
    else:
        st.markdown("""
        <div class="section-block">
            <div class="section-header">
                <p class="section-title">Desglose del Escenario</p>
                <p class="section-desc">Composición mensual de costos y gastos proyectados</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        scenario_scope = scenario_monthly[scenario_monthly["Mes"].isin(sel)].copy() if sel else scenario_monthly.copy()
        scen_detail = scenario_scope[[
            "Mes", "Ventas_30M", "Costos_30M", "MO_30M", "Electricidad_30M", "Logistica_30M",
            "Marketing_30M", "Fin_30M", "Otros_30M", "Gastos_30M", "Utilidad_30M", "Margen_30M_Pct",
        ]].rename(columns={
            "Ventas_30M": "Ventas Escenario",
            "Costos_30M": "Materia Prima",
            "MO_30M": "Mano de Obra",
            "Electricidad_30M": "Electricidad",
            "Logistica_30M": "Logística",
            "Marketing_30M": "Marketing",
            "Fin_30M": "Gasto Financiero",
            "Otros_30M": "Otros Gastos",
            "Gastos_30M": "Gastos Totales",
            "Utilidad_30M": "Utilidad Escenario",
            "Margen_30M_Pct": "Margen Escenario %",
        })
        st.dataframe(
            scen_detail,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Ventas Escenario": st.column_config.NumberColumn("Ventas Escenario", format="$%.2f"),
                "Materia Prima": st.column_config.NumberColumn("Materia Prima", format="$%.2f"),
                "Mano de Obra": st.column_config.NumberColumn("Mano de Obra", format="$%.2f"),
                "Electricidad": st.column_config.NumberColumn("Electricidad", format="$%.2f"),
                "Logística": st.column_config.NumberColumn("Logística", format="$%.2f"),
                "Marketing": st.column_config.NumberColumn("Marketing", format="$%.2f"),
                "Gasto Financiero": st.column_config.NumberColumn("Gasto Financiero", format="$%.2f"),
                "Otros Gastos": st.column_config.NumberColumn("Otros Gastos", format="$%.2f"),
                "Gastos Totales": st.column_config.NumberColumn("Gastos Totales", format="$%.2f"),
                "Utilidad Escenario": st.column_config.NumberColumn("Utilidad Escenario", format="$%.2f"),
                "Margen Escenario %": st.column_config.NumberColumn("Margen Escenario %", format="%.2f%%"),
            },
        )
