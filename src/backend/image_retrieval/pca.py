import numpy as np

def compute_pca(images, num_components):
    U, S, Vt = np.linalg.svd(images, full_matrices=False)
    U_k = U[:, :num_components]
    Vt_k = Vt[:num_components, :]
    return U_k, S[:num_components], Vt_k
