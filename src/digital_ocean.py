import requests


def get_domain_record(config):
    domain = config['domain']

    response = requests.get(
        config['api_url'] + domain + "/records",
        headers={
            'content-type': "application/json",
            'authorization': config['token']
        }
    ).json()

    record = {}
    for r in response['domain_records']:
        if r['name'] == config['domain_name'] and r['type'] == 'A':
            record = r

    return record


def update_domain_record(config, record, external_ip):
    domain = config['domain']
    record_id = str(record['id'])

    return requests.put(
        config['api_url'] + domain + "/records/" + record_id,
        data="{\n\t\"data\":\"" + external_ip + "\"\n}",
        headers={
            'content-type': "application/json",
            'authorization': config['token']
        }
    )
