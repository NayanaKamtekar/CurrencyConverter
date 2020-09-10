import requests

BASE_URL = 'https://api.exchangeratesapi.io'
LATEST_ENDPOINT = 'latest'
HISTORY_ENDPOINT = 'history'


class BadResponseError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'Bad response: {self.message}'


class Converter():
    def get_url(self, payload):
        if 'start_at' in payload:
            return '/'.join([BASE_URL, HISTORY_ENDPOINT])
        elif 'date' in payload and payload['date'] is not None:
            return '/'.join([BASE_URL, payload['date']])
        else:
            return '/'.join([BASE_URL, LATEST_ENDPOINT])

    def request_rates(self, **kwargs):
        url = self.get_url(kwargs)

        try:
            response = requests.get(url, params=kwargs)
            responsedict = response.json()

            if response.status_code != requests.codes.ok or 'error' in responsedict:
                raise BadResponseError(responsedict['error'])
        except BadResponseError as e:
            print(e)
        except ValueError as e:
            print(e)
        except:
            print(f'Connection not established {url}')
        else:
            return (responsedict)

    def covert(self, to, from_='EUR', amount=1, date=None):
        response = self.request_rates(base=from_, symbols=to, date=date)

        if response:
            print(f"As of {response['date']}, {response['base']} {amount} equals")
            for key, value in response['rates'].items():
                print(f'{key} {amount * value:,f}')

    def change(self, to, basedate, compdate, from_='EUR'):
        base_response = self.request_rates(base=from_, symbols=to, date=basedate)
        comp_response = self.request_rates(base=from_, symbols=to, date=compdate)

        if base_response:
            base_rate = base_response['rates'][to]

        if comp_response:
            comp_rate = comp_response['rates'][to]

        return ((comp_rate/base_rate)**(1/10)-1)*100

c = Converter()
c.covert(['INR', 'CAD'], from_='EUR', amount=1, date='2020-09-01')