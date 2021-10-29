# Multiprocessing-in-python
Created this demo to test the effectiveness of using Multithreading and Concurrency in python.
In the demo we download 100 images from XKCD comics. first using sequential download and the using Queue and Threadpool.
for sequential download it almost took 32s, with queues 12s, and with ThreadPool only 10 seconds.

Note: All the performance comes with an expense of cpu, so if your goal is to minimize cpu utilisation use queues else go for threadpool.
