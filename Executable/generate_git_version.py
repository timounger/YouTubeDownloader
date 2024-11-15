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
@brief  Defines Git version
********************************************************************************
"""

'''


def generate_git_version_file(s_workpath: str) -> None:
    """!
    @brief Generate git version file
    @param s_workpath : workpath
    """
    s_git_version_file = os.path.join(s_workpath, GIT_VERSION_FILE_NAME)

    log.info("Generating git version file %s", s_git_version_file)
    if not os.path.exists(s_workpath):
        os.mkdir(s_workpath)
    else:
        log.info("Directory %s already exists", s_workpath)
    repo = git.Repo(search_parent_directories=True)
    sha = repo.head.commit.hexsha
    short_sha = repo.git.rev_parse(sha, short=8)
    with open(s_git_version_file, mode="w", encoding="utf-8") as f:
        code_content = FILE_HEADER
        code_content += f"GIT_SHORT_SHA = '{short_sha}'\n"
        f.write(code_content)


if __name__ == "__main__":
    workpath = sys.argv[1]
    generate_git_version_file(workpath)
    sys.exit()
