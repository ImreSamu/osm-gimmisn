#!/usr/bin/env python3
#
# Copyright (c) 2019 Miklos Vajna and contributors.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""The test_helpers module covers the helpers module."""

import configparser
import os
from typing import List
import unittest

import yattag  # type: ignore

import helpers
import ranges
import util


def get_relations() -> helpers.Relations:
    """Returns a Relations object that uses the test data and workdir."""
    datadir = os.path.join(os.path.dirname(__file__), "data")
    workdir = os.path.join(os.path.dirname(__file__), "workdir")
    return helpers.Relations(datadir, workdir)


class TestSortStreetsCsv(unittest.TestCase):
    """Tests sort_streets_csv()."""
    def test_single_field(self) -> None:
        """Tests a single column."""
        unsorted = 'head\n2\n1'
        expected = 'head\n1\n2'
        self.assertEqual(helpers.sort_streets_csv(unsorted), expected)

    def test_two_fields(self) -> None:
        """Tests 2 columns."""
        unsorted = 'head\n1\tb\n2\ta'
        expected = 'head\n2\ta\n1\tb'
        self.assertEqual(helpers.sort_streets_csv(unsorted), expected)


class TestSortStreets(unittest.TestCase):
    """Tests sort_streets()."""
    def test_primary(self) -> None:
        """Tests that missing 2nd col is ordered last."""
        unsorted = [
            '0\t\tprimary',
            '1\tPear\tprimary',
            '2\tApple\tsecondary',
            '3\tApple\tprimary',
        ]
        expected = [
            '3\tApple\tprimary',
            '2\tApple\tsecondary',
            '1\tPear\tprimary',
            '0\t\tprimary',
        ]
        self.assertEqual(helpers.sort_streets(unsorted), expected)

    def test_service(self) -> None:
        """Tests that matching 2nd and 3rd col means ordering by 4th col."""
        unsorted = [
            '4\tMine\tservice\tdriveway',
            '5\tMine\tservice\tallay',
        ]
        sort = [
            '5\tMine\tservice\tallay',
            '4\tMine\tservice\tdriveway',
        ]
        self.assertEqual(helpers.sort_streets(unsorted), sort)


class TestSortHouseNumbersCsv(unittest.TestCase):
    """Tests sort_housenumbers_csv()."""
    def test_happy(self) -> None:
        """Tests the happy path."""
        unsorted = 'head\n2\n1'
        expected = 'head\n1\n2'
        self.assertEqual(helpers.sort_housenumbers_csv(unsorted), expected)


class TestSortHousenumbers(unittest.TestCase):
    """Tests sort_housenumbers()."""
    def test_happy(self) -> None:
        """Tests the happy path."""
        unsorted = [
            '0\t\t42\t1234\tPalace\t1000/11\t8\t0\t2\tA\tMinistry of OpenStreetMap',
            '1\tApple ave\t42\t1234\tPalace\t1000/11\t8\t0\t2\tA\tMinistry of OpenStreetMap',
            '2\tPear ave\t42\t1234\tPalace\t1000/11\t8\t0\t2\tA\tMinistry of OpenStreetMap',
            '3\tApple ave\t42\t1234\tPalace\t1000/11\t8\t0\t2\tA\tBase of OpenStreetMap',
            '4\tApple ave\t5\t1234\tPalace\t1000/11\t8\t0\t2\tA\tMinistry of OpenStreetMap',
            '5\tApple ave\t\t1234\t\t\t8\t0\t2\tA\tMinistry of OpenStreetMap',
            '6\tApple ave\t\t1234\t\t1000/11\t8\t0\t2\tA\tMinistry of OpenStreetMap',
            '7\tApple ave\t\t1234\tPalace\t1000/11\t8\t0\t2\tA\tMinistry of OpenStreetMap',
            '8\tApple ave\t42\t\tPalace\t1000/11\t8\t0\t2\tA\tMinistry of OpenStreetMap',
            '9\tApple ave\t42\t\tPalace\t1000/11',
        ]
        expected = [
            '9\tApple ave\t42\t\tPalace\t1000/11',
            '8\tApple ave\t42\t\tPalace\t1000/11\t8\t0\t2\tA\tMinistry of OpenStreetMap',
            '5\tApple ave\t\t1234\t\t\t8\t0\t2\tA\tMinistry of OpenStreetMap',
            '6\tApple ave\t\t1234\t\t1000/11\t8\t0\t2\tA\tMinistry of OpenStreetMap',
            '7\tApple ave\t\t1234\tPalace\t1000/11\t8\t0\t2\tA\tMinistry of OpenStreetMap',
            '0\t\t42\t1234\tPalace\t1000/11\t8\t0\t2\tA\tMinistry of OpenStreetMap',
            '4\tApple ave\t5\t1234\tPalace\t1000/11\t8\t0\t2\tA\tMinistry of OpenStreetMap',
            '3\tApple ave\t42\t1234\tPalace\t1000/11\t8\t0\t2\tA\tBase of OpenStreetMap',
            '1\tApple ave\t42\t1234\tPalace\t1000/11\t8\t0\t2\tA\tMinistry of OpenStreetMap',
            '2\tPear ave\t42\t1234\tPalace\t1000/11\t8\t0\t2\tA\tMinistry of OpenStreetMap',
        ]
        self.assertEqual(helpers.sort_housenumbers(unsorted), expected)


