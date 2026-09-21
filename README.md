# NHS Internal Consultancy Directory

A lightweight, searchable directory to help NHS digital leads identify and connect with internal NHS consultancy partners for strategy, transformation, analytics, and delivery programmes.

The live application is hosted on Streamlit Community Cloud: [https://nhs-consultancy-directory-7dgsy35lvdf88oikwrx9gq.streamlit.app/]

## How it works

The application is built using [Streamlit](https://streamlit.io/) and Python. It reads capability and profile data directly from the included Excel spreadsheet (`NHS consultancies mapping.xlsx.xlsx`) and generates an interactive, filterable front-end. 

Users can search by:
* Specific capabilities
* Service themes (e.g., Analytics & evaluation, Clinical service redesign)
* Geography covered
* Consultancy name

## Running locally

To run this application on your local machine:

1. Clone the repository.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
