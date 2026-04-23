import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Resolve data path relative to this file so the app works regardless of
# which directory streamlit run is invoked from
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="USDA Food Nutrition Profiling",
    page_icon="🥦",
    layout="wide",
)

CITATION = "Data source: USDA FoodData Central — SR Legacy Dataset (2019). fdc.nal.usda.gov"

CLUSTER_FEATURES = [
    "Protein (g)",
    "Total Fat (g)",
    "Carbohydrates (g)",
    "Total Sugars (g)",
    "Fiber (g)",
    "Sodium (mg)",
    "Energy (kcal)",
]

NUTRIENT_OPTIONS = {
    "Protein":       "Protein (g)",
    "Total Fat":     "Total Fat (g)",
    "Carbohydrates": "Carbohydrates (g)",
    "Sodium":        "Sodium (mg)",
    "Total Sugars":  "Total Sugars (g)",
}

# ── Data ───────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join(DATA_DIR, "food_nutrients_clustered.csv"))
    df["cluster_name"] = df["cluster_name"].fillna("Unassigned")
    return df

df = load_data()
categories = sorted(df["category"].dropna().unique())
cluster_names = sorted(df["cluster_name"].unique())

# ── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("USDA Food Nutrition Profiling")
    st.caption("CS 4379G — Final Project · Texas State University")
    st.markdown("---")
    st.markdown("**Dataset**")
    st.markdown(f"- **{df.shape[0]:,}** food items")
    st.markdown(f"- **{df['category'].nunique()}** food categories")
    st.markdown(f"- **{df['cluster_name'].nunique()}** nutritional clusters")
    st.markdown(f"- **{len(CLUSTER_FEATURES)}** clustering nutrients")
    st.markdown("---")
    st.markdown("**Source**")
    st.markdown(
        "[USDA FoodData Central](https://fdc.nal.usda.gov/download-datasets)"
        " — SR Legacy Release (2019)"
    )

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs([
    "🍎 Food Explorer",
    "🔵 Cluster Explorer",
    "📊 Nutrient Comparison",
])

# ══════════════════════════════════════════════════════════════════════════════
# VIEW 1 — FOOD EXPLORER
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.header("Food Explorer")
    st.markdown(
        "Select a food category to explore the top protein sources "
        "and the fat vs. carbohydrate spread within that group."
    )

    # DASH-3: category dropdown
    selected_cat = st.selectbox(
        "Select a food category",
        options=categories,
        index=categories.index("Beef Products") if "Beef Products" in categories else 0,
        key="cat_selector",
    )

    cat_df = df[df["category"] == selected_cat].copy()

    if cat_df.empty:
        st.warning("No foods found for the selected category.")
    else:
        col1, col2 = st.columns(2)

        # DASH-4: top 15 foods by protein
        with col1:
            st.subheader(f"Top 15 Foods by Protein")
            top15 = (
                cat_df.nlargest(15, "Protein (g)")
                [["description", "Protein (g)"]]#, "Total Fat (g)", "Carbohydrates (g)", "Energy (kcal)"]]
                .copy()
            )
            top15["label"] = top15["description"].str[:40]
            fig4 = px.bar(
                top15.sort_values("Protein (g)"),
                x="Protein (g)",
                y="label",
                orientation="h",
                hover_name="description",
                hover_data={
                    "label": False,
                    "Protein (g)": ":.1f",
                    #"Total Fat (g)": ":.1f",
                    #"Carbohydrates (g)": ":.1f",
                    #"Energy (kcal)": ":.0f",
                },
                labels={"label": "Food", "Protein (g)": "Protein (g per 100g)"},
                title=f"Top 15 Foods by Protein — {selected_cat}",
                color="Protein (g)",
                color_continuous_scale="Blues",
            )
            fig4.update_layout(
                yaxis_title="",
                coloraxis_showscale=False,
                margin=dict(l=10, r=10, t=40, b=10),
            )
            st.plotly_chart(fig4, use_container_width=True)
            st.caption(CITATION)

        # DASH-5: fat vs carbs scatter with hover showing food name
        with col2:
            st.subheader("Fat vs. Carbohydrates")
            fig5 = px.scatter(
                cat_df,
                x="Total Fat (g)",
                y="Carbohydrates (g)",
                hover_name="description",
                hover_data={
                    "Protein (g)": ":.1f",
                    "Energy (kcal)": ":.0f",
                    "Total Fat (g)": ":.1f",
                    "Carbohydrates (g)": ":.1f",
                },
                labels={
                    "Total Fat (g)": "Total Fat (g per 100g)",
                    "Carbohydrates (g)": "Carbohydrates (g per 100g)",
                },
                title=f"Fat vs. Carbohydrates — {selected_cat}",
                color_discrete_sequence=["#2C7BB6"],
            )
            fig5.update_traces(marker=dict(size=8, opacity=0.7))
            fig5.update_layout(margin=dict(l=10, r=10, t=40, b=10))
            st.plotly_chart(fig5, use_container_width=True)
            st.caption(CITATION)

