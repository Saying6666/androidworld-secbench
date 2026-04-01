from pathlib import Path

try:
    import numpy as np
except ImportError:  # pragma: no cover - optional dependency during static setup
    np = None

try:
    from PIL import Image
except ImportError:  # pragma: no cover - optional dependency during static setup
    Image = None


class ImageLogger:
    def __init__(self, output_dir: str = "outputs/reports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def log_image(self, filename: str, image):
        save_path = self.output_dir / filename
        save_path.parent.mkdir(parents=True, exist_ok=True)

        if isinstance(image, str):
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(image)
            return str(save_path)

        if hasattr(image, "save"):
            image.save(save_path)
            return str(save_path)

        if np is not None and isinstance(image, np.ndarray):
            if Image is None:
                with open(save_path, "w", encoding="utf-8") as f:
                    f.write(repr(image))
                return str(save_path)

            pil_image = Image.fromarray(image.astype("uint8"))
            pil_image.save(save_path)
            return str(save_path)

        with open(save_path, "w", encoding="utf-8") as f:
            f.write(repr(image))
        return str(save_path)

    def log_text_image_stub(self, filename: str, content: str):
        return self.log_image(filename=filename, image=content)
