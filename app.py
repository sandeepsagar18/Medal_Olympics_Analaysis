import streamlit as st
import pandas as pd
import preprocessor, helper
import plotly.express as px
import plotly.figure_factory as ff

st.set_page_config(
    page_title="Olympics Data Analytics Hub",
    page_icon="🏅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for polished dashboard aesthetic
st.markdown("""
<style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.06);
        border-left: 5px solid #1E88E5;
        margin-bottom: 10px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        padding-top: 10px;
        padding-bottom: 10px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Performance Optimization: Cache dataset loading
@st.cache_data
def load_data():
    df = pd.read_csv('athlete_events.csv')
    region_df = pd.read_csv('noc_regions.csv')
    return preprocessor.preprocess(df, region_df)

df = load_data()

st.sidebar.title("🏅 Olympics Analysis")
st.sidebar.caption("Modern Summer Games Data (1896 – 2024)")
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')

user_menu = st.sidebar.radio(
    'Explore Insights',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Country Comparison', 'Athlete wise Analysis', 'LA 2028 Predictor')
)

# ==========================================
# 1. MEDAL TALLY
# ==========================================
if user_menu == 'Medal Tally':
    st.sidebar.header("Filter Tally")
    years, country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df, selected_year, selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("🌍 All-Time Olympic Medal Tally")
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.title(f"🏅 Medal Tally in {selected_year} Olympics")
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.title(f"🏆 {selected_country} Overall Olympic Performance")
    else:
        st.title(f"🏆 {selected_country} Performance in {selected_year} Olympics")

    # Interactive tabs: Table view & World Map view
    tab1, tab2 = st.tabs(["📋 Medal Table", "🗺️ World Map (Choropleth)"])

    with tab1:
        # Download filtered table
        csv_data = medal_tally.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Tally as CSV",
            data=csv_data,
            file_name=f"medal_tally_{selected_year}_{selected_country}.csv",
            mime="text/csv",
        )
        st.dataframe(medal_tally, use_container_width=True, hide_index=True)

    with tab2:
        if 'region' in medal_tally.columns:
            fig_map = px.choropleth(
                medal_tally,
                locations="region",
                locationmode="country names",
                color="total",
                hover_name="region",
                hover_data=["Gold", "Silver", "Bronze", "total"],
                color_continuous_scale=px.colors.sequential.Plasma,
                title="Total Medals by Country"
            )
            fig_map.update_layout(margin={"r":0,"t":40,"l":0,"b":0}, height=550)
            st.plotly_chart(fig_map, use_container_width=True)
        else:
            st.info("World Map view is available when viewing all countries.")

# ==========================================
# 2. OVERALL ANALYSIS
# ==========================================
elif user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].dropna().unique().shape[0]

    st.title("📊 Historic Highlights & Statistics")

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.metric("Editions", editions)
    with col2:
        st.metric("Host Cities", cities)
    with col3:
        st.metric("Sports", sports)
    with col4:
        st.metric("Events", events)
    with col5:
        st.metric("Athletes", f"{athletes:,}")
    with col6:
        st.metric("Nations", nations)

    st.markdown("---")

    col_left, col_right = st.columns(2)
    with col_left:
        nations_over_time = helper.data_over_time(df, 'region')
        fig = px.line(nations_over_time, x="Edition", y="region", markers=True,
                      title="📈 Participating Nations Over the Years")
        fig.update_layout(xaxis_title="Olympic Edition (Year)", yaxis_title="Number of Countries")
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        events_over_time = helper.data_over_time(df, 'Event')
        fig = px.line(events_over_time, x="Edition", y="Event", markers=True,
                      title="🏅 Number of Events Over the Years", color_discrete_sequence=['#FF7F0E'])
        fig.update_layout(xaxis_title="Olympic Edition (Year)", yaxis_title="Number of Events")
        st.plotly_chart(fig, use_container_width=True)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="Name", markers=True,
                  title="🏃 Athlete Participation Over the Years", color_discrete_sequence=['#2CA02C'])
    fig.update_layout(xaxis_title="Olympic Edition (Year)", yaxis_title="Number of Athletes")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🔥 Event Density: Sports Across Editions")
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    pivot_table = x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int')
    
    fig_heatmap = px.imshow(
        pivot_table,
        labels=dict(x="Year", y="Sport", color="Events"),
        color_continuous_scale="Viridis",
        aspect="auto"
    )
    fig_heatmap.update_layout(height=800)
    st.plotly_chart(fig_heatmap, use_container_width=True)

    st.subheader("🌟 Most Successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Filter by Sport', sport_list)
    x = helper.most_successful(df, selected_sport)
    st.dataframe(x, use_container_width=True, hide_index=True)

# ==========================================
# 3. COUNTRY-WISE ANALYSIS
# ==========================================
elif user_menu == 'Country-wise Analysis':
    st.sidebar.title('Country-wise Deep Dive')
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country', country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)
    
    st.title(f"🏆 {selected_country} Olympic Journey")
    
    total_medals = country_df['Medal'].sum() if not country_df.empty else 0
    best_year_row = country_df.loc[country_df['Medal'].idxmax()] if not country_df.empty and total_medals > 0 else None
    
    mcol1, mcol2, mcol3 = st.columns(3)
    with mcol1:
        st.metric("Total Medals Won", int(total_medals))
    with mcol2:
        st.metric("Best Olympic Edition", int(best_year_row['Year']) if best_year_row is not None else "N/A")
    with mcol3:
        st.metric("Peak Medals in Single Games", int(best_year_row['Medal']) if best_year_row is not None else 0)

    fig = px.line(country_df, x="Year", y="Medal", markers=True,
                  title=f"{selected_country} Medals Won by Edition",
                  color_discrete_sequence=['#1F77B4'])
    st.plotly_chart(fig, use_container_width=True)

    st.subheader(f"🥇 Sports where {selected_country} Excels")
    pt = helper.country_event_heatmap(df, selected_country)
    if not pt.empty:
        fig_pt = px.imshow(
            pt,
            labels=dict(x="Year", y="Sport", color="Medals"),
            color_continuous_scale="YlOrRd",
            aspect="auto"
        )
        st.plotly_chart(fig_pt, use_container_width=True)
    else:
        st.info("No medal breakdown available across sports.")

    st.subheader(f"⭐ Top 10 Athletes of {selected_country}")
    top10_df = helper.most_successful_countrywise(df, selected_country)
    st.dataframe(top10_df, use_container_width=True, hide_index=True)

# ==========================================
# 4. COUNTRY HEAD-TO-HEAD COMPARISON
# ==========================================
elif user_menu == 'Country Comparison':
    st.title("⚔️ Head-to-Head Country Comparison")
    st.caption("Compare historic performance, medal trajectories, and sport dominance between any two nations.")

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    col1, col2 = st.columns(2)
    with col1:
        c1 = st.selectbox("Select Country 1", country_list, index=country_list.index("USA") if "USA" in country_list else 0)
    with col2:
        default_c2_idx = country_list.index("China") if "China" in country_list else min(1, len(country_list)-1)
        c2 = st.selectbox("Select Country 2", country_list, index=default_c2_idx)

    if c1 == c2:
        st.warning("Please choose two distinct countries to compare.")
    else:
        comp_df = helper.compare_countries(df, c1, c2)
        
        c1_tot = comp_df[f'Medal_{c1}'].sum()
        c2_tot = comp_df[f'Medal_{c2}'].sum()

        m1, m2 = st.columns(2)
        with m1:
            st.metric(f"Total Medals ({c1})", int(c1_tot))
        with m2:
            st.metric(f"Total Medals ({c2})", int(c2_tot))

        fig_comp = px.line(
            comp_df,
            x="Year",
            y=[f'Medal_{c1}', f'Medal_{c2}'],
            markers=True,
            title=f"Medal Progression: {c1} vs {c2}",
            color_discrete_sequence=['#1E88E5', '#E53935']
        )
        fig_comp.update_layout(xaxis_title="Olympic Edition", yaxis_title="Medals Won", legend_title="Country")
        st.plotly_chart(fig_comp, use_container_width=True)

        st.subheader("Historical Head-to-Head Table")
        st.dataframe(comp_df, use_container_width=True, hide_index=True)

# ==========================================
# 5. ATHLETE WISE ANALYSIS
# ==========================================
elif user_menu == 'Athlete wise Analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    st.title("🏃 Athlete Demographics & Trends")

    tab1, tab2, tab3 = st.tabs(["🎂 Age Distributions", "⚖️ Height vs Weight", "👥 Gender Participation"])

    with tab1:
        x1 = athlete_df['Age'].dropna()
        x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
        x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
        x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

        fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalists', 'Silver Medalists', 'Bronze Medalists'],
                                 show_hist=False, show_rug=False)
        fig.update_layout(autosize=False, width=1000, height=500, title="Age Distribution by Medal Status")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        sport_list = df['Sport'].unique().tolist()
        sport_list.sort()
        sport_list.insert(0, 'Overall')

        selected_sport = st.selectbox('Select Sport to Inspect Physique', sport_list)
        temp_df = helper.weight_v_height(df, selected_sport)
        
        # Plotly interactive scatter plot with hover tooltip
        fig_scatter = px.scatter(
            temp_df.dropna(subset=['Weight', 'Height']),
            x="Weight",
            y="Height",
            color="Medal",
            symbol="Sex",
            hover_name="Name",
            title=f"Height vs Weight ({selected_sport})",
            color_discrete_map={"Gold": "#FFD700", "Silver": "#C0C0C0", "Bronze": "#CD7F32", "No Medal": "#B0BEC5"}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with tab3:
        st.subheader("Gender Participation Over the Decades")
        final = helper.men_vs_women(df)
        fig_gender = px.line(final, x="Year", y=["Male", "Female"], markers=True,
                             color_discrete_sequence=['#1E88E5', '#E91E63'])
        fig_gender.update_layout(xaxis_title="Year", yaxis_title="Participant Count", legend_title="Gender")
        st.plotly_chart(fig_gender, use_container_width=True)

# ==========================================
# 6. LA 2028 OLYMPIC MEDAL PREDICTOR
# ==========================================
elif user_menu == 'LA 2028 Predictor':
    st.title("🔮 Los Angeles 2028 Olympic Medal Predictor")
    st.caption("Machine Learning (Ridge Time-Series Regression) forecast incorporating recent momentum and historical trajectories (1984 - 2024).")

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    default_idx = country_list.index("USA") if "USA" in country_list else 0
    selected_country = st.selectbox("Select Country to Predict for LA 2028", country_list, index=default_idx)

    pred, hist = helper.predict_la_2028(df, selected_country)

    if pred is None:
        st.warning(f"Insufficient modern Olympic medal data to build a reliable projection for {selected_country}.")
    else:
        st.subheader(f"🎯 Projected Medal Haul for {selected_country} in LA 2028")

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("🥇 Projected Gold", pred['Predicted_Gold'])
        with c2:
            st.metric("🥈 Projected Silver", pred['Predicted_Silver'])
        with c3:
            st.metric("🥉 Projected Bronze", pred['Predicted_Bronze'])
        with c4:
            st.metric("🏆 Total Projected Medals", pred['Predicted_Total'],
                      delta=f"{pred['Predicted_Total'] - pred['Last_Edition_Total']:+} vs Paris 2024")

        if selected_country == 'USA':
            st.info("🇺🇸 **Host Nation Factor Active**: Model includes historic host country boost for USA hosting in Los Angeles 2028.")

        # Visualizing the projection curve
        hist_modern = hist[hist['Year'] >= 1984].copy()
        
        pred_row = pd.DataFrame([{
            'Year': 2028,
            'Gold': pred['Predicted_Gold'],
            'Silver': pred['Predicted_Silver'],
            'Bronze': pred['Predicted_Bronze'],
            'Total': pred['Predicted_Total']
        }])
        
        hist_modern['Type'] = 'Actual'
        pred_row['Type'] = 'Predicted (2028)'
        chart_data = pd.concat([hist_modern, pred_row], ignore_index=True)

        fig_pred = px.line(
            chart_data,
            x="Year",
            y="Total",
            markers=True,
            title=f"{selected_country} Historical Medals and 2028 Forecast",
            color_discrete_sequence=['#1E88E5']
        )
        # Highlight the 2028 point
        fig_pred.add_scatter(
            x=[2028],
            y=[pred['Predicted_Total']],
            mode='markers+text',
            marker=dict(size=14, color='#E53935', symbol='star'),
            text=[f"2028 Forecast: {pred['Predicted_Total']} Medals"],
            textposition="top center",
            name="2028 Forecast"
        )
        fig_pred.update_layout(xaxis_title="Olympic Year", yaxis_title="Total Medals", height=500)
        st.plotly_chart(fig_pred, use_container_width=True)

        st.subheader("📊 Historical Trajectory Data (1984 - 2028 Projected)")
        st.dataframe(chart_data[['Year', 'Gold', 'Silver', 'Bronze', 'Total', 'Type']], use_container_width=True, hide_index=True)
