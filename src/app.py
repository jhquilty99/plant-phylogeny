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

options = st.multiselect(
    'Which plants would you like to visualize',
    ALL_OPTIONS,
    DEFAULT_OPTIONS
)
#st.write('You selected:', options)

for i in options:
    st.write('You selected:', i)

new_data = DATA[DATA['Common Name'].isin(options)]


st.dataframe(new_data)

fig, ax = plt.subplots()

tree_constructor.visualize_genetic_relationships(new_data, ORDERING_DATA, ax)

st.pyplot(fig)

