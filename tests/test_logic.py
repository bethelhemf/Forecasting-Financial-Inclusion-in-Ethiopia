import unittest
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.modeller import ImpactModeller

class TestInclusionLogic(unittest.TestCase):
    def setUp(self):
        # Create a tiny mock dataset to test logic
        self.df_main = pd.DataFrame({
            'indicator_code': ['EVT_TELEBIRR'],
            'record_type': ['event'],
            'observation_date': ['2021-05-01']
        })
        self.df_impact = pd.DataFrame({
            'parent_id': ['EVT_0001'],
            'related_indicator': ['ACC_OWNERSHIP'],
            'impact_magnitude': ['high'],
            'impact_direction': ['positive'],
            'lag_months': [0]
        })
        self.modeller = ImpactModeller(self.df_main, self.df_impact)

    def test_magnitude_mapping(self):
        # Test if 'high' is correctly mapped to 5.0
        matrix = self.modeller.build_association_matrix()
        self.assertEqual(matrix.loc['EVT_0001', 'ACC_OWNERSHIP'], 5.0)

if __name__ == '__main__':
    unittest.main()