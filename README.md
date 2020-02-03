# Resilience of food sufficiency to future climate and societal changes

Producing sufficient food to meet rising demand is a precondition to food security. While governance, trade, and social justice are critical dimensions of food access and thus food security, change in caloric sufficiency - adequate caloric supply to meet total demand - is a critical concern for resilience of the global food system in the face of climate and societal changes. Here we show, across five scenarios and assuming crop mix adaptation to new climate conditions, that global caloric sufficiency is likely to decrease, despite increased production, because those gains are outweighed by population growth. At a national scale, caloric sufficiency decreases consistently for most countries, and most countries facing hunger today remain vulnerable. Our results suggest that adapting crop mixes to new climate conditions will likely be insufficient to cope with global changes by 2050.


## Getting Started

To be able to run the code, you first need to open a terminal window and navigate to a directory where you want to clone this repository.

Then clone the repository:

```
git clone https://github.com/charlottegiseleweil/ResilienceOfNutrition.git
```

### Prerequisites

This code can be run using a working version of **Python 3.8** and **Jupyter notebook** but we recommend using the provided environment with the **Anaconda** distribution.

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

To activate the environment you can simply use

```
conda activate food_sufficiency
```

and

```
conda deactivate
```

to return to your base environment.

If you want to remove the environment, use:

```
conda env remove -n food_sufficiency
```


## Download the data

You can download the data from **Zenodo** following this link [INSERT LINK].

Place the **data.zip** file in the **ResilienceOfNutrition** folder then unzip it.

## Run the notebooks

To run the notebooks, open a terminal window in the **ResilienceOfNutrition** folder.

Make sure to navigate to the **Final** folder using:

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

* **Data_exploration** - Used to explore the data distribution and the features, verify the aggregation assumption and categorize the GDP per capita.
* **Model_training** - Used to train the model and run predictions on the future datasets.
* **Model_results** - Used to compute results of the model outputs: change in yields, production, etc.
* **sufficiency** - Used to compute the global and country sufficiencies
* **CtryCalSuff_in_perspective** - Put the country sufficiencies into perspective by adding related datasets such as import independency, malnutrition, water security, GFSI and GNP per capita.

## Authors

* **Charlotte Weil**
* **Romain Caristan**


## License

This code is under The MIT License (MIT)
Copyright (c) 2020 Charlotte Weil & Romain Caristan

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
