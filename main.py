"""
DDNS Script

Script to update a domain record by "A" type of domains hosted in DigitalOcean

@author Caio Tomich / caiotomich@gmail.com
@version 1.4.3
@since v1.0.0, 2019-07-27;
"""

from src.ip_api import get_external_ip
from src.digital_ocean import get_domain_record, update_domain_record
import datetime

token = ''
config = {
    'domain': '',
    'domain_name': '',
    'token': 'Bearer ' + token,
    'api_url': 'https://api.digitalocean.com/v2/domains/'
}
log_msg: list = []


def log(msg):
    with open('./ddns-execution.log', 'a') as out:
        out.write(msg + '\n')

    print(msg)


log("\n---\n\n" + str(datetime.datetime.today()))
log("\nDatagenio - DDNS Script\n")

log("Domain: %s" % config['domain'])
log("Domain Name: %s" % config['domain_name'])

# load external ip
external_ip = get_external_ip()
log("\nExternal IP: %s" % external_ip)

# load DigitalOcean record information
domain_record = get_domain_record(config)
log("Domain Record IP: %s\n" % domain_record['data'])

# compare external ip and record ip
if domain_record['data'] == external_ip:
    # if equal, exit program
    log("External IP is the same that domain record IP.")
else:
    # if not equal, update IP record in DigitalOcean
    r = update_domain_record(config, domain_record, external_ip)
    if r.status_code == 200:
        log("Domain record IP updated successfully.")
    else:
        log("Error: %s" % r.text)
