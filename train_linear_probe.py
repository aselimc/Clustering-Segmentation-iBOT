import argparse
from datetime import datetime
from random import choices, shuffle
import torch
import torch.nn as nn
import torch.optim as optim
import wandb


from utils import mIoU, MaskedCrossEntropyLoss
from dataloader import PartialDatasetVOC
from torchvision import datasets
import torchvision.transforms as transforms
import torch.nn.functional as Fun
from tqdm import tqdm
from transforms import *
from torch.utils.data import DataLoader
import models
from models.classifier import ConvLinearClassifier
from torch.utils.tensorboard import SummaryWriter


CLASS_LABELS = {
    0: "background",
    1: "aeroplane",
    2: "bicycle",
    3: "bird",
    4: "boat",
    5: "bottle",
    6: "bus",
    7: "car",
    8: "cat",
    9: "chair",
    10: "cow",
    11: "diningtable",
    12: "dog",
    13: "horse",
    14: "motorbike",
    15: "person",
    16: "pottedplant",
    17: "sheep",
    18: "sofa",
    19: "train",
    20: "tvmonitor",
    255: "contours"
}

global_step = 0

def parser_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=str, default="data")
    parser.add_argument('--weights', type=str, default="weights/ViT-S16.pth")
    parser.add_argument('--arch', type=str, default="vit_small")
    parser.add_argument('--patch_size', type=int, default=16)
    parser.add_argument('--epochs', type=int, default=100)
    parser.add_argument('--n_blocks', type=int, default=4)
    parser.add_argument('--batch_size', type=int, default=32)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--percentage", type=float, default=0.1)
    parser.add_argument("--upsample", type=str, choices=['nearest', 'bilinear'], default='nearest')

    return parser.parse_args()

def train(loader, backbone, classifier, criterion, optimizer, n_blocks):
    global global_step
    backbone.eval()
    loss_l = []

    progress_bar = tqdm(total=len(loader))
    for img, segmentation in loader:
        optimizer.zero_grad()
        img = img.cuda()
        segmentation = segmentation.cuda()
        with torch.no_grad():
            intermediate_output = backbone.get_intermediate_layers(img, n_blocks)
            output = torch.cat([x[:, 1:] for x in intermediate_output], dim=-1).detach()
        pred_logits = classifier(output)

        loss = criterion(pred_logits, segmentation)
        loss.backward()
        optimizer.step()

        loss_l.append(loss.item())
        progress_bar.update()
        global_step += 1

    return np.mean(np.array(loss_l))


def validate(loader, backbone, classifier, criterion, n_blocks):
    backbone.eval()
    classifier.eval()
    val_loss = []
    miou_arr = []
    random_pic_select = np.random.randint(len(loader))
    for idx, (img, segmentation) in enumerate(loader):
        img = img.cuda()
        segmentation = segmentation.cuda()
        with torch.no_grad():
            intermediate_output = backbone.get_intermediate_layers(img, n_blocks)
            output = torch.cat([x[:, 1:] for x in intermediate_output], dim=-1).detach()
        pred_logits = classifier(output)

        # mask contours: compute pixelwise dummy entropy loss then set it to 0.0
        loss = criterion(pred_logits, segmentation)
        val_loss.append(loss.item())
        miou = mIoU(pred_logits, segmentation)
        miou_arr.append(miou.item())

        if random_pic_select==idx:
            print("Adding Image Example to Logger")
            pred_segmentation = wandb.Image(img[0],
                masks={
                    "predictions": {
                        "mask_data": torch.argmax(pred_logits, dim=1).squeeze(0).cpu().numpy(),
                        "class_labels": CLASS_LABELS
                        }
                    })
            gt_segmentation = wandb.Image(img[0],
                masks={
                    "ground_truth": {
                        "mask_data": segmentation.squeeze(0).cpu().numpy(),
                        "class_labels": CLASS_LABELS
                        }
                    })
            wandb.log({
                "Pred Segmentation": pred_segmentation,
                "GT Segmentation": gt_segmentation},
                step=global_step)

    return np.mean(np.array(miou_arr)), np.mean(np.array(val_loss))


def main(args):
    config = {
        "arch": args.arch,
        "epochs": args.epochs,
        "batch_size": args.batch_size,
        "learning_rate": args.lr,
        "patch_size": args.patch_size,
        "number_blocks": args.n_blocks,
        "percentage_train_labels": args.percentage,
    }
    
    wandb.init(
        project="iBot",
        entity="dl_lab_enjoyers",
        name=datetime.now().strftime('%m.%d.%Y-%H:%M:%S'),
        config=config)

    # Loading the backbone
    backbone = models.__dict__[args.arch](
        patch_size=args.patch_size,
        return_all_tokens=True,
    )

    state_dict = torch.load(args.weights)['state_dict']
    backbone.load_state_dict(state_dict)
    backbone = backbone.cuda()
    
        
    for param in backbone.parameters():
        param.requires_grad = False

    n_blocks = args.n_blocks
    embed_dim = backbone.embed_dim * n_blocks
    classifier = ConvLinearClassifier(embed_dim, n_classes=21, upsample_mode=args.upsample).cuda()

    ## TRAINING DATASET ##
    train_transform = Compose([
        RandomCrop(224),
        PILToTensor(),
        RandomHorizontalFlip(),
        Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
    ])

    train_dataset = PartialDatasetVOC(percentage = args.percentage, root=args.root, image_set='train', download=False, transforms=train_transform)
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size)
    val_dataset = datasets.VOCSegmentation(root=args.root, image_set='val', download=False, transforms=train_transform)
    val_loader = DataLoader(val_dataset, batch_size=1)

    optimizer = optim.SGD(
        classifier.parameters(),
        args.lr * args.batch_size / 256.0,
        momentum=0.9,
        weight_decay=0
    )
    lr_scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, args.epochs, eta_min=0)

    criterion = MaskedCrossEntropyLoss()

    ############## TRAINING LOOP #######################

    for epoch in range(args.epochs):
        mean_loss = train(train_loader, backbone, classifier, criterion, optimizer, n_blocks)
        print(f"For epoch number {epoch} --> Average Loss {mean_loss:.2f}")
        wandb.log({"training_loss": mean_loss}, step=global_step)
        if epoch % 10 == 0:
            miou, loss = validate(val_loader, backbone, classifier, criterion, n_blocks)
            print(f"Validation for epoch {epoch}: Average mIoU {miou}, Average Loss {loss}")
            wandb.log({
                "val_loss": loss,
                "val_miou": miou
            })
        
        lr_scheduler.step()

def cosine_scheduler(base_value, final_value, epochs, niter_per_ep, warmup_epochs=0, start_warmup_value=0):
    iters = np.arange(epochs * niter_per_ep)
    schedule = final_value + 0.5 * (base_value - final_value) * (1 + np.cos(np.pi * iters / len(iters)))
    return schedule

def show_img(img):
    img_pil = transforms.functional.to_pil_image(img)
    img_pil.save("dum1.png")


if __name__ == '__main__':
    args = parser_args()
    main(args)
