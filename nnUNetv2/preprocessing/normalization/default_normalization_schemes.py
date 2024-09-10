from abc import ABC, abstractmethod
from typing import Type

import numpy as np
from numpy import number

# WP
from skimage import exposure
from skimage.filters import threshold_otsu
from scipy.ndimage import binary_dilation

from dipy.denoise.nlmeans import nlmeans
from dipy.denoise.noise_estimate import estimate_sigma

class ImageNormalization(ABC):
    leaves_pixels_outside_mask_at_zero_if_use_mask_for_norm_is_true = None

    def __init__(self, use_mask_for_norm: bool = None, intensityproperties: dict = None,
                 target_dtype: Type[number] = np.float32):
        assert use_mask_for_norm is None or isinstance(use_mask_for_norm, bool)
        self.use_mask_for_norm = use_mask_for_norm
        assert isinstance(intensityproperties, dict)
        self.intensityproperties = intensityproperties
        self.target_dtype = target_dtype

    @abstractmethod
    def run(self, image: np.ndarray, seg: np.ndarray = None) -> np.ndarray:
        """
        Image and seg must have the same shape. Seg is not always used
        """
        pass


class ZScoreNormalization(ImageNormalization):
    leaves_pixels_outside_mask_at_zero_if_use_mask_for_norm_is_true = True

    def run(self, image: np.ndarray, seg: np.ndarray = None) -> np.ndarray:
        """
        here seg is used to store the zero valued region. The value for that region in the segmentation is -1 by
        default.
        """
        image = image.astype(self.target_dtype, copy=False)
        if self.use_mask_for_norm is not None and self.use_mask_for_norm:
            # negative values in the segmentation encode the 'outside' region (think zero values around the brain as
            # in BraTS). We want to run the normalization only in the brain region, so we need to mask the image.
            # The default nnU-net sets use_mask_for_norm to True if cropping to the nonzero region substantially
            # reduced the image size.
            mask = seg >= 0
            mean = image[mask].mean()
            std = image[mask].std()
            image[mask] = (image[mask] - mean) / (max(std, 1e-8))
        else:
            mean = image.mean()
            std = image.std()
            image -= mean
            image /= (max(std, 1e-8))
        return image

#WP
class T1wPVSNormalization(ImageNormalization):
    leaves_pixels_outside_mask_at_zero_if_use_mask_for_norm_is_true = True

    def run(self, image: np.ndarray, seg: np.ndarray = None) -> np.ndarray:
        """
        here seg is used to store the zero valued region. The value for that region in the segmentation is -1 by
        default.
        
        image = image.astype(self.target_dtype, copy=False)
        if self.use_mask_for_norm is not None and self.use_mask_for_norm:
            # negative values in the segmentation encode the 'outside' region (think zero values around the brain as
            # in BraTS). We want to run the normalization only in the brain region, so we need to mask the image.
            # The default nnU-net sets use_mask_for_norm to True if cropping to the nonzero region substantially
            # reduced the image size.
            mask = seg >= 0
            #mean = image[mask].mean()
            #std = image[mask].std()
            #image[mask] = (image[mask] - mean) / (max(std, 1e-8))
        else:
            #mean = image.mean()
            #std = image.std()
            #image -= mean
            #image /= (max(std, 1e-8))
        """
        #WP: 1. otsu mask, 2. 
        thresh = threshold_otsu(image)
        mask = image > thresh
        mask = binary_dilation(mask, iterations=5)
        cleaned_image = np.where(mask, image, 0)
        
        min_brain_intensity = np.min(cleaned_image[np.where(cleaned_image!=0)])
        max_brain_intensity = np.max(cleaned_image[np.where(cleaned_image!=0)])
        
        cleaned_image[cleaned_image<min_brain_intensity] = min_brain_intensity
        cleaned_image[cleaned_image>max_brain_intensity] = max_brain_intensity
        p1, p2 = np.percentile(cleaned_image, (2,98))
        
        mask = cleaned_image > 0#p1
        cleaned_image = exposure.rescale_intensity(cleaned_image, in_range=(p1, p2))
        
        sigma = estimate_sigma(cleaned_image)
        sigma = sigma/2
        #print(sigma)
        
        image = nlmeans(cleaned_image, mask=mask, sigma=sigma, patch_radius=1,block_radius=2, rician=True)
        image = exposure.equalize_adapthist(image)
        return image

