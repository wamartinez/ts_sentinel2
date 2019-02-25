# ts_sentinel2

## Intra-annual land cover mapping

The purpose of this site is to document the process of analysis in python and R of the thesis titled "Automatic Training Sampling for Intra-annual Land Cover Mapping at Central of Portugal.".

# Abstract

Making operational efficient the production of Land Use Land cover (LULC) mapping over large areas as the consistency and accuracy keep a high quality is an essential condition for the implementation of applications that require periodic information, such as forest fire propagation, crop monitoring or climate models. The increasing spatial and temporal resolution satellite images, such as those provided by Sentinel 2, open new opportunities for producing accurate datasets that can improve the lack of production of global and regional LULC maps with fine scale and up-to-date information. In this context, while this thesis aimed to make automatic the generation of intra-annual maps implementing a workflow that consists of supervised classification in synergy with automatic extraction of training samples from an old map, it also aimed to use singular and BAP composites. Therefore, after a preliminary selection and preprocessing of the implemented spectral bands in the classification both from single and BAP composites of Sentinel 2 images of 2017, a random selection of training points is extracted from an old reference map; national LULC map of Portugal, COS 2015. We performed a classification scheme using support vector machine (SVM) and Random forest (RF) classifiers with two datasets of six and nine different number of land cover classes. The out-of-date information derived from the old map led us to evaluate the viability of implementing two refining procedures over the data to improve accuracy; one based on margins of NDVI signals and another based on an iterative learning procedure. Since the proposed methodologies did not lead to improving OA on the classification of any of the images of 2017, we questioned for robustness of the classifiers RF and SVM by injecting different levels of noise during the modeling. Finally, the free cloud and phenological maximization of the BAP composites become in a consistent and efficient input for the production of seasonal LULC mapping.

The complete report can be found [here](https://williamamartinez.github.io/ts_sentinel2/Document/Thesis_index_wm.pdf)

Moreover, this thesis had a focus on processing Sentinel 2 data products in Python and R.

Readers interested in the used scripts in R to achieve the proposed objectives can be found [here](https://williamamartinez.github.io/ts_sentinel2/ToolR/UncertantyMaps.html)
