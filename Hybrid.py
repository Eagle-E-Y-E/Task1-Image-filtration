import numpy as np

class Hybrid:
    @staticmethod
    def generate_gaussian_kernel(size, sigma):
        ax = np.arange(-size // 2 + 1., size // 2 + 1.)
        xx, yy = np.meshgrid(ax, ax)
        kernel = np.exp(-(xx**2 + yy**2) / (2. * sigma**2))
        kernel = kernel / np.sum(kernel)
        return kernel

    @staticmethod
    def convolve_image(image, kernel):
        # Ensure kernel is a NumPy array
        kernel = np.array(kernel)
        k_size = kernel.shape[0]
        pad = k_size // 2

        # Pad the image manually using NumPy
        if len(image.shape) == 2:
            # Grayscale image
            image_padded = np.pad(image, pad, mode='constant', constant_values=0)
            height, width = image.shape
            channels = 1
        else:
            # Color image
            image_padded = np.pad(image, ((pad, pad), (pad, pad), (0, 0)), mode='constant', constant_values=0)
            height, width, channels = image.shape

        # Prepare an empty array for the convolved image
        convolved_image = np.zeros_like(image, dtype=np.float32)

        # Flip the kernel (convolution operation)
        kernel_flipped = np.flipud(np.fliplr(kernel))

        # Vectorized convolution operation
        for c in range(channels):
            for i in range(height):
                for j in range(width):
                    # Extract the region of interest
                    if channels == 1:
                        region = image_padded[i:i+k_size, j:j+k_size]
                    else:
                        region = image_padded[i:i+k_size, j:j+k_size, c]

                    # Perform element-wise multiplication and sum the result
                    convolved_value = np.sum(region * kernel_flipped)
                    convolved_image[i, j] = convolved_value if channels == 1 else convolved_value

        # If the image has multiple channels, stack them back together
        return convolved_image

    @staticmethod
    def extract_low_frequencies(image, kernel_size = 15, sigma = 5):
        print(kernel_size)
        print(sigma)
        gaussian_kernel = Hybrid.generate_gaussian_kernel(kernel_size, sigma)
        low_frequencies = Hybrid.convolve_image(image, gaussian_kernel)
        return low_frequencies

    @staticmethod
    def extract_high_frequencies(image, kernel_size = 15, sigma = 5):
        low_frequencies = Hybrid.extract_low_frequencies(image, kernel_size=kernel_size, sigma=sigma)
        high_frequencies = image - low_frequencies
        return high_frequencies

    
    @staticmethod
    def combine_frequencies(low_freq_image, high_freq_image):
        hybrid_image = low_freq_image + high_freq_image

        # Clip values to valid range [0, 255]
        hybrid_image = np.clip(hybrid_image, 0, 255)
        return hybrid_image

