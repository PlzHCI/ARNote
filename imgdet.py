def localize_objects(path, api_key):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    from google.cloud import vision

    client = vision.ImageAnnotatorClient(
        client_options={"api_key": api_key}
    )

    with open(path, "rb") as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    print(f"Number of objects found: {len(objects)}")
    for object_ in objects:
        print(f"\n{object_.name} (confidence: {object_.score})")
        print("Normalized bounding polygon vertices: ")
        for vertex in object_.bounding_poly.normalized_vertices:
            print(f" - ({vertex.x}, {vertex.y})")


if __name__ == "__main__":
    localize_objects(
        "images/dog.jpg", "AIzaSyD_HTxDrvB0L4r5c2OF80XRRehMTJ0ab9w")
