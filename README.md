# Hands-on Machine Learning — Azerbaijani Notes & Summaries

Welcome to a set of Azerbaijani-language **notes, summaries, and learning materials** based on *Hands-on Machine Learning with Scikit-Learn, Keras, and TensorFlow* by Aurélien Géron.

This repository is **not a full translation of the book**. Instead, it provides:

* 📝 Azerbaijani chapter summaries, contributed by community members (not professionally edited)
* 💡 Explanations and study notes written by our contributors
* 💻 Annotated code examples with Azerbaijani comments

> **Note on copyright:** To respect the author's and O'Reilly's rights, chapters intentionally omit most figures, illustrations, and images from the original book. These notes are meant to help readers grasp the concepts quickly — for the full material, please buy the original book from [O'Reilly](https://www.oreilly.com) or an authorized retailer and read it alongside these notes.

📌 **Fair Use Disclaimer:** This repository is created for educational purposes under fair use. It does not reproduce or distribute the original book.

🔗 Original book's official code repository: [ageron/handson-ml3](https://github.com/ageron/handson-ml3)

---

## 📖 Chapters

| # | Chapter (book topic) | Notes | Author(s) |
|---|---|---|---|
| — | Introduction | [PDF](chapters/Introduction.pdf) | Ibrahim Nizami oğlu · rev. Nihad Hashimov |
| 1 | The Machine Learning Landscape | [PDF](chapters/Chapter_01.pdf) | Lala Ibadullayeva |
| 2 | End-to-End Machine Learning Project | [PDF](chapters/Chapter_02.pdf) | Lala Ibadullayeva |
| 3 | Classification | [PDF](chapters/Chapter_03.pdf) | Nihad Hashimov |
| 4 | Training Models | [PDF](chapters/Chapter_04.pdf) | Shamil Mehdiyev |
| 5 | Support Vector Machines | [PDF](chapters/Chapter_05.pdf) | Leyla Eminova |
| 6 | Decision Trees | [PDF](chapters/Chapter_06.pdf) | Laman Jafarli |
| 7 | Ensemble Learning and Random Forests | [PDF](chapters/Chapter_07.pdf) | Sevinj Rahimova |
| 8 | Dimensionality Reduction | [PDF](chapters/Chapter_08.pdf) | Laman Jafarli |
| 9 | Unsupervised Learning Techniques | [PDF](chapters/Chapter_09.pdf) | Lala Ibadullayeva |
| 10 | Intro to Artificial Neural Networks with Keras | [PDF](chapters/Chapter_10.pdf) | Ulviyya İsmayılzada |
| 11 | Training Deep Neural Networks | [PDF](chapters/Chapter_11.pdf) | Lala Ibadullayeva |
| 12 | Custom Models and Training with TensorFlow | [PDF](chapters/Chapter_12.pdf) | Lala Ibadullayeva |
| 13 | Loading and Preprocessing Data with TensorFlow | [PDF](chapters/Chapter_13.pdf) | Lala Ibadullayeva |
| 14 | Deep Computer Vision Using CNNs | [PDF](chapters/Chapter_14.pdf) | Lala Ibadullayeva |
| 15 | Processing Sequences Using RNNs and CNNs | [PDF](chapters/Chapter_15.pdf) | Sevinj Rahimova |
| 16 | NLP with RNNs and Attention | [PDF](chapters/Chapter_16.pdf) | Lala Ibadullayeva |
| 17 | Autoencoders, GANs, and Diffusion Models | [PDF](chapters/Chapter_17.pdf) | Lala Ibadullayeva |
| 18 | Reinforcement Learning | [PDF](chapters/Chapter_18.pdf) | Lala Ibadullayeva |
| 19 | Training and Deploying TensorFlow Models at Scale | [PDF](chapters/Chapter_19.pdf) | Ibrahim Nizami oğlu · rev. Nihad Hashimov |

*(Chapter titles above follow the 3rd edition table of contents, for orientation only — they are not verbatim reproductions of the book.)*

---

## 📚 EPUB edition

All chapters above are also available combined into a single e-book: [`epub/Hands-on-ML-Azerbaijani.epub`](epub/Hands-on-ML-Azerbaijani.epub).

It's built with [`scripts/build_epub.py`](scripts/build_epub.py), which reads this README's chapter table for the order/titles/authors and converts each PDF in `chapters/` into a proper reflowable chapter (text + images), so it isn't just the PDFs glued together. Whenever a chapter PDF is added or replaced, regenerate it:

```bash
pip install -r scripts/requirements.txt
python3 scripts/build_epub.py
```

This always rebuilds the whole EPUB from scratch, so it's safe to re-run any time.

---

## 🕐 Project history

Started in **November 2023**, completed in **July 2026**. The team changed several times along the way — many people contributed, some for a single chapter, others across the whole project. Thank you to everyone who took part, and especially to those who stayed until the end.

## 🤝 Contributing

This repo stays open. You're welcome to:

* ⭐ Star the repo
* 🐞 Open an issue (typos, unclear explanations, broken links)
* 🔀 Submit a pull request
* 💻 Contribute a new chapter note or improve an existing one directly

## 📄 License

MIT — see [LICENSE](LICENSE).
