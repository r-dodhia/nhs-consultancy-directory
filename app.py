import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="Internal NHS consultancies", layout="wide")

@st.cache_data
def load_data():
    # Read both sheets from the new file
    profile_df = pd.read_excel('NHS consultancies mapping.xlsx.xlsx', sheet_name='Profile')
    capability_df = pd.read_excel('NHS consultancies mapping.xlsx.xlsx', sheet_name='Capability')
    
    # Ensure text columns are strings to avoid filtering errors
    capability_df['Service Theme'] = capability_df['Service Theme'].astype(str).str.strip()
    capability_df['Capability'] = capability_df['Capability'].astype(str).str.strip()
    
    # Get unique consultancies
    all_consultancies = sorted(profile_df['Consultancy'].dropna().unique().tolist())
    
    # Create a dictionary for quick profile lookups (website and geography)
    profile_map = profile_df.set_index('Consultancy').to_dict('index')
    
    return capability_df, all_consultancies, profile_map

capability_df, all_consultancies, profile_map = load_data()

# Build the front end
st.title("Find an internal NHS consultancy")
st.write("Search and filter to find partners for your digital strategy.")

# Sidebar filters
st.sidebar.header("Filter directory")
search_query = st.sidebar.text_input("Search by consultancy or capability")

themes = ['All'] + sorted(capability_df['Service Theme'].unique().tolist())
selected_theme = st.sidebar.selectbox("Service theme", themes)

# Dynamically update capabilities based on selected theme
if selected_theme != 'All':
    caps = ['All'] + sorted(capability_df[capability_df['Service Theme'] == selected_theme]['Capability'].unique().tolist())
else:
    caps = ['All'] + sorted(capability_df['Capability'].unique().tolist())
    
selected_cap = st.sidebar.selectbox("Capability", caps)

# Filtering logic
filtered_consultancies = set(all_consultancies)

if selected_theme != 'All':
    theme_matches = capability_df[capability_df['Service Theme'] == selected_theme]['Consultancy'].unique()
    filtered_consultancies = filtered_consultancies.intersection(theme_matches)

if selected_cap != 'All':
    cap_matches = capability_df[capability_df['Capability'] == selected_cap]['Consultancy'].unique()
    filtered_consultancies = filtered_consultancies.intersection(cap_matches)

if search_query:
    search_lower = search_query.lower()
    name_matches = [c for c in all_consultancies if search_lower in c.lower()]
    cap_search_matches = capability_df[capability_df['Capability'].str.lower().str.contains(search_lower, na=False)]['Consultancy'].unique()
    combined_search_matches = set(name_matches).union(cap_search_matches)
    filtered_consultancies = filtered_consultancies.intersection(combined_search_matches)

# Display results
st.subheader(f"Results: {len(filtered_consultancies)} partners found")

for consultancy in sorted(filtered_consultancies):
    with st.expander(f"**{consultancy}**"):
        prof = profile_map.get(consultancy, {})
        geo = prof.get('Geography covered', 'Not specified')
        website = prof.get('Website', '')
        
        # Display geography and website
        st.write(f"**Geography covered:** {geo}")
        if pd.notna(website) and str(website).strip() != '':
             st.markdown(f"[Visit website]({website})")
        
        # Display capabilities grouped by theme
        c_data = capability_df[capability_df['Consultancy'] == consultancy]
        if not c_data.empty:
            for theme, group in c_data.groupby('Service Theme'):
                st.write(f"**{theme}**")
                for _, row in group.iterrows():
                    st.write(f"- {row['Capability']}")
        else:
            st.write("No specific capabilities mapped.")