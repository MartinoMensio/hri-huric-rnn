import random
import sys
import os
import json
import tensorflow as tf
from tensorflow.python import debug as tf_debug
import numpy as np

from . import data
from .model import Model
from . import metrics

# embedding size for labels
embedding_size = 64
# size of LSTM cells
hidden_size = 100
# size of batch
batch_size = 16
# number of training epochs
epoch_num = 50

MY_PATH = os.path.dirname(os.path.abspath(__file__))

DATASET = os.environ.get('DATASET', 'atis')
OUTPUT_FOLDER = os.environ.get('OUTPUT_FOLDER', 'last')
MODE = os.environ.get('MODE', None)

def get_model(vocabs, tokenizer, language, input_steps):
    model = Model(input_steps, embedding_size, hidden_size, vocabs, None)
    model.build(tokenizer, language)
    return model


def train(mode):
    # maximum length of sentences
    input_steps = 50
    print(mode)
    # load the train and dev datasets
    test_data, train_data = data.load_data(DATASET, mode)
    # fix the random seeds
    random_seed_init(len(train_data['data']))
    # preprocess them to list of training/test samples
    # a sample is made up of a tuple that contains
    # - an input sentence (list of words --> strings, padded)
    # - the real length of the sentence (int) to be able to recognize padding
    # - an output sequence (list of IOB annotations --> strings, padded)
    # - an output intent (string)
    training_samples = data.adjust_sequences(train_data)
    print('train samples', len(training_samples['data']))
    if test_data:
        test_samples = data.adjust_sequences(test_data)
        print('test samples', len(test_samples['data']))
    # get the vocabularies for input, slot and intent
    vocabs = data.get_vocabularies(training_samples)
    # and get the model
    model = get_model(vocabs, training_samples['meta']['tokenizer'], training_samples['meta']['language'], input_steps)
    global_init_op = tf.global_variables_initializer()
    table_init_op = tf.tables_initializer()
    saver = tf.train.Saver()
    sess = tf.Session()
    
    # initialize the required parameters
    sess.run(global_init_op)
    sess.run(table_init_op)

    # initialize the history that will collect some measures
    history = {
        'intent': np.zeros((epoch_num)),
        'slot': np.zeros((epoch_num))
    }
    for epoch in range(epoch_num):
        mean_loss = 0.0
        train_loss = 0.0
        for i, batch in enumerate(data.get_batch(batch_size, training_samples['data'])):
            # perform a batch of training
            _, loss, decoder_prediction, intent, mask = model.step(sess, "train", batch)
            mean_loss += loss
            train_loss += loss
            if i % 10 == 0:
                if i > 0:
                    mean_loss = mean_loss / 10.0
                #print('Average train loss at epoch %d, step %d: %f' % (epoch, i, mean_loss))
                print('.', end='')
                sys.stdout.flush()
                mean_loss = 0
        train_loss /= (i + 1)
        print("[Epoch {}] Average train loss: {}".format(epoch, train_loss))

        if test_data:
            # test each epoch once
            pred_slots = []
            pred_intents = []
            true_intents = []
            for j, batch in enumerate(data.get_batch(batch_size, test_samples['data'])):
                decoder_prediction, intent = model.step(sess, "test", batch)
                # from time-major matrix to sample-major
                decoder_prediction = np.transpose(decoder_prediction, [1, 0])
                if j == 0:
                    index = random.choice(range(len(batch)))
                    # index = 0
                    print("Input Sentence        : ", batch[index]['words'][:batch[index]['length']])
                    print("Slot Truth            : ", batch[index]['slots'][:batch[index]['length']])
                    print("Slot Prediction       : ", decoder_prediction[index][:batch[index]['length']])
                    print("Intent Truth          : ", batch[index]['intent'])
                    print("Intent Prediction     : ", intent[index])
                slot_pred_length = list(np.shape(decoder_prediction))[1]
                pred_padded = np.lib.pad(decoder_prediction, ((0, 0), (0, input_steps-slot_pred_length)),
                                        mode="constant", constant_values=0)
                pred_slots.append(pred_padded)
                #print("pred_intents", pred_intents, "intent", intent)
                pred_intents.extend(intent)
                true_intent = [sample['intent'] for sample in batch]
                true_intents.extend(true_intent)
                #print("true_intents", true_intents)
                # print("slot_pred_length: ", slot_pred_length)
                true_slot = np.array([sample['slots'] for sample in batch])
                true_length = np.array([sample['length'] for sample in batch])
                true_slot = true_slot[:, :slot_pred_length]
                # print(np.shape(true_slot), np.shape(decoder_prediction))
                # print(true_slot, decoder_prediction)
                slot_acc = metrics.accuracy_score(true_slot, decoder_prediction, true_length)
                intent_acc = metrics.accuracy_score(true_intent, intent)
                print('.', end='')
                sys.stdout.flush()
                #print("slot accuracy: {}, intent accuracy: {}".format(slot_acc, intent_acc))
            pred_slots_a = np.vstack(pred_slots)
            # print("pred_slots_a: ", pred_slots_a.shape)
            true_slots_a = np.array([sample['slots'] for sample in test_samples['data']])[:pred_slots_a.shape[0]]
            f1_intents = metrics.f1_for_intents(pred_intents, true_intents)
            f1_slots = metrics.f1_for_sequence_batch(true_slots_a, pred_slots_a)
            # print("true_slots_a: ", true_slots_a.shape)
            print('epoch {} ended'.format(epoch))
            print("F1 score SEQUENCE for epoch {}: {}".format(epoch, f1_slots))
            print("F1 score INTENTS for epoch {}: {}".format(epoch, f1_intents))
            history['intent'][epoch] = f1_intents
            history['slot'][epoch] = f1_slots

    real_folder = MY_PATH + '/results/' + OUTPUT_FOLDER + '/' + DATASET + '/'
    if not os.path.exists(real_folder):
        os.makedirs(real_folder)
    
    if test_data:
        metrics.plot_f1_history(real_folder + 'f1.png', history)
        save_history(history, real_folder + 'history.json')
    else:
        saver = tf.train.Saver()
        saver.save(sess, real_folder + 'model.ckpt')



def random_seed_init(seed):
    random.seed(seed)
    tf.set_random_seed(seed)

def save_history(history, file_path):
    history_serializable = {k:v.tolist() for k,v in history.items()}
    with open(file_path, 'w') as out_file:
        json.dump(history_serializable, out_file)

if __name__ == '__main__':
    # for those two datasets, default to train full
    if (DATASET == 'wit_en' or DATASET == 'wit_it') and not MODE:
        #train('measures') # not possible until reset py_func (2 declared)
        train('runtime')
    else:
        if not MODE:
            MODE = 'measures'
        train(MODE)