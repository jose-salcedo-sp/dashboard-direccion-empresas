import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Dashboard Financiero — Pepe Salcedo",
    page_icon="📊",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.main { background: #0f0f13; }
[data-testid="stAppViewContainer"] { background: #0f0f13; }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] { background: #16161d; border-right: 1px solid #2a2a38; }

h1, h2, h3 { font-family: 'Syne', sans-serif !important; }

.kpi-card {
    background: linear-gradient(135deg, #1a1a24 0%, #1f1f2e 100%);
    border: 1px solid #2a2a3e;
    border-radius: 16px;
    padding: 24px 20px;
    text-align: center;
    transition: transform .2s;
}
.kpi-card:hover { transform: translateY(-3px); }
.kpi-label {
    font-size: 11px;
    font-weight: 500;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #6b6b8a;
    margin-bottom: 8px;
}
.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 4px;
}
.kpi-sub { font-size: 12px; color: #6b6b8a; }

.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: #e0e0f0;
    margin: 32px 0 16px 0;
    padding-bottom: 8px;
    border-bottom: 1px solid #2a2a3e;
}
</style>
""", unsafe_allow_html=True)

# ── Data ────────────────────────────────────────────────────────────────────
MES_ORDER = [
    'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
    'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre',
]

@st.cache_data
def load_raw():
    return pd.read_csv('data.csv')

@st.cache_data
def load_summary():
    raw = load_raw()
    ventas = (
        raw[raw['Tipo'] == 'venta']
        .groupby(['Mes', 'Mes_Num'], as_index=False)['Monto']
        .sum()
        .rename(columns={'Monto': 'Ventas'})
    )
    costos = (
        raw[raw['Tipo'] == 'costo']
        .groupby(['Mes', 'Mes_Num'], as_index=False)['Monto']
        .sum()
        .rename(columns={'Monto': 'Costos'})
    )
    gastos = (
        raw[raw['Tipo'] == 'gasto']
        .groupby(['Mes', 'Mes_Num'], as_index=False)['Monto']
        .sum()
        .rename(columns={'Monto': 'Gastos'})
    )
    df = ventas.merge(costos, on=['Mes', 'Mes_Num']).merge(gastos, on=['Mes', 'Mes_Num'])
    df['Utilidad'] = df['Ventas'] - df['Gastos'] - df['Costos']
    df['Margen_Pct'] = (df['Utilidad'] / df['Ventas'] * 100).round(2)
    df['Mes'] = pd.Categorical(df['Mes'], categories=MES_ORDER, ordered=True)
    return df.sort_values('Mes_Num').reset_index(drop=True)

raw = load_raw()
df = load_summary()

COLORS = {
    'ventas':   '#00d4ff',
    'gastos':   '#ff6b6b',
    'costos':   '#ffd166',
    'utilidad': '#06d6a0',
    'bg':       '#0f0f13',
    'card':     '#1a1a24',
    'grid':     '#2a2a3e',
    'text':     '#e0e0f0',
    'muted':    '#6b6b8a',
}

# ── Sidebar filters ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🗓 Filtros")
    meses_opts = df['Mes'].tolist()
    sel = st.multiselect("Seleccionar meses", meses_opts, default=meses_opts)
    st.markdown("---")
    st.markdown("### 📂 Datos fuente")
    csv = raw.to_csv(index=False).encode('utf-8')
    st.download_button("⬇ Descargar CSV", csv, "data.csv", "text/csv")
    st.caption(f"{len(raw):,} registros · {raw['Codigo'].nunique()} cuentas")
    st.markdown("---")
    st.caption("Dashboard Financiero · Pepe Salcedo")

dff = df[df['Mes'].isin(sel)] if sel else df

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div style="padding:32px 0 8px 0">
  <h1 style="color:#e0e0f0;font-size:36px;margin:0">📊 Dashboard Financiero</h1>
  <p style="color:#6b6b8a;font-size:15px;margin:4px 0 0 2px">Pepe Salcedo · Resumen Anual de Gastos, Costos y Ventas</p>
</div>
""", unsafe_allow_html=True)

# ── KPI cards ────────────────────────────────────────────────────────────────
t_ventas   = dff['Ventas'].sum()
t_gastos   = dff['Gastos'].sum()
t_costos   = dff['Costos'].sum()
t_utilidad = dff['Utilidad'].sum()
t_margen   = t_utilidad / t_ventas * 100 if t_ventas else 0

def fmt(v): return f"${v:,.0f}"
def pct(v): return f"{v:.1f}%"

k1, k2, k3, k4, k5 = st.columns(5)
cards = [
    (k1, "Ventas Totales",   fmt(t_ventas),   COLORS['ventas'],   f"{len(dff)} meses seleccionados"),
    (k2, "Gastos Totales",   fmt(t_gastos),   COLORS['gastos'],   f"{t_gastos/t_ventas*100:.1f}% de ventas"),
    (k3, "Costos Totales",   fmt(t_costos),   COLORS['costos'],   f"{t_costos/t_ventas*100:.1f}% de ventas"),
    (k4, "Utilidad Bruta",   fmt(t_utilidad), COLORS['utilidad'], "Ventas − Gastos − Costos"),
    (k5, "Margen de Utilidad", pct(t_margen), "#c77dff",          "Sobre ventas totales"),
]
for col, label, val, color, sub in cards:
    with col:
        st.markdown(f"""
        <div class="kpi-card">
          <div class="kpi-label">{label}</div>
          <div class="kpi-value" style="color:{color}">{val}</div>
          <div class="kpi-sub">{sub}</div>
        </div>""", unsafe_allow_html=True)

# ── Chart 1: Ventas vs Gastos vs Costos (grouped bars) ──────────────────────
st.markdown('<div class="section-title">Comparativo Mensual</div>', unsafe_allow_html=True)

fig1 = go.Figure()
for col, name, color in [
    ('Ventas','Ventas', COLORS['ventas']),
    ('Gastos','Gastos', COLORS['gastos']),
    ('Costos','Costos (Mat. Prima)', COLORS['costos']),
]:
    fig1.add_trace(go.Bar(
        x=dff['Mes'], y=dff[col], name=name,
        marker_color=color, marker_line_width=0,
        hovertemplate=f"<b>{name}</b><br>%{{x}}<br>$%{{y:,.0f}}<extra></extra>"
    ))

fig1.update_layout(
    barmode='group', bargap=0.18, bargroupgap=0.05,
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color=COLORS['text'], family='DM Sans'),
    legend=dict(orientation='h', y=1.08, x=0, bgcolor='rgba(0,0,0,0)'),
    margin=dict(l=0, r=0, t=40, b=0),
    height=360,
    xaxis=dict(showgrid=False, tickfont=dict(size=12)),
    yaxis=dict(gridcolor=COLORS['grid'], tickprefix='$', tickformat=',.0f'),
    hovermode='x unified',
)
st.plotly_chart(fig1, use_container_width=True)

