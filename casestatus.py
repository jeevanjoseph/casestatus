import argparse
import requests
import re
from lxml import html
from requests.sessions import session

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def checkCaseStatus(session, receipt_number):
    data = {'data': 'changeLocale',
            'appReceiptNum': receipt_number,
            'initCaseSearch': 'CHECK STATUS'}
    page = session.post(
        'https://egov.uscis.gov/casestatus/mycasestatus.do', data=data)
    tree = html.fromstring(page.content)
    status = tree.xpath(
        '/html/body/div[2]/form/div/div[1]/div/div/div[2]/div[3]/h1/text()')
    return status[0]


def validateReceiptNum(r_num):
    matchObj = re.match(
        r'(EAC|IOE|LIN|MSC|NBC|NSC|SRC|TSC|VSC|WAC|YSC)([0-9]{2})([0-9]{3})([0-9]{5})', r_num, re.M | re.I)
    return True if matchObj else False


def validateRange(r_start, r_end):
    if validateReceiptNum(r_start) & validateReceiptNum(r_end):
        return True
    else:
        return False


def getReceiptRange(r_start, r_end):
    receipt_range = []
    matchRangeStart = re.match(
        r'(EAC|IOE|LIN|MSC|NBC|NSC|SRC|TSC|VSC|WAC|YSC)([0-9]{2})([0-9]{3})([0-9]{5})', r_start, re.M | re.I)
    matchRangeEnd = re.match(
        r'(EAC|IOE|LIN|MSC|NBC|NSC|SRC|TSC|VSC|WAC|YSC)([0-9]{2})([0-9]{3})([0-9]{5})', r_end, re.M | re.I)

    center = matchRangeStart.group(1)
    center_end = matchRangeStart.group(1)
    rangeStart = int(matchRangeStart.group(
        2)+matchRangeStart.group(3)+matchRangeStart.group(4))
    rangeEnd = int(matchRangeEnd.group(
        2)+matchRangeEnd.group(3)+matchRangeEnd.group(4))
    if((rangeStart <= rangeEnd) & (center == center_end)):
        for num in range(rangeStart, rangeEnd+1):
            receipt_range.append(center+str(num))
    return receipt_range

def processReceipts(receipt_numbers):
    with requests.Session() as s:
        res = s.get('https://egov.uscis.gov/casestatus/landing.do')
        status_dict = {}
        printProgressBar(0, len(receipt_numbers), prefix = 'Progress:', suffix = 'Complete', length = 50)
        for i,receipt in enumerate(sorted(set(receipt_numbers))):
            # cprint('res: {}'.format(res.text))
            if validateReceiptNum(receipt):
                status = checkCaseStatus(
                    session=s, receipt_number=str(receipt))
            else:
                status = 'Skipped'
            status_dict[receipt] = status
            printProgressBar(i + 1, len(receipt_numbers), prefix = 'Progress:', suffix = 'Complete', length = 50)
        return status_dict


# Setup vars
receipt_numbers = []

# Setup args parser
parser = argparse.ArgumentParser(description='Check some USCIS cases.')
parser.add_argument('-n', '--receipt-number', dest='receipt_numbers', metavar='receipt_numbers', nargs='+',
                    help='enter the receipt numbers to check for')

parser.add_argument('-r', '--range', dest='receipt_range', metavar='range', nargs=2,
                    help='enter the receipt number range')
args = parser.parse_args()

if args.receipt_range:
    validateRange(args.receipt_range[0], args.receipt_range[1])
    num_range = getReceiptRange(args.receipt_range[0], args.receipt_range[1])
    receipt_numbers.extend(num_range)

if(args.receipt_numbers):
    receipt_numbers.extend(args.receipt_numbers)

if receipt_numbers:
    caseStatus = processReceipts(receipt_numbers)
    print("{:<15} {:<35} ".format('Receipt Number', 'Status'))
    for receipt_num,status in caseStatus.items():
        print("{:<15} {:<35} ".format(receipt_num, status))
else:
    print('No valid receipt numbers')
