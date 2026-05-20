#!/usr/bin/env python3
"""
mca_loisirs.py

Script pour réaliser une Analyse des Correspondances Multiples (ACM / MCA)
et générer des graphes similaires au script R fourni.

Usage (exemples):
  python mca_loisirs.py --csv AnaDo_JeuDonnees_Loisirs.csv
  python mca_loisirs.py --csv data.csv --quali-sup 19 20 21 22 --quanti-sup 23

Le script sauvegarde plusieurs figures PNG dans le dossier courant.
"""
import argparse
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Ellipse

try:
    import prince
except Exception as e:
    print("Le package 'prince' est requis. Installez-le via 'pip install prince'.")
    raise

try:
    from adjustText import adjust_text
    _HAS_ADJUSTTEXT = True
except Exception:
    _HAS_ADJUSTTEXT = False


def draw_ellipse(ax, x, y, n_std=1.96, **kwargs):
    if len(x) < 2:
        return None
    cov = np.cov(np.vstack([x, y]))
    vals, vecs = np.linalg.eigh(cov)
    order = vals.argsort()[::-1]
    vals = vals[order]
    vecs = vecs[:, order]
    theta = np.degrees(np.arctan2(*vecs[:, 0][::-1]))
    width, height = 2 * n_std * np.sqrt(vals)
    ell = Ellipse(xy=(np.mean(x), np.mean(y)), width=width, height=height, angle=theta, **kwargs)
    ax.add_patch(ell)
    return ell


def parse_args():
    p = argparse.ArgumentParser(description="MCA plots for Loisirs dataset")
    p.add_argument("--csv", required=True, help="Path to CSV file (sep=';')")
    p.add_argument("--sep", default=';', help="CSV separator (default=';')")
    p.add_argument("--encoding", default='utf-8', help="File encoding")
    p.add_argument("--quali-sup", nargs='*', type=int,
                   help="Indices 1-based des variables qualitatives suppl. (ex: 19 20 21 22)")
    p.add_argument("--quanti-sup", type=int,
                   help="Indice 1-based de la variable quantitative suppl. (ex: 23)")
    p.add_argument("--out-dir", default='plots', help="Dossier de sortie pour les figures")
    return p.parse_args()


def ensure_outdir(path):
    os.makedirs(path, exist_ok=True)


