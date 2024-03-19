import pytest 
import pandas as pd 
import src.tree_constructor as tc
import matplotlib.pyplot as plt

class TestTreeConstructor():
    test_df_a = pd.DataFrame({
        'Clade 1':['B','B','B','C','C','D'],
        'Clade 2':['E','E','F','G','G','I'],
    })
    test_df_a['Kingdom'] = 'A'

    test_df_b = pd.DataFrame({
        'Clade 1':['B','B','B'],
        'Clade 2':['E','E','F']
    })
    test_df_b['Kingdom'] = 'A'

    test_df_c = pd.DataFrame({
        'Clade 1':['B','B'],
        'Clade 2':['E','E']
    })
    test_df_c['Kingdom'] = 'A'

    test_df_d = pd.DataFrame({
        'Clade 1':['J','K','K'],
        'Clade 2':['O','P','P'],
        'Clade 3':['M','N','Q'],
    })
    test_df_d['Kingdom'] = 'A'

    test_df_e = pd.DataFrame({
        'Clade 1':['K','K'],
        'Clade 2':['P','P'],
        'Clade 3':['N','Q'],
    })

    test_df_real = pd.DataFrame({
        'Clade 4':['Asterids','Rosids','Rosids','Rosids','Asterids','Rosids'],
        'Order':['Lamiales','Rosales','Malpighiales','Rosales','Solanales','Cucurbitales'],
        'Family':['Lamiaceae','Cannabaceae','Euphorbiaceae','Moraceae','Solanaceae','Begoniaceae'],
        'Subfamily':[None,None,'Crotonoideae',None,None,None],
        'Genus':['Ocimum','Cannabis','Croton','Ficus','Solanum','Begonia'],
        'Species':[None,None,None,'F. elastica','S. tuberosum',None],
        'Common Name':['Basil','Cannabis','Croton','Rubber Plant','Potatoes','Begonia']
    })
    test_df_real['Kingdom'] = 'Plantae'
    test_df_real['Clade 1'] = 'Tracheophytes'
    test_df_real['Clade 2'] = 'Angiosperms'
    test_df_real['Clade 3'] = 'Eudicots'

    test_df_concat = test_df_real.iloc[1:3]

    ordering_list = ['Kingdom','Clade 1','Clade 2','Clade 3','Clade 4','Order','Family','Subfamily','Genus','Species','Common Name']

    coloring = {
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

    def test_find_common_ancestor(self):
        common_level, common_ancestor, descendants, descendant_level = tc.find_common_ancestor(self.test_df_a, self.ordering_list)
        assert common_level == 'Kingdom'
        assert common_ancestor == 'A'
        assert (descendants == ['B','C','D']).all()
        assert descendant_level == 'Clade 1'

        common_level, common_ancestor, descendants, descendant_level = tc.find_common_ancestor(self.test_df_b, self.ordering_list)
        assert common_level == 'Clade 1'
        assert common_ancestor == 'B'
        assert (descendants == ['E','F']).all()
        assert descendant_level == 'Clade 2'

        common_level, common_ancestor, descendants, descendant_level = tc.find_common_ancestor(self.test_df_c, self.ordering_list)
        assert common_level == None
        assert common_ancestor == None
        assert descendants == None
        assert descendant_level == None

        common_level, common_ancestor, descendants, descendant_level = tc.find_common_ancestor(self.test_df_d, self.ordering_list)
        assert common_level == 'Kingdom'
        assert common_ancestor == 'A'
        assert (descendants == ['J','K']).all()
        assert descendant_level == 'Clade 1'

        common_level, common_ancestor, descendants, descendant_level = tc.find_common_ancestor(self.test_df_e, self.ordering_list)
        assert common_level == 'Clade 1'
        assert common_ancestor == 'K'
        assert (descendants == ['N','Q']).all()
        assert descendant_level == 'Clade 3'

        common_level, common_ancestor, descendants, descendant_level = tc.find_common_ancestor(self.test_df_real, self.ordering_list)
        assert common_level == 'Clade 3'
        assert common_ancestor == 'Eudicots'
        assert (descendants == ['Asterids','Rosids']).all()
        assert descendant_level == 'Clade 4'

        common_level, common_ancestor, descendants, descendant_level = tc.find_common_ancestor(self.test_df_concat, self.ordering_list)
        assert common_level == 'Clade 4'
        assert common_ancestor == 'Rosids'
        assert (descendants == ['Rosales','Malpighiales']).all()
        assert descendant_level == 'Order'

    def test_get_descendant_data(self):
        descendant_data = tc.get_descendant_data(self.test_df_d, 'Clade 1', 'K', self.ordering_list)
        assert (descendant_data.columns == ['Clade 1','Clade 2','Clade 3']).all()
        assert descendant_data.shape[0] == 2

    def test_get_node_colors(self): 
        nodes = ['A','B','C','D','E','F']
        node_colors = tc.get_node_colors(nodes, self.test_df_a, self.coloring)
        assert node_colors == ['#ffffcc','#ffffcc','#ffffcc','#ffffcc','#ffffcc','#ffffcc']

        nodes = ['Asterids','Lamiales','Lamiaceae','Ocimum']
        node_colors = tc.get_node_colors(nodes, self.test_df_real, self.coloring)
        assert node_colors == ['#addd8e','#78c679','#41ab5d','#005a32']


        nodes = ['Plantae','Eudicots','Lamiales','Lamiaceae','Ocimum']
        node_colors = tc.get_node_colors(nodes, self.test_df_real, self.coloring)
        assert node_colors == ['#ffffcc','#d9f0a3','#78c679','#41ab5d','#005a32']
        
    def test_visualize_genetic_relationships(self):
        fig, ax = plt.subplots()
        tc.visualize_genetic_relationships(self.test_df_a, self.ordering_list, ax, self.coloring)

        fig, ax = plt.subplots()
        tc.visualize_genetic_relationships(self.test_df_b, self.ordering_list, ax, self.coloring)

        fig, ax = plt.subplots()
        tc.visualize_genetic_relationships(self.test_df_c, self.ordering_list, ax, self.coloring)

        fig, ax = plt.subplots()
        tc.visualize_genetic_relationships(self.test_df_d, self.ordering_list, ax, self.coloring)

        fig, ax = plt.subplots()
        tc.visualize_genetic_relationships(self.test_df_e, self.ordering_list, ax, self.coloring)

        fig, ax = plt.subplots()
        tc.visualize_genetic_relationships(self.test_df_real, self.ordering_list, ax, self.coloring)

        fig, ax = plt.subplots()
        tc.visualize_genetic_relationships(self.test_df_concat, self.ordering_list, ax, self.coloring)