import csv
import reshape_util


global_class_dict = {
    'schedule.CSV': 'Schedule',
    'bkg_amendment.CSV': 'BKG Amendment',
    'bkg_creation.CSV': 'BKG Creation',
    'notification.CSV': 'Notification',
    'others_normal.CSV': 'Others_normal',
    'others_ucr.CSV': 'Others_UCR',
    'others_vgm.CSV': 'Others_VGM',
    'rate_quotation.CSV': 'Rate Quotation'
}
global_target_folder = './new_data/'


def process_single_csv_file(file_path, class_name):
    result_str = list()
    used_item = dict()
    with open(file_path) as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            subject = reshape_util.reshape_content(row['Subject'])[0]
            body = reshape_util.reshape_content(row['Body'])[0]
            if body == '':
                continue
            single_item = '!@#'.join([class_name, subject, body])
            if single_item not in used_item:
                result_str.append(single_item)
                used_item[single_item] = True
    return result_str


def process_all_file(class_dict, target_folder):
    result_str = ''
    for file_name in class_dict:
        single_result = process_single_csv_file(target_folder + file_name, class_dict[file_name])
        result_str += '\n'.join(single_result) + '\n'
    return result_str


if __name__ == '__main__':
    print(process_all_file(global_class_dict, global_target_folder))
