## Secret Christmas angel

It is an issue for us all to automate the Christmas angel this year due to COVID-19. This application let's you add the names of your family members with whom you wish to exchange gifts and sends out automated emails with the name of a random other family member.

## Usage

Set-up an app password fro Gmail if you have two-step authentication enabled outherwise just add your password in a `config.json` file:

```json
{
  "authmail": "<your-gmail-address>",
  "authpath": "<your-app-oauth2-file-:-it-is-generated-if-the-file-does-not-exist>",
  "recipients": [
    {
      "mail": "recipient@1.com",
      "name": "recipient1" // This name will be used in the mail!
    },
    // ...
    {
      "mail": "recipient@2.com",
      "name": "recipient2"
    }
  ]
}
```

## Dependencies

`yagmail` and you should install the pdf renderer. Currently the setup only works on Linux.

```bash
python3 -m venv christmas
source christmas/bin/activate
pip install -r requirements.txt
sudo apt-get install wkhtmltopdf
```

## Usage

If you have everything setup (`config.json`) you should just choose the language and send out your emails to your loved ones.

```bash
python christmas_angel.py --language hu\ # by default this is set to English
                          --config_name config.json # required but can be named differently
```

## @Regards, Alex
