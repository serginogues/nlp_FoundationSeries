from config import *

text = """The Mule said: "Since I felt it necessary to trace Channis, it was obvious I expect to gain 
something thereby. Since he went to the Second Foundation with a startling speed and 
directness, we can reasonably assume that that was what I was expecting to happen. Since I 
did not gain the knowledge from him directly, something must have been preventing me. Those 
are the facts. Channis, of course, knows the answer. So do I. Do you see it, Pritcher?" """
print(predictor.coref_resolved(text))



