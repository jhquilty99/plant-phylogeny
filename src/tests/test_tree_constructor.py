import pytest 
import pandas as pd 
import src.tree_constructor as tc

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

    ordering_list = ['Kingdom','Clade 1','Clade 2','Clade 3','Clade 4','Order','Family','Subfamily','Genus','Species','Common Name']


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

        common_level, common_ancestor, descendants, descendant_level = tc.find_common_ancestor(self.test_df_real, self.ordering_list)
        assert common_level == 'Clade 3'
        assert common_ancestor == 'Eudicots'
        assert (descendants == ['Asterids','Rosids']).all()
        assert descendant_level == 'Clade 4'
