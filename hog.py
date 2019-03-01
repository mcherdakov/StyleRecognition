import numpy as np
from sklearn import svm
from scipy import misc

eps = 0.000001

def find_gradient(img):
    h, w = len(img), len(img[0])

    brightness = img[:, :, 0] * 0.299 + img[:, :, 1] * 0.587 \
                + img[:, :, 2] * 0.114
            
    partial_x = np.zeros((h, w))
    partial_y = np.zeros((h, w))
    
    for i in range(h):
        for j in range(w):
            if j == 0:
                partial_x[i][j] = brightness[i][1] - brightness[i][0]
            elif j == w - 1:
                partial_x[i][j] = brightness[i][j] - brightness[i][j - 1]
            else:
                partial_x[i][j] = brightness[i][j + 1] - brightness[i][j - 1]
            if i == 0:
                partial_y[i][j] = brightness[1][j] - brightness[0][j]
            elif i == h - 1:
                partial_y[i][j] = brightness[i][j] - brightness[i - 1][j]
            else:
                partial_y[i][j] = brightness[i + 1][j] - brightness[i - 1][j]
    
    energy = ((partial_x ** 2 + partial_y ** 2) ** 0.5).astype(dtype='float32')
    direction = np.arctan2(partial_x, partial_y).astype(dtype='float32')
    
    return energy, direction


def make_bracket(cell_grad, cell_dir):
    flat_grad, flat_dir = cell_grad.ravel(), cell_dir.ravel()
    
    pi = np.pi
    bins = np.linspace(-pi * 9 / 8, pi * 9 / 8, 10)
    inds = np.digitize(flat_dir, bins, right=False)
    bracket = np.bincount(inds - 1, minlength=10, weights=flat_grad)
    
    return bracket

def extract_hog(img):
    gradient, direction = find_gradient(img)
    h, w = img.shape[0], img.shape[1]
    cell_h, cell_w = h // 8, w // 8
    up_space, left_space = (h % 8) // 2, (w % 8) // 2
    
    descriptor = np.zeros((0))
    for i in range(7):
        for j in range(7):
            current = np.zeros((0))
            start_h = up_space + i * cell_h
            start_w = left_space + j * cell_w
        
            for row in range(2):
                for col in range(2):
                    change_h = start_h + row * cell_h
                    change_w = start_w + col * cell_w
                    bracket = make_bracket( \
                        gradient[change_h:change_h + cell_h + 1, \
                                 change_w:change_w + cell_w + 1], \
                        direction[change_h:change_h + cell_h + 1, \
                                 change_w:change_w + cell_w + 1])
                    
                    bracket = bracket / (eps + (bracket ** 2).sum()) ** 0.5
                    current = np.concatenate([current, bracket])
            
            descriptor = np.concatenate([descriptor, current])
            
    return descriptor
