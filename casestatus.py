import argparse
import requests
import re
from lxml import html
from requests.sessions import session


# range(2190329135, 2190329171)
def checkCaseStatus(session, receipt_number):
    data = { 'data':'changeLocale',
                 'appReceiptNum':receipt_number,
                 'initCaseSearch':'CHECK STATUS'}
    page = session.post('https://egov.uscis.gov/casestatus/mycasestatus.do',data=data)
    tree = html.fromstring(page.content)
    status = tree.xpath('/html/body/div[2]/form/div/div[1]/div/div/div[2]/div[3]/h1/text()')
    return status[0]

def validateReceiptNum(r_num):
    matchObj = re.match( r'(EAC|IOE|LIN|MSC|NBC|NSC|SRC|TSC|VSC|WAC|YSC)([0-9]{2})([0-9]{3})([0-9]{5})', r_num, re.M|re.I)
    return True if matchObj else False

def validateRange(r_start, r_end):
    if validateReceiptNum(r_start) & validateReceiptNum(r_end):
        return True
    else:
        return False

def getReceiptRange(r_start, r_end):
    receipt_range = []
    matchRangeStart = re.match( r'(EAC|IOE|LIN|MSC|NBC|NSC|SRC|TSC|VSC|WAC|YSC)([0-9]{2})([0-9]{3})([0-9]{5})', r_start, re.M|re.I)
    matchRangeEnd   = re.match( r'(EAC|IOE|LIN|MSC|NBC|NSC|SRC|TSC|VSC|WAC|YSC)([0-9]{2})([0-9]{3})([0-9]{5})', r_end, re.M|re.I)

    center     = matchRangeStart.group(1)
    center_end = matchRangeStart.group(1)
    rangeStart = int(matchRangeStart.group(2)+matchRangeStart.group(3)+matchRangeStart.group(4))
    rangeEnd   = int(matchRangeEnd.group(2)+matchRangeEnd.group(3)+matchRangeEnd.group(4))
    if((rangeStart<=rangeEnd) & (center==center_end)) :
        for num in range(rangeStart, rangeEnd+1):
            receipt_range.append(center+str(num))
    return receipt_range

## Setup vars
receipt_numbers = []

# Setup args parser
parser = argparse.ArgumentParser(description='Check some USCIS cases.')


parser.add_argument('-n','--receipt-number', dest='receipt_numbers', metavar='receipt_numbers', nargs='+',
                    help='enter the receipt numbers to check for')

parser.add_argument('-r','--range', dest='receipt_range', metavar='range', nargs=2,
                    help='enter the receipt number range')

args = parser.parse_args()
print(args.receipt_range)

if args.receipt_range:
    validateRange(args.receipt_range[0], args.receipt_range[1])
    num_range = getReceiptRange(args.receipt_range[0], args.receipt_range[1])
    receipt_numbers.extend(num_range)

if(args.receipt_numbers):
    receipt_numbers.extend(args.receipt_numbers)

if receipt_numbers:
    with requests.Session() as s:
        res = s.get('https://egov.uscis.gov/casestatus/landing.do')
        for receipt in receipt_numbers:
            # cprint('res: {}'.format(res.text))
            if validateReceiptNum(receipt):
                status = checkCaseStatus(session=s, receipt_number=str(receipt))
            else :
                status = 'Skipped'
            print (receipt+' - '+status)


