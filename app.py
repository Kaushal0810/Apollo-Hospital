import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

import base64
from pathlib import Path
import plotly.io as pio
import plotly.graph_objects as go

# ==========================================
# GLOBAL PLOTLY THEME (Apollo Dark Mode)
# ==========================================
pio.templates["apollo_dark"] = go.layout.Template(
    layout=go.Layout(
        # 1. Make backgrounds transparent to blend with the image
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        
        # 2. Text and Font Colors
        font=dict(color="#E2E8F0", family="Arial, sans-serif", size=12),
        title=dict(font=dict(color="white", size=16)),
        
        # 3. Subtle Grid Lines (so they don't distract from the background)
        xaxis=dict(gridcolor="rgba(255,255,255,0.08)", zerolinecolor="rgba(255,255,255,0.1)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.08)", zerolinecolor="rgba(255,255,255,0.1)"),
        
        # 4. Legend Text
        legend=dict(font=dict(color="#E2E8F0")),
        
        # 5. Custom Apollo-Branded Color Palette
        # Blue, Cyan, Teal, Gold, Red, Purple, Orange
        colorway=["#00A3E0", "#005691", "#48C9B0", "#F4D03F", "#E74C3C", "#9B59B6", "#E67E22"]
    )
)

# Apply the template globally
pio.templates.default = "apollo_dark"

# ==========================================
# BACKGROUND IMAGE HELPER
# ==========================================
@st.cache_data
def _image_to_data_url(path: Path) -> str:
    """Convert a local image to an embedded Base64 data URL."""
    ext = path.suffix.lower()
    mime = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
        ".gif": "image/gif",
    }.get(ext, "image/png")

    encoded = base64.b64encode(path.read_bytes()).decode()
    return f"data:{mime};base64,{encoded}"


