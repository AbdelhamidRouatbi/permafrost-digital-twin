# permafrost-digital-twin

To start the physical twin:

1. Open jupyter notebook
2. Run the cells of docker/setup.ipynb
3. run the cells of physical-twin/physical_twin.ipynb

This will start sending messages containing a the temperature readings of the sensors and the timestamp. For now, all the sensor input goes into the same queue.