class TestInBoth(unittest.TestCase):
    """Tests get_in_both()."""
    def test_happy(self) -> None:
        """Tests that happy path."""
        self.assertEqual(helpers.get_in_both(["1", "2", "3"], ["2", "3", "4"]), ["2", "3"])


class TestOnlyInFirst(unittest.TestCase):
    """Tests get_only_in_first()."""
    def test_happy(self) -> None:
        """Tests the happy path."""
        self.assertEqual(helpers.get_only_in_first(["1", "2", "3"], ["3", "4"]), ["1", "2"])


class TestRelationGetOsmStreets(unittest.TestCase):
    """Tests Relation.get_osm_streets()."""
    def test_happy(self) -> None:
        """Tests the happy path."""
        relations = get_relations()
        relation = relations.get_relation("test")
        actual = relation.get_osm_streets()
        expected = ['B1', 'B2', 'HB1', 'HB2']
        self.assertEqual(actual, expected)

    def test_no_house_number(self) -> None:
        """Tests the case when we have streets, but no house numbers."""
        relations = get_relations()
        relation = relations.get_relation("ujbuda")
        actual = relation.get_osm_streets()
        expected = ['OSM Name 1', 'Törökugrató utca', 'Tűzkő utca']
        self.assertEqual(actual, expected)


class TestGetWorkdir(unittest.TestCase):
    """Tests get_workdir()."""
    def test_happy(self) -> None:
        """Tests the happy path."""
        config = configparser.ConfigParser()
        config.read_dict({"wsgi": {"workdir": "/path/to/workdir"}})
        actual = helpers.get_workdir(config)
        expected = "/path/to/workdir"
        self.assertEqual(actual, expected)


class TestRelationGetOsmStreetsQuery(unittest.TestCase):
    """Tests Relation.get_osm_streets_query()."""
    def test_happy(self) -> None:
        """Tests the happy path."""
        relations = get_relations()
        self.assertEqual(os.path.join(os.path.dirname(__file__), "workdir"), relations.get_workdir())
        relation_name = "gazdagret"
        relation = relations.get_relation(relation_name)
        ret = relation.get_osm_streets_query()
        self.assertEqual(ret, 'aaa 2713748 bbb 3602713748 ccc\n')


class TestRelationGetOsmHousenumbersQuery(unittest.TestCase):
    """Tests Relation.get_osm_housenumbers_query()."""
    def test_happy(self) -> None:
        """Tests the happy path."""
        relations = get_relations()
        relation_name = "gazdagret"
        relation = relations.get_relation(relation_name)
        ret = relation.get_osm_housenumbers_query()
        self.assertEqual(ret, 'housenr aaa 2713748 bbb 3602713748 ccc\n')


class TestRelationFilesWriteOsmStreets(unittest.TestCase):
    """Tests RelationFiles.write_osm_streets()."""
    def test_happy(self) -> None:
        """Tests the happy path."""
        relations = get_relations()
        relation_name = "gazdagret"
        relation = relations.get_relation(relation_name)
        result_from_overpass = "@id\tname\n1\tTűzkő utca\n2\tTörökugrató utca\n3\tOSM Name 1\n4\tHamzsabégi út\n"
        expected = helpers.get_content(relations.get_workdir(), "streets-gazdagret.csv")
        relation.get_files().write_osm_streets(result_from_overpass)
        actual = helpers.get_content(relations.get_workdir(), "streets-gazdagret.csv")
        self.assertEqual(actual, expected)


