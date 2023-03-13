import argparse
import math
import cv2

def _build_kernel():
    """Creates the specific kernel: MORPH_ELLIPSE, MORPH_CROSS
    or MORPH_RECT"""
    kernel_size = (5, 5)
    return cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)

def _morphological_gradient(image):
    """Applies the morfological gradient to the image with
    the specified kernel type and size"""
    kernel = _build_kernel()
    morph_gradient = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)
    return morph_gradient

def find_logo(args_dict):
    input_file = args_dict["input"]
    output_file = args_dict["output"]

    # Read source image
    image_src = cv2.imread(input_file)
    # Convert it to grayscale
    image_gray = cv2.cvtColor(image_src, cv2.COLOR_BGR2GRAY)
    # Apply the morphological gradient to the image
    image_gradient = _morphological_gradient(image_gray)

    # Initialize OpenCV's static saliency spectral residual detector and
    # compute the saliency map
    saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
    (_, saliency_map) = saliency.computeSaliency(image_gradient)
    saliency_map = (saliency_map * 255).astype("uint8")

    # Apply Gaussian filtering and then Otsu's thresholding algorithm
    image_blur = cv2.GaussianBlur(saliency_map,(5,5),0)
    _, thresh_image = cv2.threshold(image_blur, 0, 255,
                                      cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    # Find contours of each high-contrast salient region
    contours, _ = cv2.findContours(thresh_image, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_TC89_KCOS)

    # Out of all contours find the closest to the center of the source image
    # by calculating the Euclidean distance between its centers
    image_output = image_src.copy()
    img_center = (image_src.shape[0] / 2, image_src.shape[1] / 2)
    dist = 999
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        center_of_contour = ((y + (h / 2)), (x + (w / 2)))

        euclid_dist = math.sqrt(pow(img_center[0] - center_of_contour[0], 2)
                      + pow(img_center[1] - center_of_contour[1], 2))
        if euclid_dist < dist:
            dist = euclid_dist
            logo_ind = i

        cv2.rectangle(image_output, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(thresh_image, (x, y), (x + w, y + h), (255, 255, 255), 2)

    x, y, w, h = cv2.boundingRect(contours[logo_ind])
    cv2.rectangle(image_output, (x, y), (x + w, y + h), (0, 255, 0), 3)
    image_logo = image_src[y:y+h, x:x+w]
    
    if not output_file:
        src_name = input_file[:input_file.rfind('.')]
        ext = input_file[input_file.rfind('.'):]
        output_contours_path = src_name + '_contours' + ext
        output_logo_path = src_name + '_logo' + ext
        cv2.imwrite(output_logo_path, image_logo)
    else:
        src_name = output_file[:output_file.rfind('.')]
        ext = output_file[output_file.rfind('.'):]
        output_contours_path = src_name + '_contours' + ext
        cv2.imwrite(output_file, image_logo)
        
    cv2.imwrite(output_contours_path, image_output)

def main():
    """Defines command line arguments and runs the program"""
    desc = 'A python script designed to find, select and save' \
           ' a region of an image containing a logo.'
    parser = argparse.ArgumentParser(description=desc)
    req_name = parser.add_argument_group('required arguments')
    msg = 'Input image file name'
    req_name.add_argument('-i', '--input', help=msg, type=str, required=True)
    msg = "Output image file name"
    parser.add_argument('-o', '--output', help=msg, type=str)
    args_dict = vars(parser.parse_args())

    find_logo(args_dict)

if __name__ == '__main__':
    main()
    