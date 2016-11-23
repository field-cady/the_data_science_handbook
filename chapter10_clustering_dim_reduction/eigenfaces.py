import sklearn
import sklearn.datasets as datasets
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, adjusted_rand_score
from sklearn import metrics

# Get data and format it
faces_data = datasets.fetch_olivetti_faces()
person_ids, image_array = faces_data['target'], faces_data.images
# unroll each 64x64 image -> (64*64) element vector
X = image_array.reshape((len(person_ids), 64*64))

# Cluster raw data and compare
print "** Results from raw data"
model = KMeans(n_clusters=40)
model.fit(X)
print "cluster goodness: ", silhouette_score(X, model.labels_)
print "match to faces: ", metrics.adjusted_rand_score(
    model.labels_, person_ids)  # 0.15338

# Use PCA to
print "** Now using PCA"
pca = PCA(25)  # pass in number of components to fit
pca.fit(X)
X_reduced = pca.transform(X)
model_reduced = KMeans(n_clusters=40)
model_reduced.fit(X_reduced)
labels_reduced = model_reduced.labels_
print "cluster goodness: ", \
    silhouette_score(X_reduced, model_reduced.labels_)
print "match to faces: ", metrics.adjusted_rand_score(
    model_reduced.labels_, person_ids)

	# Display a random face, to get a feel for the data
sample_face = image_array[0,:,:]
plt.imshow(sample_face)
plt.title("Sample face")
plt.show()
# Show eigenface 0
eigenface0 = pca.components_[0,:].reshape((64,64))
plt.imshow(eigenface0)
plt.title("Eigenface 0")
plt.show()
eigenface1 = pca.components_[1,:].reshape((64,64))
plt.imshow(eigenface1)
plt.title("Eigenface 1")
plt.show()
# Skree plot
pd.Series(
    pca.explained_variance_ratio_).plot()
plt.title("Skree Plot of Eigenface Importance")
plt.show()

