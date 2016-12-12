import os, sys
import re
import csv
import openpyxl

parentPath = os.path.abspath("../..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
try:
    from recognition_engine.util import matcher_factory
    from recognition_engine.util import place_handler
except ImportError:
    from util import matcher_factory
    from util import place_handler
from recognizer import ContentPattern
from recognizer import recognizer


def reshape_content(content):
    content = content.replace('_x000D_', '\n')
    content, recognitions = recognizer.replace_all_specify_item(content)
    content, cities, countries = place_handler.replace_city_country_name(content)
    recognitions.cities = cities
    recognitions.countries = countries
    return content, recognitions


def combine_training_data(paths, merge_file_name='./data.csv'):
    def get_new_content(content):
        final_result = list()
        in_string = False
        tmp_string = ''
        pre_char = ''
        for single_char in content:
            single_char = single_char.lower()
            if in_string:
                if single_char == '"':
                    in_string = False
                    final_result.append(tmp_string)
                    tmp_string = ''
            elif single_char == '\n':
                final_result.append(tmp_string)
                tmp_string = ''
            elif single_char == '"' and pre_char == '\n':
                in_string = True
            else:
                tmp_string += single_char
            pre_char = single_char
        final_result = [item.strip().replace('\n', ' ') for item in final_result if item != ""]
        return [item for item in final_result if re.search(r'\w+', item) is not None]

    result = list()
    for path in paths:
        with open(path, encoding='utf-8') as f:
            all_content = f.read()
            result += get_new_content(all_content)
    result.sort()

    test_dict = dict()
    for item in result:
        item = item.split('!@#')
        if item[0] not in test_dict:
            test_dict[item[0]] = 0
        test_dict[item[0]] += 1
    for key in test_dict:
        if test_dict[key] == 1:
            print(key)

    f = open(merge_file_name, mode='w', encoding='utf-8')
    f.write('\n'.join(result))
    f.close()


def excel_data_generator(path):
    work_book = openpyxl.load_workbook(path)
    sheet_name = work_book['Sheet1']
    intention = 'E'
    bind_sender_name = 'OOCLLEVNVO/OUKL-CSU-LEVINGTON (NVO)'
    bind_send_email = '/O=OOCL/OU='
    sender_name = 'B'
    send_email = 'C'
    subject = 'F'
    body = 'G'
    start = 1
    result_list = list()
    for row in sheet_name.iter_rows():
        email_intention = sheet_name[intention + str(start)].value
        email_subject = sheet_name[subject + str(start)].value
        email_body = sheet_name[body + str(start)].value
        email_body = email_body.replace('_x000D_', '\n')
        email_body = ContentPattern.extract(email_body, ' ')
        if sheet_name[sender_name + str(start)].value != bind_sender_name \
                and sheet_name[send_email + str(start)].value.find(bind_send_email) == -1:
            email_subject = reshape_content(str(email_subject))
            email_body = reshape_content(email_body)
            print(str(start) + ".." + email_intention + '!@#' + str(email_subject) + "!@#" + email_body)
            result_list.append(email_intention + '!@#' + str(email_subject) + "!@#" + email_body)
        start += 1
    return result_list[1:]


def parse_all_common_word_from_city(path):
    import urllib.request
    url_pattern = r'http://open.iciba.com/huaci_new/dict.php?word='
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line[1:-2]
            if line.find(' ') == -1:
                line = line.lower()
                resp = urllib.request.urlopen(url_pattern + line)
                resp = resp.read().decode('utf-8')
                if resp.find('当前选中内容暂无解释') == -1 and resp.find('地名') == -1 and resp.find('省') == -1:
                    print('find one common word ' + line)


if __name__ == "__main__":
    # test1 = "i have arrive New YorK MILLS hahaha"
    # print(replace_city_country_name(test1))
    print(place_handler.is_string_a_place('to new d arrival'))
    # test2 = "i have arrive NEW YORK hahahaha"
    # print(replace_city_country_name(test2))
    # test3 = "yes this is Griesheim B . Arnstad cowboy"
    # print(replace_city_country_name(test3))
    # combine_training_data(['../../predictive-engine/data/text-learning-raw-2016-02-12.csv', '../../predictive-engine/data/text-learning-raw-2016-01-15.csv', '../../predictive-engine/data/text-learning-data-2016-02-24.csv'])

    # data = excel_data_generator('./Email-CA.xlsx')
    # f = open('./data.csv', mode='w', encoding='utf-8')
    # f.write('\n'.join(data))
    # f.close()

    # parse_all_common_word_from_city('./city.data')