def main():
    args = parse_args()
    ensure_outdir(args.out_dir)

    df = pd.read_csv(args.csv, sep=args.sep, header=0, encoding=args.encoding, low_memory=False)
    print(f"Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")

    # Convert object columns to category for safety
    for c in df.select_dtypes(include=['object']).columns:
        df[c] = df[c].astype('category')

    # Prepare quali.sup and quanti.sup (convert 1-based indices to 0-based)
    quali_sup_cols = []
    if args.quali_sup:
        for idx in args.quali_sup:
            if 1 <= idx <= df.shape[1]:
                quali_sup_cols.append(df.columns[idx - 1])
    quanti_sup_col = None
    if args.quanti_sup and 1 <= args.quanti_sup <= df.shape[1]:
        quanti_sup_col = df.columns[args.quanti_sup - 1]

    print(f"quali.sup cols: {quali_sup_cols}")
    print(f"quanti.sup col: {quanti_sup_col}")

    # Determine categorical columns to use for MCA (exclude quali.sup)
    cat_cols = df.select_dtypes(include=['category']).columns.tolist()
    mca_cols = [c for c in cat_cols if c not in quali_sup_cols]
    if len(mca_cols) == 0:
        # fallback: treat all columns except the quantitative sup as categorical
        tentative = [c for c in df.columns if c != quanti_sup_col and c not in quali_sup_cols]
        mca_cols = tentative

    print(f"Columns used for MCA ({len(mca_cols)}): {mca_cols}")

    X = df[mca_cols].copy()
    # prince expects string categories
    X = X.apply(lambda col: col.astype(str))

    # Fit MCA
    mca = prince.MCA(n_components=5, n_iter=10, copy=True, random_state=42)
    mca = mca.fit(X)

    eig = mca.eigenvalues_
    explained = mca.explained_inertia_

    # Plot eigenvalues / explained inertia
    plt.figure(figsize=(6, 4))
    plt.bar(range(1, len(explained) + 1), np.array(explained) * 100)
    plt.xlabel('Dimension')
    plt.ylabel('Inertie expliquée (%)')
    plt.title('Eigenvalues / Inertie expliquée')
    plt.tight_layout()
    pth = os.path.join(args.out_dir, 'mca_eigenvalues.png')
    plt.savefig(pth, dpi=200)
    plt.close()
    print('Saved', pth)

    # Coordinates
    row_coords = mca.row_coordinates(X)
    col_coords = mca.column_coordinates(X)

    # Individuals plot axes 1 & 2
    fig, ax = plt.subplots(figsize=(8, 6))
    hue_col = quali_sup_cols[0] if len(quali_sup_cols) > 0 else None
    if hue_col:
        hue_values = df[hue_col].astype(str)
        palette = sns.color_palette('tab10', n_colors=len(hue_values.unique()))
        sns.scatterplot(x=row_coords[0], y=row_coords[1], hue=hue_values, palette=palette, s=30, ax=ax, legend='full')
        ax.legend(title=hue_col, bbox_to_anchor=(1.02, 1), loc='upper left')
    else:
        ax.scatter(row_coords[0], row_coords[1], s=20, alpha=0.7)
    ax.axhline(0, color='grey', lw=0.7)
    ax.axvline(0, color='grey', lw=0.7)
    ax.set_xlabel('Dim 1')
    ax.set_ylabel('Dim 2')
    ax.set_title('Individus (axes 1 & 2)')
    plt.tight_layout()
    pth = os.path.join(args.out_dir, 'mca_individuals_dim1_dim2.png')
    plt.savefig(pth, dpi=200)
    plt.close()
    print('Saved', pth)

    # Individuals plot axes 2 & 3 (if available)
    if row_coords.shape[1] >= 3:
        fig, ax = plt.subplots(figsize=(8, 6))
        if hue_col:
            sns.scatterplot(x=row_coords[1], y=row_coords[2], hue=df[hue_col].astype(str), s=30, ax=ax, palette='tab10')
            ax.legend(title=hue_col, bbox_to_anchor=(1.02, 1), loc='upper left')
        else:
            ax.scatter(row_coords[1], row_coords[2], s=20, alpha=0.7)
        ax.axhline(0, color='grey', lw=0.7)
        ax.axvline(0, color='grey', lw=0.7)
        ax.set_xlabel('Dim 2')
        ax.set_ylabel('Dim 3')
        ax.set_title('Individus (axes 2 & 3)')
        plt.tight_layout()
        pth = os.path.join(args.out_dir, 'mca_individuals_dim2_dim3.png')
        plt.savefig(pth, dpi=200)
        plt.close()
        print('Saved', pth)

    # Categories (modalities) plot
    fig, ax = plt.subplots(figsize=(8, 8))
    xs = col_coords[0]
    ys = col_coords[1]
    ax.scatter(xs, ys, s=30)
    texts = []
    for i, label in enumerate(col_coords.index):
        texts.append(ax.text(xs[i], ys[i], label, fontsize=8))
    if _HAS_ADJUSTTEXT:
        adjust_text(texts, arrowprops=dict(arrowstyle='-', color='0.5'))
    ax.axhline(0, color='grey', lw=0.7)
    ax.axvline(0, color='grey', lw=0.7)
    ax.set_xlabel('Dim 1')
    ax.set_ylabel('Dim 2')
    ax.set_title('Catégories des variables (plans factoriels)')
    plt.tight_layout()
    pth = os.path.join(args.out_dir, 'mca_categories_dim1_dim2.png')
    plt.savefig(pth, dpi=200)
    plt.close()
    print('Saved', pth)

    # Ellipses per modality for a grouping variable
    group_var = hue_col if hue_col else (mca_cols[0] if len(mca_cols) > 0 else None)
    if group_var:
        fig, ax = plt.subplots(figsize=(8, 6))
        groups = df[group_var].astype(str)
        unique = groups.unique()
        colors = sns.color_palette('tab10', n_colors=len(unique))
        for k, u in enumerate(unique):
            mask = groups == u
            x = row_coords.loc[mask, 0]
            y = row_coords.loc[mask, 1]
            ax.scatter(x, y, s=15, color=colors[k], alpha=0.6, label=str(u))
            if len(x) > 2:
                draw_ellipse(ax, x, y, n_std=1.96, edgecolor=colors[k], facecolor='none', lw=1)
        ax.legend(title=group_var, bbox_to_anchor=(1.02, 1), loc='upper left')
        ax.set_xlabel('Dim 1')
        ax.set_ylabel('Dim 2')
        ax.set_title(f'Individus avec ellipse par modalité ({group_var})')
        plt.tight_layout()
        pth = os.path.join(args.out_dir, 'mca_ellipses.png')
        plt.savefig(pth, dpi=200)
        plt.close()
        print('Saved', pth)

    # If quantitative supplementary variable provided, compute correlations with components
    if quanti_sup_col is not None:
        qs = pd.to_numeric(df[quanti_sup_col], errors='coerce')
        corrs = []
        for dim in range(min(5, row_coords.shape[1])):
            corrs.append(np.corrcoef(qs.fillna(qs.mean()), row_coords[dim])[0, 1])
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar([1 + i for i in range(len(corrs))], np.abs(corrs))
        ax.set_xlabel('Dimension')
        ax.set_ylabel("|Correlation| avec la variable quantitative supp.")
        ax.set_title(f'Corrélations: {quanti_sup_col}')
        plt.tight_layout()
        pth = os.path.join(args.out_dir, 'mca_quanti_sup_corrs.png')
        plt.savefig(pth, dpi=200)
        plt.close()
        print('Saved', pth)

    print('All done. Figures are in folder:', args.out_dir)


if __name__ == '__main__':
    main()
