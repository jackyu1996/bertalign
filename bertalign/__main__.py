#!/usr/bin/env python

from pathlib import Path
import sys


def align(src_file, tgt_file, src_lang, tgt_lang):
    from bertalign import Bertalign

    with open(src_file, "r", encoding="utf-8") as sf:
        src = sf.read()

    with open(tgt_file, "r", encoding="utf-8") as tf:
        tgt = tf.read()

    aligner = Bertalign(src, tgt, src_lang, tgt_lang)
    aligner.align_sents()

    all_src = []
    all_tgt = []

    for bead in aligner.result:
        all_src.append(aligner._get_line(bead[0], aligner.src_sents))
        all_tgt.append(aligner._get_line(bead[1], aligner.tgt_sents))

    aligner.write_tmx("aligned/" + Path(src_file).stem + ".tmx")


def batch_align(src_dir, tgt_dir, src_lang, tgt_lang):
    from bertalign import Bertalign

    all_src_files = list(Path(src_dir).glob("*.txt"))
    all_tgt_files = list(Path(tgt_dir).glob("*.txt"))

    if len(all_src_files) != len(all_tgt_files):
        print("Wrong number of source and target files")
        sys.exit(1)

    for i, src_file in enumerate(all_src_files):
        with open(src_file) as sf:
            src_text = sf.read()

        with open(all_tgt_files[i]) as tf:
            tgt_text = tf.read()

        print(f"Start aligning {src_file.name} to {all_tgt_files[i].name}")

        aligner = Bertalign(src_text, tgt_text, src_lang, tgt_lang)
        aligner.align_sents()

        all_src = []
        all_tgt = []

        for bead in aligner.result:
            all_src.append(aligner._get_line(bead[0], aligner.src_sents))
            all_tgt.append(aligner._get_line(bead[1], aligner.tgt_sents))

        aligner.write_tmx("aligned/" + src_file.stem + ".tmx")


if len(sys.argv) == 6:
    if sys.argv[1] == "batch":
        batch_align(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    elif sys.argv[1] == "align":
        align(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
else:
    print(
        "Usage: python -m bertalign batch|align source_file target_file source_lang target_lang"
    )
    sys.exit(1)
