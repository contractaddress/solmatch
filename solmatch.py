import pandas as pd
import glob
import argparse
import time
import sys

flag = argparse.ArgumentParser(
    description="""\
    simple tool to pull transactions between
    two wallets or a list using one of their txn history CSV (from solscan)
    !add the csv file into the same folder!""",

    epilog="Example: python3 main.py -s 2uWxQjSjmYkn5Ab4rgfHfco5SYDKqGEJfpoTfiVJWnBo"
)

flag.add_argument('-s', '--scan', type=str, help='scan one wallet', required=False)
flag.add_argument('-l', '--list', type=str, help='scan all wallets in a list', required=False)

destination = flag.parse_args().scan
listfile = flag.parse_args().list

CSV = glob.glob('*.csv')

if len(CSV) == 0:
        sys.exit("no CSV file found!")
elif len(CSV) > 1:
        sys.exit("too many CSV files in the folder! 1 max")
else:
    CSV = CSV[0]
    print(f'\nscanning {CSV}')


if listfile:
    try:
        with open(listfile, 'r') as list:
            walletlist = [line.strip() for line in list if line.strip()]
    except FileNotFoundError:
        sys.exit(".txt file not found!")
else:
    pass
def scan(wallet):

    rc = pd.read_csv(CSV)

    result_from = rc[rc['From'].str.contains(wallet, na=False)]
    result_to = rc[rc['To'].str.contains(wallet, na=False)]

    pd.set_option('display.max_colwidth', None)

    def print_result(ToF, r_ToF): #ToF == 'to or from' when printing and r_ToF == passing result_to/from variable
        print(f'\n{ToF} -> [{wallet}]')
        for indexrow, row in r_ToF.iterrows():
            signature = row['Signature']
            amount = row['Amount']
            decimal = row['Decimals']
            token = row['TokenAddress']
            convertedAmount = amount / (10 ** decimal)
            print(f'https://solana.fm/tx/{signature} {convertedAmount} {token}')

    print_result('to', result_to)
    print_result('from', result_from)

    print(
        '\n##########################################################################################################################'
        '\n##########################################################################################################################')  # divider between wallets

if destination:
    scan(destination)
elif walletlist:
    index = 0
    while index <= len(walletlist):
        try:
            scan(walletlist[index])
        except IndexError:
            sys.exit("\nall wallets scanned!")
        time.sleep(0.3)
        index += 1

