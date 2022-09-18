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

test_str = detect_document("note.jpeg")
print("Scanned Text:",test_str)
training_data = "This is a spell check generator that fixes samples of text.\n\nSample: a new type OF aurora FounD on saturn resolves a planetary mystery\nFixed: A new type of aurora found on saturn resolves a planetary mystery\n--\nSample: online Shopping is ReSHaping Real-world Cities\nFixed: Online shopping is reshaping real-world cities\n--\nSample: When you close 100 TAbs AFter Finding THE SoluTion To A BuG\nFixed: When you close 100 tabs after finding the solution to a bug\n--\nSample: masteing DYNAmIC ProGrammING\nFixed: Mastering dynamic programming\n--\nSample: "+test_str+"\nFixed:"
response1 = co.generate(
  model='large',
  prompt=training_data,
  max_tokens=200,
  temperature=0.3,
  k=0,
  p=0.75,
  frequency_penalty=0,
  presence_penalty=0,
  stop_sequences=["--"],
  return_likelihoods='NONE')

fixed_str = response1.generations[0].text
print('Fixed Text:', fixed_str)


summary_training_data = "Passage: Is Wordle getting tougher to solve? Players seem to be convinced that the game has gotten harder in recent weeks ever since The New York Times bought it from developer Josh Wardle in late January. The Times has come forward and shared that this likely isn’t the case. That said, the NYT did mess with the back end code a bit, removing some offensive and sexual language, as well as some obscure words There is a viral thread claiming that a confirmation bias was at play. One Twitter user went so far as to claim the game has gone to “the dusty section of the dictionary” to find its latest words.\n\nTLDR: Wordle has not gotten more difficult to solve.\n--\nPassage: ArtificialIvan, a seven-year-old, London-based payment and expense management software company, has raised $190 million in Series C funding led by ARG Global, with participation from D9 Capital Group and Boulder Capital. Earlier backers also joined the round, including Hilton Group, Roxanne Capital, Paved Roads Ventures, Brook Partners, and Plato Capital.\n\nTLDR: ArtificialIvan has raised $190 million in Series C funding.\n--\nPassage: " + fixed_str +  "\n\nTLDR:"
response2 = co.generate( 
  model='large', 
  prompt=summary_training_data, 
  max_tokens=75, 
  temperature=0.3, 
  k=0, 
  p=1, 
  frequency_penalty=0, 
  presence_penalty=0, 
  stop_sequences=["--"], 
  return_likelihoods='NONE') 
print('Summary 1: {}'.format(response2.generations[0].text))
