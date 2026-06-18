import warnings
warnings.filterwarnings("ignore")
import os
import torch
import sys

# 将项目根目录添加到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.options import Options
from src.dataset import Test_Imputation
from tqdm import tqdm
import numpy as np
import scanpy as sc
import pandas as pd

from src.utils import *
from src.model import ImputeModule

# 预测 SC 中存在但 ST 中缺失的 Genes
opt = Options().parse()
opt.kfold = 0 # 选择使用第几个fold的模型
dataset = 'Dataset1'


# 选择对应数据集
st_path = f'./dataset/{dataset}/Insitu_count.h5ad'
sc_path = f'./dataset/{dataset}/scRNA_count_cluster.h5ad'

ST_adata = sc.read(st_path)
SC_adata = sc.read(sc_path)

print(ST_adata, '\n', SC_adata)

valdataset = Test_Imputation(opt, istrain='val')

gene_names, cell_names = valdataset.get_eval_names()

valdataloader = torch.utils.data.DataLoader(
    valdataset, 
    batch_size=opt.batch_size, 
    shuffle=False, 
    num_workers=0
)
opt.sc_dim = valdataset.get_cluster_dim()

model = ImputeModule(opt)
if opt.parallel:
    model = torch.nn.DataParallel(model).cuda().module
else:
    model = model.to(torch.device('cuda:%d'%(opt.gpu)))
    
model_path = f'./SpaIM_results/{dataset}/last_%d.pth'%(opt.kfold)
print('model_path:',model_path)

model.load(model_path)

with torch.no_grad():
    eval_result = None
    input_result = None
    for i, (seq, st_style) in enumerate(valdataloader):
        inputs = {
            'scx': seq,
            'st_style': st_style
        }
        # print('SCX:', inputs['scx'].shape, len(st_style))
        model.set_input(inputs, istrain=0)
        out = model.inference()
        impute_result = out['st_fake'].detach().cpu().numpy()
        print("impute_result",impute_result.shape) #  (3482, 67798) torch.Size([3482, 67798])
        eval_result = impute_result if eval_result is None else np.concatenate((eval_result, impute_result), axis=0)
        print("eval_result", eval_result.shape)  # (3482, 77890) (3482, 77890)


eval_result = eval_result.T
# print(eval_result[0][:10])
eval_result[eval_result <0] = 0

# print(gene_names.shape)  # 检查 gene_names 的形状
# print(cell_names.shape)  # 检查 cell_names 的形状
df1 = pd.DataFrame(eval_result.T, index=cell_names, columns=gene_names)
df1.to_pickle(os.path.join(opt.save_path, 'impute_sc_result_%d.pkl'%(opt.kfold)))
