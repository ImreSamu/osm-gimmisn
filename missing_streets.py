#!/usr/bin/env python3
#
# Copyright 2019 Miklos Vajna. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#

"""Compares reference streets with OSM ones and shows the diff."""

import sys
import configparser
import helpers
import util


def main() -> None:
    """Commandline interface."""
    config = configparser.ConfigParser()
    config_path = util.get_abspath("wsgi.ini")
    config.read(config_path)
    workdir = util.get_abspath(config.get('wsgi', 'workdir').strip())
    datadir = util.get_abspath("data")

    relation_name = sys.argv[1]

    relations = helpers.Relations(datadir, workdir)
    relation = relations.get_relation(relation_name)
    only_in_reference, _ = relation.get_missing_streets()

    for street in only_in_reference:
        print(street)


if __name__ == '__main__':
    main()

# vim:set shiftwidth=4 softtabstop=4 expandtab:
