
# coding: utf-8

# In[ ]:


from sklearn import preprocessing
from tqdm import tqdm 
import pandas as pd

def generate_dummies(df, columns, prefixes=""):
    
    if len(columns)>0:
        assert ((len(prefixes)>0)),                "Prefixes must be mentioned for all dummies columns"
    
    index = 0
    for col in tqdm(columns):
        if len(prefixes)>0:
            temp = pd.get_dummies(df[col],prefix=prefixes[index])
        else:
            temp = pd.get_dummies(df[col])       
        df = pd.concat([df, temp], axis=1)
        index = index + 1
    return df    

def label_encode(values):
    # Label Encoding Categorical columns
    le = preprocessing.LabelEncoder()
    values = [ element if type(element) is str else '' for element in values]
    le.fit(values)        
    return le.transform(values)

def label_decode(values, value_to_decode):
    # Label Encoding Categorical columns
    le = preprocessing.LabelEncoder()    
    values = [ element if type(element) is str else '' for element in values]
    le.fit(values)
    return le.inverse_transform(value_to_decode)

def normalize(values):
    #Normalize using StandardScaler, setting Mean zero and Variance 1
    scaler = preprocessing.StandardScaler()
    scaler.fit(values)
    return scaler.fit_transform(df[col])
    
    
def preprocess(df, columns, dummies_cols = "", dummies_cols_prefix = ""):
    for col in tqdm(columns):
        
        # Processing for String columns
        if df[col].dtype == object: #For String columns
            
            # Replace NAs with ''
            df[col] = df[col].fillna('')
            
            # Label Encoding Categorical columns 
            df[col] = label_encode(df[col])
        
        # Processing for Numeric columns
        if (df[col].dtype == int) | (df[col].dtype == float):
                        
            df[col] = normalize(df[col])    
        
    
    if len(dummies_cols)>0:
        df = generate_dummies(df, dummies_cols, dummies_cols_prefix)
        
    return df

