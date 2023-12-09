# Landmark-Annotator
## Prerequisites
### Python3
- If you already have downloaded python3 before, you do not have to download it again   
- If you do not have python3 installed, go to the link below and download python3 https://www.python.org/downloads/

### Download libraries
- Type the following in your `terminal`
```shell
pip3 install opencv-python argparse
```

### PNG files
If you are dealing with dicom files, you need to convert the files into PNG format. Please refer to https://github.com/yehyunsuh/DICOM-to-PNG.

## 1. When you have PNG files in `png` folder
### 1.1 How the folder should look like
```
Dicom
├─ png
└─ landmark_annotator.py
```
### 1.2 Run python file
- Type the following in your `terminal`
```shell
cd <<path to Landmark-Annotator Folder>>
python3 landmark_annotator.py
```

## 2. When you have PNG files in other folder
### 2.1 How the folder should look like
```
Dicom
├─ <<name of the png folder>>
└─ landmark_annotator.py
```
### 2.2 Run python file
- Type the following in your `terminal`
```shell
cd <<path to Landmark-Annotator Folder>>
python3 landmark_annotator.py --path <<name of the png folder>>
```
For example, if your folder name is `human_data`,
```shell
cd <<path to Landmark-Annotator Folder>>
python3 landmark_annotator.py --path human_data
```

## 3. How to annotate the markers
- `left click`: every time you do a click, there will be a red dot generated in the image and coordinates of the red dot will be extracted
- `b`: when you annotate the wrong point, press `b` and the dot will be erased
- `n`: when you are done with one image, press `n` and you can move on to the next image

- `q`: when you are done with annotating, press `q` and program will be terminated
- After executing the file, you will have a txt file that has `current date + current time + folder name.txt`

### Update on functions (2023.12.09) 
- `checkpoint`: your checkpoint will be created in `checkpoint` folder in the name of your `path`
    - Even if you restart the program, if you have already done an annoation, this program will skip the image
    - If you want to re-annotate an image that you have already annotated without using the `p` fuction, just erase the name of the image in the `checkpoint/<<name of path>>.txt` file
- `p`: when you want to go to previous image, press `p` and you can move to the previous image.  
    - If you go back to a specific image and re-annotate and move to the next images, the previous annotation will be overlapped with the new annotation
    - If you do not do any annotations, it will just skip the image without overlapping any annotations

## Acknowledgement
Most of the initial stage code has used example from https://gaussian37.github.io/vision-opencv-coordinate_extraction/.
