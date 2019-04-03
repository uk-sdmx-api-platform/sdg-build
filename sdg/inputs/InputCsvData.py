import pandas as pd
import sdg
from sdg.inputs import InputFiles
from sdg.Indicator import Indicator

class InputCsvData(InputFiles):
    """Sources of SDG data that are local CSV files."""

    def convert_filename_to_indicator_id(self, filename):
        """Assume the file naming convention: 'indicator_1-1-1'."""
        inid = filename.replace('indicator_', '')
        return inid

    def execute(self):
        """Get the data, edges, and headline from CSV, returning a list of indicators."""
        indicator_map = self.get_indicator_map()
        for inid in indicator_map:
            data = pd.read_csv(indicator_map[inid])
            self.indicators[inid] = Indicator(inid, data=data)
