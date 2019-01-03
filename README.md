# ts_sentinel2 

The purpose of this site is to document the process of analysis in python and R of the intra-annual variability of time series of Sentinel 2 imagery for land cover mapping of composites.

# Summary

The accuracy of the training set in the supervised classification is essential to perform good mapping. However, in real world projects this assumption is hard to achieve since the sampling usually come from different sources regarding the imagery to classify. For example, in this project our reference COS data come from aerial interpretation that turns out the sampling for the classification of Sentinel 2 imagery of 2017 in central of Portugal. Besides that. COS data differs in date respect the imagery, since this was collected during 2015. In this sense, different sources of reference data and different dates turn out in a misregistration of what truly was happening in the ground. Therefore, I propose a iterative learning workflow based on entropies where we can trace the most informative sampling that contribute to a better mapping of certain image for certain period. Moreover, this thesis, under the new paradigm in remote sensing of the best available pixel (BAP) composites (White et al., 2014), proposes to compose images by season. This approach generally benefits classification task in areas with frequent cloudy conditions. However, in this thesis beyond that purpose, it also look for reducing the spatial variation of the crop rotation between an image and another.

I have creted the following documentation for future users of the methodology

1. Explorative analysis of COS training data set [here]( https://williamamartinez.github.io/ts_sentinel2/ToolR/How_to_remove_outliers_in_time_series.html)

2. Land cover classification using sentinel 2 Imagery: a glance of how to work under static modellling. [here]( https://williamamartinez.github.io/ts_sentinel2/ToolPython/Classification_weighted_landcover.html)

3. Analysis of results [here](https://williamamartinez.github.io/ts_sentinel2/ToolR/UncertantyMaps.html)

4. Animation NDVI and training COS in Portugal [here](https://stsentinel.shinyapps.io/animation_ndvi_r/)


