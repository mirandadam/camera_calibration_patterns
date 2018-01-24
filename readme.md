Camera Calibration Patterns
=

## Introduction

This code produces patterns for camera calibration in vector format (SVG, PDF) and PNG.

The patterns are regular arrangements of circles and squares of multiple sizes that can be used for geometric calibration, point spread function (PSF) modeling and chromatic aberration modeling of a camera.

The printed patterns can be photographed with a target camera and the images can be processed using primitives such as circle detectors (OpenCV Hough Circles, for example) and corner detectors (OpenCV cornerHarris with cornerSubPix, for example).

Once the pattern is located, a "ground truth" image can be generated with the correct perspective and distortions. The pattern logical structure or even the sample file itself can be used for generating the ground truth. Camera parameters such as orientation, focal distance, PSF and distortions can be iterated to try to find the correct parameters for the camera.

## Caveats

* You need Inkscape installed to convert the SVG files to PNG and PDF. Comment the last part of the code if you don't have Inkscape installed or wish to generate only SVGs. Adjust the path accordingly if your Inkscape is in a different location.

* The image processing step is not implemented. At this time you have to code your own.

* When generating your own targets, be careful with the detail level. A good rule of thumb is to keep it between 2 and 5. The file size and the program run time increase roughly with 3 to the power of N where N is the detail level. After a certain point the detail becomes indistinguishable in the prints or in the pictures themselves.

* A template for A4 paper is provided. For other paper sizes, adjust the SVG template accordingly. Pull requests are appreciated!
