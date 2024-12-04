# type: ignore
# This file is part of ts_block_utils.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

__all__ = ["make_block_t208"]

import os
import pathlib

from lsst.ts import observing


def make_block_t208() -> None:
    """Generate configuration for BLOCK-T208."""

    scripts = []
    n_repeat = 10
    for i in range(n_repeat):
        scripts.append(
            observing.ObservingScript(
                name="maintel/take_image_comcam.py",
                standard=True,
                parameters=dict(
                    image_type="ACQ",
                    nimages=4,
                    exp_times=15,
                    reason="PointingVerification",
                    program="$program",
                    filter="r_03",
                ),
            ),
        )
        if i < n_repeat - 1:
            scripts.append(
                observing.ObservingScript(
                    name="sleep.py", standard=True, parameters=dict(sleep_for=60)
                )
            )
    scripts.pop(-1)
    block = observing.ObservingBlock(
        name="InitialPtgVerification",
        program="BLOCK-T208",
        scripts=scripts,
    )

    if "TS_CONFIG_OCS_DIR" in os.environ:
        output_dir = (
            pathlib.PosixPath(os.environ["TS_CONFIG_OCS_DIR"])
            / "Scheduler"
            / "observing_blocks_maintel"
        )
        assert output_dir.exists()
        output_file = output_dir / "BLOCK-T208.json"
        if output_file.exists():
            print(f"Output file {output_file} exists. Overwritting.")
        else:
            print(f"Writting block configuration to: {output_file}")
        with open(output_file, "w") as fp:
            fp.write(block.model_dump_json(indent=4))

    else:
        print(block.model_dump_json(indent=4))


if __name__ == "__main__":
    make_block_t208()
