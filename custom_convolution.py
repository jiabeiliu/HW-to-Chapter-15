import numpy as np

def depthwise_convolution(image, kernel):
    """
    Performs depthwise convolution on a multi-channel image.
    Each channel in the image is convolved with its corresponding kernel.
    """
    # Initialize output with the same spatial dimensions as input
    output = np.zeros((image.shape[0] - kernel.shape[1] + 1, 
                       image.shape[1] - kernel.shape[2] + 1, 
                       image.shape[2]))

    # Apply convolution for each channel independently
    for c in range(image.shape[2]):
        for i in range(output.shape[0]):
            for j in range(output.shape[1]):
                region = image[i:i+kernel.shape[1], j:j+kernel.shape[2], c]
                output[i, j, c] = np.sum(region * kernel[c])

    return output

def pointwise_convolution(image, kernel):
    """
    Performs pointwise convolution on a multi-channel image.
    Uses a 1x1 filter across all input channels to produce each output channel.
    """
    output_height, output_width, _ = image.shape
    output_channels = kernel.shape[3]
    output = np.zeros((output_height, output_width, output_channels))

    # Perform pointwise convolution (1x1 filter across channels)
    for oc in range(output_channels):
        for i in range(output_height):
            for j in range(output_width):
                region = image[i, j, :]
                output[i, j, oc] = np.sum(region * kernel[:, :, :, oc])

    return output

def convolution(image, kernel, mode='depthwise'):
    """
    Perform either depthwise or pointwise convolution based on the mode.
    """
    if mode == 'depthwise':
        return depthwise_convolution(image, kernel)
    elif mode == 'pointwise':
        return pointwise_convolution(image, kernel)
    else:
        raise ValueError("Invalid mode. Choose 'depthwise' or 'pointwise'.")

# Example Usage
# Define a 4x4x3 image (3 channels, e.g., RGB)
image = np.array([
    [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 2, 3]],
    [[4, 5, 6], [7, 8, 9], [1, 2, 3], [4, 5, 6]],
    [[7, 8, 9], [1, 2, 3], [4, 5, 6], [7, 8, 9]],
    [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 2, 3]]
])

# Define a 3x3 depthwise kernel (one 3x3 filter per channel)
depthwise_kernel = np.array([
    [[1, 0, -1], [1, 0, -1], [1, 0, -1]],  # Channel 1
    [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]],  # Channel 2
    [[1, 1, 1], [0, 0, 0], [-1, -1, -1]]   # Channel 3
])

# Define a 1x1x3x2 pointwise kernel (3 input channels, 2 output channels)
pointwise_kernel = np.array([
    [[[1, 0.5]], [[0.5, 1]], [[1, 0.5]]]
])

# Run depthwise convolution
depthwise_output = convolution(image, depthwise_kernel, mode='depthwise')
print("Depthwise Convolution Output:\n", depthwise_output)

# Run pointwise convolution
pointwise_output = convolution(image, pointwise_kernel, mode='pointwise')
print("Pointwise Convolution Output:\n", pointwise_output)
