import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='GDP Dashboard',
    page_icon='data:image/png;base64,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', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_gdp_data():
    """Grab GDP data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/gdp_data.csv'
    raw_gdp_df = pd.read_csv(DATA_FILENAME)

    MIN_YEAR = 1960
    MAX_YEAR = 2022

    # The data above has columns like:
    # - Country Name
    # - Country Code
    # - [Stuff I don't care about]
    # - GDP for 1960
    # - GDP for 1961
    # - GDP for 1962
    # - ...
    # - GDP for 2022
    #
    # ...but I want this instead:
    # - Country Name
    # - Country Code
    # - Year
    # - GDP
    #
    # So let's pivot all those year-columns into two: Year and GDP
    gdp_df = raw_gdp_df.melt(
        ['Country Code'],
        [str(x) for x in range(MIN_YEAR, MAX_YEAR + 1)],
        'Year',
        'GDP',
    )

    # Convert years from string to integers
    gdp_df['Year'] = pd.to_numeric(gdp_df['Year'])

    return gdp_df

gdp_df = get_gdp_data()

# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :earth_americas: GDP dashboard

Browse GDP data from the [World Bank Open Data](https://data.worldbank.org/) website. As you'll
notice, the data only goes to 2022 right now, and datapoints for certain years are often missing.
But it's otherwise a great (and did I mention _free_?) source of data.
'''

# Add some spacing
''
''

min_value = gdp_df['Year'].min()
max_value = gdp_df['Year'].max()

from_year, to_year = st.slider(
    'Which years are you interested in?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value])

countries = gdp_df['Country Code'].unique()

if not len(countries):
    st.warning("Select at least one country")

selected_countries = st.multiselect(
    'Which countries would you like to view?',
    countries,
    ['DEU', 'FRA', 'GBR', 'BRA', 'MEX', 'JPN'])

''
''
''

# Filter the data
filtered_gdp_df = gdp_df[
    (gdp_df['Country Code'].isin(selected_countries))
    & (gdp_df['Year'] <= to_year)
    & (from_year <= gdp_df['Year'])
]

st.header('GDP over time', divider='gray')

''

st.line_chart(
    filtered_gdp_df,
    x='Year',
    y='GDP',
    color='Country Code',
)

''
''


first_year = gdp_df[gdp_df['Year'] == from_year]
last_year = gdp_df[gdp_df['Year'] == to_year]

st.header(f'GDP in {to_year}', divider='gray')

''

cols = st.columns(4)

for i, country in enumerate(selected_countries):
    col = cols[i % len(cols)]

    with col:
        first_gdp = first_year[gdp_df['Country Code'] == country]['GDP'].iat[0] / 1000000000
        last_gdp = last_year[gdp_df['Country Code'] == country]['GDP'].iat[0] / 1000000000

        if math.isnan(first_gdp):
            growth = 'n/a'
            delta_color = 'off'
        else:
            growth = f'{last_gdp / first_gdp:,.2f}x'
            delta_color = 'normal'

        st.metric(
            label=f'{country} GDP',
            value=f'{last_gdp:,.0f}B',
            delta=growth,
            delta_color=delta_color
        )
