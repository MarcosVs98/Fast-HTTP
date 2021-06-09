"""*********************************************************************
*                                                                      *
*            Description:  A simple asynchronous http library          *
*                         Date:  12/02/2021                            *
*                 Author: Marcos Vinicios da Silveira                  *
*                                                                      *
************************************************************************
"""

info = {
        "header": [
            "Proxy list (#400) updated at Tue, 08 Jun 21 07:55:01 +0300",
            "Mirrors=https://spys.me/proxy.txt https://t.me/spys_one",
            "Support by donations:",
            "BTC 1H1ZH7WJVzU7GMDSwsAQrqvGrbLY49wdae",
            "ETC 0xd1Cf57E35003aD846524a7778D99e8856B96C241",
            "BCH 19o72EjQw3mEYNciZ4JxvpDmUbjjtXghBb",
            "LTC LMrLZNWGYK3kMHvyioBqZdXYWE3pKj7xZX",
            "IP address:Port CountryCode-Anonymity(Noa/Anm/Hia)-SSL_support(S)-Google_passed(+)"
        ],
        "updated": "2021-06-08 14:47:41.853817",
        "count_proxies": 400,
        "success": 37,
        "failure": 43,
        "no-status-available": 320,
        "success-rate": "44.75%",
        "failure-rate": "55.25%"
    }

from datetime import datetime, timedelta



def update_proxies(info):
	try:
		string_date = info['header'][0].split(',')[-1].partition(',')[0].partition(' +')[0].strip()
		datetime_object = datetime.strptime(string_date, '%d %b %y %H:%M:%S')
		updated = datetime.strptime(info['updated'], "%Y-%m-%d %H:%M:%S.%f")
		if updated < (datetime_object + timedelta(hours=10)):
			return True
	except (KeyError, AttributeError) as e:
		pass
	finally:
		return False

print(update_proxies(info))


