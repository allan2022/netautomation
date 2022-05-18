from utils.filetools import write_file
from acivalidationtools.builddict.buildsubjectfilterentrydict import BuildSubjectFilterEntryDict


class SubjectFilterEntry():

    def __init__(self, apic):
        self.output_directory = apic.output_directory
        self.config = apic.config
        self.filter_query_dict = apic.data_dict['vzFilter_data']
        self.filter_subject_relation_dict = apic.data_dict['vzRsSubjFiltAtt_data']

    
    def build_subject_filter_entry_dict(self):
        print()
        print(f'Building build_subject_filter_entry_dict...')
        print()
        build_subject_filter_entry_dict = BuildSubjectFilterEntryDict(self.filter_query_dict, self.filter_subject_relation_dict)
        subject_filter_entry_dict, filter_no_subject_dict = build_subject_filter_entry_dict.build_subject_filter_entry_dict()
        write_file(f'{self.output_directory}/subject_filter_entry_parsed.txt', subject_filter_entry_dict)
        write_file(f'{self.output_directory}/filter_no_subject_parsed.txt', filter_no_subject_dict)

