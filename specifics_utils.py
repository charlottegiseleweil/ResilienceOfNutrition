def data_cleaning(df,log_cal=True):

    df = df.set_index('pixel_id')

    # Deal with NaNs
    df['slope'] = df['slope'].replace({-9999: np.nan})  # 143 NaN in 'slope' variable
    for soil_var in ['workability_index', 'toxicity_index', 'rooting_conditions_index', 'oxygen_availability_index',
                         'nutrient_retention_index', 'nutrient_availability_index', 'excess_salts_index']:
        df[soil_var] = df[soil_var].replace({255: np.nan})
    for clim_var in bioclim_var_names:
        df[clim_var] = df[clim_var].replace({-1.700000000000003e+308: np.nan})    

    # Ignore pixels with no agriculture, so 0 or missing calories per ha.
    if log_cal ==True:
        df['calories_per_ha'] = df['calories_per_ha'].replace({np.nan: 0})
        df = df[df['calories_per_ha'] != 0]

    # Transformations
    df['slope'] = df['slope'].apply(lambda x:x-90)
    df['slope'] = df['slope'].apply(lambda x:np.radians(-x))

    for col in (['altitude', 'minutes_to_market','gdp_per_capita']+log_cal*['calories_per_ha']):
        df[str('log_'+col)] = df[col].apply(lambda x: np.log(x) if x != 0 else 0)
        df = df.drop(col,axis=1)

    ## Drop NaN
    df = df.dropna()

    # Cols to drop
    for col in df.columns:
        if ('land_mask' in col) or ('Unnamed:' in col):
            if col in df.columns:
                df = df.drop(col,axis=1)

    # Move log_calories_per_ha to the front.
    if log_cal ==True:
        cols = df.columns.tolist()
        cols.insert(0, cols.pop(cols.index('log_calories_per_ha')))
        df = df.reindex(columns=cols)

    return df