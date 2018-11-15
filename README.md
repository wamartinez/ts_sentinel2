# ts_sentinel2 

The purpose of this site is to document the process of analysis in python and R of the intra-annual variability of time series of Sentinel 2 imagery for annual land cover mapping. 

# Documentation
The integration of land cover transitions in the classification task has let to a better consistency in the discrimination of intra classes that are difficult to separate using the usual static data perspective. Probably, one drawback in its application has been the lack of dense temporal information that also has high spatial resolution. However, nowadays with the operation of sentinel 2, the research may benefit from the new data available - we never had high spatial resolution images (10 m) with a temporal resolution of 5 days and with an open data policy. 

In this sense, readers can access to the [proposal](https://williamamartinez.github.io/ts_sentinel2/Document/ProposalThesis.pdf) and the following documentation:

So far, these are part of some results of this thesis:

1. Explorative analysis of COS training data set [here]( https://williamamartinez.github.io/ts_sentinel2/ToolR/How_to_remove_outliers_in_time_series.html)

2. Land cover classification using sentinel 2 Imagery: a glance of how to work under static modellling. [here]( https://williamamartinez.github.io/ts_sentinel2/ToolPython/Classification_static_models.html)

3. Graphics of final accuracies using static classification over original images and composites [here](https://williamamartinez.github.io/ts_sentinel2/ToolR/Graphic_Accuracies.html)

Some notes:

Next attempts will involve both a better distribution of the images per seasons and lower amount of labels to classify. On the one hand, corcening the the imagery per season, I would like to reorganize the imagery for the composites according with the climate variability and the particular time frame of seasons in Portugal; for this I will use the package trendgrid (large spatio temporal variability of precipitation and temperature using netcdf files). On he other hand, labels have been static in this analysis so that they must consider also temporal variability. 

