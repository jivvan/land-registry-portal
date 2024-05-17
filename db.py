import json
import math


class Database:
    filename = "tempdb"
    transaction_filename = "temptransdb"

    def __init__(self, limit=10) -> None:
        self.limit = limit
        try:
            self.cnt = self.get_records(None)[-1].get('id')
        except:
            self.cnt = 0
        try:
            self.transaction_cnt = self.get_transactions(
                None, None)[-1].get('id')
        except:
            self.transaction_cnt = 0

    def insert_land_record(self, data):
        data = dict(data)
        data['id'] = self.cnt + 1
        self.cnt += 1
        with open(self.filename, 'a') as file:
            json.dump(data, file)
            file.write('\n')

    def insert_transaction(self, data):
        data['id'] = self.transaction_cnt + 1
        self.transaction_cnt += 1
        self.transaction_cnt += 1
        with open(self.transaction_filename, 'a') as file:
            json.dump(data, file)
            file.write('\n')

    def get_records(self, page):
        with open(self.filename, 'r') as file:
            data = [json.loads(line.strip()) for line in file]
            if not page:
                return data
        res = {
            'data': data[(page-1)*self.limit:page*self.limit],
            "total_pages": math.ceil(len(data)/self.limit),
            'current_page': page
        }
        return res

    def get_transactions(self, plot_id, page):
        with open(self.transaction_filename, 'r') as file:
            data = [json.loads(line.strip()) for line in file]
            data.reverse()
            if plot_id:
                data = [d for d in data if d['plot_id'] == plot_id]
            if not page:
                return data
        res = {
            'data': data[(page-1)*self.limit:page*self.limit],
            'total_records': len(data),
            'record_limit': self.limit,
            'current_page': page
        }
        return res

    def get_record(self, id):
        with open(self.filename, 'r') as file:
            for line in file:
                data = json.loads(line.strip())
                if data.get('id') == id:
                    return data
        return None

    def get_geojson(self):
        whole = []
        records = self.get_records(None)
        for record in records:
            new = json.loads(record['polygonData'])['features'][0]
            record.pop("polygonData")
            new['properties'] = record
            whole.append(new)
        return {
            "type": "FeatureCollection",
            "features": whole
        }

    def update_owner(self, id, owner_name, owner_id):
        with open(self.filename, 'r') as file:
            lines = file.readlines()

        updated = False
        with open(self.filename, 'w') as file:
            for line in lines:
                record = json.loads(line)
                if record['id'] == id:
                    record['landOwner'] = owner_name
                    record['ownerId'] = owner_id
                    updated = True
                json.dump(record, file)
                file.write('\n')

        if updated:
            return True
        else:
            return False

    def transact_land(self, details):
        land_id = int(details.get('landId'))
        land_details = self.get_record(land_id)
        self.update_owner(land_id, details.get(
            'buyerName'), details.get('buyerId'))
        transaction = {
            'id': self.transaction_cnt+1,
            'plot_id': land_details.get('id'),
            'sellerName': land_details.get('landOwner'),
            'sellerId': land_details.get('ownerId'),
            'buyerName': details.get('buyerName'),
            'buyerId': details.get('buyerId'),
            'transactionDate': details.get('transactionDate'),
            'transactionAmount': details.get('transactionAmount'),
            'additionalDetails': details.get('additionalDetails')
        }
        self.insert_transaction(transaction)
