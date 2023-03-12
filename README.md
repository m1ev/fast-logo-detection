# fast-logo-detection
<h2>Description</h2>
A python script designed to find, select and save a region of an image containing a logo.<br/><br/>
The image can be a photo of a t-shirt, hoodie, sweatshirt, cap, cup or any other item with a logo on it.<br/>
For an acceptable performance it is required that the logo:
<br/><br/>
<ul>
<li>is located near the center of the image</li>
<li>stands out on a monotone background</li>
<li>doesn't contain elements that are located too far apart from each other</li>
</ul>

The main idea of the implemented method is to find salient regions in the selected image, which can be described as the regions that could present the main meaningful or semantic contents and choose the one closest to the center of the image.

<h2>Usage</h2>
<h3>From the command line</h3>

`fast_logo_detection.py --help`

```
usage: fast_logo_detection.py [-h] -i INPUT [-o OUTPUT]

A python script designed to find, select and save a region of an image
containing a logo.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output image file name

required arguments:
  -i INPUT, --input INPUT
                        Input image file name
```

<h2>The basic idea</h2>

1. Select an image<br/><br/>
![Example #1_1](/readme_assets/ex1_1.jpg?raw=true)

2. Convert it to grayscale<br/><br/>
![Example #1_2](/readme_assets/ex1_2.jpg?raw=true)

3. Apply the morphological gradient<br/><br/>
![Example #1_3](/readme_assets/ex1_3.jpg?raw=true)

5. Generate the saliency map<br/><br/>
![Example #1_4](/readme_assets/ex1_4.jpg?raw=true)

7. Apply Gaussian filtering and a thresholding algorithm<br/><br/>
![Example #1_5](/readme_assets/ex1_5.jpg?raw=true)

9. Out of all generated regions find the closest to the center of the source image<br/><br/>
![Example #1_6](/readme_assets/ex1_6.jpg?raw=true)
![Example #1_7](/readme_assets/ex1_7.jpg?raw=true)

<h2>Examples</h2>

![Example #2](/readme_assets/ex2.jpg?raw=true)

![Example #3](/readme_assets/ex3.jpg?raw=true)

![Example #4](/readme_assets/ex4.jpg?raw=true)

![Example #5](/readme_assets/ex5.jpg?raw=true)

![Example #6](/readme_assets/ex6.jpg?raw=true)

