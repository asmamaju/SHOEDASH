import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load and clean dataset
df = pd.read_csv("uae_shoe_startup_synthetic_data.csv")
df.columns = df.columns.str.strip().str.replace(" ", "_").str.title()

# Set up Streamlit page
st.set_page_config(page_title="UAE Shoe Startup Dashboard", layout="wide")
st.title("👟 UAE Custom Shoe Startup - Fit Satisfaction Insights Dashboard")
st.markdown("This dashboard offers in-depth insights into customer satisfaction with shoe fit, empowering HR and stakeholders to make data-driven decisions.")

# Sidebar filters
st.sidebar.header("🔍 Filters")
gender = st.sidebar.multiselect("Select Gender", options=df["Gender"].unique(), default=df["Gender"].unique())
channel = st.sidebar.multiselect("Select Shopping Channel", options=df["Shopping_Channel"].unique(), default=df["Shopping_Channel"].unique())
style = st.sidebar.multiselect("Select Shoe Style", options=df["Preferred_Style"].unique(), default=df["Preferred_Style"].unique())

# Filtered dataset
df_filtered = df[(df["Gender"].isin(gender)) & (df["Shopping_Channel"].isin(channel)) & (df["Preferred_Style"].isin(style))]

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Demographics", "Product Preferences", "Satisfaction Analytics"])

with tab1:
    st.header("📌 Summary Statistics & Distribution")
    st.markdown("Key descriptive statistics to understand the overall data distribution.")
    st.write(df_filtered.describe())

    st.markdown("**Distribution of Fit Satisfaction Score**")
    fig1 = px.histogram(df_filtered, x="Fit_Satisfaction_Score", nbins=20, color="Shopping_Channel", barmode='overlay')
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("**Fit Score by Gender**")
    fig2 = px.box(df_filtered, x="Gender", y="Fit_Satisfaction_Score", color="Gender")
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.header("👥 Customer Demographics")

    st.markdown("**Gender Distribution**")
    fig3 = px.pie(df_filtered, names="Gender", title="Gender Breakdown")
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("**Age Distribution**")
    fig4 = px.histogram(df_filtered, x="Age", nbins=15, color="Gender")
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("**Income vs Fit Satisfaction** (Not available in this dataset)")
    st.info("The dataset does not include an 'Income' field, so this chart is skipped.")

with tab3:
    st.header("👟 Product Preferences")

    st.markdown("**Popular Shoe Styles**")
    fig6 = px.histogram(df_filtered, x="Preferred_Style", color="Gender", barmode="group")
    st.plotly_chart(fig6, use_container_width=True)

    st.markdown("**Style vs Fit Satisfaction**")
    fig7 = px.box(df_filtered, x="Preferred_Style", y="Fit_Satisfaction_Score", color="Preferred_Style")
    st.plotly_chart(fig7, use_container_width=True)

    st.markdown("**Shopping Channel Preferences**")
    fig8 = px.pie(df_filtered, names="Shopping_Channel", title="Channel Split")
    st.plotly_chart(fig8, use_container_width=True)

with tab4:
    st.header("📈 Fit Satisfaction Deep-Dive")

    st.markdown("**Heatmap - Correlation Matrix**")
    st.markdown("This heatmap shows how strongly Fit Satisfaction Score correlates with other numerical features.")
    corr = df_filtered.select_dtypes(include='number').corr()
    fig9, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig9)

    st.markdown("**Fit Score by Channel and Style**")
    pivot = df_filtered.pivot_table(index='Preferred_Style', columns='Shopping_Channel', values='Fit_Satisfaction_Score', aggfunc='mean')
    st.dataframe(pivot)

    st.markdown("**Satisfaction by Age Group**")
    df_filtered["Age_Group"] = pd.cut(df_filtered["Age"], bins=[0, 25, 35, 45, 60], labels=["<25", "25-35", "35-45", "45+"])
    fig10 = px.box(df_filtered, x="Age_Group", y="Fit_Satisfaction_Score", color="Age_Group")
    st.plotly_chart(fig10, use_container_width=True)
