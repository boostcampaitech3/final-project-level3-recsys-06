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
from torchmetrics import MeanAbsolutePercentageError

data = pd.read_csv('/opt/ml/property_dummy.csv', index_col=0) # 데이터 전처리 후 추가
num_column = data.shape[1]
data = data.to_numpy()
data = torch.tensor(data, dtype=torch.float32)

all_data = pd.read_csv('/opt/ml/all_property_dummy.csv', index_col=0)
all_data = all_data.to_numpy()
all_data = torch.tensor(all_data, dtype=torch.float32)

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

class all_dataset(Dataset):
    def __init__(self,data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        x = self.data[idx,1:]
        return x

trainset = nft_dataset(data)
all_set = all_dataset(all_data)


#dataloader
train_loader = DataLoader(
    trainset,
    batch_size=32,
    num_workers=0,
    shuffle=True
)

val_loader = DataLoader(
    all_set,
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
            nn.Linear(num_column-2,(num_column-2)//2),
            nn.Linear((num_column-2)//2,(num_column-2)//4),
            nn.Linear((num_column-2)//4,(num_column-2)//8),
            nn.Linear((num_column-2)//8,1)
        )
    def forward(self, data):
        return self.model(data)

model=linear_model()
device = torch.device('cuda')
model.to(device)

#criterion,optimizer

# criterion = nn.MSELoss()
criterion = MeanAbsolutePercentageError().to(device)
optimizer = optim.Adam(model.parameters())

# train
epochs= 50
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
        x = val_batch
        x = x[0].to(device)
        outputs = model(x)
        pred_list.append(outputs.item())

result = pd.DataFrame(pred_list)
result.to_csv('result.csv')