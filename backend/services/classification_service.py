from pathlib import Path
from io import BytesIO
from typing import Tuple

def _model_path(filename: str = 'game_model.pth') -> Path:
    root = Path(__file__).resolve().parents[2]
    return root / 'ml' / 'Classification model' / filename

def load_model(filename: str = None):
    try:
        import torch
        from torch import nn
    except Exception:
        raise RuntimeError('PyTorch is required for classification model')

    fn = filename or 'game_model.pth'
    path = _model_path(fn)
    if not path.exists():
        raise FileNotFoundError(f'Classification model not found at {path}')

    device = 'cpu'
    loaded = torch.load(path, map_location=device)
    
    if isinstance(loaded, nn.Module):
        model = loaded
    elif isinstance(loaded, dict):
        try:
            from torchvision.models import resnet50, resnet18, vgg16
            model = resnet50(num_classes=1000)
            if 'state_dict' in loaded:
                model.load_state_dict(loaded['state_dict'])
            else:
                model.load_state_dict(loaded)
        except Exception:
            try:
                model = resnet18(num_classes=1000)
                if 'state_dict' in loaded:
                    model.load_state_dict(loaded['state_dict'])
                else:
                    model.load_state_dict(loaded)
            except Exception:
                raise RuntimeError(f'Could not reconstruct model from state dict')
    else:
        raise RuntimeError(f'Loaded object is neither nn.Module nor dict: {type(loaded)}')
    
    if isinstance(model, nn.Module):
        model.eval()
    return model

def _load_class_names(path: Path):
    j = path.with_suffix('.json')
    txt = path.with_suffix('.txt')
    if j.exists():
        try:
            import json
            return json.loads(j.read_text())
        except Exception:
            pass
    if txt.exists():
        try:
            return [l.strip() for l in txt.read_text().splitlines() if l.strip()]
        except Exception:
            pass
    return None

def predict_image(image_bytes: bytes) -> Tuple[str, str]:
    import logging
    logger = logging.getLogger("classification")
    
    try:
        import torch
        from torchvision import transforms
        from PIL import Image
        import numpy as np
    except Exception as e:
        logger.error(f"Import error: {e}")
        return ('Unknown Game', 'Game')

    try:
        model = load_model()
        logger.debug("Model loaded")
    except Exception as e:
        logger.error(f"Model load error: {e}")
        return ('Unknown Game', 'Game')

    try:
        img = Image.open(BytesIO(image_bytes)).convert('RGB')
        logger.debug(f"Image opened: {img.size}")
    except Exception as e:
        logger.error(f"Image load error: {e}")
        return ('Unknown Game', 'Game')

    tf = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])
    ])

    x = tf(img).unsqueeze(0)
    logger.debug(f"Tensor shape: {x.shape}")
    
    idx = None
    try:
        with torch.no_grad():
            out = model(x)
            logger.debug(f"Model output type: {type(out)}, shape: {out.shape if hasattr(out, 'shape') else 'N/A'}")
            if hasattr(out, 'numpy'):
                probs = out.numpy()
            else:
                probs = out.cpu().numpy()
            idx = int(np.argmax(probs, axis=1)[0])
            logger.debug(f"Predicted class index: {idx}")
    except Exception as e:
        logger.error(f"Inference error (attempt 1): {e}")
        try:
            logits = model(x)
            idx = int(np.argmax(logits.cpu().numpy(), axis=1)[0])
            logger.debug(f"Predicted class index (fallback): {idx}")
        except Exception as e2:
            logger.error(f"Inference error (attempt 2): {e2}")
            return ('Unknown Game', 'Game')

    cls_names = _load_class_names(Path(model.__dict__.get('_get_name', '') or ''))
    if cls_names is None:
        if hasattr(model, 'classes'):
            cls_names = list(model.classes)
            logger.debug(f"Class names from model.classes: {len(cls_names)}")
        elif hasattr(model, 'idx_to_class'):
            cls_names = list(model.idx_to_class)
            logger.debug(f"Class names from model.idx_to_class: {len(cls_names)}")

    if cls_names and 0 <= idx < len(cls_names):
        name = cls_names[idx]
        logger.info(f"Predicted: {name} (idx={idx})")
    else:
        name = f'Predicted Game {idx}'
        logger.warning(f"No class names found or idx out of range. Using: {name}")

    return (name, 'Game')

