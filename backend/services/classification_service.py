from pathlib import Path
from io import BytesIO
from typing import Tuple, List
import torch
import torch.nn as nn
from torch.serialization import add_safe_globals
from torchvision import models
from PIL import Image
from torchvision import transforms
import types, sys


main_module = types.ModuleType("__main__")
sys.modules["__main__"] = main_module


GAME_CLASSES: List[str] = [
    "Among Us", "Celeste", "Cyberpunk 2077", "Devil May Cry 5", "GTA V",
    "God of War", "Hades", "Hollow Knight", "Inscryption", "Outer Wilds",
    "Persona 4 Golden", "Persona 5 Royal", "Red Dead Redemption 2",
    "Resident Evil 4", "Stardew Valley", "Stray", "Terraria",
    "Undertale", "Yakuza 0"
]

GENRE_CLASSES: List[str] = ["Adventure", "Brawler", "Platform", "RPG", "Strategy"]



class TwoHeadModel(nn.Module):
    def __init__(self, num_game_classes=19, num_genre_classes=5):
        super().__init__()

        self.feature_extractor = models.efficientnet_b0(
            weights=models.EfficientNet_B0_Weights.IMAGENET1K_V1
        )

        num_features = self.feature_extractor.classifier[1].in_features
        self.feature_extractor.classifier = nn.Identity()

        self.game_head = nn.Sequential(
            nn.Dropout(0.2),
            nn.Linear(num_features, num_game_classes)
        )

        self.genre_head = nn.Sequential(
            nn.Dropout(0.2),
            nn.Linear(num_features, num_genre_classes)
        )

    def forward(self, x):
        features = self.feature_extractor(x)
        game_output = self.game_head(features)
        genre_output = self.genre_head(features)
        return game_output, genre_output


add_safe_globals([TwoHeadModel])
main_module.TwoHeadModel = TwoHeadModel




def _model_path(filename: str = "game_classifier.pth") -> Path:
    root = Path(__file__).resolve().parents[2]
    return root / "ml" / "Classification model" / filename


def load_model(filename: str = None):
    path = _model_path(filename or "game_classifier.pth")
    if not path.exists():
        raise FileNotFoundError(f"Classification model not found at {path}")

    checkpoint = torch.load(path, map_location="cpu", weights_only=False)

    if isinstance(checkpoint, TwoHeadModel):
        model = checkpoint

    elif isinstance(checkpoint, dict):
        model = TwoHeadModel(
            num_game_classes=len(GAME_CLASSES),
            num_genre_classes=len(GENRE_CLASSES)
        )
        if "state_dict" in checkpoint:
            model.load_state_dict(checkpoint["state_dict"])
        else:
            model.load_state_dict(checkpoint)

    else:
        raise RuntimeError("Unknown checkpoint format for classifier")

    model.eval()
    return model


def predict_image(image_bytes: bytes) -> Tuple[str, List[str]]:
    try:
        model = load_model()
    except Exception as e:
        print("Model load error:", e)
        return ("unknown", ["Strategy"])

    tf = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485,0.456,0.406], [0.229,0.224,0.225])
    ])

    try:
        img = Image.open(BytesIO(image_bytes)).convert("RGB")
        x = tf(img).unsqueeze(0)
    except:
        return ("unknown", ["Strategy"])

    try:
        with torch.no_grad():
            game_logits, genre_logits = model(x)

        game_idx = int(torch.argmax(game_logits, dim=1).item())
        genre_idx = int(torch.argmax(genre_logits, dim=1).item())

    except Exception as e:
        print("Inference error:", e)
        return ("unknown", ["Strategy"])

    title = GAME_CLASSES[game_idx] if 0 <= game_idx < len(GAME_CLASSES) else "unknown"
    genre = GENRE_CLASSES[genre_idx] if 0 <= genre_idx < len(GENRE_CLASSES) else "Strategy"

    return (title, [genre])