# ══════════════════════════════════════════════════════════════════════════════
# VIEW 2 — CLUSTER EXPLORER
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.header("Cluster Explorer")
    st.markdown(
        "Explore the seven nutritional archetypes discovered by k-means clustering. "
        "Hover over any point in the PCA plot to see the food name and category."
    )

    # DASH-6: PCA scatter colored by cluster
    st.subheader("PCA Plot — Foods Colored by Cluster")
    fig6 = px.scatter(
        df,
        x="PC1",
        y="PC2",
        color="cluster_name",
        hover_name="description",
        hover_data={"category": True, "PC1": False, "PC2": False},
        labels={"PC1": "Principal Component 1", "PC2": "Principal Component 2"},
        title="Nutritional Clusters in PCA Space (k=7)",
        opacity=0.55,
    )
    fig6.update_traces(marker=dict(size=5))
    fig6.update_layout(
        legend_title_text="Cluster",
        margin=dict(l=10, r=10, t=40, b=10),
    )
    st.plotly_chart(fig6, use_container_width=True)
    st.caption(CITATION)

    st.markdown("---")
    col_radio, col_radar = st.columns([1, 2])

    # DASH-7: radio button → radar chart
    with col_radio:
        st.subheader("Select a Cluster")
        selected_cluster = st.radio(
            "Cluster",
            options=cluster_names,
            label_visibility="collapsed",
        )

        # DASH-8: top 10 foods by energy in selected cluster
        st.subheader("Top 10 Foods by Energy")
        cluster_foods = (
            df[df["cluster_name"] == selected_cluster]
            .nlargest(10, "Energy (kcal)")
            [["description", "Energy (kcal)", "Protein (g)", "Total Fat (g)", "Carbohydrates (g)"]]
            .reset_index(drop=True)
        )
        cluster_foods.index += 1
        cluster_foods.columns = ["Food", "Energy (kcal)", "Protein (g)", "Fat (g)", "Carbs (g)"]
        st.dataframe(cluster_foods, use_container_width=True)
        st.caption(CITATION)

    with col_radar:
        st.subheader("Avg Nutrient Profile by Cluster")

        # Build normalised profiles for radar
        profile = df.groupby("cluster_name")[CLUSTER_FEATURES].mean()
        profile_norm = (profile - profile.min()) / (profile.max() - profile.min() + 1e-9)

        angles = CLUSTER_FEATURES + [CLUSTER_FEATURES[0]]  # close polygon

        fig7 = go.Figure()
        for cname in cluster_names:
            if cname not in profile_norm.index:
                continue
            vals = profile_norm.loc[cname].tolist()
            vals += vals[:1]
            is_selected = cname == selected_cluster
            fig7.add_trace(go.Scatterpolar(
                r=vals,
                theta=angles,
                fill="toself",
                name=cname,
                opacity=1.0 if is_selected else 0.25,
                line=dict(width=3 if is_selected else 1),
            ))

        fig7.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            showlegend=True,
            legend=dict(font=dict(size=10)),
            title=f"Nutrient Profile — {selected_cluster}",
            margin=dict(l=10, r=10, t=50, b=10),
        )
        st.plotly_chart(fig7, use_container_width=True)
        st.caption(CITATION)

# ══════════════════════════════════════════════════════════════════════════════
# VIEW 3 — NUTRIENT COMPARISON
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.header("Nutrient Comparison")
    st.markdown(
        "Compare nutrient distributions across multiple food categories side by side."
    )

    ctrl_col1, ctrl_col2 = st.columns([2, 1])

    # DASH-9: multi-select categories
    with ctrl_col1:
        selected_cats = st.multiselect(
            "Select 2–4 food categories to compare",
            options=categories,
            default=["Beef Products", "Vegetables and Vegetable Products",
                     "Sweets", "Nut and Seed Products"],
            max_selections=4,
        )

    # DASH-11: nutrient selector dropdown
    with ctrl_col2:
        selected_nutrient_label = st.selectbox(
            "Select a nutrient",
            options=list(NUTRIENT_OPTIONS.keys()),
        )
    selected_nutrient_col = NUTRIENT_OPTIONS[selected_nutrient_label]

    if len(selected_cats) < 2:
        st.warning("Please select at least 2 categories to compare.")
    else:
        # DASH-10: grouped box plot
        compare_df = df[df["category"].isin(selected_cats)].copy()
        fig10 = px.box(
            compare_df,
            x="category",
            y=selected_nutrient_col,
            color="category",
            points="outliers",
            labels={
                "category": "Food Category",
                selected_nutrient_col: f"{selected_nutrient_col} per 100g",
            },
            title=f"{selected_nutrient_label} Distribution by Category",
        )
        fig10.update_layout(
            showlegend=False,
            xaxis_tickangle=-25,
            margin=dict(l=10, r=10, t=50, b=10),
            yaxis=dict(rangemode="tozero"),
        )
        st.plotly_chart(fig10, use_container_width=True)
        st.caption(CITATION)
