import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
import json
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="PowerCell Analytics Dashboard",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #00d4aa, #00a8ff);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0, 212, 170, 0.3);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .battery-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(240, 147, 251, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .healthy-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    .warning-card {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    }
    
    .success-message {
        background: linear-gradient(90deg, #56ab2f, #a8e6cf);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    
    .stSelectbox > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
        color: white;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #00d4aa, #00a8ff);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 212, 170, 0.4);
    }
    
    .battery-level {
        width: 100%;
        height: 20px;
        background: #e0e0e0;
        border-radius: 10px;
        overflow: hidden;
        margin: 10px 0;
    }
    
    .battery-fill {
        height: 100%;
        border-radius: 10px;
        transition: all 0.5s ease;
    }
    
    .fill-good {
        background: linear-gradient(90deg, #56ab2f, #a8e6cf);
    }
    
    .fill-warning {
        background: linear-gradient(90deg, #fa709a, #fee140);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'results' not in st.session_state:
    st.session_state.results = None
if 'cells_data' not in st.session_state:
    st.session_state.cells_data = {}

# Header
st.markdown("""
<div class="main-header">
    <h1>🔋 PowerCell Analytics Dashboard</h1>
    <p>Advanced Battery Cell Monitoring & Analysis System</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.markdown("## ⚙️ Cell Configuration")
    
    # Cell type options
    cell_types = {
        'lfp': 'LFP (Lithium Iron Phosphate)',
        'mnc': 'MNC (Manganese Nickel Cobalt)'
    }
    
    # Store cell configurations
    cells = []
    
    st.markdown("### Configure up to 8 battery cells:")
    
    # Number of cells selector
    num_cells = st.slider("Number of Cells", min_value=1, max_value=8, value=4)
    
    for i in range(num_cells):
        with st.expander(f"🔋 Cell #{i+1}", expanded=True):
            col1, col2 = st.columns(2)
            
            with col1:
                cell_type = st.selectbox(
                    f"Type",
                    options=list(cell_types.keys()),
                    format_func=lambda x: cell_types[x],
                    key=f"type_{i}"
                )
            
            with col2:
                current = st.number_input(
                    f"Current (A)",
                    min_value=0.0,
                    max_value=100.0,
                    value=0.0,
                    step=0.1,
                    key=f"current_{i}"
                )
            
            cells.append({'type': cell_type, 'current': current})
    
    # Calculate button
    if st.button("🚀 Analyze Battery Cells", use_container_width=True):
        # Calculate results
        results = []
        cells_data = {}
        
        for idx, cell in enumerate(cells):
            if cell['current'] > 0:
                cell_key = f"cell_{idx+1}_{cell['type']}"
                
                voltage = 3.2 if cell['type'] == "lfp" else 3.6
                max_vol = 3.4 if cell['type'] == "mnc" else 4.0
                min_vol = 2.8 if cell['type'] == "lfp" else 3.2
                current = cell['current']
                temp = round(random.uniform(25, 40), 1)
                capacity = round(voltage * current, 2)
                efficiency = round((voltage / max_vol) * 100, 1)
                health_status = 'Good' if voltage >= min_vol and voltage <= max_vol else 'Warning'
                
                cell_data = {
                    'Cell ID': cell_key,
                    'Type': cell['type'].upper(),
                    'Voltage (V)': voltage,
                    'Current (A)': current,
                    'Temperature (°C)': temp,
                    'Capacity (Wh)': capacity,
                    'Max Voltage (V)': max_vol,
                    'Min Voltage (V)': min_vol,
                    'Efficiency (%)': efficiency,
                    'Health Status': health_status
                }
                
                results.append(cell_data)
                cells_data[cell_key] = {
                    "voltage": voltage,
                    "current": current,
                    "temp": temp,
                    "capacity": capacity,
                    "Max voltage": max_vol,
                    "Min Voltage": min_vol,
                    "efficiency": efficiency,
                    "health_status": health_status
                }
        
        st.session_state.results = results
        st.session_state.cells_data = cells_data
        
        if results:
            st.success(f"✅ Successfully analyzed {len(results)} battery cells!")
        else:
            st.warning("⚠️ Please configure at least one cell with current > 0")

# Main dashboard
if st.session_state.results:
    results = st.session_state.results
    df = pd.DataFrame(results)
    
    # Summary metrics
    st.markdown("## 📊 Summary Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_capacity = df['Capacity (Wh)'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <h3>⚡ Total Capacity</h3>
            <h2>{total_capacity:.2f} Wh</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_temp = df['Temperature (°C)'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3>🌡️ Avg Temperature</h3>
            <h2>{avg_temp:.1f} °C</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        avg_efficiency = df['Efficiency (%)'].mean()
        st.markdown(f"""
        <div class="metric-card">
            <h3>⚙️ Avg Efficiency</h3>
            <h2>{avg_efficiency:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        healthy_cells = len(df[df['Health Status'] == 'Good'])
        total_cells = len(df)
        st.markdown(f"""
        <div class="metric-card">
            <h3>💚 Healthy Cells</h3>
            <h2>{healthy_cells}/{total_cells}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Battery visualization cards
    st.markdown("## 🔋 Battery Cell Status")
    
    # Create columns for battery cards
    cols = st.columns(min(len(results), 4))
    
    for i, result in enumerate(results):
        col_idx = i % 4
        with cols[col_idx]:
            health_class = "healthy-card" if result['Health Status'] == 'Good' else "warning-card"
            efficiency = result['Efficiency (%)']
            
            st.markdown(f"""
            <div class="battery-card {health_class}">
                <h4>🔋 {result['Cell ID']}</h4>
                <p><strong>Type:</strong> {result['Type']}</p>
                <p><strong>Voltage:</strong> {result['Voltage (V)']} V</p>
                <p><strong>Temperature:</strong> {result['Temperature (°C)']} °C</p>
                <p><strong>Capacity:</strong> {result['Capacity (Wh)']} Wh</p>
                <div class="battery-level">
                    <div class="battery-fill {'fill-good' if result['Health Status'] == 'Good' else 'fill-warning'}" 
                         style="width: {efficiency}%"></div>
                </div>
                <p><strong>Efficiency: {efficiency}%</strong></p>
                <p><strong>Status:</strong> {result['Health Status']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Interactive Charts
    st.markdown("## 📈 Performance Analytics")
    
    # Chart selection
    chart_tabs = st.tabs(["📊 Capacity Analysis", "🌡️ Temperature Profile", "⚙️ Efficiency Distribution", "🔋 Health Overview"])
    
    with chart_tabs[0]:
        # Capacity bar chart
        fig_capacity = px.bar(
            df, 
            x='Cell ID', 
            y='Capacity (Wh)',
            color='Type',
            title="Battery Cell Capacity Analysis",
            color_discrete_map={'LFP': '#00d4aa', 'MNC': '#00a8ff'},
            height=400
        )
        fig_capacity.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#333'),
            title_font=dict(size=20, color='#333')
        )
        st.plotly_chart(fig_capacity, use_container_width=True)
    
    with chart_tabs[1]:
        # Temperature line chart
        fig_temp = px.line(
            df, 
            x='Cell ID', 
            y='Temperature (°C)',
            markers=True,
            title="Temperature Profile Across Cells",
            color_discrete_sequence=['#fa709a'],
            height=400
        )
        fig_temp.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#333'),
            title_font=dict(size=20, color='#333')
        )
        st.plotly_chart(fig_temp, use_container_width=True)
    
    with chart_tabs[2]:
        # Efficiency distribution
        fig_efficiency = px.histogram(
            df, 
            x='Efficiency (%)',
            nbins=10,
            title="Efficiency Distribution",
            color_discrete_sequence=['#667eea'],
            height=400
        )
        fig_efficiency.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#333'),
            title_font=dict(size=20, color='#333')
        )
        st.plotly_chart(fig_efficiency, use_container_width=True)
    
    with chart_tabs[3]:
        # Health status pie chart
        health_counts = df['Health Status'].value_counts()
        fig_health = px.pie(
            values=health_counts.values,
            names=health_counts.index,
            title="Cell Health Status Distribution",
            color_discrete_map={'Good': '#00d4aa', 'Warning': '#fa709a'},
            height=400
        )
        fig_health.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#333'),
            title_font=dict(size=20, color='#333')
        )
        st.plotly_chart(fig_health, use_container_width=True)
    
    # Advanced Analytics
    st.markdown("## 🔬 Advanced Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Voltage vs Capacity scatter
        fig_scatter = px.scatter(
            df, 
            x='Voltage (V)', 
            y='Capacity (Wh)',
            color='Type',
            size='Temperature (°C)',
            title="Voltage vs Capacity Correlation",
            color_discrete_map={'LFP': '#00d4aa', 'MNC': '#00a8ff'},
            height=400
        )
        fig_scatter.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#333')
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        # Radar chart for cell comparison
        categories = ['Voltage (V)', 'Current (A)', 'Temperature (°C)', 'Capacity (Wh)', 'Efficiency (%)']
        
        fig_radar = go.Figure()
        
        for i, result in enumerate(results[:3]):  # Show first 3 cells
            values = [
                result['Voltage (V)'] * 10,  # Scale for visibility
                result['Current (A)'],
                result['Temperature (°C)'],
                result['Capacity (Wh)'],
                result['Efficiency (%)']
            ]
            
            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself',
                name=result['Cell ID']
            ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100])
            ),
            showlegend=True,
            title="Multi-Cell Performance Comparison",
            height=400
        )
        st.plotly_chart(fig_radar, use_container_width=True)
    
    # Data Table
    st.markdown("## 📋 Detailed Analysis Table")
    
    # Enhanced dataframe display
    st.dataframe(
        df,
        use_container_width=True,
        column_config={
            "Cell ID": st.column_config.TextColumn("🔋 Cell ID"),
            "Type": st.column_config.TextColumn("⚡ Type"),
            "Voltage (V)": st.column_config.NumberColumn("🔌 Voltage (V)", format="%.2f"),
            "Current (A)": st.column_config.NumberColumn("⚡ Current (A)", format="%.2f"),
            "Temperature (°C)": st.column_config.NumberColumn("🌡️ Temperature (°C)", format="%.1f"),
            "Capacity (Wh)": st.column_config.NumberColumn("🔋 Capacity (Wh)", format="%.2f"),
            "Efficiency (%)": st.column_config.ProgressColumn("⚙️ Efficiency (%)", min_value=0, max_value=100),
            "Health Status": st.column_config.TextColumn("💚 Health Status")
        }
    )
    
    # Export Options
    st.markdown("## 📤 Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv = df.to_csv(index=False)
        st.download_button(
            label="📊 Download CSV",
            data=csv,
            file_name=f"battery_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        json_data = json.dumps(st.session_state.cells_data, indent=2)
        st.download_button(
            label="📋 Download JSON",
            data=json_data,
            file_name=f"battery_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )
    
    with col3:
        # Generate report
        report = f"""
# Battery Analysis Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- Total Cells Analyzed: {len(df)}
- Total Capacity: {total_capacity:.2f} Wh
- Average Temperature: {avg_temp:.1f} °C
- Average Efficiency: {avg_efficiency:.1f}%
- Healthy Cells: {healthy_cells}/{total_cells}

## Cell Details
{df.to_string()}
        """
        
        st.download_button(
            label="📄 Download Report",
            data=report,
            file_name=f"battery_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain",
            use_container_width=True
        )

else:
    # Welcome message when no results
    st.markdown("""
    <div class="success-message">
        <h2>👈 Configure your battery cells in the sidebar</h2>
        <p>Set up cell types and current values, then click "Analyze Battery Cells" to see detailed analytics!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sample data preview
    st.markdown("## 🔬 What You'll Get:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 📊 Interactive Charts
        - Capacity analysis
        - Temperature profiles
        - Efficiency distributions
        - Health status overview
        """)
    
    with col2:
        st.markdown("""
        ### 🔋 Battery Visualization
        - Real-time battery level indicators
        - Color-coded health status
        - Performance metrics
        - Efficiency tracking
        """)
    
    with col3:
        st.markdown("""
        ### 📤 Export Options
        - CSV data export
        - JSON configuration
        - Detailed reports
        - Performance analytics
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    <p>🔋 PowerCell Analytics Dashboard | Built with Streamlit | Advanced Battery Monitoring System</p>
</div>
""", unsafe_allow_html=True)