class TestRelationFilesWriteOsmHousenumbers(unittest.TestCase):
    """Tests RelationFiles.write_osm_housenumbers()."""
    def test_happy(self) -> None:
        """Tests the happy path."""
        relations = get_relations()
        relation_name = "gazdagret"
        result_from_overpass = "@id\taddr:street\taddr:housenumber\n"
        result_from_overpass += "1\tTörökugrató utca\t1\n"
        result_from_overpass += "1\tTörökugrató utca\t2\n"
        result_from_overpass += "1\tTűzkő utca\t9\n"
        result_from_overpass += "1\tTűzkő utca\t10\n"
        result_from_overpass += "1\tOSM Name 1\t1\n"
        result_from_overpass += "1\tOSM Name 1\t2\n"
        result_from_overpass += "1\tOnly In OSM utca\t1\n"
        expected = helpers.get_content(relations.get_workdir(), "street-housenumbers-gazdagret.csv")
        relation = relations.get_relation(relation_name)
        relation.get_files().write_osm_housenumbers(result_from_overpass)
        actual = helpers.get_content(relations.get_workdir(), "street-housenumbers-gazdagret.csv")
        self.assertEqual(actual, expected)


class TestGetContent(unittest.TestCase):
    """Tests get_content()."""
    def test_happy(self) -> None:
        """Tests the happy path."""
        workdir = os.path.join(os.path.dirname(__file__), "workdir")
        actual = helpers.get_content(workdir, "gazdagret.percent")
        expected = "54.55"
        self.assertEqual(actual, expected)

    def test_one_arg(self) -> None:
        """Tests the case when only one argument is given."""
        workdir = os.path.join(os.path.dirname(__file__), "workdir")
        actual = helpers.get_content(os.path.join(workdir, "gazdagret.percent"))
        expected = "54.55"
        self.assertEqual(actual, expected)


class TestRelationGetStreetRanges(unittest.TestCase):
    """Tests Relation.get_street_ranges()."""
    def test_happy(self) -> None:
        """Tests the happy path."""
        relations = get_relations()
        relation = relations.get_relation("gazdagret")
        filters = relation.get_street_ranges()
        expected_filters = {
            "Budaörsi út": ranges.Ranges([ranges.Range(137, 165)]),
            "Csiki-hegyek utca": ranges.Ranges([ranges.Range(1, 15), ranges.Range(2, 26)]),
            'Hamzsabégi út': ranges.Ranges([ranges.Range(start=1, end=12, interpolation="all")])
        }
        self.assertEqual(filters, expected_filters)
        expected_streets = {
            'OSM Name 1': 'Ref Name 1',
            'OSM Name 2': 'Ref Name 2'
        }
        relations = get_relations()
        self.assertEqual(relations.get_relation("gazdagret").get_config().get_refstreets(), expected_streets)
        street_blacklist = relations.get_relation("gazdagret").get_config().get_street_filters()
        self.assertEqual(street_blacklist, ['Only In Ref Nonsense utca'])

    def test_empty(self) -> None:
        """Tests when the filter file is empty."""
        relations = get_relations()
        relation = relations.get_relation("empty")
        filters = relation.get_street_ranges()
        self.assertEqual(filters, {})


class TestRelationGetRefStreetFromOsmStreet(unittest.TestCase):
    """Tests Relation.get_ref_street_from_osm_street()."""
    def test_happy(self) -> None:
        """Tests the happy path."""
        relations = get_relations()
        street = "Budaörsi út"
        relation_name = "gazdagret"
        relation = relations.get_relation(relation_name)
        refmegye = relation.get_config().get_refmegye()
        street = relation.get_ref_street_from_osm_street(street)
        self.assertEqual("01", refmegye)
        self.assertEqual(["011"], relation.get_config().get_street_reftelepules(street))
        self.assertEqual("Budaörsi út", street)

    def test_reftelepules_override(self) -> None:
        """Tests street-specific reftelepules override."""
        relations = get_relations()
        street = "Teszt utca"
        relation_name = "gazdagret"
        relation = relations.get_relation(relation_name)
        refmegye = relation.get_config().get_refmegye()
        street = relation.get_ref_street_from_osm_street(street)
        self.assertEqual("01", refmegye)
        self.assertEqual(["012"], relation.get_config().get_street_reftelepules(street))
        self.assertEqual("Teszt utca", street)

    def test_refstreets(self) -> None:
        """Tests OSM -> ref name mapping."""
        relations = get_relations()
        street = "OSM Name 1"
        relation_name = "gazdagret"
        relation = relations.get_relation(relation_name)
        refmegye = relation.get_config().get_refmegye()
        street = relation.get_ref_street_from_osm_street(street)
        self.assertEqual("01", refmegye)
        self.assertEqual(["011"], relation.get_config().get_street_reftelepules(street))
        self.assertEqual("Ref Name 1", street)

    def test_nosuchrelation(self) -> None:
        """Tests a relation without a filter file."""
        relations = get_relations()
        street = "OSM Name 1"
        relation_name = "nosuchrelation"
        relation = relations.get_relation(relation_name)
        refmegye = relation.get_config().get_refmegye()
        street = relation.get_ref_street_from_osm_street(street)
        self.assertEqual("01", refmegye)
        self.assertEqual(["011"], relation.get_config().get_street_reftelepules(street))
        self.assertEqual("OSM Name 1", street)

    def test_emptyrelation(self) -> None:
        """Tests a relation with an empty filter file."""
        relations = get_relations()
        street = "OSM Name 1"
        relation_name = "empty"
        relation = relations.get_relation(relation_name)
        refmegye = relation.get_config().get_refmegye()
        street = relation.get_ref_street_from_osm_street(street)
        self.assertEqual("01", refmegye)
        self.assertEqual(["011"], relation.get_config().get_street_reftelepules(street))
        self.assertEqual("OSM Name 1", street)

    def test_range_level_override(self) -> None:
        """Tests the reftelepules range-level override."""
        relations = get_relations()
        street = "Csiki-hegyek utca"
        relation_name = "gazdagret"
        relation = relations.get_relation(relation_name)
        refmegye = relation.get_config().get_refmegye()
        street = relation.get_ref_street_from_osm_street(street)
        self.assertEqual("01", refmegye)
        self.assertEqual(["011", "013"], relation.get_config().get_street_reftelepules(street))
        self.assertEqual("Csiki-hegyek utca", street)


