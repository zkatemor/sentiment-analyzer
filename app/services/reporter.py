import datetime as dt
import json


class Reporter(object):
    def __init__(self, text, result):
        self.text = text
        self.result = result

    def __get_dict(self):
        report = {
            'text': self.text,
            'positive': [],
            'negative': [],
            'modifier': [],
            'score': self.result['score'],
            'sentiment': ""
        }

        for i in self.result['words']['positive']:
            report['positive'].append(i)

        for i in self.result['words']['negative']:
            report['negative'].append(i)

        for i in self.result['words']['modifier']:
            report['modifier'].append(i)

        if self.result['score'] > 0:
            report['sentiment'] = 'Положительная тональность. Чистая положительная оценка: ' + str(self.result['positive'])
        else:
            report['sentiment'] = 'Отрицательная тональность. Чистая отрицательная оценка: ' + str(self.result['negative'])

        return report

    def get_report(self):
        report = self.__get_dict()
        date = str(dt.datetime.now().date()) + str(dt.datetime.now().time()).replace(".", ":").replace(":", "-")
        filename = "app/static/reports/Отчёт-" + date + ".json"

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=4)
        return filename.replace('app/static/', '')
