# __all__ = ["user_controller", "product_controller"]
# OR

import glob 
import os

__all__=[os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__) + "/*.py" )]

# for f in glob.glob(os.path.dirname(__file__) + "/*.py" ):
#     __all__.append(os.path.basename(f)[:-3])