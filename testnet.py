import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

filename_queue = tf.train.string_input_producer(['circle.png'])
reader = tf.WholeFileReader()
key, value = reader.read(filename_queue)

my_img = tf.image.decode_png(value)

init_op = tf.global_variables_initializer()
with tf.Session() as sess:
    sess.run(init_op)
    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord)
    image = my_img.eval()
    print(image.shape)
    plt.imshow(image)
    plt.show()
    
    coord.request_stop()
    coord.join(threads)
