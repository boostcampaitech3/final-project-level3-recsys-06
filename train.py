from copy import deepcopy
from turtle import forward
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split
import numpy as np
import pandas as pd
from tqdm import tqdm

data = pd.read_csv('/opt/ml/remove_outlier.csv', index_col=0) # 데이터 전처리 후 추가
num_column = data.shape[1]
data = data.to_numpy()
data = torch.tensor(data, dtype=torch.float32)

#dataset
class nft_dataset(Dataset):
    def __init__(self,data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        x = self.data[idx,1:-1]
        y = self.data[idx,-1].view(1)
        return x,y

dataset = nft_dataset(data)
split=random_split(dataset, [int(len(dataset)*0.8), len(dataset)-int(len(dataset)*0.8)])
trainset,valset = split[0],split[1]


#dataloader
train_loader = DataLoader(
    trainset,
    batch_size=64,
    num_workers=0,
    shuffle=True
)

val_loader = DataLoader(
    valset,
    batch_size=1,
    num_workers=0,
    shuffle=False
)

#model
class linear_model(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(num_column-2,num_column-2),
            nn.Linear(num_column-2,7),
            nn.Linear(7,7),
            nn.Linear(7,3),
            nn.Linear(3,3),
            nn.Linear(3,1),
        )

    def forward(self, data):
        return self.model(data)

model=linear_model()
device = torch.device('cuda')
model.to(device)

#criterion,optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters())

# train
epochs= 30
model.train()
min_loss = np.inf
loss_list=[]
for epoch in tqdm(range(epochs)):
    running_loss = 0
    for i, data in enumerate(train_loader):
        x, y = data
        x, y = x[0].cuda() , y[0].cuda()
        optimizer.zero_grad()
        outputs = model(x)
        loss = criterion(outputs, y)
        running_loss += loss
        loss.backward()
        optimizer.step()
    loss_list.append(running_loss)
    if running_loss < min_loss:
        min_loss = running_loss
        best_model = deepcopy(model.state_dict())

 
with torch.no_grad():
    model.load_state_dict(best_model)
    model.to(device)
    model.eval()
    pred_list=[]
    y_list=[]
    for val_batch in val_loader:
        x, y = val_batch
        x = x[0].to(device)
        y = y[0].to(device)
        outputs = model(x)
        pred_list.append(outputs)
        y_list.append(y)
    
# result = pd.DataFrame()
# result['pred'] = pred_list
# result['y'] = y_list
# result