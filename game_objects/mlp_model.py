import tensorflow as tf
import numpy as np
from tf_utils import reset_graph, build_two_layers_mlp_inference


class TensorFlowMLP(object):
    def __init__(self, graph_method):
        reset_graph()
        self.graph_elements, self.tf_graph, self.saver = self.buildmlp()

    def buildmlp(self):
        reset_graph()
        with tf.Graph().as_default() as g:

            input_data = tf.placeholder(tf.float32, [None, (400 * 400)],
                                        name='input_data')
            #with tf.variable_scope('hidden1'):
            w1 = tf.Variable(tf.random_normal((400 * 400, 1000)),
                             name='w1')
            b1 = tf.Variable(np.zeros((1000,)),
                             name='b1', dtype=tf.float32)

            #with tf.variable_scope('hidden2'):
            w2 = tf.Variable(tf.random_normal((1000, 400)),
                             name='w2')
            b2 = tf.Variable(np.zeros((400,)),
                             name='b2', dtype=tf.float32)

            #with tf.variable_scope('output'):
            w_output = tf.Variable(tf.random_normal([400, 1]),
                                   name='w_output')
            b_output = tf.Variable(np.zeros((1,)), dtype=tf.float32)

            preactivation1 = tf.matmul(input_data, w1) + b1
            hidden1 = tf.nn.relu(preactivation1)

            preactivation2 = tf.matmul(hidden1, w2) + b2
            hidden2 = tf.nn.relu(preactivation2)

            output = tf.matmul(hidden2, w_output) + b_output
            saver = tf.train.Saver()
            return dict(input_data=input_data, w1=w1, output=output), g, saver

    def predict(self, data):
        if self.tf_graph is None:
            print("Initialize model first")
            raise TypeError
        inference_feed_dict = {self.graph_elements['input_data']: data}

        with tf.Session(graph=self.tf_graph) as sess:
            #saver = tf.train.import_meta_graph('./tf_pong.meta')
            #saver.restore(sess, './tf_pong')
            self.saver.restore(sess, "./tf_pong1.ckpt")
            print sess.run(self.graph_elements['w2'])
            raise Exception
            return sess.run(self.graph_elements['output'],
                            feed_dict=inference_feed_dict)


MLP_model = TensorFlowMLP(build_two_layers_mlp_inference)
