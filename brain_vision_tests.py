import unittest
import brain_vision_converter


class BrainVisionTests(unittest.TestCase):

    def test(self):
        self.assertTrue(True)

    def test_next_id(self):
        self.assertEqual(brain_vision_converter.BrainVisionConverter().next_id(), 2)

    def test_search_experiment_txt(self):
        files = brain_vision_converter.BrainVisionConverter().search_experiment_txt('./Testing/BrainVision')
        self.assertEqual(files[0],
                         './Testing\\BrainVision\\Experiment_341_P3_Numbers\\Data\\P3Numbers_20150618_f_10_001.txt')
        self.assertEqual(len(files), 1)

    def test_search_metadata_xml(self):
        files = brain_vision_converter.BrainVisionConverter().search_metadata_xml(
            './Testing/BrainVision/Experiment_341_P3_Numbers/Data/P3Numbers_20150618_f_10_001.vhdr')
        self.assertEqual(files[0],
                         './Testing/BrainVision\\Experiment_341_P3_Numbers\\metadata.xml')
        self.assertEqual(len(files), 1)

    def test_search_eeg_vhdr(self):
        files = brain_vision_converter.BrainVisionConverter().search_eeg_vhdr('./Testing/dataset/sub-10')
        self.assertEqual(files[0],
                         './Testing/dataset/sub-10\\eeg\\sub-10_eeg.vhdr')
        self.assertEqual(len(files), 1)


if __name__ == '__main__':
    unittest.main()
