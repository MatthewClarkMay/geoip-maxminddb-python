#!/usr/bin/python3

"""
AUTHOR: Matthew May - mcmay.web@gmail.com
"""

# Imports
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from collections import OrderedDict
from sys import argv, exit
from textwrap import dedent
import json
import maxminddb


# builds full dict for json dump
def build_full_dict(db_contents):
    selected = {}
    selected['city'] = db_contents['city']['names']['en']
    selected['continent'] = db_contents['continent']['names']['en']
    selected['continent_code'] = db_contents['continent']['code']
    selected['country'] = db_contents['country']['names']['en']
    selected['country_code'] = db_contents['country']['iso_code']
    selected['latitude/longitude'] = [db_contents['location']['latitude'],
                                    db_contents['location']['longitude']]
    selected['latitude'] = db_contents['location']['latitude']
    selected['longitude'] = db_contents['location']['longitude']
    selected['metro_code'] = db_contents['location']['metro_code']
    selected['postal_code'] = db_contents['postal']['code']
    return selected


# parse command line arguments and build dictionary of results
def build_selected_dict(args, db_contents):
    selected = {}
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
        selected['city'] = db_contents['city']['names']['en']
    if args.continent:
        selected['continent'] = db_contents['continent']['names']['en']
    if args.continent_code:
        selected['continent_code'] = db_contents['continent']['code']
    if args.country:
        selected['country'] = db_contents['country']['names']['en']
    if args.country_code:
        selected['country_code'] = db_contents['country']['iso_code']
    if args.lat_lon:
        selected['latitude/longitude'] = [db_contents['location']['latitude'],
                                        db_contents['location']['longitude']]
    if args.latitude:
        selected['latitude'] = db_contents['location']['latitude']
    if args.longitude:
        selected['longitude'] = db_contents['location']['longitude']
    if args.metro_code:
        selected['metro_code'] = db_contents['location']['metro_code']
    if args.postal_code:
        selected['postal_code'] = db_contents['postal']['code']
    # if args.readme:
    #     readme()
    if args.time_zone:
        selected['time_zone'] = db_contents['location']['time_zone']
    if len(argv) <= 3:
        selected['latitude/longitude'] = [db_contents['location']['latitude'],
                                        db_contents['location']['longitude']]
    return selected


# format and print selected output
def format_and_print_selected(selected_dict):
    ordered_dict = OrderedDict(sorted(selected_dict.items()))
    for key in ordered_dict:
        print('{}: {}'.format(key, selected_dict[key]))


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

    # define command line arguments
    parser.add_argument('dbpath', metavar='db', type=str, help='Absolute path of MaxMind DB (required)')
    parser.add_argument('address', metavar='ip', type=str, help='IPv4 address you wish to locate (required)')
    parser.add_argument('-a', action='store_true', dest='all_fields', help='all')
    parser.add_argument('-ci', action='store_true', dest='city', help='city')
    parser.add_argument('-cont', action='store_true', dest='continent', help='continent name')
    parser.add_argument('-contc', action='store_true', dest='continent_code', help='continent code')
    parser.add_argument('-countc', action='store_true', dest='country_code', help='country code')
    parser.add_argument('-count', action='store_true', dest='country', help='country')
    parser.add_argument('-la', action='store_true', dest='latitude', help='latitude')
    parser.add_argument('-lalo', action='store_true', dest='lat_lon', help='[latitude, longitude]')
    parser.add_argument('-lo', action='store_true', dest='longitude', help='longitude')
    parser.add_argument('-m', action='store_true', dest='metro_code', help='metro code')
    parser.add_argument('-p', action='store_true', dest='postal_code', help='postal code')
    # parser.add_argument('-r', action='store_true', dest='readme', help='View README')
    parser.add_argument('-tz', action='store_true', dest='time_zone', help='time zone')

    # parse arguments/options
    args = parser.parse_args()
    return args


def parse_maxminddb(db_path, ip):
    try:
        reader = maxminddb.open_database(db_path)
        response = reader.get(ip)
        reader.close()
        return response
    except FileNotFoundError:
        print('DB not found')
        print('SHUTTING DOWN')
        exit()
    except ValueError:
        return False


def readme(): # print readme contents
    pass


def json_dump(db_path, ip):
    db_contents = parse_maxminddb(db_path, ip)
    if not db_contents:
        return False
    full_dict = build_full_dict(db_contents)
    json_data = json.dumps(full_dict)
    return json_data


def main():

    args = menu()
    db_path = args.dbpath
    ip = args.address

    db_contents = parse_maxminddb(db_path, ip)

    if not db_contents:
        print('Invalid IP address')
        print('SHUTTING DOWN')
        exit()

    selected_db_contents = build_selected_dict(args, db_contents)

    print('\nDB: ' + db_path)
    print('IP: ' + ip + '\n')

    format_and_print_selected(selected_db_contents)


if __name__ == '__main__':
    main()

