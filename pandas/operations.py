
def df_agg_by_column_count(df, by_column_names, agg_on_column_names, sort_on_column_names = "", 
                           new_agg_column_names = "", ascending = True, nrows = ""):
    ##This method is used to aggregate(count) dataframe on specified columns. Sort. Rename aggregated Result
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
    ##This method is used to aggregate(mean) dataframe on specified columns. Sort. Rename aggregated Result
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
    