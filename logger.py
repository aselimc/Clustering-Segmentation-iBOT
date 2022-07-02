from datetime import datetime

import torch
import wandb


CLASS_LABELS_BINARY = {
    0: "background",
    1: "foreground",
    255: "contours"
}

CLASS_LABELS_MULTI = {
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


class WBLogger:

    def __init__(self, args):
        if args.segmentation == "binary":
            self.class_labels = CLASS_LABELS_BINARY
        else:
            self.class_labels = CLASS_LABELS_MULTI

        self.config = {
            "arch": args.arch,
            "epochs": args.epochs,
            "batch_size": args.batch_size,
            "learning_rate": args.lr,
            "patch_size": args.patch_size,
            "number_blocks": args.n_blocks,
            "percentage_train_labels": args.percentage,
            "upsample": args.upsample,
            "segmentation": args.segmentation
            }

        wandb.init(
        project="iBot",
        entity="dl_lab_enjoyers",
        name=datetime.now().strftime('%m.%d.%Y-%H:%M:%S'),
        config=self.config)

    def log_segmentation(self, img, pred_logits, segmentation, step):
        pred_segmentation = wandb.Image(img,
            masks={
                "predictions": {
                    "mask_data": torch.argmax(pred_logits, dim=1).squeeze(0).cpu().numpy(),
                    "class_labels": self.class_labels
                    }
                })
        gt_segmentation = wandb.Image(img,
            masks={
                "ground_truth": {
                    "mask_data": segmentation.squeeze(0).cpu().numpy(),
                    "class_labels": self.class_labels
                    }
                })
        wandb.log({
            "Pred Segmentation": pred_segmentation,
            "GT Segmentation": gt_segmentation},
            step=step)

    def log_scalar(self, scalars, step):
        wandb.log(scalars, step=step)
