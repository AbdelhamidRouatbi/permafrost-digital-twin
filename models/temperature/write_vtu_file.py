def write_vtu_file(filename, node, element, temperature):
    """
    Writes a VTU (XML-based) file for a 1D mesh with a scalar temperature field.
    The file can be loaded in ParaView to visualize the data.

    Parameters
    ----------
    filename : str
        Name (and path) of the .vtu file to create, e.g. 'temperature.vtu'.
    node : array_like
        1D array of node coordinates along the x-axis.
    element : array_like
        2D array of shape (numelem, 2) with element connectivity (0-indexed).
        Each row [n1, n2] indicates a line element between nodes n1 and n2.
    temperature : array_like
        1D array of scalar temperature values at each node.
    """

    num_points = len(node)
    num_cells = len(element)

    # Build the points section: each point in 3D, with y = z = 0.0
    # We'll output in ASCII format for readability.
    points_str = ""
    for x in node:
        points_str += f"{x:.6f} 0.0 0.0\n"

    # Build the connectivity (which nodes belong to each cell)
    connectivity_str = ""
    for c0, c1 in element:
        connectivity_str += f"{c0} {c1}\n"

    # Build the offsets array.
    # For a line element with 2 nodes, the offset for cell i is (i+1)*2
    offsets_str = ""
    for i in range(num_cells):
        offsets_str += f"{(i+1)*2}\n"

    # Build the cell types array.
    # VTK cell type 3 corresponds to a line element (VTK_LINE).
    types_str = ""
    for _ in range(num_cells):
        types_str += "3\n"

    # Build the temperature (or any scalar) array.
    temp_str = ""
    for t in temperature:
        temp_str += f"{t:.6f}\n"

    # Write the XML structure for an UnstructuredGrid.
    with open(filename, 'w') as f:
        f.write('<?xml version="1.0"?>\n')
        f.write('<VTKFile type="UnstructuredGrid" version="0.1" byte_order="LittleEndian">\n')
        f.write('  <UnstructuredGrid>\n')
        f.write(f'    <Piece NumberOfPoints="{num_points}" NumberOfCells="{num_cells}">\n')

        # Points section
        f.write('      <Points>\n')
        f.write('        <DataArray type="Float32" NumberOfComponents="3" format="ascii">\n')
        f.write(points_str)
        f.write('        </DataArray>\n')
        f.write('      </Points>\n')

        # Cells section
        f.write('      <Cells>\n')
        f.write('        <DataArray type="Int32" Name="connectivity" format="ascii">\n')
        f.write(connectivity_str)
        f.write('        </DataArray>\n')
        f.write('        <DataArray type="Int32" Name="offsets" format="ascii">\n')
        f.write(offsets_str)
        f.write('        </DataArray>\n')
        f.write('        <DataArray type="UInt8" Name="types" format="ascii">\n')
        f.write(types_str)
        f.write('        </DataArray>\n')
        f.write('      </Cells>\n')

        # PointData section (where we store our scalar field)
        f.write('      <PointData Scalars="Temperature">\n')
        f.write('        <DataArray type="Float32" Name="Temperature" format="ascii">\n')
        f.write(temp_str)
        f.write('        </DataArray>\n')
        f.write('      </PointData>\n')

        # (Optional) CellData section
        f.write('      <CellData>\n')
        f.write('      </CellData>\n')

        f.write('    </Piece>\n')
        f.write('  </UnstructuredGrid>\n')
        f.write('</VTKFile>\n')
