
# -*- coding: utf-8 -*

#Importing default Python Libs
import json
import ConfigParser

#Importing 3rd party libs
import dateutil.parser
import pandas as pd
import xmltodict
import argparse



class JsonUtil(object):

    def __init__(self, file_name):
        """
        This module aims to take files of different data formats and convert them
        into JSON (New line delimeter) format which allows loading the data into GBQ.
        """
        self.input_file = file_name
        config = ConfigParser.ConfigParser()
        config.readfp(open(r'config.ini'))
        self.output_file = config.get('Path', 'output_file')

    def to_json(self):
        """
        This is a controller function where
        input files are directed to read function and
        the output is directed to data_massage function
        """
        json_format = self.read_file(self.input_file)
        data_massage = self.data_massage(json_format)

    def read_file(self, file_format):
        """
        The input files of different formats are read
        using Pandas and converted into .json format.

        :param file_format: Any format files(.csv, .xlsx etc)
        :return: .json format data

        """
        if file_format.endswith('.xml'):
            with open(file_format, "rb") as out:
                xml_data = xmltodict.parse(out)
                json_file = json.dumps(xml_data, indent=4)
        else:

            if file_format.endswith('.csv'):
                json_file = pd.read_csv(file_format)
            elif file_format.endswith('.xlsx'):
                json_file = pd.read_excel(file_format)
            else:
                return
        rooms = json.loads(json_file.to_json(orient='records'))
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
            with open(self.output_file, 'a') as write_file:
                write_file.write(json.dumps(line_dict) + '\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file')
    file_name = parser.parse_args()

    obj = JsonUtil(file_name.file)
    obj.to_json()



