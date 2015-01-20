1) The current state machine doesn't handle the case which GOODBYE signal can come anytime.
	It will get delayed to the next input cycle. SOLUTION: constantly checking for packet when there are no input
2)Need some way to notify the client closed

3)queue.join() blocks if I put it inside the class///If I put it in main, the thread won't wait for message

4)do not always fire a timer.