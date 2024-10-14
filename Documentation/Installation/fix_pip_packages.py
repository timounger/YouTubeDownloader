"""!
********************************************************************************
@file    fix_pip_packages.py
@brief   Fix code from packages
********************************************************************************
"""

# autopep8: off
import sys
import os
import logging

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
from Source.Util.colored_log import init_console_logging  # pylint: disable=wrong-import-position
# autopep8: on

log = logging.getLogger("FixPipPackages")
init_console_logging(logging.INFO)

def fix_packages():
    """!
    @brief  Fix PIP packages
    """
    src_filename = "cipher.py"
    dest_filename = r"../../.env\Lib\site-packages\pytube\cipher.py"

    with open(src_filename, mode="r", encoding="utf-8") as file:
        code = file.read()


    with open(dest_filename, mode="w", encoding="utf-8") as file:
        file.write(code)

    log.info("Code fixed in %s", dest_filename)


if __name__ == "__main__":
    fix_packages()
