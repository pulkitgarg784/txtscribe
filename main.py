def detect_document(path):
    words = []
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient.from_service_account_json("HackTheNorth-4bd17a719544.json")

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)
    print(response)
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                print(paragraph.words)
                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    words.append(word_text)
    print('text:', " ".join(map(str, words)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

detect_document("photo.jpeg")