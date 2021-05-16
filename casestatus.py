import argparse
import requests
from lxml import html
from requests.sessions import session

receipt_numbers = []
parser = argparse.ArgumentParser(description='Check some USCIS cases.')
parser.add_argument('-n','--receipt-number', dest='receipt_numbers', metavar='receipt_numbers', nargs='+',
                    help='enter the receipt numbers to check for')
args = parser.parse_args()
print(args.receipt_numbers)
receipt_numbers.extend(args.receipt_numbers)

# range(2190329135, 2190329171)
def checkCaseStatus(session, center, receipt_number):
    data = { 'data':'changeLocale',
                 'appReceiptNum':'MSC'+receipt_number,
                 'initCaseSearch':'CHECK STATUS'}
    page = s.post('https://egov.uscis.gov/casestatus/mycasestatus.do',data=data)
    tree = html.fromstring(page.content)
    status = tree.xpath('/html/body/div[2]/form/div/div[1]/div/div/div[2]/div[3]/h1/text()')
    return status[0]
    
with requests.Session() as s:
    res = s.get('https://egov.uscis.gov/casestatus/landing.do')
    for index in receipt_numbers:
        # cprint('res: {}'.format(res.text))
        status = checkCaseStatus(session=s, center='MSC', receipt_number=str(index))
        print ('MSC'+str(index)+' - '+status)


