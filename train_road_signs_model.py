#!/usr/bin/python3.9
import numpy as np
import os
import sys

print("version", sys.version)
print("cwd",)

from os import listdir
print(listdir(os.getcwd()))

from tflite_model_maker.config import ExportFormat
from tflite_model_maker import model_spec
from tflite_model_maker import object_detector

import tensorflow as tf
assert tf.__version__.startswith('2')

from split_dataset import split_dataset

dataset_is_split = False

label_map = {
    1: 'duck_regular',
    2: 'duck_specialty',
    3: 'sign_stop',
    4: 'sign_oneway_right',
    5: 'sign_oneway_left',
    6: 'sign_noentry',
    7: 'sign_yield',
    8: 'road_crosswalk',
    9: 'road_oneway',
    10: 'vehicle'
}

images_in = '/content/dataset/images'
annotations_in = '/content/dataset/annotations'

train_dir, val_dir, test_dir = split_dataset(images_in, annotations_in,
                                              val_split=0.2, test_split=0.2,
                                              out_path='split-dataset')

train_data = object_detector.DataLoader.from_pascal_voc(
    os.path.join(train_dir, 'images'),
    os.path.join(train_dir, 'annotations'), label_map=label_map)
validation_data = object_detector.DataLoader.from_pascal_voc(
    os.path.join(val_dir, 'images'),
    os.path.join(val_dir, 'annotations'), label_map=label_map)
test_data = object_detector.DataLoader.from_pascal_voc(
    os.path.join(test_dir, 'images'),
    os.path.join(test_dir, 'annotations'), label_map=label_map)

print(f'train count:      {len(train_data)}')
print(f'validation count: {len(validation_data)}')
print(f'test count:       {len(test_data)}')

spec = object_detector.EfficientDetLite0Spec()

model = object_detector.create(train_data=train_data,
                               model_spec=spec,
                               validation_data=validation_data,
                               epochs=50,
                               batch_size=10,
                               train_whole_model=True)

print('Evaluating model on test data.')
results = model.evaluate(test_data)
print("model evaluation results: ")
print(results)


TFLITE_FILENAME = 'efficientdet-lite-road-signs_edgetpu.tflite'
LABELS_FILENAME = 'road-signs-labels.txt'

model.export(export_dir='.', tflite_filename=TFLITE_FILENAME, label_filename=LABELS_FILENAME,
             export_format=[ExportFormat.EDGETPU, ExportFormat.LABEL])

print('Evaluating tflite model on test data.')
results = model.evaluate_tflite(TFLITE_FILENAME, test_data)
print("tflite model evaluation results: ")
print(results)