class TestNormalize(unittest.TestCase):
    """Tests normalize()."""
    def test_happy(self) -> None:
        """Tests the happy path."""
        relations = get_relations()
        relation = relations.get_relation("gazdagret")
        normalizers = relation.get_street_ranges()
        house_numbers = helpers.normalize(relation, "139", "Budaörsi út", normalizers)
        self.assertEqual([i.get_number() for i in house_numbers], ["139"])

    def test_not_in_range(self) -> None:
        """Tests when the number is not in range."""
        relations = get_relations()
        relation = relations.get_relation("gazdagret")
        normalizers = relation.get_street_ranges()
        house_numbers = helpers.normalize(relation, "999", "Budaörsi út", normalizers)
        self.assertEqual(house_numbers, [])

    def test_not_a_number(self) -> None:
        """Tests the case when the house number is not a number."""
        relations = get_relations()
        relation = relations.get_relation("gazdagret")
        normalizers = relation.get_street_ranges()
        house_numbers = helpers.normalize(relation, "x", "Budaörsi út", normalizers)
        self.assertEqual(house_numbers, [])

    def test_nofilter(self) -> None:
        """Tests the case when there is no filter for this street."""
        relations = get_relations()
        relation = relations.get_relation("gazdagret")
        normalizers = relation.get_street_ranges()
        house_numbers = helpers.normalize(relation, "1", "Budaörs út", normalizers)
        self.assertEqual([i.get_number() for i in house_numbers], ["1"])

    def test_separator_semicolon(self) -> None:
        """Tests the case when ';' is a separator."""
        relations = get_relations()
        relation = relations.get_relation("gazdagret")
        normalizers = relation.get_street_ranges()
        house_numbers = helpers.normalize(relation, "1;2", "Budaörs út", normalizers)
        self.assertEqual([i.get_number() for i in house_numbers], ["1", "2"])

    def test_separator_interval(self) -> None:
        """Tests the 2-6 case: means implicit 4."""
        relations = get_relations()
        relation = relations.get_relation("gazdagret")
        normalizers = relation.get_street_ranges()
        house_numbers = helpers.normalize(relation, "2-6", "Budaörs út", normalizers)
        self.assertEqual([i.get_number() for i in house_numbers], ["2", "4", "6"])

    def test_separator_interval_parity(self) -> None:
        """Tests the 5-8 case: means just 5 and 8 as the parity doesn't match."""
        relations = get_relations()
        relation = relations.get_relation("gazdagret")
        normalizers = relation.get_street_ranges()
        house_numbers = helpers.normalize(relation, "5-8", "Budaörs út", normalizers)
        self.assertEqual([i.get_number() for i in house_numbers], ["5", "8"])

    def test_separator_interval_interp_all(self) -> None:
        """Tests the 2-5 case: means implicit 3 and 4."""
        relations = get_relations()
        relation = relations.get_relation("gazdagret")
        normalizers = relation.get_street_ranges()
        house_numbers = [i.get_number() for i in helpers.normalize(relation, "2-5", "Hamzsabégi út", normalizers)]
        self.assertEqual(house_numbers, ["2", "3", "4", "5"])

    def test_separator_interval_filter(self) -> None:
        """Tests the case where x-y is partially filtered out."""
        relations = get_relations()
        relation = relations.get_relation("gazdagret")
        normalizers = relation.get_street_ranges()
        # filter is 137-165
        house_numbers = helpers.normalize(relation, "163-167", "Budaörsi út", normalizers)
        # Make sure there is no 167.
        self.assertEqual([i.get_number() for i in house_numbers], ["163", "165"])

    def test_separator_interval_block(self) -> None:
        """Tests the case where x-y is nonsense: y is too large."""
        relations = get_relations()
        relation = relations.get_relation("gazdagret")
        normalizers = relation.get_street_ranges()
        house_numbers = helpers.normalize(relation, "2-2000", "Budaörs út", normalizers)
        # Make sure that we simply ignore 2000: it's larger than the default <998 filter and the
        # 2-2000 range would be too large.
        self.assertEqual([i.get_number() for i in house_numbers], ["2"])

    def test_separator_interval_block2(self) -> None:
        """Tests the case where x-y is nonsense: y-x is too large."""
        relations = get_relations()
        relation = relations.get_relation("gazdagret")
        normalizers = relation.get_street_ranges()
        house_numbers = helpers.normalize(relation, "2-56", "Budaörs út", normalizers)
        # No expansions for 4, 6, etc.
        self.assertEqual([i.get_number() for i in house_numbers], ["2", "56"])

    def test_separator_interval_block3(self) -> None:
        """Tests the case where x-y is nonsense: x is 0."""
        relations = get_relations()
        relation = relations.get_relation("gazdagret")
        normalizers = relation.get_street_ranges()
        house_numbers = helpers.normalize(relation, "0-42", "Budaörs út", normalizers)
        # No expansion like 0, 2, 4, etc.
        self.assertEqual([i.get_number() for i in house_numbers], ["42"])

    def test_separator_interval_block4(self) -> None:
        """Tests the case where x-y is only partially useful: x is OK, but y is a suffix."""
        relations = get_relations()
        relation = relations.get_relation("gazdagret")
        normalizers = relation.get_street_ranges()
        house_numbers = helpers.normalize(relation, "42-1", "Budaörs út", normalizers)
        # No "1", just "42".
        self.assertEqual([i.get_number() for i in house_numbers], ["42"])

    def test_keep_suffix(self) -> None:
        """Tests that the * suffix is preserved."""
        relations = get_relations()
        relation = relations.get_relation("gazdagret")
        normalizers = relation.get_street_ranges()
        house_number = helpers.normalize(relation, "1*", "Budaörs út", normalizers)
        self.assertEqual([i.get_number() for i in house_number], ["1*"])
        house_number = helpers.normalize(relation, "2", "Budaörs út", normalizers)
        self.assertEqual([i.get_number() for i in house_number], ["2"])


