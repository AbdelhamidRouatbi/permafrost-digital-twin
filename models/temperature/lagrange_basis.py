import numpy as np

def lagrange_basis(elem_type, coord, dim=1):

    # Ensure coord is a NumPy array for indexing
    coord = np.asarray(coord)
    
    # Initialize N and dNdxi for the different element types.
    if elem_type == 'L2':
        # L2 TWO NODE LINE ELEMENT
        if coord.size < 1:
            print("Error coordinate needed for the L2 element")
            N = np.array([])
            dNdxi = np.array([])
        else:
            xi = coord[0]
            N = np.array([(1 - xi) / 2, (1 + xi) / 2])
            dNdxi = np.array([-1, 1]) / 2

    elif elem_type == 'L3':
        # L3 THREE NODE LINE ELEMENT
        if coord.size < 1:
            print("Error coordinate needed for the L3 element")
            N = np.array([])
            dNdxi = np.array([])
        else:
            xi = coord[0]
            N = np.array([xi*(xi - 1)/2,
                          (1 + xi)*(1 - xi),
                          xi*(xi + 1)/2])
            dNdxi = np.array([xi - 0.5, -2*xi, xi + 0.5])

    elif elem_type in ['T3', 'T3fs']:
        # T3 and T3fs THREE NODE TRIANGULAR ELEMENT
        if coord.size < 2:
            print("Error two coordinates needed for the T3 element")
            N = np.array([])
            dNdxi = np.array([])
        else:
            xi, eta = coord[0], coord[1]
            N = np.array([1 - xi - eta, xi, eta])
            dNdxi = np.array([[-1, -1],
                              [ 1,  0],
                              [ 0,  1]])

    elif elem_type == 'T4':
        # T4 FOUR NODE TRIANGULAR CUBIC BUBBLE ELEMENT
        if coord.size < 2:
            print("Error two coordinates needed for the T4 element")
            N = np.array([])
            dNdxi = np.array([])
        else:
            xi, eta = coord[0], coord[1]
            N = np.array([1 - xi - eta - 3*xi*eta,
                          xi*(1 - 3*eta),
                          eta*(1 - 3*xi),
                          9*xi*eta])
            dNdxi = np.array([[-1 - 3*eta,   -1 - 3*xi],
                              [ 1 - 3*eta,   -3*xi],
                              [   -3*eta,  1 - 3*xi],
                              [     9*eta,     9*xi]])

    elif elem_type == 'T6':
        # T6 SIX NODE TRIANGULAR ELEMENT
        if coord.size < 2:
            print("Error two coordinates needed for the T6 element")
            N = np.array([])
            dNdxi = np.array([])
        else:
            xi, eta = coord[0], coord[1]
            N = np.array([
                1 - 3*(xi + eta) + 4*xi*eta + 2*(xi**2 + eta**2),
                xi*(2*xi - 1),
                eta*(2*eta - 1),
                4*xi*(1 - xi - eta),
                4*xi*eta,
                4*eta*(1 - xi - eta)
            ])
            dNdxi = np.array([
                [4*(xi + eta) - 3,      4*(xi + eta) - 3],
                [4*xi - 1,                      0],
                [       0,              4*eta - 1],
                [4*(1 - eta - 2*xi),           -4*xi],
                [       4*eta,                 4*xi],
                [      -4*eta,         4*(1 - xi - 2*eta)]
            ])

    elif elem_type == 'Q4':
        # Q4 FOUR NODE QUADRILATERAL ELEMENT
        if coord.size < 2:
            print("Error two coordinates needed for the Q4 element")
            N = np.array([])
            dNdxi = np.array([])
        else:
            xi, eta = coord[0], coord[1]
            N = 1/4 * np.array([
                (1 - xi) * (1 - eta),
                (1 + xi) * (1 - eta),
                (1 + xi) * (1 + eta),
                (1 - xi) * (1 + eta)
            ])
            dNdxi = 1/4 * np.array([
                [-(1 - eta), -(1 - xi)],
                [ 1 - eta,   -(1 + xi)],
                [ 1 + eta,    1 + xi],
                [-(1 + eta),   1 - xi]
            ])

    elif elem_type == 'Q8':
        # Q8 EIGHT NODE QUADRILATERAL ELEMENT (labeled Q9 in the MATLAB code)
        if coord.size < 2:
            print("Error two coordinates needed for the Q9 element")
            N = np.array([])
            dNdxi = np.array([])
        else:
            xi, eta = coord[0], coord[1]
            N = 1/4 * np.array([
                (1 - xi) * (1 - eta) * (-xi - eta - 1),
                (1 + xi) * (1 - eta) * ( xi - eta - 1),
                (1 + xi) * (1 + eta) * ( xi + eta - 1),
                (1 - xi) * (1 + eta) * (-xi + eta - 1),
                2 * (1 - xi**2) * (1 - eta),
                2 * (1 - eta**2) * (1 + xi),
                2 * (1 - xi**2) * (1 + eta),
                2 * (1 - eta**2) * (1 - xi)
            ])
            dNdxi = 1/4 * np.array([
                [-(1 - eta)*(-xi - eta - 1) - (1 - xi)*(1 - eta),
                 -(1 - xi)*(-xi - eta - 1) - (1 - xi)*(1 - eta)],
                [(1 - eta)*( xi - eta - 1) + (1 + xi)*(1 - eta),
                 -(1 + xi)*( xi - eta - 1) - (1 + xi)*(1 - eta)],
                [(1 + eta)*( xi + eta - 1) + (1 + xi)*(1 + eta),
                 (1 + xi)*( xi + eta - 1) + (1 + xi)*(1 + eta)],
                [-(1 + eta)*(-xi + eta - 1) - (1 - xi)*(1 + eta),
                 (1 - xi)*(-xi + eta - 1) + (1 - xi)*(1 + eta)],
                [2 * (-2*xi) * (1 - eta),
                 -2 * (1 - xi**2)],
                [2 * (1 - eta**2),
                 2 * (-2*eta) * (1 + xi)],
                [2 * (-2*xi) * (1 + eta),
                 2 * (1 - xi**2)],
                [-2 * (1 - eta**2),
                 2 * (-2*eta) * (1 - xi)]
            ])
    else:
        print(f"Element {elem_type} not yet supported")
        N = np.array([])
        dNdxi = np.array([])

    # Build Nv: for each node, stack the identity matrix scaled by N[i].
    if N.size == 0:
        Nv = np.array([])
    else:
        n_nodes = N.size  # number of nodes
        I = np.eye(dim)
        Nv_list = [I * N[i] for i in range(n_nodes)]
        Nv = np.vstack(Nv_list)

    # Assemble B matrix
    if dim == 1:
        B = dNdxi
    elif dim == 2:
        if dNdxi.size == 0:
            B = np.array([])
        else:
            n_nodes = dNdxi.shape[0]
            B = np.zeros((2 * n_nodes, 3))
            for i in range(n_nodes):
                B[2*i,   0] = dNdxi[i, 0]
                B[2*i+1, 1] = dNdxi[i, 1]
                B[2*i,   2] = dNdxi[i, 1]
                B[2*i+1, 2] = dNdxi[i, 0]
    else:
        B = np.array([])

    return Nv, dNdxi, B
