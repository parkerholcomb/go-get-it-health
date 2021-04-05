from geopy.distance import geodesic
from .Messager import Messager
from .Subscriber import Subscriber
from .Loader import TdemLoader

class Notifier:

    def __init__(self, source = 'tdem', env = 'dev'):
        self.env = env
        print(f"Running notifier. ENV: {self.env}")
        self.source = source
        self.updates_df = TdemLoader().updates_df
        print(f"There are {len(self.updates_df)} locations in TX with positive vaccine delta")
        self.subscribers = Subscriber(self.env).load_subscribers()
        self.messager = Messager(self.env)
    
    @staticmethod
    def _miles_away(lat_lng_a, lat_lng_b):
        try:
            return int(geodesic(lat_lng_a, lat_lng_b).miles)
        except:
            return 9999

    def _get_filtered_location_updates(self, subscriber):
        print(subscriber)
        df = self.updates_df
        df['miles_away'] = df['lat_lng'].apply(self._miles_away, args=(subscriber['lat_lng'],))
        df = df[df['miles_away'] < subscriber['radius']].sort_values(by='miles_away')
        df['miles_away'] = df['miles_away'].astype(int)
        df = df.sort_values(by='miles_away').reset_index(drop = True)
        print(df)
        return df

    def _generate_body(self, df):
        body = []
        for idx in df.index:
            body.append(f"💉 {df.loc[idx]['name']} has {df.loc[idx]['vaccines_delta']} new vaccines available, {df.loc[idx]['miles_away']} miles away")
        zip_ =  df['zip_'][0] # passing the zip of the first record to center the map on that location
        body.append(f"\nVisit vaccinatetexas.org/q?zip={zip_} for more information #goandgetgetit")
        if self.env != 'prod':
            body.append(f"Source: {self.source}")
        return '\n'.join(body)

    def process_push_notifications(self):
        update_count = 0
        for subscriber in self.subscribers:
            updates = self._get_filtered_location_updates(subscriber)
            if len(updates) > 0:
                body = self._generate_body(updates)
                self.messager.send_sms(subscriber['phone'], body)
                update_count += 1
        return update_count

# class TdemNotifier(Notifier):