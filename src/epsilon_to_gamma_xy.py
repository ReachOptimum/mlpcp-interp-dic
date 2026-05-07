import os
import csv
import numpy as np
from tqdm import tqdm

# Variables
DATA = r"data/cleaned"
X_TRAIN = os.path.join(DATA, "x_train_dic.csv")
X_TEST = os.path.join(DATA, "x_test_dic.csv")

buff_tshold = 1

def count_lines(path):
    with open(path, "r", newline="") as f:
        return sum(1 for _ in f)

for infile in [X_TRAIN, X_TEST]:
    new_fname = infile.replace(".csv", "_exy_x2.csv")

    infile_len = count_lines(infile)

    with open(infile, mode="r", newline="", encoding="utf-8") as fin:
        reader = csv.reader(fin)
        total_cols = 1637800
        n_timesteps = 20
        # each timestep has (2 + 3*x_len) columns
        x_len = (total_cols // n_timesteps - 2) // 3

        bg_bf = []

        with open(new_fname, mode="w", newline="", encoding="utf-8") as fout:
            writer = csv.writer(fout)

            for k, row in enumerate(tqdm(reader, total=infile_len, dynamic_ncols=True, ascii=True), start=1):
                expected_len = n_timesteps * (2 + 3 * x_len)
                if len(row) != expected_len:
                    raise ValueError(
                        f"Row {k}: expected {expected_len} columns (={n_timesteps}*(2+3*{x_len})), got {len(row)}."
                    )

                out = list(row)

                for j in range(n_timesteps):
                    c = j * (2 + 3 * x_len)
                    start = c + 2

                    # def_xy is the 3rd item of each (def_x, def_y, def_xy) triplet
                    for idx in range(start + 2, start + 3 * x_len, 3):
                        out[idx] = str(float(out[idx]) * 2.0)

                bg_bf.append(out)

                if len(bg_bf) >= buff_tshold:
                    writer.writerows(bg_bf)
                    bg_bf.clear()

            # flush remainder
            if bg_bf:
                writer.writerows(bg_bf)
                bg_bf.clear()