class TestRelationGetRefStreets(unittest.TestCase):
    """Tests Relation.GetRefStreets()."""
    def test_happy(self) -> None:
        """Tests the happy path."""
        relation_name = "gazdagret"
        relations = get_relations()
        relation = relations.get_relation(relation_name)
        house_numbers = relation.get_ref_streets()
        self.assertEqual(house_numbers, ['Hamzsabégi út',
                                         'Only In Ref Nonsense utca',
                                         'Only In Ref utca',
                                         'Ref Name 1',
                                         'Törökugrató utca',
                                         'Tűzkő utca'])


class TestRelationGetOsmHouseNumbers(unittest.TestCase):
    """Tests Relation.get_osm_house_numbers()."""
    def test_happy(self) -> None:
        """Tests the happy path."""
        relation_name = "gazdagret"
        street_name = "Törökugrató utca"
        relations = get_relations()
        relation = relations.get_relation(relation_name)
        house_numbers = relation.get_osm_housenumbers(street_name)
        self.assertEqual([i.get_number() for i in house_numbers], ["1", "2"])


class TestRelationGetMissingHousenumbers(unittest.TestCase):
    """Tests Relation.get_missing_housenumbers()."""
    def test_happy(self) -> None:
        """Tests the happy path."""
        relations = get_relations()
        relation_name = "gazdagret"
        relation = relations.get_relation(relation_name)
        ongoing_streets, done_streets = relation.get_missing_housenumbers()
        ongoing_streets_strs = [(name, [i.get_number()
                                        for i in house_numbers]) for name, house_numbers in ongoing_streets]
        # Notice how 11 and 12 is filtered out by the 'invalid' mechanism for 'Törökugrató utca'.
        self.assertEqual(ongoing_streets_strs, [('Törökugrató utca', ['7', '10']),
                                                ('Tűzkő utca', ['1', '2']),
                                                ('Hamzsabégi út', ['1'])])
        expected = [('OSM Name 1', ['1', '2']), ('Törökugrató utca', ['1', '2']), ('Tűzkő utca', ['9', '10'])]
        done_streets_strs = [(name, [i.get_number()
                                     for i in house_numbers]) for name, house_numbers in done_streets]
        self.assertEqual(done_streets_strs, expected)


