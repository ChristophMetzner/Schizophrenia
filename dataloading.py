from pathlib import Path

class subject:
    def __init__(self, subjectID):
        self.basedir = Path('C:\\Users\Kamp\Documents\SCAN\Thesis\Data')
        self.id = subjectID
        for group in ['SCZ', 'HC', 'SCZaff']:
            dir = Path(self.basedir, group, subjectID)
            if dir.exists():
                self.group = group
                self.dir = dir
                break
            else:
                print("Directory of subject" , subjectID, "not found.")
        self.tc_dir=Path(self.dir, 'rsfMRI', 'ExtractedTC')

        assert Path(self.tc_dir, 'Corr_Matrix.mat').exists(), "Correlation Matrix not found."
        self.corr_file = Path(self.tc_dir, 'Corr_Matrix.mat')

        assert Path(self.tc_dir, 'Time_Course_Matrix.mat').exists(), "Time Course Matrix missing."
        self.tc_file = Path(self.tc_dir, 'Time_Course_Matrix.mat')
        