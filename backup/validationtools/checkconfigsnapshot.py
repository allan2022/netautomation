from utils.filetools import write_file, create_folder
from utils.generalutils import dict_reorder


class CheckConfigSnapshot():

    def __init__(self, config, folder=None):
        self.data_dict = config.data_dict
        if folder:
            self.output_directory = folder
            self.build_config_snapshot_dict_sequence_list = config.build_dict_sequence
            create_folder(self.output_directory)
        else:
            self.output_directory = config.output_directory
            self.build_config_snapshot_dict_sequence_list = config.config.cfg.get('build_dict_sequence')['build_config_snapshot_dict_sequence'].split()


    def build_config_snapshot_dict(self):
        print()
        print('Building config_snapshot_dict...')
        print()
        for build_class in self.build_config_snapshot_dict_sequence_list:
            config_snapshot_dict, creation_time_snapshot_dict = self.build_config_snapshot_dict_sub(build_class)
        write_file(f'{self.output_directory}/config_snapshot_file_name_as_key_parsed.txt', config_snapshot_dict)
        write_file(f'{self.output_directory}/config_snapshot_creation_time_as_key_parsed.txt', creation_time_snapshot_dict)


    def build_config_snapshot_dict_sub(self, build_class):
        config_snapshot_dict = {}
        creation_time_snapshot_dict = {}
        for item in self.data_dict[f'{build_class}_data']:
            item_dn = item[build_class]['attributes']['dn']
            if build_class == 'configSnapshot':
                createTime = item[build_class]['attributes']['createTime']
                descr = item[build_class]['attributes']['descr']
                fileName = item[build_class]['attributes']['fileName']
                retire = item[build_class]['attributes']['retire']
                name= item[build_class]['attributes']['name']
                size = item[build_class]['attributes']['size']
                config_snapshot_dict.update({
                    fileName:{
                        'dn': item_dn,
                        'createTime': createTime,
                        'description': descr,
                        'name': name,
                        'size': size,
                        'retire': retire
                    }
                })
                creation_time_snapshot_dict.update({createTime:fileName})
        config_snapshot_dict = dict_reorder(config_snapshot_dict)
        creation_time_snapshot_dict = dict_reorder(creation_time_snapshot_dict)
        return config_snapshot_dict, creation_time_snapshot_dict
