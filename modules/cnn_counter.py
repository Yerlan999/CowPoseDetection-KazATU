# Convolution layer parameters
image_size = (300, 200, 3)
kernel_size = (3, 3)
strides = (1, 1)
padding = 1 #   1 if zero padding "same" is applied, otherwise "valid" then 0
num_filters = 1

# Pooling layer parameters
pool_size = (2, 2)
pool_strides = (2, 2)

# Convolution layer ((W-K+2P)/S)+1
width_output_size = round((image_size[0]-kernel_size[0]+2*padding)/strides[0]+1)
height_output_size = round((image_size[1]-kernel_size[1]+2*padding)/strides[1]+1)
num_params = (kernel_size[0]*kernel_size[1]*image_size[2])*num_filters

print("After applying Convolution layer: ", width_output_size, height_output_size, image_size[2])
print("Number of parameters: ", num_params)

# Pooling layer  ((W-K)/S)+1
width_output_size = round((width_output_size-pool_size[0])/pool_strides[0]+1)
height_output_size = round((height_output_size-pool_size[1])/pool_strides[1]+1)

print("After applying Convolution layer: ", width_output_size, height_output_size, image_size[2])
print("Number of parameters: ", num_params)