# ── Chart 2: Utilidad line + Margen area ────────────────────────────────────
c_left, c_right = st.columns(2)

with c_left:
    st.markdown('<div class="section-title">Utilidad Bruta Mensual</div>', unsafe_allow_html=True)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=dff['Mes'], y=dff['Utilidad'], name='Utilidad',
        mode='lines+markers',
        line=dict(color=COLORS['utilidad'], width=3),
        marker=dict(size=8, color=[COLORS['utilidad'] if v >= 0 else COLORS['gastos'] for v in dff['Utilidad']]),
        fill='tozeroy',
        fillcolor='rgba(6,214,160,0.08)',
        hovertemplate="<b>%{x}</b><br>Utilidad: $%{y:,.0f}<extra></extra>"
    ))
    fig2.add_hline(y=0, line_dash='dot', line_color=COLORS['muted'], line_width=1)
    fig2.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text'], family='DM Sans'),
        margin=dict(l=0, r=0, t=40, b=0), height=300,
        xaxis=dict(showgrid=False, tickfont=dict(size=11)),
        yaxis=dict(gridcolor=COLORS['grid'], tickprefix='$', tickformat=',.0f'),
        showlegend=False,
    )
    st.plotly_chart(fig2, use_container_width=True)

with c_right:
    st.markdown('<div class="section-title">Margen de Utilidad (%)</div>', unsafe_allow_html=True)
    bar_colors = [COLORS['utilidad'] if v >= 0 else COLORS['gastos'] for v in dff['Margen_Pct']]
    fig3 = go.Figure(go.Bar(
        x=dff['Mes'], y=dff['Margen_Pct'],
        marker_color=bar_colors, marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>Margen: %{y:.1f}%<extra></extra>"
    ))
    fig3.add_hline(y=0, line_dash='dot', line_color=COLORS['muted'], line_width=1)
    fig3.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=COLORS['text'], family='DM Sans'),
        margin=dict(l=0, r=0, t=40, b=0), height=300,
        xaxis=dict(showgrid=False, tickfont=dict(size=11)),
        yaxis=dict(gridcolor=COLORS['grid'], ticksuffix='%'),
        showlegend=False,
    )
    st.plotly_chart(fig3, use_container_width=True)

