## ImageStacks
**Summary:** Imports non-DICOM image sequences (TIF/PNG/JPG/BMP) into 3D Slicer. `ImageStacks` offers additional features such as quickly previewing large datasets at very low resolution, specifying an ROI to import only a subset of the data, downsampling, skipping slice(s) along the Z plane, and reverse the stack order. Users can also specify the voxel spacing for their dataset at the import time. Unlike the volume generated by the Slicer's default Load Data mechanism, `ImageStacks` always produces a ScalarVolume (single channel), so that volumes can be immediately visualized or can be processed with `Segment Editor`.

### USAGE

#### Input Files
If you want to load all the images in a folder, drag either the folder or a single image from the folder onto the main Slicer application window. A popup message will ask if you want to use the `ImageStacks` module to load the data. File list table will be populated after accepting to use `ImageStacks`.

**Filename Pattern:** If the folder contains multiple image stacks with different conventions, **Filename Pattern** option can be used to pick one sample file, which will be used to automatically select and order all files that use the same convention.   

**Size:** Reports the image dimensions and data type of the files currently selected along with its estimated memory usage at full resolution.

**Reverse:** If checked, it will reverse the ordering of files. This is useful to mitigate the mirror reflection problem of the specimens due to unknown nature of slice ordering (top to bottom vs bottom to top).

**Spacing:** This specifies the voxel spacing in each axis. Note that unless changed by users, default unit in Slicer and SlicerMorph is millimeters. Values should be entered accordingly. (e.g., 15 micrometer should be entered as 0.015). Always cross-check the values reported here with known pixel spacing of the dataset. 2D formats may not store this value correctly.  

#### Output

**Output Volume:** If left as _(Create New Volume)_, the very first file in file selection will be used as the output volume node name. Alternatively, users create their own volume names using **Create New Volume As** option

**Region of Interest:** By default this is set to full extend of the volume _(Full Volume)_. Alternatively, users can specify a ROI to import only a subset of the volume.

**Quality:** There are three presets options: **Preview:** downsamples dataset by 4 in each axis (64 folds reduction in data volume); **Half resolution:** downsamples dataset by 2 in each axis (8 folds reduction in data volume); **Full Volumes:** does not modify the resolution. 

**Slice skip:** Allows alternatively to import only every (N+1)th slice to further downsample the volume. 0 means no skipping slice. 

**Grayscale:** Force output image to be grayscale (single scalar component). This is particularly useful when grayscale images are stored using RGB (or RGBA) voxels. Most processing and analysis algorithms require grayscale input, therefore it is recommended to enable this option.

**Output Size:** Reports the image dimensions and data type of the files along with its estimated memory usage at the specified quality setting.

**Output Spacing:** Reports the image spacing of the output volume at the specified quality setting.

### USAGE SUGGESTIONS and CONSIDERATIONS
MicroCT scans of whole specimens can contain regions of black space, or the user many not be interested in the entire content of the volume. In such cases, Preview quality allows for very fast import and exploration the data. After importing the full extend of the data in preview quality, user can draw a Region of Interest (ROI) to only import the region they are interested. After drawing the ROI, go back to `ImageStacks` output options, set the **Region of Interest** to the newly created ROI, and then change the quality to desired output (e.g., Full Volume). This will import only the region within the ROI at the full resolution of the data. 

### TUTORIAL
Please see https://github.com/SlicerMorph/Tutorials/tree/main/ImageStacks

[A video tutorial of ImageStacks module highlighting preview and ROI selection functionality](https://www.youtube.com/watch?v=tjZUOqnrc_Y&t=2s)



