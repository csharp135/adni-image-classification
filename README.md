# adni-image-classification

Using the ADNI dataset containing raw MRI images, I have created a process to extract the image of the brain, normalize and segment it using the FSL toolset and Python. I have also built a CNN image classifier that focuses on the coronal axis and hippocampus regions of the brain.

## Setup
* Clone this project via: git clone https://github.com/csharp135/adni-image-classification.git
* I have saved the pre-processed images in the adni-1-5t-normalized-slices directory. However, the steps to build them are listed below in the Pre-Processing section. This step takes about 3.5 hours on a 20 CPU machine.

## Pre-Processing
* Download and install FSL from: https://fsl.fmrib.ox.ac.uk/fsl/docs/#/install/index
* The next step will ask for a kaggle id and token provided in my email. It will then download the raw MRI files, execute a series of FSL commands for each of them and save several slices of the brain scan to a PNG file. It is very CPU intensive and runs in parallel, but it will take several hours to complete. Each file takes approximately 5 minutes to run and there are 807 mri files to process. 
* From the linux command line in the adni-image-classification directory, run: _python3 python/parallel_exec_worker.py adni-1-5t-3d-human-brain-mri-raw-dataset/ADNI/ adni-1-5t-3d-human-brain-mri-raw-dataset/ADNI1_Screening_1.5T_2_20_2024.csv_
* The files are not saved in the fsl_script/image_output under the correct classification. 

## Notebook
You can run all cells in the notebook to initialize and run the model. I have documented each step as needed. 