class TestRelationGetMissingStreets(unittest.TestCase):
    """Tests Relation.get_missing_streets()."""
    def test_happy(self) -> None:
        """Tests the happy path."""
        relations = get_relations()
        relation_name = "gazdagret"
        relation = relations.get_relation(relation_name)
        only_in_reference, in_both = relation.get_missing_streets()

        # Not that 'Only In Ref Nonsense utca' is missing from this list.
        self.assertEqual(only_in_reference, ['Only In Ref utca'])

        self.assertEqual(in_both, ['Hamzsabégi út', 'Ref Name 1', 'Törökugrató utca', 'Tűzkő utca'])


def table_doc_to_string(table: List[List[yattag.Doc]]) -> List[List[str]]:
    """Unwraps an escaped matrix of yattag documents into a string matrix."""
    table_content = []
    for row in table:
        row_content = []
        for cell in row:
            row_content.append(cell.getvalue())
        table_content.append(row_content)
    return table_content


class TestRelationWriteMissingHouseNumbers(unittest.TestCase):
    """Tests Relation.write_missing_housenumbers()."""
    def test_happy(self) -> None:
        """Tests the happy path."""
        relations = get_relations()
        relation_name = "gazdagret"
        relation = relations.get_relation(relation_name)
        expected = helpers.get_content(relations.get_workdir(), "gazdagret.percent")
        ret = relation.write_missing_housenumbers()
        todo_street_count, todo_count, done_count, percent, table = ret
        self.assertEqual(todo_street_count, 3)
        self.assertEqual(todo_count, 5)
        self.assertEqual(done_count, 6)
        self.assertEqual(percent, '54.55')
        table = table_doc_to_string(table)
        self.assertEqual(table, [['Street name', 'Missing count', 'House numbers'],
                                 ['Törökugrató utca', '2', '7<br />10'],
                                 ['Tűzkő utca', '2', '1<br />2'],
                                 ['Hamzsabégi út', '1', '1']])
        actual = helpers.get_content(relations.get_workdir(), "gazdagret.percent")
        self.assertEqual(actual, expected)

    def test_empty(self) -> None:
        """Tests the case when percent can't be determined."""
        relations = get_relations()
        relation_name = "empty"
        relation = relations.get_relation(relation_name)
        ret = relation.write_missing_housenumbers()
        _todo_street_count, _todo_count, _done_count, percent, _table = ret
        self.assertEqual(percent, '100.00')
        os.unlink(os.path.join(relations.get_workdir(), "empty.percent"))
        self.assertEqual({}, relation.get_config().get_filters())

    def test_interpolation_all(self) -> None:
        """Tests the case when the street is interpolation=all and coloring is wanted."""
        relations = get_relations()
        relation_name = "budafok"
        relation = relations.get_relation(relation_name)
        ret = relation.write_missing_housenumbers()
        _todo_street_count, _todo_count, _done_count, _percent, table = ret
        table = table_doc_to_string(table)
        self.assertEqual(table, [['Street name', 'Missing count', 'House numbers'],
                                 ['Vöröskúti határsor', '2', '34, <span style="color: blue;">36</span>']])


class TestRelationWriteMissingStreets(unittest.TestCase):
    """Tests Relation.write_missing_streets()."""
    def test_happy(self) -> None:
        """Tests the happy path."""
        relations = get_relations()
        relation_name = "gazdagret"
        relation = relations.get_relation(relation_name)
        expected = helpers.get_content(relations.get_workdir(), "gazdagret-streets.percent")
        ret = relation.write_missing_streets()
        todo_count, done_count, percent, streets = ret
        self.assertEqual(todo_count, 1)
        self.assertEqual(done_count, 4)
        self.assertEqual(percent, '80.00')
        self.assertEqual(streets, ['Only In Ref utca'])
        actual = helpers.get_content(relations.get_workdir(), "gazdagret-streets.percent")
        self.assertEqual(actual, expected)

    def test_empty(self) -> None:
        """Tests the case when percent can't be determined."""
        relations = get_relations()
        relation_name = "empty"
        relation = relations.get_relation(relation_name)
        ret = relation.write_missing_streets()
        _todo_count, _done_count, percent, _streets = ret
        self.assertEqual(percent, '100.00')
        os.unlink(os.path.join(relations.get_workdir(), "empty-streets.percent"))


