#### This python script is meant to pre-process data before feeding into models ####

from sklearn import preprocessing
from tqdm import tqdm 
import pandas as pd
from sklearn import model_selection
from sklearn.model_selection import train_test_split

def interactionterms(df, include_original_features = False):
    #Initializing the interaction terms df
    interaction_terms_df = pd.DataFrame([])    

    #Multiplying the columns with each other in pairs - Interaction
    pos = 0
    for column in df:

        nextpos = pos +1
        for i in range(nextpos,df.columns.size):       

            temp = pd.DataFrame([])
            temp[str(column)+' X '+ str(df.columns[i])] = df[column] * df[df.columns[i]]

            interaction_terms_df = pd.concat([interaction_terms_df,temp],axis=1)

        pos = pos+1

    if include_original_features:
        df1 = pd.concat([df, interaction_terms_df],axis=1)
    else:
        df1 = interaction_terms_df
        
    return df1

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

def standardize(values):
    #Standardize using StandardScaler, setting Mean zero and Variance 1
    scaler = preprocessing.StandardScaler()
    values = values.values.reshape(-1,1)
    scaler.fit(values)
    return scaler.transform(values)

def normalize(values):
    #Normalize using Normalize
    normalizer = preprocessing.Normalizer()
    values = values.values.reshape(-1,1)
    normalizer.fit(values)
    return normalizer.transform(values)
       
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

            df[col] = standardize(df[col])    
        
    
    if len(dummies_cols)>0:
        df = generate_dummies(df, dummies_cols, dummies_cols_prefix)
        
    return df

def preprocess_detailed(df, numeric_cols = "", label_encode_cols = "", dummies_cols = "", dummies_cols_prefix = "", standardizeFlag = True, normalizeFlag = True):
    
    temp_df = df.copy()
    
    for col in tqdm(numeric_cols):
        
        temp_df[col] = temp_df[col].astype(int)
        
        if normalizeFlag:
            temp_df[col] = normalize(temp_df[col])
        
        if standardizeFlag:
            temp_df[col] = standardize(temp_df[col])
    
    for col in tqdm(label_encode_cols):
        
        # Replace NAs with ''
        temp_df[col] = temp_df[col].fillna('')
            
        # Label Encoding Categorical columns - Encoding for ordered categorical values
        temp_df[col] = label_encode(temp_df[col])              
    
    if len(dummies_cols)>0:
        # Encoding for unordered categorical values
        temp_df = generate_dummies(temp_df, dummies_cols, dummies_cols_prefix)
        
    return temp_df


def traintestidssplit(df, id_col, test_perc = 0.33, seed = 7):
    
    train_ids, test_ids = train_test_split(df[id_col], test_size=test_perc, 
                                           random_state= seed
                                          )
    
    train_ids = train_ids.tolist()
    test_ids = test_ids.tolist()
    return train_ids, test_ids

def getDummyColumnNamesWithPrefix(df, dummies_cols, dummies_cols_prefix):
    # List to contain names of dummies column generated with prefix
    dummies_cols_prefixed = []

    for index in range(0,len(dummies_cols)):
        for value in df[dummies_cols[index]].unique():
            if (value != '') & (value != 'nan') & (pd.notna(value)):
                dummies_cols_prefixed.append(dummies_cols_prefix[index] + '_' + value)
        
    return dummies_cols_prefixed    

def split_values_and_extract_column_names(df, source_col, prefix,delimiter = ";"):
    column_values = []
    for value in df[source_col].unique():
        tmp_list = []
        value = str.strip(value)
        if value != '':
            tmp_list = value.split(';')
        column_values = column_values + tmp_list

    column_values = set(column_values)

    column_values_colnames = [prefix + str.upper(value) for value in column_values]
    
    return column_values_colnames
    
def add_empty_cols_to_df(df, column_names):   
    return pd.concat([df,pd.DataFrame(columns=column_names)], axis=1)


def null_analysis(df):
    print('Missing data analysis\n')
    print('Column'.ljust(50,' ') + 'Null count')    
    for col in df.columns:
        print('{0} {1} '.format(col.ljust(50,' '), str(df[df[col].isnull()].shape[0])))
        
        
def df_agg_by_column_count(df, by_column_names, agg_on_column_names, sort_on_column_names = "", 
                           new_agg_column_names = "", ascending = True, nrows = ""):
    newdf = df.copy()
    newdf = newdf.groupby(by=by_column_names)[agg_on_column_names].count().reset_index()
                            
    if sort_on_column_names:
        newdf = newdf.sort_values(by=sort_on_column_names, ascending=ascending)
    
    if new_agg_column_names:        
        if len(new_agg_column_names) == len(agg_on_column_names):
            for i in range(0,len(new_agg_column_names)):
                newdf = newdf.rename(columns={agg_on_column_names[i]:new_agg_column_names[i]})
    if nrows:
        newdf = newdf.head(nrows)
        
    return newdf


def df_agg_by_column_mean(df, by_column_names, agg_on_column_names, sort_on_column_names = "", 
                          new_agg_column_names = "", ascending = True, nrows = ""):
    newdf = df.copy()
    newdf = newdf.groupby(by=by_column_names)[agg_on_column_names].mean().reset_index()
                            
    if sort_on_column_names:
        newdf = newdf.sort_values(by=sort_on_column_names, ascending=ascending)
    
    if new_agg_column_names:        
        if len(new_agg_column_names) == len(agg_on_column_names):
            for i in range(0,len(new_agg_column_names)):
                newdf = newdf.rename(columns={agg_on_column_names[i]:new_agg_column_names[i]})
    if nrows:
        newdf = newdf.head(nrows)
        
    return newdf


def df_agg_by_column_median(df, by_column_names, agg_on_column_names, sort_on_column_names = "", 
                          new_agg_column_names = "", ascending = True, nrows = ""):
    newdf = df.copy()
    newdf = newdf.groupby(by=by_column_names)[agg_on_column_names].median().reset_index()
                            
    if sort_on_column_names:
        newdf = newdf.sort_values(by=sort_on_column_names, ascending=ascending)
    
    if new_agg_column_names:        
        if len(new_agg_column_names) == len(agg_on_column_names):
            for i in range(0,len(new_agg_column_names)):
                newdf = newdf.rename(columns={agg_on_column_names[i]:new_agg_column_names[i]})
    if nrows:
        newdf = newdf.head(nrows)
        
    return newdf

def df_agg_by_column_sum(df, by_column_names, agg_on_column_names, sort_on_column_names = "", 
                          new_agg_column_names = "", ascending = True, nrows = ""):
    newdf = df.copy()
    newdf = newdf.groupby(by=by_column_names)[agg_on_column_names].sum().reset_index()
                            
    if sort_on_column_names:
        newdf = newdf.sort_values(by=sort_on_column_names, ascending=ascending)
    
    if new_agg_column_names:        
        if len(new_agg_column_names) == len(agg_on_column_names):
            for i in range(0,len(new_agg_column_names)):
                newdf = newdf.rename(columns={agg_on_column_names[i]:new_agg_column_names[i]})
    if nrows:
        newdf = newdf.head(nrows)
        
    return newdf