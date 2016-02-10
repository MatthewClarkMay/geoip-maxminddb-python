#!/usr/bin/python3

"""
AUTHOR: Matthew May - mcmay.web@gmail.com
"""

# Imports
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from sys import argv
from textwrap import dedent
import geoip2.database


def city(db, ip): # return string("city")
    reader = geoip2.database.Reader(db)
    response = reader.city(ip) # REQUIRES MAXMIND CITY DB
    reader.close()
    return response.city.name


def country(db, ip): # return string("country")
    reader = geoip2.database.Reader(db)
    response = reader.country(ip) # REQUIRES MAXMIND COUNTRY DB
    reader.close()
    return response.country.name


def country_code(db, ip): # return string("country_code")
    reader = geoip2.database.Reader(db)
    response = reader.country(ip) # REQUIRES MAXMIND COUNTRY DB
    reader.close()
    return response.country.iso_code


def domain(db, ip): # return string("domain") REQUIRES PAID DB
    pass


def isp(db, ip): # return string("Internet Service Provider") REQUIRES PAID DB
    pass


def lat(db, ip): # return float(latitude)
    reader = geoip2.database.Reader(db)
    response = reader.city(ip) # REQUIRES MAXMIND CITY DB
    reader.close()
    return response.location.latitude


def lat_lon(db, ip): # return [float(latitude), float(longitude)]
    # REQUIRES MAXMIND CITY DB
    latitude = lat(db, ip)
    longitude = lon(db, ip)
    return [latitude, longitude]


def lon(db, ip): # return float(longitude)
    reader = geoip2.database.Reader(db) # REQUIRES MAXMIND CITY DB
    response = reader.city(ip)
    reader.close()
    return response.location.longitude


def postal(db, ip): # return int(postal_code)
    reader = geoip2.database.Reader(db) # REQUIRES MAXMIND CITY DB
    response = reader.city(ip)
    reader.close()
    return response.postal.code


def readme(): # print readme contents
    pass


def main():
    # instantiate parser
    parser = ArgumentParser(
            prog='geoLocate.py',
            usage='%(prog)s [DB] [IP] [OPTIONS]',
            formatter_class=RawDescriptionHelpFormatter,
            description=dedent('''\
                    GeoIP Locator: Returns city, country, or latitude/longitude, depending on the option(s) passed.

                    Default output with no options passed: [latitude, longitude]'''))

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
    # longitude option
    parser.add_argument('-lo', action='store_true', dest='longitude', help='Return IP longitude. REQUIRES MAXMIND CITY DB')
    # postal code option
    parser.add_argument('-p', action='store_true', dest='postal_code', help='Return IP postal code REQUIRES MAXMIND CITY DB')
    # README option
    # parser.add_argument('-r', action='store_true', dest='readme', help='View README')

    # parse arguments/options
    args = parser.parse_args()

    db = args.dbpath
    ip = args.address

    print('\nDB PATH: ' + db)
    print('IP: ' + ip + '\n')

    if args.city:
        ci = city(db, ip)
        print(ci)
    if args.country:
        co = country(db, ip)
        print(co)
    if args.country_code:
        cc = country_code(db, ip)
        print(cc)
    # if args.domain: # REQUIRES PAID DB
    #     d = domain(db, ip)
    #     print(d)
    # if args.isp: # REQUIRES PAID DB
    #     i = isp(db, ip)
    #     print(i)
    if args.latitude:
        la = lat(db, ip)
        print(la)
    if args.longitude:
        lo = lon(db, ip)
        print(lo)
    if args.postal_code:
        p = postal(db, ip)
        print(p)
    # if args.readme:
    #     readme()
    if len(argv) <= 3:
        ll = lat_lon(db, ip)
        print(ll)


if __name__ == '__main__':
    main()