class TestRelationBuildRefHousenumbers(unittest.TestCase):
    """Tests Relation.build_ref_housenumbers()."""
    def test_happy(self) -> None:
        """Tests the happy path."""
        refdir = os.path.join(os.path.dirname(__file__), "refdir")
        relations = get_relations()
        refpath = os.path.join(refdir, "hazszamok_20190511.tsv")
        memory_cache = util.build_reference_cache(refpath)
        relation_name = "gazdagret"
        street = "Törökugrató utca"
        relation = relations.get_relation(relation_name)
        ret = relation.build_ref_housenumbers(memory_cache, street, "")
        expected = [
            'Törökugrató utca 1',
            'Törökugrató utca 10',
            'Törökugrató utca 11',
            'Törökugrató utca 12',
            'Törökugrató utca 2',
            'Törökugrató utca 7',
        ]
        self.assertEqual(ret, expected)

    def test_missing(self) -> None:
        """Tests the case when the street is not in the reference."""
        relations = get_relations()
        refdir = os.path.join(os.path.dirname(__file__), "refdir")
        refpath = os.path.join(refdir, "hazszamok_20190511.tsv")
        memory_cache = util.build_reference_cache(refpath)
        relation_name = "gazdagret"
        street = "No such utca"
        relation = relations.get_relation(relation_name)
        ret = relation.build_ref_housenumbers(memory_cache, street, "")
        self.assertEqual(ret, [])


class TestRelationBuildRefStreets(unittest.TestCase):
    """Tests Relation.build_ref_streets()."""
    def test_happy(self) -> None:
        """Tests the happy path."""
        refdir = os.path.join(os.path.dirname(__file__), "refdir")
        refpath = os.path.join(refdir, "utcak_20190514.tsv")
        memory_cache = util.build_street_reference_cache(refpath)
        relation_name = "gazdagret"
        relations = get_relations()
        relation = relations.get_relation(relation_name)
        ret = relation.build_ref_streets(memory_cache)
        self.assertEqual(ret, ['Törökugrató utca',
                               'Tűzkő utca',
                               'Ref Name 1',
                               'Only In Ref utca',
                               'Only In Ref Nonsense utca',
                               'Hamzsabégi út'])


class TestRelationWriteRefHousenumbers(unittest.TestCase):
    """Tests Relation.write_ref_housenumbers()."""
    def test_happy(self) -> None:
        """Tests the happy path."""
        refdir = os.path.join(os.path.dirname(__file__), "refdir")
        refpath = os.path.join(refdir, "hazszamok_20190511.tsv")
        refpath2 = os.path.join(refdir, "hazszamok_kieg_20190808.tsv")
        relations = get_relations()
        relation_name = "gazdagret"
        expected = helpers.get_content(relations.get_workdir(), "street-housenumbers-reference-gazdagret.lst")
        relation = relations.get_relation(relation_name)
        relation.write_ref_housenumbers([refpath, refpath2])
        actual = helpers.get_content(relations.get_workdir(), "street-housenumbers-reference-gazdagret.lst")
        self.assertEqual(actual, expected)

    def test_nosuchrefmegye(self) -> None:
        """Tests the case when the refmegye code is missing in the reference."""
        refdir = os.path.join(os.path.dirname(__file__), "refdir")
        refpath = os.path.join(refdir, "hazszamok_20190511.tsv")
        relations = get_relations()
        relation_name = "nosuchrefmegye"
        relation = relations.get_relation(relation_name)
        try:
            relation.write_ref_housenumbers([refpath])
        except KeyError:
            self.fail("write_ref_housenumbers() raised KeyError unexpectedly")

    def test_nosuchreftelepules(self) -> None:
        """Tests the case when the reftelepules code is missing in the reference."""
        refdir = os.path.join(os.path.dirname(__file__), "refdir")
        refpath = os.path.join(refdir, "hazszamok_20190511.tsv")
        relations = get_relations()
        relation_name = "nosuchreftelepules"
        relation = relations.get_relation(relation_name)
        try:
            relation.write_ref_housenumbers([refpath])
        except KeyError:
            self.fail("write_ref_housenumbers() raised KeyError unexpectedly")


class TestRelationWriteRefStreets(unittest.TestCase):
    """Tests Relation.WriteRefStreets()."""
    def test_happy(self) -> None:
        """Tests the happy path."""
        refdir = os.path.join(os.path.dirname(__file__), "refdir")
        refpath = os.path.join(refdir, "utcak_20190514.tsv")
        relations = get_relations()
        relation_name = "gazdagret"
        relation = relations.get_relation(relation_name)
        expected = helpers.get_content(relations.get_workdir(), "streets-reference-gazdagret.lst")
        relation.write_ref_streets(refpath)
        actual = helpers.get_content(relations.get_workdir(), "streets-reference-gazdagret.lst")
        self.assertEqual(actual, expected)


