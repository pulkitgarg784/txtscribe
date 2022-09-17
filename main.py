import cohere
co = cohere.Client('dG9FO5NCPecnNjWtiSGAlXmQf3qbkVkBGX2krkBg')

def detect_document(path):
    words = []
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient.from_service_account_json("HackTheNorth-4bd17a719544.json")

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = ''.join([
                        symbol.text for symbol in word.symbols
                    ])
                    words.append(word_text)
    return(" ".join(map(str, words)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

test_str = detect_document("photo.jpeg")
print(test_str)
training_data = "This is a spell check generator that fixes samples of text.\n\nSample: a new type OF aurora FounD on saturn resolves a planetary mystery\nFixed: A new type of aurora found on saturn resolves a planetary mystery\n--\nSample: online Shopping is ReSHaping Real-world Cities\nFixed: Online shopping is reshaping real-world cities\n--\nSample: When you close 100 TAbs AFter Finding THE SoluTion To A BuG\nFixed: When you close 100 tabs after finding the solution to a bug\n--\nSample: masteing DYNAmIC ProGrammING\nFixed: Mastering dynamic programming\n--\nSample: "+test_str+"\nFixed:"
response = co.generate(
  model='large',
  prompt=training_data,
  max_tokens=50,
  temperature=0.3,
  k=0,
  p=0.75,
  frequency_penalty=0,
  presence_penalty=0,
  stop_sequences=["--"],
  return_likelihoods='NONE')
print('Prediction: {}'.format(response.generations[0].text))