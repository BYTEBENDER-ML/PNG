from logic import *

rain = Symbol("rain") # it is raining.
hagrid = Symbol("hagrid") # harry visited hagrid.
dumbledore = Symbol("dumbledore") # harry visited dumbeldore.

sentence = And(rain, hagrid)

knowledge = And(
    Implication(Not(rain), hagrid),
    Or(hagrid,dumbledore),
    Not(And(hagrid,dumbledore)),
    dumbledore
)

print (model_check(knowledge,rain))
