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

data = pd.read_csv('/opt/ml/test.csv', index_col=0) # 데이터 전처리 후 추가
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
        x = self.data[idx,:-1]
        y = self.data[idx,-1]
        return x,y

dataset = nft_dataset(data)
split=random_split(dataset, [int(len(dataset)*0.8), int(len(dataset)-len(dataset)*0.8)])
trainset,valset = split[0],split[1]


#dataloader
train_loader = DataLoader(
    trainset,
    batch_size=1,
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
            nn.Linear(num_column-1,1)
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
epochs= 50
model.train()
min_loss = np.inf
for epoch in range(epochs):
    for i, data in tqdm(enumerate(train_loader)):
        x, y = data
        x, y = x[0].cuda() , y[0].cuda()
        optimizer.zero_grad()
        outputs = model(x)
        loss = criterion(outputs, y)
        loss.backward()
        optimizer.step()
        if loss < min_loss:
            min_loss = loss
            best_model = deepcopy(model.state_dict())

 
with torch.no_grad():
    model.load_state_dict(best_model)
    model.to(device)
    model.eval()
    for val_batch in tqdm(val_loader):
        x, y = val_batch
        x = x[0].to(device)
        y = y[0].to(device)
        outputs = model(x)
    print(outputs,y)
    
# TODO 결과 저장하기
# TODO argparser 만들기 (데이터, epoch ...)
# TODO preprocessing 만들기
# TODO 평가 방법 생각? MSE? loss를 MSE로 설정 