import unittest
from os import path, rmdir, remove

import metadata_transform


class MetadataTransformTests(unittest.TestCase):

    def test(self):
        self.assertTrue(True)

    def test_create_data_source_directory(self):
        metadata_transform.MetadataConvert().create_data_source_directory('./')
        self.assertTrue(path.exists('./sourcedata'))
        rmdir('./sourcedata')

    def test_create_meta_data_file(self):
        metadata_transform.MetadataConvert().create_meta_data_file()
        self.assertTrue(path.exists('./participants.tsv'))
        remove('./participants.tsv')


if __name__ == '__main__':
    unittest.main()
