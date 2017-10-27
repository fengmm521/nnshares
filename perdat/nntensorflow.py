#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-10-24 09:29:05
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import json

import tensorflow as tf

from numpy.random import RandomState

batch_size = 100

hidlayerCount = 300

def runNN(inport,outport,dats): #500,529

    
    datasize = len(dats)
    

    w1 = tf.Variable(tf.truncated_normal([inport,hidlayerCount],stddev = 0.1))
    b1 = tf.Variable(tf.zeros([hidlayerCount]))

    w2 = tf.Variable(tf.truncated_normal([hidlayerCount,outport]))
    b2 = tf.Variable(tf.zeros([outport]))

    x = tf.placeholder(tf.float32,[None,inport])

    keep_prob = tf.placeholder(tf.float32)

    hidden1 = tf.nn.relu(tf.matmul(x,w1) + b1)

    hidden1_drop = tf.nn.dropout(hidden1, keep_prob)

    y = tf.nn.softmax(tf.matmul(hidden1_drop,w2) + b2)

    y_ = tf.placeholder(tf.float32,[None,outport])


    cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y),reduction_indices=[1]))
    # cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y)))

    train_step = tf.train.GradientDescentOptimizer(0.1).minimize(cross_entropy)


    

    with tf.Session() as sess:
        init_op = tf.global_variables_initializer()
        sess.run(init_op)

        

        STEPS = 40000
        for i in range(STEPS):
            start = (i * batch_size) % datasize
            end = min(start + batch_size,datasize)

            batch_xtmps = dats[start:end]
            batch_xs = []
            batch_ys = []
            for d in batch_xtmps:
                tmpxs = []
                for xx in d[0]:
                    tmpxs +=xx
                batch_xs.append(tmpxs)
                tmpys = [float(yi) for yi in d[1]]
                batch_ys.append(tmpys)
            sess.run(train_step,feed_dict={x:batch_xs,y_:batch_ys,keep_prob:0.75})

            if i % 1000 == 0:

                tbatch_xs = []
                tbatch_ys = []

                for td in dats:
                    tmpxs2 = []
                    for xx2 in td[0]:
                        tmpxs2 += xx2
                    tbatch_xs.append(tmpxs2)
                    tmpys2 = [float(yi2) for yi2 in td[1]]
                    tbatch_ys.append(tmpys2)

                total_cross_entropy = sess.run(cross_entropy,feed_dict={x:tbatch_xs,y_:tbatch_ys,keep_prob:1.0})
                print "After %d training step(s),cross entropy on all data is %g"%(i,total_cross_entropy)

# batch_size = 8

# w1 = tf.Variable(tf.random_normal([2,3],stddev=1,seed=1))
# w2 = tf.Variable(tf.random_normal([3,2],stddev=1,seed=1))

# b1 = tf.Variable(tf.zeros([3]))
# b2 = tf.Variable(tf.zeros([2]))

# x = tf.placeholder(tf.float32,shape=(None,2),name='x-input')
# y_ = tf.placeholder(tf.float32,shape=(None,2),name='y-input')

# a = tf.matmul(x, w1) + b1
# y = tf.nn.softmax(tf.matmul(a,w2) + b2)

# cross_entropy = -tf.reduce_mean(tf.reduce_sum( y_ * tf.log(y)))
# train_step = tf.train.GradientDescentOptimizer(0.002).minimize(cross_entropy)

# #random data
# rdm = RandomState(1)
# dataset_size = 1280
# X = rdm.rand(dataset_size, 2)
# Y = [[int(x1+x2 < 1),int(x1+x2>=1)] for (x1,x2) in X]

# rdm2 = RandomState(1)
# Xc = rdm2.rand(10, 2)

# #tensorflow session
# with tf.Session() as sess:
#     init_op = tf.global_variables_initializer()
#     sess.run(init_op)
#     '''
#     w1 = [[-0.81131822,1.48459876,0.06532937]]
#             [-2.44270396,0.0992484,0.59122431]
#     w2 = [[-0.81131822],[1.48459876],[0.06532937]]

#     '''

#     STEPS = 50000
#     for i in range(STEPS):
#         start = (i * batch_size) % dataset_size
#         end = min(start + batch_size,dataset_size)
#         sess.run(train_step,feed_dict={x:X[start:end],y_:Y[start:end]})

#         if i % 1000 == 0:
#             total_cross_entropy = sess.run(cross_entropy,feed_dict={x:X,y_:Y})
#             print "After %d training step(s),cross entropy on all data is %g"%(i,total_cross_entropy)

#     print 'w1',sess.run(w1)
#     print 'w2',sess.run(w2)
#     for d in Xc:
#         xt = d
#         xtinput = tf.constant(xt,shape=[1,2],dtype=tf.float32)
#         a1 = tf.matmul(xtinput, w1) + b1
#         y1 = tf.nn.softmax(tf.matmul(a1,w2) + b2)
#         yt = sess.run(y1)
#         yout = 0
#         if yt[0][1] > 0.5:
#             yout = 1
#         print xt,yout,yt

def main():
    pass
    # f = open('/media/mage/000FBF7E00093795/linuxfiles/perdata/tmp100_7/SH600015.txt','r')

    f = open('tmp100_7/SZ002355.txt','r')

    ltxt = f.read()
    f.close()
    dats = json.loads(ltxt)
    percount = len(dats[0][0])*len(dats[0][0][0])
    lablecount = len(dats[0][1])

    print percount,lablecount

    runNN(percount, lablecount, dats)

if __name__ == '__main__':  
    main()
    # test()