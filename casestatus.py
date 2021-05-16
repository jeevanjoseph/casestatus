import requests
from lxml import html

with requests.Session() as s:
    res = s.get('https://egov.uscis.gov/casestatus/landing.do')
    for index in range(2190329135, 2190329171):
        # cprint('res: {}'.format(res.text))
        data = { 'data':'changeLocale',
                 'appReceiptNum':'MSC'+str(index),
                 'initCaseSearch':'CHECK STATUS'}
        page = s.post('https://egov.uscis.gov/casestatus/mycasestatus.do',data=data)
        tree = html.fromstring(page.content)
        status = tree.xpath('/html/body/div[2]/form/div/div[1]/div/div/div[2]/div[3]/h1/text()')
        print ('MSC'+str(index)+' - '+status[0])
