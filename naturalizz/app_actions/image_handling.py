from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO

from PIL import Image
from pyinaturalist.models.media import Photo
from requests import get
from streamlit import cache_data


def clear_image_cache() -> None:
    retrieve_and_resize_img_list.clear()


@cache_data(show_spinner=False)
def retrieve_and_resize_img_list(
    _img_list: list[Photo],
    max_height: int = 400,
) -> Image:
    """Retrieve and resize each image of a list."""
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(retrieve_and_resize_img, photo, max_height)
            for photo in _img_list
        ]
        return [future.result() for future in as_completed(futures)]


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
