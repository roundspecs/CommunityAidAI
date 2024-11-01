from PIL import Image
from transformers import BlipForConditionalGeneration, BlipProcessor


class CaptionService:
    def __init__(self):
        model_name = "Salesforce/blip-image-captioning-large"
        self.processor = BlipProcessor.from_pretrained(model_name)
        self.model = BlipForConditionalGeneration.from_pretrained(model_name).to("mps")  # type: ignore

    def generate_caption(self, image_path: str) -> str:
        image = Image.open(image_path)
        inputs = self.processor(images=image, return_tensors="pt").to("mps")  # type: ignore
        outputs = self.model.generate(**inputs)  # type: ignore
        caption = self.processor.decode(outputs[0], skip_special_tokens=True)  # type: ignore
        return caption
