#!/usr/bin/python3

"""
AUTHOR: Matthew May - mcmay.web@gmail.com
"""

# Imports
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from collections import OrderedDict
from sys import argv, exit
from textwrap import dedent
import maxminddb


def build_results_dict(args, db_contents):
    results = {}
    if args.all_fields:
        args.city = True
        args.continent = True
        args.continent_code = True
        args.country = True
        args.country_code = True
        args.lat_lon = True
        args.metro_code = True
        args.postal_code = True
        args.time_zone = True
    if args.city:
        results['city'] = db_contents['city']['names']['en']
    if args.continent:
        results['continent'] = db_contents['continent']['names']['en']
    if args.continent_code:
        results['continent_code'] = db_contents['continent']['code']
    if args.country:
        results['country'] = db_contents['country']['names']['en']
    if args.country_code:
        results['country_code'] = db_contents['country']['iso_code']
    if args.lat_lon:
        results['latitude/longitude'] = [db_contents['location']['latitude'],
                                        db_contents['location']['longitude']]
    if args.latitude:
        results['latitude'] = db_contents['location']['latitude']
    if args.longitude:
        results['longitude'] = db_contents['location']['longitude']
    if args.metro_code:
        results['metro_code'] = db_contents['location']['metro_code']
    if args.postal_code:
        results['postal_code'] = db_contents['postal']['code']
    # if args.readme:
    #     readme()
    if args.time_zone:
        results['time_zone'] = db_contents['location']['time_zone']
    if len(argv) <= 3:
        results['latitude/longitude'] = [db_contents['location']['latitude'],
                                        db_contents['location']['longitude']]
    return results


def format_and_print_results(results):
    ordered_results = OrderedDict(sorted(results.items()))
    for key in ordered_results:
        print('{}: {}'.format(key, results[key]))


def menu():
    # instantiate parser
    parser = ArgumentParser(
            prog='geoip.py',
            usage='%(prog)s [DB] [IP] [OPTIONS]',
            formatter_class=RawDescriptionHelpFormatter,
            description=dedent('''\
                    --------------------------------------------------------------
                    GeoIP Locator: Returns city, continent, continent code,
                    country, country code, latitude/longitude, metro code,
                    postal code, or time zone, depending on the option(s) passed.
                    --------------------------------------------------------------

                    Default output with no optional arguments passed: [latitude, longitude]'''))

    # DB argument
    parser.add_argument('dbpath', metavar='db', type=str, help='Absolute path of MaxMind DB (required)')
    # IP argument
    parser.add_argument('address', metavar='ip', type=str, help='IPv4 address you wish to locate (required)')
    # all option
    parser.add_argument('-a', action='store_true', dest='all_fields', help='all')
    # city option
    parser.add_argument('-ci', action='store_true', dest='city', help='city')
    # continent name option
    parser.add_argument('-cont', action='store_true', dest='continent', help='continent name')
    # continent code option
    parser.add_argument('-contc', action='store_true', dest='continent_code', help='continent code')
    # country code option
    parser.add_argument('-countc', action='store_true', dest='country_code', help='country code')
    # country option
    parser.add_argument('-count', action='store_true', dest='country', help='country')
    # latitude option
    parser.add_argument('-la', action='store_true', dest='latitude', help='latitude')
    # latitude/longitude option
    parser.add_argument('-lalo', action='store_true', dest='lat_lon', help='[latitude, longitude]')
    # longitude option
    parser.add_argument('-lo', action='store_true', dest='longitude', help='longitude')
    # metro_code option
    parser.add_argument('-m', action='store_true', dest='metro_code', help='metro code')
    # postal code option
    parser.add_argument('-p', action='store_true', dest='postal_code', help='postal code')
    # README option
    # parser.add_argument('-r', action='store_true', dest='readme', help='View README')
    # time zone option
    parser.add_argument('-tz', action='store_true', dest='time_zone', help='time zone')

    # parse arguments/options
    args = parser.parse_args()
    return args


def parse_maxminddb(db, ip):
    try:
        reader = maxminddb.open_database(db)
        response = reader.get(ip)
        reader.close()
        return response
    except FileNotFoundError:
        print('DB not found')
        print('SHUTTING DOWN')
        exit()
    except ValueError:
        print('Invalid IP address')
        print('SHUTTING DOWN')
        exit()


def readme(): # print readme contents
    pass


def main():

    args = menu()
    db_path = args.dbpath
    ip = args.address

    db_contents = parse_maxminddb(db_path, ip)
    selected_db_contents = build_results_dict(args, db_contents)

    print('\nDB: ' + db_path)
    print('IP: ' + ip + '\n')

    format_and_print_results(selected_db_contents)


if __name__ == '__main__':
    main()

