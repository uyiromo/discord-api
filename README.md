# discord-api

## Initialize

```sh
virtualenv -p "python3.13" .venv
chmod +x .venv/bin/activate
source .venv/bin/activate
pip3 install -r requirements.txt
```

## cli

```sh
source .venv/bin/activate
./cli.py --channels-json ../channels.json --channel cli "test"
```

- `channels.json` format:

  ```json
  {
      "cli": {
          "chid": "<channel id of cli>",
          "token": "<token for discord bot>"
      }
  }
  ```

## smtpd

```sh
./install.sh
```
