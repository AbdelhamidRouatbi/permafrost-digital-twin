import numpy as np
import time
import scipy.sparse as sp
import scipy.sparse.linalg as spla
import matplotlib.pyplot as plt
import os
import shutil

# Import the helper functions
from lagrange_basis import lagrange_basis  # returns (Nv, dNdxi, B); we use the first two outputs here
from quadrature import quadrature        # returns (W, Q)
from write_vtu_file import write_vtu_file
from write_pvd import write_pvd

# Define the output folder for VTK files.
output_folder = 'output'
# Remove the output folder if it exists
if os.path.exists(output_folder):
    shutil.rmtree(output_folder)

# Create a new, empty output folder
os.makedirs(output_folder)

vtk_files = []   # List to store VTK filenames
time_steps = []  # List to store time step values

# ---------------------------
# INPUT and PARAMETERS
# ---------------------------
# Time parameters
duration = 240 * 60 * 60          # [s]
dt = 3600                        # [s]
nstep = int(np.round(duration / dt))
Time = np.zeros(nstep + 1)

# General properties
poro    = 1.0       # Initial porosity
rho_s   = 2000      # Density of soil  [kg/m3]
rho_w   = 1000      # Density of water [kg/m3]
rho_i   = 920       # Density of ice   [kg/m3]
gravity = 9.81      # Gravity [m/s2]

# Thermal properties
Tr        = 273.15    # Reference temperature [K]
k_parameter = 5.0
landa_s   = 1.1       # Thermal conductivity of soil  [J/s/m/K]
landa_w   = 0.58      # Thermal conductivity of water [J/s/m/K]
landa_i   = 2.20      # Thermal conductivity of ice   [J/s/m/K]
cap_s     = 900       # Specific heat capacity of soil  [J/kg/K]
cap_w     = 4190      # Specific heat capacity of water [J/kg/K]
cap_i     = 2090      # Specific heat capacity of ice   [J/kg/K]
Lf        = 3.34e5    # Latent heat of fusion [J/kg]

# Element Properties
elemType1 = 'L2'
integ     = 'GAUSS'
order1    = 2

# ---------------------------
# MESHING and GEOMETRY
# ---------------------------
bar_length = 4.0      # Length of the bar in meters
dx = 0.005            # Node spacing in meters

# Number of nodes and node coordinates
numnode = int(bar_length / dx) + 1
node = np.linspace(0, bar_length, numnode)

# Generate element connectivity (0-indexed)
numelem = numnode - 1
element = np.zeros((numelem, 2), dtype=int)
for i in range(numelem):
    element[i, :] = [i, i + 1]

# Fixed temperature nodes (convert MATLAB 1-indexed to Python 0-indexed)
FixedNodesT = np.array([0, 800])  # In MATLAB: [1;801]

# ---------------------------
# INITIAL CONDITIONS
# ---------------------------
total_unknown = numnode
temp_unknown  = numnode

# Temperature field (unknown)
T = np.full(numnode, 263.15)
T[0] = 308.15

# Degrees of freedom for temperature (essential BCs)
Tdofs = FixedNodesT.copy()
numTdof = numnode

# Set initial unknown vector
Xn = T.copy()

tol_r = 1e-6
# Get quadrature rule for 1D Gaussian integration
W1, Q1 = quadrature(order1, 'GAUSS', 1)

# Prepare variables for saving temperature profiles at given times
T4 = T12 = T28 = T60 = T124 = T240 = None

# Start timing
tic = time.time()

