

import unittest
from any_to_gbq_format_converter import JsonUtil


class DataTest(unittest.TestCase):


    def test_date_1(self):

        data = '[{"date": "2019-02-03T14:29:34", "building": "building", "notes": "djhf", "name": "Room"}]'
        out = {u'building': u'building', u'date': '20190203 14:02:34', u'name': u'Room', u'notes': u'djhf'}
        obj1 = JsonUtil(data)

        self.assertEqual(obj1.data_massage(data), out)

    def test_date_2(self):
        data = '[{"date": "2019-02-03 14:29:34", "building": "building", "notes": "djhf", "name": "Room"}]'
        out = {u'building': u'building', u'date': '20190203 14:02:34', u'name': u'Room', u'notes': u'djhf'}
        obj2 = JsonUtil(data)

        self.assertEqual(obj2.data_massage(data), out)

    def test_date_3(self):
        data = '[{"date": "2019-02-03 14:29:34", "building": "building", "notes": "djhf", "name": "Room"}]'
        out = {u'building': u'building', u'date': '20190203 14:02:34', u'name': u'Room', u'notes': u'djhf'}
        obj3 = JsonUtil(data)

        self.assertEqual(obj3.data_massage(data), out)

    def test_date_4(self):
        data = '[{"date": "2019/02/03 14:29:34", "building": "building", "notes": "djhf", "name": "Room"}]'
        out = {u'building': u'building', u'date': '20190203 14:02:34', u'name': u'Room', u'notes': u'djhf'}
        obj3 = JsonUtil(data)

        self.assertEqual(obj3.data_massage(data), out)

    def test_date_5(self):
        data = '[{"date": "02-03-2019 14:29:34", "building": "building", "notes": "djhf", "name": "Room"}]'
        out = {u'building': u'building', u'date': '20190203 14:02:34', u'name': u'Room', u'notes': u'djhf'}
        obj3 = JsonUtil(data)

        self.assertEqual(obj3.data_massage(data), out)

    def test_date_6(self):
        data = '[{"date": "Feb 03 2019 14:29:34", "building": "building", "notes": "djhf", "name": "Room"}]'
        out = {u'building': u'building', u'date': '20190203 14:02:34', u'name': u'Room', u'notes': u'djhf'}
        obj3 = JsonUtil(data)

        self.assertEqual(obj3.data_massage(data), out)

    def test_date_7(self):
        data = '[{"date": " 03 Feb 2019 14:29:34", "building": "building", "notes": "djhf", "name": "Room"}]'
        out = {u'building': u'building', u'date': '20190203 14:02:34', u'name': u'Room', u'notes': u'djhf'}
        obj3 = JsonUtil(data)

        self.assertEqual(obj3.data_massage(data), out)

    def test_date_8(self):
        data = '[{"date": " 02.03.2019 14:29:34", "building": "building", "notes": "djhf", "name": "Room"}]'
        out = {u'building': u'building', u'date': '20190203 14:02:34', u'name': u'Room', u'notes': u'djhf'}
        obj3 = JsonUtil(data)

        self.assertEqual(obj3.data_massage(data), out)


if __name__ == '__main__':

    unittest.main()