def set_background(image="assets/apollo_bg.jpg", overlay=0.80):
    """
    Apply a background image to the whole Streamlit app.
    overlay = white wash strength (0.0 = full image, 0.9 = very faint image)
    """
    path = Path(__file__).resolve().parent / image

    if not path.exists():
        st.warning(f"⚠️ Background image not found at: `{path}`")
        return

    bg_url = _image_to_data_url(path)

    st.markdown(
        f"""
        <style>
            /* 1. Main App Background */
            [data-testid="stAppViewContainer"] {{
                background-image:
                    linear-gradient(rgba(10, 25, 45, 0.88), rgba(10, 25, 45, 0.88)),
                    url("{bg_url}");
                background-size: cover;
                background-position: center top;
                background-attachment: fixed;
            }}

            /* 2. Make Sidebar COMPLETELY Transparent */
            section[data-testid="stSidebar"],
            [data-testid="stSidebar"] {{
                background-color: transparent !important;
                background-image: none !important;
            }}

            /* 3. Style the Filter Boxes (Multiselect & Selectbox) */
            div[data-testid="stSidebar"] div[data-baseweb="select"] > div {{
                background-color: rgba(30, 41, 59, 0.75) !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
                border-radius: 8px !important;
            }}

            /* 4. Make text inside filters White */
            div[data-testid="stSidebar"] div[data-baseweb="select"] span,
            div[data-testid="stSidebar"] div[data-baseweb="input"] span {{
                color: #ffffff !important;
            }}

            /* 5. Style the Selected Tags (Chips) in Multiselect */
            div[data-testid="stSidebar"] div[data-baseweb="tag"] {{
                background-color: #00A3E0 !important; /* Apollo Blue */
                color: white !important;
                border-radius: 4px !important;
            }}

            /* 6. Style the Dropdown Menu when it opens */
            div[data-testid="stSidebar"] div[data-baseweb="popover"] {{
                background-color: rgba(15, 23, 42, 0.98) !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
            }}
            div[data-testid="stSidebar"] div[data-baseweb="popover"] span {{
                color: white !important;
            }}

            /* 7. KPI Cards & Tabs (Kept from before) */
            [data-testid="stMetric"] {{
                background: rgba(30, 41, 59, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 14px 18px;
            }}
            [data-testid="stMetric"] div {{ color: white !important; }}
            
            .stTabs [data-baseweb="tab-list"] {{
                background-color: rgba(30, 41, 59, 0.9);
                border-radius: 10px;
                padding: 6px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# ==========================================
# 1. PAGE CONFIG & DATA LOADING
# ==========================================
st.set_page_config(page_title="Apollo Hospitals Analytics", page_icon="🏥", layout="wide")

set_background("assets/apollo_bg.jpg", overlay=0.85)

@st.cache_data
def load_and_merge_data():
    # Load data
    fact_df = pd.read_csv('apollo_appointments_fact.csv')
    dim_df = pd.read_csv('apollo_doctors_dim.csv')
    
    # Date conversions
    fact_df['appointment_date'] = pd.to_datetime(fact_df['appointment_date'])
    fact_df['booking_date'] = pd.to_datetime(fact_df['booking_date'])
    
    # FIX: Explicitly define suffixes so overlapping columns become _fact and _dim
    df = pd.merge(fact_df, dim_df, on='doctor_id', how='left', suffixes=('_fact', '_dim'))
    
    # Create historical and completed subsets
    df['is_historical'] = df['appointment_status'] != 'Scheduled'
    df['is_completed'] = df['appointment_status'] == 'Completed'
    
    # Ensure lead_time_bin and patient_segment exist (in case they weren't saved in CSV)
    if 'lead_time_bin' not in df.columns:
        bins = [0, 1, 3, 7, 14, 30, 100]
        labels = ['Same Day', '1-3 Days', '4-7 Days', '1-2 Weeks', '2-4 Weeks', '>1 Month']
        df['lead_time_bin'] = pd.cut(df['booking_lead_days'], bins=bins, labels=labels, right=True)
        
    if 'patient_segment' not in df.columns:
        df['patient_segment'] = df['apollo_member'].astype(str) + ' - ' + df['repeat_visit'].astype(str)
        
    return df

# Load data
df = load_and_merge_data()

# ==========================================
# 2. SIDEBAR FILTERS
# ==========================================
st.sidebar.title("🔍 Dashboard Filters")

# Filter by Year
years = st.sidebar.multiselect(
    "Select Year(s):", 
    sorted(df['appointment_year'].unique()), 
    default=sorted(df['appointment_year'].unique())
)

# Filter by Specialty (using _fact column)
specialties = st.sidebar.multiselect(
    "Select Specialty:", 
    sorted(df['specialty_fact'].dropna().unique()), 
    default=sorted(df['specialty_fact'].dropna().unique())
)

# Filter by City (using _fact column)
cities = st.sidebar.multiselect(
    "Select City:", 
    sorted(df['city_fact'].dropna().unique()), 
    default=sorted(df['city_fact'].dropna().unique())
)

# Apply filters
filtered_df = df[
    (df['appointment_year'].isin(years)) & 
    (df['specialty_fact'].isin(specialties)) & 
    (df['city_fact'].isin(cities))
]

# Create filtered subsets
hist_df = filtered_df[filtered_df['is_historical'] == True]
comp_df = filtered_df[filtered_df['is_completed'] == True]

# ==========================================
# 3. HEADER & KPI CARDS
# ==========================================
st.title("🏥 Apollo Hospitals Operations Dashboard")
st.markdown("Analyzing appointment data across multiple cities and specialties (2022-2024).")

# Calculate KPIs
total_appts = len(hist_df)
noshow_rate = (hist_df['no_show_flag'].mean() * 100) if len(hist_df) > 0 else 0
# Use consultation_fee_fact for opportunity cost of no-shows
revenue_lost = hist_df[hist_df['no_show_flag'] == 1]['consultation_fee_fact'].sum()
avg_satisfaction = comp_df['patient_satisfaction_score'].mean() if len(comp_df) > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Appointments", f"{total_appts:,}")
col2.metric("No-Show Rate", f"{noshow_rate:.1f}%")
col3.metric("Revenue Lost (No-Shows)", f"₹{revenue_lost:,.0f}")
col4.metric("Avg Satisfaction (1-5)", f"{avg_satisfaction:.2f}" if avg_satisfaction > 0 else "N/A")

st.divider()

# ==========================================
# 4. DASHBOARD TABS
# ==========================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📈 Business Overview", 
    "🚫 No-Show Analysis", 
    "🔔 Reminders & Engagement", 
    "👥 Demographics", 
    "💰 Financials", 
    "🩺 Doctor & Quality"
])

# --- TAB 1: BUSINESS OVERVIEW ---
with tab1:
    st.subheader("Appointment Volume & Outcomes")
    col1, col2 = st.columns(2)
    
    with col1:
        monthly_vol = hist_df.groupby(['appointment_year', 'appointment_month']).size().reset_index(name='volume')
        monthly_vol['year_month'] = monthly_vol['appointment_year'].astype(str) + '-' + monthly_vol['appointment_month'].astype(str).str.zfill(2)
        fig_trend = px.line(monthly_vol, x='year_month', y='volume', markers=True, title='Monthly Appointment Volume')
        fig_trend.update_layout(
         paper_bgcolor="rgba(30, 41, 59, 0.4)",  # Semi-transparent dark blue
         plot_bgcolor="rgba(30, 41, 59, 0.4)",
         margin=dict(l=10, r=10, t=30, b=10)     # Reduces padding for a cleaner look)
         )
        st.plotly_chart(fig_trend, use_container_width=True)
        
    with col2:
        outcome_counts = hist_df['appointment_status'].value_counts().reset_index()
        outcome_counts.columns = ['Status', 'Count']
        fig_pie = px.pie(outcome_counts, values='Count', names='Status', hole=0.4, title='Outcome Distribution',
                         color='Status', color_discrete_map={'Completed': '#2ca02c', 'No-Show': '#d62728', 'Cancelled': '#ff7f0e', 'Scheduled': '#1f77b4'})
        
        fig_pie.update_layout(
         paper_bgcolor="rgba(30, 41, 59, 0.4)",  # Semi-transparent dark blue
         plot_bgcolor="rgba(30, 41, 59, 0.4)",
         margin=dict(l=10, r=10, t=30, b=10)     # Reduces padding for a cleaner look)
         )
        st.plotly_chart(fig_pie, use_container_width=True)

    channel_vol = hist_df['booking_channel'].value_counts().reset_index()
    channel_vol.columns = ['Channel', 'Count']
    fig_chan = px.bar(channel_vol, x='Channel', y='Count', text='Count', title='Volume by Booking Channel')
    fig_chan.update_traces(textposition='outside')
    fig_chan.update_layout(
         paper_bgcolor="rgba(30, 41, 59, 0.4)",  # Semi-transparent dark blue
         plot_bgcolor="rgba(30, 41, 59, 0.4)",
         margin=dict(l=10, r=10, t=30, b=10)     # Reduces padding for a cleaner look)
         )
    st.plotly_chart(fig_chan, use_container_width=True)

# --- TAB 2: NO-SHOW ANALYSIS ---
with tab2:
    st.subheader("No-Show Risk Factors")
    col1, col2 = st.columns(2)
    
    with col1:
        noshow_spec = hist_df.groupby('specialty_fact')['no_show_flag'].mean().reset_index()
        noshow_spec['pct'] = (noshow_spec['no_show_flag'] * 100).round(1)
        noshow_spec = noshow_spec.sort_values('pct', ascending=False)
        fig_ns_spec = px.bar(noshow_spec.head(10), x='pct', y='specialty_fact', orientation='h',
                             title='Top 10 Specialties by No-Show Rate (%)', color='pct', color_continuous_scale='Reds')
        fig_ns_spec.update_layout(
         paper_bgcolor="rgba(30, 41, 59, 0.4)",  # Semi-transparent dark blue
         plot_bgcolor="rgba(30, 41, 59, 0.4)",
         margin=dict(l=10, r=10, t=30, b=10)     # Reduces padding for a cleaner look)
         )
        st.plotly_chart(fig_ns_spec, use_container_width=True)

    with col2:
        lead_ns = hist_df.groupby('lead_time_bin', observed=False)['no_show_flag'].mean().reset_index()
        lead_ns['pct'] = (lead_ns['no_show_flag'] * 100).round(1)
        fig_lead = px.line(lead_ns, x='lead_time_bin', y='pct', markers=True, title='No-Show Rate by Booking Lead Time')
        fig_lead.update_layout(
         paper_bgcolor="rgba(30, 41, 59, 0.4)",  # Semi-transparent dark blue
         plot_bgcolor="rgba(30, 41, 59, 0.4)",
         margin=dict(l=10, r=10, t=30, b=10)     # Reduces padding for a cleaner look)
         )
        st.plotly_chart(fig_lead, use_container_width=True)

    time_ns = hist_df.groupby('time_of_day')['no_show_flag'].mean().reset_index()
    time_ns['pct'] = (time_ns['no_show_flag'] * 100).round(1)
    fig_time = px.bar(time_ns, x='time_of_day', y='pct', text_auto='.1f', title='No-Show Rate by Time of Day')
    fig_time.update_layout(
         paper_bgcolor="rgba(30, 41, 59, 0.4)",  # Semi-transparent dark blue
         plot_bgcolor="rgba(30, 41, 59, 0.4)",
         margin=dict(l=10, r=10, t=30, b=10)     # Reduces padding for a cleaner look)
         )
    st.plotly_chart(fig_time, use_container_width=True)

# --- TAB 3: REMINDERS & ENGAGEMENT ---
with tab3:
    st.subheader("Reminder Effectiveness & Patient Segments")
    col1, col2 = st.columns(2)
    
    with col1:
        rem_ns = hist_df.groupby('reminder_type')['no_show_flag'].mean().reset_index()
        rem_ns['pct'] = (rem_ns['no_show_flag'] * 100).round(1)
        rem_ns = rem_ns.sort_values('pct')
        fig_rem = px.bar(rem_ns, x='reminder_type', y='pct', text_auto='.1f', title='No-Show Rate by Reminder Type',
                         color='pct', color_continuous_scale='RdYlGn_r')
        fig_rem.update_layout(
         paper_bgcolor="rgba(30, 41, 59, 0.4)",  # Semi-transparent dark blue
         plot_bgcolor="rgba(30, 41, 59, 0.4)",
         margin=dict(l=10, r=10, t=30, b=10)     # Reduces padding for a cleaner look)
         )
        st.plotly_chart(fig_rem, use_container_width=True)

    with col2:
        seg_ns = hist_df.groupby('patient_segment')['no_show_flag'].mean().reset_index()
        seg_ns['pct'] = (seg_ns['no_show_flag'] * 100).round(1)
        fig_seg = px.bar(seg_ns, x='patient_segment', y='pct', text_auto='.1f', title='No-Show Rate by Patient Segment')
        fig_seg.update_layout(
         paper_bgcolor="rgba(30, 41, 59, 0.4)",  # Semi-transparent dark blue
         plot_bgcolor="rgba(30, 41, 59, 0.4)",
         margin=dict(l=10, r=10, t=30, b=10)     # Reduces padding for a cleaner look)
         )
        st.plotly_chart(fig_seg, use_container_width=True)

# --- TAB 4: DEMOGRAPHICS ---
with tab4:
    st.subheader("Patient Age & Visit Reasons")
    col1, col2 = st.columns(2)
    
    with col1:
        target_specs = ['Paediatrics', 'Gynaecology', 'Psychiatry']
        filt_demo = hist_df[hist_df['specialty_fact'].isin(target_specs)]
        fig_age = px.histogram(filt_demo, x='patient_age', color='specialty_fact', barmode='overlay', opacity=0.7,
                               title='Age Distribution in Key Specialties', nbins=30)
        fig_age.update_layout(
         paper_bgcolor="rgba(30, 41, 59, 0.4)",  # Semi-transparent dark blue
         plot_bgcolor="rgba(30, 41, 59, 0.4)",
         margin=dict(l=10, r=10, t=30, b=10)     # Reduces padding for a cleaner look)
         )
        st.plotly_chart(fig_age, use_container_width=True)

    with col2:
        reason_ns = hist_df.groupby('visit_reason')['no_show_flag'].mean().reset_index()
        reason_ns['pct'] = (reason_ns['no_show_flag'] * 100).round(1)
        reason_ns = reason_ns.sort_values('pct', ascending=False)
        fig_reason = px.bar(reason_ns, x='pct', y='visit_reason', orientation='h', title='No-Show Rate by Visit Reason')
        fig_reason.update_layout(
         paper_bgcolor="rgba(30, 41, 59, 0.4)",  # Semi-transparent dark blue
         plot_bgcolor="rgba(30, 41, 59, 0.4)",
         margin=dict(l=10, r=10, t=30, b=10)     # Reduces padding for a cleaner look)
         )
        st.plotly_chart(fig_reason, use_container_width=True)

# --- TAB 5: FINANCIALS ---
with tab5:
    st.subheader("Revenue & Payment Metrics")
    
    city_rev = comp_df.groupby(['city_fact', 'payment_mode'])['revenue_realized'].sum().reset_index()
    fig_city_rev = px.bar(city_rev, x='city_fact', y='revenue_realized', color='payment_mode', barmode='stack',
                          title='Total Realized Revenue by City and Payment Mode')
    fig_city_rev.update_layout(
         paper_bgcolor="rgba(30, 41, 59, 0.4)",  # Semi-transparent dark blue
         plot_bgcolor="rgba(30, 41, 59, 0.4)",
         margin=dict(l=10, r=10, t=30, b=10)     # Reduces padding for a cleaner look)
         )
    st.plotly_chart(fig_city_rev, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        ins_oop = comp_df.groupby('insurance_coverage')['patient_out_of_pocket'].mean().reset_index()
        fig_ins = px.bar(ins_oop, x='insurance_coverage', y='patient_out_of_pocket', text_auto='₹,.0f',
                         title='Avg Out-of-Pocket by Insurance Status')
        fig_ins.update_layout(
         paper_bgcolor="rgba(30, 41, 59, 0.4)",  # Semi-transparent dark blue
         plot_bgcolor="rgba(30, 41, 59, 0.4)",
         margin=dict(l=10, r=10, t=30, b=10)     # Reduces padding for a cleaner look)
         )
        st.plotly_chart(fig_ins, use_container_width=True)
        
    with col2:
        spec_rev = comp_df.groupby('specialty_fact')['revenue_realized'].sum().reset_index().sort_values('revenue_realized', ascending=False)
        fig_spec_rev = px.bar(spec_rev.head(10), x='revenue_realized', y='specialty_fact', orientation='h',
                              title='Top 10 Specialties by Revenue')
        fig_spec_rev.update_layout(
         paper_bgcolor="rgba(30, 41, 59, 0.4)",  # Semi-transparent dark blue
         plot_bgcolor="rgba(30, 41, 59, 0.4)",
         margin=dict(l=10, r=10, t=30, b=10)     # Reduces padding for a cleaner look)
         )
        st.plotly_chart(fig_spec_rev, use_container_width=True)

# --- TAB 6: DOCTOR & QUALITY ---
with tab6:
    st.subheader("Service Quality & Doctor Metrics")
    col1, col2 = st.columns(2)
    
    with col1:
        fig_exp = px.scatter(comp_df, x='experience_years', y='consultation_fee_dim', 
                             color='specialty_dim', trendline='ols', hover_data=['doctor_name'],
                             title='Doctor Experience vs Consultation Fee')
        fig_exp.update_layout(
         paper_bgcolor="rgba(30, 41, 59, 0.4)",  # Semi-transparent dark blue
         plot_bgcolor="rgba(30, 41, 59, 0.4)",
         margin=dict(l=10, r=10, t=30, b=10)     # Reduces padding for a cleaner look)
         )
        st.plotly_chart(fig_exp, use_container_width=True)

    with col2:
        clean_q = comp_df.dropna(subset=['wait_time_minutes', 'patient_satisfaction_score'])
        fig_wait = px.scatter(clean_q, x='wait_time_minutes', y='patient_satisfaction_score', 
                              color='specialty_fact', trendline='lowess', opacity=0.6,
                              title='Wait Time vs Satisfaction (Completed Only)')
        fig_wait.update_layout(
         paper_bgcolor="rgba(30, 41, 59, 0.4)",  # Semi-transparent dark blue
         plot_bgcolor="rgba(30, 41, 59, 0.4)",
         margin=dict(l=10, r=10, t=30, b=10)     # Reduces padding for a cleaner look)
         )
        st.plotly_chart(fig_wait, use_container_width=True)

    util_spec = comp_df.groupby('specialty_fact')['doctor_utilization_pct'].mean().reset_index().sort_values('doctor_utilization_pct', ascending=False)
    fig_util = px.bar(util_spec, x='doctor_utilization_pct', y='specialty_fact', orientation='h',
                      title='Avg Doctor Utilization Rate (%) by Specialty')
    fig_util.update_layout(
         paper_bgcolor="rgba(30, 41, 59, 0.4)",  # Semi-transparent dark blue
         plot_bgcolor="rgba(30, 41, 59, 0.4)",
         margin=dict(l=10, r=10, t=30, b=10)     # Reduces padding for a cleaner look)
         )
    st.plotly_chart(fig_util, use_container_width=True)