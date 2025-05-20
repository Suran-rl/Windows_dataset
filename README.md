# Windows_dataset
代码存储于仓库的main与master双分支中，代码库主要包含算法核心逻辑的初步实现。

分支说明：
（1）main分支：包含最优立面选择和立面布局规则化代码
（2）master分支：包含DeeplabV3+和FastSCNN语义分割代码

其中语义分割代码主要实现单张相片的窗户语义分割，为二分语义分割代码。主要通过FastSCNN和DeepLabV3+在LOD3_buildings数据集上找的最优立面影像进行分割。
训练数据集来源：https://github.com/lck1201/win_det_heatmaps

本文已经训练好的权重文件过大暂未上传，如有需要可以联系本人，本人邮箱ruolan@csuft.edu.cn

最后声明，但由于该代码目前侧重于核心流程验证，尚未进行工程优化，尚未达到学术引用标准，建议读者优先引用本文方法论部分而非具体实现。

资源链接
OpenMMLab主页：https://openmmlab.com

OpenMMLab开源语义分割算法库MMSegmentation：https://github.com/open-mmlab/mmsegmentation

AI算力云GPU平台Featurize

https://featurize.cn?s=d7ce99f842414bfcaea5662a97581bd1
