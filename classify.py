def classify(train_features, train_labels, test_features):
    clf = svm.SVC(kernel='linear')
    clf.fit(train_features, train_labels)
    answer = clf.predict(test_features)

    return answer
    
def train(train_size):
    train_features = []
    test_features = []
    train_labels = []
    for genre in ['Rock/', 'Pop/', 'Falk/', 'Electronic/']:
        for i in range(1, train_size + 1):
            train_features.append(extract_hog(misc.imread(\
                genre + str(i) + ".jpg")))
            train_labels.append(genre[:-1])
            test_features.append(extract_hog(misc.imread(\
                genre + str(i + train_size) + ".jpg")))            
    
    ans = classify(train_features, train_labels, test_features)
  
