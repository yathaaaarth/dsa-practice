# Question link -> https://leetcode.com/problems/time-needed-to-buy-tickets

class Solution:
    def timeRequiredToBuy(self, tickets: List[int], k: int) -> int:
        result = 0
        for i in range(len(tickets)):
            if i <= k:
                # Person i stands at or before k in the queue, so they get a turn in every
                # round that k gets a turn: they buy min(their need, k's need) tickets.
                result += min(tickets[i], tickets[k])
            else:
                # Person i stands AFTER k. On k's final round the loop ends the moment k
                # buys their last ticket, so person i never gets that final turn -- they
                # take part in only tickets[k] - 1 rounds.
                # FIX: the old code added tickets[i] whenever tickets[i] <= tickets[k],
                # which over-counted by 1 for every i > k with tickets[i] == tickets[k].
                # e.g. [2,2], k=0 returned 4; the correct answer is 3.
                result += min(tickets[i], tickets[k] - 1)
        return result
