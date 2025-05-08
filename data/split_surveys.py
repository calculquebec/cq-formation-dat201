import os
import pandas as pd
import sys


def split_by(df, col):
    dir_name = f'by_{col}'

    if dir_name in os.listdir('.'):
        print(f'Le dossier "{dir_name}" existe')
    else:
        os.mkdir(dir_name)
        print(f'Nouveau dossier: "{dir_name}"')

    for value in sorted(df[col].unique()):
        filename = os.path.join(dir_name, f'surveys_{value}.csv')
        print(filename)

        sub_df = df[df[col] == value]
        sub_df.to_csv(filename, index=False)


def main():
    os.chdir(sys.path[0])
    surveys_df = pd.read_csv('surveys_0_NA.csv')

    split_by(surveys_df, 'year')
    split_by(surveys_df, 'species_id')


if __name__ == '__main__':
    main()
