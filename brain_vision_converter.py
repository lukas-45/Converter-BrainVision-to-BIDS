# pylint: disable=W0601
# pylint: disable=W0603
# pylint: disable=C0103
"""
    Modul contains class BrainVisionConverter
    which convert data from
    BrainVision to BIDS
    """
import os
import glob
import json
import mne
import metadata_transform
from mne_bids import write_raw_bids

IID = 1


class BrainVisionConverter:
    """
    Class converts data from
    BrainVision to BIDS
    """
    @staticmethod
    def next_id():
        """
        counter id
        """
        global IID
        IID += 1
        res = IID
        return res

    def transform_data_to_bids_call(self, directory, data_name, data_tar_name, xml_files):
        """
        transform data from BrainVision to BIDS format
        :param directory: BrainVision directory
        :param data_name: dataset name
        :param data_tar_name: name of target directory to save BIDS format
        :param xml_files: list of metadata.xml
        """
        global IID
        idd = str(IID)

        raw = mne.io.read_raw_brainvision(
            directory,
            preload=False)

        if IID < 10:
            idd = '0' + idd

        write_raw_bids(raw, 'sub-' + idd + '_task-' + data_name,
                       bids_root=data_tar_name + '/' + data_name)
        if IID == 1:
            metadata_transform.MetadataConvert().create_data_source_directory(data_tar_name +
                                                                              '/' + data_name + '/')

        file_json = self.search_eeg_json(data_tar_name+'/'+data_name+'/sub-'+idd)
        self.update_json_file(file_json, data_name)

        file_txt = self.search_experiment_txt(directory)
        file_metadata_xml = self.search_metadata_xml(directory)
        print(directory)
        print("velikost je: " + str(len(file_metadata_xml)))
        print(IID)

        if len(file_metadata_xml) > 0:
            metadata_transform.MetadataConvert().copy_xml_file(file_metadata_xml[0],
                                                               data_tar_name + '/' + data_name +
                                                               '/sourcedata', 'sub-' + idd +
                                                               '_task-' + data_name)
        if len(file_txt) > 0:
            metadata_transform.MetadataConvert().read_txt_file(file_txt[0], idd)
            metadata_transform.MetadataConvert().read_xml_eeg_reference(file_metadata_xml[IID - 1],
                                                                        file_json[0])
        else:
            if len(xml_files) > IID-1:
                metadata_transform.MetadataConvert.read_xml_file(xml_files[IID-1], idd)
                metadata_transform.MetadataConvert().read_xml_eeg_reference(file_metadata_xml[IID - 1],
                                                                            file_json[0])
        IID = self.next_id()

    def transform_data_to_bids_call_experiment(self, directory, data_tar_name):
        """
        transform data (one experiment) from BrainVision to BIDS format
        :param directory: BrainVision directory
        :param data_tar_name: name of target directory
        """
        global IID
        idd = str(IID)
        data_name = os.path.basename(data_tar_name)
        raw = mne.io.read_raw_brainvision(
            directory,
            preload=False)
        if IID < 10:
            idd = '0' + idd
        write_raw_bids(raw, 'sub-' + idd + '_task-' + data_name, bids_root=data_tar_name)
        file_json = self.search_eeg_json(data_tar_name + '/sub-' + idd)
        self.update_json_file(file_json, data_name)
        file_txt = self.search_experiment_txt(directory)
        xml_file = self.search_metadata_xml(directory)
        if len(file_txt) > 0:
            metadata_transform.MetadataConvert().read_txt_file(file_txt[0], idd)
        elif len(xml_file) > 0:
            metadata_transform.MetadataConvert.read_xml_file(xml_file[0], idd)
        IID = self.next_id()

    @staticmethod
    def get_id(dir_name):
        """
        get id
        :param dir_name: path of BIDS directory
        """
        sub_folders = [f.path for f in os.scandir(dir_name) if f.is_dir()]
        global IID
        IID = len(sub_folders)+1

    @staticmethod
    def search_eeg_json(dir_name):
        """
        search eeg.json file in directory
        :param dir_name: path to directory
        """
        eeg_file = glob.glob(dir_name + "/**/*eeg.json", recursive=True)
        return eeg_file

    @staticmethod
    def search_eeg_vhdr(dir_name):
        """
        search eeg.vhdr file in directory
        :param dir_name: path to directory
        """
        eeg_file = glob.glob(dir_name + "/**/*eeg.vhdr", recursive=True)
        return eeg_file

    @staticmethod
    def search_experiment_txt(file_name):
        """
        search .txt file in directory
        :param file_name: path to vhdr file
        """
        dir_name = os.path.dirname(file_name)
        eeg_file = glob.glob(dir_name + "/**/*.txt", recursive=True)
        return eeg_file

    @staticmethod
    def search_metadata_xml(file_name):
        """
        search .xml file in directory
        :param file_name: path to vhdr file
        """
        dir_name = os.path.dirname(os.path.dirname(os.path.dirname(file_name)))
        xml_file = glob.glob(dir_name + "/**/*.xml", recursive=True)
        return xml_file

    @staticmethod
    def update_json_file(file, task_name):
        """
        update *eeg.json file
        set Taskname, PowerLineFrequency, EEGGround
        and EEGPlacementScheme
        :param file: path to *eeg.json file
        :param task_name: name of task
        """
        a_file = open(file[0], "r")

        json_object = json.load(a_file)

        a_file.close()

        print(json_object)

        json_object["TaskName"] = task_name
        json_object["PowerLineFrequency"] = 50
        json_object["EEGGround"] = "right ear"
        json_object["EEGPlacementScheme"] = "10-20"

        a_file = open(file[0], "w")

        json.dump(json_object, a_file)

        a_file.close()
