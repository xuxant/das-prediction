import joblib
import pandas as pd

anx_model = joblib.load("/app/pickle/anxiety_model.pkl")
dep_model = joblib.load("/app/pickle/depression_model.pkl")
str_model = joblib.load("/app/pickle/stress_model.pkl")

DASS_KEY = {'Depression': [3, 5, 10, 13, 16, 17, 21],
             'Anxiety': [2, 4, 7, 9, 15, 19, 20],
             'Stress': [1, 6, 8, 11, 12, 14, 18]}

class Pridiction(object):
    def __init__(
        self,
        questions
    ):
        self.questions = questions.dict()
        self.depression = None
        self.anxiety = None
        self.stress = None
        self.df = None
        self.non_dass_df = None

    def parse_age_group(self):
        def condition(x):
            if x<=9:
                return 0
            if  10<=x<=13:
                return 1
            if 14<=x<=20:
                return 2
            if 21<=x<=27:
                return 3
            if x>28:
                return 4
        self.df['Age_Group']=self.df['age'].apply(condition)
        self.df = self.df.drop(columns=['age', 'name'])
        
    def create_depression_df(self):
        Dep = []
        for i in DASS_KEY["Depression"]:
            Dep.append('q'+str(i)+'a')
        self.depression = self.df.filter(Dep)

    def create_anxiety_df(self):
        Anx = []
        for i in DASS_KEY["Anxiety"]:
            Anx.append('q'+str(i)+'a')
        
        self.anxiety = self.df.filter(Anx)

    def create_stress_df(self):
        Stress = []
        for i in DASS_KEY["Stress"]:
            Stress.append('q'+str(i)+'a')
        self.stress = self.df.filter(Stress)

    def create_data_frame(self):
        self.df = pd.DataFrame.from_dict([self.questions])
        self.parse_age_group()
        self.seperate_non_dass_data()
        self.create_anxiety_df()
        self.create_depression_df()
        self.create_stress_df()
        self.append_non_dass_data()
        
    def seperate_non_dass_data(self):
        self.non_dass_df = self.df.iloc[:, 21:]

    def score(self):
        dep_col = list(self.depression)
        anx_col = list(self.anxiety)
        strs_col = list(self.stress)
        self.depression['Total_count'] = self.depression[dep_col].sum(axis=1)
        self.anxiety['Total_count'] = self.anxiety[anx_col].sum(axis=1)
        self.stress['Total_count'] = self.stress[strs_col].sum(axis=1)

    def append_non_dass_data(self):
        self.anxiety = pd.merge(self.anxiety, self.non_dass_df, how='inner', left_index=True, right_index=True)

        self.stress = pd.merge(self.stress, self.non_dass_df, how='inner', left_index=True, right_index=True)
        self.depression = pd.merge(self.depression, self.non_dass_df, how='inner', left_index=True, right_index=True)
        

    def predict(self):
        self.create_data_frame()
        prid_depression = dep_model.predict(self.depression.values)
        prid_anxiety = anx_model.predict(self.anxiety.values)
        prid_stress = str_model.predict(self.stress.values)
        return {"deprission_level": prid_depression[0], "stress_level": prid_stress[0], "anxiety_level": prid_anxiety[0]}