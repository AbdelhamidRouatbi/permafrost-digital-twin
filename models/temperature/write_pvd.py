def write_pvd(filename, vtk_files, time_steps):
    """
    Writes a .pvd file to group a series of VTK files as a time series.
    
    Parameters
    ----------
    filename : str
        Name of the .pvd file to create (e.g., 'temperature.pvd').
    vtk_files : list of str
        List of VTK file names (e.g., ['temperature_0000.vtk', 'temperature_0001.vtk', ...]).
    time_steps : list of float
        List of time step values corresponding to each VTK file.
    """
    with open(filename, 'w') as f:
        f.write('<?xml version="1.0"?>\n')
        f.write('<VTKFile type="Collection" version="0.1" byte_order="LittleEndian" header_type="UInt64">\n')
        f.write('  <Collection>\n')
        for t, vtk_file in zip(time_steps, vtk_files):
            f.write(f'    <DataSet timestep="{t}" group="" part="0" file="{vtk_file}"/>\n')
        f.write('  </Collection>\n')
        f.write('</VTKFile>\n')
