from preprocess import preprocess

text = """"The thanks of a weak one are of but little value," he muttered, "but you have them, for truly, in 
this past week, little but scraps have come my way - and for all my body is small, yet is my 
appetite unseemly great." 

"Well, then, eat!" said Bayta, with a smile. "Don't waste your time on thanks. Isn't there a 
Central Galaxy proverb about gratitude that I once heard?" 

"Truly there is, my lady. For a wise man, I have been told, once said, 'Gratitude is best and 
most effective when it does not evaporate itself in empty phrases.' But alas, my lady, I am but a 
mass of empty phrases, it would seem. When my empty phrases pleased the Mule, it brought 
me a court dress, and a grand name - for, see you, it was originally simply Bobo, one that 
pleases him not - and then when my empty phrases pleased him not, it would bring upon my 
poor bones beatings and whippings." 

Toran entered from the pilot room, "Nothing to do now but wait, Bay. I hope the Mule is capable 
of understanding that a Foundation ship is Foundation territory." 

Magnifico Giganticus, once Bobo, opened his eyes wide and exclaimed, "How great is the 
Foundation before which even the cruel servants of the Mule tremble." 

"Have you heard of the Foundation, too?" asked Bayta, with a little smile."""


doc = preprocess(text)  # get the spaCy Doc (composed of Tokens)

print(doc._.coref_clusters)
# Result: [Eva and Martha: [Eva and Martha, their, they], Jenny: [Jenny, her]]

print(doc._.coref_resolved)
# Result: "Eva and Martha didn't want Eva and Martha friend Jenny to feel lonely so Eva and Martha invited Jenny to the party."


