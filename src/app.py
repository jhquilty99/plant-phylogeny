import streamlit as st
import pandas as pd
import tree_constructor
import matplotlib.pyplot as plt

ALL_OPTIONS = ['Basil','Cannabis','Croton','Rubber Plant','Potatoes','Begonia']
DEFAULT_OPTIONS = ['Basil','Cannabis']

DATA = pd.DataFrame({
        'Clade 4':['Asterids','Rosids','Rosids','Rosids','Asterids','Rosids'],
        'Order':['Lamiales','Rosales','Malpighiales','Rosales','Solanales','Cucurbitales'],
        'Family':['Lamiaceae','Cannabaceae','Euphorbiaceae','Moraceae','Solanaceae','Begoniaceae'],
        'Subfamily':[None,None,'Crotonoideae',None,None,None],
        'Genus':['Ocimum','Cannabis','Croton','Ficus','Solanum','Begonia'],
        'Species':[None,None,None,'F. elastica','S. tuberosum',None],
        'Common Name':['Basil','Cannabis','Croton','Rubber Plant','Potatoes','Begonia']
    })
DATA['Kingdom'] = 'Plantae'
DATA['Clade 1'] = 'Tracheophytes'
DATA['Clade 2'] = 'Angiosperms'
DATA['Clade 3'] = 'Eudicots'

ORDERING_DATA = ['Kingdom','Clade 1','Clade 2','Clade 3','Clade 4','Order','Family','Subfamily','Genus','Species','Common Name']

COLORING_DATA = {
    'Kingdom':'#ffffcc',
    'Clade 1':'#ffffcc',
    'Clade 2':'#ffffcc',
    'Clade 3':'#d9f0a3',
    'Clade 4':'#addd8e',
    'Order':'#78c679',
    'Family':'#41ab5d',
    'Subfamily':'#238443',
    'Genus':'#005a32',
    'Species':'#005030',
    'Common Name':'#000000'
}

# Rearrange data to be in descending complexity
DATA = DATA[ORDERING_DATA]

options = st.multiselect(
    'Which plants would you like to visualize',
    ALL_OPTIONS,
    DEFAULT_OPTIONS
)
#st.write('You selected:', options)

for i in options:
    st.write('You selected:', i)

new_data = DATA[DATA['Common Name'].isin(options)]
new_data.dropna(how='all', axis=1, inplace=True) 


st.dataframe(new_data)

fig, ax = plt.subplots()

tree_constructor.visualize_genetic_relationships(new_data, ORDERING_DATA, ax, COLORING_DATA)

st.pyplot(fig)

