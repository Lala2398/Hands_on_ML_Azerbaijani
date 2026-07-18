#!/usr/bin/env bash
# Run this INSIDE your local clone of the repo (same folder as README.md).
# It moves all chapter PDFs into a chapters/ folder with consistent,
# zero-padded names so they sort correctly and match the README table.
set -e

mkdir -p chapters

git mv "Chapter 1.pdf"                                 "chapters/Chapter_01.pdf"
git mv "Chapter_02_AZ.pdf"                              "chapters/Chapter_02.pdf"
git mv "Chapter 3.pdf"                                  "chapters/Chapter_03.pdf"
git mv "Chapter_4.pdf"                                  "chapters/Chapter_04.pdf"
git mv "Chapter 5.pdf"                                  "chapters/Chapter_05.pdf"
git mv "Chapter_6.pdf"                                  "chapters/Chapter_06.pdf"
git mv "Chapter_7.pdf"                                  "chapters/Chapter_07.pdf"
git mv "Chapter 8.pdf"                                  "chapters/Chapter_08.pdf"
git mv "Chapter__9.pdf"                                 "chapters/Chapter_09.pdf"
git mv "Chapter 10.pdf"                                 "chapters/Chapter_10.pdf"
git mv "Chapter_11.pdf"                                 "chapters/Chapter_11.pdf"
git mv "Chapter_12.pdf"                                 "chapters/Chapter_12.pdf"
git mv "Chapter 13.pdf"                                 "chapters/Chapter_13.pdf"
git mv "Chapter_14_CNN.docx.pdf"                        "chapters/Chapter_14.pdf"
git mv "Hands on machine learning - Chapter 15.pdf"     "chapters/Chapter_15.pdf"
git mv "Chapter_16.pdf"                                 "chapters/Chapter_16.pdf"
git mv "Chapter_17.pdf"                                 "chapters/Chapter_17.pdf"
git mv "Chapter_18.pdf"                                 "chapters/Chapter_18.pdf"
git mv "Chapter 19.pdf"                                 "chapters/Chapter_19.pdf"
git mv "Introduction.pdf"                                "chapters/Introduction.pdf"

echo "Done. Review with 'git status', then replace README.md with the updated version, and commit:"
echo "  git add -A"
echo "  git commit -m 'Reorganize chapters into chapters/ with consistent naming'"
