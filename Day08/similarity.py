from sentence_transformers import util, SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
sentences = [
    "I love playing football",
    "I enjoy playing soccer",
    "I like eating pizza",
    #"I love programming in Python",
    #"Python is a great programming language",
    #"I enjoy solving problems with code",
]
sentence_embeddings = model.encode(sentences)
similarity1 = util.cos_sim(sentence_embeddings[0], sentence_embeddings[1])
similarity3 = util.cos_sim(sentence_embeddings[1], sentence_embeddings[2])
print(similarity1.item())
print(similarity3.item())