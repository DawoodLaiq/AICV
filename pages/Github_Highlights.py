import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
import requests
import json
from datetime import datetime, timedelta
import pandas as pd
import altair as alt
from streamlit.components.v1 import html

st.set_page_config(page_title='AI CV',layout="wide")

container = st.container()
col1,col2 = container.columns(2)
metric_cols = container.columns(6)
with st.sidebar:
    add_vertical_space(30)
    st.title('SOCIALS:')
    st.markdown('👾 [GITHUB](https://github.com/DawoodLaiq)')
    st.markdown('📰 [LINKEDIN](https://github.com/DawoodLaiq)')

hide_streamlit_style = """
        <style>
        [data-testid="stToolbar"] {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        [data-testid="stSidebarNav"]::before {content: "AI CV";margin-left: 20px;margin-top: 20px;margin-bottom: 20px;font-size: 30px;position: relative;top: 100px;}
        </style>
        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def get_github_data():
        # Your GitHub token
    TOKEN = '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'
    # Headers
    headers = {
        'Authorization': f'bearer {TOKEN}',
        'Content-Type': 'application/json'
    }

    # One year ago
    one_year_ago = datetime.now() - timedelta(days=365)

    # GraphQL query
    query = """
    {
    user(login: "USERNAME") {
        repositories(first: 100, privacy: PUBLIC) {
        totalCount
        nodes {
            name
            stargazers {
            totalCount
            }
            issues(states: [OPEN, CLOSED]) {
            totalCount
            }
            defaultBranchRef {
            target {
                ... on Commit {
                history(first: 100) {
                    totalCount
                }
                }
            }
            }
            pullRequests(states: [OPEN, CLOSED]) {
            totalCount
            }
            languages(first: 100) {
            nodes {
                name
            }
            }
        }
        }
        contributionsCollection(from: "ONE_YEAR_AGO") {
        totalRepositoriesWithContributedCommits
        }
    }
    }
    """

    # GraphQL query
    data_query = """
    {
    user(login: "USERNAME") {
        repositories(first: 100) {
        nodes {
            name
            url
            description
            readme: object(expression: "master:README.md") {
            ... on Blob {
                text
            }
            }
        }
        }
    }
    }
    """

    # Replace "USERNAME" with the GitHub username and "ONE_YEAR_AGO" with the date one year ago
    query = query.replace('USERNAME', 'DawoodLaiq').replace('ONE_YEAR_AGO', one_year_ago.isoformat())
    data_query = data_query.replace('USERNAME', 'DawoodLaiq').replace('ONE_YEAR_AGO', one_year_ago.isoformat())

    # Send the request
    r = requests.post('https://api.github.com/graphql', headers=headers, data=json.dumps({'query': query}))
    response = requests.post('https://api.github.com/graphql', json={'query': data_query}, headers=headers)
    
    # Print the resulting JSON data for inspection
    data_repo =response.json()
    # Get the data
    data = r.json()
    if "data" in data_repo:
        repos = data_repo["data"]["user"]["repositories"]["nodes"]

    # Total number of public repositories
    num_repos = data['data']['user']['repositories']['totalCount']

    # Total number of commits in the default branch of each public repository
    num_commits = sum([repo['defaultBranchRef']['target']['history']['totalCount'] for repo in data['data']['user']['repositories']['nodes'] if repo['defaultBranchRef']])

    # Total number of stars
    num_stars = sum([repo['stargazers']['totalCount'] for repo in data['data']['user']['repositories']['nodes']])

    # Total number of open issues
    num_issues = sum([repo['issues']['totalCount'] for repo in data['data']['user']['repositories']['nodes']])

    # Total number of open pull requests in public repositories
    num_pulls = sum([repo['pullRequests']['totalCount'] for repo in data['data']['user']['repositories']['nodes']])

    # Most used language in public repositories
    languages = [lang['name'] for repo in data['data']['user']['repositories']['nodes'] for lang in repo['languages']['nodes']]
    most_used_language = max(set(languages), key=languages.count)

    # Total number of repositories with contributed commits in the last year
    num_contributions_last_year = data['data']['user']['contributionsCollection']['totalRepositoriesWithContributedCommits']

    # Create a DataFrame for Altair
    data = pd.DataFrame({
        'Category': ['Repos', 'Commits', 'Pull Requests', 'Stars', 'Issues', 'Contributions'],
        'Values': [num_repos, num_commits, num_pulls, num_stars, num_issues, num_contributions_last_year]
    })
    return data,repos,most_used_language


def open_page(url):
    open_script= """
        <script type="text/javascript">
            window.open('%s', '_blank').focus();
        </script>
    """ % (url)
    html(open_script)



gitdata,repos,most_used_language= get_github_data()
# Create the base Altair chart
base = alt.Chart(gitdata, width=700, height=500).encode(
    theta=alt.Theta(field='Values', type='quantitative', stack=True),
    color=alt.Color(field='Category', type='nominal',legend=alt.Legend(orient='bottom',labelFontSize=20))
)

# Create the pie chart and labels
c1 = base.mark_arc(innerRadius=70,outerRadius=150, stroke="#fff")

col1.header("CHART")
# Display the chart in Streamlit
col1.altair_chart(c1, theme=None, use_container_width=True)


projects_container = col2.container()
projects_container.header("PROJECTS")

# Begin constructing the HTML string
html_content = '<div class="scrollable" style="max-height: 500px; overflow-y: auto;">'

for repo in repos:
    # Add the repo name linking to the repo URL as a header
    html_content += f'<h2><a href="{repo["url"]}" target="_blank">{repo["name"]}</a></h2>'
    
    # Add the description if it exists
    if repo["description"]:
        html_content += f"<p>{repo['description']}</p>"
    html_content += '<hr>'  # Add a divider

html_content += '</div>'

# Render the HTML string
projects_container.markdown(html_content, unsafe_allow_html=True)

with col1:
    add_vertical_space(5)

for idx, row in gitdata.iterrows():
    metric_cols[idx].metric(label=row['Category'], value=row['Values'])
container.subheader("Most Used Language")
container.write(most_used_language)