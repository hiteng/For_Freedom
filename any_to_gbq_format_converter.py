
# -*- coding: utf-8 -*

#Importing default Python Libs
import json
import ConfigParser
import os

#Importing 3rd party libs
import dateutil.parser
import pandas as pd
import xmltodict
import argparse
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
        self.logger = logger

    def to_json(self):
        """
        This is a controller function where
        input files are directed to read function and
        the output is directed to data_massage function
        """
        if os.path.exists(self.input_file):
            json_format = self.read_file(self.input_file)
            if json_format is None:
                return
            else:
                data_massage = self.data_massage(json_format)
                self.logger.info('The {0} file has been formatted to New Line Json '
                                 'format with standard date.'.format(self.input_file))
        else:
            self.logger.info('The {0} file does not exist'.format(self.input_file))

    def read_file(self, file_format):
        """
        The input files of different formats are read
        using Pandas and converted into .json format.

        :param file_format: Any format files(.csv, .xlsx etc)
        :return: .json format data

        """
        if file_format.endswith(('.csv', '.xlsx', '.xml')):
            if file_format.endswith('.xml'):
                try:
                    with open(file_format, "rb") as out:
                        xml_data = xmltodict.parse(out)
                        self.logger.info("Reading the {0} xml file...".format(file_format))
                        json_file = json.dumps(xml_data, indent=4)
                except IOError as e:
                    logging.error("IO Error {}".format(e))
            else:

                if file_format.endswith('.csv'):
                    json_file = pd.read_csv(file_format)
                    self.logger.info("Reading the {0} csv file...".format(file_format))
                    self.logger.debug('json_file: {0}'.format(json_file))
                elif file_format.endswith('.xlsx'):
                    json_file = pd.read_excel(file_format)
                    self.logger.info("Reading the {0} file...".format(file_format))
                    self.logger.debug('json_file: {0}'.format(json_file))
                else:
                    return
                self.logger.info('The {0} file is read successfully!'.format(file_format))
                rooms = json.loads(json_file.to_json(orient='records'))
                self.logger.info("Converting the {0} file to json format".format(file_format))
                room_data = json.dumps(rooms)
                return room_data
        else:
            self.logger.info('The {0} file is not supported for format conversion.'.format(file_format))


    def data_massage(self, json_format):
        """
        The date in input .json format data is converted to YYYYMMDD format
        and the output is wriiten to file in JSON NLJ format.

        :param json_format: .json format data
        :return: NLJ format data with standard YYYYMMDD date and
                write the output on to a file.
        """
        result = [json.dumps(record) for record in json.loads(json_format)]
        self.logger.info('The date is changed to YMD format.')
        for line in result:
            line_dict = json.loads(line)
            date_val = dateutil.parser.parse(line_dict['date'])
            date_val = date_val.strftime('%Y%m%d %H:%m:%S')
            line_dict['date'] = date_val
            self.logger.debug('%s iteration, line=%s', line)
            try:
                with open('output_nlj.json', 'a') as write_file:
                    write_file.write(json.dumps(line_dict) + '\n')
            except IOError as e:
                self.logger.error("IO Error {}".format(e))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', help='Enter a File Name')
    args = parser.parse_args()

    obj = JsonUtil(args.file)
    obj.to_json()


if __name__ == '__main__':
    main()




