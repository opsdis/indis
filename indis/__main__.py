# -*- coding: utf-8 -*-
"""
    Copyright (C) 2021  Opsdis AB

    This file is part of indis - Icinga native directory importer service.

    indis is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    indis is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with indis.  If not, see <http://www.gnu.org/licenses/>.

"""

import argparse
import json
import os
import traceback
# from cmdb2monitor.cmdbmo import create_monitor
from distutils.util import strtobool
from typing import Dict, Tuple

import indis.configuration as conf
from indis.cache import factory as cache_factory
from indis.configuration import Configuration
from indis.logging import Log as log
from indis.output.api_writer import Connection
from indis.output_factory import Factory as output_factory
from indis.processor import processing
from indis.source_factory import Factory as source_factory

logger = log(__name__)


def execute(source_name, dryrun: bool, source_reader=None) -> Tuple[Dict[str, int], Dict[str, Dict[str, int]]]:
    if not source_name and not os.getenv('INDIS_PROVIDER'):
        raise Exception("provider name not set")
    source_name = os.getenv('INDIS_PROVIDER', source_name)
    dryrun = bool(strtobool(os.getenv('INDIS_DRYRUN', str(dryrun))))

    try:
        # Get the output class
        output = output_factory(source_name, conf.Configuration)
        logger.info_fmt({'name': output.output_name}, f"created output factory")
        # Get the source provider class and
        source = source_factory(source_name, conf.Configuration, source_reader)
        logger.info_fmt({'name': source.source_module}, f"created source factory")
        logger.info_fmt({'name': source.source_interface}, f"created source factory reader")

        # Fetch transfer from source
        transfer = source.fetch()
        logger.info_fmt(transfer.stats(), "created objects")
        # Process
        processed = processing(transfer=transfer, config=conf.Configuration.get('processor'))
        logger.info_fmt(processed, f"processed")

        # Get cache
        cache_imp = cache_factory(prefix=source_name, config=conf.Configuration.get('cache'), transfer=transfer)

        # apply rules
        con = Connection(conf.Configuration.get('output').get('configuration'))
        con.read_apply_rules()
        # Write output
        output.write(transfer=transfer, cache=cache_imp)
        logger.info("output executed")
        return transfer.stats(), output.write_stats()

    except Exception as err:
        raise err


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='indis - the icinga2 native director importer service')

    parser.add_argument('-d', '--dryrun', action="store_true",
                        dest="dry_run", help="Dry run no updates")

    parser.add_argument('-f', '--configfile',
                        dest="configfile", help="configuration file")

    parser.add_argument('-s', '--source',
                        dest="source_name", help="source provider to run")

    parser.add_argument('-v', '--verbose', action="store_true",
                        dest="verbose", help="verbose output of processing")

    args = parser.parse_args()

    if args.configfile:
        Configuration(args.configfile)
    else:
        Configuration()

    if args.dry_run:
        dry_run = True
    else:
        dry_run = False

    try:
        transfer_stats, ops_stat = execute(source_name=args.source_name, dryrun=dry_run)
        if args.verbose:
            verbose_output = {'source': transfer_stats, 'processed': ops_stat}
            print(json.dumps(verbose_output, indent=4, sort_keys=True))

    except Exception as err:
        traceback.print_exc()
        print(err)
