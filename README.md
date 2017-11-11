# Trading cryptos

This is a poloniex bot based on PAMR strategy.
PAMR strategy explained : https://link.springer.com/article/10.1007/s10994-012-5281-z

## Using the bot

This is the latest version of the bot, so I didn't had time testing it a lot.
Be carefull, I don't say that the bot will win money, use it are your own risks and test it first on paper trading ! I use the script trading_past to back test the different algorithms I want to use.

* First you have to put a file named keys.data in this folder with your poloniex api keys (public on the first line, private on the second)
* Then you lanch the script init.py and it should trade for you, you have to have only bitcoins when starting the bot
* Wait and see your money disepear on Poloniex fees

## Futur improvements

I have a lot of trouble with poloniex fees because I wanted to make really fast trading (one trade every 10 minutes for instance)
Work can be done in optimizing the buy / sell functions


## Feedback

I'm interested in your feedback or in your corrections to this bot

## License

Feel free to reuse the code to make your own bots, if you want to share them with me then I'm interested
