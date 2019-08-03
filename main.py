"""
DDNS Script

Script to update a domain record by "A" type of domains hosted in DigitalOcean

@author Caio Tomich / caiotomich@gmail.com
@version 1.3.3
@since v1.0.0, 2019-07-27;
"""
import requests
import datetime

config = {
    'domain': 'domain.com',
    'domain_name': '',
    'token': 'Bearer TOKEN'
}
log_msg = []


def get_external_ip():
    # using "ipapi.co" to get about external ip informations
    return requests.request(
        "GET",
        "https://ipapi.co/json",
        headers={
            'content-type': 'application/json',
            'User-Agent': 'Mozilla/5.0'
        }
    ).json()


def get_domain_record(config):
    response = requests.request(
        "GET",
        "https://api.digitalocean.com/v2/domains/" + config['domain'] + "/records",
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
    return requests.request(
        "PUT",
        "https://api.digitalocean.com/v2/domains/" + config['domain'] + "/records/" + str(record['id']),
        data="{\n\t\"data\":\"" + external_ip['ip'] + "\"\n}",
        headers={
            'content-type': "application/json",
            'authorization': config['token']
        }
    )


def log(msg):
    with open('./ddns-log.txt', 'a') as out:
        out.write(msg + '\n')

    print(msg)


log("\n---\n\n" + str(datetime.datetime.today()))
log("\nDatagenio - DDNS Script\n")

log("Domain: %s" % config['domain'])
log("Domain Name: %s" % config['domain_name'])

# load external ip
external_ip = get_external_ip()
log("\nExternal IP: %s" % external_ip['ip'])

# load DigitalOcean record information
domain_record = get_domain_record(config)
log("Domain Record IP: %s\n" % domain_record['data'])

# compare external ip and record ip
if domain_record['data'] == external_ip['ip']:
    # if equal, exit program
    log("External IP is the same that domain record IP.")
else:
    # if not equal, update IP record in DigitalOcean
    r = update_domain_record(config, domain_record, external_ip)
    if r.status_code == 200:
        log("Domain record IP updated successfully.")
    else:
        log("Error: %s" % r.text)
