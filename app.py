"""
JETA Africa Holding — Business Intelligence Dashboard
======================================================
Interactive dashboard for viewing and analyzing lead data
across all JETA business verticals (Pharma, Fintech, etc.)

Run:
    streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="JETA Africa Holding — Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #1F4E79;
        margin-bottom: 0;
    }
    .sub-header {
        font-size: 1rem;
        color: #666;
        margin-top: 0;
    }
    .metric-card {
        background: linear-gradient(135deg, #1F4E79 0%, #2E7D32 100%);
        padding: 1.2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
    }
    .metric-label {
        font-size: 0.85rem;
        opacity: 0.9;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ─── Data Loading ─────────────────────────────────────────────────────────────
DATA_DIR = Path(__file__).parent

@st.cache_data
def load_pharma_data():
    path = DATA_DIR / "pharma_africa_leads.xlsx"
    if path.exists():
        df = pd.read_excel(path, sheet_name="All Companies")
        df["Country"] = df["Country"].fillna("Unknown")
        return df
    return pd.DataFrame()

@st.cache_data
def load_fintech_data():
    path = DATA_DIR / "fintech_africa_leads.xlsx"
    if path.exists():
        df = pd.read_excel(path, sheet_name="All Companies")
        df["Country"] = df["Country"].fillna("Unknown")
        return df
    return pd.DataFrame()


def rating_to_num(val):
    return {"גבוה": 3, "בינוני": 2, "נמוך": 1}.get(val, 0)


# ─── Sidebar Navigation ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        '<h2 style="color: #1F4E79; margin: 0;">JETA Africa</h2>'
        '<p style="color: #666; font-size: 0.85rem; margin: 0;">Holding Group</p>',
        unsafe_allow_html=True,
    )
    st.markdown("---")

    menu = st.radio(
        "Navigation",
        [
            "Overview",
            "Pharma — Africa",
            "Fintech — Africa",
            "Company Explorer",
            "Export Data",
        ],
        index=0,
    )

    st.markdown("---")
    st.markdown(
        "<small style='color: #888;'>JETA Africa Holding<br>"
        "Business Intelligence Dashboard<br>"
        "© 2026</small>",
        unsafe_allow_html=True,
    )


# ─── Helper: Metric Cards ────────────────────────────────────────────────────
def metric_row(cols_data):
    cols = st.columns(len(cols_data))
    for col, (value, label, color) in zip(cols, cols_data):
        col.markdown(
            f"""<div style="background: {color}; padding: 1rem; border-radius: 10px;
                            color: white; text-align: center;">
                <div style="font-size: 2rem; font-weight: 700;">{value}</div>
                <div style="font-size: 0.85rem; opacity: 0.9;">{label}</div>
            </div>""",
            unsafe_allow_html=True,
        )


# ─── Helper: Data Table with Styling ─────────────────────────────────────────
def show_leads_table(df, key_prefix=""):
    """Display a filterable leads table."""
    if df.empty:
        st.info("No data available yet for this vertical.")
        return

    # Filters
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        countries = ["All"] + sorted(df["Country"].dropna().unique().tolist())
        sel_country = st.selectbox("Country", countries, key=f"{key_prefix}_country")
    with col2:
        potentials = ["All", "גבוה", "בינוני", "נמוך"]
        sel_potential = st.selectbox("Strategic Potential", potentials, key=f"{key_prefix}_potential")
    with col3:
        values = ["All", "גבוה", "בינוני", "נמוך"]
        sel_value = st.selectbox("Business Value", values, key=f"{key_prefix}_value")
    with col4:
        search = st.text_input("Search company name", key=f"{key_prefix}_search")

    filtered = df.copy()
    if sel_country != "All":
        filtered = filtered[filtered["Country"] == sel_country]
    if sel_potential != "All":
        filtered = filtered[filtered["Strategic Potential"] == sel_potential]
    if sel_value != "All":
        filtered = filtered[filtered["Estimated Business Value"] == sel_value]
    if search:
        filtered = filtered[filtered["Company Name"].str.contains(search, case=False, na=False)]

    st.markdown(f"**Showing {len(filtered)} of {len(df)} companies**")

    # Display columns
    display_cols = [
        "Company Name", "Country", "Website", "Email",
        "Product Focus", "Manufacturer Type",
        "Estimated Business Value", "Strategic Potential",
        "Confidence Level",
    ]
    available_cols = [c for c in display_cols if c in filtered.columns]
    st.dataframe(
        filtered[available_cols],
        width="stretch",
        height=500,
        column_config={
            "Website": st.column_config.LinkColumn("Website"),
            "Email": st.column_config.TextColumn("Email"),
        },
    )
    return filtered


# ═══════════════════════════════════════════════════════════════════════════════
# PAGES
# ═══════════════════════════════════════════════════════════════════════════════

# ─── Overview ─────────────────────────────────────────────────────────────────
if menu == "Overview":
    st.markdown('<p class="main-header">JETA Africa Holding</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Business Intelligence Dashboard — Lead Pipeline Overview</p>', unsafe_allow_html=True)
    st.markdown("---")

    df_pharma = load_pharma_data()
    df_fintech = load_fintech_data()

    total = len(df_pharma) + len(df_fintech)
    pharma_high = len(df_pharma[df_pharma["Strategic Potential"] == "גבוה"]) if not df_pharma.empty else 0
    fintech_high = len(df_fintech[df_fintech["Strategic Potential"] == "גבוה"]) if not df_fintech.empty else 0
    with_email = 0
    if not df_pharma.empty:
        with_email += len(df_pharma[df_pharma["Email"].notna() & (df_pharma["Email"] != "לא נמצא")])
    if not df_fintech.empty:
        with_email += len(df_fintech[df_fintech["Email"].notna() & (df_fintech["Email"] != "לא נמצא")])

    countries_set = set()
    if not df_pharma.empty:
        countries_set.update(df_pharma["Country"].dropna().unique())
    if not df_fintech.empty:
        countries_set.update(df_fintech["Country"].dropna().unique())

    metric_row([
        (total, "Total Companies", "#1F4E79"),
        (pharma_high + fintech_high, "High Potential", "#2E7D32"),
        (with_email, "With Contact Email", "#E65100"),
        (len(countries_set), "Countries Covered", "#6A1B9A"),
    ])

    st.markdown("---")

    # Two columns: Pharma summary + Fintech summary
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Pharma — Africa")
        if not df_pharma.empty:
            st.metric("Companies", len(df_pharma))
            st.metric("High Potential", pharma_high)

            fig = px.pie(
                df_pharma, names="Country",
                title="Companies by Country",
                color_discrete_sequence=px.colors.qualitative.Set2,
            )
            fig.update_traces(textposition="inside", textinfo="value+label")
            fig.update_layout(showlegend=False, height=350)
            st.plotly_chart(fig, width="stretch")
        else:
            st.info("Pharma data not loaded yet.")

    with col2:
        st.subheader("Fintech — Africa")
        if not df_fintech.empty:
            st.metric("Companies", len(df_fintech))
            st.metric("High Potential", fintech_high)

            fig = px.pie(
                df_fintech, names="Country",
                title="Companies by Country",
                color_discrete_sequence=px.colors.qualitative.Pastel,
            )
            fig.update_traces(textposition="inside", textinfo="value+label")
            fig.update_layout(showlegend=False, height=350)
            st.plotly_chart(fig, width="stretch")
        else:
            st.info("Fintech data will appear here once the Fintech agent runs.")

    # JETA Target Markets
    st.markdown("---")
    st.subheader("JETA Priority Markets")
    priority = ["Nigeria", "South Africa", "Kenya", "Ghana", "Angola",
                 "Ethiopia", "Rwanda", "Tanzania", "Senegal", "Mauritius", "Uganda"]

    if not df_pharma.empty:
        market_data = []
        for country in priority:
            pharma_count = len(df_pharma[df_pharma["Country"].str.contains(country, case=False, na=False)])
            fintech_count = len(df_fintech[df_fintech["Country"].str.contains(country, case=False, na=False)]) if not df_fintech.empty else 0
            market_data.append({
                "Country": country,
                "Pharma Leads": pharma_count,
                "Fintech Leads": fintech_count,
                "Total": pharma_count + fintech_count,
            })
        df_markets = pd.DataFrame(market_data)
        df_markets = df_markets[df_markets["Total"] > 0].sort_values("Total", ascending=False)

        if not df_markets.empty:
            fig = px.bar(
                df_markets, x="Country", y=["Pharma Leads", "Fintech Leads"],
                title="Leads by JETA Priority Market",
                barmode="stack",
                color_discrete_map={"Pharma Leads": "#1F4E79", "Fintech Leads": "#2E7D32"},
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, width="stretch")


# ─── Pharma Page ──────────────────────────────────────────────────────────────
elif menu == "Pharma — Africa":
    st.markdown('<p class="main-header">Pharma — Africa</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Pharmaceutical Manufacturers Across Africa</p>', unsafe_allow_html=True)
    st.markdown("---")

    df = load_pharma_data()

    if not df.empty:
        # Top metrics
        high_sp = len(df[df["Strategic Potential"] == "גבוה"])
        high_bv = len(df[df["Estimated Business Value"] == "גבוה"])
        with_email = len(df[df["Email"].notna() & (df["Email"] != "לא נמצא")])
        high_conf = len(df[df["Confidence Level"] == "גבוהה"])

        metric_row([
            (len(df), "Total Companies", "#1F4E79"),
            (high_sp, "High Strategic Potential", "#2E7D32"),
            (with_email, "With Email", "#E65100"),
            (high_conf, "High Confidence", "#6A1B9A"),
        ])

        st.markdown("---")

        # Tabs
        tab1, tab2, tab3 = st.tabs(["All Companies", "Top 10", "Analytics"])

        with tab1:
            show_leads_table(df, key_prefix="pharma")

        with tab2:
            st.subheader("Top 10 — Highest Potential Companies")
            top10 = df.head(10)
            for i, row in top10.iterrows():
                with st.expander(f"**{i+1}. {row['Company Name']}** — {row['Country']}", expanded=(i < 3)):
                    c1, c2 = st.columns([2, 1])
                    with c1:
                        st.markdown(f"**Website:** {row.get('Website', 'N/A')}")
                        st.markdown(f"**Email:** {row.get('Email', 'N/A')}")
                        st.markdown(f"**Phone:** {row.get('Phone', 'N/A')}")
                        st.markdown(f"**Products:** {row.get('Product Focus', 'N/A')}")
                        summary = row.get('Business Summary', '')
                        if summary and str(summary) != 'nan':
                            st.markdown(f"**Summary:** {summary}")
                    with c2:
                        st.markdown(f"**Business Value:** {row.get('Estimated Business Value', 'N/A')}")
                        st.markdown(f"**Strategic Potential:** {row.get('Strategic Potential', 'N/A')}")
                        st.markdown(f"**Type:** {row.get('Manufacturer Type', 'N/A')}")
                        st.markdown(f"**Certifications:** {row.get('Certifications / Regulatory', 'N/A')}")
                        st.markdown(f"**Year Founded:** {row.get('Year Founded', 'N/A')}")
                        st.markdown(f"**Confidence:** {row.get('Confidence Level', 'N/A')}")
                        st.markdown(f"**Rating Reasons:** {row.get('Key Reasons for Rating', 'N/A')}")

        with tab3:
            col1, col2 = st.columns(2)

            with col1:
                # By country
                fig = px.bar(
                    df["Country"].value_counts().reset_index(),
                    x="Country", y="count",
                    title="Companies by Country",
                    color="count",
                    color_continuous_scale="Viridis",
                )
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, width="stretch")

            with col2:
                # By strategic potential
                sp_counts = df["Strategic Potential"].value_counts().reset_index()
                fig = px.pie(
                    sp_counts, names="Strategic Potential", values="count",
                    title="Strategic Potential Distribution",
                    color="Strategic Potential",
                    color_discrete_map={"גבוה": "#2E7D32", "בינוני": "#FF9800", "נמוך": "#F44336"},
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, width="stretch")

            col3, col4 = st.columns(2)

            with col3:
                # Manufacturer type
                if "Manufacturer Type" in df.columns:
                    mt_counts = df["Manufacturer Type"].value_counts().reset_index()
                    fig = px.bar(
                        mt_counts, x="Manufacturer Type", y="count",
                        title="By Manufacturer Type",
                        color="Manufacturer Type",
                    )
                    fig.update_layout(height=400, showlegend=False)
                    st.plotly_chart(fig, width="stretch")

            with col4:
                # Confidence level
                conf_counts = df["Confidence Level"].value_counts().reset_index()
                fig = px.pie(
                    conf_counts, names="Confidence Level", values="count",
                    title="Data Confidence Level",
                    color="Confidence Level",
                    color_discrete_map={"גבוהה": "#2E7D32", "בינונית": "#FF9800", "נמוכה": "#F44336"},
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, width="stretch")

    else:
        st.warning("No pharma data found. Run the pharma agent first.")


# ─── Fintech Page ─────────────────────────────────────────────────────────────
elif menu == "Fintech — Africa":
    st.markdown('<p class="main-header">Fintech — Africa</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Fintech & Digital Finance Companies Across Africa</p>', unsafe_allow_html=True)
    st.markdown("---")

    df = load_fintech_data()

    if not df.empty:
        high_sp = len(df[df["Strategic Potential"] == "גבוה"])
        with_email = len(df[df["Email"].notna() & (df["Email"] != "לא נמצא")])

        metric_row([
            (len(df), "Total Companies", "#1F4E79"),
            (high_sp, "High Strategic Potential", "#2E7D32"),
            (with_email, "With Email", "#E65100"),
            (len(df["Country"].dropna().unique()), "Countries", "#6A1B9A"),
        ])

        st.markdown("---")
        tab1, tab2 = st.tabs(["All Companies", "Analytics"])

        with tab1:
            show_leads_table(df, key_prefix="fintech")

        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                fig = px.bar(
                    df["Country"].value_counts().reset_index(),
                    x="Country", y="count",
                    title="Fintech Companies by Country",
                    color="count", color_continuous_scale="Viridis",
                )
                fig.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig, width="stretch")
            with col2:
                sp_counts = df["Strategic Potential"].value_counts().reset_index()
                fig = px.pie(
                    sp_counts, names="Strategic Potential", values="count",
                    title="Strategic Potential",
                    color="Strategic Potential",
                    color_discrete_map={"גבוה": "#2E7D32", "בינוני": "#FF9800", "נמוך": "#F44336"},
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, width="stretch")
    else:
        st.info(
            "Fintech data is not available yet.\n\n"
            "Once the Fintech Africa agent runs, place the output file "
            "(`fintech_africa_leads.xlsx`) in this directory and refresh."
        )


# ─── Company Explorer ────────────────────────────────────────────────────────
elif menu == "Company Explorer":
    st.markdown('<p class="main-header">Company Explorer</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Deep dive into any company</p>', unsafe_allow_html=True)
    st.markdown("---")

    df_pharma = load_pharma_data()
    df_fintech = load_fintech_data()

    # Combine all data
    all_dfs = []
    if not df_pharma.empty:
        df_pharma_copy = df_pharma.copy()
        df_pharma_copy["Vertical"] = "Pharma"
        all_dfs.append(df_pharma_copy)
    if not df_fintech.empty:
        df_fintech_copy = df_fintech.copy()
        df_fintech_copy["Vertical"] = "Fintech"
        all_dfs.append(df_fintech_copy)

    if all_dfs:
        df_all = pd.concat(all_dfs, ignore_index=True)
        companies = sorted(df_all["Company Name"].dropna().unique().tolist())
        selected = st.selectbox("Select a company", companies)

        if selected:
            row = df_all[df_all["Company Name"] == selected].iloc[0]

            col1, col2 = st.columns([2, 1])

            with col1:
                st.subheader(row["Company Name"])
                st.markdown(f"**Vertical:** {row.get('Vertical', 'N/A')}")
                st.markdown(f"**Country:** {row.get('Country', 'N/A')}")
                st.markdown(f"**City / Address:** {row.get('City / Address', 'N/A')}")
                st.markdown(f"**Website:** {row.get('Website', 'N/A')}")
                st.markdown(f"**Email:** {row.get('Email', 'N/A')}")
                st.markdown(f"**Phone:** {row.get('Phone', 'N/A')}")

                st.markdown("---")
                st.markdown("**Business Summary:**")
                summary = row.get("Business Summary", "")
                st.markdown(summary if summary and str(summary) != "nan" else "No summary available.")

            with col2:
                st.markdown("### Ratings")

                bv = row.get("Estimated Business Value", "N/A")
                sp = row.get("Strategic Potential", "N/A")
                bv_color = {"גבוה": "green", "בינוני": "orange", "נמוך": "red"}.get(bv, "gray")
                sp_color = {"גבוה": "green", "בינוני": "orange", "נמוך": "red"}.get(sp, "gray")

                st.markdown(f"**Business Value:** :{bv_color}[{bv}]")
                st.markdown(f"**Strategic Potential:** :{sp_color}[{sp}]")
                st.markdown(f"**Confidence:** {row.get('Confidence Level', 'N/A')}")

                st.markdown("---")
                st.markdown("### Details")
                st.markdown(f"**Type:** {row.get('Manufacturer Type', 'N/A')}")
                st.markdown(f"**Products:** {row.get('Product Focus', 'N/A')}")
                st.markdown(f"**Certifications:** {row.get('Certifications / Regulatory', 'N/A')}")
                st.markdown(f"**Year Founded:** {row.get('Year Founded', 'N/A')}")
                st.markdown(f"**Rating Reasons:** {row.get('Key Reasons for Rating', 'N/A')}")
    else:
        st.warning("No data available. Run the agents first.")


# ─── Export ───────────────────────────────────────────────────────────────────
elif menu == "Export Data":
    st.markdown('<p class="main-header">Export Data</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Download lead data in various formats</p>', unsafe_allow_html=True)
    st.markdown("---")

    df_pharma = load_pharma_data()
    df_fintech = load_fintech_data()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Pharma Leads")
        if not df_pharma.empty:
            st.write(f"{len(df_pharma)} companies")

            # CSV download
            csv = df_pharma.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                "Download CSV",
                csv,
                "pharma_africa_leads.csv",
                "text/csv",
                key="pharma_csv",
            )

            # Excel download
            pharma_path = DATA_DIR / "pharma_africa_leads.xlsx"
            if pharma_path.exists():
                with open(pharma_path, "rb") as f:
                    st.download_button(
                        "Download Excel (Styled)",
                        f.read(),
                        "pharma_africa_leads.xlsx",
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key="pharma_xlsx",
                    )

            # High potential only
            high_pot = df_pharma[df_pharma["Strategic Potential"] == "גבוה"]
            if not high_pot.empty:
                csv_high = high_pot.to_csv(index=False).encode("utf-8-sig")
                st.download_button(
                    f"Download High Potential Only ({len(high_pot)} companies)",
                    csv_high,
                    "pharma_high_potential.csv",
                    "text/csv",
                    key="pharma_high_csv",
                )
        else:
            st.info("No pharma data available.")

    with col2:
        st.subheader("Fintech Leads")
        if not df_fintech.empty:
            st.write(f"{len(df_fintech)} companies")
            csv = df_fintech.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                "Download CSV",
                csv,
                "fintech_africa_leads.csv",
                "text/csv",
                key="fintech_csv",
            )
        else:
            st.info("No fintech data available yet.")
