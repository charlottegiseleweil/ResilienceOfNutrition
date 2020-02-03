# Resilience of food sufficiency to future climate and societal changes

## Abstract

Producing sufficient food to meet rising demand is a precondition to food security. While governance, trade, and social justice are critical dimensions of food access and thus food security, change in caloric sufficiency - adequate caloric supply to meet total demand - is a critical concern for resilience of the global food system in the face of climate and societal changes. Here we show, across five scenarios and assuming crop mix adaptation to new climate conditions, that global caloric sufficiency is likely to decrease, despite increased production, because those gains are outweighed by population growth. At a national scale, caloric sufficiency decreases consistently for most countries, and most countries facing hunger today remain vulnerable. Our results suggest that adapting crop mixes to new climate conditions will likely be insufficient to cope with global changes by 2050.


## Getting Started

To be able to run the code, you first need to open a terminal window and navigate to a directory where you want to clone this repository.

Then clone the repository:

```
git clone https://github.com/charlottegiseleweil/ResilienceOfNutrition.git
```

### Prerequisites

This code can be run using a working version of **Python 3.8** and **Jupyter notebook** but we recommend using the provided virtual environment with the **Anaconda** distribution.

If you do not have **Anaconda** installed, you can download the Python 3 version here: https://www.anaconda.com/distribution/


### Install the environment

A virtual environment that contains all the necessary libraries to run the code is provided to spare the user from having to install them one by one.

Navigate to the **ResilienceOfNutrition** folder:

```
cd ResilienceOfNutrition
```

Install the **food_sufficiency** environment using:

```
conda env create -f food_sufficiency.yml
```

To activate the environment:

```
conda activate food_sufficiency
```

## Download the data

You can download the data from **Zenodo** following this link [INSERT LINK].

Place the **data.zip** file in the **ResilienceOfNutrition** folder, then unzip it.

## Run the notebooks

First, make sure to have the latest version of the code. Open a terminal window in the **ResilienceOfNutrition** folder then use:

```
git pull
```

Make sure to update the environment using:

```
conda env update -f food_sufficiency.yml
```

Navigate to the **Final** folder:

```
cd Final
```

Activate the environment:

```
conda activate food_sufficiency
```

You can now access the notebooks using **Jupyter** with:

```
jupyter notebook
```

This command should open a new window in your prefered browser. If it does not, copy and past the link displayed in your terminal into your browser.

## Contents
In folder "Final":

#### **Data_exploration.ipynb** 
This notebook is used to explore the data distribution and the features, verify the aggregation assumption and categorize the GDP per capita.

* Inputs : 
  * data/intermediate/Baseline_df_iterations/with_irrig/baseline_df.csv: the file with the current features for each data point
  * data/intermediate/Future_dfs/All_change+irrig/gdp_cont/original/*: the files with the future predicted features for each data point

* Outputs: 
  * data/intermediate/Baseline_df_iterations/with_irrig/normalized_2000.csv: the standardized data
  * data/intermediate/Baseline_df_iterations/with_irrig/clustered_2000.csv: the clustered data points using K-means
  * data/intermediate/Baseline_df_iterations/with_irrig/normalized_2000_gdp_cat_new.csv: the standardized data with categorized GDP per capita
  * data/intermediate/Baseline_df_iterations/with_irrig/clustered_2000_gdp_cat_new.csv: the clustered data points using K-means with categorized GDP per capita
  
  * data/intermediate/Future_dfs/All_change+irrig/gdp_cont/clustered/*: the future data points clustered with respect to the current clusters
  
  * data/intermediate/Future_dfs/All_change+irrig/gdp_cat_stat/original/*: the files with the future predicted features for each data point with categorized GDP per capita and their standardized equivalent (used later in the model)
  * data/intermediate/Future_dfs/All_change+irrig/gdp_cat_stat/clustered/*: the future data points clustered with respect to the current clusters with categorized GDP per capita
  


#### **Model_training.ipynb**
Trains the model and run predictions on the future datasets.


* Inputs:
  * data/intermediate/Baseline_df_iterations/with_irrig/normalized_2000_gdp_cat_new.csv: used to train our model
  * data/intermediate/Future_dfs/All_change+irrig/gdp_cat_stat/original/model_input_*: used to run the predictions
  * data/inputs/Base/country_ids.csv and data/inputs/Base/country_names.csv: used to get the country name of each data point
  * data/inputs/LU/*: used to get the land use per data point
  * data/inputs/population/*: used to get the population in each data point

* Outputs:
  * data/models/: the models trained used for the future predictions
  * data/outputs/with_irrig/model_output/*: the prediction outputs of the model on every future file
  * data/outputs/with_irrig/composite/*: the prediction outputs for each SSP average over the global circulation models (GCM)
  * data/outputs/with_irrig/compare/*: the composite files merged with the current yields, population, land use and country data, with some preliminary results (yield, cropland change, current and future calories produced per data point, etc.)

#### **Model_results.ipynb**
Used to compute results of the model outputs: change in yields, production, etc.


* Inputs: 
  * data/intermediate/Baseline_df_iterations/with_irrig/normalized_2000_gdp_cat_new.csv: used to get the current yields per data point
  * data/outputs/with_irrig/compare/*: used to get the future predictions and the preliminary results

* Outputs:
  * Figures and maps showing differences between current values and predicted ones

#### **Sufficiency.ipynb** 
Computes caloric sufficiency (global and country-scale) 


* Inputs:
  * data/outputs/with_irrig/compare/*: used to get calorie production 
  * data/inputs/Diet/*: used to get diet information


* Outputs:
  * data/outputs/with_irrig/sufficiency/country_sufficiencies_new.csv: the current and predicted sufficiency for each SSP at country scale
  * data/outputs/with_irrig/sufficiency/suff_map_new.csv: a file with country sufficiency used to create maps with QGIS

#### **CtryCalSuff_in_perspective.ipynb** 

Explores the country sufficiencies into perspective by adding related datasets: import independency, malnutrition, water security, GFSI and GNP per capita.

* Inputs:
  * data/outputs/related_datasets/sufficiencies_input.csv: a copy of the previously created country sufficiency file used as a baseline here
  * data/outputs/related_datasets/Food_security/*: GFSI by country data
  * data/outputs/related_datasets/Food_security/GNP_WorldBank_2018/*: GNP per capita data
  * data/outputs/related_datasets/import_independency/Matti_Kummu_2019/shp_trade_dep.gpkg: import independency data
  * data/outputs/related_datasets/Malnutrition/API_SH.STA.MALN.ZS_DS2_en_csv_v2_49604.csv: malnutrition data
  * data/outputs/related_datasets/Water_Security/GlobalWaterScarcity/*: water security data

* Outputs :
  * data/outputs/related_datasets/sufficiencies_added_data.csv: the country sufficiencies with the added external data
  * data/outputs/related_datasets/sufficiencies_full.csv: the country sufficiencies with extra data, results and corresponding category


## Authors

* **Charlotte Weil**
* **Romain Caristan**


## License

This code is under The MIT License (MIT)
Copyright (c) 2020 Charlotte Weil & Romain Caristan

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
