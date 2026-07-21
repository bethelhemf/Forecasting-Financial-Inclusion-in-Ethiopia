import unittest
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.modeller import ImpactModeller

class TestModeller(unittest.TestCase):
    def test_magnitude_map(self):
        # Dummy data to test logic
        df_main = pd.DataFrame({'indicator_code': ['EVT_0001'], 'record_type': ['event'], 'observation_date': ['2021-01-01']})
        df_impact = pd.DataFrame({'parent_id': ['EVT_0001'], 'related_indicator': ['ACC_OWNERSHIP'], 'impact_magnitude': ['high'], 'impact_direction': ['positive'], 'lag_months': [0]})
        engine = ImpactModeller(df_main, df_impact)
        self.assertEqual(engine.mag_map['high'], 5.0)

if __name__ == '__main__':
    unittest.main()