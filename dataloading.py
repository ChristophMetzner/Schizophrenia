from pathlib import Path
import numpy as np
import scipy.io

class subject:
    """Dataset class.
    """
    def __init__(self, subjectID, basedir):
        """
        Load the correct pathways to the
        """

        assert Path(basedir).exists(), "Base Directory not found."
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

        assert list(self.dir.glob('**/Time_Course_Mat*')), f"Time Course Matrix of {self.id} not found."
        self.tc_file = list(self.dir.glob('**/Time_Course_Mat*'))[0]

        assert list(self.dir.glob('**/Corr_Mat*')), f"Correlation Matrix of {self.id} not found."
        self.corr_file=list(self.dir.glob('**/Corr_Mat*'))[0]

        self.Tcourses = self.loadfile(self.tc_file)
        self.Cmat = self.loadfile(self.corr_file)

    def loadfile(self, path):
        """
        :param file: path to .mat file that should be loaded
        :return: array with the data from .mat file
        """

        if str(path).find('Corr_Mat') != -1:    #Checks which file is loaded and creates key
            key='corr_mat'
        elif str(path).find('Time_Course_Mat') != -1:
            key='tc'

        mat_dict = scipy.io.loadmat(path)
        mat = np.array(mat_dict[key])
        return mat