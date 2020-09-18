import logging

import dask.array as da
import napari

logging.basicConfig(level=logging.DEBUG)

FNAME = "https://s3.embassy.ebi.ac.uk/idr/zarr/v0.1/9822151.zarr"

pyramid = [da.from_zarr(FNAME + '/' + str(i)) for i in range(11)]

with napari.gui_qt():
    napari.view_image(pyramid)
