# Relevant code begins on line 60
import numpy as np 
def parse_percent(x):
    return 0.01 * np.asarray(x if hasattr(x, "__len__") else [x, x, x, x, x], np.float64)
quality_names = ["common", "uncommon", "rare", "epic", "legendary"]
class Recycler:
    def __init__(self, quality, inputs):
        self.quality = parse_percent(quality)
        self.inputs = inputs
        self.loops = 30
        self.recovery_percent = 25 * 0.01
    def summarize(self):
        if len(self.inputs) == 0:
            print("\tA recycler is declared, but has no input rarities configured? Did you mean to do that?\n")
        else:
            print("\tThese output rarities will be re-rolled with a recycler:")
            for rarity in self.inputs:
                print("\t\t{0:10}   {1:10} % quality of recycler".format(
                quality_names[rarity-1], 
                self.quality[rarity-1] * 100.))
            print(" ")

class Assembler:
    def __init__(self, name, quality, productivity, recycler = None):
        self.name = name
        self.quality = parse_percent(quality)
        self.productivity = parse_percent(productivity)
        self.recycler = recycler
    def summarize(self, max_rarity):
        print("\n\t\t\t" + self.name + "\n")
        print("\tBonuses per input rarity are:")
        for rarity in range(max_rarity):
            print("\t\t{0:10}   {1:10} % quality   {2:10} % productivity".format(
                quality_names[rarity], 
                self.quality[rarity] * 100., 
                self.productivity[rarity] * 100.))
        print(" ")
def quality_module_bonus(tier, quality_of_module):
    LUT = [
        [1.0,  1.3,  1.6,  1.9,  2.5],
        [1.5,  1.9,  2.4,  2.8,  3.7],
        [2.5,  3.2,  4.0,  4.7,  6.2]]
    return LUT[tier-1][quality_of_module-1]
def productivity_module_bonus(tier, quality_of_module):
    LUT = [
        [ 4.0,  5.2,  6.4,  7.6, 10.0],
        [ 6.0,  7.8,  9.6, 11.4, 15.0],
        [10.0, 13.0, 16.0, 19.0, 25.0]]
    return LUT[tier-1][quality_of_module-1]
common = 1
uncommon = 2
rare = 3
epic = 4
legendary = 5

tier_1 = 1
tier_2 = 2
tier_3 = 3
#### IGNORE STUFF ABOVE, CHANGE STUFF BELOW

max_quality = epic
input_quality_distribution = [100, 0, 0, 0, 0]

production_chain = [
    Assembler(
        "Production Stage 1",
        4 * quality_module_bonus(tier_2, rare), 
        50, # intrinsic productivity bonus
        Recycler(
            4 * quality_module_bonus(tier_2, rare), 
            [uncommon]
        )
    ),
    Assembler(
        "Production Stage 2",
        [
            0,
            4 * quality_module_bonus(tier_1, common),
            4 * quality_module_bonus(tier_1, common),
            4 * quality_module_bonus(tier_1, common),
            4 * quality_module_bonus(tier_1, common)
        ], 
        [
            4 * productivity_module_bonus(tier_1, common),
            0,
            0,
            0,
            0
        ], 
        None
    )
]
    
#verbose = True
verbose = False

#### IMPLEMENTATION DETAILS BELOW
max_quality = max(1, min(max_quality, 5))
input_quality = np.asarray(input_quality_distribution, np.float64)
np.set_printoptions(suppress=True)

def transition_matrix(probabilities):
    matrix = np.identity(5) 
    
    for i in range(max_quality, 5):
        matrix[i,i] = 0.0
    
    for c in range(0, max_quality):
        q = 1
        p = probabilities[c]
        for r in range(c, max_quality):
            if r == max_quality - 1:
                matrix[r,c] = q
            else:
                matrix[r,c] = q * (1 - p)
                q *= p
                
    return matrix

print("The max rarity is set to " + quality_names[max_quality-1] + ".\n")


print("Distribution of input rarities:")
print(input_quality)
for machine in production_chain:
    machine.summarize(max_quality)
    #print("\n\t\t" + machine.name + "\n")
    matrix = transition_matrix(machine.quality)
    if verbose:
        print("Transition matrix of the assembler, before productivity:")
        print(matrix)
    for row in range(5):
        matrix[row] *= 1 + machine.productivity[row]
    if verbose:
        print("Transition matrix of the assembler, after productivity:")
        print(matrix)
    
    output_quality = matrix.dot(input_quality)
        
    if machine.recycler:
        recycler = machine.recycler
        recycler.summarize()

        if verbose:
            print("Distribution of output quality:")
            print(output_quality)

        recycler_matrix = transition_matrix(recycler.quality)
        recycler_matrix *= recycler.recovery_percent
        if verbose:
            print("Transition matrix for the recycler is:")
            print(recycler_matrix)
        
        if len(recycler.inputs):
            for loop in range(recycler.loops):
                if verbose:
                    print("\tRecycler loop " + str(1 + loop))
                recycler_input = 1.0 * np.array([0,0,0,0,0])
                for qual in recycler.inputs:
                    recycler_input[qual-1] = output_quality[qual-1]
                    output_quality[qual-1] = 0.
                if verbose:
                    print("Input to the recycler is:")
                    print(recycler_input)
                recycler_output = recycler_matrix.dot(recycler_input)
                if verbose:
                    print("Output from the recycler is:")
                    print(recycler_output)
    
                feedback = matrix.dot(recycler_output)
                if verbose:
                    print("Feedback to the assembler from the recycler:")
                    print(feedback)
                output_quality += feedback
                if verbose:
                    print("Output from the assembler so far")
                    print(output_quality)
            
            if verbose:
                print("\tAll recycler loops done")
                print("Total assembler output after all recycling loops:")
                print(output_quality)

    print("Distribution of output rarities:")
    print(output_quality)

    input_quality = output_quality

print("\nNote, output distribution might not sum to 100%, because of gains from productivity and loss from recyclers.")
