#!/usr/bin/python3

"""
AUTHOR: Matthew May - mcmay.web@gmail.com
"""

# Imports
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from collections import OrderedDict
from sys import argv, exit
from textwrap import dedent
import geoip2.database


def build_results_dict(args, db, ip):
    results = {}
    if args.city:
        city = read_and_respond(db, ip, str('response.city.name'))
        results['city'] = city
    if args.country:
        country = read_and_respond(db, ip, str('response.country.name'))
        results['country'] = country
    if args.country_code:
        country_code = read_and_respond(db, ip, str('response.country.iso_code'))
        results['country_code'] = country_code
    # if args.domain: # REQUIRES PAID DB
    #     domain = read_and_respond(db, ip, response.?.?)
    #     results['domain'] = domain
    # if args.isp: # REQUIRES PAID DB
    #     isp = read_and_respond(db, ip, response.?.?)
    #     results['isp'] = isp
    if args.lat_lon:
        lat = read_and_respond(db, ip, str('response.location.latitude'))
        lon = read_and_respond(db, ip, str('response.location.longitude'))
        results['lat_lon'] = [lat, lon]
    if args.latitude:
        latitude = read_and_respond(db, ip, str('response.location.latitude'))
        results['latitude'] = latitude
    if args.longitude:
        longitude = read_and_respond(db, ip, str('response.location.longitude'))
        results['longitude'] = longitude
    if args.postal_code:
        postal_code = read_and_respond(db, ip, str('response.postal.code'))
        results['postal'] = postal_code
    # if args.readme:
    #     readme()
    if len(argv) <= 3:
        lat = read_and_respond(db, ip, str('response.location.latitude'))
        lon = read_and_respond(db, ip, str('response.location.longitude'))
        results['lat_lon'] = [lat, lon]
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
                    GeoIP Locator: Returns city, country, country code, postal code, or latitude/longitude, depending on the option(s) passed.

                    Default output with no optional arguments passed: [latitude, longitude]'''))

    # DB argument
    parser.add_argument('dbpath', metavar='db', type=str, help='Absolute path of MaxMind DB')
    # IP argument
    parser.add_argument('address', metavar='ip', type=str, help='IPv4 address you wish to locate (required)')
    # country code option
    parser.add_argument('-cc', action='store_true', dest='country_code', help='Return IP country code. REQUIRES MAXMIND COUNTRY DB')
    # city option
    parser.add_argument('-ci', action='store_true', dest='city', help='Return IP city. REQUIRES MAXMIND CITY DB')
    # country option
    parser.add_argument('-co', action='store_true', dest='country', help='Return IP country. REQUIRES MAXMIND COUNTRY DB')
    # domain option REQUIRES PAID DB
    # parser.add_argument('-d', action='store_true', dest='domain', help='Return IP domain')
    # isp option REQUIRES PAID DB
    # parser.add_argument('-i', action='store_true', dest='isp', help='Return IP Internet Service Provider')
    # latitude option
    parser.add_argument('-la', action='store_true', dest='latitude', help='Return IP latitude. REQUIRES MAXMIND CITY DB')
    # lat_lon option
    parser.add_argument('-lalo', action='store_true', dest='lat_lon', help='Return IP latitude and longitude. REQUIRES MAXMIND CITY DB')
    # longitude option
    parser.add_argument('-lo', action='store_true', dest='longitude', help='Return IP longitude. REQUIRES MAXMIND CITY DB')
    # postal code option
    parser.add_argument('-p', action='store_true', dest='postal_code', help='Return IP postal code REQUIRES MAXMIND CITY DB')
    # README option
    # parser.add_argument('-r', action='store_true', dest='readme', help='View README')

    # parse arguments/options
    args = parser.parse_args()
    return args


def read_and_respond(db, ip, query):
    try:
        reader = geoip2.database.Reader(db)
        response = reader.city(ip)
        result = eval(query)
        reader.close()
        return result
    except FileNotFoundError:
        print('DB not found')
        print('SHUTTING DOWN')
        exit()
        pass
    except ValueError:
        print('Invalid IP address')
        print('SHUTTING DOWN')
        exit()
    except TypeError:
        try:
            reader = geoip2.database.Reader(db)
            response = reader.country(ip)
            result = eval(query)
            reader.close()
            return result
        except ValueError:
            print('Invalid IP address')
            print('SHUTTING DOWN')
            exit()
        except TypeError:
            print('You did not provide a compatible database.')
            print('SHUTTING DOWN')
            exit()


def readme(): # print readme contents
    pass


def main():

    args = menu()
    db = args.dbpath
    ip = args.address

    print('\nDB: ' + db)
    print('IP: ' + ip + '\n')

    results = build_results_dict(args, db, ip)
    format_and_print_results(results)


if __name__ == '__main__':
    main()