class TestRelations(unittest.TestCase):
    """Tests the Relations class."""
    def test_happy(self) -> None:
        """Tests the happy path."""
        relations = get_relations()
        expected_relation_names = [
            "budafok",
            "empty",
            "gazdagret",
            "inactiverelation",
            "nosuchrefmegye",
            "nosuchreftelepules",
            "nosuchrelation",
            "test",
            "ujbuda"
        ]
        self.assertEqual(relations.get_names(), expected_relation_names)
        self.assertTrue("inactiverelation" not in relations.get_active_names())
        osmids = sorted([relation.get_config().get_osmrelation() for relation in relations.get_relations()])
        self.assertEqual([13, 42, 42, 43, 44, 45, 66, 221998, 2713748], osmids)
        self.assertEqual("only", relations.get_relation("ujbuda").get_config().should_check_missing_streets())

        relations.activate_all(True)
        self.assertTrue("inactiverelation" in relations.get_active_names())

        # Allow seeing data of a relation even if it's not in relations.yaml.
        relations.get_relation("gh195")


class TestRelationConfigMissingStreets(unittest.TestCase):
    """Tests RelationConfig.should_check_missing_streets()."""
    def test_happy(self) -> None:
        """Tests the happy path."""
        relation_name = "ujbuda"
        relations = get_relations()
        relation = relations.get_relation(relation_name)
        ret = relation.get_config().should_check_missing_streets()
        self.assertEqual(ret, "only")

    def test_empty(self) -> None:
        """Tests the default value."""
        relation_name = "empty"
        relations = get_relations()
        relation = relations.get_relation(relation_name)
        self.assertEqual(relation.get_name(), "empty")
        ret = relation.get_config().should_check_missing_streets()
        self.assertEqual(ret, "yes")

    def test_nosuchrelation(self) -> None:
        """Tests a relation without a filter file."""
        relation_name = "nosuchrelation"
        relations = get_relations()
        relation = relations.get_relation(relation_name)
        ret = relation.get_config().should_check_missing_streets()
        self.assertEqual(ret, "yes")


class TestRefmegyeGetName(unittest.TestCase):
    """Tests refmegye_get_name()."""
    def test_happy(self) -> None:
        """Tests the happy path."""
        relations = get_relations()
        self.assertEqual(relations.refmegye_get_name("01"), "Budapest")
        self.assertEqual(relations.refmegye_get_name("99"), "")


class TestRefmegyeGetReftelepulesIds(unittest.TestCase):
    """Tests refmegye_get_reftelepules_ids()."""
    def test_happy(self) -> None:
        """Tests the happy path."""
        relations = get_relations()
        self.assertEqual(relations.refmegye_get_reftelepules_ids("01"), ["011"])
        self.assertEqual(relations.refmegye_get_reftelepules_ids("99"), [])


class TestReftelepulesGetName(unittest.TestCase):
    """Tests reftelepules_get_name()."""
    def test_happy(self) -> None:
        """Tests the happy path."""
        relations = get_relations()
        self.assertEqual(relations.reftelepules_get_name("01", "011"), "Újbuda")
        self.assertEqual(relations.reftelepules_get_name("99", ""), "")
        self.assertEqual(relations.reftelepules_get_name("01", "99"), "")


class TestRelationStreetIsEvenOdd(unittest.TestCase):
    """Tests RelationConfig.get_street_is_even_odd()."""
    def test_happy(self) -> None:
        """Tests the happy path."""
        relations = get_relations()
        relation = relations.get_relation("gazdagret")
        self.assertFalse(relation.get_config().get_street_is_even_odd("Hamzsabégi út"))

        self.assertTrue(relation.get_config().get_street_is_even_odd("Teszt utca"))


class TestRelationIsActive(unittest.TestCase):
    """Tests RelationConfig.is_active()."""
    def test_happy(self) -> None:
        """Tests the happy path."""
        relations = get_relations()
        relation = relations.get_relation("gazdagret")
        self.assertTrue(relation.get_config().is_active())


class TestMakeTurboQueryForStreets(unittest.TestCase):
    """Tests make_turbo_query_for_streets()."""
    def test_happy(self) -> None:
        """Tests the happy path."""
        relations = get_relations()
        relation = relations.get_relation("gazdagret")
        fro = [[util.html_escape("A1"),
                util.html_escape("B1")],
               [util.html_escape("A2"),
                util.html_escape("B2")]]
        ret = helpers.make_turbo_query_for_streets(relation, fro)
        expected = """[out:json][timeout:425];
rel(2713748)->.searchRelation;
area(3602713748)->.searchArea;
(way["name"="A2"](r.searchRelation);
way["name"="A2"](area.searchArea);
);
out body;
>;
out skel qt;"""
        self.assertEqual(ret, expected)


if __name__ == '__main__':
    unittest.main()
