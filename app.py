import os
from dash import Dash, html, dcc, Input, Output, callback
import dash_bio as dashbio

# List of genes with associated locus and pathology info
genes_info = {
    'FBN1': {
        'chromosome': '15',
        'locus': '15q21',
        'start': 48400000,
        'end': 48800000,
        'color': 'red',
        'pathology': {
            'title': 'Syndrome de Marfan',
            'definition': "Le syndrome de Marfan est une maladie génétique qui affecte le tissu conjonctif.",
            'prevalence': "Rare, environ 1 personne sur 5000.",
            'symptoms_general': "Symptômes cardiovasculaires, oculaires et squelettiques.",
            'symptoms_oral': "Palais ogival, dents encombrées.",
            'medical_management': "Suivi cardiaque, prévention des complications.",
            'dental_management': "Prévention des infections buccales et soins orthodontiques."
        }
    },
    # You can add more genes here in the same format as FBN1
}

# Create the Dash app
app = Dash(__name__)

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
            'name': gene,
            'chr': info['chromosome'],
            'start': info['start'],
            'stop': info['end'],
            'color': info['color']
        } for gene, info in genes_info.items()]
    ),

    dcc.Dropdown(
        id='gene-dropdown',
        options=[{'label': gene, 'value': gene} for gene in genes_info.keys()],
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
        gene = genes_info[selected_gene]
        pathology = gene['pathology']
        return html.Div([
            html.H2(pathology['title']),
            html.P(f"Locus: {gene['locus']}"),
            html.P(f"Definition: {pathology['definition']}"),
            html.P(f"Prevalence: {pathology['prevalence']}"),
            html.P(f"General Symptoms: {pathology['symptoms_general']}"),
            html.P(f"Oral Symptoms: {pathology['symptoms_oral']}"),
            html.P(f"Medical Management: {pathology['medical_management']}"),
            html.P(f"Dental Management: {pathology['dental_management']}")
        ])
    return "Select a gene to view pathology information."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Default to port 10000 if PORT is not set
    app.run_server(host='0.0.0.0', port=port, debug=False)  # Keep host as 0.0.0.0