# ── Chart 3: Stacked area – composición del gasto ───────────────────────────
st.markdown('<div class="section-title">Composición de Egresos vs Ventas</div>', unsafe_allow_html=True)
fig4 = go.Figure()
fig4.add_trace(go.Scatter(
    x=dff['Mes'], y=dff['Ventas'], name='Ventas',
    mode='lines', line=dict(color=COLORS['ventas'], width=2, dash='dot'),
    hovertemplate="Ventas: $%{y:,.0f}<extra></extra>"
))
fig4.add_trace(go.Scatter(
    x=dff['Mes'], y=dff['Costos'], name='Costos',
    stackgroup='one', fillcolor='rgba(255,209,102,0.5)',
    line=dict(color=COLORS['costos'], width=1),
    hovertemplate="Costos: $%{y:,.0f}<extra></extra>"
))
fig4.add_trace(go.Scatter(
    x=dff['Mes'], y=dff['Gastos'], name='Gastos',
    stackgroup='one', fillcolor='rgba(255,107,107,0.5)',
    line=dict(color=COLORS['gastos'], width=1),
    hovertemplate="Gastos: $%{y:,.0f}<extra></extra>"
))
fig4.update_layout(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color=COLORS['text'], family='DM Sans'),
    legend=dict(orientation='h', y=1.08, x=0, bgcolor='rgba(0,0,0,0)'),
    margin=dict(l=0, r=0, t=40, b=0), height=320,
    xaxis=dict(showgrid=False),
    yaxis=dict(gridcolor=COLORS['grid'], tickprefix='$', tickformat=',.0f'),
    hovermode='x unified',
)
st.plotly_chart(fig4, use_container_width=True)

# ── Tabla detallada ──────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Tabla Detallada</div>', unsafe_allow_html=True)

display = dff[['Mes','Ventas','Gastos','Costos','Utilidad','Margen_Pct']].copy()
display.columns = ['Mes','Ventas','Gastos Totales','Costos (Mat. Prima)','Utilidad Bruta','Margen %']
for col in ['Ventas','Gastos Totales','Costos (Mat. Prima)','Utilidad Bruta']:
    display[col] = display[col].apply(lambda x: f"${x:,.2f}")
display['Margen %'] = display['Margen %'].apply(lambda x: f"{x:.2f}%")

st.dataframe(
    display,
    use_container_width=True,
    hide_index=True,
)

# ── Desglose por categoría ───────────────────────────────────────────────────
st.markdown('<div class="section-title">Desglose por Categoría</div>', unsafe_allow_html=True)

sel_nums = dff['Mes_Num'].tolist()
detalle = raw[raw['Mes_Num'].isin(sel_nums)].copy()
cat = (
    detalle.groupby(['Tipo', 'Categoria', 'Subcategoria', 'Codigo', 'Concepto'], dropna=False)['Monto']
    .sum()
    .reset_index()
    .sort_values(['Tipo', 'Categoria', 'Subcategoria', 'Codigo'])
)
cat_display = cat.copy()
cat_display['Monto'] = cat_display['Monto'].apply(lambda x: f"${x:,.2f}")
cat_display.columns = ['Tipo', 'Categoría', 'Subcategoría', 'Código', 'Concepto', 'Total']
st.dataframe(cat_display, use_container_width=True, hide_index=True)
