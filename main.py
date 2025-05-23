import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Delivery TAT Calculator")
st.write("Debug: Application Started")

def parse_date(date_str):
    """Try different date formats and return parsed datetime"""
    if pd.isna(date_str):
        return None
        
    # List of possible date formats (with and without 'at')
    formats = [
        '%A, %B %d, %Y, %I:%M:%S %p',      # Monday, April 21, 2025, 11:45:14 PM
        '%A, %B %d, %Y at %I:%M:%S %p',    # Monday, April 21, 2025 at 11:45:14 PM
        '%A, %B %d, %Y, %I:%M %p',         # Monday, April 21, 2025, 11:45 PM
        '%A, %B %d, %Y at %I:%M %p',       # Monday, April 21, 2025 at 11:45 PM
        '%m/%d/%y %H:%M',                  # 12/12/24 23:33
        '%m/%d/%Y %H:%M',                  # 12/13/2024 10:25
        '%m/%d/%Y %H:%M:%S'                # 12/13/2024 10:25:00
    ]
    
    for fmt in formats:
        try:
            return pd.to_datetime(date_str, format=fmt)
        except:
            continue
    
    # If none of the specific formats work, try pandas' general parser
    try:
        return pd.to_datetime(date_str)
    except:
        return None

def calculate_tat(df):
    st.write("Debug: Calculating TAT")
    # Create a copy of the dataframe
    df_processed = df.copy()
    
    # Debug: Show sample of input dates
    st.write("Debug: Sample dates from input:")
    st.write("Created time:", df_processed['Created time'].iloc[0] if not df_processed.empty else "No data")
    st.write("Approval time:", df_processed['Approval time'].iloc[0] if not df_processed.empty else "No data")
    st.write("Delivered time:", df_processed['Delivered time'].iloc[0] if not df_processed.empty else "No data")
    
    try:
        # Convert string timestamps to datetime objects using the flexible parser
        df_processed['created_datetime'] = df_processed['Created time'].apply(parse_date)
        df_processed['approval_datetime'] = df_processed['Approval time'].apply(parse_date)
        df_processed['delivery_datetime'] = df_processed['Delivered time'].apply(parse_date)
        
        # Debug: Show sample of parsed dates
        st.write("Debug: Sample parsed dates:")
        st.write("created_datetime:", df_processed['created_datetime'].iloc[0] if not df_processed.empty else "No data")
        st.write("approval_datetime:", df_processed['approval_datetime'].iloc[0] if not df_processed.empty else "No data")
        st.write("delivery_datetime:", df_processed['delivery_datetime'].iloc[0] if not df_processed.empty else "No data")
        
        # Calculate time differences in minutes
        df_processed['Created to Approval TAT (minutes)'] = (df_processed['approval_datetime'] - df_processed['created_datetime']).dt.total_seconds() / 60
        df_processed['Created to Delivery TAT (minutes)'] = (df_processed['delivery_datetime'] - df_processed['created_datetime']).dt.total_seconds() / 60
        df_processed['Approval to Delivery TAT (minutes)'] = (df_processed['delivery_datetime'] - df_processed['approval_datetime']).dt.total_seconds() / 60
        
        # Debug: Show sample of calculated differences
        st.write("Debug: Sample time differences (minutes):")
        st.write("Created to Approval:", df_processed['Created to Approval TAT (minutes)'].iloc[0] if not df_processed.empty else "No data")
        st.write("Created to Delivery:", df_processed['Created to Delivery TAT (minutes)'].iloc[0] if not df_processed.empty else "No data")
        st.write("Approval to Delivery:", df_processed['Approval to Delivery TAT (minutes)'].iloc[0] if not df_processed.empty else "No data")
        
    except Exception as e:
        st.error(f"Error during date processing: {str(e)}")
    
    # Format TAT as days, hours, and minutes
    def format_tat_detailed(minutes):
        if pd.isna(minutes):
            return "No delivery data"
        days = int(minutes // (24 * 60))
        remaining_minutes = minutes % (24 * 60)
        hours = int(remaining_minutes // 60)
        mins = int(remaining_minutes % 60)
        if days > 0:
            return f"{days}d {hours}h {mins}m"
        return f"{hours}h {mins}m"
    
    # Format TAT as hours and minutes (for summary metrics)
    def format_tat_simple(minutes):
        if pd.isna(minutes):
            return "No delivery data"
        hours = int(minutes // 60)
        mins = int(minutes % 60)
        return f"{hours}h {mins}m"
    
    # Apply detailed formatting to all TAT columns
    df_processed['Created to Approval TAT'] = df_processed['Created to Approval TAT (minutes)'].apply(format_tat_detailed)
    df_processed['Created to Delivery TAT'] = df_processed['Created to Delivery TAT (minutes)'].apply(format_tat_detailed)
    df_processed['Approval to Delivery TAT'] = df_processed['Approval to Delivery TAT (minutes)'].apply(format_tat_detailed)
    
    st.write("Debug: TAT Calculation Complete")
    return df_processed, format_tat_simple

# File upload
st.write("Debug: Before file uploader")
uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])
st.write("Debug: After file uploader")

if uploaded_file is not None:
    st.write("Debug: File uploaded")
    try:
        # Read CSV
        df = pd.read_csv(uploaded_file)
        st.write("Debug: CSV read successful")
        st.write("Debug: CSV columns:", df.columns.tolist())
        st.write("Debug: First row of data:", df.iloc[0].to_dict())
        
        # Calculate TAT
        df_with_tat, format_tat_simple = calculate_tat(df)
        
        # Display summary statistics for all TAT metrics
        st.subheader("Delivery TAT Summary")
        
        # Function to display metrics for each TAT type
        def display_tat_metrics(tat_column, title):
            tat_stats = df_with_tat[df_with_tat[tat_column].notna()]
            if not tat_stats.empty:
                st.write(f"**{title}**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Average", 
                             format_tat_simple(tat_stats[tat_column].mean()))
                with col2:
                    st.metric("Minimum", 
                             format_tat_simple(tat_stats[tat_column].min()))
                with col3:
                    st.metric("Maximum", 
                             format_tat_simple(tat_stats[tat_column].max()))
        
        # Display metrics for all three TAT calculations
        display_tat_metrics('Created to Approval TAT (minutes)', 'Created to Approval Time')
        display_tat_metrics('Created to Delivery TAT (minutes)', 'Created to Delivery Time')
        display_tat_metrics('Approval to Delivery TAT (minutes)', 'Approval to Delivery Time')
        
        # Display the processed dataframe
        st.subheader("Processed Data")
        display_columns = [
            'Created time', 
            'Approval time',
            'Delivered time',
            'Created to Approval TAT',
            'Created to Delivery TAT', 
            'Approval to Delivery TAT',
            'order_id'
        ]
        # Only show columns that exist
        display_columns = [col for col in display_columns if col in df_with_tat.columns]
        st.dataframe(df_with_tat[display_columns])
        
        # Download button for processed data
        csv = df_with_tat.to_csv(index=False)
        st.download_button(
            label="Download processed data as CSV",
            data=csv,
            file_name="delivery_data_with_tat.csv",
            mime="text/csv"
        )
        
    except Exception as e:
        st.error(f"An error occurred while processing the file: {str(e)}")
        st.write("Please ensure your CSV file has the correct format with 'Created time', 'Approval time', and 'Delivered time' columns.")
        st.write("Supported date formats:")
        st.write("1. 'Monday, April 21, 2025, 11:45:14 PM'")
        st.write("2. 'Monday, April 21, 2025 at 11:45:14 PM'")
        st.write("3. '12/12/24 23:33'")
        st.write("4. '12/13/2024 10:25'")
else:
    st.write("Debug: No file uploaded yet")