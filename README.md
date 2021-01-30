
Read `requirements.txt` for required `pip` packages

To download data, run `webscrape.py`
```
python webscrape.py
```

To train the TF model,
run `ml_tensorflow.py`
```
python ml_tensorflow.py
```
Alternatiely, you can run `webscrape.py` and use that data instead.

To run the discord bot, first generate a `.env` file. Then, paste in the following:
``` 
DISCORD_TOKEN = <YOUR-BOT-TOKEN-HERE>
BOT_PREFIX = '!'
```
where `<YOUR-BOT-TOKEN-HERE>` from the Discord Developer Portal after creating a bot. 
Then, run
```
python dc_bot.py
```
# egirl_detector_discord_bot
