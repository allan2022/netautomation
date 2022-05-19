import datetime
from os import getcwd
from validationtools.validationconfig import ValidationConfig
from validationtools.validationcheck import ValidationCheck
from pyatstools.pyatsdiff import PyatsDiff
from utils.filetools import rename_folder_with_suffix


ACI_VALIDATION_CONFIG = getcwd() + '/src/aci_validation_config.yaml'


class AciValidation():
    def __init__(self):
        self.config = ValidationConfig(ACI_VALIDATION_CONFIG, 'aci')


    def aci_validation(self):
        start =  datetime.datetime.now()
        apic = ValidationCheck(self.config)
        apic.output_directory = rename_folder_with_suffix(apic.output_directory, self.config.folder_suffix)
        if self.config.task.startswith('post_check'):
            print('PyatsDiff......')
            PyatsDiff(parent_class=apic, keyword='aci')

        end = datetime.datetime.now()
        print('Execution time : ', end - start)
        print()


def main():
    validation = AciValidation()
    validation.aci_validation()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
