from pathlib import Path
import numpy as np
import scipy.io

class dataset:
    """Dataset class.
    """
    def __init__(self, basedir, subject_list=""):
        """Loads complete dataset
        """
        if type(basedir) != str:
            raise Exception(f"Input error. {basedir} is no string.")
        assert Path(basedir).exists(), f"Basedirectory {basedir} not found."
        self.dir = Path(basedir)
        self.sub_list = subject_list.split()
        if len(self.sub_list) == 0:  #if no subject id is specified
            self.sub_list=[str(s)[str(s).find('sub-'):] for s in self.dir.rglob('*/sub-*')] #list of all subjects found in subdirectories

        for subjectID in self.sub_list:
            setattr(self, subjectID.replace("-","_"), subject(subjectID, basedir))

class subject:
    """Subject class.
    """
    def __init__(self, subjectID, basedir, file_dict={'Corr_Matrix':'corr_mat', 'Time_Course_Matrix':'tc'}):
        """
        Load the correct pathways to the
        """
        if type(subjectID) != str or type(basedir) != str or type(file_dict) != dict:
            raise Exception(f"Input error of {subjectID}.")

        assert Path(basedir).exists(), f"Base Directory of {subjectID} not found."
        self.basedir = Path(basedir)
        self.id = subjectID

        groups=['SCZ', 'HC', 'SCZaff']
        for group_name in groups:
            dir = Path(self.basedir, group_name, self.id)
            found_group=False
            if dir.exists():
                self.group = group_name
                self.dir = dir
                found_group=True
                break
        assert found_group, f"Group of {self.id} not found."

        for f in file_dict:
            assert list(self.dir.glob(f'**/{f}*')), f"{f} of {self.id} not found."
            setattr(self, f'{file_dict[f]}_file', list(self.dir.glob(f'**/{f}*'))[0])
            setattr(self, f'{file_dict[f]}', self.loadfile(getattr(self, f'{file_dict[f]}_file'), file_dict[f]))


    def loadfile(self, path, key):
        """
        :param file: path to .mat file that should be loaded
        :return: np.array containing data from .mat file
        """
        mat_dict = scipy.io.loadmat(path)
        assert type(mat_dict[key]) != np.array, "Matrix in .mat file not found. Consider key error"
        mat = mat_dict[key]
        return mat