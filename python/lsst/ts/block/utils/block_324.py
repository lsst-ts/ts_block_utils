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

__all__ = ["make_block_324"]

import os
import pathlib

from lsst.ts import observing


def make_block_324() -> None:
    """Generate configuration for BLOCK-324."""

    scripts = [
        observing.ObservingScript(
            name="maintel/track_target.py",
            standard=True,
            parameters=dict(
                target_name="$name",
                slew_icrs=dict(ra="$ra", dec="$dec"),
                rot_value="$rot",
                rot_type="PhysicalSky",
                az_wrap_strategy="NOUNWRAP",
            ),
        ),
        observing.ObservingScript(
            name="maintel/close_loop_comcam.py",
            standard=True,
            parameters=dict(
                exposure_time=15,
                max_iter=2,
                gain_sequence=[0.75, 0.5],
                mode="FAM",
                program="$program",
                note="pointing_lut_closed_loop",
                reason="PtgModel",
                used_dofs=[
                    0,
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11,
                    12,
                    13,
                    14,
                    15,
                    16,
                    17,
                    18,
                    19,
                    20,
                    21,
                    22,
                    23,
                    24,
                    25,
                    26,
                    27,
                    30,
                    31,
                    32,
                    33,
                    34,
                    35,
                    36,
                    37,
                    38,
                    39,
                    40,
                    41,
                    42,
                    43,
                    44,
                    45,
                    46,
                ],
                apply_corrections=True,
                use_ocps=True,
            ),
        ),
        observing.ObservingScript(
            name="maintel/take_image_comcam.py",
            standard=True,
            parameters=dict(
                image_type="ACQ",
                nimages=1,
                exp_times=15,
                reason="PtgModel",
                program="$program",
                filter="r_03",
            ),
        ),
    ]

    block_name = "BLOCK-324"
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
    make_block_324()
