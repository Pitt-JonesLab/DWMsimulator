from scipy.special import comb
import config as config
# Input values
numBits = config.numBits
max_fault = config.max_fault
R = config.R
p_extreme = config.P_extreme

def calculate_probability(extremes):
    total_bits = numBits
    probability_list = [0] * (max_fault + 1)

    for f in range(max_fault + 1):
        # Probability for no increase in count
        no_fault_prob = (1 - R) ** (total_bits - f)

        # Probability for increase in count
        fault_prob = R ** f

        half_prob_effect = 0
        chance_occurrence = []
        for k in range(min(extremes, f) + 1):
            percent_effect = comb(extremes, k) * (p_extreme ** k) * comb(total_bits - extremes, f - k) / comb(total_bits, f)
            half_prob_effect += percent_effect
            chance_occurrence.append(percent_effect)
        # Calculate probabilities for extreme cases

        probability_list[f] = comb(total_bits, f) * no_fault_prob * fault_prob * half_prob_effect
        if 0 < f <= extremes:
            for past in range(f):
                probability_list[past] += chance_occurrence[len(chance_occurrence) - 1 - past] * probability_list[f]

    return probability_list



