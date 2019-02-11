
# -*- coding: utf-8 -*

#Importing default Python Libs
import json
import ConfigParser

#Importing 3rd party libs
import dateutil.parser
import pandas as pd
import xmltodict


class JsonUtil(object):

    def __init__(self):
        """
        This module aims to take files of different data formats and convert them
        into JSON (New line delimeter) format which allows loading the data into GBQ.
        """
        config = ConfigParser.ConfigParser()
        config.readfp(open(r'config.ini'))
        self.input_file = config.get('Path', 'input_file')
        self.output_file = config.get('Path', 'output_file')

    def to_json(self):
        """
        This is a controller function where
        input files are directed to read function and
        the output is directed to data_massage function
        """
        json_format = self.read_file(fileformat=self.input_file)
        data_massage = self.data_massage(json_format)

    def read_file(self, fileformat):
        """
        The input files of different formats are read
        using Pandas and converted into .json format.

        :param fileformat: Any format files(.csv, .xlsx etc)
        :return: .json format data

        """
        if fileformat.endswith('.xml'):
            with open(fileformat, "rb") as out:
                xml_data = xmltodict.parse(out)
                jfile = json.dumps(xml_data, indent=4)
        else:

            if fileformat.endswith('.csv'):
                jfile = pd.read_csv(fileformat, chunksize=10000)
            elif fileformat.endswith('.xlsx'):
                jfile = pd.read_excel(fileformat, chunksize=10000)
            else:
                return
        rooms = json.loads(jfile.to_json(orient='records'))
        room_data = json.dumps(rooms)
        return room_data

    def data_massage(self, json_format):
        """
        The date in input .json format data is converted to YYYYMMDD format
        and the output is wriiten to file in JSON NLJ format.

        :param json_format: .json format data
        :return: NLJ format data with standard YYYYMMDD date and
                write the output on to a file.
        """
        result = [json.dumps(record) for record in json.loads(json_format)]
        for line in result:
            line_dict = json.loads(line)
            date_val = dateutil.parser.parse(line_dict['date'])
            date_val = date_val.strftime('%Y%m%d')
            line_dict['date'] = date_val
            print line_dict
            with open(self.output_file, 'a') as write_file:
                write_file.write(json.dumps(line_dict) + '\n')

if __name__ == '__main__':

    obj = JsonUtil()
    obj.to_json()

