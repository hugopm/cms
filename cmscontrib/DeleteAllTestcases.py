#!/usr/bin/env python3

# Contest Management System - http://cms-dev.github.io/
# Copyright © 2016 Peyman Jabbarzade Ganje <peyman.jabarzade@gmail.com>
# Copyright © 2016 Stefano Maggiolo <s.maggiolo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""This script deletes all testcases from the active dataset of a task."""

import argparse
import logging
import sys

from cms import utf8_decoder
from cms.db import SessionGen, Task
from cms.db.filecacher import FileCacher


logger = logging.getLogger(__name__)


def delete_all_testcases(task_name):
    with SessionGen() as session:
        task = session.query(Task)\
            .filter(Task.name == task_name).first()
        if not task:
            logger.error("No task called %s found." % task_name)
            return False
        dataset = task.active_dataset

        file_cacher = FileCacher()
        try:
            logger.info(f"task {task_name}: {len(dataset.testcases)} tests found in active dataset")
            for codename in dataset.testcases:
                testcase = dataset.testcases[codename]
                session.delete(testcase)
                try:
                    session.commit()
                    logger.info(f"test {codename} deleted")
                except Exception as error:
                    logger.error(f"Error when trying to delete {codename}: {str(error)}")
                    continue
        except Exception as error:
            logger.error(str(error))
            return False

    return True


def main():
    """Parse arguments and launch process."""
    parser = argparse.ArgumentParser(description="Delete all testcases from the active dataset of a task.")
    parser.add_argument("task_name", action="store", type=utf8_decoder,
                        help="task whose testcases will be deleted")
    args = parser.parse_args()

    success = delete_all_testcases(args.task_name) 
    return 0 if success is True else 1


if __name__ == "__main__":
    sys.exit(main())
