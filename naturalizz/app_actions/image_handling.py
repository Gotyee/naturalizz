from io import BytesIO

from PIL import Image
from pyinaturalist.models.media import Photo
from requests import get


def retrieve_and_resize_img_list(img_list: list[Photo], max_height: int = 400) -> Image:
    """Retrieve and resize each image of a list."""
    print(img_list)
    return [retrieve_and_resize_img(photo, max_height) for photo in img_list]


def retrieve_and_resize_img(photo: Photo, max_height: int = 400) -> Image:
    """Retrieve image from Photo class and resize it."""
    if not photo:
        return _fill_unfound_images(max_height)
    url = photo.url_size("medium") or photo.url
    response = get(url, timeout=10)
    image = Image.open(BytesIO(response.content))
    return _resize_img(image, max_height)


def _resize_img(image: Image, max_height: int) -> Image:
    """Resize image according to maximum height whil keeping aspect ratio."""
    width, height = image.size
    aspect_ratio = width / height
    new_width = int(max_height * aspect_ratio)
    return image.resize((new_width, max_height))


def _fill_unfound_images(max_height: int) -> Image:
    return _resize_img(Image.open("naturalizz/media/image_filler.jpg"), max_height)
