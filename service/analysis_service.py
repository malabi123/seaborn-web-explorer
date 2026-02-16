from .data_service import DataService as ds
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import os
import numpy as np

matplotlib.use('Agg')


class AnalysisService:

    QUESTIONS_INFO = [
        {
            "title": "Survival Rate Overall",
            "explanation": (
                "Shows the overall survival rate in the dataset. "
                "It calculates the proportion of passengers who survived "
                "out of the total number of passengers."
            )
        },
        {
            "title": "Survival Rate by Sex",
            "explanation": (
                "Compares survival rates between males and females by grouping "
                "passengers by sex and computing survival proportions."
            )
        },
        {
            "title": "Survival Rate by Class",
            "explanation": (
                "Shows how survival rates differ between passenger classes "
                "and visualizes survival counts per class."
            )
        },
        {
            "title": "Age Distribution",
            "explanation": (
                "Displays the distribution of passenger ages, including the mean age "
                "and the number of missing values."
            )
        },
        {
            "title": "Embarked Counts",
            "explanation": (
                "Shows how many passengers embarked from each port and how survival "
                "varies by embarkation point."
            )
        }
    ]

    @staticmethod
    def get_questions_info():
        return AnalysisService.QUESTIONS_INFO

    @staticmethod
    def __save_pic(title: str):
        folder = r"static\plots"
        fname = f"{title.strip().replace(' ', '_')}.png"
        os.makedirs(folder, exist_ok=True)
        plt.savefig(os.path.join(folder, fname))
        return fname

    @staticmethod
    def __q1():
        title = 'Survival Rate Overall'
        df = ds.get_df()
        surv_count = (df['survived'] == 1).sum()
        dead_count = (df['survived'] == 0).sum()
        survival_rate = float(surv_count/(surv_count+dead_count))
        df_plot = df['survived'].value_counts()
        x = np.arange(len(df_plot))

        plt.figure(figsize=(8, 6))
        plt.bar(df_plot.index, df_plot.values)
        plt.title('Survival count')
        plt.xlabel('Did survive?')
        plt.ylabel('Amount of People')
        plt.xticks(x, ['No', 'Yes'])
        fname = AnalysisService.__save_pic(title)
        dic = {title: survival_rate}

        plt.close()
        return (title, dic, fname)

    @staticmethod
    def __q2():

        title = 'Survival Rate by Sex'
        df = ds.get_df()
        table = df.groupby('sex')['survived'].apply(
            lambda x: float(x.eq(True).sum()/x.notna().sum()))

        df_plot = df.groupby(['sex', 'survived'])[
            'survived'].size().unstack(fill_value=0)
        x = np.arange(len(df_plot))
        width = 0.35

        plt.figure(figsize=(8, 6))
        plt.bar(x - width*0.5, df_plot[1], width, label='Survived')
        plt.bar(x + width*0.5, df_plot[0], width, label="Didn't Survive")
        plt.xticks(x, df_plot.index)
        plt.title('Survival count by Sex')
        plt.ylabel('Amount of People')
        plt.legend()
        fname = AnalysisService.__save_pic(title)
        plt.tight_layout()

        plt.close()
        return (title, table.to_dict(), fname)

    @staticmethod
    def __q3():

        title = 'Survival Rate by Class'
        df = ds.get_df()
        table = df.groupby('class')['survived'].apply(
            lambda x: float(x.eq(True).sum()/x.notna().sum()))

        df_plot = df.groupby(['class', 'survived'])[
            'survived'].size().unstack(fill_value=0)
        x = np.arange(len(df_plot))
        width = 0.35

        plt.figure(figsize=(8, 6))
        plt.bar(x - width*0.5, df_plot[1], width, label='Survived')
        plt.bar(x + width*0.5, df_plot[0], width, label="Didn't Survive")
        plt.xticks(x, df_plot.index)
        plt.title('Survival count by Class')
        plt.ylabel('Amount of People')
        plt.legend()
        fname = AnalysisService.__save_pic(title)
        plt.tight_layout()

        plt.close()
        return (title, table.to_dict(), fname)

    @staticmethod
    def __q4():
        title = 'Age Distribution'
        table = {}
        df = ds.get_df()

        table['Mean Age'] = float(df['age'].mean())
        table['Missing Count'] = int(df['age'].isna().sum())

        plt.figure(figsize=(8, 6))
        plt.hist(df["age"], bins=7, edgecolor='blue')
        plt.title(title)
        plt.xlabel('Age Distribution')
        plt.ylabel('Amount of People')
        plt.tight_layout()

        fname = AnalysisService.__save_pic(title)
        plt.close()
        return (title, table, fname)

    @staticmethod
    def __q5():
        title = 'Embarked Counts'
        df = ds.get_df()

        df_em_cont = df['embarked'].value_counts()

        df_plot = df.groupby(['embarked', 'survived'])[
            'survived'].size().unstack(fill_value=0)
        x = np.arange(len(df_plot))
        width = 0.35

        plt.figure(figsize=(8, 6))
        plt.bar(x - width*0.5, df_plot[1], width, label='Survived')
        plt.bar(x + width*0.5, df_plot[0], width, label="Didn't Survive")
        plt.xticks(x, df_plot.index)
        plt.title('Survival count by Embarked')
        plt.ylabel('Amount of People')
        plt.legend()
        fname = AnalysisService.__save_pic(title)
        plt.tight_layout()

        plt.close()
        return (title, df_em_cont.to_dict(), fname)

    @staticmethod
    def run_question(number: int):
        questions = {
            1: AnalysisService._AnalysisService__q1,
            2: AnalysisService._AnalysisService__q2,
            3: AnalysisService._AnalysisService__q3,
            4: AnalysisService._AnalysisService__q4,
            5: AnalysisService._AnalysisService__q5,
        }
        if number not in questions:
            raise ValueError(
                f"Question {number} not found. Choose between 1-{len(questions)}.")

        return questions[number]()


__all__ = ['AnalysisService']
