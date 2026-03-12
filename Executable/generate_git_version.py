"""!
********************************************************************************
@file   generate_git_version.py
@brief  Utility script to generate a python file containing the git
        short SHA as a variable for the executable.
        Called within the build process (generate_executable.py).
********************************************************************************
"""

import sys
import os
import logging
import git

log = logging.getLogger("GenerateGitVersion")

GIT_VERSION_FILE_NAME = "git_version.py"

FILE_HEADER = f'''"""!
********************************************************************************
@file   {GIT_VERSION_FILE_NAME}
@brief  Defines Git version.
********************************************************************************
"""

'''


def generate_git_version_file(workpath: str) -> None:
    """!
    @brief Generate git_version.py containing the current Git short SHA as a constant.
    @param workpath : output directory (created if it does not exist)
    """
    git_version_file = os.path.join(workpath, GIT_VERSION_FILE_NAME)

    log.info("Generating git version file %s", git_version_file)
    if not os.path.exists(workpath):
        os.mkdir(workpath)
    else:
        log.info("Directory %s already exists", workpath)
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.commit.hexsha
    short_sha = repo.git.rev_parse(sha, short=8)
    with open(git_version_file, mode="w", encoding="utf-8") as f:
        f.write(f"{FILE_HEADER}GIT_SHORT_SHA = '{short_sha}'\n")


if __name__ == "__main__":
    workpath = sys.argv[1]
    generate_git_version_file(workpath)
    sys.exit()
