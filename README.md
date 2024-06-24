# BT-23_24

## Summary and Instructions for GitHub Repository
This repository contains the code developed as part of the Bachelor Thesis conducted during the course 2023-2024. The code is designed to streamline a pool of synthetic patients through a theoretically optimized CAD diagnosing process. It includes a GUI intended for clinicians, integrating some steps (the ones not running in the background) of this optimized process.

### How to Use the Code
#### 1. Download the Full Code:
- Download the entire 'Code' directory from the repository.
- Ensure not to move any files or folders from 'Code' to avoid directory issues.

#### 2. Running the GUI:
- Run the Python script GUI_script.py.
- You will be prompted for a username and password (simulating clinician login).
- Enter the following credentials:
  - **User:** test
  - **Password:** password

*Note: This user type has permission to perform all actions available in the interface.*
- Click enter and follow the different interface flows.

### Data for Testing
Some data (images) necessary to test this code at its fullest is either not available or cannot be uploaded due to storage constraints.
#### 1. Curved Multi-Planar Reformations (cMPRs):
- The cMPRs images were extracted from anonymized patient data and cannot be uploaded due to data protection policies.
- To test this feature:
  - Obtain screenshots of cMPRs of coronary vessels for the following stenosis ranges: 0%, 1-24%, 25-49%, 50-69%, 70-99%, and 100%.
  - Create a new folder inside the 'Code' directory called 'CPR'.
  - Save each screenshot in the 'CPR' folder with the following names for the stenosis ranges presented above, respectively: 'noCAD.png', 'minimalCAD.png', 'mildCAD.png', 'moderateCAD.png', 'severeCAD.png', 'obstructiveCAD.png'.

#### 2. Original CCTA Image and Segmentation:
- These images can be obtained from the public database ASOCA (https://asoca.grand-challenge.org/access/).
- The images used are from the Case 1 Normal of the ASOCA database:
  - **Original CCTA:** Normal/CTCA/Normal_1.nrrd
  - **CCTA Segmentation:** Normal/Annotations/Normal_1.nrrd
- Convert these from .nrrd to .nii format using the following code:

      import SimpleITK as sitk
      
      img = sitk.ReadImage("Normal_1.nrrd")
      
      sitk.WriteImage(img, "Normal_1.nii.gz")

- Save the converted images as follows:
  - **Original CCTA Image:**
    - Inside the 'Code' folder exists another folder named 'Case1_ASOCA'.
    - Inside 'Case1_ASOCA', create a new folder named 'Test_nifti.nii'.
    - Place the NIfTI archive generated from the original CCTA image in the folder 'Test_nifti.nii'. This NIfTI archive should be named 'Test_nifti.nii'.
  - **CCTA Segmentation:**
    - Inside the 'Code' folder, create a new folder named 'Normal_1_segmentation.nii'.
    - Place the NIfTI archive generated from the coronary arteries segmentation in the folder 'Normal_1_segmentation.nii'. This NIfTI archive should be named 'Normal_1 (1).nii'.
