import os
import unittest

def verify_directories_and_files(base_directory, dataset_folders):
    verification_results = {}
    for folder in dataset_folders:
        folder_path = os.path.join(base_directory, folder)
        if os.path.isdir(folder_path):
            print(f"Directory found: {folder_path}")
            # Verify that the directory is not empty
            if os.listdir(folder_path):
                verification_results[folder] = True
            else:
                print(f"Directory is empty: {folder_path}")
                verification_results[folder] = False
        else:
            print(f"Directory not found: {folder_path}")
            verification_results[folder] = False
    return verification_results

class DatasetTest(unittest.TestCase):
    def setUp(self):
        self.base_directory = "../data"
        self.dataset_folders = [
            "shrutibhargava94-india-air-quality-data",
            "rohanrao-air-quality-data-in-india",
            "abhisheksjha-time-series-air-quality-data-of-india-2010-2023",
            "fedesoriano-air-quality-data-in-india",
            "neomatrix369-air-quality-data-in-india-extended"
        ]

    def test_directories_and_files_exist(self):
        expected_results = {folder: True for folder in self.dataset_folders}
        results = verify_directories_and_files(self.base_directory, self.dataset_folders)
        self.assertEqual(results, expected_results)
        if results == expected_results:
            print("Success: All directories and files exist.")

if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
