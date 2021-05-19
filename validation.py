"""
If there is no such data set (e.g. you use a book): create a
validation set by manually validating a small random subset
(50-100 data points).
Do this with different judges (ask friends or family for help) and calculate kappa distance.
About Kappa: https://stats.stackexchange.com/questions/82162/cohens-kappa-in-plain-english
"""

DATASET = ["""The mayor chuckled. "Got in first, did you? All right. By the way," he observed, and added 
softly, "Ambassador Verisof is returning to Terminus. Temporarily, I hope." 

There was a short silence, faintly horrified, and then Lee said, "Was that the message? Are 
things breaking already?" 

"Don't know. I can't tell till I hear what Verisof has to say. They may be, though. After all, they 
have to before election. But what are you looking so dead about?" 

"Because I don't know how it's going to turn out. You're too deep, Hardin, and you're playing 
the game too close to your chest." 

"Even you?" murmured Hardin. And aloud, "Does that mean you're going to join Sermak's new 
party?" 

Lee smiled against his will. "All right. You win. How about lunch now?" """,
           ]
