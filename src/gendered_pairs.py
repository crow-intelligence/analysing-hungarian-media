from src.svd_algebra import *

a = SVDAlgebra("langmods")

# how to add artificially created vector to the embedding
t = a.U[a.vocabulary.index('nő')]
b1 = a.U[a.vocabulary.index('százalék')]
b2 = a.U[a.vocabulary.index('szám')]
b3 = a.U[a.vocabulary.index('növekedés')]
num = np.add(b1, b2, b3)
totest = np.subtract(t, num)
a.U = np.vstack((a.U, totest))

# def get_gendered_pairs(wd1, wd2):
#     """
#     Generates gendered pairs
#     Based on: http://realerthinks.com/implicit-biases-word-embeddings-methods/
#     """
#     DELTA = 1
#     gendered_pairs = []
#     idx1 = a.vocabulary.index(wd1)
#     idx2 = a.vocabulary.index(wd2)
#     wvec1 = a.U[idx1]
#     wvec2 = a.U[idx2]
#     ab = wvec1 - wvec2
#     for i, x in enumerate(a.U):
#         dist_xy = x - a.U[0:]
#         norms = np.linalg.norm(dist_xy, axis=1)
#         mask = norms > DELTA  # hide these
#         S = np.dot(dist_xy, ab)
#         S = np.ma.masked_array(S, mask=mask)
#         mx = S.max()
#         if mx > 0:
#             j = np.where(S == mx)[0][0]
#             gendered_pairs.append((a.vocabulary[i], a.vocabulary[j], S[j]))
#     gendered_pairs.sort(key=lambda s: s[2], reverse=True)
#     return gendered_pairs
#
# t = get_gendered_pairs("fiú", "lány")
# print(t)
