import numpy as np

def quadrature(quadorder, qt='GAUSS', sdim=None):

    # Currently, only GAUSS quadrature is implemented.
    if qt != 'GAUSS':
        raise ValueError("Only 'GAUSS' quadrature is supported.")

    # Limit the quadrature order to 8 if too high.
    if quadorder > 8:
        print("Order of quadrature too high for Gaussian Quadrature; setting quadorder to 8.")
        quadorder = 8

    # Allocate arrays for quadrature points and weights.
    num_points = quadorder ** sdim
    quadpoint = np.zeros((num_points, sdim))
    quadweight = np.zeros(num_points)

    # Allocate arrays for 1D quadrature points and weights.
    r1pt = np.zeros(quadorder)
    r1wt = np.zeros(quadorder)

    # Define the 1D Gaussian quadrature rules.
    if quadorder == 1:
        r1pt[0] = 0.0
        r1wt[0] = 2.0

    elif quadorder == 2:
        r1pt[0] = 0.577350269189626
        r1pt[1] = -0.577350269189626
        r1wt[0] = 1.0
        r1wt[1] = 1.0

    elif quadorder == 3:
        r1pt[0] = 0.774596669241483
        r1pt[1] = -0.774596669241483
        r1pt[2] = 0.0
        r1wt[0] = 0.555555555555556
        r1wt[1] = 0.555555555555556
        r1wt[2] = 0.888888888888889

    elif quadorder == 4:
        r1pt[0] = 0.861134311594053
        r1pt[1] = -0.861134311594053
        r1pt[2] = 0.339981043584856
        r1pt[3] = -0.339981043584856
        r1wt[0] = 0.347854845137454
        r1wt[1] = 0.347854845137454
        r1wt[2] = 0.652145154862546
        r1wt[3] = 0.652145154862546

    elif quadorder == 5:
        r1pt[0] = 0.906179845938664
        r1pt[1] = -0.906179845938664
        r1pt[2] = 0.538469310105683
        r1pt[3] = -0.538469310105683
        r1pt[4] = 0.0
        r1wt[0] = 0.236926885056189
        r1wt[1] = 0.236926885056189
        r1wt[2] = 0.478628670499366
        r1wt[3] = 0.478628670499366
        r1wt[4] = 0.568888888888889

    elif quadorder == 6:
        r1pt[0] = 0.932469514203152
        r1pt[1] = -0.932469514203152
        r1pt[2] = 0.661209386466265
        r1pt[3] = -0.661209386466265
        r1pt[4] = 0.238619186003152
        r1pt[5] = -0.238619186003152
        r1wt[0] = 0.171324492379170
        r1wt[1] = 0.171324492379170
        r1wt[2] = 0.360761573048139
        r1wt[3] = 0.360761573048139
        r1wt[4] = 0.467913934572691
        r1wt[5] = 0.467913934572691

    elif quadorder == 7:
        r1pt[0] = 0.949107912342759
        r1pt[1] = -0.949107912342759
        r1pt[2] = 0.741531185599394
        r1pt[3] = -0.741531185599394
        r1pt[4] = 0.405845151377397
        r1pt[5] = -0.405845151377397
        r1pt[6] = 0.0
        r1wt[0] = 0.129484966168870
        r1wt[1] = 0.129484966168870
        r1wt[2] = 0.279705391489277
        r1wt[3] = 0.279705391489277
        r1wt[4] = 0.381830050505119
        r1wt[5] = 0.381830050505119
        r1wt[6] = 0.417959183673469

    elif quadorder == 8:
        r1pt[0] = 0.960289856497536
        r1pt[1] = -0.960289856497536
        r1pt[2] = 0.796666477413627
        r1pt[3] = -0.796666477413627
        r1pt[4] = 0.525532409916329
        r1pt[5] = -0.525532409916329
        r1pt[6] = 0.183434642495650
        r1pt[7] = -0.183434642495650
        r1wt[0] = 0.101228536290376
        r1wt[1] = 0.101228536290376
        r1wt[2] = 0.222381034453374
        r1wt[3] = 0.222381034453374
        r1wt[4] = 0.313706645877887
        r1wt[5] = 0.313706645877887
        r1wt[6] = 0.362683783378362
        r1wt[7] = 0.362683783378362

    else:
        print("Order of quadrature too high for Gaussian Quadrature")

    # Build the multidimensional quadrature grid.
    n = 0
    if sdim == 1:
        for i in range(quadorder):
            quadpoint[n, :] = [r1pt[i]]
            quadweight[n] = r1wt[i]
            n += 1

    elif sdim == 2:
        for i in range(quadorder):
            for j in range(quadorder):
                quadpoint[n, :] = [r1pt[i], r1pt[j]]
                quadweight[n] = r1wt[i] * r1wt[j]
                n += 1

    elif sdim == 3:
        for i in range(quadorder):
            for j in range(quadorder):
                for k in range(quadorder):
                    quadpoint[n, :] = [r1pt[i], r1pt[j], r1pt[k]]
                    quadweight[n] = r1wt[i] * r1wt[j] * r1wt[k]
                    n += 1

    # Return weights and points.
    W = quadweight
    Q = quadpoint
    return W, Q
