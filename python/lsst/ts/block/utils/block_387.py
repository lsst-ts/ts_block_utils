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

__all__ = ["make_block_387"]

import os
import pathlib

from lsst.ts import observing


def make_block_387() -> None:
    """Generate configuration for BLOCK-387."""

    scripts = [
        observing.ObservingScript(
            name="maintel/track_target.py",
            standard=True,
            parameters=dict(
                target_name="$name",
                slew_icrs=dict(ra="$ra", dec="$dec"),
                rot_value="$rot",
                rot_type="Sky",
                az_wrap_strategy="NOUNWRAP",
            ),
        ),
        observing.ObservingScript(
            name="maintel/take_image_lsstcam.py",
            standard=True,
            parameters=dict(
                image_type="ENGTEST",
                nimages=1,
                exp_times=15,
                reason="PtgModel",
                program="$program",
            ),
        ),
    ]

    block_name = "BLOCK-387"
    block = observing.ObservingBlock(
        name="PtgModel",
        program=block_name,
        scripts=scripts,
    )

    if "TS_CONFIG_OCS_DIR" in os.environ:
        output_dir = (
            pathlib.PosixPath(os.environ["TS_CONFIG_OCS_DIR"])
            / "Scheduler"
            / "observing_blocks_maintel"
        )
        assert output_dir.exists()
        output_file = output_dir / f"{block_name}.json"
        if output_file.exists():
            print(f"Output file {output_file} exists. Overwritting.")
        else:
            print(f"Writting block configuration to: {output_file}")
        with open(output_file, "w") as fp:
            fp.write(block.model_dump_json(indent=4))

    else:
        print(block.model_dump_json(indent=4))


if __name__ == "__main__":
    make_block_387()
