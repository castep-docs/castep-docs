# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml", "pandas", "tabulate"]
# ///

"""Program to dump parameters tables from CASTEP exported parameters."""

import sys
from collections import defaultdict
from pathlib import Path

import pandas as pd
import yaml

footnotes = defaultdict(list)


def add_footnote(df: pd.DataFrame, key: str, footnote: str) -> None:
    """Mark KEY with a footnote (FN) in DF.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe to modify.
    key : str
        Name in df to modify.
    footnote : str
        Footnote to add.

    Raises
    ------
    KeyError
        Key not found or matches multiple.
    """
    ind: pd.Index = df[df["name"].str.match(rf"{key}(\$|$)")].index

    if not len(ind):
        raise KeyError(f"Key ({key}) matched no elements.")
    if len(ind) != 1:
        raise KeyError(f"Key ({key}) matched multiple elements.")

    footnotes[footnote].append(key)
    fn_ind = next(i for i, k in enumerate(footnotes, 1) if k == footnote)
    df.loc[ind[0], "name"] += f"$^{fn_ind}$"


def add_mutex(df: pd.DataFrame, *keys: str) -> None:
    """Mark mutually exclusive paramteters.

    Parameters
    ----------
    df : pd.DataFrame
        Dataframe to modify.
    *keys : str
        Mutex keys.

    Raises
    ------
    KeyError
        Keys in different files.
    ValueError
        No keys given.
    """
    if len(keys) < 2:
        raise ValueError("Not enough keys given in mutex")

    data = df[df["name"].str.match(rf"({'|'.join(keys)})(\$|$)")]

    if not len(data):
        raise KeyError(f"Key ({', '.join(keys)}) matched no elements.")

    ftype = data.iloc[0]["source"]

    if not all(c["source"] == ftype for _, c in data.iterrows()):
        raise KeyError("Not all mutex are in the same file")

    key_str = [f"`{key}`" for key in keys]
    msg = " and ".join((", ".join(key_str[:-1]), key_str[-1]))
    msg = f"Only one of {msg} may be present in a {ftype} file"

    for key in keys:
        add_footnote(df, key, msg)


ROOT_PATH = Path(__file__).parents[1]
TEMPLATE = Path(__file__).with_name("template.md")

with open(sys.argv[1]) as in_file:
    keywords = yaml.safe_load(in_file)

df = pd.DataFrame.from_records(keywords)

# Remove obsolete vars
df = df[~df["summary"].str.contains("OBSOLETE", case=False, regex=False)]
df["description"] = df["description"].str.replace("\n", "<br><br>")

for mutex in (
    ("LATTICE_CART", "LATTICE_ABC"),
    ("POSITIONS_ABS", "POSITIONS_FRAC"),
    ("KPOINTS_LIST", "KPOINTS_MP_GRID", "KPOINTS_MP_SPACING"),
    (
        "SPECTRAL_KPOINTS_PATH",
        "SPECTRAL_KPOINTS_MP_GRID",
        "SPECTRAL_KPOINTS_MP_SPACING",
        "SPECTRAL_KPOINT_LIST",
    ),
    ("PHONON_KPOINT_PATH", "PHONON_KPOINT_LIST"),
    ("SYMMETRY_GENERATE", "SYMMETRY_OPS"),
):
    add_mutex(df, *mutex)

for component in ("cell", "parameters"):
    label = component[:5]

    section = df[df["source"] == component]
    section = section.sort_values(["level", "name"], ignore_index=True)
    file = ROOT_PATH / f"docs/documentation/Input_Files/{label}_keywords.md"

    page = TEMPLATE.read_text().format(
        component=component,
        label=label,
        table=section.get(
            ["name", "type", "summary", "description", "level"]
        ).to_markdown(index=False),
        footnotes="\n\n".join(
            f"$^{i}$ {fn}"
            for i, fn in enumerate(
                (
                    fn
                    for fn, keys in footnotes.items()
                    if len(section[section["name"].str.match(rf"({'|'.join(keys)})(\$|$)")])
                ),
                1,
            )
        ),
    )

    file.write_text(page)
