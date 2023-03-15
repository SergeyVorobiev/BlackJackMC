# MCBlackJack
 
The BJ rules are simple. Dealer stops at 17. Ace can be 1. Card deck replaces every game, and as it is not just a random number but a separate class it can be manageable. Bet is 1.

MC.py main() - to run brute force process. 

game_count1 - the count of games to brute force, default is 1 million.

greedy_factor - percentage of choosing only the best action, should not be 1 to avoid constantly using the wrong action because of first luck.

file_name - name of the file to save the result of brute forcing into ./blackjack/resources folder.

BlackJackEnv.py main() - actual playing to check the result.

Third party libraries such as graphics, pandas, sklearn... can be installed automatically via PyCharm or by using pip.

![BJTable](https://user-images.githubusercontent.com/17081096/225321795-aee16590-83b3-4dd2-a5ac-0e6c4587e879.jpg)

The table shows all possible combinations. 11 - 6 means that we have a sum of 11 and the visible dealer card is 6.

In the last row we can see that no matter what we do, if the dealer shows 11 we will lose more often than win. But it is still more appropriate to 'hit' than 'stick' up until 17 to decrease losses.

