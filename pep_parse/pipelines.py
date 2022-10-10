import csv
import datetime as dt
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'


class PepParsePipeline:
    count_status = {}
    total_sum = 0

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        self.count_status[
            item['status']
        ] = self.count_status.get(item['status'], 0) + 1
        self.total_sum += 1
        return item

    def close_spider(self, spider):
        results_dir = BASE_DIR / 'results'
        results_dir.mkdir(exist_ok=True)
        now = dt.datetime.now()
        now_formatted = now.strftime(DATETIME_FORMAT)
        file_name = f'status_summary_{now_formatted}.csv'
        file_path = results_dir / file_name
        with open(file_path, 'w', newline='\n', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Статус', 'Количество'])
            writer.writerows(list(self.count_status.items()))
            writer.writerow(['Total', self.total_sum])
