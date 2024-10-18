# main.py

from dash import Dash, html, dcc, Input, Output, callback
import dash_bio as dashbio
import os

# Create the Dash app
app = Dash(__name__)

# Define the server
server = app.server  # This defines the server for Gunicorn

# Layout of the app
app.layout = html.Div([
    'Select which chromosomes to display on the ideogram below:',
    dcc.Dropdown(
        id='my-default-displayed-chromosomes',
        options=[{'label': str(i), 'value': str(i)} for i in range(1, 23)] + [{'label': 'X', 'value': 'X'}, {'label': 'Y', 'value': 'Y'}],
        multi=True,
        value=[str(i) for i in range(1, 23)] + ['X', 'Y']  # Default selection: All chromosomes
    ),
    dashbio.Ideogram(
        id='my-default-dashbio-ideogram',
        chromosomes=[str(i) for i in range(1, 23)] + ['X', 'Y'],  # Display all chromosomes by default
        annotations=[{
            'name': 'FBN1',
            'chr': '15',
            'start': 48400000,
            'stop': 48800000,
            'color': 'red'
        }]
    ),
    dcc.Dropdown(
        id='gene-dropdown',
        options=[{'label': 'FBN1', 'value': 'FBN1'}],
        value='FBN1',  # Default gene selection (can be changed)
        placeholder="Select a gene"
    ),
    html.Div(id='gene-info')
])

# Update gene information based on dropdown selection
@callback(
    Output('gene-info', 'children'),
    Input('gene-dropdown', 'value')
)
def display_gene_info(selected_gene):
    if selected_gene:
        return html.Div([html.H2(selected_gene)])  # Simplified for demo
    return "Select a gene to view pathology information."

# Run the server if the script is executed directly (not when imported)
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=int(os.environ.get('PORT', 8050)), debug=True)
