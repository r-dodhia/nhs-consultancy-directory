import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="Internal NHS consultancies", layout="wide")

# Theme icon mapping matching your directory categories
THEME_ICONS = {
    "Strategy & Advisory": "🧭",
    "Transformation & Change": "🔄",
    "Digital and automation": "⚙️",
    "Analytics and evaluation": "📊",
    "Clinical Service Redesign": "🩺",
    "Engagement/ consultation": "💬",
    "Engagement and consultation": "💬",
    "Finance & Corporate": "🏛️",
    "Interims including senior roles": "💼",
    "Interims and senior roles": "💼",
    "OD and leadership development": "👥",
    "PMO and delivery support": "📋",
    "Quality Improvement": "✅",
}

@st.cache_data
def load_data():
    profile_df = pd.read_excel('NHS consultancies mapping.xlsx.xlsx', sheet_name='Profile')
    capability_df = pd.read_excel('NHS consultancies mapping.xlsx.xlsx', sheet_name='Capability')
    
    # Ensure text columns are clean strings
    capability_df['Service Theme'] = capability_df['Service Theme'].astype(str).str.strip()
    capability_df['Capability'] = capability_df['Capability'].astype(str).str.strip()
    
    all_consultancies = sorted(profile_df['Consultancy'].dropna().unique().tolist())
    profile_map = profile_df.set_index('Consultancy').to_dict('index')
    
    return capability_df, all_consultancies, profile_map

capability_df, all_consultancies, profile_map = load_data()

# Header
st.title("Find an internal NHS consultancy")
st.write("Search and filter to find partners for your digital strategy.")

# Sidebar filters
st.sidebar.header("Filter directory")
search_query = st.sidebar.text_input("Search by consultancy or capability")

themes = ['All'] + sorted(capability_df['Service Theme'].unique().tolist())
selected_theme = st.sidebar.selectbox("Service theme", themes)

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

# Results
st.subheader(f"Results: {len(filtered_consultancies)} partners found")

for consultancy in sorted(filtered_consultancies):
    with st.expander(f"**{consultancy}**"):
        prof = profile_map.get(consultancy, {})
        geo = prof.get('Geography covered', 'Not specified')
        website = prof.get('Website', '')
        
        st.write(f"**Geography covered:** {geo}")
        
        # Contrasting primary action button
        if pd.notna(website) and str(website).strip() != '':
            st.link_button(
                f"Visit {consultancy} website",
                url=str(website).strip(),
                type="primary"
            )
        
        st.write("")
        
        # Two-column layout for themes and capabilities
        c_data = capability_df[capability_df['Consultancy'] == consultancy]
        if not c_data.empty:
            themes_in_consultancy = list(c_data.groupby('Service Theme'))
            col1, col2 = st.columns(2)
            
            for idx, (theme, group) in enumerate(themes_in_consultancy):
                target_col = col1 if idx % 2 == 0 else col2
                icon = THEME_ICONS.get(theme, "🔹")
                
                with target_col:
                    st.markdown(f"### {icon} {theme}")
                    for _, row in group.iterrows():
                        st.markdown(f"- {row['Capability']}")
                    st.write("")
        else:
            st.write("No specific capabilities mapped.")
