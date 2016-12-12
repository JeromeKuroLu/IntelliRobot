import os, sys

parentPath = os.path.abspath("../..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
parentPath = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)
try:
    from recognition_engine.util import matcher_factory
except ImportError:
    from util import matcher_factory


def generate_dict_from_csv(file_name):
    with open(file_name, encoding="utf-8") as f:
        result = dict()
        for line in f:
            target_line = line[1:-2]
            # target_array = [item.strip() for item in target_line.split(" ") if item != '']
            target_array = matcher_factory.split_all_words(target_line)
            tmp_dict = result
            for item in target_array:
                item = item.upper()
                if item not in tmp_dict:
                    tmp_dict[item] = dict()
                tmp_dict = tmp_dict[item]
            tmp_dict['Finished'] = True
    return result


city = generate_dict_from_csv(os.path.dirname(os.path.abspath(__file__)) + '/city.data')
country = generate_dict_from_csv(os.path.dirname(os.path.abspath(__file__)) + '/country.data')


def search_in_dict(target_dict, target_array, start_index):
    if 'Finished' in target_dict and len(target_dict) == 1:
        return start_index
    if start_index >= len(target_array):
        if 'Finished' not in target_dict:
            return -1
        else:
            return start_index
    current_item = target_array[start_index].upper()
    if 'Finished' in target_dict:
        if current_item not in target_dict:
            return start_index
        else:
            new_index = search_in_dict(target_dict[current_item], target_array, start_index + 1)
            if new_index == -1:
                return start_index
            else:
                return new_index
    if current_item not in target_dict:
        return -1
    else:
        return search_in_dict(target_dict[current_item], target_array, start_index + 1)


def search_next_places(target_array, array_index):
    city_name = '_City_'
    country_name = '_Country_'
    start_index = array_index
    end_index = search_in_dict(country, target_array, start_index)
    replace_string = country_name
    if end_index == -1:
        end_index = search_in_dict(city, target_array, start_index)
        replace_string = city_name
        if end_index == -1:
            end_index = start_index
    return start_index, end_index, replace_string


def is_string_a_place(target_string):
    target_array = matcher_factory.split_all_words(target_string)
    array_index = 0
    while array_index < len(target_array):
        start_index, end_index, replace_string = search_next_places(target_array, array_index)
        if start_index == end_index:
            array_index += 1
        else:
            return ' '.join(target_array[start_index: end_index])
    return False


def replace_city_country_name(target_string):
    target_array = matcher_factory.split_all_words(target_string)
    array_index = 0
    cities = list()
    countries = list()
    while array_index < len(target_array):
        start_index, end_index, replace_string = search_next_places(target_array, array_index)
        if start_index == end_index:
            array_index += 1
        else:
            # print(' '.join(target_array[start_index:end_index]) + "," + replace_string)
            if replace_string == '_City_':
                cities.append(' '.join(target_array[start_index: end_index]))
            else:
                countries.append(' '.join(target_array[start_index: end_index]))
            target_array[start_index] = replace_string
            target_array = target_array[:start_index + 1] + target_array[end_index:]
            array_index = end_index
    return ' '.join(target_array), cities, countries
