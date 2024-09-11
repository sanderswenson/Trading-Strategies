import csv
from datetime import datetime

class DataLoader:
    @staticmethod
    def load_csv(file_path):
        data = []
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append({
                    'date': datetime.strptime(row['Date'], '%m/%d/%y'),
                    'price': float(row['Value'])
                })
        return data

# Usage example
# loader = DataLoader('historical_data.csv')
# price_data = loader.load_data()