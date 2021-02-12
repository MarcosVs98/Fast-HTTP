import random
from settings import LUMINATI

def generate_proxy_address():
    session  = ''.join(random.choices([str(i) for i in range(10)], k=15))
    country  = random.choice(LUMINATI['coutries'])
    passwd   = LUMINATI['passwd']
    hostname = LUMINATI['hostname']
    port     = LUMINATI['port']
    baseuser = LUMINATI['baseuser']
    zone     = LUMINATI['zone']
    return f"{baseuser}-zone-{zone}-session-{session}-country-{country}:{passwd}@{hostname}:{port}"

#end-of-file