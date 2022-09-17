import cohere
co = cohere.Client('dG9FO5NCPecnNjWtiSGAlXmQf3qbkVkBGX2krkBg')
response = co.generate(
  model='large',
  prompt='This is a spell check generator that fixes samples of text.\n\nSample: a new type OF aurora FounD on saturn resolves a planetary mystery\nFixed: A new type of aurora found on saturn resolves a planetary mystery\n--\nSample: online Shopping is ReSHaping Real-world Cities\nFixed: Online shopping is reshaping real-world cities\n--\nSample: When you close 100 TAbs AFter Finding THE SoluTion To A BuG\nFixed: When you close 100 tabs after finding the solution to a bug\n--\nSample: masteing DYNAmIC ProGrammING\nFixed: Mastering dynamic programming\n--\nSample: LET\'S ALL WORK TOGETHER TO KEP OUR LOUNGE CLEAN ! PLEASE CLEAN UP AFTER YOURSELF BEFORE LAVING THE LOUNGE . Thank you for your co - opertion\nFixed: ',
  max_tokens=50,
  temperature=0.3,
  k=0,
  p=0.75,
  frequency_penalty=0,
  presence_penalty=0,
  stop_sequences=["--"],
  return_likelihoods='NONE')
print('Prediction: {}'.format(response.generations[0].text))