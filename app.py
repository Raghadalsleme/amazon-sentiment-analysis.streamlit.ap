import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Amazon Reviews Dashboard", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #F8F9FA;
    }
    
    .main-header {
        color: #232F3E;
        font-weight: 700;
        font-size: 2.2rem;
        margin-bottom: 0px;
        padding-bottom: 10px;
        border-bottom: 3px solid #FF9900;
        display: inline-block;
    }
    
    .sub-header {
        color: #6c757d;
        font-size: 1.1rem;
        margin-top: 10px;
        margin-bottom: 30px;
    }
    
    .kpi-container {
        background-color: white;
        padding: 25px 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border-top: 4px solid #232F3E;
        text-align: center;
        transition: transform 0.2s;
    }
    
    .kpi-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .kpi-container.orange-border {
        border-top: 4px solid #FF9900;
    }
    
    .kpi-label {
        color: #6c757d;
        font-size: 0.9rem;
        text-transform: uppercase;
        font-weight: 600;
        letter-spacing: 1px;
    }
    
    .kpi-val {
        color: #232F3E;
        font-size: 2.2rem;
        font-weight: 700;
        margin-top: 5px;
    }
    
    .chart-container {
        background-color: white;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>Amazon Product Reviews Analytics</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Executive Summary & Sentiment Extraction Dashboard</p>", unsafe_allow_html=True)

@st.cache_data
def load_data():
    sentiment_counts = pd.read_csv('sentiment_counts.csv')
    pos_pd = pd.read_csv('positive_patterns.csv')
    neg_pd = pd.read_csv('negative_patterns.csv')
    return sentiment_counts, pos_pd, neg_pd

sentiment_counts, pos_pd, neg_pd = load_data()

total_reviews = sentiment_counts['count'].sum()
pos_reviews = sentiment_counts[sentiment_counts['sentiment'] == 'Positive']['count'].values[0]
satisfaction_rate = (pos_reviews / total_reviews) * 100

c1, c2, c3 = st.columns(3)
c1.markdown(f"<div class='kpi-container'><div class='kpi-label'>Total Reviews Processed</div><div class='kpi-val'>{total_reviews:,}</div></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='kpi-container orange-border'><div class='kpi-label'>Overall Satisfaction Rate</div><div class='kpi-val'>{satisfaction_rate:.1f}%</div></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='kpi-container'><div class='kpi-label'>Top Positive Pattern</div><div class='kpi-val' style='font-size:1.8rem; margin-top:10px;'>{pos_pd.iloc[0]['bigram'].title()}</div></div>", unsafe_allow_html=True)

st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("<h3 style='color: #232F3E; font-size: 1.2rem; font-weight: 600;'>Sentiment Distribution</h3>", unsafe_allow_html=True)
    fig_pie = px.pie(sentiment_counts, values='count', names='sentiment', hole=0.5,
                     color='sentiment', color_discrete_map={'Positive':"#04162C", 'Negative':'#FF9900'})
    fig_pie.update_layout(
        margin=dict(t=20, b=20, l=0, r=0), 
        showlegend=True, 
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    st.markdown("<h3 style='color: #232F3E; font-size: 1.2rem; font-weight: 600;'>Linguistic Pattern Extraction</h3>", unsafe_allow_html=True)
    tab_pos, tab_neg = st.tabs(["Positive Feedback Patterns", "Negative Feedback Patterns"])
    
    with tab_pos:
        fig_pos = px.bar(pos_pd, x='frequency', y='bigram', orientation='h')
        fig_pos.update_traces(marker_color="#051C38")
        fig_pos.update_layout(
            yaxis={'categoryorder':'total ascending'}, 
            margin=dict(t=10, b=0, l=0, r=0), 
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#E2E8F0'),
            yaxis_title=None,
            xaxis_title="Frequency"
        )
        st.plotly_chart(fig_pos, use_container_width=True)
        
    with tab_neg:
        fig_neg = px.bar(neg_pd, x='frequency', y='bigram', orientation='h')
        fig_neg.update_traces(marker_color='#FF9900')
        fig_neg.update_layout(
            yaxis={'categoryorder':'total ascending'}, 
            margin=dict(t=10, b=0, l=0, r=0), 
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='#E2E8F0'),
            yaxis_title=None,
            xaxis_title="Frequency"
        )
        st.plotly_chart(fig_neg, use_container_width=True)