#WP
class AHENormalization(ImageNormalization):
    leaves_pixels_outside_mask_at_zero_if_use_mask_for_norm_is_true = True

    def run(self, image: np.ndarray, seg: np.ndarray = None) -> np.ndarray:
        """
        here seg is used to store the zero valued region. The value for that region in the segmentation is -1 by
        default.
        
        image = image.astype(self.target_dtype, copy=False)
        if self.use_mask_for_norm is not None and self.use_mask_for_norm:
            # negative values in the segmentation encode the 'outside' region (think zero values around the brain as
            # in BraTS). We want to run the normalization only in the brain region, so we need to mask the image.
            # The default nnU-net sets use_mask_for_norm to True if cropping to the nonzero region substantially
            # reduced the image size.
            mask = seg >= 0
            #mean = image[mask].mean()
            #std = image[mask].std()
            #image[mask] = (image[mask] - mean) / (max(std, 1e-8))
        else:
            #mean = image.mean()
            #std = image.std()
            #image -= mean
            #image /= (max(std, 1e-8))
        """
        #WP: 1. otsu mask, 2. 
        thresh = threshold_otsu(image)
        mask = image > thresh
        mask = binary_dilation(mask, iterations=5)
        cleaned_image = np.where(mask, image, 0)
        
        min_brain_intensity = np.min(cleaned_image[np.where(cleaned_image!=0)])
        max_brain_intensity = np.max(cleaned_image[np.where(cleaned_image!=0)])
        
        cleaned_image[cleaned_image<min_brain_intensity] = min_brain_intensity
        cleaned_image[cleaned_image>max_brain_intensity] = max_brain_intensity
        p1, p2 = np.percentile(cleaned_image, (2,98))
        
        mask = cleaned_image > 0#p1
        cleaned_image = exposure.rescale_intensity(cleaned_image, in_range=(p1, p2))
        
        sigma = estimate_sigma(cleaned_image)
        sigma = sigma/2
        #print(sigma)
        
        #image = nlmeans(cleaned_image, mask=mask, sigma=sigma, patch_radius=1,block_radius=2, rician=True)
        image = exposure.equalize_adapthist(cleaned_image)
        return image

#WP
class NLMFNormalization(ImageNormalization):
    leaves_pixels_outside_mask_at_zero_if_use_mask_for_norm_is_true = True

    def run(self, image: np.ndarray, seg: np.ndarray = None) -> np.ndarray:
        """
        here seg is used to store the zero valued region. The value for that region in the segmentation is -1 by
        default.
        
        image = image.astype(self.target_dtype, copy=False)
        if self.use_mask_for_norm is not None and self.use_mask_for_norm:
            # negative values in the segmentation encode the 'outside' region (think zero values around the brain as
            # in BraTS). We want to run the normalization only in the brain region, so we need to mask the image.
            # The default nnU-net sets use_mask_for_norm to True if cropping to the nonzero region substantially
            # reduced the image size.
            mask = seg >= 0
            #mean = image[mask].mean()
            #std = image[mask].std()
            #image[mask] = (image[mask] - mean) / (max(std, 1e-8))
        else:
            #mean = image.mean()
            #std = image.std()
            #image -= mean
            #image /= (max(std, 1e-8))
        """
        #WP: 1. otsu mask, 2. 
        thresh = threshold_otsu(image)
        mask = image > thresh
        mask = binary_dilation(mask, iterations=5)
        cleaned_image = np.where(mask, image, 0)
        
        min_brain_intensity = np.min(cleaned_image[np.where(cleaned_image!=0)])
        max_brain_intensity = np.max(cleaned_image[np.where(cleaned_image!=0)])
        
        cleaned_image[cleaned_image<min_brain_intensity] = min_brain_intensity
        cleaned_image[cleaned_image>max_brain_intensity] = max_brain_intensity
        p1, p2 = np.percentile(cleaned_image, (2,98))
        
        mask = cleaned_image > 0#p1
        cleaned_image = exposure.rescale_intensity(cleaned_image, in_range=(p1, p2))
        
        sigma = estimate_sigma(cleaned_image)
        sigma = sigma/2
        #print(sigma)
        
        image = nlmeans(cleaned_image, mask=mask, sigma=sigma, patch_radius=1,block_radius=2, rician=True)
        #image = exposure.equalize_adapthist(image)
        return image

class CTNormalization(ImageNormalization):
    leaves_pixels_outside_mask_at_zero_if_use_mask_for_norm_is_true = False

    def run(self, image: np.ndarray, seg: np.ndarray = None) -> np.ndarray:
        assert self.intensityproperties is not None, "CTNormalization requires intensity properties"
        mean_intensity = self.intensityproperties['mean']
        std_intensity = self.intensityproperties['std']
        lower_bound = self.intensityproperties['percentile_00_5']
        upper_bound = self.intensityproperties['percentile_99_5']

        image = image.astype(self.target_dtype, copy=False)
        np.clip(image, lower_bound, upper_bound, out=image)
        image -= mean_intensity
        image /= max(std_intensity, 1e-8)
        return image


class NoNormalization(ImageNormalization):
    leaves_pixels_outside_mask_at_zero_if_use_mask_for_norm_is_true = False

    def run(self, image: np.ndarray, seg: np.ndarray = None) -> np.ndarray:
        return image.astype(self.target_dtype, copy=False)


class RescaleTo01Normalization(ImageNormalization):
    leaves_pixels_outside_mask_at_zero_if_use_mask_for_norm_is_true = False

    def run(self, image: np.ndarray, seg: np.ndarray = None) -> np.ndarray:
        image = image.astype(self.target_dtype, copy=False)
        image -= image.min()
        image /= np.clip(image.max(), a_min=1e-8, a_max=None)
        return image


class RGBTo01Normalization(ImageNormalization):
    leaves_pixels_outside_mask_at_zero_if_use_mask_for_norm_is_true = False

    def run(self, image: np.ndarray, seg: np.ndarray = None) -> np.ndarray:
        assert image.min() >= 0, "RGB images are uint 8, for whatever reason I found pixel values smaller than 0. " \
                                 "Your images do not seem to be RGB images"
        assert image.max() <= 255, "RGB images are uint 8, for whatever reason I found pixel values greater than 255" \
                                   ". Your images do not seem to be RGB images"
        image = image.astype(self.target_dtype, copy=False)
        image /= 255.
        return image
