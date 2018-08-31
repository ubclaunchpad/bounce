"""Defines an interface for storing and retreiving images."""

import os
from enum import Enum


class EntityType(Enum):
    """Represents types of entities for which images are stored."""
    USER = 'user'
    CLUB = 'club'


def save(directory,
         entity_type,
         entity_id,
         image_name,
         image_content,
         must_exist=False):
    """Saves the given image and returns the path to the image."""
    path = os.path.join(directory, entity_type.value, str(entity_id),
                        image_name)
    if must_exist and not os.path.exists(path):
        raise FileNotFoundError(f'No such image {path}')
    else:
        # Create the directory(s) to store the file in before creating it
        os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as image_file:
        image_file.write(image_content)
    return path


def load(directory, entity_type, entity_id, image_name):
    """Returns the image by the given name."""
    with open(
            os.path.join(directory, entity_type.value, str(entity_id),
                         image_name), 'rb') as image_file:
        image = image_file.read()
    return image


def delete(directory, entity_type, entity_id, image_name, must_exist=False):
    """Deletes the image by the given name."""
    path = os.path.join(directory, entity_type.value, str(entity_id),
                        image_name)
    if os.path.exists(path):
        os.remove(path)
    elif must_exist:
        raise FileNotFoundError(f'No such image {path}')


def delete_dir(directory, entity_type, entity_id, must_exist=False):
    """Deletes the directory by the given name."""
    path = os.path.join(directory, entity_type.value, str(entity_id))
    if os.path.exists(path):
        os.remove(path)
    elif must_exist:
        raise FileNotFoundError(f'No such image {path}')
