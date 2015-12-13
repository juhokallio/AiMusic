from sklearn.ensemble import RandomForestClassifier
import math
from . music import extract_note_features, extract_notes_from_dict


def get_classifiers(compositions):
    X, Ys = get_training_data(compositions)
    clfs = {}
    for category in Ys:
        clf = RandomForestClassifier()
        clf.fit(X, Ys[category])
        clfs[category] = clf
    return clfs


def get_training_data(compositions):
    """ Extract training data from compositions
    :param compositions:
    :return:
    """
    X = []
    Ys = {}
    for composition in compositions:
        # TODO: One day, support for multiple critics
        critic_entity = composition.critics.first()
        if critic_entity is None:
            continue
        critic = critic_entity.critic
        notes = extract_notes_from_dict(composition.music)
        for i, note in enumerate(notes):
            history = notes[:i]
            X.append(extract_note_features(history, note))
            note_critic = critic[i]
            for t in Ys:
                Ys[t].append(1)
            if note_critic in Ys:
                Ys[t][-1] = 0
            else:
                Y = [1] * len(X)
                Y[-1] = 0
                Ys[note_critic] = [1] * len(X)
    return X, Ys


def classify(clf, notes):
    sum = 0.0
    for index, note in enumerate(notes):
        X = extract_note_features(notes[:index], note)
        sum += clf.predict_log_proba([X])[0][0]
    return sum - math.log2(len(notes))
