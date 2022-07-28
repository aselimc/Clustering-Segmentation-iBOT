# Clustering Segmentation based on iBOT
Studying well-structuredness of 
<a href="https://github.com/bytedance/ibot">iBOT's</a> learned feature space using 
Linear Probing, K-Nearest Neighbors, K-Means and Agglomerative Clustering.
<img src=".github/Clustering_Segmentation_Overview.png">

## Installation
System Requirements:
* Python 3.7.9
* Cuda 11.0

Install packages by running
```sh
pip install -r requirements.txt
```

Make sure to download the <a href="http://host.robots.ox.ac.uk/pascal/VOC/voc2012/index.html">PASCAL VOC Dataset</a> and the models pretrained on ImageNet-22K:
<ul>
  <li> ViT-Base: <a href=https://lf3-nlp-opensource.bytetos.com/obj/nlp-opensource/archive/2022/ibot/vitb_16_pt22k/checkpoint.pth> full cpkt </a>
  <li> ViT-Large: <a href="https://lf3-nlp-opensource.bytetos.com/obj/nlp-opensource/archive/2022/ibot/vitl_16_pt22k/checkpoint.pth"> full cpkt </a>
</ul>

## Evaluation
Each method can be evaluated by running its respective script
```sh
python eval_linear.py
python eval_knn.py
python eval_kmeans.py
python eval_agglomerative.py.py
```
together with the specified settings. For further details, please either run the script
with a `--help` flag or refer to our provided example 
<a href="https://github.com/aselimc/iBot-cv/tree/main/example">bash scripts</a>.

## Segmentation

<table>
  <tr>
    <td><img src=".github\segmentation\bus.png"></td>
    <td><img src=".github\segmentation\motorbike.png"></td>
    <td><img src=".github\segmentation\plane.png"></td>
    <td><img src=".github\segmentation\train.png"></td>
  </tr>
  <tr>
  <td><img src=".github\segmentation\kid.png"></td>
  <td><img src=".github\segmentation\women.png"></td>
  <td><img src=".github\segmentation\dog.png"></td>
  <td><img src=".github\segmentation\cat.png"></td>
  </td>
</table>

## Mean Intersection over Union
Linear Probing
<table>
  <tr>
    <td>Arch</td>
    <td colspan=3 align="center">Intermediate</td>
    <td colspan=3 align="center">Query</td>
    <td colspan=3 align="center">Key</td>
    <td colspan=3 align="center">Value</td>
  </tr>
  <tr>
    <td></td>
    <td>10%</td>
    <td>50%</td>
    <td>100%</td>
    <td>10%</td>
    <td>50%</td>
    <td>100%</td>
    <td>10%</td>
    <td>50%</td>
    <td>100%</td>
    <td>10%</td>
    <td>50%</td>
    <td>100%</td>
  </tr>
  <tr>
    <td>ViT-Base</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>ViT-Large</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
</table>

KNN
<table>
  <tr>
    <td>Arch</td>
    <td colspan=3 align="center">Intermediate</td>
    <td colspan=3 align="center">Query</td>
    <td colspan=3 align="center">Key</td>
    <td colspan=3 align="center">Value</td>
  </tr>
  <tr>
    <td></td>
    <td>10%</td>
    <td>50%</td>
    <td>100%</td>
    <td>10%</td>
    <td>50%</td>
    <td>100%</td>
    <td>10%</td>
    <td>50%</td>
    <td>100%</td>
    <td>10%</td>
    <td>50%</td>
    <td>100%</td>
  </tr>
  <tr>
    <td>ViT-Base</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>ViT-Large</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
</table>

KMeans
<table>
  <tr>
    <td>Arch</td>
    <td colspan=3 align="center">Intermediate</td>
    <td colspan=3 align="center">Query</td>
    <td colspan=3 align="center">Key</td>
    <td colspan=3 align="center">Value</td>
  </tr>
  <tr>
    <td></td>
    <td>10%</td>
    <td>50%</td>
    <td>100%</td>
    <td>10%</td>
    <td>50%</td>
    <td>100%</td>
    <td>10%</td>
    <td>50%</td>
    <td>100%</td>
    <td>10%</td>
    <td>50%</td>
    <td>100%</td>
  </tr>
  <tr>
    <td>ViT-Base</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>ViT-Large</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
</table>

Agglomerative Clustering
<table>
  <tr>
    <td>Arch</td>
    <td colspan=3 align="center">Intermediate</td>
    <td colspan=3 align="center">Query</td>
    <td colspan=3 align="center">Key</td>
    <td colspan=3 align="center">Value</td>
  </tr>
  <tr>
    <td></td>
    <td>10%</td>
    <td>50%</td>
    <td>100%</td>
    <td>10%</td>
    <td>50%</td>
    <td>100%</td>
    <td>10%</td>
    <td>50%</td>
    <td>100%</td>
    <td>10%</td>
    <td>50%</td>
    <td>100%</td>
  </tr>
  <tr>
    <td>ViT-Base</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
  <tr>
    <td>ViT-Large</td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
    <td></td>
  </tr>
</table>