# ---------------------------
# TIME-STEPPING LOOP
# ---------------------------
for step in range(nstep):
    converged = False
    iter_count = 0

    # Create sparse matrices for stiffness and capacity (using LIL for assembly)
    Ktt = sp.lil_matrix((numnode, numnode))
    Ctt = sp.lil_matrix((numnode, numnode))
    
    # Force vector (here zero)
    fT = np.zeros(temp_unknown)
    
    # Initialize unknowns for the current time step
    X_new = Xn.copy()
    T = X_new.copy()
    
    # Loop over elements
    for iel in range(numelem):
        # Global node indices for the element
        sctrT = element[iel, :]  
        nn = len(sctrT)
        
        # Loop over quadrature points (1D rule, since elemType1 is 'L2')
        for jel in range(W1.shape[0]):
            pt = Q1[jel, :]  # quadrature point (1D coordinate)

            # Get shape functions and their derivatives.
            # Our lagrange_basis function returns (Nv, dNdxi, B); we use the first two.
            N, dNdxi, _ = lagrange_basis(elemType1, pt)
            
            # Compute the element Jacobian:
            # In the 1D bar, node[sctrT] gives the coordinates of the two nodes.
            # MATLAB: J0 = node(sctrT,:)'*dNdxi, which for scalars is the dot product.
            J0 = np.dot(node[sctrT], dNdxi)
            dNdx = dNdxi / J0  # derivative with respect to the physical coordinate
            
            # Make N a row vector and dNdx a row vector (for consistency)
            Nt = N.reshape(1, nn)
            Bt = dNdx.reshape(1, nn)
            
            # Compute temperature at the quadrature point
            T_temp = np.dot(Nt, T[sctrT])[0]
            
            # ---------------------------
            # Auxiliary relations
            # ---------------------------
            X_exp = np.exp(k_parameter * (T_temp - Tr))
            si = 1.0 / (1.0 + X_exp)
            dsidT = -k_parameter * X_exp / ((1.0 + X_exp)**2)
            sw = 1 - si
            
            landa = (1 - poro) * landa_s + (poro * sw) * landa_w + (poro * si) * landa_i
            rhoc_eff = ((1 - poro) * rho_s * cap_s +
                        (poro * sw) * rho_w * cap_w +
                        (poro * si) * rho_i * cap_i)
            
            # ---------------------------
            # Assemble volume integrals
            # ---------------------------
            # Local stiffness matrix contribution:
            localK = (Bt.T @ Bt) * landa * W1[jel] * J0
            # Local capacity matrix contribution:
            localC = (Nt.T @ Nt) * (rhoc_eff - Lf * rho_i * poro * dsidT) * W1[jel] * J0
            
            # Assemble into global matrices
            for a in range(nn):
                for b in range(nn):
                    Ktt[sctrT[a], sctrT[b]] += localK[a, b]
                    Ctt[sctrT[a], sctrT[b]] += localC[a, b]
                    
            # (Force vector fT assembly is omitted, as in the MATLAB code.)
    
    # Convert assembled matrices to CSR format for efficient arithmetic/solving
    K_matrix = Ktt.tocsr()
    C_matrix = Ctt.tocsr()
    Jacoubian = C_matrix / dt + K_matrix
    Fext = fT.copy()
    
    # Compute the residual vector: Fext - (K_matrix * Xn)
    residual = Fext - K_matrix @ Xn
    
    # Apply essential boundary conditions.
    # Use the average of the Jacobian’s diagonal as a scaling measure.
    bcwt = np.mean(Jacoubian.diagonal())
    # Convert to LIL for row/column modifications
    Jacoubian = Jacoubian.tolil()
    for dof in Tdofs:
        Jacoubian[dof, :] = 0
        Jacoubian[:, dof] = 0
        Jacoubian[dof, dof] = bcwt
        residual[dof] = 0
    # Convert back to CSR for solving
    Jacoubian = Jacoubian.tocsr()
    
    # ---------------------------
    # Newton-Raphson Iteration
    # ---------------------------
    while not converged:
        iter_count += 1
        
        # Solve for the update dX: Jacoubian * dX = residual
        dX = spla.spsolve(Jacoubian, residual)
        X_new = X_new + dX
        
        # Update the residual:
        residual = Fext + (C_matrix @ Xn) / dt - ((K_matrix) + (C_matrix / dt)) @ X_new
        for dof in Tdofs:
            residual[dof] = 0
        
        res_norm = np.linalg.norm(residual)
        print(f'Norm In iter({iter_count}) = {res_norm}')
        if res_norm < tol_r:
            converged = True
            print(' converged! ')
    
    # Final unknowns update for the time step
    T = X_new.copy()
    Xn = T.copy()

    # Compute elapsed time for reporting
    elapsed = time.time() - tic
    sec = int(np.floor(elapsed - np.floor(elapsed / 60) * 60))
    mint = int(np.floor(np.floor(elapsed / 60) - np.floor(elapsed / 3600) * 60))
    hr = int(np.floor(elapsed / 3600))
    
    print(f'\t\t\t {step + 1} Step \t {iter_count} Iterations \t Elapsed time {hr:02d}:{mint:02d}:{sec:02d}')
    print('--------------------------------------------------------------')
    
    # Save time history
    Time[step + 1] = (step + 1) * dt
    
    # Save temperature profiles at specific times (using np.isclose for floating‐point comparisons)
    current_time = Time[step + 1]
    if np.isclose(current_time, 4 * 60 * 60):
        T4 = T.copy()
    elif np.isclose(current_time, 12 * 60 * 60):
        T12 = T.copy()
    elif np.isclose(current_time, 28 * 60 * 60):
        T28 = T.copy()
    elif np.isclose(current_time, 60 * 60 * 60):
        T60 = T.copy()
    elif np.isclose(current_time, 124 * 60 * 60):
        T124 = T.copy()
    elif np.isclose(current_time, 240 * 60 * 60):
        T240 = T.copy()
        
    
    # Create a unique filename for the current time step.
    vtk_filename = f"temperature_{step:04d}.vtu"
    full_vtk_path = os.path.join(output_folder, vtk_filename)
    
    # Write the VTU file for this time step.
    write_vtu_file(full_vtk_path, node, element, T)
    
    # Since the .pvd file will be placed in the same folder,
    # we store only the filename (relative to the output folder).
    vtk_files.append(vtk_filename)
    time_steps.append(Time[step + 1])

# ---------------------------
# Plotting and Saving Results
# ---------------------------
plt.figure(1)
if T4 is not None:
    plt.plot(node, T4 - 273.15, label='T4')
if T12 is not None:
    plt.plot(node, T12 - 273.15, label='T12')
if T28 is not None:
    plt.plot(node, T28 - 273.15, label='T28')
if T60 is not None:
    plt.plot(node, T60 - 273.15, label='T60')
if T124 is not None:
    plt.plot(node, T124 - 273.15, label='T124')
if T240 is not None:
    plt.plot(node, T240 - 273.15, label='T240')
plt.grid(True)
plt.xlim([0, 1])
plt.xlabel("Node coordinate")
plt.ylabel("Temperature (°C)")
plt.legend()
plt.show()

# Save data to .npy files
if T4 is not None:
    np.save('T4.npy', T4)
if T12 is not None:
    np.save('T12.npy', T12)
if T28 is not None:
    np.save('T28.npy', T28)
if T60 is not None:
    np.save('T60.npy', T60)
if T124 is not None:
    np.save('T124.npy', T124)
if T240 is not None:
    np.save('T240.npy', T240)

pvd_filename = os.path.join(output_folder, "temperature.pvd")
write_pvd(pvd_filename, vtk_files, time_steps)