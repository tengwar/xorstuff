# ---------------------------------------------------------------
# Author: hellman ( hellman1908@gmail.com )
# License: GNU GPL v2 ( http://opensource.org/licenses/gpl-2.0.php )
# ---------------------------------------------------------------

from operator import itemgetter

class GuessKeyLength:

    def __init__(self):
        self.max_key_length = 16

    def guess_key_length(self, text):
        """Try key lengths from 1 to max_key_length and print local maximums.
           Set key_length to the most possible if it's not set by user.
        """
        fitnesses = self.calculate_fitnesses(text)
        self.fitnesses = fitnesses
        return self.get_max_fitnessed_key_length(fitnesses)


    def calculate_fitnesses(self, text):
        """ Calc. fitnesses for each keylen

        """
        prev = 0
        pprev = 0
        fitnesses = []
        for key_length in range(1,self.max_key_length + 1):
            fitness = self.count_equals(text, key_length)

            # smaller key-length with nearly the same fitness is preferable
            fitness = (float(fitness) /
                       (self.max_key_length + key_length ** 1.5))

            if pprev < prev and prev > fitness:  # local maximum
                fitnesses += [(key_length - 1, prev)]

            pprev = prev
            prev = fitness

        return fitnesses

    def calculate_fitness_sum(self, fitnesses):
        """Calculate sum of fitnesses

        """
        return sum([f[1] for f in fitnesses])


    def count_equals(self, text, key_length):
        """Count equal chars count for each offset and sum them

        """
        equals_count = 0
        if key_length >= len(text):
            return 0

        for offset in range(key_length):
            chars_count = self.chars_count_at_offset(text, key_length, offset)
            equals_count += max(chars_count.values()) - 1  # why -1? don't know
        return equals_count

    def get_max_fitnessed_key_length(self, fitnesses):
        """Get the most probable key length

        """
        max_fitness = 0
        max_fitnessed_key_length = 0
        for key_length, fitness in fitnesses:
            if fitness > max_fitness:
                max_fitness = fitness
                max_fitnessed_key_length = key_length
        return max_fitnessed_key_length


    def chars_count_at_offset(self, text, key_length, offset):
        """Get char count for given text, key length and offset

        """
        chars_count = dict()
        for pos in range(offset, len(text), key_length):
            c = text[pos]
            if c in chars_count:
                chars_count[c] += 1
            else:
                chars_count[c] = 1
        return chars_count

    def guess_and_print_divisors(self):
        """ Prints common divisors and returns the most common divisor

        """
        fitnesses = self.fitnesses
        divisors_counts = [0] * (self.max_key_length + 1)
        for key_length, fitness in fitnesses:
            for number in range(3, key_length + 1):
                if key_length % number == 0:
                    divisors_counts[number] += 1
        max_divisors = max(divisors_counts)

        limit = 3
        ret = 2
        for number, divisors_count in enumerate(divisors_counts):
            if divisors_count == max_divisors:
                ret = number
                limit -= 1
                if limit == 0:
                    return ret
        return ret

    def print_fitnesses(self):
        """Get fitnesses

        """
        # top sorted by fitness, but print sorted by length
        result = []
        fitnesses = self.fitnesses
        fitnesses.sort(key=itemgetter(1), reverse=True)
        top10 = fitnesses[:10]
        best_fitness = top10[0][1]
        top10.sort(key=itemgetter(0))

        fitness_sum = self.calculate_fitness_sum(top10)

        for key_length, fitness in top10:
            s1 = str(key_length)
            s2 = str(round(100 * fitness * 1.0 / fitness_sum, 1))
            result.append({'length' : s1, 'percents' : s2})
        return result

