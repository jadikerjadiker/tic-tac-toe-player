import pickle
a = range(10)
b = range(5)

with open("yo.pkl", 'wb') as f:
    pickle.dump(a, f, pickle.HIGHEST_PROTOCOL)
with open("yo.pkl", 'wb') as f:
    pickle.dump(b, f, pickle.HIGHEST_PROTOCOL)
  
with open("yo.pkl", 'rb') as f:
    print(pickle.load(f))