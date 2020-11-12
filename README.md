![Python application](https://github.com/mattermat/async-redis-infinite-context/workflows/Python%20application/badge.svg)

# async-redis-infinite-context

### TODO
Actually, through Stream.stop() it is possible to exit the context loop.
However, since Stream.stop isn't async, it can be called internally after a new
element is caught by the data stream.
So we need a solution to stop the loop in the extact moment the function is
called.
