import datetime as dt
from pathlib import Path


BASE_DIR = Path(__file__).parent.parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'


class PepParsePipeline:
    count_dict = {}
    total_sum = 0

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        self.count_dict[
            item['status']
        ] = self.count_dict.get(item['status'], 0) + 1
        self.total_sum += 1
        return item

    def close_spider(self, spider):
        results_dir = BASE_DIR / 'results'
        results_dir.mkdir(exist_ok=True)
        now = dt.datetime.now()
        now_formatted = now.strftime(DATETIME_FORMAT)
        file_name = f'status_summary_{now_formatted}.csv'
        file_path = results_dir / file_name
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('Статус,Количество\n')
            for status in self.count_dict:
                f.write(f'{status},{self.count_dict[status]}\n')
            f.write(f'Total,{self.total_sum}\n')
