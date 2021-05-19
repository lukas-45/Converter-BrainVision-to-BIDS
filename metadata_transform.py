# pylint: disable=W0601
# pylint: disable=W0603
# pylint: disable=C0103
"""
The module  that converts metadata
"""
import json
import os
import shutil
import xml.etree.ElementTree as Etree
import csv


class MetadataConvert:
    """
    The class  that converts metadata
    """
    def read_xml_eeg_reference(self, path, target_file):
        """
        read metadata.xml file and get EEG reference
        if existing eeg cap in metadata.xml, then
        EEG reference is cap reference else forehead
        :param path: path to metadata.xml file
        :param target_file: path to target file (*eeg.json)
        """
        tree = Etree.parse(path)
        root = tree.getroot()
        global value_eeg_cap
        value_eeg_cap = False
        sections = root.findall('section')

        for section in sections:
            section_name = section.find('name')
            if section_name.text == 'Devices':
                devices = section.findall('section')
                for device in devices:
                    names = device.findall('name')
                    for name in names:
                        if name.text == "EEG Cap":
                            value_eeg_cap = True

        self.update_json_file_eeg_cap(target_file, value_eeg_cap)
        return value_eeg_cap

    def read_xml_info(self, path, target_file, task_name):
        """
        read metadata.xml and get authors
        :param path: path to xml file
        :param target_file: path to target file (dataset_description.json)
        :param task_name: name of task
        """
        tree = Etree.parse(path)
        root = tree.getroot()
        global value_name
        global value_surname
        value_name = 'N/A'
        value_surname = 'N/A'
        surname_list = []
        name_list = []
        authors_list = []
        sections = root.findall('section')

        for section in sections:
            section_name = section.find('name')
            if section_name.text == 'Experimentators':
                authors = section.findall('section')
                for author in authors:
                    properties = author.findall('property')
                    for prop in properties:
                        names = prop.findall('name')
                        for name in names:
                            if name.text == "surname":
                                value = prop.find('value')
                                value_surname = value.text
                                value_surname = value_surname.strip()
                                surname_list.append(value_surname)
                            elif name.text == "givenname":
                                value = prop.find('value')
                                value_name = value.text
                                value_name = value_name.strip()
                                name_list.append(value_name)
        if len(surname_list) == len(name_list):
            i = 0
            while i < len(surname_list):
                authors_list.append(name_list[i]+' '+surname_list[i])
                i = i + 1
        self.update_json_file(target_file, task_name, authors_list)
        return authors_list

    @staticmethod
    def create_data_source_directory(path):
        """
        create sourcedata directory
        :param path: path to BIDS project
        """
        os.mkdir(path+'sourcedata')

    @staticmethod
    def create_meta_data_file():
        """
        create participants.tsv file
        """
        with open('./participants.tsv', 'wt', newline='') as out_file:
            tsv_writer = csv.writer(out_file, delimiter='\t')
            tsv_writer.writerow(['participant_id', 'age', 'sex', 'hand'])

    @staticmethod
    def read_xml_file(path, idd):
        """
        read metadata.xml and get sex, age and handedness participants
        :param path: path to xml file
        :param idd: id of experiment
        """
        global sex
        global age
        global handedness

        tree = Etree.parse(path)
        root = tree.getroot()
        sex = 'N/A'
        age = 'N/A'
        handedness = 'N/A'
        sections = root.findall('section')

        for section in sections:
            section_name = section.find('name')
            if section_name.text == 'Subject':
                properties = section.findall('property')
                for prop in properties:
                    names = prop.findall('name')
                    for name in names:
                        if name.text == "gender":
                            value = prop.find('value')
                            sex = value.text
                            sex = sex.strip()
                        elif name.text == "age":
                            value = prop.find('value')
                            age = value.text
                            age = age.strip()

        if sex == 'female':
            sex = 'F'
        elif sex == 'male':
            sex = 'M'

        with open('./participants.tsv', 'a', newline='') as out_file:
            tsv_writer = csv.writer(out_file, delimiter='\t')
            tsv_writer.writerow(['sub-'+idd, age, sex, handedness])

    @staticmethod
    def read_txt_file(file_name, idd):
        """
        read txt file and get sex, age and handedness participants
        :param file_name: path to xml file
        :param idd: id of experiment
        """
        global sex
        global age
        global handedness

        list_txt_values = open(file_name).read().split()
        i = 0
        sex = 'N/A'
        age = 'N/A'
        handedness = 'N/A'

        while i < len(list_txt_values):
            if list_txt_values[i] == 'sex:':
                sex = list_txt_values[i+1]
                if sex == 'female':
                    sex = 'F'
                elif sex == 'male':
                    sex = 'M'

            if list_txt_values[i] == 'age:':
                age = list_txt_values[i + 1]

            if list_txt_values[i] == 'handedness:':
                handedness = list_txt_values[i + 1]
                if handedness == 'right':
                    handedness = 'R'
                elif handedness == 'left':
                    handedness = 'L'
                elif handedness == 'ambidextrous':
                    handedness = 'A'
            i = i + 1

        with open('./participants.tsv', 'a', newline='') as out_file:
            tsv_writer = csv.writer(out_file, delimiter='\t')
            tsv_writer.writerow(['sub-'+idd, age, sex, handedness])

    @staticmethod
    def update_json_file(file, task_name, authors):
        """
        update dataset_description.json - set name authors
        and task name
        :param file: path to dataset_description.json
        :param task_name: task name
        :param authors: authors names
        """
        a_file = open(file, "r")

        json_object = json.load(a_file)

        a_file.close()

        json_object["Name"] = task_name
        json_object["Authors"] = authors

        a_file = open(file, "w")

        json.dump(json_object, a_file)

        a_file.close()

    @staticmethod
    def update_json_file_eeg_cap(file, eeg_cap):
        """
        set EEG reference in *eeg.json
        :param file: path to *eeg.json file
        :param eeg_cap: true to cap reference,
                        false to forehead
        :return:
        """
        a_file = open(file, "r")

        json_object = json.load(a_file)

        a_file.close()

        if eeg_cap:
            json_object["EEGReference"] = "cap reference"
        else:
            json_object["EEGReference"] = "forehead"

        a_file = open(file, "w")

        json.dump(json_object, a_file)

        a_file.close()

    @staticmethod
    def copy_xml_file(path, copy_path, name):
        """
        copy metadata.xml file to BIDS project
        :param path: path to metadata.xml (in BrainVision)
        :param copy_path: path to target (BIDS project)
        :param name: name of experiment
        """
        shutil.copy(path, copy_path)
        os.rename(copy_path+'/metadata.xml',
                  copy_path+'/'+name+'_metadata.xml')
