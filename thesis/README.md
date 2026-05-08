# Thesis LaTeX Source

LaTeX source files for *Networks of Influence: Legislative Text Diffusion 
in State Reproductive Policy After Dobbs* (Kowalski, 2026).

## Compiling

This project was compiled on [Overleaf](https://overleaf.com) using the 
`guthesis` document class. To recompile locally:

1. Ensure you have a full TeX distribution installed (TeX Live or MiKTeX)
2. Run `pdflatex` on the main entry file, then `biber`, then `pdflatex` twice more:
pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex
## Dependencies

- Document class: `guthesis`
- Bibliography: `biblatex` with Biber backend (APSA style)
- Key packages: `booktabs`, `threeparttable`, `dcolumn`

## Note

Figures are referenced from the `../figures/` directory. 
Ensure that folder is present when compiling locally.
