import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

st.set_page_config(page_title="Customer Shopping Behaviour Analysis", layout="wide")

st.title("Customer Shopping Behaviour Analysis")
st.markdown("**Prepared by: Rohit Patel**")
st.markdown("---")

engine = create_engine(
    "postgresql+psycopg2://postgres:indrajeet123@localhost:5432/customer_behaviour"
)

@st.cache_data
def load_data():
    df = pd.read_sql("SELECT * FROM customer", engine)
    return df

df = load_data()

# ── Sidebar filters ───────────────────────────────────────────────
st.sidebar.header("Filters")

gender = st.sidebar.selectbox("Gender", ["All"] + sorted(df["gender"].unique().tolist()))
category = st.sidebar.selectbox("Category", ["All"] + sorted(df["category"].unique().tolist()))
season = st.sidebar.selectbox("Season", ["All"] + sorted(df["season"].unique().tolist()))
subscription = st.sidebar.selectbox("Subscription Status", ["All"] + sorted(df["subscription_status"].unique().tolist()))

filtered = df.copy()
if gender != "All":
    filtered = filtered[filtered["gender"] == gender]
if category != "All":
    filtered = filtered[filtered["category"] == category]
if season != "All":
    filtered = filtered[filtered["season"] == season]
if subscription != "All":
    filtered = filtered[filtered["subscription_status"] == subscription]

# ── KPI metrics ───────────────────────────────────────────────────
st.subheader("Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Customers", f"{len(filtered):,}")
col2.metric("Avg Purchase", f"${filtered['purchase_amount'].mean():.2f}")
col3.metric("Total Revenue", f"${filtered['purchase_amount'].sum():,.0f}")
col4.metric("Avg Review Rating", f"{filtered['review_rating'].mean():.2f} / 5")

st.markdown("---")

# ── Row 1: Revenue by Category + Gender split ─────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Category")
    cat_rev = filtered.groupby("category")["purchase_amount"].sum().reset_index()
    cat_rev.columns = ["Category", "Total Revenue"]
    fig = px.bar(cat_rev, x="Category", y="Total Revenue", color="Category",
                 color_discrete_sequence=px.colors.qualitative.Set2)
    fig.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Customers by Gender")
    gender_count = filtered["gender"].value_counts().reset_index()
    gender_count.columns = ["Gender", "Count"]
    fig2 = px.pie(gender_count, names="Gender", values="Count",
                  color_discrete_sequence=["#378ADD", "#D4537E"])
    st.plotly_chart(fig2, use_container_width=True)

# ── Row 2: Season + Payment Method ───────────────────────────────
col3, col4 = st.columns(2)

with col3:
    st.subheader("Purchases by Season")
    season_count = filtered["season"].value_counts().reset_index()
    season_count.columns = ["Season", "Count"]
    fig3 = px.bar(season_count, x="Season", y="Count", color="Season",
                  color_discrete_sequence=px.colors.qualitative.Pastel)
    fig3.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("Payment Method Distribution")
    pay_count = filtered["payment_method"].value_counts().reset_index()
    pay_count.columns = ["Payment Method", "Count"]
    fig4 = px.bar(pay_count, x="Count", y="Payment Method", orientation="h",
                  color="Payment Method",
                  color_discrete_sequence=px.colors.qualitative.Set3)
    fig4.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig4, use_container_width=True)

# ── Row 3: Age group + Subscription ──────────────────────────────
col5, col6 = st.columns(2)

with col5:
    st.subheader("Avg Purchase by Age Group")
    if "age_group" in filtered.columns:
        age_rev = filtered.groupby("age_group")["purchase_amount"].mean().reset_index()
        age_rev.columns = ["Age Group", "Avg Purchase"]
        fig5 = px.bar(age_rev, x="Age Group", y="Avg Purchase",
                      color="Age Group",
                      color_discrete_sequence=px.colors.qualitative.Bold)
        fig5.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig5, use_container_width=True)
    else:
        st.info("age_group column not found. Run the notebook preprocessing first.")

with col6:
    st.subheader("Subscription vs Avg Rating")
    sub_rating = filtered.groupby("subscription_status")["review_rating"].mean().reset_index()
    sub_rating.columns = ["Subscription", "Avg Rating"]
    fig6 = px.bar(sub_rating, x="Subscription", y="Avg Rating",
                  color="Subscription",
                  color_discrete_sequence=["#1D9E75", "#D85A30"])
    fig6.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)",
                       yaxis=dict(range=[3, 4]))
    st.plotly_chart(fig6, use_container_width=True)

# ── Row 4: Discount impact ────────────────────────────────────────
st.subheader("Impact of Discount on Avg Purchase Amount")
if "discount_applied" in filtered.columns:
    disc = filtered.groupby("discount_applied")["purchase_amount"].mean().reset_index()
    disc.columns = ["Discount Applied", "Avg Purchase"]
    fig7 = px.bar(disc, x="Discount Applied", y="Avg Purchase",
                  color="Discount Applied",
                  color_discrete_sequence=["#534AB7", "#BA7517"])
    fig7.update_layout(showlegend=False, plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig7, use_container_width=True)

st.markdown("---")

# ── Raw data ──────────────────────────────────────────────────────
st.subheader("Raw Data")
st.dataframe(filtered, use_container_width=True)